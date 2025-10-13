# Phase 4 Quick Start - Copy-Paste Commands

**Goal:** Test complete system locally (Frontend + Backend multi-agent flow)

**Time Estimate:** 15-20 minutes

---

## Step 1: Install Frontend Dependencies (2 min)

```bash
cd /Users/rz/local-dev/asi-agents-track/medichain-web
npm install
```

Wait for: `added 350 packages`

---

## Step 2: Configure Frontend (30 sec)

```bash
cd /Users/rz/local-dev/asi-agents-track/medichain-web
cp .env.example .env.local
```

File `medichain-web/.env.local` should contain:
```
COORDINATOR_URL=http://localhost:8080
```

---

## Step 3: Start All Backend Agents (4 terminals)

### Terminal 1: Coordinator (HTTP + uAgent)
```bash
cd /Users/rz/local-dev/asi-agents-track
source venv/bin/activate
python src/agents/coordinator_http.py
```
**Wait for:** `Running on http://0.0.0.0:8080`

---

### Terminal 2: Patient Intake
```bash
cd /Users/rz/local-dev/asi-agents-track
source venv/bin/activate
python src/agents/patient_intake.py
```
**Wait for:** `Agent address: agent1qgr8...`

---

### Terminal 3: Symptom Analysis
```bash
cd /Users/rz/local-dev/asi-agents-track
source venv/bin/activate
python src/agents/symptom_analysis.py
```
**Wait for:** `MeTTa KB loaded: 200+ facts`

---

### Terminal 4: Treatment Recommendation
```bash
cd /Users/rz/local-dev/asi-agents-track
source venv/bin/activate
python src/agents/treatment_recommendation.py
```
**Wait for:** `MeTTa KB loaded: 45+ contraindications`

---

## Step 4: Start Frontend (Terminal 5)

```bash
cd /Users/rz/local-dev/asi-agents-track/medichain-web
npm run dev
```
**Wait for:** `Ready in 2.3s` and `Local: http://localhost:3000`

---

## Step 5: Run Automated Tests (Terminal 6)

```bash
cd /Users/rz/local-dev/asi-agents-track
./test_local_setup.sh
```

**Expected output:**
```
✓ PASS - Coordinator Health Check
✓ PASS - Next.js API Health
✓ PASS - Simple Diagnostic Query
✓ PASS - Frontend Homepage

Passed: 4
Failed: 0
✓ All tests passed! System is ready.
```

---

## Step 6: Manual Browser Test

1. **Open:** http://localhost:3000
2. **Scroll to:** "Try It Now - Live Demo" section
3. **Test Emergency Case:**

**Input:**
```
I have a severe headache, high fever 103°F, and my neck is very stiff.
This started 6 hours ago. I'm 28 years old.
```

**Expected Response (within 10 seconds):**
- Urgency: **EMERGENCY - Seek immediate medical attention**
- Condition: Meningitis (or similar)
- Red flags detected
- Call 911 recommendation

---

## Step 7: Verify Multi-Agent Flow

Watch Terminal 1 (Coordinator) logs during test:

```
INFO: [HTTP] Processing request: http-abc123
INFO: [HTTP] Routing to Patient Intake: agent1qgr8...
INFO: [HTTP] Received diagnostic request for http-abc123
INFO: [HTTP] Routing to Symptom Analysis: agent1qdxq...
INFO: [HTTP] Received symptom analysis for http-abc123
INFO: [HTTP] Routing to Treatment Agent: agent1qg9m...
INFO: [HTTP] Received treatment recommendations for http-abc123
INFO: [HTTP] Request completed: http-abc123
```

**✓ Success:** All 4 agents communicated, response returned

---

## Troubleshooting Quick Fixes

### Issue: Port already in use
```bash
# Kill process on port 8080
lsof -ti:8080 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

---

### Issue: Agent addresses not found
```bash
# Check .env file has addresses
cat .env | grep ADDRESS

# Should show:
# PATIENT_INTAKE_ADDRESS=agent1qgr8ga84fyjsy478ctvzp3zf5r8rw9nulzmrl9w0l3x83suxuzt6zjq29y2
# SYMPTOM_ANALYSIS_ADDRESS=agent1qdxqnfmu735ren2geq9f3n8ehdk43lvm9x0vxswv6xj6a5hn40yfqv0ar42
# TREATMENT_RECOMMENDATION_ADDRESS=agent1qg9m6r976jq4lj64qfnp679qu8lu4jzcy06y09mf7ta4l2sm8uq9qfqrc9v
```

---

### Issue: Connection refused
```bash
# Verify coordinator is running
lsof -i :8080

# Should show Python process on port 8080
```

---

### Issue: Frontend build errors
```bash
cd medichain-web
rm -rf node_modules package-lock.json .next
npm install
npm run dev
```

---

## Success Criteria Checklist

Phase 4.1: Frontend → Coordinator
- [ ] Frontend loads at http://localhost:3000
- [ ] Chat interface visible
- [ ] Can send message
- [ ] Response received within 10 seconds
- [ ] No console errors

Phase 4.2: Multi-Agent Flow
- [ ] Coordinator logs show HTTP request
- [ ] Patient Intake processes message
- [ ] Symptom Analysis queries MeTTa
- [ ] Treatment checks contraindications
- [ ] Complete response returned
- [ ] All 4 agents show activity in logs

---

## Next Steps After Success

✅ **All tests passed?** → Ready for Phase 5 Deployment!

```bash
# Stop all local services (Ctrl+C in each terminal)
# Proceed to Phase 5: Deploy to Render + Vercel
```

---

## Quick Reference: Test Cases

### Test 1: Simple Query
```
Input: I have a fever and cough
Expected: Influenza or COVID-19, urgent care
Time: < 5 seconds
```

### Test 2: Emergency
```
Input: Severe headache, stiff neck, high fever, confusion
Expected: Meningitis, EMERGENCY, call 911
Time: < 8 seconds
```

### Test 3: Routine
```
Input: Runny nose and sneezing for 2 days
Expected: Common cold, routine care
Time: < 5 seconds
```

---

**Alhamdulillah! May this testing go smoothly! 🚀**
