# Project Setup Guide

This document walks through installing and running both the FastAPI/vLLM backend and the React/Vite frontend. The existing READMEs remain unchanged; use this guide when you need the full stack running together.

## Prerequisites

- Python 3.10 or newer with `pip`.
- Node.js 18+ (Vite works best on an active LTS release) and `npm`.
- GPU with CUDA support is recommended for vLLM; CPU mode works but is slower and more memory intensive.
- Access to the `Qwen/Qwen3-4B` weights if your hosting provider gates downloads.

## Backend (FastAPI + vLLM)

1. Open a terminal in `src/backend`.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. (Optional) Set environment variables to customise behaviour:
   - `VLLM_MODEL` – model identifier (defaults to `Qwen/Qwen3-4B`).
   - `VLLM_MAX_TOKENS` – default `max_tokens` for generation (defaults to `512`).
   - `VLLM_TENSOR_PARALLEL_SIZE` – tensor parallelism when multiple GPUs are available.
   - `VLLM_TRUST_REMOTE_CODE` – set to `true` if the model requires it.
   - `BACKEND_ALLOW_ORIGINS` – comma-separated list of permitted CORS origins (defaults to `*`).
5. Launch the server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8001
   ```
6. Verify it is running by visiting `http://localhost:8001/health` or calling the `POST /generate` endpoint.

## Frontend (React + Vite)

1. Open a new terminal in `src/frontend` (keep the backend running in its own shell).
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Vite prints a local URL (typically `http://localhost:5173`). Open it in a browser to interact with the app.
5. Ensure the frontend is configured to call the backend URL (`http://localhost:8001` by default). Update any environment files or constants if your backend runs elsewhere.

## Common Workflow

1. Start the backend (`uvicorn ...`) so the API is available.
2. Start the frontend (`npm run dev`) for live reloading during development.
3. When finished, stop each server with `CTRL+C` in its terminal. Deactivate the Python virtual environment with `deactivate` if desired.

With both services running, you can develop or test the full stack end-to-end. Adjust environment variables or Vite configuration files as needed for your deployment targets.
