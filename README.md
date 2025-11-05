# MARC - Multi-Agent Requirement Collaboration

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](./TESTING.md)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3+-61DAFB.svg)](https://react.dev)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Overview

**MARC** (Multi-Agent Requirement Collaboration) is an AI-powered framework for collaborative Requirements Engineering that leverages multiple LLM-based agents to gather, analyze, and synthesize software requirements from diverse stakeholder perspectives. Built on IEEE 29148 standards, MARC enables teams to create comprehensive, unambiguous, and testable requirements documentation through intelligent multi-agent collaboration.

The system simulates five distinct stakeholder personas:
- **Developer** - Technical feasibility and implementation concerns
- **Product Manager** - User value, business metrics, and prioritization
- **Customer** - Usability, simplicity, and end-user needs
- **Sales** - Value proposition and competitive positioning
- **Shareholder** - Financial returns, ROI, and strategic value

By synthesizing insights from these diverse perspectives, MARC produces well-rounded requirements that balance technical constraints with business objectives and user needs.

### Key Features

- **Multi-Persona Analysis**: Gather requirements from 5 distinct stakeholder perspectives
- **IEEE 29148 Compliant**: Ensures requirements meet industry standards
- **LLM-Powered**: Built on Meta-Llama-3.1-8B-Instruct with vLLM for efficient inference
- **Real-time Streaming**: Asynchronous API with streaming support for responsive UX
- **Structured Extraction**: Automated parsing and validation of requirement fields
- **Comprehensive Testing**: 80%+ test coverage with unit, integration, and compliance tests
- **Full-Stack Solution**: FastAPI backend + React frontend for complete workflow

---

## Who Should Use This Software

MARC is designed for:

### Software Engineering Teams
- **Requirements Engineers** who need to gather comprehensive requirements from multiple stakeholders
- **Product Managers** planning new features or products with complex stakeholder landscapes
- **Development Teams** who want to ensure requirements are technically feasible before implementation
- **QA/Test Engineers** who need clear, testable acceptance criteria

### Businesses & Organizations
- **Startups** building MVPs and need to balance diverse stakeholder needs quickly
- **Enterprise Teams** managing complex projects with multiple departments
- **Consulting Firms** gathering requirements from clients across various domains
- **Agile Teams** conducting sprint planning and backlog refinement

### Education & Research
- **Software Engineering Students** learning requirements engineering best practices
- **CS Educators** teaching collaborative software development
- **Researchers** studying LLM applications in software engineering
- **Academic Projects** exploring multi-agent systems and AI collaboration

### Use Cases
- E-commerce platforms
- Healthcare patient portals
- Food delivery applications
- Financial services applications
- Any software project requiring multi-stakeholder requirements analysis

---

## Quick Start

Get MARC up and running in under 5 minutes:

### Prerequisites

- **Python 3.10+** (for backend)
- **Node.js 18+** (for frontend)
- **CUDA-capable GPU** (recommended for vLLM, CPU is possible but slower)
- **8GB+ RAM** (16GB+ recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/SEproj1a1.git
cd SEproj1a1

# Install backend dependencies
cd src/backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

### Running the Application

#### Terminal 1 - Backend Server
```bash
cd src/backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

The backend will be available at `http://localhost:8001`

#### Terminal 2 - Frontend Development Server
```bash
cd src/frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Your First Requirement

1. Open your browser to `http://localhost:5173`
2. Select a persona (e.g., "Developer")
3. Enter a requirement prompt (e.g., "I need user authentication with email and password")
4. Click "Generate" and watch the AI create structured requirements in real-time
5. Review the generated requirement with ID, category, priority, and acceptance criteria

---

## Features & Usage Guide

### 1. Persona-Based Requirement Generation

Each persona provides a unique lens for analyzing requirements:

#### Developer Persona
```
Input: "Build a payment processing system"
Output:
- REQ-DEV-001: Secure payment gateway integration
- Technical considerations: PCI DSS compliance, encryption
- Dependencies: Payment provider API keys, SSL certificates
- Acceptance criteria: Process transactions < 3 seconds
```

#### Product Manager Persona
```
Input: "Build a payment processing system"
Output:
- REQ-PM-001: Payment processing capability
- Business value: Enable revenue generation
- Success metrics: 99.9% transaction success rate
- User story: As a customer, I want to pay securely...
```

#### Customer Persona
```
Input: "Build a payment processing system"
Output:
- REQ-CUST-001: Easy and secure checkout
- Pain points: Too many steps, security concerns
- Usability: One-click checkout option
- Customer value: Fast, trustworthy payment
```

### 2. Requirements Structure (IEEE 29148 Compliant)

All generated requirements follow a consistent structure:

```
REQ-[PERSONA]-[NUMBER]

Category: [Functional/Non-functional/Performance/Security]
Priority: [High/Medium/Low]

Description:
[Clear, unambiguous description of the requirement]

Rationale:
[Why this requirement is needed]

Acceptance Criteria:
- [Testable criterion 1]
- [Testable criterion 2]
- [Testable criterion 3]

Dependencies:
- [Related requirement or system]

Verification Method:
[How to verify/test this requirement]
```

### 3. Backend API

The FastAPI backend provides these endpoints:

#### POST /generate
Generate requirements from a prompt with persona context.

**Request:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a Developer analyzing requirements..."
    },
    {
      "role": "user",
      "content": "Build user authentication"
    }
  ],
  "max_tokens": 512,
  "temperature": 0.7,
  "top_p": 0.9,
  "stream": true
}
```

**Response (streaming):**
```json
{"id": "req-123", "event": "token", "text": "REQ-DEV-001...", "finished": false}
{"id": "req-123", "event": "token", "text": "Category: Security", "finished": false}
{"id": "req-123", "event": "end", "finished": true}
```

### 4. Frontend Interface

The React-based frontend provides:
- **Persona Selection**: Choose from 5 stakeholder personas
- **Prompt Input**: Enter requirement descriptions in natural language
- **Real-time Streaming**: Watch requirements generate token-by-token
- **History View**: Review previously generated requirements
- **Export Options**: Download requirements in various formats

### 5. Multi-Agent Collaboration (Coming Soon)

Future features include:
- **Orchestrator Agent**: Synthesizes requirements from all personas
- **Conflict Detection**: Identifies contradicting requirements across personas
- **Requirement Refinement**: Iterative improvement through multi-agent discussion
- **RAG Integration**: Search and retrieve similar requirements from database
- **Feedback Loops**: Stakeholder critiques and requirement updates

### 6. Testing & Validation

MARC includes comprehensive testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest -m unit          # Fast unit tests
pytest -m integration   # Integration tests
pytest -m slow          # Long-running tests

# Use the convenient test script
./run_tests.sh coverage
```

Test categories:
- **Backend API Tests**: Endpoint validation, CORS, error handling
- **Persona Tests**: Each persona generates appropriate requirements
- **Requirements Extraction**: Parse requirement fields correctly
- **IEEE Compliance**: Verify requirements meet standards
- **Multi-Agent**: Placeholder tests for future collaboration features

---

## Building From Source

### Backend (Python/FastAPI)

```bash
# Navigate to backend directory
cd src/backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Optional: Install development dependencies
pip install pytest pytest-cov pytest-asyncio httpx black flake8

# Run the server
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

#### Environment Variables

Configure the backend with these environment variables:

```bash
# Model configuration
export VLLM_MODEL_NAME="meta-llama/Meta-Llama-3.1-8B-Instruct"
export VLLM_MAX_TOKENS=8192
export VLLM_TENSOR_PARALLEL_SIZE=1
export VLLM_TRUST_REMOTE_CODE=false

# GPU configuration
export GPU_MEMORY_UTILIZATION=0.9

# CORS configuration
export BACKEND_ALLOW_ORIGINS="http://localhost:5173,http://localhost:3000"
```

### Frontend (React/Vite)

```bash
# Navigate to frontend directory
cd src/frontend

# Install dependencies
npm install

# Development server (hot reload)
npm run dev

# Production build
npm run build

# Preview production build
npm run preview
```

#### Configuration

Edit `src/frontend/src/config/api.js` to set the backend URL:

```javascript
export const API_BASE_URL = process.env.VITE_API_URL || 'http://localhost:8001';
```

### Docker (Optional)

```bash
# Build Docker image
docker build -t marc:latest .

# Run container
docker run -p 8001:8001 -p 5173:5173 marc:latest

# Or use Docker Compose
docker-compose up --build
```

---

## Running the Test Suite

MARC has a comprehensive test suite with 80%+ code coverage.

### Quick Test Commands

```bash
# Install test dependencies first
pip install -r tests/requirements.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Test Categories

```bash
# Unit tests only (fast, no external dependencies)
pytest -m unit

# Integration tests (may require services)
pytest -m integration

# Tests that require actual LLM
pytest -m requires_llm

# Exclude slow tests
pytest -m "not slow"
```

### Test Specific Components

```bash
# Backend API tests
pytest tests/backend/

# Persona system tests
pytest tests/integration/test_personas.py

# Requirements extraction tests
pytest tests/requirements/test_extraction.py

# IEEE 29148 compliance tests
pytest tests/requirements/test_ieee_compliance.py

# Multi-agent collaboration tests
pytest tests/integration/test_multi_agent.py
```

### Using the Test Script

The included `run_tests.sh` script provides convenient test running:

```bash
# Make executable
chmod +x run_tests.sh

# Run all tests
./run_tests.sh

# Run specific test suites
./run_tests.sh unit
./run_tests.sh integration
./run_tests.sh backend
./run_tests.sh personas
./run_tests.sh requirements
./run_tests.sh ieee

# Generate coverage report
./run_tests.sh coverage

# Quick tests (unit only, short output)
./run_tests.sh quick

# Fast tests (exclude slow tests)
./run_tests.sh fast

# Show help
./run_tests.sh help
```

### Test Output Example

```bash
$ ./run_tests.sh coverage

╔════════════════════════════════════════╗
║   MARC Testing Suite                  ║
║   Multi-Agent Requirement Collaboration║
╚════════════════════════════════════════╝

Running tests with coverage report...
tests/backend/test_api.py ......              [ 40%]
tests/integration/test_personas.py ....       [ 70%]
tests/requirements/test_extraction.py .....   [100%]

---------- coverage: platform linux, python 3.11.5 -----------
Name                          Stmts   Miss  Cover
-------------------------------------------------
src/backend/app/main.py         156     12    92%
src/personas/developer.py        45      3    93%
src/requirements/extract.py      78      8    90%
-------------------------------------------------
TOTAL                            279     23    92%

✓ All tests passed!
```

### Continuous Integration

Tests run automatically on:
- Push to any branch
- Pull requests
- Merges to main

See [TESTING.md](./TESTING.md) for detailed testing documentation.

---

## Project Structure

```
SEproj1a1/
├── src/
│   ├── backend/              # FastAPI backend
│   │   ├── app/
│   │   │   ├── main.py       # API endpoints
│   │   │   └── __init__.py
│   │   ├── requirements.txt   # Python dependencies
│   │   └── README.md
│   └── frontend/             # React frontend
│       ├── src/
│       │   ├── components/    # React components
│       │   ├── hooks/         # Custom React hooks
│       │   ├── api/           # API client
│       │   ├── config/        # Configuration
│       │   ├── App.jsx        # Main app component
│       │   └── main.jsx       # Entry point
│       ├── package.json
│       ├── vite.config.js
│       └── index.html
├── tests/
│   ├── backend/              # Backend API tests
│   ├── integration/          # Integration & persona tests
│   ├── requirements/         # Requirement extraction tests
│   ├── fixtures/             # Test fixtures & mock data
│   ├── conftest.py           # Pytest configuration
│   ├── requirements.txt      # Test dependencies
│   └── README.md
├── proj1/                    # Project documentation (PDFs)
├── proj1e/                   # MARC pamphlet
├── README.md                 # This file
├── TESTING.md                # Quick testing reference
├── pytest.ini                # Pytest configuration
└── run_tests.sh              # Test runner script
```

---

## Configuration

### Backend Configuration

Edit `src/backend/app/main.py` or use environment variables:

- **MODEL_NAME**: HuggingFace model identifier (default: meta-llama/Meta-Llama-3.1-8B-Instruct)
- **TENSOR_PARALLEL_SIZE**: GPU parallelism (default: 1)
- **GPU_MEMORY_UTILIZATION**: GPU memory fraction (default: 0.9)
- **MAX_TOKENS**: Maximum generation tokens (default: 512)
- **TEMPERATURE**: Sampling temperature (default: 0.7)
- **TOP_P**: Nucleus sampling parameter (default: 0.9)

### Frontend Configuration

Edit `src/frontend/src/config/api.js`:

- **API_BASE_URL**: Backend API URL (default: http://localhost:8001)
- **DEFAULT_MAX_TOKENS**: Default token limit (default: 512)
- **DEFAULT_TEMPERATURE**: Default temperature (default: 0.7)

---

## Documentation

- **[TESTING.md](./TESTING.md)** - Quick testing reference guide
- **[tests/README.md](./tests/README.md)** - Comprehensive testing documentation
- **[src/backend/README.md](./src/backend/README.md)** - Backend API documentation
- **[proj1e/MARC-pamphlet.pdf](./proj1e/MARC-pamphlet.pdf)** - MARC system overview pamphlet

---

## Requirements

### Backend Dependencies
- fastapi>=0.111.0
- uvicorn[standard]>=0.30.0
- vllm>=0.5.0
- pydantic>=2.7.0

### Frontend Dependencies
- react>=18.3.1
- react-dom>=18.3.1
- vite>=5.1.0

### Test Dependencies
- pytest>=8.0.0
- pytest-cov>=4.1.0
- pytest-asyncio>=0.23.0
- httpx>=0.26.0

---

## Troubleshooting

### vLLM GPU Memory Issues
```bash
# Reduce GPU memory utilization
export GPU_MEMORY_UTILIZATION=0.7

# Use CPU (slower)
export CUDA_VISIBLE_DEVICES=""
```

### Frontend Can't Connect to Backend
```bash
# Check backend is running
curl http://localhost:8001/health

# Check CORS settings
export BACKEND_ALLOW_ORIGINS="http://localhost:5173"
```

### Test Import Errors
```bash
# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or run from project root
cd /path/to/SEproj1a1
pytest
```

### Model Download Issues
```bash
# Pre-download model
python -c "from transformers import AutoTokenizer; AutoTokenizer.from_pretrained('meta-llama/Meta-Llama-3.1-8B-Instruct')"

# Or use a different model
export VLLM_MODEL_NAME="gpt2"  # For testing
```

---

## Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write tests for new features
5. Ensure all tests pass (`./run_tests.sh`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript
- Maintain 80%+ test coverage
- Add docstrings to all functions
- Update documentation for new features

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## Acknowledgments

- Built for **NCSU CSC 510: Software Engineering** (Fall 2025)
- Powered by **Meta-Llama-3.1-8B-Instruct** via vLLM
- Inspired by IEEE 29148 Requirements Engineering standards
- Based on multi-agent collaboration research in software engineering

---

## Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/SEproj1a1/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/SEproj1a1/discussions)
- **Documentation**: See [docs](./docs) directory

---

## Roadmap

### Current Features (v1.0)
- ✅ 5 persona-based requirement generation
- ✅ IEEE 29148 compliant output
- ✅ Real-time streaming API
- ✅ React frontend with persona selection
- ✅ Comprehensive test suite (80%+ coverage)

### Coming Soon (v1.1)
- 🔄 Orchestrator agent for requirement synthesis
- 🔄 Multi-agent conflict detection
- 🔄 Requirement refinement through iteration
- 🔄 Export to PDF/Word/Markdown
- 🔄 Requirement version history

### Future (v2.0)
- 🔮 RAG-based requirement search
- 🔮 Custom persona creation
- 🔮 Integration with JIRA/GitHub Issues
- 🔮 Requirement traceability matrix
- 🔮 Automated acceptance test generation

---

**MARC** - Making Requirements Engineering Collaborative, Comprehensive, and Intelligent.
