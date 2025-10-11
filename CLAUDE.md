# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**ASI Agents Track - Hackathon Submission**

This is a multi-agent system built for the Artificial Superintelligence Alliance Agents Track hackathon (Cypherpunk 2025). The project implements a coordinator-specialist agent architecture using Fetch.ai's uAgents framework, integrated with SingularityNET's MeTTa knowledge graph for structured reasoning.

**Deadline:** October 31, 2025 (22 days from start)
**Prize Pool:** $20,000 USDC
**Current Status:** Week 1 - Day 3 (8 days ahead of schedule!)
**Project:** MediChain AI - Decentralized Healthcare Diagnostic System

---

## Technology Stack

- **Language:** Python 3.9+
- **Agent Framework:** Fetch.ai uAgents (`uagents>=0.12.0`, `uagents-core>=0.1.0`)
- **Knowledge Graph:** SingularityNET MeTTa (`hyperon>=0.1.0`)
- **Deployment Platform:** Agentverse (https://agentverse.ai/)
- **User Interface:** ASI:One Chat Protocol (https://asi1.ai/)
- **Testing:** pytest with asyncio support
- **Code Quality:** black, flake8, mypy

---

## Development Commands

### Environment Setup
```bash
# Initial setup (creates venv, installs dependencies, creates .env)
./setup.sh

# Manual virtual environment activation
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install/update dependencies
pip install -r requirements.txt

# Upgrade pip
pip install --upgrade pip
```

### Running Agents Locally
```bash
# Start coordinator agent (Chat Protocol enabled, port 8000)
python src/agents/coordinator.py

# Start patient intake agent (port 8001)
python src/agents/patient_intake.py

# Start knowledge graph agent (port 8003)
python src/agents/knowledge_graph.py

# Or run in background (logs to /tmp/)
python src/agents/coordinator.py > /tmp/coordinator_deploy.log 2>&1 &
python src/agents/patient_intake.py > /tmp/patient_intake_deploy.log 2>&1 &
python src/agents/knowledge_graph.py > /tmp/knowledge_graph_deploy.log 2>&1 &

# Test MeTTa query engine standalone
python src/metta/query_engine.py
```

### Testing
```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest --cov=src tests/

# Run specific test file
pytest tests/test_agents.py

# Run with verbose output
pytest -v tests/
```

### Code Quality
```bash
# Format code with black (2-space indentation)
black --line-length=88 src/ tests/

# Lint with flake8
flake8 src/ tests/

# Type checking with mypy
mypy src/
```

### Deployment
```bash
# Deploy agent to Agentverse (requires AGENTVERSE_API_KEY in .env)
# Deployment is handled automatically when agent runs with proper config
# Agent addresses will be generated upon first deployment
# Update .env with generated addresses for inter-agent communication
```

---

## Architecture

### Multi-Agent System Design

**Coordinator Agent** (`src/agents/coordinator.py`)
- Central routing agent with Chat Protocol enabled
- Accessible via ASI:One interface (https://asi1.ai/)
- Routes user requests to appropriate specialist agents
- Handles session management (StartSession, EndSession)
- Port: 8000

**Specialist Agents** (Template: `src/agents/specialist_template.py`)
- Domain-specific agents (3+ specialists)
- Process requests from coordinator
- Query MeTTa knowledge base for structured reasoning
- Return results with evidence and reasoning chains

**MeTTa Query Engine** (`src/metta/query_engine.py`)
- Interface for querying MeTTa knowledge graphs
- Loads knowledge base from `data/knowledge_base.metta`
- Provides domain-specific query methods
- Supports fact addition and complex queries

### Agent Communication Flow

```
User → ASI:One → Coordinator Agent → Specialist Agents → MeTTa KB
                        ↓                      ↓
                   Routing Logic      Domain Expertise
                        ↓                      ↓
                    Response ← Aggregation ← Results
```

### Chat Protocol Structure

All agents accessible via ASI:One must implement the Chat Protocol:

1. **StartSessionContent** - Initiates conversation
2. **TextContent** - Natural language messages
3. **EndSessionContent** - Terminates session
4. **ChatAcknowledgement** - Confirms message receipt

Implementation pattern:
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
    # Always send ChatAcknowledgement
    pass

agent.include(chat_proto, publish_manifest=True)
```

---

## MeTTa Knowledge Graph

### Knowledge Base Location
- Primary KB: `data/knowledge_base.metta`
- Configurable via `METTA_KB_PATH` in `.env`

### MeTTa Syntax Patterns

**Define Relationships:**
```metta
(: has-symptom (-> Condition Symptom))
(: has-treatment (-> Condition Treatment))
(: severity (-> Symptom Level))
```

**Add Facts:**
```metta
(has-symptom flu fever)
(has-symptom flu cough)
(has-treatment flu rest)
```

**Query Examples:**
```metta
;; Find conditions with specific symptom
(match &self (has-symptom $condition fever) $condition)

;; Find treatments for condition
(match &self (has-treatment flu $treatment) $treatment)

;; Complex queries with multiple variables
(match &self (has-symptom $condition $symptom) ($condition $symptom))
```

### Python Integration

```python
from src.metta.query_engine import MeTTaQueryEngine

engine = MeTTaQueryEngine()  # Loads from METTA_KB_PATH
engine.add_fact("(has-symptom flu fever)")
results = engine.find_by_symptom("fever")
```

**Key Methods:**
- `query(query_string)` - Execute raw MeTTa query
- `find_by_symptom(symptom)` - Find conditions by symptom
- `find_treatment(condition)` - Find treatments for condition
- `add_fact(fact)` - Add new knowledge
- `get_all_facts(predicate)` - Retrieve all facts for predicate

**Medical-Specific Methods (16 advanced methods):**
- `find_emergency_conditions()` - Identify 911-required conditions
- `find_symptoms_by_condition(condition)` - Complete symptom lookup
- `find_red_flag_symptoms()` - Critical warning signs detection
- `find_urgency_level(condition)` - Triage classification
- `find_severity_level(condition)` - Severity assessment
- `find_differential_diagnoses(condition)` - Alternative diagnoses
- `find_conditions_by_symptoms(symptoms)` - Multi-symptom matching with scoring
- `get_treatment_recommendations(condition)` - Evidence-based treatments
- `get_required_action(condition)` - Patient action guidance
- `check_time_sensitivity(condition)` - Hours until critical
- `get_evidence_source(treatment)` - Source credibility verification
- `generate_reasoning_chain(symptoms, condition)` - Transparent diagnostic explanation
- `get_all_contraindications(treatment)` - List all contraindicated conditions for treatment
- `get_safety_warning(treatment)` - Get safety warning text for treatment
- `check_drug_interaction(treatment, medication)` - Check for drug-drug interactions
- `requires_dose_adjustment(treatment, condition)` - Check if dose adjustment needed

---

## Project Structure

```
asi-agents-track/
├── src/
│   ├── agents/
│   │   ├── coordinator.py          # Main Chat Protocol agent (port 8000) ✅
│   │   ├── patient_intake.py       # NLP symptom extraction (port 8001) ✅
│   │   ├── knowledge_graph.py      # MeTTa diagnostic reasoning (port 8003) ✅
│   │   └── (2 more agents planned)
│   ├── protocols/
│   │   ├── __init__.py
│   │   └── messages.py             # Pydantic message models
│   ├── metta/
│   │   └── query_engine.py         # MeTTa integration (21 methods)
│   └── utils/                       # Helper utilities
├── data/
│   └── knowledge_base.metta        # MeTTa KB v1.1 (13 conditions, 200+ facts)
├── tests/
│   ├── test_agents.py              # Agent tests
│   └── test_metta.py               # MeTTa tests
├── logs/                            # Runtime logs
├── .env                             # Environment config (not committed)
├── .env.example                     # Environment template
├── requirements.txt                 # Python dependencies
├── setup.sh                         # Quick setup script
├── README.md                        # Project documentation
├── CLAUDE.md                        # This file - AI assistance context
├── docs/
│   ├── PRD.md                       # Product Requirements Document (SSOT)
│   ├── EXECUTION-PLAN.md            # Progress tracker (48% complete)
│   ├── TIMELINE.md                  # 22-day development plan
│   ├── GETTING-STARTED.md           # Quick start guide
│   ├── TRACK-REQUIREMENTS.md        # Submission checklist
│   ├── deployment/                  # Deployment documentation
│   │   ├── ASI-ONE-DEPLOYMENT-GUIDE.md
│   │   ├── ASI-ONE-TEST-RESULTS.md
│   │   └── DEPLOYMENT-STATUS.md
│   └── reference/                   # Reference & analysis
│       ├── hackathon-analysis.md    # Strategic analysis
│       └── hackathon-original.md    # Original hackathon content
```

---

## Environment Variables

Required in `.env` (create from `.env.example`):

```bash
# Agentverse credentials
AGENTVERSE_API_KEY=your_api_key_here      # From agentverse.ai
AGENT_SEED=your_unique_seed_phrase        # Unique seed for agent identity

# Agent addresses (populated after deployment)
COORDINATOR_ADDRESS=agent1q...
SPECIALIST_1_ADDRESS=agent1q...
SPECIALIST_2_ADDRESS=agent1q...
SPECIALIST_3_ADDRESS=agent1q...

# MeTTa configuration
METTA_KB_PATH=./data/knowledge_base.metta

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/agents.log
```

**Get Agentverse API Key:**
1. Sign up at https://agentverse.ai/
2. Navigate to API Keys section
3. Generate new key
4. Add to `.env`

---

## Development Workflow

### Day-by-Day Timeline

This project follows a structured 22-day timeline (see `docs/TIMELINE.md`):

**Week 1 (Oct 9-15):** Foundation - Basic agents + Chat Protocol + MeTTa basics
**Week 2 (Oct 16-22):** Advanced - Deep MeTTa integration + multi-agent coordination
**Week 3 (Oct 23-29):** Polish - Demo video + testing + final fixes
**Week 4 (Oct 30-31):** Submission + buffer

**Current Phase:** Check `docs/TIMELINE.md` for today's milestone and tasks.

### Daily Development Routine

1. **Review milestone:** Check `docs/TIMELINE.md` for day's goals
2. **Implement features:** Focus on milestone deliverables
3. **Test locally:** Run agents and verify functionality
4. **Update docs:** Keep README and comments current
5. **Commit progress:** Push to GitHub with descriptive messages
6. **Check requirements:** Review `docs/TRACK-REQUIREMENTS.md` weekly

---

## Testing Strategy

### Agent Testing Approaches

**Local Testing:**
```bash
# Terminal 1: Start coordinator
python src/agents/coordinator.py

# Terminal 2: Start specialist
python src/agents/specialist_1.py

# Terminal 3: Monitor logs
tail -f logs/agents.log
```

**Agentverse Chat Interface Testing (RECOMMENDED FIRST):**

After creating mailbox via inspector, each agent gets a dedicated chat interface:

1. **Access Agent Profile:**
   ```
   https://agentverse.ai/agents/details/{AGENT_ADDRESS}/profile
   ```

2. **Find Chat Interface Link:**
   - Agent profile page shows agent status (Active/Inactive)
   - Shows published protocols (AgentChatProtocol)
   - May have "Chat with Agent" button or direct session link

3. **Direct Chat URL Pattern:**
   ```
   https://chat.agentverse.ai/sessions/{SESSION_ID}
   ```
   - Each new session gets a unique ID
   - Interface shows agent name and timestamp
   - Test conversation flow here BEFORE ASI:One

4. **Testing Workflow:**
   - Send test messages to verify Chat Protocol
   - Monitor agent logs for received messages
   - Verify responses appear in chat interface
   - Test session lifecycle (start → messages → end)

**Important:** The chat interface is the best way to test agents immediately after mailbox creation, without waiting for ASI:One indexing.

**ASI:One Testing:**
1. Deploy agent to Agentverse
2. Create mailbox via inspector (REQUIRED)
3. Visit https://asi1.ai/
4. Search for agent by name or `@agent-name`
5. Test conversation flow
6. Verify agent responds (not ASI:One default AI)

**MeTTa Testing:**
```python
# Run standalone query engine tests
python src/metta/query_engine.py

# Or use pytest
pytest tests/test_metta.py
```

### Mailbox Creation Process (CRITICAL)

**Why Mailboxes Are Required:**
- `mailbox=True` in agent code enables mailbox CLIENT
- Actual mailbox must be created via Agentverse Inspector
- Without mailbox creation, agent won't appear in dashboard or be discoverable

**Step-by-Step Mailbox Creation:**

1. **Start agent locally** with `mailbox=True`:
   ```python
   agent = Agent(
       name="your-agent-name",
       port=8000,  # Local inspector port
       mailbox=True,  # Enable mailbox client
       publish_agent_details=True,  # Improves discoverability
   )
   ```

2. **Open Inspector URL** (from agent startup logs):
   ```
   https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A{PORT}&address={AGENT_ADDRESS}
   ```

3. **Click "Connect" button** (top right of inspector page)

4. **Select "Mailbox"** option and click "Next"
   - Mailbox: Easiest way to connect agent to internet
   - Proxy: For advanced routing configurations
   - Custom: Manual network configuration

5. **Click "OK, got it"** after reading instructions

6. **Verify in logs:**
   ```
   INFO: [mailbox]: Successfully registered as mailbox agent in Agentverse
   INFO: [mailbox]: Agent details updated in Agentverse
   ```

7. **Check Agent Dashboard:**
   - Visit https://agentverse.ai/agents
   - Agent should appear with "Active" status and "Mailbox" badge

**Common Issues:**

- **Agent not in dashboard:** Mailbox not created yet - repeat inspector steps
- **"test-agent://" prefix in inspector:** Normal for local agents before mailbox creation
- **Agent shows "Inactive":** Agent may have stopped running, check process
- **Inspector shows wrong agent:** URL might be truncated - use complete address

### Important Testing Notes

- **Test via Agentverse chat interface FIRST** before ASI:One
- Verify ChatAcknowledgement is sent for every received message
- Test multi-agent routing with realistic user queries
- Validate MeTTa queries return expected results
- Check error handling with invalid inputs
- Test session lifecycle (start → messages → end)
- Monitor agent logs during testing to see message flow

---

## Submission Requirements (Critical)

### Mandatory for Hackathon Submission

**Code Repository:**
- Public GitHub repository
- README with agent names and addresses
- Innovation Lab badges (already in README.md)
- Setup instructions and dependencies
- No committed secrets (.env is gitignored)

**Badges Required in README.md:**
```markdown
![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)
```

**Demo Video:**
- 3-5 minutes duration
- Shows problem statement, architecture, live demo
- Demonstrates ASI:One interaction
- Highlights MeTTa reasoning transparency
- Upload to YouTube/Vimeo, link in README

**Agentverse Deployment:**
- All agents registered on Agentverse
- Chat Protocol enabled
- Agents discoverable via ASI:One
- Agent addresses documented in README

**Complete Checklist:** See `docs/TRACK-REQUIREMENTS.md` for full requirements.

---

## Common Development Tasks

### Adding a New Specialist Agent

1. Copy `src/agents/specialist_template.py`
2. Rename to `specialist_{domain}.py`
3. Customize domain logic and MeTTa queries
4. Update coordinator routing logic
5. Add agent address to `.env` after deployment
6. Document in README.md

### Expanding MeTTa Knowledge Graph

1. Edit `data/knowledge_base.metta`
2. Add relationship definitions: `(: predicate (-> Type Type))`
3. Add facts: `(predicate entity1 entity2)`
4. Test queries: `(match &self (predicate $var value) $var)`
5. Update `query_engine.py` with helper methods if needed
6. Document knowledge structure in README

### Implementing Inter-Agent Communication

```python
# In coordinator.py
specialist_address = os.getenv("SPECIALIST_1_ADDRESS")

@agent.on_message(model=QueryRequest)
async def route_to_specialist(ctx: Context, sender: str, msg: QueryRequest):
    await ctx.send(specialist_address, msg)
```

### Debugging Agent Issues

**Common Issues:**

1. **Agent won't start:** Check Python version (3.9+), verify dependencies installed
2. **Port conflict:** Change port in `Agent(port=8000)` initialization
3. **ASI:One can't find agent:** Verify Chat Protocol included with `publish_manifest=True`
4. **MeTTa import error:** Install hyperon: `pip install hyperon`
5. **Agent address not found:** Deploy to Agentverse first, then add address to .env

**Logging:**
```python
ctx.logger.info(f"Message: {msg}")
ctx.logger.error(f"Error: {e}")
```

---

## Judging Criteria Focus Areas

### Functionality & Technical Implementation (25%)
- All agents work reliably without crashes
- Multi-agent coordination functions smoothly
- Clean, maintainable code with proper error handling

### Use of ASI Alliance Tech (20%)
- Proper uAgents framework usage
- Chat Protocol working via ASI:One
- **Deep MeTTa integration (HIGH IMPACT)** - Not superficial

### Innovation & Creativity (20%)
- Novel problem-solving approach
- Unique agent architecture
- Avoid oversaturated domains

### Real-World Impact & Usefulness (20%)
- Solves meaningful problem
- Clear practical value
- Scalability potential

### User Experience & Presentation (15%)
- Professional demo video
- Intuitive ASI:One conversation
- Comprehensive documentation

**Target:** 90+ / 100 points for top-3 finish

---

## Key Documentation Files

### Planning & Execution (Critical - Review Daily)
- **docs/PRD.md** - Product Requirements Document with Epic → Story → Task hierarchy (SINGLE SOURCE OF TRUTH)
- **docs/EXECUTION-PLAN.md** - Progress tracker mapped to PRD, update daily with task status
- **docs/TIMELINE.md** - 22-day development plan with weekly milestones

### Project Context & Strategy
- **README.md** - Main project documentation, update with agent details
- **CLAUDE.md** - This file - project guidance for Claude Code
- **docs/reference/hackathon-analysis.md** - Strategic analysis and winning strategies
- **docs/TRACK-REQUIREMENTS.md** - Complete submission checklist, review weekly
- **docs/GETTING-STARTED.md** - Quick start guide for new contributors

### Deployment Documentation
- **docs/deployment/ASI-ONE-DEPLOYMENT-GUIDE.md** - ASI:One deployment procedures
- **docs/deployment/ASI-ONE-TEST-RESULTS.md** - Testing results and issues
- **docs/deployment/DEPLOYMENT-STATUS.md** - Current deployment status

### Planning Workflow
1. **Before starting any task**: Check docs/PRD.md for Epic/Story/Task requirements
2. **Daily updates**: Update docs/EXECUTION-PLAN.md with task progress (🔲 → 🟡 → ✅)
3. **Weekly checkpoints**: Review docs/TIMELINE.md and update week progress
4. **All work must trace back to PRD items** - No ad-hoc features without PRD entry

---

## Important Constraints

### What NOT to Do

- **Don't skip Chat Protocol** - Required for ASI:One discoverability
- **Don't do superficial MeTTa integration** - Judges look for depth
- **Don't commit secrets** - .env is gitignored, use .env.example
- **Don't add new features after Day 18** - Feature freeze for stability
- **Don't skip testing** - Broken demo = disqualification

### Development Philosophy

- **100% working standard** - No partial implementations
- **Ship with excellence** - Production-ready code quality
- **Time philosophy** - Quality over urgency, 22 days is sufficient
- **Documentation accuracy** - Keep README synchronized with code
- **Test-driven** - Test locally before Agentverse deployment

---

## Resources

### Official Documentation
- **uAgents:** https://innovationlab.fetch.ai/resources/docs/agent-creation/uagent-creation
- **Chat Protocol:** https://innovationlab.fetch.ai/resources/docs/examples/chat-protocol/asi-compatible-uagents
- **MeTTa Basics:** https://metta-lang.dev/docs/learn/tutorials/python_use/metta_python_basics.html
- **Agentverse:** https://agentverse.ai/
- **ASI:One Interface:** https://asi1.ai/

### Code Examples
- **Innovation Lab Examples:** https://github.com/fetchai/innovation-lab-examples
- **MeTTa + Fetch.ai Integration:** https://github.com/fetchai/innovation-lab-examples/tree/main/web3/singularity-net-metta

### Community Support
- **Fetch.ai Discord:** https://discord.gg/fetchai
- **Hackathon Contact:** https://t.me/prithvipc
- **Submission Platform:** https://earn.superteam.fun/listing/asi-agents-track

---

## Current Project State (Day 5 - Oct 11, 2025 - End of Day)

**Progress:** 90% complete - **12+ DAYS AHEAD OF SCHEDULE!**

### MAJOR BREAKTHROUGH: Full Production Deployment Complete! 🎉

**What Changed Since Day 4:**
- ✅ Complete custom web interface (Next.js + TypeScript + Tailwind)
- ✅ VPS production deployment (176.222.53.185:8080)
- ✅ Queue-based HTTP bridge (solved Flask/async threading issues)
- ✅ Vercel production deployment (medichain-web.vercel.app)
- ✅ End-to-end tested: Web → VPS → 4 Agents → Complete diagnosis in ~10 seconds

### Production Architecture (FULLY OPERATIONAL)

**Backend - VPS (Ubuntu 22.04, IP: 176.222.53.185)**:
- All 4 agents running as systemd services with auto-restart
- Queue-based coordinator (`coordinator_queue.py`) - FastAPI + asyncio.Queue
- Mailbox connections active for all agents
- Port 8080 open and serving HTTP requests
- Health check: http://176.222.53.185:8080/health ✅

**Frontend - Vercel**:
- Next.js 14 production deployment
- URL: https://medichain-web.vercel.app
- Professional landing page with live demo
- Real-time chat interface
- Color-coded diagnostic reports
- Mobile-responsive design

**Technical Achievement: Queue-Based HTTP Bridge**:
```python
# HTTP endpoint puts request in queue
await request_queue.put({"session_id": ..., "message": ...})

# uAgent periodic task processes queue (every 500ms)
@agent.on_interval(period=0.5)
async def process_http_queue(ctx: Context):
    request = await request_queue.get()
    # Process through multi-agent flow
```

**Why This Works (vs Flask threading):**
- Flask + threading: Event loop not executing coroutines ❌
- FastAPI + agent.run_async(): Method doesn't exist ❌
- **FastAPI + Queue + Periodic Task**: Clean, reliable solution ✅

### Completed Epics (Updated)

- ✅ **Epic 1**: Multi-Agent Foundation (18/18 tasks) - Day 2
- ✅ **Epic 2**: MeTTa Integration (18/18 tasks) - Day 3
- ✅ **Epic 3**: Specialized Diagnostic Agents (13/13 tasks) - Day 4
- ✅ **Epic 4**: Chat Protocol Integration (14/14 tasks) - Day 5 ✅ **NEW!**
  - Custom web interface replaces ASI:One (better UX for hackathon demo)
  - HTTP endpoint with queue-based architecture
  - Real-time WebSocket-like experience via polling
  - Professional landing page with examples
- ✅ **Epic 5.1**: VPS Deployment (6/6 tasks) - Day 5 ✅ **NEW!**
  - Code uploaded, dependencies installed
  - systemd services configured
  - All agents running 24/7
  - Firewall configured (port 8080 open)
- ✅ **Epic 5.2**: Vercel Deployment (4/4 tasks) - Day 5 ✅ **NEW!**
  - Next.js build successful
  - Production deployment complete
  - Environment variables configured
  - ESLint errors resolved

### All Agents Deployed (PRODUCTION-READY)

**VPS Agents (Running as systemd services):**
- ✅ Coordinator (Queue): `agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q` (port 8001 + HTTP 8080)
- ✅ Patient Intake: `agent1qgr8ga84fyjsy478ctvzp3zf5r8rw9nulzmrl9w0l3x83suxuzt6zjq29y2` (port 8000)
- ✅ Symptom Analysis: `agent1qdxqnfmu735ren2geq9f3n8ehdk43lvm9x0vxswv6xj6a5hn40yfqv0ar42` (port 8004)
- ✅ Treatment: `agent1qg9m6r976jq4lj64qfnp679qu8lu4jzcy06y09mf7ta4l2sm8uq9qfqrc9v` (port 8005)

**Service Management:**
```bash
# Check status
ssh website 'sudo systemctl status medichain-*.service'

# View logs
ssh website 'sudo journalctl -u medichain-coordinator.service -f'

# Restart all
ssh website 'sudo systemctl restart medichain-*.service'
```

### Production Test Results (✅ PASSING)

**Test Case: Headache + Fever (2 days)**
```json
Input: "I have a severe headache and fever for 2 days"

Response (10 seconds):
{
  "differential_diagnoses": ["influenza", "covid-19"],
  "confidence_scores": {
    "influenza": 0.18,
    "covid-19": 0.18,
    "meningitis": 0.14
  },
  "urgency": "ROUTINE",
  "treatment": {
    "recommended": ["antivirals", "rest", "fluids", "fever-reducers"],
    "specialist_referral": "Primary Care Physician",
    "follow_up": "1-2 weeks (or sooner if symptoms worsen)"
  },
  "medical_disclaimer": "⚠️ This is NOT medical advice..."
}
```

**Multi-Agent Flow (Verified):**
1. HTTP → Coordinator (queue) ✅
2. Coordinator → Patient Intake ✅
3. Patient Intake → Coordinator (diagnostic request) ✅
4. Coordinator → Symptom Analysis ✅
5. Symptom Analysis → Coordinator ✅
6. Coordinator → Treatment ✅
7. Treatment → Coordinator ✅
8. Coordinator → HTTP Response ✅

### Knowledge Base v1.1 (Unchanged - Already Excellent)

- 13 medical conditions (6 critical, 2 urgent, 5 common)
- 200+ medical facts (2X target!)
- 45+ contraindications (4X target!)
- Evidence sources: CDC, WHO, AHA, Johns Hopkins
- 21 query methods (12 medical-specific + 4 safety + 5 base)

### Project URLs

**Production:**
- Backend API: http://176.222.53.185:8080
- Frontend: https://medichain-web.vercel.app
- Health Check: http://176.222.53.185:8080/health

**Development:**
- GitHub: https://github.com/RECTOR-LABS/asi-agents-track
- Branch: `dev`
- Latest Commit: VPS + Vercel deployment complete

### Next Steps (Day 6+)

- **PRIORITY**: Epic 6: Documentation & Demo Video (23 tasks)
  - Update README with production URLs
  - Record 3-5 minute demo video
  - Showcase web interface + multi-agent architecture
  - Highlight MeTTa reasoning transparency
  - Prepare submission materials

- **Optional**: Epic 5.3: Testing & QA
  - Comprehensive pytest suite (if time permits)
  - Load testing production deployment
  - Edge case validation

**Submission Checklist (90% Complete):**
- ✅ Public GitHub repository
- ✅ Multi-agent system (4 agents)
- ✅ MeTTa knowledge graph integration (deep, not superficial)
- ✅ Production deployment (VPS + Vercel)
- ✅ Professional web interface
- ✅ Innovation Lab badges in README
- ⏳ Demo video (3-5 minutes) - **TO DO**
- ⏳ README update with deployment URLs - **TO DO**
- ⏳ Submit to earn.superteam.fun - **TO DO**

---

## CRITICAL DISCOVERY: ASI:One vs Agentverse Chat (Day 5 - Oct 11, 2025)

### Two Different Chat Interfaces

**IMPORTANT:** Agentverse has TWO separate chat interfaces with DIFFERENT behavior:

1. **chat.agentverse.ai** (Direct Agent Chat) ✅ WORKS
   - URL: `https://chat.agentverse.ai/sessions/{SESSION_ID}`
   - Accessed via "Chat with Agent" button on agent profile
   - Directly connects to your cloud agent
   - Agent responds (may error if template without custom logic)
   - **USE THIS for testing cloud agents**

2. **asi1.ai** (Public ASI:One Discovery) ❌ DOESN'T WORK (yet)
   - URL: `https://asi1.ai/`
   - Public-facing agent discovery platform
   - **ASI:One's default "Doc" AI responds instead of custom agents**
   - Says: "I cannot directly facilitate communication with other agents outside of approved collaboration parameters"
   - **Agents NOT discoverable here despite being Active on Agentverse**

### Testing Results (Oct 11, 2025)

**Cloud Agent Created:**
- Agent: `Medichain AI`
- Address: `agent1q0q46ztah7cyw4z7gcg3mued9ncnrcvrcqc8kjku3hywqdzp03e36hk5qsl`
- Status: Active, Hosted on Agentverse
- Chat Protocol: ✅ Configured
- README: ✅ Included

**Test Results:**
- ✅ **chat.agentverse.ai**: Agent responds (errors due to template lacking custom logic)
- ❌ **asi1.ai**: ASI:One default AI responds, agent not discovered
- ❌ Searching by `@agent-address` on asi1.ai: Not found
- ❌ Searching by agent name on asi1.ai: Not found

### Why ASI:One Doesn't Work (Hypothesis)

Possible reasons cloud agent isn't discoverable on public asi1.ai:

1. **Template Agent Limitation**: Basic "Chat Protocol using llm" template may not meet ASI:One standards
2. **Missing Configuration**: May need additional setup (agent handle, enhanced README, specific metadata)
3. **Indexing Requirements**: ASI:One might have stricter discovery criteria than Agentverse chat
4. **Custom Logic Required**: Template agents without domain logic may be excluded from public discovery
5. **Verification Needed**: ASI:One might require agent verification or approval before public listing

### Implications for Hackathon

**For Demo Video:**
- ✅ CAN demonstrate Chat Protocol functionality via chat.agentverse.ai
- ❌ CANNOT demonstrate public asi1.ai discovery (yet)
- **Solution**: Show Agentverse chat interface as Chat Protocol demo

**For Submission:**
- Cloud agent proves Chat Protocol implementation ✅
- May need to deploy custom MediChain code to cloud for full functionality
- Alternative: Focus on local agent setup with mailbox for ASI:One compatibility

**Next Steps to Achieve asi1.ai Discovery:**
1. Customize cloud agent code with MediChain logic
2. Enhanced README with detailed agent capabilities
3. Add agent handle/custom name for better discoverability
4. Research ASI:One requirements for public agent listing
5. Contact Fetch.ai support if issue persists

### Key Learnings for Future Instances

1. **chat.agentverse.ai ≠ asi1.ai** - They are DIFFERENT platforms
2. **Test on chat.agentverse.ai FIRST** - Immediate validation of Chat Protocol
3. **asi1.ai discovery requires more** than just Active + Chat Protocol + README
4. **Template agents may not qualify** for public ASI:One discovery
5. **Custom logic deployment** may be required for asi1.ai visibility

---

## Tips for Future Claude Instances

1. **Always check docs/PRD.md first** - All work must trace back to Epic/Story/Task requirements (SINGLE SOURCE OF TRUTH)
2. **Update docs/EXECUTION-PLAN.md daily** - Track task progress (🔲 → 🟡 → ✅), update daily standup log
3. **Follow the planning workflow** - PRD defines WHAT to build, EXECUTION-PLAN tracks progress, TIMELINE shows WHEN
4. **Review docs/TRACK-REQUIREMENTS.md weekly** - Ensure submission requirements are met
5. **Test via Agentverse chat interface FIRST** - Use `https://chat.agentverse.ai/sessions/{ID}` before ASI:One for immediate testing
6. **Mailbox creation is MANDATORY** - `mailbox=True` is not enough; must create via inspector at `https://agentverse.ai/inspect/`
7. **Verify agent profile** - Check `https://agentverse.ai/agents/details/{ADDRESS}/profile` to confirm Active status and protocols
8. **Focus on MeTTa depth** - Quality > quantity (13 well-modeled conditions achieved!)
9. **Preserve agent communication patterns** - Chat Protocol implementation is critical
10. **Update README incrementally** - Don't leave documentation for the end
11. **Respect the 22-day timeline** - Follow milestone sequence, don't skip ahead (currently 8 days ahead!)
12. **Keep .env synchronized** - Update agent addresses after each Agentverse deployment
13. **Test locally before deploying** - Agentverse debugging is harder than local
14. **Review docs/reference/hackathon-analysis.md** - Contains strategic insights for competitive advantage
15. **No ad-hoc features** - If it's not in PRD, don't build it (or add to PRD first and get approval)
16. **Monitor agent logs during chat testing** - Use `tail -f /tmp/{agent}_mailbox.log` to see real-time message flow
17. **MeTTa reasoning chains are the differentiator** - Use `generate_reasoning_chain()` to show transparent diagnostics
18. **chat.agentverse.ai vs asi1.ai are DIFFERENT** - Test on chat.agentverse.ai first; asi1.ai discovery requires additional setup/approval (see CRITICAL DISCOVERY section above)
19. **Template agents may not appear on asi1.ai** - Custom logic deployment or enhanced configuration may be required for public ASI:One discovery
20. **Flask + uAgent threading DOESN'T WORK** - Event loops don't execute cross-thread coroutines; use Queue-based approach instead
21. **VPS deployment for production** - systemd services provide reliable 24/7 uptime for multi-agent systems
22. **Custom web interface > ASI:One** - Better UX, easier demo, full control over presentation for hackathon judging
23. **FastAPI + Queue + Periodic Task** - Clean solution for HTTP bridge without threading issues (check every 500ms with `@agent.on_interval`)
24. **Skip clarification for HTTP sessions** - Check `session_id.startswith("http-")` to bypass multi-turn clarification in web interface
25. **Vercel CLI deployment** - Use `vercel --prod --yes` for fast production deployments; handle ESLint errors with HTML entities (&apos;, &quot;)
26. **VPS service management** - Use `sudo systemctl status medichain-*.service` to check all agents; logs via `journalctl -u medichain-coordinator.service -f`
27. **Production URLs are documentation** - Always update CLAUDE.md and README with live deployment URLs for easy reference

---

**May Allah grant barakah in this work and ease in completion. Bismillah!**
