# MARC Testing Documentation

This directory contains the testing apparatus for the MARC (Multi-Agent Requirement Collaboration) system.

## Overview

MARC is a framework for collaborative, LLM-powered Requirements Engineering documentation through multi-agent collaboration. The testing suite validates:

1. **Backend API functionality** - FastAPI endpoints, request/response handling
2. **Persona system** - Different stakeholder perspectives (Developer, PM, Customer, Sales, Shareholder)
3. **Requirements extraction** - Parsing and validating structured requirements from LLM responses
4. **IEEE 29148 compliance** - Ensuring requirements meet industry standards
5. **Multi-agent collaboration** - Testing future features for agent-to-agent communication

## Directory Structure

```
tests/
├── README.md                          # This file
├── requirements.txt                   # Test dependencies
├── conftest.py                        # Shared pytest fixtures
├── backend/                           # Backend API tests
│   ├── test_api.py                   # API endpoint tests
│   └── test_engine.py                # LLM engine tests
├── integration/                       # Integration tests
│   ├── test_personas.py              # Persona system tests
│   └── test_multi_agent.py           # Multi-agent collaboration tests
├── requirements/                      # Requirements extraction tests
│   ├── test_extraction.py            # Requirement parsing tests
│   └── test_ieee_compliance.py       # IEEE standard compliance tests
└── fixtures/                          # Test fixtures and mock data
    ├── mock_responses.py             # Mock LLM responses for each persona
    └── test_scenarios.py             # Realistic test scenarios
```

## Installation

### 1. Install Test Dependencies

```bash
# From the project root directory
pip install -r tests/requirements.txt

# Also install the main project dependencies
pip install -r src/requirements.txt
```

### 2. Verify Installation

```bash
pytest --version
# Should show pytest 8.0.0 or higher
```

## Running Tests

### Run All Tests

```bash
# From the project root directory
pytest
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Tests that require LLM (skip by default)
pytest -m requires_llm
```

### Run Specific Test Files

```bash
# Backend API tests
pytest tests/backend/test_api.py

# Persona system tests
pytest tests/integration/test_personas.py

# Requirements extraction tests
pytest tests/requirements/test_extraction.py

# IEEE compliance tests
pytest tests/requirements/test_ieee_compliance.py
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/backend/test_api.py::TestGenerateEndpoint

# Run a specific test function
pytest tests/requirements/test_extraction.py::test_extract_requirement_id
```

### Run with Coverage

```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# View coverage report
# Open htmlcov/index.html in a browser
```

### Run with Verbose Output

```bash
# Show detailed test output
pytest -v

# Show even more detail (including print statements)
pytest -vv -s
```

## Test Markers

Tests are organized with pytest markers:

- `@pytest.mark.unit` - Fast unit tests (no external dependencies)
- `@pytest.mark.integration` - Integration tests (may require services)
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.requires_llm` - Tests that need actual LLM connection

## Test Fixtures

Common fixtures are defined in `conftest.py`:

- `sample_messages` - Basic chat messages for testing
- `developer_persona_messages` - Messages with developer context
- `pm_persona_messages` - Messages with PM context
- `mock_llm_response` - Mock LLM completion response
- `mock_streaming_response` - Mock streaming response chunks
- `all_personas` - List of all persona keys
- `sample_requirements` - Sample structured requirements

## Writing New Tests

### Example: Unit Test for API Endpoint

```python
import pytest
from fastapi.testclient import TestClient

@pytest.mark.unit
def test_new_endpoint(client):
    """Test description."""
    response = client.get("/api/new-endpoint")
    assert response.status_code == 200
    assert "expected_field" in response.json()
```

### Example: Integration Test for Persona

```python
import pytest

@pytest.mark.integration
class TestNewPersona:
    """Test suite for new persona."""

    def test_persona_behavior(self):
        """Test specific persona behavior."""
        # Test implementation
        assert True
```

### Example: Requirements Extraction Test

```python
import pytest
from tests.requirements.test_extraction import RequirementExtractor

@pytest.mark.unit
def test_extract_new_field():
    """Test extraction of a new requirement field."""
    text = "New Field: value"
    result = RequirementExtractor.extract_new_field(text)
    assert result == "value"
```

## Testing Different Personas

Each persona has specific behaviors and output formats:

### Developer Persona
- Focus: Technical feasibility, implementation details
- Requirements: REQ-DEV-XXX format
- Includes: Technical notes, dependencies, acceptance criteria

### Product Manager Persona
- Focus: User value, business metrics, prioritization
- Requirements: REQ-PM-XXX format
- Includes: User stories, success metrics, business value

### Customer Persona
- Focus: Usability, value, simplicity
- Requirements: REQ-CUST-XXX format
- Includes: Customer stories, pain points, usability notes

### Sales Persona
- Focus: Value proposition, competitive positioning
- Requirements: REQ-MKT-XXX format
- Includes: Messaging, go-to-market strategy, sales enablement

### Shareholder Persona
- Focus: Financial returns, ROI, risk management
- Requirements: REQ-SH-XXX format
- Includes: Financial metrics, risk assessment, strategic value

## Mock Responses

Mock LLM responses are provided in `tests/fixtures/mock_responses.py`:

```python
from tests.fixtures.mock_responses import DEVELOPER_RESPONSES

# Use in tests
mock_response = DEVELOPER_RESPONSES["authentication_requirement"]
```

Available mock responses:
- `DEVELOPER_RESPONSES` - Developer persona responses
- `PM_RESPONSES` - Product Manager persona responses
- `CUSTOMER_RESPONSES` - Customer persona responses
- `SALES_RESPONSES` - Sales persona responses
- `SHAREHOLDER_RESPONSES` - Shareholder persona responses
- `STREAMING_RESPONSES` - Chunked streaming responses
- `ERROR_RESPONSES` - Error and edge case responses

## Test Scenarios

Realistic test scenarios are provided in `tests/fixtures/test_scenarios.py`:

- `FOOD_DELIVERY_SCENARIO` - Food delivery app (from MARC pamphlet)
- `HEALTHCARE_PORTAL_SCENARIO` - Healthcare patient portal
- `ECOMMERCE_SCENARIO` - E-commerce platform

These scenarios include:
- Stakeholder inputs for each persona
- Expected requirement conflicts
- Sample synthesized requirements

## IEEE 29148 Compliance Testing

Tests verify that requirements follow IEEE 29148 standard:

- Unique identifier
- Clear description
- Rationale
- Priority
- Verification method (acceptance criteria)
- Unambiguous language
- Testable/measurable criteria

Run compliance tests:

```bash
pytest tests/requirements/test_ieee_compliance.py -v
```

## Future Features (Placeholders)

Some tests are placeholders for future functionality:

1. **Orchestrator Agent** - Synthesizes requirements from all personas
2. **Multi-Agent Communication** - Agent-to-agent collaboration
3. **Database & RAG** - Requirement storage and retrieval
4. **Feedback Loop** - Stakeholder critiques and updates
5. **Real-time Updates** - Emergency requirement changes
6. **Automated Progress Updates** - Status notifications

These tests currently `assert True` as placeholders and will be implemented as features are built.

## Continuous Integration

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
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r tests/requirements.txt
          pip install -r src/requirements.txt
      - name: Run tests
        run: pytest -v --cov=src
```

## Troubleshooting

### Import Errors

If you encounter import errors:

```bash
# Make sure you're running from the project root
cd /path/to/SEproj1a1

# Verify Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Run tests
pytest
```

### vLLM Engine Errors

Tests that require the actual vLLM engine will fail if it's not available. These should be mocked in unit tests:

```python
from unittest.mock import patch

@patch('app.engine.get_engine')
def test_with_mocked_engine(mock_get_engine):
    # Test implementation
    pass
```

### FastAPI TestClient Issues

Ensure you have the correct dependencies:

```bash
pip install 'fastapi[all]' httpx
```

## Best Practices

1. **Mock External Dependencies** - Don't call real LLMs in unit tests
2. **Use Fixtures** - Reuse common test data via fixtures
3. **Test Edge Cases** - Test error conditions, not just happy path
4. **Keep Tests Fast** - Unit tests should run in < 1 second
5. **Descriptive Names** - Test names should describe what they test
6. **One Assertion per Test** - Makes failures easier to debug
7. **Use Markers** - Tag tests appropriately (unit, integration, slow)

## Contributing

When adding new features to MARC:

1. Write tests first (TDD approach)
2. Ensure tests pass locally: `pytest`
3. Check coverage: `pytest --cov=src`
4. Add docstrings to test functions
5. Update this README if adding new test categories

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [IEEE 29148 Standard](https://standards.ieee.org/standard/29148-2018.html)
- [MARC Project Documentation](../README.md)

## Contact

For questions about testing, see the main project README or open an issue.
