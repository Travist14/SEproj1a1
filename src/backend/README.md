# vLLM Backend Service

This folder hosts a FastAPI application that wraps a [vLLM](https://github.com/vllm-project/vllm) inference engine. It exposes endpoints consumed by the React frontend:

- `GET /api/health` – simple readiness probe.
- `POST /api/generate` – accepts chat messages and returns either a JSON response or a server-sent-event stream of tokens, depending on the `stream` flag.

## Quick start

1. Install Python dependencies (ideally inside a virtual environment):
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Export the model you want vLLM to load (defaults to `llama3.1-8b-instruct`):
   ```bash
   export VLLM_MODEL=llama3.1-8b-instruct
   ```
3. Launch the server with uvicorn:
   ```bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
   ```

The frontend is already configured to proxy `/api/*` calls to `http://localhost:8000` when you run `npm run dev` (Vite).

## Using `vllm serve` with Llama 3.1 8B Instruct

If you prefer to run the official vLLM OpenAI-compatible server, start it in a separate terminal:

```bash
vllm serve meta-llama/Llama-3.1-8B-Instruct --host 0.0.0.0 --port 8001 --max-model-len 8192
```

<!-- Then point this backend at the running instance:

```bash
export VLLM_SERVE_URL=http://127.0.0.1:8001
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
``` -->

When `VLLM_SERVE_URL` is set, the FastAPI wrapper forwards requests to `vllm serve`, preserving streaming and persona metadata, so the frontend continues to work unchanged.
