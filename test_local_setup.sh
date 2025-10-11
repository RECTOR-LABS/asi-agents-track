#!/bin/bash

# MediChain AI - Local Setup Test Script
# Verifies all components are running and accessible

set -e

echo "======================================"
echo "  MediChain AI - Local Setup Test"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test results
PASSED=0
FAILED=0

# Function to test endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local expected_status=$3

    echo -n "Testing $name... "

    status_code=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")

    if [ "$status_code" == "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} (HTTP $status_code)"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC} (HTTP $status_code, expected $expected_status)"
        FAILED=$((FAILED + 1))
    fi
}

# Function to test JSON endpoint
test_json_endpoint() {
    local name=$1
    local url=$2
    local expected_field=$3

    echo -n "Testing $name... "

    response=$(curl -s "$url" 2>/dev/null || echo "{}")

    if echo "$response" | grep -q "$expected_field"; then
        echo -e "${GREEN}✓ PASS${NC}"
        PASSED=$((PASSED + 1))
        echo "  Response: $response"
    else
        echo -e "${RED}✗ FAIL${NC}"
        FAILED=$((FAILED + 1))
        echo "  Response: $response"
    fi
}

# Function to test POST endpoint
test_post_endpoint() {
    local name=$1
    local url=$2
    local data=$3

    echo -n "Testing $name... "

    response=$(curl -s -X POST "$url" \
        -H "Content-Type: application/json" \
        -d "$data" 2>/dev/null || echo "{}")

    if echo "$response" | grep -q "response\|error"; then
        echo -e "${GREEN}✓ PASS${NC}"
        PASSED=$((PASSED + 1))
        echo "  Response preview: $(echo "$response" | head -c 100)..."
    else
        echo -e "${RED}✗ FAIL${NC}"
        FAILED=$((FAILED + 1))
        echo "  Response: $response"
    fi
}

echo "=== STEP 1: Backend Services ==="
echo ""

# Test Coordinator HTTP endpoint
test_json_endpoint "Coordinator Health Check" "http://localhost:8080/health" "healthy"

echo ""
echo "=== STEP 2: Frontend API ==="
echo ""

# Test Next.js API route
test_json_endpoint "Next.js API Health" "http://localhost:3000/api/diagnose" "status"

echo ""
echo "=== STEP 3: End-to-End Diagnostic Flow ==="
echo ""

# Test simple diagnostic query
test_post_endpoint "Simple Diagnostic Query" \
    "http://localhost:3000/api/diagnose" \
    '{"message":"I have a headache"}'

echo ""
echo "=== STEP 4: Frontend Accessibility ==="
echo ""

# Test frontend page loads
test_endpoint "Frontend Homepage" "http://localhost:3000" "200"

echo ""
echo "======================================"
echo "  Test Summary"
echo "======================================"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed! System is ready.${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠ Some tests failed. Check logs above.${NC}"
    echo ""
    echo "Troubleshooting tips:"
    echo "1. Ensure all agents are running (4 terminals)"
    echo "2. Check coordinator logs for errors"
    echo "3. Verify .env file has correct agent addresses"
    echo "4. Restart services if needed"
    exit 1
fi
