"""
Unit tests for MARC backend engine module.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "backend"))

from app.engine import (
    build_prompt,
    sampling_params_from_request,
)


@pytest.mark.unit
def test_build_prompt_basic():
    """Test basic prompt building without persona."""
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "How are you?"}
    ]

    prompt = build_prompt(messages)

    assert "User: Hello" in prompt
    assert "Assistant: Hi there!" in prompt
    assert "User: How are you?" in prompt
    assert prompt.endswith("Assistant:")


@pytest.mark.unit
def test_build_prompt_with_persona():
    """Test prompt building with persona."""
    messages = [{"role": "user", "content": "Test message"}]

    prompt = build_prompt(messages, persona="developer")

    assert "Persona: developer" in prompt
    assert "User: Test message" in prompt


@pytest.mark.unit
def test_build_prompt_with_system_message():
    """Test prompt building with system message."""
    messages = [
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "Hello"}
    ]

    prompt = build_prompt(messages)

    assert "System: You are helpful" in prompt
    assert "User: Hello" in prompt


@pytest.mark.unit
def test_build_prompt_empty_content():
    """Test that empty content messages are skipped."""
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "user", "content": ""},  # Empty
        {"role": "user", "content": "   "},  # Whitespace only
        {"role": "user", "content": "Goodbye"}
    ]

    prompt = build_prompt(messages)

    assert "Hello" in prompt
    assert "Goodbye" in prompt
    # Empty messages should not appear
    lines = [line for line in prompt.split('\n') if line.strip()]
    assert len([l for l in lines if l.startswith("User:")]) == 2


@pytest.mark.unit
def test_sampling_params_from_request_defaults():
    """Test sampling params with default values."""
    params = sampling_params_from_request()

    assert params.max_tokens == 1024  # DEFAULT_MAX_TOKENS
    assert params.temperature == 0.7  # DEFAULT_TEMPERATURE
    assert params.stop is not None


@pytest.mark.unit
def test_sampling_params_from_request_custom():
    """Test sampling params with custom values."""
    params = sampling_params_from_request(max_tokens=1024, temperature=0.9)

    assert params.max_tokens == 1024
    assert params.temperature == 0.9


@pytest.mark.unit
def test_sampling_params_from_request_zero_temperature():
    """Test sampling params with temperature of 0."""
    params = sampling_params_from_request(temperature=0)

    assert params.temperature == 0
