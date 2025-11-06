# Testing Guide

Comprehensive guide to testing MARC and validating generated requirements.

## Running Tests

### Quick Start

```bash
# Navigate to project root
cd /path/to/SEproj1a1

# Install test dependencies (if not already installed)
pip install -r tests/requirements.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html --cov-report=term
```

### Using the Test Script

```bash
# Make executable
chmod +x run_tests.sh

# Run all tests
./run_tests.sh

# Run specific categories
./run_tests.sh unit
./run_tests.sh integration
./run_tests.sh backend
./run_tests.sh personas

# Generate coverage report
./run_tests.sh coverage

# Quick tests only
./run_tests.sh quick
```

## Test Categories

### Unit Tests

**Purpose**: Test individual functions and classes in isolation

**Run**: `pytest -m unit`

**Coverage**:
- Data model validation
- Prompt formatting
- Helper functions
- Configuration loading

**Example**:
```python
def test_chat_message_validation():
    # Valid message
    msg = ChatMessage(role="user", content="Test")
    assert msg.role == "user"

    # Invalid role
    with pytest.raises(ValueError):
        ChatMessage(role="invalid", content="Test")
```

### Integration Tests

**Purpose**: Test component interactions

**Run**: `pytest -m integration`

**Coverage**:
- API endpoint flows
- Frontend-backend integration
- Streaming protocol
- Error handling

**Example**:
```python
@pytest.mark.asyncio
async def test_generate_endpoint(client):
    response = await client.post("/generate", json={
        "messages": [{"role": "user", "content": "Test"}],
        "stream": False
    })

    assert response.status_code == 200
    data = response.json()
    assert "output" in data
```

### Persona Tests

**Purpose**: Validate persona-specific requirement generation

**Run**: `pytest tests/integration/test_personas.py`

**Coverage**:
- Each persona generates appropriate requirements
- Persona-specific focus areas
- Consistent output format

### Requirements Tests

**Purpose**: Verify requirement structure and IEEE compliance

**Run**: `pytest tests/requirements/`

**Coverage**:
- Requirement ID format
- Required sections present
- Acceptance criteria testability
- IEEE 29148 compliance

## Test Structure

```
tests/
├── backend/              # Backend API tests
│   ├── test_api.py      # Endpoint tests
│   └── test_models.py   # Pydantic model tests
├── integration/          # Integration tests
│   ├── test_personas.py # Persona-specific tests
│   └── test_multi_agent.py  # Multi-agent tests (planned)
├── requirements/         # Requirement validation tests
│   ├── test_extraction.py   # Parse requirements
│   └── test_ieee_compliance.py  # IEEE 29148 checks
├── fixtures/             # Test data and mocks
│   └── sample_requirements.py
├── conftest.py           # Pytest configuration
└── requirements.txt      # Test dependencies
```

## Writing Tests

### Backend API Test

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
```

### Async Test

```python
import pytest

@pytest.mark.asyncio
async def test_generate_streaming(client):
    async with client.stream(
        "POST",
        "/generate",
        json={"messages": [{"role": "user", "content": "Test"}], "stream": True}
    ) as response:
        chunks = []
        async for line in response.aiter_lines():
            if line:
                chunks.append(json.loads(line))

        assert len(chunks) > 0
        assert chunks[-1]["type"] == "done"
```

### Persona Test

```python
@pytest.mark.requires_llm
def test_developer_persona_generates_technical_requirements():
    persona = "developer"
    prompt = "Build user authentication"

    response = generate_requirement(persona, prompt)
    requirement = parse_requirement(response)

    # Developer should focus on technical aspects
    assert "security" in requirement.description.lower() or \
           "encryption" in requirement.description.lower()
    assert requirement.category in ["Security", "Functional"]
```

### Requirement Validation Test

```python
def test_requirement_has_all_ieee_sections():
    requirement_text = """
    REQ-DEV-001: User Authentication

    Category: Security
    Priority: High

    Description: ...
    Rationale: ...
    Acceptance Criteria: ...
    Dependencies: ...
    Verification Method: ...
    """

    sections = parse_requirement_sections(requirement_text)

    required_sections = [
        "Description",
        "Rationale",
        "Acceptance Criteria",
        "Dependencies",
        "Verification Method"
    ]

    for section in required_sections:
        assert section in sections
        assert len(sections[section].strip()) > 0
```

## Test Fixtures

### Mock LLM Response

```python
@pytest.fixture
def mock_llm_response():
    return """
    REQ-DEV-001: Test Requirement

    Category: Functional
    Priority: High

    Description: Test description
    Rationale: Test rationale
    Acceptance Criteria:
    - Criterion 1
    - Criterion 2
    Dependencies: None
    Verification Method: Unit tests
    """
```

### Test Client

```python
@pytest.fixture
def test_client():
    from app.main import app
    from fastapi.testclient import TestClient
    return TestClient(app)
```

## Coverage Goals

Target: **80%+ code coverage**

```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Current Coverage (Example)

```
Name                          Stmts   Miss  Cover
-------------------------------------------------
src/backend/app/main.py         156     12    92%
src/backend/app/__init__.py       2      0   100%
-------------------------------------------------
TOTAL                           158     12    92%
```

## Continuous Integration

Tests run automatically on:
- Push to any branch
- Pull requests
- Merges to main

### GitHub Actions (Example)

```yaml
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
      run: pytest --cov=src --cov-report=term

    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Validating Generated Requirements

### Manual Validation Checklist

After generating requirements, verify:

- [ ] **ID Format**: REQ-{PERSONA}-{NUMBER}
- [ ] **Category**: Valid category (Functional, Security, etc.)
- [ ] **Priority**: High, Medium, or Low
- [ ] **Description**: Clear, unambiguous statement
- [ ] **Rationale**: Explains why it's needed
- [ ] **Acceptance Criteria**: At least 2-3 testable criteria
- [ ] **Dependencies**: Lists any dependencies (or "None")
- [ ] **Verification Method**: Describes how to test

### Automated Validation

```python
from requirements_validator import validate_requirement

requirement_text = """..."""

result = validate_requirement(requirement_text)

if result.is_valid:
    print("✓ Requirement is valid")
else:
    print("✗ Issues found:")
    for issue in result.issues:
        print(f"  - {issue}")
```

## Performance Testing

### Load Testing

Test API under load:

```bash
# Install locust
pip install locust

# Create locustfile.py
# Run load test
locust -f locustfile.py --host=http://localhost:8001
```

### Response Time Testing

```python
import time

def test_generate_response_time():
    start = time.time()

    response = client.post("/generate", json={
        "messages": [{"role": "user", "content": "Test"}],
        "stream": False
    })

    elapsed = time.time() - start

    assert response.status_code == 200
    assert elapsed < 5.0  # Should respond within 5 seconds
```

## Debugging Tests

### Run Single Test

```bash
pytest tests/backend/test_api.py::test_health_endpoint -v
```

### Show Print Statements

```bash
pytest -s  # Don't capture stdout
```

### Debug with pdb

```python
def test_something():
    import pdb; pdb.set_trace()
    # Test code...
```

### Verbose Logging

```bash
pytest --log-cli-level=DEBUG
```

## Next Steps

- [Contributing Guide](../development/contributing.md) - Write tests for new features
- [Code Standards](../development/standards.md) - Testing conventions
- [API Reference](../api/rest-api.md) - Understand what to test
