import asyncio
import json
import logging
import os
import uuid
from functools import lru_cache
from typing import AsyncGenerator, Iterable, Optional

import httpx
from vllm import AsyncLLMEngine, EngineArgs, SamplingParams

logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("VLLM_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")
DEFAULT_MAX_TOKENS = int(os.getenv("VLLM_MAX_TOKENS", "512"))
DEFAULT_TEMPERATURE = float(os.getenv("VLLM_TEMPERATURE", "0.7"))
SERVE_URL = os.getenv("VLLM_SERVE_URL", "").rstrip("/")
SERVE_MODEL = os.getenv("VLLM_SERVE_MODEL", DEFAULT_MODEL)
SERVE_API_KEY = os.getenv("VLLM_API_KEY")

_stop_env = os.getenv("VLLM_STOP")
if _stop_env:
    STOP_SEQUENCES: Iterable[str] = tuple(s.strip() for s in _stop_env.split(",") if s.strip())
else:
    STOP_SEQUENCES = ("\nUser:", "\nSystem:")

USE_REMOTE_SERVE = bool(SERVE_URL)


@lru_cache()
def get_engine() -> AsyncLLMEngine:
    if USE_REMOTE_SERVE:
        raise RuntimeError("Local engine is disabled when VLLM_SERVE_URL is provided.")

    model = DEFAULT_MODEL
    if not model:
        raise RuntimeError("VLLM_MODEL environment variable must be set")

    engine_args = EngineArgs(
        model=model,
        tensor_parallel_size=int(os.getenv("VLLM_TENSOR_PARALLEL_SIZE", "1")),
        pipeline_parallel_size=int(os.getenv("VLLM_PIPELINE_PARALLEL_SIZE", "1")),
        dtype=os.getenv("VLLM_DTYPE", "auto"),
        download_dir=os.getenv("VLLM_DOWNLOAD_DIR"),
    )
    logger.info("Loading vLLM engine for model %s", model)
    return AsyncLLMEngine.from_engine_args(engine_args)


def sampling_params_from_request(
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
) -> SamplingParams:
    return SamplingParams(
        max_tokens=max_tokens or DEFAULT_MAX_TOKENS,
        temperature=temperature if temperature is not None else DEFAULT_TEMPERATURE,
        stop=STOP_SEQUENCES,
    )


async def _remote_stream_generate(
    messages: Iterable[dict],
    sampling_params: SamplingParams,
    persona: Optional[str] = None,
) -> AsyncGenerator[str, None]:
    if not SERVE_URL:
        raise RuntimeError("VLLM_SERVE_URL must be set to use remote vllm serve mode.")

    url = f"{SERVE_URL}/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    if SERVE_API_KEY:
        headers["Authorization"] = f"Bearer {SERVE_API_KEY}"

    request_body = {
        "model": SERVE_MODEL,
        "messages": list(messages),
        "stream": True,
        "max_tokens": sampling_params.max_tokens,
        "temperature": sampling_params.temperature,
    }
    if STOP_SEQUENCES:
        request_body["stop"] = list(STOP_SEQUENCES)
    if persona:
        request_body.setdefault("metadata", {})["persona"] = persona

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", url, headers=headers, json=request_body) as response:
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                text = await response.aread()
                logger.error("vLLM serve returned error %s: %s", exc.response.status_code, text)
                raise

            async for line in response.aiter_lines():
                if not line:
                    continue
                if not line.startswith("data: "):
                    continue
                data = line[6:].strip()
                if data == "[DONE]":
                    break
                try:
                    payload = json.loads(data)
                except json.JSONDecodeError:
                    logger.warning("Failed to decode streaming payload: %s", data)
                    continue
                choices = payload.get("choices", [])
                if not choices:
                    continue
                delta = choices[0].get("delta", {})
                text_delta = delta.get("content")
                if text_delta:
                    yield text_delta


async def _remote_complete(
    messages: Iterable[dict],
    sampling_params: SamplingParams,
    persona: Optional[str] = None,
) -> str:
    if not SERVE_URL:
        raise RuntimeError("VLLM_SERVE_URL must be set to use remote vllm serve mode.")

    url = f"{SERVE_URL}/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    if SERVE_API_KEY:
        headers["Authorization"] = f"Bearer {SERVE_API_KEY}"

    request_body = {
        "model": SERVE_MODEL,
        "messages": list(messages),
        "stream": False,
        "max_tokens": sampling_params.max_tokens,
        "temperature": sampling_params.temperature,
    }
    if STOP_SEQUENCES:
        request_body["stop"] = list(STOP_SEQUENCES)
    if persona:
        request_body.setdefault("metadata", {})["persona"] = persona

    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(url, headers=headers, json=request_body)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error("vLLM serve returned error %s: %s", exc.response.status_code, response.text)
            raise

    payload = response.json()
    text_chunks: list[str] = []
    for choice in payload.get("choices", []):
        message = choice.get("message", {})
        content = message.get("content")
        if content:
            text_chunks.append(content)
    return "".join(text_chunks)


def build_prompt(messages: Iterable[dict], persona: Optional[str] = None) -> str:
    role_labels = {
        "system": "System",
        "user": "User",
        "assistant": "Assistant",
    }

    lines: list[str] = []
    if persona:
        lines.append(f"Persona: {persona}")

    for message in messages:
        role = message.get("role", "user").lower()
        label = role_labels.get(role, role.capitalize())
        content = message.get("content", "").strip()
        if not content:
            continue
        lines.append(f"{label}: {content}")

    lines.append("Assistant:")
    return "\n".join(lines)


async def _local_stream_generate(
    messages: Iterable[dict],
    sampling_params: SamplingParams,
    persona: Optional[str] = None,
) -> AsyncGenerator[str, None]:
    engine = get_engine()
    prompt = build_prompt(messages, persona=persona)
    request_id = str(uuid.uuid4())

    await engine.add_request(
        request_id=request_id,
        prompt=prompt,
        sampling_params=sampling_params,
    )

    previous_text = ""
    try:
        async for request_output in engine.get_request_stream(request_id):
            if not request_output.outputs:
                continue
            current_text = request_output.outputs[0].text
            if not current_text:
                continue
            delta = current_text[len(previous_text) :]
            previous_text = current_text
            if delta:
                yield delta
    except asyncio.CancelledError:
        await engine.abort_request(request_id)
        raise
    except Exception:
        logger.exception("Error during vLLM generation; aborting request %s", request_id)
        await engine.abort_request(request_id)
        raise


async def _local_complete(
    messages: Iterable[dict],
    sampling_params: SamplingParams,
    persona: Optional[str] = None,
) -> str:
    chunks: list[str] = []
    async for chunk in _local_stream_generate(messages, sampling_params, persona=persona):
        chunks.append(chunk)
    return "".join(chunks)


async def stream_generate(
    messages: Iterable[dict],
    sampling_params: SamplingParams,
    persona: Optional[str] = None,
) -> AsyncGenerator[str, None]:
    if USE_REMOTE_SERVE:
        async for item in _remote_stream_generate(messages, sampling_params, persona=persona):
            yield item
        return

    async for item in _local_stream_generate(messages, sampling_params, persona=persona):
        yield item


async def complete(
    messages: Iterable[dict],
    sampling_params: SamplingParams,
    persona: Optional[str] = None,
) -> str:
    if USE_REMOTE_SERVE:
        return await _remote_complete(messages, sampling_params, persona=persona)

    return await _local_complete(messages, sampling_params, persona=persona)
