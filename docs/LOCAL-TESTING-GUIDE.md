# Local Testing Guide - Phase 4

Complete guide for testing the MediChain AI system locally before deployment.

---

## Prerequisites

- Python 3.9+ with virtual environment activated
- Node.js 18+ and npm installed
- All agent addresses populated in `.env` file
- MeTTa knowledge base at `data/knowledge_base.metta`

---

## Phase 4.1: Frontend → Coordinator Integration Test

### Step 1: Install Frontend Dependencies

```bash
cd medichain-web
npm install
```

**Expected output:**
```
added 350 packages in 45s
```

**Troubleshooting:**
- If `npm` not found: Install Node.js from https://nodejs.org/
- If permission errors: Don't use `sudo`, check npm prefix
- If package conflicts: Delete `node_modules/` and `package-lock.json`, retry

---

### Step 2: Configure Frontend Environment

Create `.env.local` file in `medichain-web/`:

```bash
cd medichain-web
cp .env.example .env.local
```

Edit `.env.local`:

```bash
# For local testing
COORDINATOR_URL=http://localhost:8080
```

**Note:** This points to the local coordinator's HTTP endpoint (port 8080).

---

### Step 3: Start Backend Agents

Open **4 separate terminal windows** in project root:

#### Terminal 1: Coordinator (HTTP + uAgent)
```bash
cd /Users/rz/local-dev/asi-agents-track
source venv/bin/activate
python src/agents/coordinator_http.py
```

**Expected output:**
```
🚀 Starting MediChain Coordinator with HTTP Bridge...
   - uAgent: Mailbox + ASI:One
   - HTTP: Port 8080

INFO: [coordinator] Agent address: agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q
✅ uAgent started
🌐 Starting HTTP server...
 * Running on http://0.0.0.0:8080
```

**Troubleshooting:**
- Port 8080 in use: Kill process with `lsof -ti:8080 | xargs kill -9`
- Import errors: Check `pip list | grep uagents`

---

#### Terminal 2: Patient Intake Agent
```bash
cd /Users/rz/local-dev/asi-agents-track
source venv/bin/activate
python src/agents/patient_intake.py > /tmp/patient_intake_test.log 2>&1 &
tail -f /tmp/patient_intake_test.log
```

**Expected output:**
```
INFO: [patient-intake] Agent address: agent1qgr8ga84fyjsy478ctvzp3zf5r8rw9nulzmrl9w0l3x83suxuzt6zjq29y2
INFO: [patient-intake] Listening for diagnostic requests...
```

---

#### Terminal 3: Symptom Analysis Agent
```bash
cd /Users/rz/local-dev/asi-agents-track
source venv/bin/activate
python src/agents/symptom_analysis.py > /tmp/symptom_analysis_test.log 2>&1 &
tail -f /tmp/symptom_analysis_test.log
```

**Expected output:**
```
INFO: [symptom-analysis] Agent address: agent1qdxqnfmu735ren2geq9f3n8ehdk43lvm9x0vxswv6xj6a5hn40yfqv0ar42
INFO: [symptom-analysis] MeTTa KB loaded: 200+ facts, 13 conditions
```

---

#### Terminal 4: Treatment Recommendation Agent
```bash
cd /Users/rz/local-dev/asi-agents-track
source venv/bin/activate
python src/agents/treatment_recommendation.py > /tmp/treatment_test.log 2>&1 &
tail -f /tmp/treatment_test.log
```

**Expected output:**
```
INFO: [treatment] Agent address: agent1qg9m6r976jq4lj64qfnp679qu8lu4jzcy06y09mf7ta4l2sm8uq9qfqrc9v
INFO: [treatment] MeTTa KB loaded: 45+ contraindications
```

---

### Step 4: Start Frontend Development Server

Open **Terminal 5**:

```bash
cd /Users/rz/local-dev/asi-agents-track/medichain-web
npm run dev
```

**Expected output:**
```
  ▲ Next.js 14.2.5
  - Local:        http://localhost:3000
  - Network:      http://192.168.1.10:3000

 ✓ Ready in 2.3s
```

**Troubleshooting:**
- Port 3000 in use: Use `PORT=3001 npm run dev`
- TypeScript errors: Check `tsconfig.json` paths
- Module not found: Run `npm install` again

---

### Step 5: Open Browser and Test

1. **Open:** http://localhost:3000
2. **Verify landing page loads:**
   - Hero section with "MediChain AI"
   - 6 feature cards
   - Architecture diagram
   - Live chat interface at bottom

3. **Scroll to "Try It Now" section**

4. **Test Case 1: Simple Query**
   - Input: `I have a headache and fever`
   - Click Send
   - **Expected:** Loading indicator appears, then AI response

5. **Monitor Terminal 1 (Coordinator logs):**
   ```
   INFO: [HTTP] Processing request: http-{uuid}
   INFO: [HTTP] Routing to Patient Intake: agent1qgr8...
   INFO: [HTTP] Received symptom analysis for http-{uuid}
   INFO: [HTTP] Routing to Treatment Agent: agent1qg9m...
   INFO: [HTTP] Request completed: http-{uuid}
   ```

6. **Verify response contains:**
   - Diagnostic analysis
   - Urgency level
   - Treatment recommendations
   - Medical disclaimer

---

### Step 6: Test Emergency Case

Input:
```
I have a severe headache, high fever 103°F, and my neck is very stiff.
This started 6 hours ago. I'm 28 years old and feel confused.
```

**Expected response should include:**
- **Urgency:** EMERGENCY - Seek immediate medical attention
- **Condition:** Meningitis (or similar critical condition)
- **Red Flags:** Neck stiffness, high fever, altered mental status
- **Action:** Call 911 immediately

**Monitor logs for:**
```
INFO: [symptom-analysis] Red flags detected: ['neck-stiffness', 'high-fever', ...]
INFO: [symptom-analysis] Urgency level: emergency
INFO: [treatment] Primary condition: meningitis
INFO: [treatment] Contraindications checked: 5 items
```

---

### Step 7: Test API Health Check

Open new terminal:

```bash
curl http://localhost:3000/api/diagnose
```

**Expected output:**
```json
{
  "status": "ok",
  "service": "MediChain AI - Diagnostic API",
  "coordinator_url": "http://localhost:8080",
  "timestamp": "2025-10-11T12:34:56.789Z"
}
```

Test coordinator directly:

```bash
curl http://localhost:8080/health
```

**Expected output:**
```json
{
  "status": "healthy",
  "agent": "medichain-coordinator",
  "timestamp": "2025-10-11T12:34:56.789Z"
}
```

---

## Phase 4.2: Multi-Agent Flow Verification

### Detailed Log Analysis

Run a test query and observe the complete flow:

#### 1. User Input → Frontend
```
Browser: User types "fever and cough"
Frontend: POST /api/diagnose {"message": "fever and cough"}
```

#### 2. Next.js API Route → Coordinator HTTP
```
Terminal (Next.js): [13:45:12] POST /api/diagnose 200 in 5234ms
Terminal 1 (Coordinator): [HTTP] Processing request: http-abc123
```

#### 3. Coordinator → Patient Intake Agent
```
Terminal 1: [HTTP] Routing to Patient Intake: agent1qgr8...
Terminal 2: [patient-intake] Received intake message from coordinator
Terminal 2: [patient-intake] Extracted symptoms: ['fever', 'cough']
Terminal 2: [patient-intake] Sending diagnostic request to coordinator
```

#### 4. Coordinator → Symptom Analysis Agent
```
Terminal 1: [HTTP] Received diagnostic request for http-abc123
Terminal 1: [HTTP] Routing to Symptom Analysis: agent1qdxq...
Terminal 3: [symptom-analysis] Analyzing symptoms: ['fever', 'cough']
Terminal 3: [symptom-analysis] MeTTa query: find_conditions_by_symptoms
Terminal 3: [symptom-analysis] Confidence scores: {'influenza': 0.75, 'covid-19': 0.68, ...}
Terminal 3: [symptom-analysis] Urgency level: urgent
```

#### 5. Coordinator → Treatment Agent
```
Terminal 1: [HTTP] Received symptom analysis for http-abc123
Terminal 1: [HTTP] Routing to Treatment Agent: agent1qg9m...
Terminal 4: [treatment] Primary condition: influenza
Terminal 4: [treatment] MeTTa query: get_treatment_recommendations
Terminal 4: [treatment] Checking contraindications...
Terminal 4: [treatment] Treatments: ['rest', 'hydration', 'oseltamivir']
Terminal 4: [treatment] Sending response to coordinator
```

#### 6. Coordinator → Frontend Response
```
Terminal 1: [HTTP] Received treatment recommendations for http-abc123
Terminal 1: [HTTP] Request completed: http-abc123
Browser: Response received, diagnostic report displayed
```

**Total time:** Should be < 10 seconds

---

## Verification Checklist

### Frontend Tests
- [ ] Landing page loads without errors
- [ ] Chat interface renders correctly
- [ ] Message input accepts text
- [ ] Send button is clickable
- [ ] Loading indicator appears during processing
- [ ] Response displays in chat bubbles
- [ ] Auto-scroll works
- [ ] Mobile responsive layout works

### Backend Tests
- [ ] All 4 agents start without errors
- [ ] HTTP endpoint responds to health check
- [ ] Coordinator receives HTTP requests
- [ ] Patient Intake processes symptoms
- [ ] Symptom Analysis queries MeTTa KB
- [ ] Treatment Agent checks contraindications
- [ ] Complete diagnostic flow completes

### Multi-Agent Communication
- [ ] Coordinator → Patient Intake (IntakeTextMessage)
- [ ] Patient Intake → Coordinator (DiagnosticRequest)
- [ ] Coordinator → Symptom Analysis (SymptomAnalysisRequestMsg)
- [ ] Symptom Analysis → Coordinator (SymptomAnalysisResponseMsg)
- [ ] Coordinator → Treatment (TreatmentRequestMsg)
- [ ] Treatment → Coordinator (TreatmentResponseMsg)
- [ ] Coordinator → HTTP Response (Complete JSON)

### Error Handling
- [ ] Empty message rejected by API route
- [ ] Invalid JSON returns 400 error
- [ ] Timeout after 30 seconds returns 504
- [ ] Agent offline shows error message
- [ ] Network error handled gracefully

---

## Common Issues and Solutions

### Issue: "Connection refused" error

**Symptoms:**
```
ERROR: Failed to connect to coordinator at http://localhost:8080
```

**Solution:**
1. Verify coordinator is running: `lsof -i :8080`
2. Check coordinator logs for startup errors
3. Ensure Flask server started (look for "Running on http://0.0.0.0:8080")

---

### Issue: "Agent not configured" error

**Symptoms:**
```json
{
  "error": "Agent not configured",
  "message": "Patient Intake Agent address not configured"
}
```

**Solution:**
1. Check `.env` file has all agent addresses
2. Verify addresses match running agents
3. Restart coordinator after updating `.env`

---

### Issue: Agents not communicating

**Symptoms:**
- Request timeout after 30 seconds
- No logs in specialist agent terminals

**Solution:**
1. Verify all agents are running (4 terminals active)
2. Check agent addresses in `.env` match agent logs
3. Look for connection errors in coordinator logs
4. Restart all agents in order: Patient Intake → Symptom Analysis → Treatment → Coordinator

---

### Issue: Frontend build errors

**Symptoms:**
```
Error: Cannot find module 'lucide-react'
```

**Solution:**
1. Delete `node_modules/` and `package-lock.json`
2. Run `npm install` again
3. Clear Next.js cache: `rm -rf .next/`
4. Restart dev server

---

### Issue: TypeScript errors

**Symptoms:**
```
Type error: Property 'content' does not exist on type 'Message'
```

**Solution:**
1. Check `tsconfig.json` paths are correct
2. Restart TypeScript server in IDE
3. Run `npm run build` to see full errors
4. Check imports match exported types

---

## Performance Benchmarks

Target response times for local testing:

| Test Case | Expected Time | Max Acceptable |
|-----------|---------------|----------------|
| Simple query (2 symptoms) | 3-5 seconds | 10 seconds |
| Complex query (5+ symptoms) | 5-8 seconds | 15 seconds |
| Emergency case | 4-6 seconds | 12 seconds |
| Health check | < 100ms | 500ms |

**If times exceed max acceptable:**
1. Check MeTTa KB size (should be < 1MB)
2. Verify no network delays (all local)
3. Profile MeTTa queries (use `time` module)
4. Check CPU/memory usage

---

## Next Steps After Successful Testing

Once all tests pass:

✅ **Phase 4 Complete** → Proceed to Phase 5: Deployment

- Deploy all 4 agents to Render
- Create mailbox connections
- Deploy frontend to Vercel
- Configure custom domain
- Run production tests

---

## Testing Log Template

Use this template to document your test results:

```
MEDICHAIN AI - LOCAL TESTING LOG
Date: YYYY-MM-DD
Tester: [Your Name]

=== ENVIRONMENT ===
Python Version: [version]
Node Version: [version]
OS: [macOS/Linux/Windows]

=== AGENTS STARTED ===
[ ] Coordinator (port 8080)
[ ] Patient Intake (port 8000)
[ ] Symptom Analysis (port 8004)
[ ] Treatment (port 8005)

=== FRONTEND ===
[ ] Dependencies installed
[ ] Dev server running (port 3000)
[ ] Landing page loads

=== TEST CASES ===
[ ] Test 1: Simple query - PASS/FAIL
    Input: "I have a headache"
    Response time: [X seconds]
    Notes: [any issues]

[ ] Test 2: Emergency case - PASS/FAIL
    Input: "Severe headache, stiff neck, high fever"
    Response time: [X seconds]
    Urgency detected: [emergency/urgent/routine]
    Notes: [any issues]

[ ] Test 3: API health check - PASS/FAIL
    Status: [200/error]
    Response: [json output]

=== MULTI-AGENT FLOW ===
[ ] Coordinator logs show HTTP request
[ ] Patient Intake receives message
[ ] Symptom Analysis queries MeTTa
[ ] Treatment checks contraindications
[ ] Complete response returned

=== ISSUES ENCOUNTERED ===
1. [Issue description]
   Solution: [how resolved]

=== OVERALL RESULT ===
[ ] PASS - Ready for deployment
[ ] FAIL - Issues need resolution

Notes: [additional observations]
```

---

**May Allah grant ease in testing and success in deployment! Bismillah!**
