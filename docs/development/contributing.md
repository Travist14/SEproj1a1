# Contributing to MARC

Thank you for your interest in contributing to MARC! This guide will help you get started.

## Getting Started

### 1. Fork and Clone

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/SEproj1a1.git
cd SEproj1a1

# Add upstream remote
git remote add upstream https://github.com/original/SEproj1a1.git
```

### 2. Set Up Development Environment

```bash
# Backend
cd src/backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r ../../tests/requirements.txt  # Test dependencies

# Frontend
cd ../frontend
npm install
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

## Development Workflow

### 1. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add comments for complex logic
- Update documentation as needed

### 2. Write Tests

```bash
# Add tests for new features
touch tests/backend/test_your_feature.py

# Run tests
pytest
```

### 3. Run Linters

```bash
# Python (backend)
black src/backend
flake8 src/backend

# JavaScript (frontend)
cd src/frontend
npm run lint
```

### 4. Test Locally

```bash
# Start backend
cd src/backend
uvicorn app.main:app --reload

# Start frontend (new terminal)
cd src/frontend
npm run dev

# Run tests
pytest --cov=src
```

### 5. Commit Changes

```bash
# Stage changes
git add .

# Commit with clear message
git commit -m "feat: Add multi-agent orchestration"
# or
git commit -m "fix: Resolve streaming timeout issue"
```

**Commit Message Format**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring
- `style:` Code style changes
- `chore:` Build/config changes

### 6. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

## Pull Request Guidelines

### PR Checklist

- [ ] Code follows project style guide
- [ ] All tests pass (`pytest`)
- [ ] New features have tests
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] PR description explains changes
- [ ] No merge conflicts

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All existing tests pass
- [ ] Added tests for new features
- [ ] Manually tested changes

## Screenshots (if applicable)
Add screenshots for UI changes
```

## Code Style Guidelines

### Python (Backend)

**Style**: PEP 8 + Black formatting

```python
# Good
def format_chat_prompt(messages: List[ChatMessage]) -> str:
    """Convert structured chat messages into plain-text prompt.

    Args:
        messages: List of ChatMessage objects

    Returns:
        Formatted prompt string

    Raises:
        ValueError: If messages list is empty
    """
    if not messages:
        raise ValueError("At least one message is required.")

    # Implementation...
```

**Key Points**:
- Type hints for all function parameters and returns
- Docstrings for all public functions (Google style)
- Use `async/await` for async functions
- Maximum line length: 88 characters (Black default)

### JavaScript (Frontend)

**Style**: ESLint + Prettier

```javascript
// Good
export function ChatWindow({ messages }) {
  const containerRef = useRef(null);

  useEffect(() => {
    // Auto-scroll to bottom
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <div ref={containerRef} className="chat-window">
      {messages.map((msg, idx) => (
        <Message key={idx} role={msg.role} content={msg.content} />
      ))}
    </div>
  );
}
```

**Key Points**:
- Functional components with hooks
- PropTypes or TypeScript types
- Destructure props
- Use `const` over `let`

## Testing Guidelines

### Writing Tests

**Backend Tests**:
```python
import pytest
from fastapi.testclient import TestClient

def test_health_endpoint(client):
    """Test health check returns OK status."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

**Frontend Tests** (if adding):
```javascript
import { render, screen } from '@testing-library/react';
import { ChatWindow } from './ChatWindow';

test('renders messages', () => {
  const messages = [
    { role: 'user', content: 'Hello' }
  ];

  render(<ChatWindow messages={messages} />);

  expect(screen.getByText('Hello')).toBeInTheDocument();
});
```

### Test Coverage

- Maintain 80%+ code coverage
- Test happy paths and edge cases
- Test error handling
- Mock external dependencies

## Documentation Guidelines

### Code Documentation

```python
def complex_function(param1: str, param2: int) -> Dict[str, Any]:
    """Brief one-line description.

    More detailed description if needed. Explain the purpose,
    not just what the code does.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When param1 is invalid
        HTTPException: When API call fails

    Example:
        >>> result = complex_function("test", 42)
        >>> print(result["status"])
        "success"
    """
    # Implementation...
```

### README Updates

When adding features, update:
- `README.md` - If it affects quick start or features
- `docs/` - Add detailed documentation
- `TESTING.md` - If adding test categories

## Areas to Contribute

### High Priority

1. **Multi-Agent Orchestration**
   - Implement orchestrator agent
   - Parallel persona execution
   - Conflict detection

2. **Frontend Enhancements**
   - Requirement export (PDF, Markdown)
   - Side-by-side persona comparison
   - History/search functionality

3. **Testing**
   - Increase coverage to 90%+
   - Add frontend tests
   - Performance tests

4. **Documentation**
   - Tutorial videos
   - More code examples
   - Architecture diagrams

### Medium Priority

1. **RAG Integration**
   - Vector database for requirements
   - Similarity search
   - Learning from past requirements

2. **API Enhancements**
   - Authentication/API keys
   - Rate limiting
   - WebSocket support

3. **UI/UX Improvements**
   - Dark mode
   - Keyboard shortcuts
   - Mobile optimization

### Good First Issues

Look for issues labeled `good-first-issue`:
- Documentation improvements
- Test additions
- Small bug fixes
- Code formatting

## Getting Help

### Communication

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Questions and ideas
- **Pull Requests**: Code review and feedback

### Resources

- [Architecture Documentation](../architecture/overview.md)
- [API Reference](../api/rest-api.md)
- [Testing Guide](testing.md)
- [Code Standards](standards.md)

## Code Review Process

### What Reviewers Look For

1. **Correctness**: Does it work as intended?
2. **Tests**: Are there adequate tests?
3. **Style**: Does it follow code standards?
4. **Documentation**: Is it well-documented?
5. **Performance**: Any performance concerns?
6. **Security**: Any security issues?

### Responding to Feedback

- Be open to feedback
- Ask questions if unclear
- Make requested changes
- Update PR description if scope changes
- Request re-review after changes

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Acknowledged in documentation

Thank you for contributing to MARC!
