# vLLM Backend Service

This folder hosts a FastAPI application that wraps a [vLLM](https://github.com/vllm-project/vllm) inference engine. It exposes endpoints consumed by the React frontend:

- `GET /api/health` – simple readiness probe.
- `POST /api/generate` – accepts chat messages and returns either a JSON response or a server-sent-event stream of tokens, depending on the `stream` flag.

## Quick start

1. Install Python dependencies (ideally inside a virtual environment):
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Export the model you want vLLM to load (defaults to `facebook/opt-125m`):
   ```bash
   export VLLM_MODEL=meta-llama/Llama-3-8B-Instruct
   ```
3. Launch the server with uvicorn:
   ```bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
   ```

The frontend is already configured to proxy `/api/*` calls to `http://localhost:8000` when you run `npm run dev` (Vite).

## Configuration

You can further tune the engine via environment variables:

- `VLLM_MODEL` – Hugging Face model name or local path **(required for meaningful results)**.
- `VLLM_MAX_TOKENS` – default generation length (default: `512`).
- `VLLM_TEMPERATURE` – default sampling temperature (default: `0.7`).
- `VLLM_STOP` – comma-separated stop sequences appended to defaults (`"\\nUser:","\\nSystem:"`).
- `VLLM_TENSOR_PARALLEL_SIZE`, `VLLM_PIPELINE_PARALLEL_SIZE` – advanced parallelism settings.
- `VLLM_DTYPE` – numeric precision (`"auto"`, `"float16"`, etc.).
- `VLLM_DOWNLOAD_DIR` – custom model cache directory.

Set these before launching uvicorn to adjust behavior without touching code.
