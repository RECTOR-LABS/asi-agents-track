#!/bin/bash
# MediChain AI - Production End-to-End Test Script
# Tests VPS backend + Vercel frontend integration

set -e  # Exit on error

echo "======================================================================"
echo "🏥 MEDICHAIN AI - PRODUCTION END-TO-END TEST"
echo "======================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Test function
test_step() {
    local description=$1
    local command=$2

    echo -n "Testing: $description... "

    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}"
        ((FAILED++))
    fi
}

test_step_with_output() {
    local description=$1
    local command=$2

    echo "Testing: $description..."

    if output=$(eval "$command" 2>&1); then
        echo -e "${GREEN}✅ PASS${NC}"
        echo "Response: $output"
        echo ""
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo "Error: $output"
        echo ""
        ((FAILED++))
    fi
}

echo "======================================================================"
echo "1. VPS BACKEND TESTS"
echo "======================================================================"
echo ""

# Test VPS health endpoint
test_step "VPS health endpoint" \
    "curl -sf http://176.222.53.185:8080/health | grep -q 'healthy'"

# Test VPS services
echo "Checking VPS services..."
ssh website 'sudo systemctl is-active medichain-coordinator.service medichain-patient-intake.service medichain-symptom-analysis.service medichain-treatment.service' | while read status; do
    if [ "$status" = "active" ]; then
        echo -e "  ${GREEN}✅ Service active${NC}"
        ((PASSED++))
    else
        echo -e "  ${RED}❌ Service inactive${NC}"
        ((FAILED++))
    fi
done

echo ""
echo "======================================================================"
echo "2. VERCEL FRONTEND TESTS"
echo "======================================================================"
echo ""

# Test Vercel deployment
test_step "Vercel frontend loads" \
    "curl -sf -o /dev/null -w '%{http_code}' https://medichain-web.vercel.app | grep -q '200'"

test_step "Vercel API route works" \
    "curl -sf https://medichain-web.vercel.app/api/diagnose -X POST -H 'Content-Type: application/json' -d '{\"message\":\"test\"}' > /dev/null"

echo ""
echo "======================================================================"
echo "3. END-TO-END DIAGNOSTIC TESTS"
echo "======================================================================"
echo ""

# Test Case 1: Routine Condition
echo -e "${YELLOW}Test Case 1: Routine Condition (Headache + Fever)${NC}"
test_step_with_output "Routine diagnostic flow" \
    "curl -sf -X POST http://176.222.53.185:8080/api/diagnose -H 'Content-Type: application/json' -d '{\"message\": \"I have a severe headache and fever for 2 days\"}' | python3 -c 'import sys, json; d=json.load(sys.stdin); print(f\"Urgency: {d[\"analysis\"][\"urgency_level\"]}, Diagnoses: {d[\"analysis\"][\"differential_diagnoses\"]}\"); exit(0 if d[\"status\"]==\"completed\" else 1)'"

# Test Case 2: Emergency Condition
echo -e "${YELLOW}Test Case 2: Emergency Condition (Meningitis Symptoms)${NC}"
test_step_with_output "Emergency diagnostic flow" \
    "curl -sf -X POST http://176.222.53.185:8080/api/diagnose -H 'Content-Type: application/json' -d '{\"message\": \"Severe headache, high fever, stiff neck - started 6 hours ago, age 28\"}' | python3 -c 'import sys, json; d=json.load(sys.stdin); print(f\"Urgency: {d[\"analysis\"][\"urgency_level\"]}, Red Flags: {len(d[\"analysis\"][\"red_flags\"])}\"); exit(0 if d[\"status\"]==\"completed\" else 1)'"

echo ""
echo "======================================================================"
echo "4. PERFORMANCE TEST"
echo "======================================================================"
echo ""

echo "Measuring response time..."
START=$(date +%s)
curl -sf -X POST http://176.222.53.185:8080/api/diagnose \
    -H "Content-Type: application/json" \
    -d '{"message": "I have a fever"}' > /dev/null
END=$(date +%s)
DURATION=$((END - START))

echo "Response time: ${DURATION}s"
if [ $DURATION -lt 30 ]; then
    echo -e "${GREEN}✅ PASS (< 30s)${NC}"
    ((PASSED++))
else
    echo -e "${RED}❌ FAIL (> 30s)${NC}"
    ((FAILED++))
fi

echo ""
echo "======================================================================"
echo "TEST SUMMARY"
echo "======================================================================"
echo ""
echo -e "Passed: ${GREEN}${PASSED}${NC}"
echo -e "Failed: ${RED}${FAILED}${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED! Production deployment is ready for demo.${NC}"
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed. Please investigate before demo.${NC}"
    exit 1
fi
