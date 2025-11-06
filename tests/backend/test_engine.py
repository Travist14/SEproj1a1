"""
Unit tests for prompt formatting and sampling-param helpers in the backend.

These tests call small, deterministic helpers implemented in `app.main` so they
remain fast unit tests and don't require an actual LLM.
"""

import sys
from pathlib import Path
import pytest
import json
from unittest.mock import MagicMock, AsyncMock

# Make backend package importable
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "backend"))

from app.main import ChatMessage, format_chat_prompt, build_sampling_params, GenerateRequest
from app.main import DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE
import app.main as app_main


@pytest.mark.unit
def test_format_chat_prompt_basic():
    msgs = [
        ChatMessage(role="user", content="Hello"),
        ChatMessage(role="assistant", content="Hi there!"),
        ChatMessage(role="user", content="How are you?"),
    ]

    prompt = format_chat_prompt(msgs)

    assert "User: Hello" in prompt
    assert "Assistant: Hi there!" in prompt
    assert "User: How are you?" in prompt
    assert prompt.strip().endswith("Assistant:")


@pytest.mark.unit
def test_format_chat_prompt_empty_raises():
    with pytest.raises(ValueError):
        format_chat_prompt([])


@pytest.mark.unit
def test_build_sampling_params_defaults_and_custom():
    # Use a minimal GenerateRequest to build params
    req = GenerateRequest(messages=[ChatMessage(role="user", content="Hi")])
    params = build_sampling_params(req)

    assert params.max_tokens == DEFAULT_MAX_TOKENS
    assert params.temperature == DEFAULT_TEMPERATURE

    # custom values
    req2 = GenerateRequest(messages=[ChatMessage(role="user", content="Hi")], max_tokens=128, temperature=0.1)
    params2 = build_sampling_params(req2)
    assert params2.max_tokens == 128
    assert params2.temperature == 0.1


@pytest.mark.unit
@pytest.mark.asyncio
async def test_engine_manager_raises_when_vllm_missing(monkeypatch):
    """EngineManager.get_engine should raise when vLLM imports are unavailable."""
    # Simulate missing vllm imports
    monkeypatch.setattr(app_main, "AsyncLLMEngine", None)
    monkeypatch.setattr(app_main, "AsyncEngineArgs", None)
    monkeypatch.setattr(app_main, "SamplingParams", None)

    em = app_main.EngineManager()

    with pytest.raises(RuntimeError):
        await em.get_engine()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_iterate_generation_with_mocked_engine(monkeypatch):
    """iterate_generation should stream token chunks and a final done message given a mocked engine."""

    # Minimal Generation and RequestOutput classes used by the real code
    class Generation:
        def __init__(self, text, finish_reason=None):
            self.text = text
            self.finish_reason = finish_reason

    class RequestOutput:
        def __init__(self, generation: Generation):
            self.outputs = [generation]

    async def fake_generate(prompt, sampling_params, request_id):
        # yield two incremental updates then finish
        yield RequestOutput(Generation("Hello"))
        yield RequestOutput(Generation("Hello world", finish_reason="stop"))

    mock_engine = MagicMock()
    mock_engine.generate = fake_generate

    # Patch the global engine_manager.get_engine to return our mock
    monkeypatch.setattr(app_main.engine_manager, "get_engine", AsyncMock(return_value=mock_engine))

    # Create test data
    messages = [ChatMessage(role="user", content="Hello")]
    persona = "developer"  # or None if the function accepts None
    generation_parameters = GenerateRequest(messages=messages)

    chunks = []
    async for raw in app_main.iterate_generation(
        messages=messages,
        persona=persona,
        generation_parameters=generation_parameters,
        request_id = 'req-123',
        prompt = 'prompt',
        sampling_params = None
    ):
        chunks.append(json.loads(raw.decode("utf-8")))

    # Expect at least one token chunk and one done message
    types = [c.get("type") for c in chunks]
    assert "token" in types
    assert "done" in types

