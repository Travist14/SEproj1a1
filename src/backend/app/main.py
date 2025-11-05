"""FastAPI application for chat completions powered by vLLM."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import uuid
from typing import AsyncIterator, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field, field_validator

try:
    from vllm import AsyncEngineArgs, AsyncLLMEngine
    from vllm.sampling_params import SamplingParams
except Exception as exc:  # pragma: no cover - informative import guard.
    AsyncEngineArgs = None  # type: ignore[assignment]
    AsyncLLMEngine = None  # type: ignore[assignment]
    SamplingParams = None  # type: ignore[assignment]
    _IMPORT_EXCEPTION = exc
else:
    _IMPORT_EXCEPTION = None

LOGGER = logging.getLogger(__name__)

MODEL_ENV_VAR = "VLLM_MODEL"
DEFAULT_MODEL_ID = "Qwen/Qwen3-4B"
DEFAULT_MAX_TOKENS = int(os.getenv("VLLM_MAX_TOKENS", "512"))
DEFAULT_TOP_P = float(os.getenv("VLLM_TOP_P", "0.95"))
DEFAULT_TEMPERATURE = float(os.getenv("VLLM_TEMPERATURE", "0.7"))


class ChatMessage(BaseModel):
    """Single message exchanged in the chat conversation."""

    role: str = Field(..., description="The role of the message author (system|user|assistant).")
    content: str = Field(..., description="The text content for this message.")

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        allowed = {"system", "user", "assistant"}
        if value not in allowed:
            raise ValueError(f"role must be one of {sorted(allowed)}")
        return value


class GenerateRequest(BaseModel):
    """Request payload for the /generate endpoint."""

    messages: List[ChatMessage] = Field(..., description="Ordered list of chat messages.")
    stream: bool = Field(default=True, description="Whether to stream tokens as they are generated.")
    max_tokens: int = Field(default=DEFAULT_MAX_TOKENS, ge=1, description="Maximum new tokens to sample.")
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE, ge=0.0, le=2.0, description="Sampling temperature."
    )
    top_p: float = Field(default=DEFAULT_TOP_P, ge=0.0, le=1.0, description=" nucleus sampling threshold.")
    presence_penalty: float = Field(
        default=0.0, ge=-2.0, le=2.0, description="Presence penalty following OpenAI semantics."
    )
    frequency_penalty: float = Field(
        default=0.0, ge=-2.0, le=2.0, description="Frequency penalty following OpenAI semantics."
    )
    stop: Optional[List[str]] = Field(
        default=None, description="Optional list of strings that will terminate generation."
    )
    persona: Optional[str] = Field(
        default=None,
        description="Optional persona identifier forwarded by the frontend. Currently informational only.",
    )


class EngineManager:
    """Lazy-initialises and caches a single AsyncLLMEngine instance."""

    def __init__(self) -> None:
        self._engine: Optional[AsyncLLMEngine] = None
        self._lock = asyncio.Lock()

    @property
    def is_ready(self) -> bool:
        return self._engine is not None

    async def get_engine(self) -> AsyncLLMEngine:
        if AsyncLLMEngine is None or AsyncEngineArgs is None or SamplingParams is None:
            raise RuntimeError("vLLM is not available") from _IMPORT_EXCEPTION

        if self._engine is not None:
            return self._engine

        async with self._lock:
            if self._engine is not None:
                return self._engine

            env_model_id = os.getenv(MODEL_ENV_VAR)
            model_id = env_model_id or DEFAULT_MODEL_ID
            if not env_model_id:
                LOGGER.info(
                    "Environment variable %s not set; defaulting to '%s'",
                    MODEL_ENV_VAR,
                    DEFAULT_MODEL_ID,
                )

            engine_args = AsyncEngineArgs(
                model=model_id,
                trust_remote_code=os.getenv("VLLM_TRUST_REMOTE_CODE", "false").lower() == "true",
                tensor_parallel_size=int(os.getenv("VLLM_TENSOR_PARALLEL_SIZE", "1")),
                max_model_len=int(os.getenv("VLLM_MAX_MODEL_LEN", "4096")),
            )
            LOGGER.info("Initialising vLLM engine with model '%s'", model_id)
            self._engine = AsyncLLMEngine.from_engine_args(engine_args)
            return self._engine


engine_manager = EngineManager()

app = FastAPI(title="SEproj Chat Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("BACKEND_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def format_chat_prompt(messages: List[ChatMessage]) -> str:
    """Convert structured chat messages into a plain-text prompt."""
    if not messages:
        raise ValueError("At least one message is required.")

    prompt_segments: List[str] = []
    for message in messages:
        role = message.role.capitalize()
        content = message.content.strip()
        prompt_segments.append(f"{role}: {content}")

    # Ensure the model continues the assistant turn.
    prompt_segments.append("Assistant:")
    return "\n\n".join(prompt_segments)


def build_sampling_params(payload: GenerateRequest) -> SamplingParams:
    """Create sampling parameters for vLLM from the request payload."""
    return SamplingParams(
        n=1,
        best_of=1,
        max_tokens=payload.max_tokens,
        temperature=payload.temperature,
        top_p=payload.top_p,
        presence_penalty=payload.presence_penalty,
        frequency_penalty=payload.frequency_penalty,
        stop=payload.stop,
    )


async def iterate_generation(
    prompt: str,
    sampling_params: SamplingParams,
    request_id: str,
) -> AsyncIterator[bytes]:
    """Stream generation results in an NDJSON format."""
    engine = await engine_manager.get_engine()

    previous_text = ""
    last_generation = None

    try:
        async for request_output in engine.generate(
            prompt=prompt,
            sampling_params=sampling_params,
            request_id=request_id,
        ):
            if not request_output.outputs:
                continue

            generation = request_output.outputs[0]
            text = generation.text
            delta = text[len(previous_text) :]
            last_generation = generation
            if delta:
                previous_text = text
                LOGGER.debug("Streaming token chunk: %s", delta)
                yield json.dumps(
                    {
                        "type": "token",
                        "delta": delta,
                        "content": text,
                        "request_id": request_id,
                    }
                ).encode("utf-8") + b"\n"

        finish_reason = getattr(last_generation, "finish_reason", None)
        yield json.dumps(
            {
                "type": "done",
                "content": previous_text,
                "finish_reason": finish_reason,
                "request_id": request_id,
            }
        ).encode("utf-8") + b"\n"
    except Exception as exc:  # pragma: no cover - defensive logging.
        LOGGER.exception("Generation failed (request_id=%s)", request_id, exc_info=exc)
        yield json.dumps({"type": "error", "message": str(exc), "request_id": request_id}).encode("utf-8") + b"\n"
        raise


@app.get("/health")
async def health() -> JSONResponse:
    """Basic health probe with engine status."""
    model_id = os.getenv(MODEL_ENV_VAR)
    payload = {
        "status": "ok",
        "model": model_id,
        "engine_ready": engine_manager.is_ready,
    }
    status_code = 200 if model_id else 503
    return JSONResponse(status_code=status_code, content=payload)


@app.post("/generate")
async def generate(payload: GenerateRequest):
    """Generate a chat completion, optionally streaming tokens."""
    try:
        prompt = format_chat_prompt(payload.messages)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        sampling_params = build_sampling_params(payload)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    request_id = uuid.uuid4().hex

    if payload.stream:
        headers = {"Cache-Control": "no-cache", "X-Request-ID": request_id}
        stream = iterate_generation(prompt, sampling_params, request_id)
        return StreamingResponse(stream, media_type="application/x-ndjson", headers=headers)

    engine = await engine_manager.get_engine()
    latest_text = ""
    finish_reason = None

    async for request_output in engine.generate(
        prompt=prompt,
        sampling_params=sampling_params,
        request_id=request_id,
    ):
        if not request_output.outputs:
            continue
        generation = request_output.outputs[0]
        latest_text = generation.text
        finish_reason = generation.finish_reason

    return {
        "output": latest_text.strip(),
        "finish_reason": finish_reason,
        "request_id": request_id,
    }
