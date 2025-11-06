# Backend API Documentation

Python module and class documentation for MARC backend.

## Module: app.main

**Location**: `src/backend/app/main.py`

### Classes

#### ChatMessage

**Purpose**: Single message exchanged in chat conversation

```python
class ChatMessage(BaseModel):
    role: str  # system|user|assistant
    content: str
```

**Fields**:
- `role` (str): Message author role. Must be one of: `system`, `user`, `assistant`
- `content` (str): Text content of the message

**Validation**:
- Role is validated against allowed values
- Content must be non-empty string

**Example**:
```python
message = ChatMessage(
    role="user",
    content="Build user authentication"
)
```

---

#### GenerateRequest

**Purpose**: Request payload for /generate endpoint

```python
class GenerateRequest(BaseModel):
    messages: List[ChatMessage]
    stream: bool = True
    max_tokens: int = DEFAULT_MAX_TOKENS
    temperature: float = DEFAULT_TEMPERATURE
    top_p: float = DEFAULT_TOP_P
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    stop: Optional[List[str]] = None
    persona: Optional[str] = None
```

**Fields**:
- `messages`: Ordered list of chat messages (required)
- `stream`: Enable token streaming (default: True)
- `max_tokens`: Maximum tokens to generate (≥1, default: 512)
- `temperature`: Sampling temperature (0.0-2.0, default: 0.7)
- `top_p`: Nucleus sampling threshold (0.0-1.0, default: 0.95)
- `presence_penalty`: Presence penalty (-2.0 to 2.0, default: 0.0)
- `frequency_penalty`: Frequency penalty (-2.0 to 2.0, default: 0.0)
- `stop`: Optional stop sequences
- `persona`: Optional persona identifier (informational)

**Example**:
```python
request = GenerateRequest(
    messages=[
        ChatMessage(role="system", content="You are a developer."),
        ChatMessage(role="user", content="Build authentication")
    ],
    stream=True,
    max_tokens=512,
    temperature=0.7
)
```

---

#### EngineManager

**Purpose**: Lazy-initializes and caches AsyncLLMEngine singleton

```python
class EngineManager:
    def __init__(self) -> None
    @property
    def is_ready(self) -> bool
    async def get_engine(self) -> AsyncLLMEngine
```

**Methods**:

##### `__init__`
Initialize the engine manager.

```python
manager = EngineManager()
```

##### `is_ready` (property)
Check if engine is initialized.

**Returns**: `bool` - True if engine is ready

```python
if engine_manager.is_ready:
    print("Engine loaded")
```

##### `get_engine` (async)
Get or initialize the singleton engine instance.

**Returns**: `AsyncLLMEngine` - The vLLM engine

**Raises**: `RuntimeError` - If vLLM is not available

```python
engine = await engine_manager.get_engine()
```

**Thread Safety**: Uses asyncio.Lock for concurrent access

**Implementation Details**:
- First call initializes engine (slow)
- Subsequent calls return cached instance (fast)
- Reads model configuration from environment variables
- Logs model initialization

---

### Functions

#### format_chat_prompt

Convert structured chat messages into plain-text prompt.

```python
def format_chat_prompt(messages: List[ChatMessage]) -> str
```

**Parameters**:
- `messages`: List of ChatMessage objects

**Returns**: `str` - Formatted prompt string

**Raises**: `ValueError` - If messages list is empty

**Example**:
```python
messages = [
    ChatMessage(role="system", content="You are helpful."),
    ChatMessage(role="user", content="Hello")
]

prompt = format_chat_prompt(messages)
# Output:
# System: You are helpful.
#
# User: Hello
#
# Assistant:
```

**Format**:
```
{Role}: {content}

{Role}: {content}