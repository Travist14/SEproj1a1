"""FastAPI application for chat completions powered by vLLM."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import textwrap
import uuid
from datetime import datetime, timezone
from typing import Any, AsyncIterator, Dict, List, Optional, Sequence

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field, field_validator

from .chat_storage import ChatStorage, ChatTranscript

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
DEFAULT_MODEL_ID = "Qwen/Qwen3-4B" # change this model to someting better for better performance. We just use qwen 4b cause vram 
DEFAULT_MAX_TOKENS = int(os.getenv("VLLM_MAX_TOKENS", "1024"))
DEFAULT_TOP_P = float(os.getenv("VLLM_TOP_P", "0.95"))
DEFAULT_TEMPERATURE = float(os.getenv("VLLM_TEMPERATURE", "0.7"))
DEFAULT_FREQUENCY_PENALTY = float(os.getenv("VLLM_FREQUENCY_PENALTY", "0.8"))
DEFAULT_STOP_SEQUENCES = ["\nSystem:", "\nUser:"]


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
        default=DEFAULT_FREQUENCY_PENALTY, ge=-2.0, le=2.0, description="Frequency penalty following OpenAI semantics."
    )
    stop: Optional[List[str]] = Field(
        default=None, description="Optional list of strings that will terminate generation."
    )
    persona: Optional[str] = Field(
        default=None,
        description="Optional persona identifier forwarded by the frontend. Currently informational only.",
    )


class OrchestratorRequest(BaseModel):
    """Request payload for orchestrator endpoint."""

    personas: Optional[List[str]] = Field(
        default=None,
        description="Optional subset of personas/stakeholders to include. Defaults to all stored transcripts.",
    )
    max_transcripts_per_persona: Optional[int] = Field(
        default=5,
        ge=1,
        le=50,
        description="Maximum number of recent transcripts loaded per persona.",
    )
    summary_max_tokens: int = Field(
        default=512,
        ge=128,
        le=2048,
        description="Token budget for each stakeholder summary.",
    )
    requirements_max_tokens: int = Field(
        default=1024,
        ge=256,
        le=3072,
        description="Token budget for the requirements document.",
    )
    include_requirements: bool = Field(
        default=True,
        description="Generate the requirements engineering document as part of the orchestrator run.",
    )


class OrchestratorResponse(BaseModel):
    """Response payload for orchestrator endpoint."""

    summaries: Dict[str, str] = Field(description="Generated summaries keyed by persona.")
    requirements_document: str = Field(description="Generated requirements engineering document.")


class OrchestratorStateResponse(BaseModel):
    """State payload returned by orchestrator state endpoint."""

    updated_at: datetime = Field(description="Timestamp when the orchestrator plan was last updated.")
    summaries: Dict[str, str] = Field(description="Latest stakeholder summaries keyed by persona.")
    requirements_document: str = Field(description="Latest requirements engineering document.")


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
chat_storage = ChatStorage()

ORCHESTRATOR_DEFAULT_MAX_TRANSCRIPTS = 5
ORCHESTRATOR_DEFAULT_SUMMARY_TOKENS = 512
ORCHESTRATOR_DEFAULT_REQUIREMENTS_TOKENS = 1024

_orchestrator_state_lock = asyncio.Lock()
_orchestrator_state: Optional[OrchestratorResponse] = None
_orchestrator_state_updated_at: Optional[datetime] = None
_orchestrator_update_task: Optional[asyncio.Task] = None
_orchestrator_refresh_pending = False

app = FastAPI(title="SEproj Chat Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("BACKEND_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def trigger_initial_orchestrator_refresh() -> None:
    """Ensure the orchestrator plan is computed shortly after startup."""
    schedule_orchestrator_refresh()


def format_chat_prompt(messages: List[ChatMessage]) -> str:
    """Convert structured chat messages into a plain-text prompt."""
    if not messages:
        raise ValueError("At least one message is required.")

    prompt_segments: List[str] = []
    for message in messages:
        role = message.role.capitalize()
        content = message.content.strip()
        prompt_segments.append(f"{role}: {content}")

    prompt_segments.append(
        "System: Reply directly to the user. Do not narrate analysis or internal thoughts. "
        "Do not create new System/User/Assistant turns, restate the conversation log, or add meta commentary such as "
        "'Assistant:'/'Answer:' labels or closing markers. Provide a single, user-facing answer."
    )
    # Ensure the model continues the assistant turn.
    prompt_segments.append("Assistant:")
    return "\n\n".join(prompt_segments)


def serialise_messages(messages: List[ChatMessage]) -> List[Dict[str, str]]:
    """Convert Pydantic chat messages into plain dictionaries."""
    return [message.model_dump() for message in messages]


def build_generation_metadata(payload: GenerateRequest) -> Dict[str, Any]:
    """Capture the caller-specified sampling configuration for persistence."""
    return {
        "max_tokens": payload.max_tokens,
        "temperature": payload.temperature,
        "top_p": payload.top_p,
        "presence_penalty": payload.presence_penalty,
        "frequency_penalty": payload.frequency_penalty,
        "stop": payload.stop,
        "stream": payload.stream,
    }


async def persist_chat_transcript(
    request_id: str,
    *,
    messages: List[Dict[str, str]],
    response_text: str,
    finish_reason: Optional[str],
    persona: Optional[str],
    generation_parameters: Dict[str, Any],
) -> None:
    """Persist a completed chat interaction for downstream orchestration."""
    transcript = ChatTranscript(
        request_id=request_id,
        messages=messages,
        response_text=response_text,
        finish_reason=finish_reason,
        persona=persona,
        parameters=generation_parameters,
        created_at=datetime.now(timezone.utc),
    )
    try:
        await chat_storage.save_transcript(transcript)
    except Exception as exc:  # pragma: no cover - defensive logging.
        LOGGER.exception("Failed to persist chat transcript (request_id=%s)", request_id, exc_info=exc)


def truncate_text(value: str, max_length: int = 600) -> str:
    """Trim long text blocks to keep prompts manageable."""
    text = value.strip()
    if len(text) <= max_length:
        return text
    return text[: max_length - 3].rstrip() + "..."


def format_transcript_for_prompt(transcript: ChatTranscript) -> str:
    """Render a transcript into a compact textual format for prompting."""
    lines = [
        f"- request_id: {transcript.request_id}",
        f"  timestamp: {transcript.created_at.isoformat()}",
        "  dialogue:",
    ]

    for message in transcript.messages:
        role = message.get("role", "unknown")
        content = truncate_text(message.get("content", ""))
        lines.append(f"    - {role}: {content}")

    response = truncate_text(transcript.response_text)
    if response:
        lines.append(f"    - assistant_response: {response}")
    if transcript.finish_reason:
        lines.append(f"  finish_reason: {transcript.finish_reason}")
    if transcript.parameters:
        lines.append(f"  parameters: {json.dumps(transcript.parameters, ensure_ascii=True)}")

    return "\n".join(lines)


def build_summary_prompt(persona: str, transcripts: Sequence[ChatTranscript]) -> str:
    """Create a prompt asking the model to summarise a stakeholder's transcripts."""
    persona_label = persona or "general"
    joined_transcripts = "\n".join(format_transcript_for_prompt(t) for t in transcripts)
    instructions = textwrap.dedent(
        f"""
        You are the orchestrator agent for a requirements engineering project.
        Summarise the key goals, pain points, and constraints expressed by the '{persona_label}' stakeholder
        across the chat transcripts. Focus on actionable insights that influence product requirements.

        Provide a concise summary using bullet points. Use at most five lines in total.
        """
    ).strip()

    return (
        f"{instructions}\n\n"
        f"Transcripts:\n{joined_transcripts}\n\n"
        "Stakeholder Summary:\n"
    )


def build_requirements_prompt(summaries: Dict[str, str]) -> str:
    """Create a prompt that asks the model to produce a requirements engineering document."""
    stakeholder_section = "\n\n".join(
        f"Stakeholder: {persona or 'general'}\nSummary:\n{summary.strip()}"
        for persona, summary in summaries.items()
    )

    instructions = textwrap.dedent(
        """
        You are a senior requirements engineer. Using the stakeholder summaries below,
        produce a cohesive requirements document that reconciles all perspectives.

        Structure the response with the following sections:
        1. Project Overview
        2. Stakeholder Goals (grouped by stakeholder)
        3. Functional Requirements
        4. Non-Functional Requirements / Constraints
        5. Risks and Open Questions

        Keep each section succinct but specific enough to guide implementation planning.
        """
    ).strip()

    return (
        f"{instructions}\n\n"
        f"Stakeholder Summaries:\n{stakeholder_section}\n\n"
        "Requirements Document:\n"
    )


def clamp_lines(text: str, *, max_lines: int) -> str:
    """Clamp text to at most the specified number of non-empty lines."""
    if not text:
        return text
    lines = [line.rstrip() for line in text.strip().splitlines()]
    limited = lines[:max_lines]
    return "\n".join(limited).strip()


async def generate_requirements_document(
    summaries: Dict[str, str],
    *,
    requirements_max_tokens: int,
) -> str:
    """Generate the requirements engineering document from prepared summaries."""
    requirements_prompt = build_requirements_prompt(summaries)
    return await generate_text_response(
        requirements_prompt,
        max_tokens=requirements_max_tokens,
        temperature=0.45,
        top_p=0.92,
    )


async def generate_text_response(
    prompt: str,
    *,
    max_tokens: int,
    temperature: float = 0.4,
    top_p: float = 0.9,
    presence_penalty: float = 0.0,
    frequency_penalty: float = 0.2,
) -> str:
    """Run a single-turn completion with the shared model."""
    engine = await engine_manager.get_engine()
    sampling_params = SamplingParams(
        n=1,
        best_of=1,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        presence_penalty=presence_penalty,
        frequency_penalty=frequency_penalty,
    )

    latest_text = ""
    async for request_output in engine.generate(
        prompt=prompt,
        sampling_params=sampling_params,
        request_id=uuid.uuid4().hex,
    ):
        if not request_output.outputs:
            continue
        generation = request_output.outputs[0]
        latest_text = generation.text

    return latest_text.strip()


async def _set_orchestrator_state(result: OrchestratorResponse) -> None:
    """Store the latest orchestrator result for quick retrieval."""
    global _orchestrator_state, _orchestrator_state_updated_at
    async with _orchestrator_state_lock:
        _orchestrator_state = result
        _orchestrator_state_updated_at = datetime.now(timezone.utc)


async def run_orchestrator_job(
    *,
    personas: Optional[Sequence[str]],
    max_transcripts_per_persona: Optional[int],
    summary_max_tokens: int,
    requirements_max_tokens: int,
    include_requirements: bool,
) -> OrchestratorResponse:
    """Execute the orchestrator pipeline and return the generated artefacts."""
    transcripts_by_persona = await chat_storage.load_transcripts(
        personas=personas,
        limit_per_persona=max_transcripts_per_persona,
    )

    if not transcripts_by_persona:
        raise ValueError("No transcripts available for the requested personas.")

    summaries: Dict[str, str] = {}
    for persona, transcripts in transcripts_by_persona.items():
        if not transcripts:
            continue
        summary_prompt = build_summary_prompt(persona, transcripts)
        summary_text = await generate_text_response(
            summary_prompt,
            max_tokens=summary_max_tokens,
            temperature=0.35,
            top_p=0.9,
        )
        summaries[persona] = clamp_lines(summary_text, max_lines=5)

    if not summaries:
        raise ValueError("No transcripts available for the requested personas.")

    requirements_document = ""
    if include_requirements:
        requirements_document = await generate_requirements_document(
            summaries,
            requirements_max_tokens=requirements_max_tokens,
        )

    return OrchestratorResponse(summaries=summaries, requirements_document=requirements_document)


async def refresh_orchestrator_state() -> None:
    """Recompute and cache the orchestrator plan using default parameters."""
    try:
        result = await run_orchestrator_job(
            personas=None,
            max_transcripts_per_persona=ORCHESTRATOR_DEFAULT_MAX_TRANSCRIPTS,
            summary_max_tokens=ORCHESTRATOR_DEFAULT_SUMMARY_TOKENS,
            requirements_max_tokens=ORCHESTRATOR_DEFAULT_REQUIREMENTS_TOKENS,
            include_requirements=False,
        )
    except ValueError:
        LOGGER.info("Skipping orchestrator refresh; no transcripts available.")
        return
    except Exception as exc:  # pragma: no cover - defensive logging.
        LOGGER.exception("Orchestrator refresh failed", exc_info=exc)
        return

    await _set_orchestrator_state(result)


def schedule_orchestrator_refresh() -> None:
    """Schedule a background orchestrator refresh if one is not already running."""
    global _orchestrator_update_task, _orchestrator_refresh_pending
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        LOGGER.warning("No running event loop; cannot schedule orchestrator refresh.")
        return

    if _orchestrator_update_task and not _orchestrator_update_task.done():
        _orchestrator_refresh_pending = True
        return

    task = loop.create_task(refresh_orchestrator_state())
    _orchestrator_update_task = task

    def _handle_completion(completed: asyncio.Task) -> None:
        global _orchestrator_update_task, _orchestrator_refresh_pending
        try:
            completed.result()
        except Exception as exc:  # pragma: no cover - defensive logging.
            LOGGER.exception("Background orchestrator refresh failed", exc_info=exc)
        finally:
            _orchestrator_update_task = None
            if _orchestrator_refresh_pending:
                _orchestrator_refresh_pending = False
                schedule_orchestrator_refresh()

    task.add_done_callback(_handle_completion)

def build_sampling_params(payload: GenerateRequest) -> SamplingParams:
    """Create sampling parameters for vLLM from the request payload."""
    stop_sequences = list(DEFAULT_STOP_SEQUENCES)
    if payload.stop:
        # Preserve caller-provided stops while ensuring role prefixes still terminate output.
        stop_sequences = list(dict.fromkeys(payload.stop + stop_sequences))
    return SamplingParams(
        n=1,
        best_of=1,
        max_tokens=payload.max_tokens,
        temperature=payload.temperature,
        top_p=payload.top_p,
        presence_penalty=payload.presence_penalty,
        frequency_penalty=payload.frequency_penalty,
        stop=stop_sequences,
    )


async def iterate_generation(
    prompt: str,
    sampling_params: SamplingParams,
    request_id: str,
    *,
    messages: List[Dict[str, str]],
    persona: Optional[str],
    generation_parameters: Dict[str, Any],
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
        await persist_chat_transcript(
            request_id,
            messages=messages,
            response_text=previous_text,
            finish_reason=finish_reason,
            persona=persona,
            generation_parameters=generation_parameters,
        )
        schedule_orchestrator_refresh()
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
@app.post("/api/generate")
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
    message_payload = serialise_messages(payload.messages)
    generation_metadata = build_generation_metadata(payload)
    persona = payload.persona

    if payload.stream:
        headers = {"Cache-Control": "no-cache", "X-Request-ID": request_id}
        stream = iterate_generation(
            prompt,
            sampling_params,
            request_id,
            messages=message_payload,
            persona=persona,
            generation_parameters=generation_metadata,
        )
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

    await persist_chat_transcript(
        request_id,
        messages=message_payload,
        response_text=latest_text.strip(),
        finish_reason=finish_reason,
        persona=persona,
        generation_parameters=generation_metadata,
    )
    schedule_orchestrator_refresh()

    return {
        "output": latest_text.strip(),
        "finish_reason": finish_reason,
        "request_id": request_id,
    }


@app.post("/orchestrate", response_model=OrchestratorResponse)
@app.post("/api/orchestrate", response_model=OrchestratorResponse)
async def orchestrate(payload: OrchestratorRequest) -> OrchestratorResponse:
    """Run the orchestrator agent to summarise transcripts and produce a requirements document."""
    try:
        result = await run_orchestrator_job(
            personas=payload.personas,
            max_transcripts_per_persona=payload.max_transcripts_per_persona,
            summary_max_tokens=payload.summary_max_tokens,
            requirements_max_tokens=payload.requirements_max_tokens,
            include_requirements=payload.include_requirements,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:  # pragma: no cover - defensive logging.
        LOGGER.exception("Failed to execute orchestrator request", exc_info=exc)
        raise HTTPException(status_code=500, detail="Failed to run orchestrator.") from exc

    await _set_orchestrator_state(result)
    return result


@app.get("/orchestrator/state", response_model=OrchestratorStateResponse)
@app.get("/api/orchestrator/state", response_model=OrchestratorStateResponse)
async def get_orchestrator_state() -> OrchestratorStateResponse:
    """Return the cached orchestrator plan if one is available."""
    async with _orchestrator_state_lock:
        if _orchestrator_state is None or _orchestrator_state_updated_at is None:
            raise HTTPException(status_code=404, detail="Orchestrator state not yet available.")
        return OrchestratorStateResponse(
            updated_at=_orchestrator_state_updated_at,
            summaries=_orchestrator_state.summaries,
            requirements_document=_orchestrator_state.requirements_document,
        )
