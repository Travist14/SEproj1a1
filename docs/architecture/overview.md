# Architecture Overview

MARC follows a modern full-stack architecture with a FastAPI backend and React frontend, leveraging vLLM for efficient LLM inference.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                         │
│                   (http://localhost:5173)                   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/WebSocket
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                   React Frontend (Vite)                     │
│  ┌────────────────┬──────────────────┬───────────────────┐ │
│  │   Components   │   Custom Hooks   │   API Client      │ │
│  │  - ChatWindow  │   - useChat      │   - streamAPI     │ │
│  │  - Login       │                  │                   │ │
│  │  - MessageInput│                  │                   │ │
│  └────────────────┴──────────────────┴───────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API (HTTP/NDJSON)
                         ↓
┌─────────────────────────────────────────────────────────────┐
│               FastAPI Backend (Uvicorn)                     │
│  ┌────────────────┬──────────────────┬───────────────────┐ │
│  │   Endpoints    │  EngineManager   │   Data Models     │ │
│  │  - /generate   │  - get_engine()  │  - ChatMessage    │ │
│  │  - /health     │  - lazy init     │  - GenerateRequest│ │
│  │  - /api/*      │                  │                   │ │
│  └────────────────┴──────────────────┴───────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │ Python API
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                    vLLM Inference Engine                    │
│  ┌────────────────┬──────────────────┬───────────────────┐ │
│  │  AsyncLLMEngine│ SamplingParams   │  Model Cache      │ │
│  │  - generate()  │  - temperature   │  - HuggingFace    │ │
│  │  - streaming   │  - top_p         │  - tokenizer      │ │
│  └────────────────┴──────────────────┴───────────────────┘ │
└────────────────────────┬────────────────────────────────────┘
                         │ Model Inference
                         ↓
┌─────────────────────────────────────────────────────────────┐
│                  LLM Model (Qwen3-4B)                       │
│             Loaded from HuggingFace Hub                     │
└─────────────────────────────────────────────────────────────┘
```

## System Components

### Frontend Layer

**Technology**: React 18.3+ with Vite build tool

**Responsibilities**:
- User interface and interaction
- Persona selection and management
- Real-time streaming display
- Chat history management

**Key Files**:
- `src/frontend/src/App.jsx` - Main application component
- `src/frontend/src/hooks/useChat.js` - Chat state management
- `src/frontend/src/api/client.js` - API communication
- `src/frontend/src/config/personas.js` - Persona configurations

### Backend Layer

**Technology**: FastAPI (async Python) with Uvicorn server

**Responsibilities**:
- HTTP API endpoints
- Request validation
- LLM engine management
- Streaming response generation
- CORS handling

**Key Files**:
- `src/backend/app/main.py` - FastAPI application and endpoints
- `src/backend/app/__init__.py` - Module initialization

### Inference Layer

**Technology**: vLLM (optimized LLM inference)

**Responsibilities**:
- Model loading and caching
- Efficient GPU utilization
- Token generation
- Sampling strategy execution

## Data Flow

### Request Flow

1. **User Input** → User enters a requirement prompt
2. **Frontend Processing** → useChat hook prepares request with persona context
3. **API Request** → POST to `/api/generate` with messages and parameters
4. **Backend Validation** → Pydantic validates request payload
5. **Prompt Formatting** → Convert chat messages to model prompt
6. **LLM Inference** → vLLM generates tokens asynchronously
7. **Streaming Response** → Tokens streamed back as NDJSON
8. **Frontend Display** → Real-time token accumulation and display

### Streaming Protocol

The backend uses NDJSON (Newline Delimited JSON) for streaming:

```json
{"type": "token", "delta": "REQ", "content": "REQ", "request_id": "abc123"}
{"type": "token", "delta": "-DEV", "content": "REQ-DEV", "request_id": "abc123"}
{"type": "token", "delta": "-001", "content": "REQ-DEV-001", "request_id": "abc123"}
...
{"type": "done", "content": "REQ-DEV-001...", "finish_reason": "stop", "request_id": "abc123"}
```

## Multi-Agent Architecture (Planned)

The current implementation supports single-agent (persona) interactions. The future multi-agent system will include:

```
┌──────────────────────────────────────────────────────────────┐
│                    Orchestrator Agent                        │
│     Coordinates multi-persona requirement synthesis          │
└───┬─────────┬──────────┬──────────┬──────────┬──────────────┘
    │         │          │          │          │
    ↓         ↓          ↓          ↓          ↓
┌─────────┬───────┬──────────┬────────┬────────────────┐
│Developer│Product│ Customer │ Sales  │ Shareholder    │
│ Agent   │Manager│  Agent   │ Agent  │ Agent          │
└─────────┴───────┴──────────┴────────┴────────────────┘
    │         │          │          │          │
    └─────────┴──────────┴──────────┴──────────┘
                         │
                         ↓
              ┌──────────────────────┐
              │  Conflict Detector   │
              │  & Synthesizer       │
              └──────────────────────┘
                         │
                         ↓
              ┌──────────────────────┐
              │  Unified Requirements│
              │  Document (IEEE      │
              │  29148 Compliant)    │
              └──────────────────────┘
```

## Design Patterns

### Backend Patterns

**Singleton Pattern** - EngineManager ensures only one vLLM engine instance
```python
class EngineManager:
    def __init__(self):
        self._engine = None
        self._lock = asyncio.Lock()
```

**Dependency Injection** - FastAPI's dependency system for request handling

**Async/Await** - Non-blocking I/O for concurrent request handling

### Frontend Patterns

**Custom Hooks** - React hooks for reusable logic (useChat)

**Component Composition** - Modular, reusable UI components

**State Management** - Local state with useState for simplicity

## Security Architecture

### Current Security Measures

1. **CORS Protection**: Configured allowed origins
2. **Request Validation**: Pydantic models validate all inputs
3. **Error Handling**: Graceful degradation with proper error responses
4. **Rate Limiting**: Planned for production

### Future Security Enhancements

- API key authentication
- Rate limiting per user/IP
- Request signing
- Input sanitization for prompt injection attacks

## Scalability Considerations

### Current Limitations

- Single vLLM engine instance
- In-memory state (no persistence)
- No load balancing
- No caching layer

### Scaling Strategy

**Horizontal Scaling**:
- Multiple backend replicas behind load balancer
- Shared model cache (Redis)
- Session persistence (database)

**Vertical Scaling**:
- Multi-GPU support (tensor parallelism)
- Larger models for better quality
- Increased memory for longer contexts

**Caching**:
- Response caching for common requirements
- Model output caching (vLLM prefix caching)

## Technology Choices

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Backend Framework | FastAPI | Async support, automatic docs, Pydantic validation |
| Frontend Framework | React | Component model, large ecosystem, great DX |
| Build Tool | Vite | Fast HMR, modern ESM support |
| LLM Inference | vLLM | Optimized GPU utilization, PagedAttention |
| Model | Qwen3-4B | Good balance of quality and performance |
| Server | Uvicorn | ASGI server, high performance |

## Next Steps

- [Backend Architecture](backend.md) - Deep dive into backend design
- [Frontend Architecture](frontend.md) - Frontend patterns and structure
- [Multi-Agent System](multi-agent.md) - Planned multi-agent architecture
- [API Reference](../api/rest-api.md) - Complete API documentation
