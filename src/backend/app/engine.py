import asyncio
import logging
import os
import uuid
from functools import lru_cache
from typing import AsyncGenerator, Iterable

from vllm import AsyncLLMEngine, EngineArgs, SamplingParams

logger = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("VLLM_MODEL", "facebook/opt-125m")
DEFAULT_MAX_TOKENS = int(os.getenv("VLLM_MAX_TOKENS", "512"))
DEFAULT_TEMPERATURE = float(os.getenv("VLLM_TEMPERATURE", "0.7"))
_stop_env = os.getenv("VLLM_STOP")
if _stop_env:
    STOP_SEQUENCES: Iterable[str] = tuple(s.strip() for s in _stop_env.split(",") if s.strip())
else:
    STOP_SEQUENCES = ("\nUser:", "\nSystem:")


@lru_cache()
def get_engine() -> AsyncLLMEngine:
    """Create (or fetch cached) vLLM engine instance."""
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


def build_prompt(messages: Iterable[dict], persona: str | None = None) -> str:
    """Convert chat-style messages to a single text prompt."""
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


def sampling_params_from_request(
    max_tokens: int | None = None,
    temperature: float | None = None,
) -> SamplingParams:
    return SamplingParams(
        max_tokens=max_tokens or DEFAULT_MAX_TOKENS,
        temperature=temperature if temperature is not None else DEFAULT_TEMPERATURE,
        stop=STOP_SEQUENCES,
    )


async def stream_generate(
    messages: Iterable[dict],
    sampling_params: SamplingParams,
    persona: str | None = None,
) -> AsyncGenerator[str, None]:
    """Yield completion text chunks for the given conversation."""
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


async def complete(
    messages: Iterable[dict],
    sampling_params: SamplingParams,
    persona: str | None = None,
) -> str:
    """Return a full completion string without streaming."""
    chunks: list[str] = []
    async for chunk in stream_generate(messages, sampling_params, persona=persona):
        chunks.append(chunk)
    return "".join(chunks)
