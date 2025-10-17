from __future__ import annotations

import logging
from typing import AsyncGenerator, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from .engine import complete, sampling_params_from_request, stream_generate

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="vLLM Inference Server", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str = Field(..., description="Chat role such as system, user, assistant")
    content: str = Field(..., description="Message content")


class GenerateRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., description="Conversation history")
    stream: bool = Field(False, description="Enable server-sent events streaming")
    max_tokens: Optional[int] = Field(None, ge=1, le=4096)
    temperature: Optional[float] = Field(None, ge=0)
    persona: Optional[str] = Field(None, description="Persona identifier from the frontend")


@app.get("/api/health")
async def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


def _validate_messages(messages: List[ChatMessage]) -> None:
    if not messages:
        raise HTTPException(status_code=400, detail="messages must not be empty")


@app.post("/api/generate")
async def generate(payload: GenerateRequest):
    _validate_messages(payload.messages)
    sampling_params = sampling_params_from_request(
        max_tokens=payload.max_tokens,
        temperature=payload.temperature,
    )

    message_dicts = [message.dict() for message in payload.messages]

    if payload.stream:
        async def event_publisher() -> AsyncGenerator[bytes, None]:
            try:
                async for chunk in stream_generate(
                    message_dicts, sampling_params, persona=payload.persona
                ):
                    for line in chunk.replace("\r", "").split("\n"):
                        if not line:
                            continue
                        yield f"data: {line}\n\n".encode()
                yield b"data: [DONE]\n\n"
            except Exception as exc:  # pylint: disable=broad-except
                logger.exception("Streaming generation failed")
                yield f"data: ERROR: {exc}\n\n".encode()

        return StreamingResponse(event_publisher(), media_type="text/event-stream")

    try:
        text = await complete(
            message_dicts,
            sampling_params,
            persona=payload.persona,
        )
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Generation request failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {"output": text}


@app.get("/")
async def root():
    return {"message": "vLLM backend is running"}
