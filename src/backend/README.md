# FastAPI + vLLM Backend

This backend boots a [FastAPI](https://fastapi.tiangolo.com/) service that loads a [vLLM](https://github.com/vllm-project/vllm) inference engine for `meta-llama/Meta-Llama-3.1-8B-Instruct` by default. The server exposes simple endpoints that the frontend can call for health checks and text generation.

## Prerequisites

- Python 3.10 or newer.
- An environment that can run vLLM (ideally with a CUDA-capable GPU). CPU execution is possible but significantly slower and memory-intensive.
- (Optional) Access to the `meta-llama/Meta-Llama-3.1-8B-Instruct` weights if they are gated on the hosting provider you are using.

## Installation

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

Environment variables you can set before running:

- `VLLM_MODEL_NAME` – overrides the default model path/name.
- `VLLM_MAX_TOKENS` – default `max_tokens` value for generation requests (defaults to 512).
- `VLLM_TENSOR_PARALLEL_SIZE` – sets tensor parallelism when multiple GPUs are available.
- `VLLM_TRUST_REMOTE_CODE` – set to `true` if the selected model requires trusted code.
- `BACKEND_ALLOW_ORIGINS` – comma-separated list of allowed CORS origins (defaults to `*`).

## API

- `GET /` – simple readiness message listing available endpoints.
- `GET /health` – returns `{ "status": "ok", "model": "<loaded-model>" }`.
- `POST /generate` – accepts a JSON body:

  ```json
  {
    "prompt": "Write a haiku about FastAPI.",
    "max_tokens": 64,
    "temperature": 0.7,
    "top_p": 0.95,
    "stop": ["Human:"]
  }
  ```

  The response contains the generated text plus the model identifier:

  ```json
  {
    "text": "...",
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct"
  }
  ```

## Frontend integration

Point the frontend to `http://localhost:8001/generate` (or wherever the backend is hosted) to request completions. You can adjust the payload to support additional controls as needed.
