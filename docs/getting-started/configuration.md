# Configuration Guide

This guide covers all configuration options for customizing MARC to your needs.

## Backend Configuration

The backend can be configured through environment variables or by editing `src/backend/app/main.py`.

### Environment Variables

Create a `.env` file in `src/backend/`:

```bash
# Model Configuration
VLLM_MODEL=Qwen/Qwen3-4B
VLLM_MAX_TOKENS=512
VLLM_TEMPERATURE=0.7
VLLM_TOP_P=0.95
VLLM_MAX_MODEL_LEN=4096
VLLM_TRUST_REMOTE_CODE=false

# GPU Configuration
VLLM_TENSOR_PARALLEL_SIZE=1
GPU_MEMORY_UTILIZATION=0.9

# Server Configuration
BACKEND_ALLOW_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Configuration Options

#### Model Selection

```bash
VLLM_MODEL=Qwen/Qwen3-4B
```

Options:
- `Qwen/Qwen3-4B` (default) - Balanced performance and quality
- `meta-llama/Meta-Llama-3.1-8B-Instruct` - High quality, requires more resources
- `gpt2` - Fast, for testing only

#### Generation Parameters

**Max Tokens**
```bash
VLLM_MAX_TOKENS=512
```
Maximum number of tokens to generate (default: 512, range: 1-8192)

**Temperature**
```bash
VLLM_TEMPERATURE=0.7
```
Sampling temperature (default: 0.7, range: 0.0-2.0)
- Lower (0.1-0.5): More deterministic, focused responses
- Higher (0.8-1.5): More creative, varied responses

**Top-P (Nucleus Sampling)**
```bash
VLLM_TOP_P=0.95
```
Nucleus sampling threshold (default: 0.95, range: 0.0-1.0)

#### GPU Configuration

**Tensor Parallel Size**
```bash
VLLM_TENSOR_PARALLEL_SIZE=1
```
Number of GPUs to use for model parallelism (default: 1)

**Max Model Length**
```bash
VLLM_MAX_MODEL_LEN=4096
```
Maximum context length (default: 4096 tokens)

**Trust Remote Code**
```bash
VLLM_TRUST_REMOTE_CODE=false
```
Allow execution of remote code in model (default: false, set to true only for trusted models)

#### CORS Configuration

```bash
BACKEND_ALLOW_ORIGINS=http://localhost:5173,http://localhost:3000
```
Comma-separated list of allowed origins (use `*` for all origins in development only)

### Using Environment Variables

#### Linux/macOS

```bash
export VLLM_MODEL=Qwen/Qwen3-4B
export VLLM_MAX_TOKENS=512
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

#### Windows (PowerShell)

```powershell
$env:VLLM_MODEL="Qwen/Qwen3-4B"
$env:VLLM_MAX_TOKENS="512"
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

#### Using .env File

Install python-dotenv:
```bash
pip install python-dotenv
```

Load in your application:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Frontend Configuration

### API Configuration

Edit `src/frontend/src/config/api.js`:

```javascript
export const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:8001';
export const DEFAULT_MAX_TOKENS = 512;
export const DEFAULT_TEMPERATURE = 0.7;
export const DEFAULT_TOP_P = 0.95;
```

### Persona Configuration

Edit `src/frontend/src/config/personas.js` to customize personas:

```javascript
export const PERSONAS = {
  developer: {
    key: 'developer',
    label: 'Developer',
    description: 'Technical feasibility and implementation',
    systemPrompt: 'You are a software developer...',
    color: '#2563eb'
  },
  // Add custom personas...
};
```

### Build Configuration

Edit `src/frontend/vite.config.js`:

```javascript
export default defineConfig({
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': 'http://localhost:8001'
    }
  }
});
```

## Production Configuration

### Backend Production Settings

```bash
# Disable reload
uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 4

# Use gunicorn for production
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
```

### Frontend Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Serve with a static server
npx serve -s dist -p 5173
```

### Environment-Specific Configuration

Create multiple .env files:

- `.env.development`
- `.env.production`
- `.env.test`

Load based on environment:

```bash
# Development
NODE_ENV=development npm run dev

# Production
NODE_ENV=production npm run build
```

## Docker Configuration

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY src/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/backend ./backend

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8001:8001"
    environment:
      - VLLM_MODEL=Qwen/Qwen3-4B
      - VLLM_MAX_TOKENS=512
    volumes:
      - ./models:/root/.cache/huggingface

  frontend:
    image: node:18
    working_dir: /app
    volumes:
      - ./src/frontend:/app
    ports:
      - "5173:5173"
    command: npm run dev
```

## Performance Tuning

### Backend Performance

**GPU Memory Optimization**
```bash
# Reduce GPU memory usage
export GPU_MEMORY_UTILIZATION=0.7

# Use CPU (slower)
export CUDA_VISIBLE_DEVICES=""
```

**Connection Pooling**
Add connection pooling for database connections if using a database.

**Caching**
Implement response caching for common queries:

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

FastAPICache.init(InMemoryBackend())
```

### Frontend Performance

**Code Splitting**
```javascript
// Use dynamic imports
const ChatWindow = lazy(() => import('./components/ChatWindow'));
```

**Bundle Size Optimization**
```bash
# Analyze bundle
npm run build -- --analyze

# Use production mode
NODE_ENV=production npm run build
```

## Security Configuration

### API Authentication

Add API key authentication:

```python
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

@app.post("/generate")
async def generate(payload: GenerateRequest, api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
    # ...
```

### Rate Limiting

```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/generate")
@limiter.limit("10/minute")
async def generate(request: Request, payload: GenerateRequest):
    # ...
```

### HTTPS Configuration

```bash
# Generate self-signed certificate for development
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with HTTPS
uvicorn app.main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

## Monitoring & Logging

### Backend Logging

Configure logging in `src/backend/app/main.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('marc.log'),
        logging.StreamHandler()
    ]
)
```

### Health Checks

The `/health` endpoint provides system status:

```bash
curl http://localhost:8001/health
```

Response:
```json
{
  "status": "ok",
  "model": "Qwen/Qwen3-4B",
  "engine_ready": true
}
```

## Next Steps

- [Architecture Overview](../architecture/overview.md) - Understand the system design
- [API Reference](../api/rest-api.md) - Explore the complete API
- [Development Guide](../development/contributing.md) - Start contributing
