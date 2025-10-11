# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**ASI Agents Track - Hackathon Submission**

Multi-agent healthcare diagnostic system built for the Artificial Superintelligence Alliance Agents Track hackathon (Cypherpunk 2025). Implements coordinator-specialist agent architecture using Fetch.ai's uAgents framework + SingularityNET's MeTTa knowledge graph.

**Key Info:**
- **Deadline:** October 31, 2025 (22 days from start)
- **Prize Pool:** $20,000 USDC
- **Current Status:** 95% complete - 13+ days ahead of schedule!
- **Project:** MediChain AI - Decentralized Healthcare Diagnostic System

---

## Technology Stack

- **Language:** Python 3.9+
- **Agent Framework:** Fetch.ai uAgents (`uagents>=0.12.0`, `uagents-core>=0.1.0`)
- **Knowledge Graph:** SingularityNET MeTTa (`hyperon>=0.1.0`)
- **Deployment:** Agentverse (https://agentverse.ai/) + VPS (Ubuntu 22.04)
- **Frontend:** Next.js 14 (Vercel) - Static landing page
- **Testing:** pytest, Agentverse chat interface

---

## Development Commands

### Environment Setup
```bash
# Initial setup
./setup.sh

# Activate virtual environment
source venv/bin/activate  # macOS/Linux

# Install/update dependencies
pip install -r requirements.txt
```

### Running Agents Locally
```bash
# Start coordinator (Chat Protocol enabled, port 8000)
python src/agents/coordinator.py

# Start specialist agents
python src/agents/patient_intake.py        # Port 8001
python src/agents/symptom_analysis.py      # Port 8004
python src/agents/treatment_recommendation.py  # Port 8005

# Test MeTTa query engine
python src/metta/query_engine.py
```

### Testing
```bash
# Run all tests
pytest tests/

# With coverage
pytest --cov=src tests/

# Code quality
black --line-length=88 src/ tests/
flake8 src/ tests/
mypy src/
```

### VPS Service Management
```bash
# Check status
ssh website 'sudo systemctl status medichain-*.service'

# View logs
ssh website 'sudo journalctl -u medichain-coordinator.service -f'

# Restart all
ssh website 'sudo systemctl restart medichain-*.service'
```

---

## Current Architecture & Production URLs

### Production Architecture (Day 6 - Current)

```
User → Vercel Landing Page → "Test on Agentverse" Button
                                      ↓
                        Agentverse Chat Interface
                                      ↓
                          VPS Multi-Agent System
                        (4 agents via mailbox protocol)
```

**Why This Architecture:**
- Vercel Free tier has 10-second timeout (multi-agent flow takes ~15 seconds)
- Leverages official ASI infrastructure (better for hackathon judging)
- Complete separation: Marketing (Vercel) + Functionality (Agentverse)

### Production URLs

**User-Facing:**
- **Pitch Website:** https://medichain-web.rectorspace.com
- **Testing Platform:** https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q

**Backend (VPS):**
- **Health Check:** http://176.222.53.185:8080/health
- **All 4 agents:** Running as systemd services (24/7 uptime)

### Deployed Agents

- **Coordinator:** `agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q` (port 8001)
- **Patient Intake:** `agent1qgr8ga84fyjsy478ctvzp3zf5r8rw9nulzmrl9w0l3x83suxuzt6zjq29y2` (port 8000)
- **Symptom Analysis:** `agent1qdxqnfmu735ren2geq9f3n8ehdk43lvm9x0vxswv6xj6a5hn40yfqv0ar42` (port 8004)
- **Treatment:** `agent1qg9m6r976jq4lj64qfnp679qu8lu4jzcy06y09mf7ta4l2sm8uq9qfqrc9v` (port 8005)

---

## MeTTa Knowledge Graph (Quick Reference)

### Knowledge Base Location
- **File:** `data/knowledge_base.metta`
- **Config:** `METTA_KB_PATH` in `.env`

### Key Statistics
- 13 medical conditions (6 critical, 2 urgent, 5 common)
- 200+ medical facts
- 45+ contraindications
- Evidence sources: CDC, WHO, AHA, Johns Hopkins

### Essential Methods
```python
from src.metta.query_engine import MeTTaQueryEngine

engine = MeTTaQueryEngine()

# Basic queries
results = engine.find_by_symptom("fever")
treatments = engine.find_treatment("influenza")

# Medical-specific (16 advanced methods)
emergencies = engine.find_emergency_conditions()
red_flags = engine.find_red_flag_symptoms()
urgency = engine.find_urgency_level("meningitis")
reasoning = engine.generate_reasoning_chain(symptoms, condition)
contraindications = engine.get_all_contraindications("aspirin")
```

**See:** `src/metta/query_engine.py` for complete method list (21 methods total)

---

## Testing Strategy

### Agentverse Chat Testing (RECOMMENDED)

**After mailbox creation, test via Agentverse chat interface:**

1. **Access agent profile:**
   ```
   https://agentverse.ai/agents/details/{AGENT_ADDRESS}/profile
   ```

2. **Click "Chat with Agent" button**

3. **Test conversation flow** - Verify:
   - ChatAcknowledgement sent for every message
   - Multi-agent routing works
   - MeTTa queries return expected results
   - Session lifecycle (start → messages → end)

**Example test case:**
- Emergency: "Severe headache, high fever, stiff neck - started 6 hours ago, age 28"
- Routine: "I have a severe headache and fever for 2 days"

### Mailbox Creation (CRITICAL)

1. Start agent locally with `mailbox=True`
2. Open inspector URL from logs: `https://agentverse.ai/inspect/?uri=...`
3. Click "Connect" → Select "Mailbox" → "OK, got it"
4. Verify in logs: `Successfully registered as mailbox agent in Agentverse`
5. Check dashboard: Agent should show "Active" status

**Note:** `mailbox=True` enables mailbox CLIENT. Actual mailbox must be created via inspector.

---

## Key Documentation Files

### Planning & Execution (Review Daily)
- **docs/PRD.md** - Product Requirements (Epic → Story → Task) - **SINGLE SOURCE OF TRUTH**
- **docs/EXECUTION-PLAN.md** - Progress tracker (update daily: 🔲 → 🟡 → ✅)
- **docs/TIMELINE.md** - 22-day development plan

### Current Guidance
- **CLAUDE.md** - This file - current development guidance
- **README.md** - Main project documentation
- **docs/TRACK-REQUIREMENTS.md** - Submission checklist

### Reference & History
- **docs/PROJECT-HISTORY.md** - Complete development history (Day 5/6 logs, fixes, 30 lessons)
- **docs/reference/hackathon-analysis.md** - Strategic analysis
- **docs/deployment/** - Deployment guides and status

### Planning Workflow
1. **Before starting:** Check docs/PRD.md for Epic/Story/Task requirements
2. **Daily updates:** Update docs/EXECUTION-PLAN.md with progress
3. **Weekly checkpoints:** Review docs/TIMELINE.md
4. **All work traces back to PRD** - No ad-hoc features

---

## Chat Protocol Implementation

### Pattern
```python
from uagents_core.contrib.protocols.chat import (
    ChatMessage, ChatAcknowledgement,
    StartSessionContent, TextContent, EndSessionContent,
    chat_protocol_spec
)

chat_proto = Protocol(spec=chat_protocol_spec)

@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    # Process msg.content items
    # ALWAYS send ChatAcknowledgement
    await ctx.send(sender, ChatAcknowledgement())

agent.include(chat_proto, publish_manifest=True)
```

**Key:** Always include `publish_manifest=True` for ASI:One discoverability.

---

## Judging Criteria Focus

- **Functionality (25%):** Reliable multi-agent coordination
- **ASI Tech (20%):** Deep MeTTa integration (not superficial)
- **Innovation (20%):** Novel problem-solving approach
- **Impact (20%):** Real-world usefulness
- **Presentation (15%):** Professional demo + docs

**Target:** 90+/100 points for top-3 finish

---

## Submission Requirements

**Must Have:**
- ✅ Public GitHub repo with Innovation Lab badges
- ✅ Multi-agent system deployed on Agentverse
- ✅ Deep MeTTa integration (200+ facts)
- ✅ Chat Protocol working
- ⏳ Demo video (3-5 minutes) - **IN PROGRESS**
- ⏳ README with agent addresses and URLs

**Innovation Lab Badges:**
```markdown
![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)
```

---

## Important Constraints

### What NOT to Do
- **Don't skip Chat Protocol** - Required for discoverability
- **Don't do superficial MeTTa** - Judges look for depth
- **Don't commit secrets** - .env is gitignored
- **Don't skip testing** - Broken demo = disqualification

### Development Philosophy
- **100% working standard** - No partial implementations
- **Ship with excellence** - Production-ready quality
- **Time philosophy** - Quality over urgency
- **Test-driven** - Test locally before deployment

---

## 12 Crucial Tips for Future Claude Instances

1. **PRD is SSOT** - All work traces back to docs/PRD.md Epic/Story/Task structure
2. **Update EXECUTION-PLAN daily** - Track progress (🔲 → 🟡 → ✅)
3. **Test Agentverse chat FIRST** - Use chat.agentverse.ai before ASI:One
4. **Mailbox creation is MANDATORY** - `mailbox=True` + create via inspector
5. **Verify agent profile** - Check agentverse.ai/agents/details/{ADDRESS}/profile
6. **MeTTa depth matters** - Quality > quantity (13 conditions achieved)
7. **Chat Protocol critical** - Always include with `publish_manifest=True`
8. **Session ID patterns** - Handle both `http-*` and `session-*` prefixes
9. **Coordinator types** - Use `coordinator.py` (Chat Protocol) vs `coordinator_queue.py` (HTTP)
10. **VPS for production** - systemd services = reliable 24/7 uptime
11. **Agentverse testing > custom API** - Leverages official infrastructure
12. **Monitor logs** - Use `journalctl -u medichain-*.service -f` for debugging

**For complete development history and 30 detailed lessons:** See `docs/PROJECT-HISTORY.md`

---

## Resources

### Official Documentation
- **uAgents:** https://innovationlab.fetch.ai/resources/docs/agent-creation/uagent-creation
- **Chat Protocol:** https://innovationlab.fetch.ai/resources/docs/examples/chat-protocol/asi-compatible-uagents
- **MeTTa Basics:** https://metta-lang.dev/docs/learn/tutorials/python_use/metta_python_basics.html
- **Agentverse:** https://agentverse.ai/
- **ASI:One:** https://asi1.ai/

### Code Examples
- **Innovation Lab:** https://github.com/fetchai/innovation-lab-examples
- **MeTTa + Fetch.ai:** https://github.com/fetchai/innovation-lab-examples/tree/main/web3/singularity-net-metta

### Community
- **Discord:** https://discord.gg/fetchai
- **Hackathon Contact:** https://t.me/prithvipc
- **Submission:** https://earn.superteam.fun/listing/asi-agents-track

---

## Project Structure

```
asi-agents-track/
├── src/
│   ├── agents/              # 4 deployed agents
│   │   ├── coordinator.py   # Chat Protocol (port 8001)
│   │   ├── patient_intake.py
│   │   ├── symptom_analysis.py
│   │   └── treatment_recommendation.py
│   ├── protocols/messages.py
│   ├── metta/query_engine.py  # 21 methods
│   └── utils/
├── data/knowledge_base.metta   # 200+ facts
├── tests/
├── docs/
│   ├── PRD.md                  # SSOT
│   ├── EXECUTION-PLAN.md
│   ├── TIMELINE.md
│   ├── PROJECT-HISTORY.md      # Dev history
│   ├── TRACK-REQUIREMENTS.md
│   └── deployment/
├── .env (not committed)
├── requirements.txt
└── README.md
```

---

**May Allah grant barakah in this work and ease in completion. Bismillah!**
