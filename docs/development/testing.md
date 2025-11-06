# Development Testing Guide

Comprehensive testing guide for MARC developers.

## Test Philosophy

MARC follows a **test-driven development (TDD)** approach where possible:

1. Write failing test
2. Write minimal code to pass test
3. Refactor while keeping tests green

## Test Pyramid

```
       /\
      /  \     E2E Tests (Few)
     /────\
    /      \   Integration Tests (Some)
   /────────\
  /          \ Unit Tests (Many)
 /────────────\
```

- **Unit Tests**: Fast, isolated, many
- **Integration Tests**: Moderate speed, test interactions
- **E2E Tests**: Slow, test full workflows (future)

## Test Structure

```
tests/
├── backend/              # Backend tests
│   ├── test_api.py      # API endpoint tests
│   ├── test_models.py   # Pydantic model tests
│   └── test_engine.py   # EngineManager tests
├── integration/          # Integration tests
│   ├── test_personas.py # Persona generation tests
│   ├── test_streaming.py # Streaming protocol tests
│   └── test_multi_agent.py # Future multi-agent tests
├── requirements/         # Requirement validation
│   ├── test_extraction.py # Parsing tests
│   └── test_ieee_compliance.py # Standards compliance
├── frontend/            # Frontend tests (future)
│   ├── test_components.py
│   └── test_hooks.py
├── fixtures/            # Shared test data
│   ├── __init__.py
│   └── sample_data.py
├── conftest.py          # Pytest configuration
└── requirements.txt     # Test dependencies
```

## Writing Unit Tests

### Backend Unit Test Example

```python
# tests/backend/test_models.py
import pytest
from pydantic import ValidationError
from app.main import ChatMessage, GenerateRequest

class TestChatMessage:
    """Tests for ChatMessage model."""

    def test_valid_message(self):
        """Test creating valid message."""
        msg = ChatMessage(role="user", content="Hello")

        assert msg.role == "user"
        assert msg.content == "Hello"

    def test_invalid_role(self):
        """Test invalid role raises error."""
        with pytest.raises(ValidationError) as exc_info:
            ChatMessage(role="invalid", content="Hello")

        assert "role must be one of" in str(exc_info.value)

    @pytest.mark.parametrize("role", ["system", "user", "assistant"])
    def test_all_valid_roles(self, role):
        """Test all valid roles accepted."""
        msg = ChatMessage(role=role, content="Test")
        assert msg.role == role
```

### Frontend Unit Test Example

```javascript
// tests/frontend/test_hooks.test.js
import { renderHook, act } from '@testing-library/react-hooks';
import { useChat } from '../../src/hooks/useChat';

describe('useChat hook', () => {
  it('initializes with empty messages', () => {
    const { result } = renderHook(() => useChat('developer'));

    expect(result.current.messages).toEqual([]);
    expect(result.current.status).toBe('idle');
  });

  it('adds message when sendMessage called', async () => {
    const { result } = renderHook(() => useChat('developer'));

    await act(async () => {
      await result.current.sendMessage('Hello');
    });

    expect(result.current.messages.length).toBeGreaterThan(0);
    expect(result.current.messages[0].role).toBe('user');
  });
});
```

## Writing Integration Tests

### API Integration Test

```python
# tests/integration/test_api_flow.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)

class TestAPIFlow:
    """Test complete API workflows."""

    def test_health_check_flow(self, client):
        """Test health endpoint returns expected data."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert "model" in data
        assert "engine_ready" in data

    def test_generate_non_streaming_flow(self, client):
        """Test complete non-streaming generation."""
        payload = {
            "messages": [
                {"role": "user", "content": "Test requirement"}
            ],
            "stream": False,
            "max_tokens": 100
        }

        response = client.post("/generate", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert "output" in data
        assert "request_id" in data
        assert len(data["output"]) > 0

    @pytest.mark.asyncio
    async def test_generate_streaming_flow(self, client):
        """Test complete streaming generation."""
        payload = {
            "messages": [{"role": "user", "content": "Test"}],
            "stream": True
        }

        with client.stream("POST", "/generate", json=payload) as response:
            assert response.status_code == 200

            chunks = []
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    chunks.append(data)

            # Verify we got tokens and done event
            assert any(c["type"] == "token" for c in chunks)
            assert chunks[-1]["type"] == "done"
```

### Persona Integration Test

```python
# tests/integration/test_personas.py
import pytest

@pytest.mark.requires_llm
class TestPersonaGeneration:
    """Test persona-specific requirement generation."""

    def test_developer_persona(self, generate_requirement):
        """Developer generates technical requirements."""
        response = generate_requirement(
            persona="developer",
            prompt="Build user authentication"
        )

        # Developer should mention technical details
        technical_keywords = [
            "security", "encryption", "bcrypt", "jwt",
            "api", "database", "hash"
        ]

        response_lower = response.lower()
        assert any(kw in response_lower for kw in technical_keywords)

    def test_product_manager_persona(self, generate_requirement):
        """Product Manager focuses on business value."""
        response = generate_requirement(
            persona="product_manager",
            prompt="Build user authentication"
        )

        # PM should mention business aspects
        business_keywords = [
            "user", "value", "business", "metric",
            "kpi", "success", "adoption"
        ]

        response_lower = response.lower()
        assert any(kw in response_lower for kw in business_keywords)
```

## Test Fixtures

### conftest.py

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Provide test client for API tests."""
    return TestClient(app)

@pytest.fixture
def sample_messages():
    """Provide sample chat messages."""
    return [
        {"role": "system", "content": "You are a developer."},
        {"role": "user", "content": "Build authentication"}
    ]

@pytest.fixture
def sample_requirement():
    """Provide sample requirement text."""
    return """
    REQ-DEV-001: User Authentication

    Category: Security
    Priority: High

    Description: Implement secure authentication
    Rationale: Protect user data
    Acceptance Criteria:
    - Password hashing with bcrypt
    - JWT token generation
    Dependencies: bcrypt, JWT library
    Verification Method: Unit tests
    """

@pytest.fixture
def generate_requirement():
    """Fixture for generating requirements in tests."""
    def _generate(persona: str, prompt: str) -> str:
        # Implementation depends on your setup
        # Could call API or mock LLM
        pass
    return _generate
```

## Test Markers

### Custom Markers

```python
# pytest.ini
[pytest]
markers =
    unit: Unit tests (fast, no external dependencies)
    integration: Integration tests (may require services)
    requires_llm: Tests that need actual LLM (slow, expensive)
    slow: Tests that take > 5 seconds
```

### Using Markers

```python
@pytest.mark.unit
def test_fast_function():
    """Fast unit test."""
    pass

@pytest.mark.integration
def test_api_endpoint():
    """Integration test."""
    pass

@pytest.mark.requires_llm
@pytest.mark.slow
def test_full_generation():
    """Full LLM generation test."""
    pass
```

### Running by Marker

```bash
# Run only unit tests
pytest -m unit

# Run everything except slow tests
pytest -m "not slow"

# Run integration but not LLM tests
pytest -m "integration and not requires_llm"
```

## Mocking

### Mock vLLM Engine

```python
# tests/fixtures/mock_engine.py
from unittest.mock import Mock, AsyncMock

@pytest.fixture
def mock_llm_engine():
    """Mock vLLM engine for testing without actual LLM."""
    engine = Mock()
    engine.generate = AsyncMock()

    async def generate_mock(*args, **kwargs):
        # Yield mock request outputs
        mock_output = Mock()
        mock_output.outputs = [Mock(text="Mocked response")]
        yield mock_output

    engine.generate.side_effect = generate_mock
    return engine
```

### Mock API Responses

```python
import responses

@responses.activate
def test_api_call():
    """Test with mocked HTTP responses."""
    responses.add(
        responses.POST,
        "http://localhost:8001/generate",
        json={"output": "Mocked"},
        status=200
    )

    # Your test code that calls the API
```

## Coverage

### Measuring Coverage

```bash
# Run with coverage
pytest --cov=src --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

### Coverage Configuration

```ini
# .coveragerc
[run]
source = src
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
```

### Coverage Goals

- **Overall**: 80%+
- **Critical paths**: 90%+
- **New code**: 100%

## Performance Testing

### Response Time Test

```python
import time

def test_generate_performance(client):
    """Test response time is acceptable."""
    start = time.time()

    response = client.post("/generate", json={
        "messages": [{"role": "user", "content": "Test"}],
        "stream": False
    })

    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 5.0  # Should respond within 5 seconds
```

### Load Testing with Locust

```python
# locustfile.py
from locust import HttpUser, task, between

class MARCUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def generate_requirement(self):
        self.client.post("/generate", json={
            "messages": [
                {"role": "user", "content": "Build authentication"}
            ],
            "stream": False
        })
```

Run: `locust -f locustfile.py --host=http://localhost:8001`

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        pip install -r src/backend/requirements.txt
        pip install -r tests/requirements.txt

    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
```

## Best Practices

1. **Test Naming**: `test_<what>_<condition>_<expected>`
   - ✅ `test_generate_with_invalid_role_raises_error`
   - ❌ `test_1`

2. **One Assertion Per Test** (when possible)
   - Makes failures easier to diagnose

3. **Arrange-Act-Assert (AAA) Pattern**
   ```python
   def test_something():
       # Arrange
       data = setup_test_data()

       # Act
       result = function_under_test(data)

       # Assert
       assert result == expected
   ```

4. **Don't Test Implementation Details**
   - Test behavior, not internal state

5. **Clean Up After Tests**
   - Use fixtures with yield for cleanup
   - Reset mocks between tests

## Next Steps

- [Code Standards](standards.md) - Coding conventions
- [Contributing Guide](contributing.md) - How to contribute
- [Testing Guide](../guide/testing.md) - User-facing testing docs
