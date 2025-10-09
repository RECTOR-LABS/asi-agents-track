# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**ASI Agents Track - Hackathon Submission**

This is a multi-agent system built for the Artificial Superintelligence Alliance Agents Track hackathon (Cypherpunk 2025). The project implements a coordinator-specialist agent architecture using Fetch.ai's uAgents framework, integrated with SingularityNET's MeTTa knowledge graph for structured reasoning.

**Deadline:** October 31, 2025 (22 days from start)
**Prize Pool:** $20,000 USDC
**Current Status:** Foundation phase (Week 1)

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

# Start specialist agents (run in separate terminals)
python src/agents/specialist_1.py
python src/agents/specialist_2.py
python src/agents/specialist_3.py

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
- `find_by_symptom(symptom)` - Domain-specific helper
- `find_treatment(condition)` - Domain-specific helper
- `add_fact(fact)` - Add new knowledge
- `get_all_facts(predicate)` - Retrieve all facts for predicate

---

## Project Structure

```
asi-agents-track/
├── src/
│   ├── agents/
│   │   ├── coordinator.py          # Main Chat Protocol agent
│   │   ├── specialist_template.py  # Template for specialists
│   │   └── specialist_{1,2,3}.py   # Domain specialists
│   ├── protocols/                   # Custom protocols (if needed)
│   ├── metta/
│   │   └── query_engine.py         # MeTTa integration
│   └── utils/                       # Helper utilities
├── data/
│   └── knowledge_base.metta        # MeTTa knowledge graph
├── tests/
│   ├── test_agents.py              # Agent tests
│   └── test_metta.py               # MeTTa tests
├── logs/                            # Runtime logs
├── .env                             # Environment config (not committed)
├── .env.example                     # Environment template
├── requirements.txt                 # Python dependencies
├── setup.sh                         # Quick setup script
├── README.md                        # Project documentation
├── TRACK-REQUIREMENTS.md            # Submission checklist
├── TIMELINE.md                      # 22-day development plan
└── GETTING-STARTED.md               # Quick start guide
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

This project follows a structured 22-day timeline (see `TIMELINE.md`):

**Week 1 (Oct 9-15):** Foundation - Basic agents + Chat Protocol + MeTTa basics
**Week 2 (Oct 16-22):** Advanced - Deep MeTTa integration + multi-agent coordination
**Week 3 (Oct 23-29):** Polish - Demo video + testing + final fixes
**Week 4 (Oct 30-31):** Submission + buffer

**Current Phase:** Check `TIMELINE.md` for today's milestone and tasks.

### Daily Development Routine

1. **Review milestone:** Check `TIMELINE.md` for day's goals
2. **Implement features:** Focus on milestone deliverables
3. **Test locally:** Run agents and verify functionality
4. **Update docs:** Keep README and comments current
5. **Commit progress:** Push to GitHub with descriptive messages
6. **Check requirements:** Review `TRACK-REQUIREMENTS.md` weekly

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

**ASI:One Testing:**
1. Deploy agent to Agentverse
2. Visit https://asi1.ai/
3. Search for agent by name or address
4. Test conversation flow
5. Verify StartSession, TextContent, EndSession handling

**MeTTa Testing:**
```python
# Run standalone query engine tests
python src/metta/query_engine.py

# Or use pytest
pytest tests/test_metta.py
```

### Important Testing Notes

- Always test Chat Protocol via ASI:One before considering feature complete
- Verify ChatAcknowledgement is sent for every received message
- Test multi-agent routing with realistic user queries
- Validate MeTTa queries return expected results
- Check error handling with invalid inputs
- Test session lifecycle (start → messages → end)

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

**Complete Checklist:** See `TRACK-REQUIREMENTS.md` for full requirements.

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

- **README.md** - Main project documentation, update with agent details
- **TRACK-REQUIREMENTS.md** - Complete submission checklist, review weekly
- **TIMELINE.md** - 22-day development plan, track daily progress
- **GETTING-STARTED.md** - Quick start guide for new contributors
- **hackathon-analysis.md** - Strategic analysis and winning strategies

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

## Tips for Future Claude Instances

1. **Always check TIMELINE.md first** - Understand current development phase and daily goals
2. **Review TRACK-REQUIREMENTS.md weekly** - Ensure submission requirements are met
3. **Test via ASI:One frequently** - Don't wait until the end to test Chat Protocol
4. **Focus on MeTTa depth** - Quality > quantity (10 well-modeled conditions > 50 superficial)
5. **Preserve agent communication patterns** - Chat Protocol implementation is critical
6. **Update README incrementally** - Don't leave documentation for the end
7. **Respect the 22-day timeline** - Follow milestone sequence, don't skip ahead
8. **Keep .env synchronized** - Update agent addresses after each Agentverse deployment
9. **Test locally before deploying** - Agentverse debugging is harder than local
10. **Review hackathon-analysis.md** - Contains strategic insights for competitive advantage

---

**May Allah grant barakah in this work and ease in completion. Bismillah!**
