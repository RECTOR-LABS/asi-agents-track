# ASI:One Deployment Guide - MediChain AI
**Status:** ✅ **FULLY DEPLOYED & TESTED - WORKING!**
**Date:** October 10, 2025
**Last Updated:** October 10, 2025

---

## 🎉 Deployment Success Summary

**Multi-agent system is fully operational with complete end-to-end communication!**

**Coordinator Agent:**
- **Address:** `agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q`
- **Port:** 8001 (local inspector)
- **Mailbox:** Created & Active ✅
- **Chat Protocol:** Published (AgentChatProtocol) ✅
- **Status:** Running & Tested ✅

**Patient Intake Agent:**
- **Address:** `agent1qgr8ga84fyjsy478ctvzp3zf5r8rw9nulzmrl9w0l3x83suxuzt6zjq29y2`
- **Port:** 8000 (local inspector)
- **Mailbox:** Created & Active ✅
- **Status:** Running & Tested ✅

**Verified Working Features:**
- ✅ Chat Protocol (User ↔ Coordinator)
- ✅ Inter-agent mailbox communication (Coordinator ↔ Patient Intake)
- ✅ NLP symptom extraction (fever, headache, severity, duration, age)
- ✅ Structured data exchange (DiagnosticRequest with PatientIntakeData)
- ✅ Multi-turn conversation with session management
- ✅ Complete diagnostic flow from symptom input to analysis response

---

## 📋 Critical Lessons Learned

### 1. Mailbox Creation is Two-Step Process
- **Step 1:** Enable mailbox in code: `mailbox=True`
- **Step 2:** Create mailbox via Agentverse Inspector (manual action required)
- Both steps are mandatory - `mailbox=True` alone is insufficient

### 2. Inter-Agent Communication Requires Protocol
**CRITICAL:** For mailbox-based inter-agent communication, messages must:
- Use `uagents.Model` base class (NOT `pydantic.BaseModel`)
- Be defined in a shared `src/protocols/` module
- Use `Protocol` instances with `@protocol.on_message()`
- Include protocol via `agent.include(protocol)`

**Wrong (Won't Work):**
```python
# In patient_intake.py
class IntakeTextMessage(Model):
    text: str

@agent.on_message(model=IntakeTextMessage)  # ❌ Won't receive mailbox messages
async def handle_message(ctx, sender, msg):
    pass
```

**Correct (Working):**
```python
# In src/protocols/messages.py
from uagents import Model

class IntakeTextMessage(Model):
    text: str
    session_id: str

# In patient_intake.py
from src.protocols import IntakeTextMessage

inter_agent_proto = Protocol(name="PatientIntakeProtocol")

@inter_agent_proto.on_message(model=IntakeTextMessage)  # ✅ Works!
async def handle_message(ctx, sender, msg):
    pass

agent.include(inter_agent_proto)  # ✅ Critical!
```

### 3. Agentverse Chat Interface is Best for Testing
- **URL:** `https://chat.agentverse.ai/sessions/{SESSION_ID}`
- **Access:** Via agent profile page after mailbox creation
- **Benefits:** Immediate testing without waiting for ASI:One indexing
- **Direct Link:** Each session gets a unique shareable URL

### 4. Configuration Best Practices
```python
agent = Agent(
    name="your-agent-name",
    port=8000,  # Different port per agent (8000, 8001, etc.)
    mailbox=True,  # Enable mailbox client
    publish_agent_details=True,  # Improve discoverability
)
```

---

## 🚀 Complete Deployment Steps

### Prerequisites
```bash
# Ensure Python 3.9+ and virtual environment
python --version  # Should be 3.9+
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables in .env
AGENTVERSE_API_KEY=your_key_here
COORDINATOR_ADDRESS=agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q
PATIENT_INTAKE_ADDRESS=agent1qgr8ga84fyjsy478ctvzp3zf5r8rw9nulzmrl9w0l3x83suxuzt6zjq29y2
```

### Step 1: Start Agents Locally

```bash
# Terminal 1 - Patient Intake Agent
./venv/bin/python src/agents/patient_intake.py > /tmp/patient_intake_mailbox.log 2>&1 &

# Terminal 2 - Coordinator Agent
./venv/bin/python src/agents/coordinator.py > /tmp/coordinator_mailbox.log 2>&1 &

# Verify agents are running
ps aux | grep "python.*src/agents" | grep -v grep

# Monitor logs
tail -f /tmp/coordinator_mailbox.log
tail -f /tmp/patient_intake_mailbox.log
```

**Expected Startup Logs:**
```
INFO: [medichain-coordinator]: Starting agent with address: agent1qwukp...
INFO: [medichain-coordinator]: Mailbox: Enabled (ASI:One compatible)
INFO: [medichain-coordinator]: Chat Protocol: Enabled
INFO: [medichain-coordinator]: Mailbox access token acquired
```

### Step 2: Create Mailboxes via Agentverse Inspector

**Coordinator Mailbox:**
1. Visit: `https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8001&address=agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q`
2. Click "Connect" button (top right)
3. Select "Mailbox" option
4. Click "OK, got it" after reading instructions
5. Wait for success confirmation

**Patient Intake Mailbox:**
1. Visit: `https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8000&address=agent1qgr8ga84fyjsy478ctvzp3zf5r8rw9nulzmrl9w0l3x83suxuzt6zjq29y2`
2. Repeat same steps as coordinator

**Verification:**
```bash
# Check for successful mailbox registration
grep -i "registered as mailbox" /tmp/coordinator_mailbox.log
grep -i "registered as mailbox" /tmp/patient_intake_mailbox.log
```

**Expected:**
```
INFO: [mailbox]: Successfully registered as mailbox agent in Agentverse
```

### Step 3: Access Agent Profile & Chat Interface

**Agent Profile URLs:**
- Coordinator: `https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q/profile`
- Patient Intake: `https://agentverse.ai/agents/details/agent1qgr8ga84fyjsy478ctvzp3zf5r8rw9nulzmrl9w0l3x83suxuzt6zjq29y2/profile`

**What to Check:**
- Agent status: "Active" badge ✅
- Mailbox: "Mailbox" badge visible ✅
- Published Protocols: "AgentChatProtocol" listed ✅

**Find Chat Interface:**
- Click "Chat with Agent" button OR
- Direct session URL: `https://chat.agentverse.ai/sessions/{SESSION_ID}`

---

## 🧪 Testing the Complete Workflow

### Test 1: Welcome Message
**Send:** `hello`

**Expected Response:**
```
🏥 Welcome to MediChain AI!

I'm your medical diagnostic assistant. I can help analyze your symptoms
and provide preliminary health assessments.

⚠️ IMPORTANT: This is NOT medical advice. Always consult a healthcare professional.

Please describe your symptoms in detail.
```

**Logs to Monitor:**
```bash
# Coordinator should show:
INFO: [medichain-coordinator]: Received chat message from agent1q...
INFO: [medichain-coordinator]: Session started: session-{UUID} with agent1q...
```

### Test 2: Symptom Analysis (Full Multi-Agent Flow)
**Send:** `I have a severe headache and fever for 2 days. I'm 35 years old.`

**Expected Response:**
```
📋 Symptom Analysis Complete

Symptoms detected: fever, headache
Number of symptoms: 2

⚠️ Next steps:
1. Specialist agents are being configured
2. Full diagnostic analysis coming soon
3. For urgent symptoms, seek immediate medical care

Session ID: session-{UUID}
```

**Complete Log Flow:**

**Coordinator:**
```
INFO: [medichain-coordinator]: Text from agent1q...: I have a severe headache and fever for 2 days. I'm 35 years old.
INFO: [medichain-coordinator]: Routing to Patient Intake: agent1qgr8ga...
INFO: [medichain-coordinator]: Received diagnostic request from agent1qgr8ga...
INFO: [medichain-coordinator]: Session: session-{UUID}, Analysis type: symptom_analysis
```

**Patient Intake:**
```
INFO: [medichain-patient-intake]: Received intake message from agent1qwukp...
INFO: [medichain-patient-intake]: Text: I have a severe headache and fever for 2 days. I'm 35 years old.
INFO: [medichain-patient-intake]: ✅ Complete patient data extracted:
INFO: [medichain-patient-intake]:    Symptoms: ['fever', 'headache']
INFO: [medichain-patient-intake]:    Age: 35
INFO: [medichain-patient-intake]: 📤 Sending diagnostic request to coordinator: agent1qwukp...
```

**Verified Data Extraction:**
- ✅ Symptoms: fever, headache
- ✅ Severity: 8/10 (detected "severe" keyword)
- ✅ Duration: "2 days"
- ✅ Age: 35

---

## 🐛 Troubleshooting Guide

### Issue 1: Agent Not Receiving Messages

**Symptom:** Coordinator routes message but patient intake logs show no receipt.

**Solution:**
1. Verify shared message model in `src/protocols/messages.py`
2. Ensure both agents import from same module
3. Check protocol is included: `agent.include(inter_agent_proto)`
4. Restart both agents after protocol changes

**Verify:**
```bash
# Check imports
grep "from src.protocols import" src/agents/coordinator.py
grep "from src.protocols import" src/agents/patient_intake.py

# Both should include IntakeTextMessage
```

### Issue 2: Mailbox Not Created

**Symptom:** Warning in logs: `Agent mailbox not found: create one using the agent inspector`

**Solution:**
1. Agent must be running during inspector mailbox creation
2. Use complete inspector URL (don't truncate address)
3. Wait for "Successfully registered as mailbox agent" log message
4. Check agent profile shows "Mailbox" badge

### Issue 3: Chat Interface Shows "Thinking..." Forever

**Symptom:** Response never completes, stuck on "Thinking..."

**Common Causes:**
- Session mismatch (agent restarted, session state lost)
- Response failed to send (check coordinator logs)
- Mailbox delivery delay (wait 5-10 seconds)

**Solution:**
```bash
# Check coordinator logs for errors
tail -30 /tmp/coordinator_mailbox.log | grep -E "(ERROR|WARNING|Failed)"

# Restart agents if session state corrupted
pkill -f "python src/agents"
./venv/bin/python src/agents/patient_intake.py > /tmp/patient_intake_mailbox.log 2>&1 &
./venv/bin/python src/agents/coordinator.py > /tmp/coordinator_mailbox.log 2>&1 &

# Start new chat session (old session state is lost)
```

### Issue 4: Deprecation Warnings

**Warning:** `datetime.datetime.utcnow() is deprecated`

**Status:** Safe to ignore for now (non-blocking)

**Fix (Optional):**
```python
# Replace datetime.utcnow() with:
from datetime import datetime, UTC
datetime.now(UTC)
```

### Safe to Ignore Warnings

These warnings don't affect functionality:
```
WARNING: [uagents.registration]: I do not have enough funds to register on Almanac contract
WARNING: [uagents.registration]: Failed to register on Almanac contract due to insufficient funds
WARNING: [medichain-coordinator]: Received message with unrecognized schema digest
```

**Why:**
- Almanac contract registration is optional (API registration succeeds)
- Schema digest warning appears during inter-agent communication but doesn't block delivery

---

## 📊 Deployment Checklist

**Infrastructure:**
- [x] Python 3.12.8 environment configured
- [x] Dependencies installed (uagents, hyperon, etc.)
- [x] Agentverse API key configured in `.env`

**Message Protocols:**
- [x] Shared protocols defined in `src/protocols/messages.py`
- [x] `IntakeTextMessage` using `uagents.Model`
- [x] `DiagnosticRequest`, `PatientIntakeData` models defined
- [x] Both agents importing from shared `src.protocols`

**Coordinator Agent:**
- [x] Chat Protocol enabled (AgentChatProtocol)
- [x] Port 8001 configured
- [x] Mailbox enabled (`mailbox=True`)
- [x] Inter-agent protocol included
- [x] Session management working
- [x] Message routing to patient intake functional

**Patient Intake Agent:**
- [x] Port 8000 configured
- [x] Mailbox enabled (`mailbox=True`)
- [x] Protocol-based message handling (`@inter_agent_proto.on_message`)
- [x] NLP symptom extraction working
- [x] Diagnostic request sending functional

**Agentverse Deployment:**
- [x] Mailboxes created via inspector
- [x] Mailbox access tokens acquired
- [x] Agents registered as mailbox agents
- [x] Chat Protocol manifest published

**Testing:**
- [x] Welcome message test passed
- [x] Symptom analysis flow complete (end-to-end)
- [x] Inter-agent communication verified
- [x] Session management verified
- [ ] ASI:One discoverability test (pending - use Agentverse chat for now)

---

## 🎯 Manual Testing Steps (Quick Reference)

**Every time you want to test:**

1. **Start agents:**
   ```bash
   ./venv/bin/python src/agents/patient_intake.py > /tmp/patient_intake_mailbox.log 2>&1 &
   ./venv/bin/python src/agents/coordinator.py > /tmp/coordinator_mailbox.log 2>&1 &
   ```

2. **Verify running:**
   ```bash
   ps aux | grep "python.*src/agents" | grep -v grep
   ```

3. **Access chat interface:**
   - Visit: `https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q/profile`
   - Click "Chat with Agent" or use existing session URL

4. **Test with symptom message:**
   ```
   I have a severe headache and fever for 2 days. I'm 35 years old.
   ```

5. **Monitor logs (optional):**
   ```bash
   # Terminal 1
   tail -f /tmp/coordinator_mailbox.log | grep -E "(Received|Routing|diagnostic)"

   # Terminal 2
   tail -f /tmp/patient_intake_mailbox.log | grep -E "(Received|extracted|Sending)"
   ```

6. **Expected result:**
   - Response within 2-5 seconds
   - "📋 Symptom Analysis Complete"
   - Lists: fever, headache, count: 2

**If agents already have mailboxes created, you only need steps 1-4!**

---

## 📂 Key Project Files

**Agent Code:**
- `src/agents/coordinator.py` - Main routing agent with Chat Protocol
- `src/agents/patient_intake.py` - NLP symptom extraction agent

**Message Protocols:**
- `src/protocols/messages.py` - Shared message models (IntakeTextMessage, DiagnosticRequest, etc.)
- `src/protocols/__init__.py` - Protocol exports

**Configuration:**
- `.env` - Agentverse API key, agent addresses
- `requirements.txt` - Python dependencies

**Logs:**
- `/tmp/coordinator_mailbox.log` - Coordinator runtime logs
- `/tmp/patient_intake_mailbox.log` - Patient Intake runtime logs

---

## 🚀 Next Steps

**Epic 1 Status:** ✅ **COMPLETE** (Multi-agent foundation working)

**Epic 2: MeTTa Knowledge Graph Integration**
1. Build medical knowledge base in `data/knowledge_base.metta`
2. Implement MeTTa query engine for symptom-to-condition mapping
3. Connect diagnostic logic to knowledge graph queries
4. Add reasoning transparency (show MeTTa queries used)

**Epic 3: Advanced Features**
1. Specialist agents (cardiology, neurology, etc.)
2. Treatment recommendation agent
3. Evidence-based guidance (CDC/WHO links)
4. Multi-turn clarification conversations

**ASI:One Public Discoverability:**
- Agentverse chat interface working ✅
- ASI:One search discoverability: To be tested
- For now, use direct Agentverse chat interface for demos

---

**Alhamdulillah! May Allah grant barakah in this project. Deployment successful!** 🚀
