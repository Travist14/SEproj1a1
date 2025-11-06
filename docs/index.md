# MARC - Multi-Agent Requirement Collaboration

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](../TESTING.md)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.3+-61DAFB.svg)](https://react.dev)

## Overview

**MARC** (Multi-Agent Requirement Collaboration) is an AI-powered framework for collaborative Requirements Engineering that leverages multiple LLM-based agents to gather, analyze, and synthesize software requirements from diverse stakeholder perspectives.

Built on **IEEE 29148** standards, MARC enables teams to create comprehensive, unambiguous, and testable requirements documentation through intelligent multi-agent collaboration.

## Key Features

- **Multi-Persona Analysis**: Gather requirements from 5 distinct stakeholder perspectives
- **IEEE 29148 Compliant**: Ensures requirements meet industry standards
- **LLM-Powered**: Built on Meta-Llama-3.1-8B-Instruct with vLLM for efficient inference
- **Real-time Streaming**: Asynchronous API with streaming support for responsive UX
- **Structured Extraction**: Automated parsing and validation of requirement fields
- **Comprehensive Testing**: 80%+ test coverage with unit, integration, and compliance tests
- **Full-Stack Solution**: FastAPI backend + React frontend for complete workflow

## Stakeholder Personas

MARC simulates five distinct stakeholder perspectives:

| Persona | Focus Area | Key Concerns |
|---------|-----------|--------------|
| **Developer** | Technical feasibility | Implementation, dependencies, technical debt |
| **Product Manager** | User value & metrics | Business value, prioritization, KPIs |
| **Customer** | Usability & simplicity | User experience, ease of use, pain points |
| **Sales** | Value proposition | Competitive positioning, selling points |
| **Shareholder** | Financial returns | ROI, strategic value, growth |

By synthesizing insights from these diverse perspectives, MARC produces well-rounded requirements that balance technical constraints with business objectives and user needs.

## Quick Links

- [Installation Guide](getting-started/installation.md) - Get MARC up and running
- [Quick Start](getting-started/quickstart.md) - Your first requirement in 5 minutes
- [Architecture Overview](architecture/overview.md) - Understanding MARC's design
- [API Reference](api/rest-api.md) - Complete API documentation
- [Testing Guide](guide/testing.md) - Running and writing tests

## Use Cases

MARC is designed for:

**Software Engineering Teams**
- Requirements Engineers gathering comprehensive requirements
- Product Managers planning new features with complex stakeholder landscapes
- Development Teams ensuring technical feasibility before implementation
- QA/Test Engineers needing clear, testable acceptance criteria

**Businesses & Organizations**
- Startups building MVPs and balancing diverse stakeholder needs
- Enterprise Teams managing complex projects with multiple departments
- Consulting Firms gathering client requirements across various domains
- Agile Teams conducting sprint planning and backlog refinement

**Education & Research**
- Software Engineering Students learning requirements engineering best practices
- CS Educators teaching collaborative software development
- Researchers studying LLM applications in software engineering
- Academic Projects exploring multi-agent systems

## Technology Stack

**Backend**
- FastAPI (async Python web framework)
- vLLM (efficient LLM inference)
- Pydantic (data validation)
- Meta-Llama-3.1-8B-Instruct (LLM model)

**Frontend**
- React 18.3+ (UI framework)
- Vite (build tool)
- Custom hooks for chat management

**Testing**
- pytest (backend testing)
- pytest-asyncio (async test support)
- httpx (HTTP client testing)
- 80%+ code coverage

## Getting Started

Ready to try MARC? Head over to the [Installation Guide](getting-started/installation.md) to get started in under 5 minutes!

## Documentation Structure

This documentation is organized into several sections:

- **Getting Started**: Installation, configuration, and quick start guides
- **Architecture**: Deep dive into system design and components
- **API Reference**: Complete API documentation and module references
- **User Guide**: How to use MARC effectively for requirements engineering
- **Development**: Contributing guidelines, testing, and code standards
