# Backend Architecture

Deep dive into the FastAPI backend architecture, design patterns, and implementation details.

## Technology Stack

- **FastAPI**: Modern async web framework
- **Uvicorn**: ASGI server for FastAPI
- **vLLM**: Optimized LLM inference engine
- **Pydantic**: Data validation and settings management
- **Python 3.10+**: Type hints and modern Python features

## Module Structure

```
src/backend/
├── app/
│   ├── __init__.py         # Module initialization
│   └── main.py             # FastAPI application
└── requirements.txt        # Python dependencies
```

## Core Components

### 1. FastAPI Application

Located in `src/backend/app/main.py:121`

```python
app = FastAPI(title="SEproj Chat Backend", version="0.1.0")
```

**Configuration**:
- CORS middleware for cross-origin requests
- Automatic OpenAPI documentation
- Request/response validation

### 2. EngineManager (Singleton)

Located in `src/backend/app/main.py:77`

**Purpose**: Lazy initialization and caching of the vLLM engine

**Key Methods**:
- `get_engine()`: Returns singleton AsyncLLMEngine instance
- `is_ready`: Property to check if engine is initialized

**Implementation**:
```python
class EngineManager:
    def __init__(self) -> None:
        self._engine: Optional[AsyncLLMEngine] = None
        self._lock = asyncio.Lock()

    async def get_engine(self) -> AsyncLLMEngine:
        if self._engine is not None:
            return self._engine

        async with self._lock:
            if self._engine is not None:
                return self._engine
            # Initialize engine...
```

**Thread Safety**: Uses asyncio.Lock for concurrent access

### 3. Data Models (Pydantic)

#### ChatMessage

Located in `src/backend/app/main.py:37`

```python
class ChatMessage(BaseModel):
    role: str  # system|user|assistant
    content: str
```

**Validation**:
- Role must be one of: system, user, assistant
- Custom validator ensures role validity

#### GenerateRequest

Located in `src/backend/app/main.py:52`

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

**Validation Rules**:
- `max_tokens`: ≥ 1
- `temperature`: 0.0 to 2.0
- `top_p`: 0.0 to 1.0
- Penalties: -2.0 to 2.0

## API Endpoints

### GET /health

Located in `src/backend/app/main.py:213`

**Purpose**: Health check with engine status

**Response**:
```json
{
  "status": "ok",
  "model": "Qwen/Qwen3-4B",
  "engine_ready": true
}
```

**Status Codes**:
- 200: Model configured and ready
- 503: Model not configured

### POST /generate

Located in `src/backend/app/main.py:226`

**Purpose**: Generate chat completions with optional streaming

**Request Body**:
```json
{
  "messages": [
    {"role": "system", "content": "You are a developer..."},
    {"role": "user", "content": "Build user authentication"}
  ],
  "stream": true,
  "max_tokens": 512,
  "temperature": 0.7,
  "top_p": 0.95
}
```

**Streaming Response** (NDJSON):
```json
{"type": "token", "delta": "REQ", "content": "REQ", "request_id": "abc123"}
{"type": "token", "delta": "-DEV", "content": "REQ-DEV", "request_id": "abc123"}
{"type": "done", "content": "...", "finish_reason": "stop", "request_id": "abc123"}
```

**Non-Streaming Response**:
```json
{
  "output": "Generated requirement...",
  "finish_reason": "stop",
  "request_id": "abc123"
}
```

### POST /api/generate

Alias for `/generate` to support different routing patterns.

## Request Processing Flow

### 1. Request Validation

```python
@app.post("/generate")
async def generate(payload: GenerateRequest):
    # FastAPI automatically validates payload against GenerateRequest model
```

Pydantic ensures:
- All required fields present
- Field types correct
- Values within allowed ranges
- Custom validators pass

### 2. Prompt Formatting

Located in `src/backend/app/main.py:132`

```python
def format_chat_prompt(messages: List[ChatMessage]) -> str:
    prompt_segments: List[str] = []
    for message in messages:
        role = message.role.capitalize()
        content = message.content.strip()
        prompt_segments.append(f"{role}: {content}")

    prompt_segments.append("Assistant:")
    return "\n\n".join(prompt_segments)
```

**Format**:
```
System: You are a developer...

User: Build user authentication