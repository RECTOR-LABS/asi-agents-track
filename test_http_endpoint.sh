#!/bin/bash
# Test script for HTTP endpoint
# Tests the coordinator HTTP bridge locally

echo "🧪 MediChain AI - HTTP Endpoint Test Script"
echo "==========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Base URL
BASE_URL="http://localhost:8080"

echo "📍 Testing endpoint: $BASE_URL"
echo ""

# Test 1: Health Check
echo "Test 1: Health Check"
echo "---------------------"
response=$(curl -s -w "\n%{http_code}" "$BASE_URL/health")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" == "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} - Health check returned 200"
    echo "Response: $body"
else
    echo -e "${RED}✗ FAIL${NC} - Health check returned $http_code"
fi
echo ""

# Test 2: Simple Symptom Query
echo "Test 2: Simple Symptom Query"
echo "-----------------------------"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/diagnose" \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a fever and headache"}')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" == "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} - Diagnosis returned 200"
    echo "Response:"
    echo "$body" | jq '.' 2>/dev/null || echo "$body"
else
    echo -e "${RED}✗ FAIL${NC} - Diagnosis returned $http_code"
    echo "Error: $body"
fi
echo ""

# Test 3: Emergency Case (Meningitis)
echo "Test 3: Emergency Case (Meningitis Symptoms)"
echo "---------------------------------------------"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/diagnose" \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a severe headache, high fever, and my neck is very stiff. This started 6 hours ago. I'\''m 28 years old."}')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" == "200" ]; then
    echo -e "${GREEN}✓ PASS${NC} - Emergency diagnosis returned 200"

    # Check for expected fields
    urgency=$(echo "$body" | jq -r '.analysis.urgency_level' 2>/dev/null)
    if [ "$urgency" == "emergency" ]; then
        echo -e "${GREEN}✓ PASS${NC} - Urgency level correctly identified as emergency"
    else
        echo -e "${YELLOW}⚠ WARNING${NC} - Expected emergency urgency, got: $urgency"
    fi

    # Check for red flags
    red_flags=$(echo "$body" | jq -r '.analysis.red_flags | length' 2>/dev/null)
    if [ "$red_flags" -gt 0 ]; then
        echo -e "${GREEN}✓ PASS${NC} - Red flags detected: $red_flags"
    else
        echo -e "${YELLOW}⚠ WARNING${NC} - No red flags detected (expected for meningitis)"
    fi

    echo ""
    echo "Full Response:"
    echo "$body" | jq '.' 2>/dev/null || echo "$body"
else
    echo -e "${RED}✗ FAIL${NC} - Emergency diagnosis returned $http_code"
    echo "Error: $body"
fi
echo ""

# Test 4: Invalid Request (Missing message field)
echo "Test 4: Invalid Request Handling"
echo "----------------------------------"
response=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/diagnose" \
  -H "Content-Type: application/json" \
  -d '{}')

http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" == "400" ]; then
    echo -e "${GREEN}✓ PASS${NC} - Invalid request correctly returned 400"
    echo "Error message: $body"
else
    echo -e "${RED}✗ FAIL${NC} - Expected 400, got $http_code"
fi
echo ""

echo "==========================================="
echo "🏁 Test suite completed"
echo ""
echo "Note: Full multi-agent flow requires all 4 agents running."
echo "If tests fail with 'Agent not configured' errors, this is expected"
echo "when other agents are not running."
