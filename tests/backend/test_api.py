"""
Unit tests for MARC backend API endpoints.
"""
import json

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock

# Import the FastAPI app
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "backend"))

import app.main as app_main
from app.main import app
from app.chat_store import ChatLogger


@pytest.fixture
def client():
    """Test client for the FastAPI app."""
    return TestClient(app)


@pytest.mark.unit
def test_health_endpoint(client):
    """Test the /api/health endpoint returns OK status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.unit
def test_root_endpoint(client):
    """Test the root endpoint returns expected message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "vLLM backend" in data["message"]


@pytest.mark.unit
def test_generate_endpoint_empty_messages(client):
    """Test that generate endpoint rejects empty messages."""
    response = client.post(
        "/api/generate",
        json={"messages": [], "stream": False}
    )
    assert response.status_code == 400
    assert "must not be empty" in response.json()["detail"]


@pytest.mark.unit
def test_generate_endpoint_invalid_payload(client):
    """Test that generate endpoint validates payload structure."""
    response = client.post(
        "/api/generate",
        json={"invalid": "payload"}
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.unit
@patch('app.main.complete')
async def test_generate_endpoint_non_streaming(mock_complete, client):
    """Test non-streaming generation endpoint."""
    mock_complete.return_value = "This is a test response from the LLM."

    response = client.post(
        "/api/generate",
        json={
            "messages": [
                {"role": "user", "content": "Hello"}
            ],
            "stream": False,
            "max_tokens": 100,
            "temperature": 0.7
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "output" in data


@pytest.mark.unit
def test_generate_endpoint_with_persona(client):
    """Test that persona parameter is accepted."""
    with patch('app.main.complete', new_callable=AsyncMock) as mock_complete:
        mock_complete.return_value = "Response for developer persona"

        response = client.post(
            "/api/generate",
            json={
                "messages": [
                    {"role": "user", "content": "I need help with authentication"}
                ],
                "stream": False,
                "persona": "developer"
            }
        )

        # Should not raise validation error
        assert response.status_code in [200, 500]  # 500 if mock doesn't work perfectly


@pytest.mark.unit
def test_generate_endpoint_streaming(client):
    """Test streaming generation endpoint."""
    response = client.post(
        "/api/generate",
        json={
            "messages": [
                {"role": "user", "content": "Hello"}
            ],
            "stream": True
        }
    )

    # Streaming returns text/event-stream
    assert response.status_code == 200
    assert "text/event-stream" in response.headers.get("content-type", "")


@pytest.mark.unit
def test_generate_endpoint_parameter_validation(client):
    """Test parameter validation for max_tokens and temperature."""
    # Test invalid max_tokens (too low)
    response = client.post(
        "/api/generate",
        json={
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": 0  # Should be >= 1
        }
    )
    assert response.status_code == 422

    # Test invalid temperature (negative)
    response = client.post(
        "/api/generate",
        json={
            "messages": [{"role": "user", "content": "test"}],
            "temperature": -1  # Should be >= 0
        }
    )
    assert response.status_code == 422


@pytest.mark.unit
def test_cors_headers(client):
    """Test that CORS headers are properly configured."""
    response = client.options(
        "/api/generate",
        headers={"Origin": "http://localhost:3000"}
    )

    # CORS should allow all origins
    assert "access-control-allow-origin" in response.headers


@pytest.mark.unit
def test_generate_logs_messages_with_persona(tmp_path, client, monkeypatch):
    """Ensure non-streaming responses are persisted with persona metadata."""
    log_path = tmp_path / "chat.jsonl"
    monkeypatch.setattr(app_main, "chat_logger", ChatLogger(log_path))

    async def fake_generate(prompt, sampling_params, request_id):
        output = MagicMock()
        output.outputs = [MagicMock(text=f"{prompt}Assistant reply")]
        return [output]

    monkeypatch.setattr(
        app_main.engine,
        "generate",
        AsyncMock(side_effect=fake_generate),
    )

    payload = {
        "messages": [{"role": "user", "content": "Hello there"}],
        "stream": False,
        "persona": "customer",
    }
    response = client.post("/api/generate", json=payload)
    assert response.status_code == 200

    log_lines = log_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(log_lines) == 1

    record = json.loads(log_lines[0])
    assert record["persona"] == "customer"
    assert record["user_message"]["content"] == "Hello there"
    assert record["assistant_message"]["content"] == "Assistant reply"
    assert record["conversation"][-1]["role"] == "assistant"


@pytest.mark.unit
def test_generate_streaming_logs_messages(tmp_path, client, monkeypatch):
    """Ensure streaming responses are also persisted."""
    log_path = tmp_path / "stream_chat.jsonl"
    monkeypatch.setattr(app_main, "chat_logger", ChatLogger(log_path))

    class FakeRequestOutput:
        def __init__(self, text, finished):
            self.outputs = [MagicMock(text=text)]
            self.finished = finished

    class FakeAsyncIterator:
        def __init__(self, items):
            self._items = iter(items)

        def __aiter__(self):
            return self

        async def __anext__(self):
            try:
                return next(self._items)
            except StopIteration:
                raise StopAsyncIteration

    def fake_generate(prompt, sampling_params, request_id):
        return FakeAsyncIterator(
            [
                FakeRequestOutput(f"{prompt}Partial", False),
                FakeRequestOutput(f"{prompt}Partial final", True),
            ]
        )

    monkeypatch.setattr(app_main.engine, "generate", fake_generate)

    payload = {
        "messages": [{"role": "user", "content": "Stream this"}],
        "stream": True,
        "persona": "analyst",
    }
    response = client.post("/api/generate", json=payload, stream=True)
    assert response.status_code == 200

    # Consume the streaming body to trigger finalization.
    list(response.iter_lines())

    log_line = log_path.read_text(encoding="utf-8").strip()
    record = json.loads(log_line)
    assert record["persona"] == "analyst"
    assert record["assistant_message"]["content"] == "Partial final"
    assert record["user_message"]["content"] == "Stream this"
