"""
Shared pytest fixtures for MARC testing.
"""
import pytest
from typing import AsyncGenerator, Dict, List
from unittest.mock import AsyncMock, MagicMock

# Mark all tests as async-compatible
pytest_plugins = ('pytest_asyncio',)


@pytest.fixture
def sample_messages() -> List[Dict[str, str]]:
    """Sample chat messages for testing."""
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is MARC?"},
    ]


@pytest.fixture
def developer_persona_messages() -> List[Dict[str, str]]:
    """Sample messages with developer persona context."""
    return [
        {
            "role": "system",
            "content": "You are a Requirements Engineering Assistant for developers.",
        },
        {
            "role": "user",
            "content": "I need to implement a user authentication system with OAuth2.",
        },
    ]


@pytest.fixture
def pm_persona_messages() -> List[Dict[str, str]]:
    """Sample messages with product manager persona context."""
    return [
        {
            "role": "system",
            "content": "You are a Requirements Engineering Assistant for product managers.",
        },
        {
            "role": "user",
            "content": "We need a dashboard to track user engagement metrics.",
        },
    ]


@pytest.fixture
def mock_llm_response() -> str:
    """Mock LLM response for testing."""
    return (
        "Based on your requirement, here's a structured approach:\n\n"
        "REQ-DEV-001: User Authentication System\n"
        "Category: Functional\n"
        "Priority: Must-have\n"
        "Description: The system shall implement OAuth2 authentication.\n"
        "Acceptance Criteria:\n"
        "- Support OAuth2 authorization code flow\n"
        "- Integrate with Google and GitHub providers\n"
        "- Secure token storage\n"
        "- Session management with JWT\n"
    )


@pytest.fixture
def mock_streaming_response() -> List[str]:
    """Mock streaming LLM response chunks."""
    return [
        "Based on ",
        "your requirement, ",
        "here's a ",
        "structured approach:\n\n",
        "REQ-DEV-001: ",
        "User Authentication ",
        "System\n",
    ]


@pytest.fixture
def mock_engine():
    """Mock vLLM engine for testing."""
    mock = MagicMock()
    mock.add_request = AsyncMock()

    async def mock_stream():
        # Mock streaming output
        mock_output = MagicMock()
        mock_output.outputs = [MagicMock(text="Test response")]
        yield mock_output

    mock.get_request_stream = MagicMock(return_value=mock_stream())
    mock.abort_request = AsyncMock()
    return mock


@pytest.fixture
def all_personas() -> List[str]:
    """List of all available persona keys."""
    return ['developer', 'pm', 'customer', 'sales', 'shareholder']


@pytest.fixture
def sample_requirements() -> Dict[str, List[Dict]]:
    """Sample requirements organized by persona."""
    return {
        "developer": [
            {
                "id": "REQ-DEV-001",
                "category": "Functional",
                "priority": "Must-have",
                "description": "The system shall implement OAuth2 authentication",
                "acceptance_criteria": [
                    "Support OAuth2 authorization code flow",
                    "Integrate with Google and GitHub providers",
                ],
            }
        ],
        "pm": [
            {
                "id": "REQ-PM-001",
                "category": "User Story",
                "priority": "Must-have (P0)",
                "user_story": "As a product manager, I want to track user engagement metrics so that I can make data-driven decisions",
                "acceptance_criteria": [
                    "Dashboard displays daily active users",
                    "Shows user retention over time",
                ],
            }
        ],
    }


@pytest.fixture
def mock_requirement_response() -> str:
    """Mock response containing structured requirements."""
    return """
REQ-DEV-001: API Rate Limiting
Category: Non-Functional (Performance)
Priority: Must-have

Description: The system shall implement rate limiting on all API endpoints to prevent abuse.

Acceptance Criteria:
- Limit to 100 requests per minute per user
- Return 429 status code when limit exceeded
- Include retry-after header in response
- Track rate limits per API key

Technical Notes:
- Use Redis for distributed rate limiting
- Implement sliding window algorithm
- Monitor rate limit violations

Dependencies: REQ-DEV-002 (API Authentication)
"""
