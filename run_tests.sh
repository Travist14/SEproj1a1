#!/bin/bash
# MARC Test Runner Script
# Quick script to run different test suites

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   MARC Testing Suite                  ║${NC}"
echo -e "${BLUE}║   Multi-Agent Requirement Collaboration║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest not found!${NC}"
    echo "Please install test dependencies:"
    echo "  pip install -r tests/requirements.txt"
    exit 1
fi

# Parse command line arguments
case "${1:-all}" in
    all)
        echo -e "${GREEN}Running all tests...${NC}"
        pytest -v
        ;;

    unit)
        echo -e "${GREEN}Running unit tests...${NC}"
        pytest -m unit -v
        ;;

    integration)
        echo -e "${GREEN}Running integration tests...${NC}"
        pytest -m integration -v
        ;;

    backend)
        echo -e "${GREEN}Running backend API tests...${NC}"
        pytest tests/backend/ -v
        ;;

    personas)
        echo -e "${GREEN}Running persona system tests...${NC}"
        pytest tests/integration/test_personas.py -v
        ;;

    requirements)
        echo -e "${GREEN}Running requirements extraction tests...${NC}"
        pytest tests/requirements/ -v
        ;;

    ieee)
        echo -e "${GREEN}Running IEEE 29148 compliance tests...${NC}"
        pytest tests/requirements/test_ieee_compliance.py -v
        ;;

    coverage)
        echo -e "${GREEN}Running tests with coverage report...${NC}"
        pytest --cov=src --cov-report=html --cov-report=term
        echo ""
        echo -e "${YELLOW}Coverage report generated in htmlcov/index.html${NC}"
        ;;

    quick)
        echo -e "${GREEN}Running quick tests (unit tests only)...${NC}"
        pytest -m unit -v --tb=short
        ;;

    fast)
        echo -e "${GREEN}Running fast tests (excluding slow tests)...${NC}"
        pytest -v -m "not slow"
        ;;

    watch)
        echo -e "${GREEN}Running tests in watch mode...${NC}"
        if command -v pytest-watch &> /dev/null; then
            ptw
        else
            echo -e "${RED}pytest-watch not installed!${NC}"
            echo "Install it with: pip install pytest-watch"
            echo "Or run tests manually: pytest -v"
            exit 1
        fi
        ;;

    help|--help|-h)
        echo "Usage: ./run_tests.sh [COMMAND]"
        echo ""
        echo "Available commands:"
        echo "  all           - Run all tests (default)"
        echo "  unit          - Run unit tests only"
        echo "  integration   - Run integration tests only"
        echo "  backend       - Run backend API tests"
        echo "  personas      - Run persona system tests"
        echo "  requirements  - Run requirements extraction tests"
        echo "  ieee          - Run IEEE compliance tests"
        echo "  coverage      - Run tests with coverage report"
        echo "  quick         - Run quick tests (unit only, short output)"
        echo "  fast          - Run fast tests (exclude slow tests)"
        echo "  watch         - Run tests in watch mode (requires pytest-watch)"
        echo "  help          - Show this help message"
        echo ""
        echo "Examples:"
        echo "  ./run_tests.sh                # Run all tests"
        echo "  ./run_tests.sh unit           # Run unit tests only"
        echo "  ./run_tests.sh coverage       # Generate coverage report"
        echo ""
        ;;

    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo "Run './run_tests.sh help' for available commands"
        exit 1
        ;;
esac

# Exit code from pytest
EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
else
    echo -e "${RED}✗ Some tests failed. Exit code: $EXIT_CODE${NC}"
fi

exit $EXIT_CODE
