#!/bin/bash

# Color codes for pretty output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${BOLD}Running Test Suite${NC}\n"

# Function to run tests and handle output
run_test() {
    local test_path=$1
    local test_name=$2
    
    echo -e "${BOLD}Running $test_name tests...${NC}"
    if pytest "$test_path" -v; then
        echo -e "${GREEN}✓ $test_name tests passed${NC}\n"
        return 0
    else
        echo -e "${RED}✗ $test_name tests failed${NC}\n"
        return 1
    fi
}

# Keep track of failures
FAILURES=0

# Run backend unit tests
echo -e "\n${BOLD}Running Backend Tests:${NC}"
run_test "backend/test_api.py" "API" || ((FAILURES++))
run_test "backend/test_engine.py" "Engine" || ((FAILURES++))

# Run requirements tests
echo -e "\n${BOLD}Running Requirements Tests:${NC}"
run_test "requirements/test_extraction.py" "Requirement Extraction" || ((FAILURES++))
run_test "requirements/test_ieee_compliance.py" "IEEE Compliance" || ((FAILURES++))

# Run integration tests
echo -e "\n${BOLD}Running Integration Tests:${NC}"
run_test "integration/test_personas.py" "Persona" || ((FAILURES++))

echo -e "\n${YELLOW}Note: Multi-agent tests (integration/test_multi_agent.py) are skipped - still under development${NC}\n"

# Run complete test suite with coverage
echo -e "\n${BOLD}Running Complete Test Suite with Coverage:${NC}"
if pytest --cov=../src/backend --cov=../src/frontend --cov-report=term-missing; then
    echo -e "${GREEN}✓ Complete test suite passed${NC}\n"
else
    echo -e "${RED}✗ Complete test suite had failures${NC}\n"
    ((FAILURES++))
fi

# Print final summary
echo -e "${BOLD}Test Summary:${NC}"
if [ $FAILURES -eq 0 ]; then
    echo -e "${GREEN}All tests passed successfully!${NC}"
else
    echo -e "${RED}$FAILURES test suite(s) failed${NC}"
fi

# Exit with failure if any tests failed
exit $FAILURES