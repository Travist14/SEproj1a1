# Installation Guide

This guide will help you install and set up MARC on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** (for backend)
- **Node.js 18+** (for frontend)
- **pip** (Python package manager)
- **npm** (Node.js package manager)
- **Git** (version control)

### Optional but Recommended

- **CUDA-capable GPU** (for faster vLLM inference, CPU is possible but slower)
- **8GB+ RAM** (16GB+ recommended for smoother performance)
- **Docker** (for containerized deployment)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SEproj1a1.git
cd SEproj1a1
```

### 2. Backend Setup

#### Create Virtual Environment

```bash
cd src/backend
python -m venv .venv
```

#### Activate Virtual Environment

**Linux/macOS:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

#### Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Verify Installation

```bash
python -c "import fastapi; import vllm; print('Backend dependencies installed successfully!')"
```

### 3. Frontend Setup

```bash
cd ../frontend
npm install
```

#### Verify Installation

```bash
npm run build
```

If the build succeeds, your frontend is set up correctly!

### 4. Configuration

#### Backend Environment Variables

Create a `.env` file in `src/backend/`:

```bash
# Model configuration
VLLM_MODEL=Qwen/Qwen3-4B
VLLM_MAX_TOKENS=512
VLLM_TEMPERATURE=0.7
VLLM_TOP_P=0.95

# Server configuration
BACKEND_ALLOW_ORIGINS=http://localhost:5173,http://localhost:3000

# GPU configuration (optional)
VLLM_TENSOR_PARALLEL_SIZE=1
VLLM_TRUST_REMOTE_CODE=false
VLLM_MAX_MODEL_LEN=4096
```

#### Frontend Configuration

The frontend is pre-configured to connect to `http://localhost:8001`. To change this, edit `src/frontend/src/config/api.js`.

## Verification

### Test Backend

```bash
cd src/backend
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

Open http://localhost:8001/docs in your browser. You should see the FastAPI Swagger documentation.

### Test Frontend

In a new terminal:

```bash
cd src/frontend
npm run dev
```

Open http://localhost:5173 in your browser. You should see the MARC login screen.

## Common Installation Issues

### vLLM Installation Fails

**Issue:** vLLM requires CUDA toolkit
**Solution:** Install CUDA toolkit or use CPU-only mode:
```bash
export CUDA_VISIBLE_DEVICES=""
```

### Port Already in Use

**Issue:** Port 8001 or 5173 is already occupied
**Solution:** Use different ports:
```bash
# Backend
uvicorn app.main:app --port 8002

# Frontend (edit vite.config.js)
npm run dev -- --port 5174
```

### Permission Denied

**Issue:** Cannot create virtual environment or install packages
**Solution:** Use user-level installation:
```bash
pip install --user -r requirements.txt
```

### Model Download Timeout

**Issue:** Large model download times out
**Solution:** Pre-download the model:
```bash
python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('Qwen/Qwen3-4B')"
```

## Docker Installation (Alternative)

If you prefer Docker:

```bash
# Build image
docker build -t marc:latest .

# Run container
docker run -p 8001:8001 -p 5173:5173 marc:latest

# Or use Docker Compose
docker-compose up --build
```

## Next Steps

- [Quick Start Guide](quickstart.md) - Generate your first requirement
- [Configuration](configuration.md) - Customize MARC for your needs
- [Architecture Overview](../architecture/overview.md) - Understand how MARC works
