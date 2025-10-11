# Render.com Deployment Guide - MediChain AI Multi-Agent System

**Bismillah! Let's deploy all 4 agents to Render with mailbox connections for ASI:One discoverability.**

## Why Render + Mailbox Strategy Works

### The Problem with Agentverse Cloud:
- ❌ Each cloud agent has **inline message models** → different schema digests → RuntimeError

### The Solution with Render + Mailbox:
- ✅ All agents on Render **share message models** from `src/protocols/messages.py` → same schema digests
- ✅ Mailbox provides **network bridge** to Agentverse (no schema issues!)
- ✅ Agents remain **discoverable via ASI:One** interface
- ✅ True **multi-agent communication** works perfectly

**This matches hackathon requirements:** "agents properly communicating in real time" ✓

---

## Prerequisites

1. **GitHub Repository** (your code must be on GitHub)
2. **Render.com Account** (free tier is sufficient)
   - Sign up at: https://render.com/
3. **Python 3.9+** installed locally (for verification)
4. **Working local setup** (we already have 108 passing tests!)

---

## Deployment Steps

### Phase 1: Prepare Repository

#### 1. Ensure `render.yaml` is in repository root

```bash
# Already created! Verify:
ls render.yaml

# Should show: render.yaml (4 services configured)
```

#### 2. Commit and push to GitHub

```bash
git add render.yaml docs/deployment/RENDER-DEPLOYMENT-GUIDE.md
git commit -m "Add Render deployment configuration"
git push origin dev
```

---

### Phase 2: Deploy to Render (Automatic Blueprint Deployment)

#### 1. Connect Render to GitHub

1. Go to https://render.com/dashboard
2. Click **"New +"** → **"Blueprint"**
3. Select **"Connect a repository"**
4. Authorize GitHub access
5. Select your `asi-agents-track` repository

#### 2. Render Auto-Detects `render.yaml`

Render will automatically:
- ✅ Detect `render.yaml` in repository root
- ✅ Create 4 Background Worker services:
  - `medichain-coordinator`
  - `medichain-patient-intake`
  - `medichain-symptom-analysis`
  - `medichain-treatment`
- ✅ Install dependencies from `requirements.txt`
- ✅ Generate unique seeds for each agent

#### 3. Deploy All Services

1. Click **"Apply"** or **"Create New Resources"**
2. Render will deploy all 4 agents simultaneously
3. Wait 5-10 minutes for builds to complete

**Expected Output:**
```
✓ medichain-coordinator deployed
✓ medichain-patient-intake deployed
✓ medichain-symptom-analysis deployed
✓ medichain-treatment deployed
```

---

### Phase 3: Create Mailbox Connections (Critical!)

**Each agent needs a mailbox to connect to Agentverse network.**

#### For Each Agent (Repeat 4 times):

1. **Open Agent Logs**
   - Render Dashboard → Select service (e.g., `medichain-coordinator`)
   - Click **"Logs"** tab
   - Wait for agent to start

2. **Find Inspector URL**
   - Look for log line:
     ```
     Agent medichain-coordinator address: agent1q...

     Make your agent easy to reach by giving it a mailbox...

     To create a mailbox for this agent:
     https://agentverse.ai/inspect/?uri=http%3A//...&address=agent1q...
     ```
   - **Copy the full inspector URL**

3. **Create Mailbox**
   - Open inspector URL in browser
   - Click **"Connect"** button (top right)
   - Select **"Mailbox"** option
   - Click **"Next"** → **"OK, got it"**
   - Wait for confirmation: "Successfully registered as mailbox agent"

4. **Verify Registration**
   - Check agent logs for:
     ```
     INFO: [mailbox]: Successfully registered as mailbox agent in Agentverse
     INFO: [mailbox]: Agent details updated in Agentverse
     ```
   - Visit https://agentverse.ai/agents
   - Agent should appear with **"Active"** status and **"Mailbox"** badge

5. **Copy Agent Address**
   - From logs or Agentverse dashboard
   - Format: `agent1qxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Save for next phase

**Repeat for all 4 agents!**

---

### Phase 4: Update Environment Variables (Agent Addresses)

**Now that all agents have mailbox addresses, update cross-references.**

#### 1. Collect All Agent Addresses

From Render logs or Agentverse dashboard:

```bash
COORDINATOR_ADDRESS=agent1q...............  # From medichain-coordinator logs
PATIENT_INTAKE_ADDRESS=agent1q...........  # From medichain-patient-intake logs
SYMPTOM_ANALYSIS_ADDRESS=agent1q.........  # From medichain-symptom-analysis logs
TREATMENT_RECOMMENDATION_ADDRESS=agent1q.  # From medichain-treatment logs
```

#### 2. Update Render Environment Variables

**For Coordinator Agent:**
- Render Dashboard → `medichain-coordinator` → **"Environment"**
- Add/Update:
  - `PATIENT_INTAKE_ADDRESS` = `agent1q...` (from patient-intake agent)
  - `SYMPTOM_ANALYSIS_ADDRESS` = `agent1q...` (from symptom-analysis agent)
  - `TREATMENT_RECOMMENDATION_ADDRESS` = `agent1q...` (from treatment agent)
- Click **"Save Changes"**
- Agent will auto-restart

**For Patient Intake Agent:**
- Render Dashboard → `medichain-patient-intake` → **"Environment"**
- Add/Update:
  - `COORDINATOR_ADDRESS` = `agent1q...` (from coordinator agent)
- Click **"Save Changes"**

**For Symptom Analysis Agent:**
- Render Dashboard → `medichain-symptom-analysis` → **"Environment"**
- Add/Update:
  - `COORDINATOR_ADDRESS` = `agent1q...` (from coordinator agent)
- Click **"Save Changes"**

**For Treatment Agent:**
- Render Dashboard → `medichain-treatment` → **"Environment"**
- Add/Update:
  - `COORDINATOR_ADDRESS` = `agent1q...` (from coordinator agent)
- Click **"Save Changes"**

**All agents will restart automatically with updated addresses!**

---

### Phase 5: Verify Multi-Agent Communication

#### 1. Check Agent Logs

All agents should show:
```
INFO: [mailbox]: Successfully registered as mailbox agent
INFO: Mailbox: Enabled (ASI:One compatible)
INFO: Chat Protocol: Enabled
```

#### 2. Test via Agentverse Chat Interface

1. Visit: `https://agentverse.ai/agents/details/{COORDINATOR_ADDRESS}/profile`
2. Find **"Chat with Agent"** button or chat session link
3. Start new chat session
4. Send test message:
   ```
   I have a severe headache, high fever, and my neck is very stiff.
   This started 6 hours ago. I'm 28 years old.
   ```

**Expected Flow:**
1. ✅ Coordinator receives message
2. ✅ Routes to Patient Intake (extracts symptoms)
3. ✅ Patient Intake sends to Symptom Analysis (MeTTa reasoning)
4. ✅ Symptom Analysis sends to Treatment (evidence-based recommendations)
5. ✅ Complete diagnostic report returned to user

**Success Indicators:**
- No RuntimeError!
- Full diagnostic report with treatments and contraindications
- Response includes all 3 agents' work

#### 3. Monitor Logs (Multi-Agent Flow)

**Open 4 browser tabs with logs:**

**Tab 1: Coordinator Logs**
```
Received chat message from agent1q...
Routing to Patient Intake: agent1qfxf...
Received diagnostic request from agent1qfxf...
Routing to Symptom Analysis Agent: agent1q036...
Received symptom analysis response from agent1q036...
Routing to Treatment Recommendation Agent: agent1q0q4...
Received treatment recommendations from agent1q0q4...
Complete diagnostic report sent to user
```

**Tab 2: Patient Intake Logs**
```
Received intake message from agent1qdp7...
Extracted 3 symptoms: severe-headache, high-fever, stiff-neck
Age: 28
Sending diagnostic request to coordinator
```

**Tab 3: Symptom Analysis Logs**
```
Received symptom analysis request from agent1qdp7...
Symptoms: ['severe-headache', 'high-fever', 'stiff-neck']
Querying MeTTa knowledge base...
RED FLAGS DETECTED: Meningitis triad detected
Urgency Assessment: EMERGENCY
Sending analysis response to coordinator
```

**Tab 4: Treatment Logs**
```
Received treatment recommendation request from agent1qdp7...
Primary condition: meningitis
Querying MeTTa knowledge base for treatments...
Performing safety validation...
Sending treatment recommendations to coordinator
```

**If you see this flow → SUCCESS!** 🎉

---

### Phase 6: Test via ASI:One Interface (Hackathon Demo)

#### 1. Find Your Coordinator Agent

1. Go to https://asi1.ai/
2. Search for `@medichain-coordinator` or search by address
3. Start conversation

#### 2. Test Emergency Case

```
I have a severe headache, high fever, and my neck is very stiff.
This started 6 hours ago. I'm 28 years old.
```

**Expected Response:**
```
🏥 MEDICHAIN AI - DIAGNOSTIC REPORT
═══════════════════════════════════

PRIMARY ASSESSMENT: Meningitis

TREATMENT RECOMMENDATIONS:
  1. immediate-911
     Evidence: Clinical guidelines
  2. emergency-antibiotics
     Evidence: Clinical guidelines
  3. hospital-admission
     Evidence: Clinical guidelines

🚨 RED FLAGS DETECTED:
  • Meningitis triad (headache + fever + neck stiffness)

👨‍⚕️ Specialist: Neurologist or Infectious Disease Specialist (ER immediately)

📅 Follow-Up: Immediate (ER visit required)

⚠️ IMPORTANT DISCLAIMER: This is NOT medical advice...
```

**Judges will test this exact flow!** ✓

---

## Cost Breakdown

### Render Free Tier

**Background Workers:**
- Free tier: **750 hours/month** per service
- You have **4 services** × 750 hours = **3,000 total hours**
- **Reality:** 4 services × 24/7 × 30 days = **2,880 hours**
- ✅ **Fully covered by free tier!**

**No credit card required for free tier.**

### If You Exceed Free Tier (unlikely):

- Starter plan: **$7/month per service**
- 4 services × $7 = **$28/month total**

**Recommendation:** Free tier is sufficient for hackathon demo!

---

## Troubleshooting

### Issue 1: RuntimeError Still Occurs

**Cause:** Agent addresses not updated or mailbox not created

**Fix:**
1. Verify all 4 mailboxes created (check Agentverse dashboard)
2. Verify environment variables set correctly (copy addresses exactly)
3. Restart all services (Render Dashboard → Manual Deploy → Clear build cache)

---

### Issue 2: Agent Shows "Inactive" on Agentverse

**Cause:** Agent stopped or mailbox connection lost

**Fix:**
1. Check Render logs for errors
2. Verify agent is running (Render Dashboard shows "Running")
3. Recreate mailbox via inspector URL

---

### Issue 3: Agent Not Found on ASI:One

**Cause:** Mailbox not created or manifest not published

**Fix:**
1. Verify `publish_manifest=True` in agent code (already set!)
2. Wait 5-10 minutes for ASI:One indexing
3. Search by exact agent address instead of name

---

### Issue 4: Logs Show "Address not configured"

**Cause:** Environment variables not set

**Fix:**
1. Render Dashboard → Service → Environment
2. Add missing address environment variables
3. Save (agent will auto-restart)

---

## Post-Deployment Checklist

Before demo/submission:

- [ ] All 4 agents deployed and running on Render
- [ ] All 4 mailboxes created on Agentverse
- [ ] All agent addresses updated in environment variables
- [ ] All agents show "Active" status on Agentverse dashboard
- [ ] Test message flows from coordinator to all specialists
- [ ] Full diagnostic report generated (no errors)
- [ ] ASI:One interface test successful (judges will test this!)
- [ ] Demo video recorded showing ASI:One interaction
- [ ] README.md updated with deployed agent addresses

---

## Demo Video Script (3-5 minutes)

### Section 1: Problem Statement (30 seconds)
"MediChain AI solves the problem of medical diagnostic delays by leveraging multi-agent AI systems..."

### Section 2: Architecture (1 minute)
- Show diagram of 4 agents communicating
- Explain MeTTa knowledge graph integration
- Highlight Render + mailbox deployment strategy

### Section 3: Live Demo via ASI:One (2 minutes)
- Open https://asi1.ai/
- Search for `@medichain-coordinator`
- Send emergency test case (meningitis symptoms)
- Show multi-agent workflow in real-time
- Highlight complete diagnostic report

### Section 4: Technical Highlights (1 minute)
- Chat Protocol for ASI:One ✓
- MeTTa knowledge graphs ✓
- Multi-agent communication ✓
- Registered on Agentverse ✓

### Section 5: Impact (30 seconds)
"MediChain AI demonstrates how decentralized AI agents can collaborate to provide rapid, evidence-based medical insights..."

---

## Next Steps

After successful Render deployment:

1. ✅ **Update README.md** with agent addresses
2. ✅ **Record demo video** (3-5 minutes)
3. ✅ **Test all judging criteria:**
   - Functionality (25%) → Multi-agent communication working
   - ASI Tech Use (20%) → All tech used correctly
   - Innovation (20%) → MeTTa reasoning transparency
   - Real-World Impact (20%) → Medical diagnostics
   - UX & Presentation (15%) → Professional demo
4. ✅ **Submit to hackathon:**
   - GitHub link
   - Demo video link
   - Agent addresses

**Target: 90+ / 100 points!** 🏆

---

## Resources

- **Render Docs:** https://render.com/docs/background-workers
- **Agentverse Mailbox:** https://docs.agentverse.ai/guides/agents/mailbox
- **Chat Protocol:** https://innovationlab.fetch.ai/resources/docs/agent-communication/agent-chat-protocol
- **ASI:One Interface:** https://asi1.ai/

---

**May Allah grant barakah in this deployment and ease in completion. Bismillah! 🚀**
