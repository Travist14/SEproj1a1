# Code Standards

Coding standards and conventions for MARC development.

## General Principles

1. **Readability First**: Code is read more often than written
2. **Consistency**: Follow existing patterns
3. **Simplicity**: Choose the simplest solution that works
4. **Documentation**: Document why, not what
5. **Testing**: Write tests for all new code

## Python Standards (Backend)

### Style Guide

Follow **PEP 8** with **Black** formatting:

```bash
# Format code
black src/backend

# Check style
flake8 src/backend
```

### Naming Conventions

```python
# Variables and functions: snake_case
user_count = 10
def calculate_total(items):
    pass

# Classes: PascalCase
class UserManager:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Private: leading underscore
def _internal_helper():
    pass

# Protected: single underscore
class MyClass:
    def _protected_method(self):
        pass
```

### Type Hints

Always use type hints:

```python
from typing import List, Dict, Optional, Union

def process_messages(
    messages: List[ChatMessage],
    max_tokens: int = 512,
    temperature: float = 0.7
) -> Dict[str, Any]:
    """Process chat messages."""
    pass

# Optional for nullable values
def get_user(user_id: str) -> Optional[User]:
    """Get user by ID, returns None if not found."""
    pass

# Union for multiple types
def parse_input(data: Union[str, dict]) -> dict:
    """Parse input from string or dict."""
    pass
```

### Docstrings

Use **Google Style** docstrings:

```python
def generate_requirement(
    persona: str,
    prompt: str,
    max_tokens: int = 512
) -> str:
    """Generate a requirement from persona and prompt.

    This function uses the specified persona's system prompt
    to generate an IEEE 29148-compliant requirement.

    Args:
        persona: The persona key (developer, product_manager, etc.)
        prompt: User's requirement description
        max_tokens: Maximum tokens to generate (default: 512)

    Returns:
        Generated requirement text in IEEE 29148 format

    Raises:
        ValueError: If persona is invalid
        RuntimeError: If LLM engine is not available

    Example:
        >>> req = generate_requirement("developer", "Build auth")
        >>> print(req[:20])
        "REQ-DEV-001: User..."
    """
    pass
```

### Code Organization

```python
"""Module for chat message handling.

This module provides classes and functions for processing
chat messages in the MARC system.
"""

# Standard library imports
import asyncio
import logging
from typing import List, Optional

# Third-party imports
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Local imports
from app.config import settings
from app.utils import format_prompt

# Module-level constants
LOGGER = logging.getLogger(__name__)
MAX_RETRIES = 3

# Classes
class ChatMessage(BaseModel):
    """Represents a single chat message."""
    pass

# Functions
def process_messages(messages: List[ChatMessage]) -> str:
    """Process chat messages into prompt."""
    pass
```

### Error Handling

```python
# Specific exceptions
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logger.exception("Unexpected error")
    raise HTTPException(status_code=500, detail="Internal server error")

# Don't catch Exception unless necessary
# Don't use bare except:
```

### Async/Await

```python
# Use async for I/O-bound operations
async def fetch_data(url: str) -> dict:
    """Fetch data from URL asynchronously."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Use await for async function calls
result = await fetch_data("http://example.com")

# Use asyncio.gather for parallel operations
results = await asyncio.gather(
    fetch_data(url1),
    fetch_data(url2),
    fetch_data(url3)
)
```

## JavaScript Standards (Frontend)

### Style Guide

Use **ESLint** with **Prettier**:

```bash
# Check lint
npm run lint

# Fix automatically
npm run lint:fix

# Format with Prettier
npm run format
```

### Naming Conventions

```javascript
// Variables and functions: camelCase
const userCount = 10;
function calculateTotal(items) {}

// Components: PascalCase
function ChatWindow({ messages }) {}

// Constants: UPPER_SNAKE_CASE
const MAX_RETRIES = 3;
const API_BASE_URL = "http://localhost:8001";

// Private: leading underscore (convention)
function _internalHelper() {}

// Boolean: is/has prefix
const isLoading = true;
const hasError = false;
```

### Component Structure

```javascript
import { useState, useEffect } from 'react';
import PropTypes from 'prop-types';

/**
 * ChatWindow displays the chat message history.
 *
 * @param {Object} props - Component props
 * @param {Array} props.messages - Array of message objects
 * @returns {JSX.Element} The rendered component
 */
export function ChatWindow({ messages }) {
  // Hooks at the top
  const [isScrolled, setIsScrolled] = useState(false);
  const containerRef = useRef(null);

  // Effects
  useEffect(() => {
    // Auto-scroll logic
  }, [messages]);

  // Event handlers
  const handleScroll = () => {
    setIsScrolled(true);
  };

  // Render helpers (if needed)
  const renderMessage = (msg, idx) => (
    <div key={idx} className={`message ${msg.role}`}>
      {msg.content}
    </div>
  );

  // Return JSX
  return (
    <div ref={containerRef} onScroll={handleScroll}>
      {messages.map(renderMessage)}
    </div>
  );
}

// PropTypes
ChatWindow.propTypes = {
  messages: PropTypes.arrayOf(
    PropTypes.shape({
      role: PropTypes.oneOf(['user', 'assistant']).isRequired,
      content: PropTypes.string.isRequired
    })
  ).isRequired
};
```

### Hooks Best Practices

```javascript
// Custom hooks start with "use"
function useChat(personaKey) {
  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState('idle');

  // Logic...

  return { messages, status };
}

// Dependencies array
useEffect(() => {
  // Effect code
}, [dependency1, dependency2]); // Only re-run if these change

// Cleanup
useEffect(() => {
  const subscription = subscribe();

  return () => {
    subscription.unsubscribe();
  };
}, []);
```

### Comments

```javascript
// Good: Explain WHY
// Debounce to avoid too many API calls
const debouncedSend = debounce(sendMessage, 300);

// Bad: Explain WHAT (code is self-explanatory)
// Set messages to empty array
setMessages([]);

// JSDoc for functions
/**
 * Stream generation from API.
 *
 * @param {Object} payload - Request payload
 * @param {Function} onChunk - Callback for each token
 * @param {AbortSignal} signal - Abort signal for cancellation
 * @returns {Promise<void>}
 * @throws {Error} If request fails
 */
async function streamGenerate(payload, onChunk, signal) {
  // Implementation...
}
```

## File Naming

### Python Files

- Modules: `snake_case.py`
- Tests: `test_<module>.py`
- Example: `chat_handler.py`, `test_chat_handler.py`

### JavaScript Files

- Components: `PascalCase.jsx`
- Hooks: `camelCase.js` (with `use` prefix)
- Utilities: `camelCase.js`
- Example: `ChatWindow.jsx`, `useChat.js`, `apiClient.js`

## Git Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Build, config, dependencies

### Examples

```bash
# Good
git commit -m "feat(backend): Add multi-agent orchestration"
git commit -m "fix(frontend): Resolve streaming timeout issue"
git commit -m "docs(api): Update REST API documentation"

# With body
git commit -m "feat(personas): Add shareholder persona

- Add shareholder persona configuration
- Update persona selection UI
- Add tests for shareholder requirements

Closes #42"
```

## Code Review Checklist

### Before Submitting PR

- [ ] Code follows style guide
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation updated
- [ ] No console.log or debug prints
- [ ] No commented-out code
- [ ] Meaningful variable names
- [ ] Error handling added
- [ ] Type hints/PropTypes present

### During Review

**Reviewers should check**:

1. **Correctness**: Does it work as intended?
2. **Style**: Follows code standards?
3. **Tests**: Adequate test coverage?
4. **Documentation**: Well-documented?
5. **Performance**: Any concerns?
6. **Security**: Any vulnerabilities?
7. **Maintainability**: Easy to understand and modify?

## Project Structure Standards

### Backend Structure

```
src/backend/
├── app/
│   ├── __init__.py       # Package initialization
│   ├── main.py           # FastAPI app and endpoints
│   ├── models/           # Pydantic models (if growing)
│   ├── services/         # Business logic (if needed)
│   ├── utils/            # Utility functions
│   └── config.py         # Configuration
└── requirements.txt      # Dependencies
```

### Frontend Structure

```
src/frontend/
├── src/
│   ├── components/       # React components
│   ├── hooks/            # Custom hooks
│   ├── api/              # API clients
│   ├── config/           # Configuration
│   ├── utils/            # Utility functions
│   ├── styles/           # CSS files (if separate)
│   ├── App.jsx           # Root component
│   └── main.jsx          # Entry point
├── public/               # Static assets
└── package.json          # Dependencies
```

## Documentation Standards

### README Structure

1. **Title** and badges
2. **Overview**: What is it?
3. **Features**: Key capabilities
4. **Quick Start**: Get running fast
5. **Installation**: Detailed setup
6. **Usage**: How to use
7. **Testing**: How to test
8. **Contributing**: How to contribute
9. **License**: License info

### Code Comments

```python
# Good: Explain non-obvious decisions
# Use exponential backoff to avoid rate limiting
await asyncio.sleep(2 ** retry_count)

# Bad: Redundant comments
# Increment counter
counter += 1
```

### API Documentation

Use OpenAPI/Swagger for REST APIs (automatically generated by FastAPI).

For additional docs:
- Endpoint purpose
- Request/response examples
- Error codes
- Rate limits
- Authentication requirements

## Performance Guidelines

### Backend

- Use async/await for I/O operations
- Implement connection pooling
- Cache frequently accessed data
- Use pagination for large datasets
- Profile before optimizing

### Frontend

- Lazy load components
- Memoize expensive computations
- Debounce user input
- Optimize re-renders
- Bundle size optimization

## Security Guidelines

- Never commit secrets/keys
- Validate all user input
- Use parameterized queries
- Implement rate limiting
- Keep dependencies updated
- Use HTTPS in production
- Sanitize error messages (don't leak internals)

## Next Steps

- [Contributing Guide](contributing.md) - How to contribute
- [Testing Guide](testing.md) - Testing standards
- [Architecture](../architecture/overview.md) - System design
