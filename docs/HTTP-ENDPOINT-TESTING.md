# HTTP Endpoint Testing Guide

> **⚠️ DEPRECATED:** This guide covers legacy HTTP coordinator variants (`coordinator_http.py`, `coordinator_queue.py`) that are no longer deployed. Current production uses **Chat Protocol (mailbox-based)** via Agentverse. For testing, use the [Agentverse chat interface](https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q) instead.

**Testing the coordinator HTTP bridge locally** *(Legacy)*

## Quick Start

### 1. Install Flask Dependencies

```bash
pip install flask flask-cors
```

Or reinstall all requirements:
```bash
pip install -r requirements.txt
```

### 2. Start Coordinator with HTTP Bridge

```bash
python src/agents/coordinator_http.py
```

**Expected Output:**
```
🚀 Starting MediChain Coordinator with HTTP Bridge...
   - uAgent: Mailbox + ASI:One
   - HTTP: Port 8080

✅ uAgent started
🌐 Starting HTTP server...
 * Running on http://0.0.0.0:8080
```

### 3. Run Test Script (Automated)

```bash
chmod +x test_http_endpoint.sh
./test_http_endpoint.sh
```

---

## Manual Testing with curl

### Test 1: Health Check

```bash
curl http://localhost:8080/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "agent": "medichain-coordinator",
  "timestamp": "2025-10-11T..."
}
```

### Test 2: Simple Diagnosis

```bash
curl -X POST http://localhost:8080/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{"message": "I have a fever and headache"}'
```

**Expected Response** (if all agents running):
```json
{
  "session_id": "http-...",
  "status": "completed",
  "timestamp": "2025-10-11T...",
  "analysis": {
    "urgency_level": "routine",
    "red_flags": [],
    "differential_diagnoses": ["influenza", "common-cold", ...],
    "confidence_scores": {...},
    "recommended_action": "..."
  },
  "treatment": {
    "condition": "influenza",
    "treatments": [...],
    "evidence_sources": {...},
    "contraindications": {...},
    "safety_warnings": [...],
    "specialist_referral": "...",
    "follow_up_timeline": "...",
    "medical_disclaimer": "..."
  }
}
```

### Test 3: Emergency Case (Meningitis)

```bash
curl -X POST http://localhost:8080/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have a severe headache, high fever, and my neck is very stiff. This started 6 hours ago. I am 28 years old."
  }'
```

**Expected:**
- `urgency_level: "emergency"`
- `red_flags: ["Meningitis triad..."]`
- `treatments: ["immediate-911", ...]`

---

## Testing with Postman / Insomnia

**Import this request:**

**URL:** `http://localhost:8080/api/diagnose`
**Method:** `POST`
**Headers:**
```
Content-Type: application/json
```
**Body (JSON):**
```json
{
  "message": "I have a severe headache, high fever, and my neck is very stiff. This started 6 hours ago. I'm 28 years old."
}
```

---

## Multi-Agent Flow Testing

**To test the complete multi-agent flow, you need all 4 agents running:**

### Terminal 1: Coordinator (HTTP Bridge)
```bash
python src/agents/coordinator_http.py
```

### Terminal 2: Patient Intake
```bash
python src/agents/patient_intake.py
```

### Terminal 3: Symptom Analysis
```bash
python src/agents/symptom_analysis.py
```

### Terminal 4: Treatment Recommendation
```bash
python src/agents/treatment_recommendation.py
```

### Terminal 5: Send Test Request
```bash
curl -X POST http://localhost:8080/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{"message": "I have severe headache and high fever"}'
```

**Watch the logs across all 4 terminals to see the multi-agent flow!**

---

## Expected Errors (When Testing Without Other Agents)

### Agent Not Configured Error

```json
{
  "error": "Agent not configured",
  "message": "Patient Intake Agent address not configured. Please set PATIENT_INTAKE_ADDRESS environment variable."
}
```

**This is expected!** The HTTP endpoint works, but needs agent addresses configured.

**Solution:** Either:
1. Run all 4 agents locally (as shown above)
2. Or configure agent addresses in `.env` (after Render deployment)

---

## Timeout Testing

The endpoint has a **30-second timeout**. If processing takes longer, you'll get:

```json
{
  "error": "Request timeout",
  "message": "The diagnostic process took too long. Please try again."
}
```

**This is rare but can happen if:**
- MeTTa queries are slow
- Network delays between agents
- Agent overload

---

## CORS Testing (Frontend Integration)

When testing with Next.js frontend:

**Allowed Origins:**
- `http://localhost:3000` (local development)
- `https://*.vercel.app` (Vercel preview deployments)
- `https://*.rectorspace.com` (production domain)

**Test CORS:**
```bash
curl -X OPTIONS http://localhost:8080/api/diagnose \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST"
```

**Expected:** CORS headers in response allowing the origin.

---

## Troubleshooting

### Issue 1: "Connection refused"

**Cause:** Coordinator not running or wrong port

**Fix:**
```bash
# Check if process is running
lsof -i :8080

# If not running, start coordinator
python src/agents/coordinator_http.py
```

### Issue 2: "Module 'flask' not found"

**Cause:** Flask not installed

**Fix:**
```bash
pip install flask flask-cors
```

### Issue 3: "Request timeout"

**Cause:** Multi-agent flow taking too long or agents not responding

**Fix:**
- Check all agent logs for errors
- Verify agent addresses in `.env`
- Ensure all 4 agents are running

### Issue 4: Empty response or 500 error

**Cause:** Exception in agent processing

**Fix:**
- Check coordinator logs for stack trace
- Verify message models match across agents
- Test with simpler message first

---

## Performance Benchmarks

**Expected Response Times:**

| Test Case | Time | Notes |
|-----------|------|-------|
| Health check | <50ms | No agent processing |
| Simple diagnosis (all agents local) | 2-5s | Full multi-agent flow |
| Emergency case (all agents local) | 3-6s | More complex reasoning |
| Timeout threshold | 30s | Hard limit |

**Note:** Remote agents (Render) may add 1-2s network latency.

---

## Next Steps

After successful local testing:

1. ✅ Proceed to **Phase 2.3:** Update `render.yaml`
2. ✅ Then **Phase 3:** Build Next.js frontend
3. ✅ Deploy to Render (Phase 5)
4. ✅ Test production endpoint at `https://medichain-coordinator.onrender.com`

---

**Alhamdulillah! HTTP endpoint testing complete!** 🎉
