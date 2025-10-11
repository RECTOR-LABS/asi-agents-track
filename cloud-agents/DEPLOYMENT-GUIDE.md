# MediChain AI - Cloud Deployment Guide

## 📋 Overview

This guide provides step-by-step instructions for deploying all 5 MediChain AI agents to Agentverse cloud.

**Deployment Time**: ~30-45 minutes (all 5 agents)
**Prerequisites**: Agentverse account, 5 agents already created

---

## 🎯 Agent Summary

| # | Agent Name | File | Address | Purpose |
|---|------------|------|---------|---------|
| 1 | **MediChain Coordinator** | `1_coordinator_agent.py` | `agent1qdp74e...` | Main router, Chat Protocol, ASI:One interface |
| 2 | **MediChain Patient Intake** | `2_patient_intake_agent.py` | `agent1qfxfjs...` | Symptom extraction, NLP pattern matching |
| 3 | **(Skip Knowledge Graph)** | *(Not used)* | `agent1qtjcz8...` | *(Legacy - not in current flow)* |
| 4 | **MediChain Symptom Analysis** | `4_symptom_analysis_agent.py` | `agent1q036yw...` | Diagnosis, urgency assessment, MeTTa KB |
| 5 | **MediChain Treatment** | `5_treatment_recommendation_agent.py` | `agent1q0q46z...` | Treatments, contraindications, MeTTa KB |

**Note**: We created 5 agents on Agentverse, but only 4 are used in the current workflow. The Knowledge Graph agent is legacy and can be skipped or deleted.

---

## 📁 Files Structure

```
cloud-agents/
├── 1_coordinator_agent.py               # Coordinator code (copy to Build tab)
├── 1_coordinator_README.md              # Coordinator docs (copy to README tab)
├── 2_patient_intake_agent.py            # Patient Intake code
├── 2_patient_intake_README.md           # Patient Intake docs
├── 4_symptom_analysis_agent.py          # Symptom Analysis code (with MeTTa KB)
├── 4_symptom_analysis_README.md         # Symptom Analysis docs
├── 5_treatment_recommendation_agent.py  # Treatment code (with MeTTa KB)
├── 5_treatment_recommendation_README.md # Treatment docs
└── DEPLOYMENT-GUIDE.md                  # This file
```

---

## 🚀 Deployment Steps

### 🔹 Agent 1: MediChain Coordinator

**Purpose**: Main orchestrator with Chat Protocol for ASI:One

1. **Navigate to Agentverse Dashboard**
   ```
   https://agentverse.ai/agents
   ```

2. **Select Agent**: Click "MediChain Coordinator" (agent1qdp74e...)

3. **Open Build Tab**: Click "Build" in left sidebar

4. **Replace agent.py**:
   - Click on `agent.py` file in the file list
   - **Delete all existing code**
   - Open `/cloud-agents/1_coordinator_agent.py` in your editor
   - **Copy entire file contents** (Ctrl+A, Ctrl+C)
   - **Paste into Agentverse editor** (Ctrl+V)
   - Click "Save" button (top right)

5. **Update README**:
   - Click "New File" button → Enter filename: `README.md` → Click Create
   - Open `/cloud-agents/1_coordinator_README.md` in your editor
   - **Copy entire file contents**
   - **Paste into Agentverse README.md**
   - Click "Save"

6. **Deploy**:
   - Click "Deploy" button (top right)
   - Wait for "Deployed successfully" message
   - ✅ Agent 1 complete!

---

### 🔹 Agent 2: MediChain Patient Intake

**Purpose**: Symptom extraction via NLP pattern matching

1. **Select Agent**: Click "MediChain Patient Intake" (agent1qfxfjs...)

2. **Build Tab**: Click "Build"

3. **Replace agent.py**:
   - Click `agent.py`
   - **Delete all code**
   - Open `/cloud-agents/2_patient_intake_agent.py`
   - **Copy entire contents**
   - **Paste into editor**
   - Click "Save"

4. **Create README.md**:
   - Click "New File" → `README.md` → Create
   - Open `/cloud-agents/2_patient_intake_README.md`
   - **Copy and paste contents**
   - Click "Save"

5. **Deploy**:
   - Click "Deploy"
   - Wait for success message
   - ✅ Agent 2 complete!

---

### 🔹 Agent 3: MediChain Knowledge Graph (SKIP - Legacy)

**Status**: Created but not used in current workflow

**Options**:
- **Option A (Recommended)**: Leave empty / unused
- **Option B**: Delete the agent from Agentverse
- **Option C**: Deploy placeholder code (not recommended)

**Why skip?** The Symptom Analysis and Treatment agents now have embedded MeTTa KB, making the standalone Knowledge Graph agent redundant.

---

### 🔹 Agent 4: MediChain Symptom Analysis

**Purpose**: Diagnostic reasoning with embedded MeTTa KB (585 lines)

⚠️ **IMPORTANT**: This file is large (~1100 lines) due to embedded knowledge base

1. **Select Agent**: Click "MediChain Symptom Analysis" (agent1q036yw...)

2. **Build Tab**: Click "Build"

3. **Replace agent.py**:
   - Click `agent.py`
   - **Delete all code**
   - Open `/cloud-agents/4_symptom_analysis_agent.py`
   - **Copy entire contents** (this may take a moment - file is large)
   - **Paste into editor**
   - Click "Save" (may take a few seconds to process)

4. **Create README.md**:
   - Click "New File" → `README.md` → Create
   - Open `/cloud-agents/4_symptom_analysis_README.md`
   - **Copy and paste contents**
   - Click "Save"

5. **Deploy**:
   - Click "Deploy"
   - ⏳ Wait for deployment (may take 30-60 seconds due to file size)
   - ✅ Agent 4 complete!

**Troubleshooting**:
- If deployment fails with "timeout", try again - large files may need multiple attempts
- If editor is slow, paste in smaller chunks (e.g., first half, save, then second half)

---

### 🔹 Agent 5: MediChain Treatment Recommendation

**Purpose**: Evidence-based treatment recommendations with safety validation

⚠️ **IMPORTANT**: This file is also large (~900 lines) due to embedded knowledge base

1. **Select Agent**: Click "MediChain Treatment" (agent1q0q46z...)

2. **Build Tab**: Click "Build"

3. **Replace agent.py**:
   - Click `agent.py`
   - **Delete all code**
   - Open `/cloud-agents/5_treatment_recommendation_agent.py`
   - **Copy entire contents** (large file)
   - **Paste into editor**
   - Click "Save"

4. **Create README.md**:
   - Click "New File" → `README.md` → Create
   - Open `/cloud-agents/5_treatment_recommendation_README.md`
   - **Copy and paste contents**
   - Click "Save"

5. **Deploy**:
   - Click "Deploy"
   - ⏳ Wait for deployment (30-60 seconds)
   - ✅ Agent 5 complete!

---

## ✅ Deployment Verification

### Check Agent Status

1. **Go to Agents Dashboard**: https://agentverse.ai/agents

2. **Verify All Agents Show "Active"**:
   - ✅ MediChain Coordinator - Active
   - ✅ MediChain Patient Intake - Active
   - ✅ MediChain Symptom Analysis - Active
   - ✅ MediChain Treatment - Active

3. **Check Logs**:
   - Click each agent → "Logs" tab
   - Look for startup messages:
     - "MediChain AI - [Agent Name] (Cloud)"
     - "Agent address: agent1q..."
     - "Agent is READY"

### Test Basic Functionality

**Option 1: Agentverse Chat Interface**

1. Go to any agent's profile page:
   ```
   https://agentverse.ai/agents/details/{AGENT_ADDRESS}/profile
   ```

2. Click "Chat with Agent" or open direct chat link

3. For **Coordinator Only**: Send test message:
   ```
   Hello, I have a fever and headache
   ```

4. Expected response: Welcome message + symptom analysis in progress

**Option 2: ASI:One Interface** (May take time to index)

1. Visit: https://asi1.ai/ or https://chat.agentverse.ai/

2. Search for: `@medichain-coordinator`

3. Start conversation with symptom description

4. Verify complete diagnostic flow

---

## 🔧 Post-Deployment Configuration

### No Configuration Needed! ✨

All agent addresses are **hard-coded** in the cloud deployment files:

```python
# In Coordinator
PATIENT_INTAKE_ADDRESS = "agent1qfxfjs7y6gxa8psr5mzugcg45j46znra4qg0t5mxljjv5g9mx7dw6238e4a"
SYMPTOM_ANALYSIS_ADDRESS = "agent1q036yw3pwsal2qsrq502k546lyxvnf6wt5l83qfhzhvceg6nm2la7nd6d5n"
TREATMENT_RECOMMENDATION_ADDRESS = "agent1q0q46ztah7cyw4z7gcg3mued9ncnrcvrcqc8kjku3hywqdzp03e36hk5qsl"

# In Patient Intake, Symptom Analysis, Treatment
COORDINATOR_ADDRESS = "agent1qdp74ezv3eas5q60s4650xt97ew5kmyt9de77w2ku55jxys8uq2uk0u440d"
```

**Benefits**:
- No .env file needed
- No Agent Secrets configuration
- Works immediately after deployment
- Zero inter-agent communication setup

---

## 📊 Expected Performance

| Metric | Target | Actual (Cloud) |
|--------|--------|----------------|
| **Response Time** | < 5 seconds | ~3-7 seconds (depends on MeTTa queries) |
| **Uptime** | 24/7 | Agentverse managed |
| **Concurrent Sessions** | Multiple | Supported |
| **Knowledge Base** | 13 conditions, 200+ facts | ✅ Embedded |
| **Chat Protocol** | ASI:One compatible | ✅ Enabled |

---

## 🐛 Troubleshooting

### Issue: Agent shows "Inactive" after deployment

**Solutions**:
1. Check Logs tab for error messages
2. Verify entire code was copied (check file size)
3. Re-deploy agent
4. If persistent, delete and recreate agent

### Issue: "hyperon package not available" warning

**Impact**: Low - agents will use fallback rule-based logic
**Solutions**:
- ✅ **Recommended**: Ignore warning - fallback mode works for hackathon demo
- ⚠️ Advanced: Contact Agentverse support to install hyperon package

### Issue: Inter-agent communication not working

**Checks**:
1. Verify all 4 active agents show "Active" status
2. Check agent addresses match hard-coded values in code
3. Review Coordinator logs for "Routing to..." messages
4. Review specialist agent logs for "Received request from..." messages

### Issue: Chat interface not responding

**Checks**:
1. Verify Coordinator agent is "Active"
2. Check Coordinator has Chat Protocol enabled (agent.include(chat_proto, publish_manifest=True))
3. Try direct Agentverse chat interface first: `https://chat.agentverse.ai/`
4. ASI:One (asi1.ai) may take 15-30 minutes to index new agents

---

## 📝 Testing Checklist

After deployment, test the following scenarios:

### ✅ Basic Flow
- [ ] Welcome message appears when starting session
- [ ] Symptom extraction works (fever, headache → structured data)
- [ ] Urgency assessment completes (emergency/urgent/routine)
- [ ] Differential diagnoses returned (2-5 conditions)
- [ ] Treatment recommendations provided
- [ ] Final report compiled correctly

### ✅ Edge Cases
- [ ] No symptoms detected → Clarification question
- [ ] Red flag symptoms → Emergency urgency
- [ ] Multiple conditions matched → Ranked list
- [ ] Contraindications flagged correctly
- [ ] Age-based risk adjustment (test with age < 5 or > 65)

### ✅ Error Handling
- [ ] Invalid input → Graceful error message
- [ ] Network timeout → Retry or fallback
- [ ] Session end → Clean cleanup

---

## 🎉 Success Criteria

**Deployment is successful when**:

✅ All 4 agents show "Active" status
✅ Coordinator agent responds to test message
✅ End-to-end diagnostic flow completes
✅ Final report includes:
   - Symptom summary
   - Urgency assessment
   - Differential diagnoses
   - Treatment recommendations
   - Safety warnings
   - Specialist referral
   - Medical disclaimer

---

## 📚 Next Steps

After successful deployment:

1. **Test via ASI:One** (https://asi1.ai/)
   - Search for `@medichain-coordinator`
   - Test multiple symptom scenarios
   - Document any issues

2. **Record Demo Video**
   - Show ASI:One interaction
   - Demonstrate diagnostic flow
   - Highlight MeTTa reasoning transparency

3. **Update README.md** (main project)
   - Add cloud agent addresses
   - Update deployment status
   - Link to demo video

4. **Prepare Hackathon Submission**
   - GitHub repository link
   - Demo video URL
   - Agent addresses
   - Innovation Lab badges

---

## 🆘 Support

**Issues?** Check:
- Agent Logs tab in Agentverse
- This troubleshooting guide
- Project CLAUDE.md for context

**Still stuck?** Document the issue with:
- Agent name
- Error message from logs
- Steps to reproduce
- Expected vs actual behavior

---

**Deployment Guide Version**: 1.0
**Last Updated**: October 11, 2025
**Author**: MediChain AI Development Team

Bismillah - May Allah grant ease in deployment! 🚀
