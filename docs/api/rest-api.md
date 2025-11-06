# REST API Reference

Complete API documentation for the MARC backend.

## Base URL

```
http://localhost:8001
```

## Interactive Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: [http://localhost:8001/docs](http://localhost:8001/docs)
- **ReDoc**: [http://localhost:8001/redoc](http://localhost:8001/redoc)
- **OpenAPI JSON**: [http://localhost:8001/openapi.json](http://localhost:8001/openapi.json)

## Endpoints

### GET /health

Health check endpoint with model status.

**Response**: 200 OK

```json
{
  "status": "ok",
  "model": "Qwen/Qwen3-4B",
  "engine_ready": true
}
```

**Response**: 503 Service Unavailable

```json
{
  "status": "ok",
  "model": null,
  "engine_ready": false
}
```

**Example**:
```bash
curl http://localhost:8001/health
```

---

### POST /generate

Generate chat completion with optional streaming.

**Request Body**:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a software developer..."
    },
    {
      "role": "user",
      "content": "I need user authentication"
    }
  ],
  "stream": true,
  "max_tokens": 512,
  "temperature": 0.7,
  "top_p": 0.95,
  "presence_penalty": 0.0,
  "frequency_penalty": 0.0,
  "stop": null,
  "persona": "developer"
}
```

**Request Fields**:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| messages | array | Yes | - | Array of ChatMessage objects |
| stream | boolean | No | true | Enable token streaming |
| max_tokens | integer | No | 512 | Maximum tokens to generate (≥1) |
| temperature | float | No | 0.7 | Sampling temperature (0.0-2.0) |
| top_p | float | No | 0.95 | Nucleus sampling (0.0-1.0) |
| presence_penalty | float | No | 0.0 | Presence penalty (-2.0 to 2.0) |
| frequency_penalty | float | No | 0.0 | Frequency penalty (-2.0 to 2.0) |
| stop | array | No | null | Stop sequences |
| persona | string | No | null | Persona identifier (informational) |

**ChatMessage Object**:

```json
{
  "role": "system" | "user" | "assistant",
  "content": "Message text"
}
```

**Streaming Response** (Content-Type: `application/x-ndjson`):

Each line is a JSON object:

```json
{"type": "token", "delta": "REQ", "content": "REQ", "request_id": "abc123"}
{"type": "token", "delta": "-DEV", "content": "REQ-DEV", "request_id": "abc123"}
{"type": "token", "delta": "-001", "content": "REQ-DEV-001", "request_id": "abc123"}
{"type": "done", "content": "REQ-DEV-001...", "finish_reason": "stop", "request_id": "abc123"}
```

**Response Event Types**:

| Type | Fields | Description |
|------|--------|-------------|
| token | delta, content, request_id | Incremental token |
| done | content, finish_reason, request_id | Generation complete |
| error | message, request_id | Error occurred |

**Finish Reasons**:
- `stop`: Natural completion
- `length`: Reached max_tokens
- `abort`: Request cancelled

**Non-Streaming Response** (Content-Type: `application/json`):

```json
{
  "output": "Generated requirement text...",
  "finish_reason": "stop",
  "request_id": "abc123"
}
```

**Example** (streaming):
```bash
curl -X POST http://localhost:8001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a developer."},
      {"role": "user", "content": "Build authentication"}
    ],
    "stream": true
  }'
```

**Example** (non-streaming):
```bash
curl -X POST http://localhost:8001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Build authentication"}
    ],
    "stream": false
  }'
```

**Example** (Python):
```python
import requests

response = requests.post(
    'http://localhost:8001/generate',
    json={
        'messages': [
            {'role': 'system', 'content': 'You are a developer.'},
            {'role': 'user', 'content': 'Build authentication'}
        ],
        'stream': False,
        'max_tokens': 512,
        'temperature': 0.7
    }
)

result = response.json()
print(result['output'])
```

**Example** (Python streaming):
```python
import requests
import json

response = requests.post(
    'http://localhost:8001/generate',
    json={
        'messages': [
            {'role': 'user', 'content': 'Build authentication'}
        ],
        'stream': True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        data = json.loads(line)
        if data['type'] == 'token':
            print(data['delta'], end='', flush=True)
        elif data['type'] == 'done':
            print(f"\n\nFinish reason: {data['finish_reason']}")
```

---

### POST /api/generate

Alias for `/generate` endpoint. Identical behavior.

---

## Error Responses

### 400 Bad Request

Invalid request payload or parameters.

```json
{
  "detail": "role must be one of ['assistant', 'system', 'user']"
}
```

### 422 Unprocessable Entity

Validation error (Pydantic).

```json
{
  "detail": [
    {
      "loc": ["body", "messages"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error

Server-side error during generation.

```json
{
  "detail": "Internal server error"
}
```

### Streaming Error

Error during streaming (sent as NDJSON):

```json
{"type": "error", "message": "Generation failed", "request_id": "abc123"}
```

## Rate Limiting

Currently not implemented. Recommended for production:

- 10 requests per minute per IP
- 100 requests per hour per IP
- Use headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

## Authentication

Currently not implemented. Recommended for production:

```bash
curl -X POST http://localhost:8001/generate \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

## CORS

Configured via `BACKEND_ALLOW_ORIGINS` environment variable.

Default: `*` (allow all origins)

Recommended: Specific origins only
```bash
export BACKEND_ALLOW_ORIGINS="http://localhost:5173,https://yourdomain.com"
```

## WebSocket Support

Not currently implemented. Future feature for real-time bidirectional communication.

## Versioning

Current API version: `v0.1.0`

No versioning in URLs yet. Future versions may use:
- Path versioning: `/v1/generate`, `/v2/generate`
- Header versioning: `Accept: application/vnd.marc.v1+json`

## Client Libraries

### JavaScript/TypeScript

```javascript
// src/frontend/src/api/client.js
export async function streamGenerate(payload, onChunk, signal) {
  const response = await fetch(`${API_BASE_URL}/api/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
    signal
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    for (const line of lines) {
      if (line.trim()) {
        const data = JSON.parse(line);
        if (data.type === 'token') {
          onChunk(data.delta);
        } else if (data.type === 'error') {
          throw new Error(data.message);
        }
      }
    }
  }
}
```

### Python

```python
# client.py
import requests
import json
from typing import Iterator, Dict

def generate(messages: list, stream: bool = True, **kwargs) -> Dict | Iterator[str]:
    payload = {
        'messages': messages,
        'stream': stream,
        **kwargs
    }

    response = requests.post(
        'http://localhost:8001/generate',
        json=payload,
        stream=stream
    )

    if stream:
        def token_generator():
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if data['type'] == 'token':
                        yield data['delta']
                    elif data['type'] == 'error':
                        raise Exception(data['message'])

        return token_generator()
    else:
        return response.json()
```

## Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8001/health

# Simple generation
curl -X POST http://localhost:8001/generate \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Test"}],"stream":false}'

# Streaming generation
curl -X POST http://localhost:8001/generate \
  -H "Content-Type: application/json" \
  -N \
  -d '{"messages":[{"role":"user","content":"Test"}],"stream":true}'
```

### Using HTTPie

```bash
# Install: pip install httpie

# Health check
http GET http://localhost:8001/health

# Generation
http POST http://localhost:8001/generate \
  messages:='[{"role":"user","content":"Test"}]' \
  stream:=false
```

### Using Postman

1. Import OpenAPI spec: http://localhost:8001/openapi.json
2. All endpoints auto-configured with examples
3. Test streaming with "Send and Download" option

## Next Steps

- [Backend Modules](backend.md) - Python module documentation
- [Frontend Components](frontend.md) - React component API
- [Configuration](../getting-started/configuration.md) - API configuration options
