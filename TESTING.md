# MARC Testing Guide

Quick reference for testing the MARC (Multi-Agent Requirement Collaboration) system.

## Quick Start

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

## Test Categories

| Command | Description |
|---------|-------------|
| `pytest -m unit` | Fast unit tests |
| `pytest -m integration` | Integration tests |
| `pytest -m slow` | Long-running tests |
| `pytest tests/backend/` | Backend API tests |
| `pytest tests/integration/` | Persona & multi-agent tests |
| `pytest tests/requirements/` | Requirements extraction tests |

## What's Being Tested

### 1. Backend API (`tests/backend/`)
- ✅ Health check endpoint
- ✅ Generate endpoint (streaming & non-streaming)
- ✅ Request validation
- ✅ Error handling
- ✅ CORS configuration
- ✅ Persona parameter support

### 2. Persona System (`tests/integration/test_personas.py`)
- ✅ All 5 personas exist (Developer, PM, Customer, Sales, Shareholder)
- ✅ Each persona has unique focus areas
- ✅ Persona-specific requirement formats
- ✅ Different perspectives on same requirements

### 3. Requirements Extraction (`tests/requirements/test_extraction.py`)
- ✅ Extract requirement ID (REQ-XXX-NNN)
- ✅ Extract category, priority, description
- ✅ Extract acceptance criteria
- ✅ Extract dependencies
- ✅ Validate requirement completeness

### 4. IEEE 29148 Compliance (`tests/requirements/test_ieee_compliance.py`)
- ✅ Unique identifiers
- ✅ Clear descriptions
- ✅ Rationale/justification
- ✅ Priority levels
- ✅ Verification methods
- ✅ Unambiguous language
- ✅ Testable criteria

### 5. Multi-Agent Collaboration (`tests/integration/test_multi_agent.py`)
- 🔄 Orchestrator agent (placeholder for future)
- 🔄 Agent-to-agent communication (placeholder)
- 🔄 Requirement conflict detection (placeholder)
- 🔄 Requirement synthesis (placeholder)
- 🔄 Database & RAG (placeholder)
- 🔄 Feedback loops (placeholder)

Legend:
- ✅ Currently tested
- 🔄 Placeholder for future implementation

## Common Test Commands

```bash
# Run specific test file
pytest tests/backend/test_api.py -v

# Run specific test function
pytest tests/backend/test_api.py::test_health_endpoint -v

# Run tests matching pattern
pytest -k "test_extract" -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

## Test Results Interpretation

### ✅ All Passing
```
tests/backend/test_api.py ......              [ 40%]
tests/integration/test_personas.py ....       [ 70%]
tests/requirements/test_extraction.py .....   [100%]

====== 15 passed in 2.34s ======
```
All tests passed! Code is working as expected.

### ❌ Some Failing
```
tests/backend/test_api.py .F....              [ 40%]
FAILED tests/backend/test_api.py::test_generate - AssertionError

====== 1 failed, 14 passed in 2.45s ======
```
One test failed. Check the error message and fix the code.

### ⚠️ Some Skipped
```
tests/integration/test_multi_agent.py s....   [100%]

====== 4 passed, 1 skipped in 1.23s ======
```
Some tests were skipped (usually requires_llm tests).

## Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

Target: **>80% code coverage**

## Persona Testing Examples

### Test Developer Persona
```bash
pytest tests/integration/test_personas.py::TestDeveloperPersona -v
```

### Test All Persona Perspectives
```bash
pytest tests/integration/test_personas.py::TestPersonaInteractions -v
```

## Requirements Testing Examples

### Test Requirement Extraction
```bash
pytest tests/requirements/test_extraction.py -v
```

### Test IEEE Compliance
```bash
pytest tests/requirements/test_ieee_compliance.py -v
```

## Mock Data

Mock responses for each persona are available in `tests/fixtures/mock_responses.py`:

```python
from tests.fixtures.mock_responses import DEVELOPER_RESPONSES

# Developer response for authentication requirement
auth_response = DEVELOPER_RESPONSES["authentication_requirement"]
```

Test scenarios are in `tests/fixtures/test_scenarios.py`:

```python
from tests.fixtures.test_scenarios import FOOD_DELIVERY_SCENARIO

# Access stakeholder inputs
customer_input = FOOD_DELIVERY_SCENARIO["stakeholder_inputs"]["customer"]
```

## Troubleshooting

### Import Errors
```bash
# Run from project root
cd /path/to/SEproj1a1
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
pytest
```

### Missing Dependencies
```bash
pip install -r tests/requirements.txt
pip install -r src/requirements.txt
```

### vLLM Engine Not Available
Unit tests should mock the engine. If you see engine errors, ensure tests use `@patch('app.engine.get_engine')`.

## Adding New Tests

1. Create test file in appropriate directory:
   - `tests/backend/` for API tests
   - `tests/integration/` for persona/collaboration tests
   - `tests/requirements/` for requirement validation tests

2. Use appropriate markers:
   ```python
   @pytest.mark.unit
   def test_my_feature():
       assert True
   ```

3. Write descriptive test names:
   ```python
   def test_developer_persona_extracts_technical_requirements():
       """Test that developer persona includes technical details."""
       pass
   ```

4. Run your new tests:
   ```bash
   pytest tests/your_new_test.py -v
   ```

## CI/CD Integration

Tests should run automatically on:
- Push to any branch
- Pull requests
- Merges to main

Ensure all tests pass before merging!

## More Information

For detailed documentation, see [tests/README.md](tests/README.md).

For MARC system overview, see [README.md](README.md).
