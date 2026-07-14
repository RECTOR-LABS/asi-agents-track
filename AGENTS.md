<!-- Satellite context file — extends the global hub (~/.claude/CLAUDE.md | ~/.pi/agent/AGENTS.md). Host-neutral; project-specific only. Do not duplicate hub standards here. -->

# ASI Agents Track (MediChain AI)

> Multi-agent healthcare diagnostic system built for the Artificial Superintelligence Alliance Agents Track hackathon (Cypherpunk 2025). Coordinator-specialist agent architecture using Fetch.ai's uAgents framework + SingularityNET's MeTTa knowledge graph.

**Project:** MediChain AI — Decentralized Healthcare Diagnostic System
**Deadline:** October 31, 2025 · **Prize pool:** $20,000 USDC · **Status:** 90% complete, 13+ days ahead of schedule.

## Tech Stack

- **Language:** Python 3.9+
- **Agent Framework:** Fetch.ai uAgents (`uagents>=0.12.0`, `uagents-core>=0.1.0`)
- **Knowledge Graph:** SingularityNET MeTTa (`hyperon>=0.1.0`)
- **Deployment:** Agentverse (https://agentverse.ai/) + VPS (Ubuntu 22.04, systemd services)
- **Frontend:** Next.js 14 (Vercel) — static landing page
- **Testing:** pytest, Agentverse chat interface

## Common Commands

```bash
./setup.sh                                          # initial setup
source venv/bin/activate
pip install -r requirements.txt

# Run agents locally
python src/agents/coordinator.py             # port 8001 (Chat Protocol enabled)
python src/agents/patient_intake.py           # port 8000
python src/agents/symptom_analysis.py         # port 8004
python src/agents/treatment_recommendation.py # port 8005
python src/metta/query_engine.py              # test MeTTa query engine

# Testing
pytest tests/
pytest --cov=src tests/
black --line-length=88 src/ tests/
flake8 src/ tests/
mypy src/
python test_validation.py                     # 14-scenario input validation
pytest tests/ -k validation

# VPS service management
ssh website 'sudo systemctl status medichain-*.service'
ssh website 'sudo journalctl -u medichain-coordinator.service -f'
ssh website 'sudo systemctl restart medichain-*.service'
```

## Production Architecture

```
User → Vercel Landing Page → "Test on Agentverse" Button → Agentverse Chat Interface → VPS Multi-Agent System (4 agents via mailbox protocol)
```

Vercel Free tier has 10s timeout (multi-agent flow ~15s), so functionality runs on Agentverse + VPS, marketing on Vercel.

### Production URLs
- **Pitch:** https://medichain-web.rectorspace.com
- **Testing:** https://agentverse.ai/agents/details/agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q

### Deployed Agents (systemd, 24/7)
- **Coordinator:** `agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q` (8001)
- **Patient Intake:** `agent1qgr8ga84fyjsy478ctvzp3zf5r8rw9nulzmrl9w0l3x83suxuzt6zjq29y2` (8000)
- **Symptom Analysis:** `agent1qdxqnfmu735ren2geq9f3n8ehdk43lvm9x0vxswv6xj6a5hn40yfqv0ar42` (8004)
- **Treatment:** `agent1qg9m6r976jq4lj64qfnp679qu8lu4jzcy06y09mf7ta4l2sm8uq9qfqrc9v` (8005)

## Input Validation System (14 scenarios)

`src/utils/input_validation.py` (430+ lines) — safety-first edge case handler. Critical: emergency detection ("chest pain", "can't breathe" → 911), mental health crisis (→ 988/Crisis Text Line/911), prescription requests (AI cannot prescribe). Important: proxy symptoms (pediatric caution), session history (no memory), self-diagnosis. UX: greetings, gibberish, pet symptoms, off-topic, meta questions, vague input, insufficient info, valid medical → diagnostic flow. Each validation includes confidence (0.0-1.0); priority-based; zero false negatives on safety-critical. Tests: `test_validation.py` (12/12). Coordinator validates before routing to patient intake.

## MeTTa Knowledge Graph (v2.0 — Epic 7 COMPLETE)

`data/knowledge_base.metta` (`METTA_KB_PATH` in `.env`): **25 conditions** (9 critical, 7 urgent, 9 common), **2,074 lines** (+232%), **83 contraindications**, **180 risk factors with multipliers**, **60 treatment protocol steps** (8 critical conditions), **56 symptom attributes**, **41 diagnostic criteria** (8 clinical systems), **37+ lab test types**, **12 imaging types**, **96 seasonal + 10 geographic prevalence**, **21 clarifying questions**. Evidence sources: CDC, WHO, AHA, Johns Hopkins, Mayo Clinic.

```python
from src.metta.query_engine import MeTTaQueryEngine
engine = MeTTaQueryEngine()
results = engine.find_by_symptom("fever")
treatments = engine.find_treatment("influenza")
emergencies = engine.find_emergency_conditions()
red_flags = engine.find_red_flag_symptoms()
urgency = engine.find_urgency_level("meningitis")
reasoning = engine.generate_reasoning_chain(symptoms, condition)
contraindications = engine.get_all_contraindications("aspirin")
lab_tests = engine.find_lab_tests("diabetic-ketoacidosis")
risk_score = engine.calculate_risk_score("heart-attack", ["age-over-65", "diabetes-mellitus"])
protocol = engine.get_treatment_protocol("heart-attack")
```

**34 methods total** — see `src/metta/query_engine.py`.

## Chat Protocol

```python
from uagents_core.contrib.protocols.chat import (ChatMessage, ChatAcknowledgement, StartSessionContent, TextContent, EndSessionContent, chat_protocol_spec)
chat_proto = Protocol(spec=chat_protocol_spec)
@chat_proto.on_message(ChatMessage)
async def handle_message(ctx, sender, msg):
    await ctx.send(sender, ChatAcknowledgement())  # ALWAYS acknowledge
    # process msg.content items
agent.include(chat_proto, publish_manifest=True)  # REQUIRED for ASI:One discoverability
```

**Mailbox creation (mandatory):** start agent with `mailbox=True` → open inspector URL from logs → Connect → select Mailbox → verify "Successfully registered as mailbox agent in Agentverse" + dashboard "Active".

## Project Structure

```
src/agents/{coordinator,patient_intake,symptom_analysis,treatment_recommendation}.py
src/protocols/messages.py
src/metta/query_engine.py          # 34 methods
src/utils/input_validation.py      # 14-scenario handler
data/knowledge_base.metta          # 2,074 lines
resources/medichain-avatar*.svg
tests/test_epic7_phase{1,2,3}.py + test_attribute_matching + test_treatment_protocols + test_risk_scenarios
docs/{PRD,EXECUTION-PLAN,TIMELINE,PROJECT-HISTORY,TRACK-REQUIREMENTS}.md · docs/deployment/
```

## Key Docs

`docs/PRD.md` (SSOT — Epic/Story/Task) · `docs/EXECUTION-PLAN.md` (daily tracker 🔲→🟡→✅) · `docs/TIMELINE.md` · `docs/PROJECT-HISTORY.md` (dev history + 30 lessons) · `docs/TRACK-REQUIREMENTS.md` (submission checklist) · `docs/deployment/`.

## Judging Criteria

Functionality 25% · ASI Tech 20% (deep MeTTa, not superficial) · Innovation 20% · Impact 20% · Presentation 15%. Target: 90+/100 for top-3.

## Submission Requirements

Public GitHub repo with Innovation Lab badges · multi-agent system on Agentverse · deep MeTTa integration (2,074 lines) · Chat Protocol working · demo video (3-5 min, [YouTube](https://www.youtube.com/watch?v=Fjz9C6GShIQ)) · README with agent addresses + URLs.

**Innovation Lab badges:** `![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)` · `![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)`

## Constraints

**Don't:** skip Chat Protocol (required for discoverability) · do superficial MeTTa (judges look for depth) · commit secrets (.env gitignored) · skip testing (broken demo = DQ; 70/70 tests passing).
**Do:** 100% working standard · production-ready · TDD · PRD is SSOT · update EXECUTION-PLAN daily.