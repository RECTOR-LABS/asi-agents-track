# ASI Agents Track - Hackathon Project

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

**Hackathon:** Cypherpunk - ASI Agents Track
**Sponsor:** Artificial Superintelligence Alliance
**Deadline:** October 31, 2025
**Prize Pool:** $20,000 USDC

---

## 🎯 Project Overview

**MediChain AI** is a decentralized healthcare diagnostic system that combines Fetch.ai's autonomous agents with SingularityNET's MeTTa knowledge graphs to provide accurate, explainable medical assessments accessible through ASI:One chat interface.

**Problem Statement:** Medical misdiagnosis affects 12 million Americans annually, leading to $40 billion in healthcare costs and thousands of preventable deaths. Current solutions lack transparency, scalability, and 24/7 accessibility.

**Solution:** Multi-agent diagnostic system with transparent MeTTa-powered reasoning that analyzes symptoms, identifies conditions with evidence-based recommendations, and provides explainable diagnostic chains showing "why" behind every diagnosis.

**Impact:** Democratizes access to preliminary medical diagnosis through AI agents, providing 24/7 assessment with transparent reasoning, evidence-linked treatments, and appropriate urgency classification to guide patients to timely care.

---

## 🏗️ Architecture

### Agent System

**Current Deployment (3/5 Agents - 60%):**
- **Coordinator Agent** - Central routing with Chat Protocol (`agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q`) ✅
- **Patient Intake Agent** - NLP symptom extraction (`agent1qgr8ga84fyjsy478ctvzp3zf5r8rw9nulzmrl9w0l3x83suxuzt6zjq29y2`) ✅
- **Knowledge Graph Agent** - MeTTa diagnostic reasoning (`agent1qdjy30exkpc0zxu6p8urwnllg9fygj27h3nzksq9twmqcsyundvckavn6v6`) ✅
- **Symptom Analysis Agent** - Urgency assessment (planned) 📋
- **Treatment Recommendation Agent** - Evidence-based treatments (planned) 📋

### Technology Stack

- **Agent Framework:** Fetch.ai uAgents
- **Knowledge Graph:** SingularityNET MeTTa
- **Deployment:** Agentverse
- **Interface:** ASI:One Chat Protocol
- **Language:** Python 3.9+

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager
- Agentverse account ([sign up here](https://agentverse.ai/))

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd asi-agents-track
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Agentverse API keys
```

### Running Locally

1. Start the coordinator agent:
```bash
python src/agents/coordinator.py
```

2. In separate terminals, start specialist agents:
```bash
python src/agents/patient_intake.py
python src/agents/knowledge_graph.py
# Additional agents coming soon
```

3. Test via ASI:One interface: [https://asi1.ai/](https://asi1.ai/)

---

## 📋 Agent Details

### Coordinator Agent
- **Name:** MediChain Coordinator
- **Address:** `agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q`
- **Role:** Routes user requests to appropriate specialist agents
- **Chat Protocol:** ✅ Enabled (ASI:One accessible)
- **Status:** ✅ Deployed

### Patient Intake Agent
- **Name:** MediChain Patient Intake
- **Address:** `agent1qgr8ga84fyjsy478ctvzp3zf5r8rw9nulzmrl9w0l3x83suxuzt6zjq29y2`
- **Role:** Natural language symptom extraction and validation
- **Features:** Regex + keyword extraction, symptom normalization, clarifying questions
- **Status:** ✅ Deployed

### Knowledge Graph Agent
- **Name:** MediChain Knowledge Graph
- **Address:** `agent1qdjy30exkpc0zxu6p8urwnllg9fygj27h3nzksq9twmqcsyundvckavn6v6`
- **Role:** MeTTa-powered diagnostic reasoning with transparent explanation chains
- **Features:** Multi-hop reasoning, differential diagnosis, uncertainty handling, safety validation
- **MeTTa Integration:** ✅ Deep integration (13 conditions, 200+ facts, 21 query methods)
- **Status:** ✅ Deployed (Day 3)

### Symptom Analysis Agent
- **Name:** MediChain Symptom Analyzer
- **Address:** (planned)
- **Role:** Urgency assessment (emergency/urgent/routine) and red flag detection
- **Status:** 📋 Planned (Epic 3)

### Treatment Recommendation Agent
- **Name:** MediChain Treatment Advisor
- **Address:** (planned)
- **Role:** Evidence-based treatment recommendations with source linking
- **Status:** 📋 Planned (Epic 3)

---

## 🧠 MeTTa Knowledge Graph

**Medical Diagnostic Knowledge Base (v1.1):**

- **13 Medical Conditions:** Critical (6), Urgent (1), Common (3), Differential (3)
  - Meningitis, Stroke, Heart Attack, Appendicitis, Pulmonary Embolism, Sepsis
  - Pneumonia, Migraine, Influenza, Gastroenteritis
  - COVID-19, Tension Headache, Common Cold
- **200+ Medical Facts:** Symptoms, treatments, urgency levels, evidence sources, contraindications, safety warnings
- **10+ Relationship Types:** has-symptom, has-treatment, has-urgency, red-flag-symptom, differential-from, time-sensitive, contraindication, safety-warning, drug-interaction, requires-dose-adjustment
- **45+ Contraindications:** Comprehensive safety validation across all medication classes
- **Evidence Sources:** CDC, WHO, American Heart Association, Johns Hopkins Medicine

**Query Capabilities (21 Methods):**
- Emergency condition detection & red flag symptom identification
- Multi-symptom diagnostic matching with confidence scoring
- Differential diagnosis generation
- Treatment safety validation (contraindications, drug interactions, dose adjustments)
- **Transparent reasoning chain explanation** with evidence tracing
- Multi-hop reasoning for complex diagnostic scenarios

Example diagnostic query:
```python
from src.metta.query_engine import MeTTaQueryEngine

engine = MeTTaQueryEngine()
symptoms = ['fever', 'severe-headache', 'stiff-neck', 'non-blanching-rash']

# Find matching conditions
matches = engine.find_conditions_by_symptoms(symptoms)
# Output: {'meningitis': 4, 'pneumonia': 1, 'influenza': 1, 'covid-19': 1}

# Generate reasoning chain
reasoning = engine.generate_reasoning_chain(symptoms, 'meningitis')
# Shows: symptom matching, severity, urgency, red flags, treatments, differentials
```

---

## 🎥 Demo Video

**[Demo Video Link]** - 3-5 minute demonstration of the agent system

**Video Contents:**
- Problem statement and motivation
- Agent architecture overview
- Live demonstration via ASI:One
- MeTTa reasoning transparency
- Multi-agent coordination showcase
- Real-world impact and benefits

---

## 📚 Documentation

### Planning & Requirements
- [Product Requirements Document (PRD)](docs/PRD.md) - Epic → Story → Task hierarchy
- [Execution Plan & Progress Tracker](docs/EXECUTION-PLAN.md) - Daily task tracking
- [Development Timeline](docs/TIMELINE.md) - 22-day milestone schedule
- [Submission Requirements Checklist](docs/TRACK-REQUIREMENTS.md) - Hackathon requirements

### Technical Documentation
- [Getting Started Guide](docs/GETTING-STARTED.md) - Quick start for contributors
- [Hackathon Strategic Analysis](docs/hackathon-analysis.md) - Competitive strategy
- [Architecture Diagram](docs/architecture.md) (coming soon)
- [MeTTa Knowledge Graph Structure](docs/metta-knowledge.md) (coming soon)
- [API Documentation](docs/api.md) (coming soon)
- [Deployment Guide](docs/deployment.md) (coming soon)

---

## 🧪 Testing

Run tests:
```bash
python -m pytest tests/
```

Run with coverage:
```bash
python -m pytest --cov=src tests/
```

---

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Agentverse Configuration
AGENTVERSE_API_KEY=your_api_key_here
AGENT_SEED=your_agent_seed

# Agent Addresses (update after deployment)
COORDINATOR_ADDRESS=agent1...
SPECIALIST_1_ADDRESS=agent1...
SPECIALIST_2_ADDRESS=agent1...
SPECIALIST_3_ADDRESS=agent1...

# MeTTa Configuration
METTA_KB_PATH=./data/knowledge_base.metta
```

---

## 📦 Project Structure

```
asi-agents-track/
├── src/
│   ├── agents/
│   │   ├── coordinator.py          # Main routing agent
│   │   ├── specialist_1.py         # Domain specialist 1
│   │   ├── specialist_2.py         # Domain specialist 2
│   │   └── specialist_3.py         # Domain specialist 3
│   ├── protocols/
│   │   ├── chat_protocol.py        # ASI:One Chat Protocol
│   │   └── agent_protocol.py       # Inter-agent messaging
│   ├── metta/
│   │   ├── knowledge_base.metta    # MeTTa knowledge graph
│   │   └── query_engine.py         # MeTTa query interface
│   └── utils/
│       ├── logging.py              # Logging utilities
│       └── helpers.py              # Helper functions
├── tests/
│   ├── test_agents.py
│   ├── test_metta.py
│   └── test_protocols.py
├── data/
│   └── knowledge_base.metta        # Main knowledge base
├── docs/                            # All documentation
│   ├── PRD.md                      # Product Requirements Document
│   ├── EXECUTION-PLAN.md           # Progress tracker
│   ├── TIMELINE.md                 # Development timeline
│   ├── TRACK-REQUIREMENTS.md       # Submission checklist
│   ├── GETTING-STARTED.md          # Quick start guide
│   ├── hackathon-analysis.md       # Strategic analysis
│   ├── hackathon-original.md       # Original content backup
│   └── architecture.md             # System architecture (coming soon)
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md                        # Main documentation
└── CLAUDE.md                        # AI assistant context
```

---

## 🛠️ Development Roadmap

**Current Progress:** 48% complete (37/80 tasks) - **7+ DAYS AHEAD OF SCHEDULE!**

Track detailed progress in [EXECUTION-PLAN.md](docs/EXECUTION-PLAN.md)

- [x] **Epic 1:** Multi-Agent Foundation ✅ (Day 2, planned Day 7)
- [x] **Epic 2:** MeTTa Integration ✅ 100% (Day 3, planned Day 10 - **7 DAYS AHEAD!**)
- [ ] **Epic 3:** Specialized Diagnostic Agents (Days 5-12)
- [ ] **Epic 4:** ASI:One Chat Protocol (Days 11-14)
- [ ] **Epic 5:** Production Polish & Quality (Days 12-20)
- [ ] **Epic 6:** Documentation & Demo Video (Days 13-21)

**Week Progress:**
- [x] Week 1: Foundation - Basic agents + Chat Protocol + MeTTa basics ✅ **COMPLETE - 7 DAYS AHEAD!**
- [ ] Week 2: Advanced - Deep MeTTa integration + multi-agent coordination (In progress)
- [ ] Week 3: Polish - Demo video + testing + final fixes
- [ ] Week 4: Submission - Final review and submit

**Epic 2 Achievements (Day 3):**
- ✅ Medical knowledge base v1.1 with 200+ facts
- ✅ 45+ contraindications and safety validation
- ✅ 21 MeTTa query methods (12 medical + 4 safety + 5 base)
- ✅ Knowledge Graph Agent deployed and tested
- ✅ Multi-hop reasoning with differential diagnosis
- ✅ Transparent reasoning chain generation

See detailed timeline in [TIMELINE.md](docs/TIMELINE.md)

---

## 🏆 Hackathon Requirements

All requirements tracked in [TRACK-REQUIREMENTS.md](docs/TRACK-REQUIREMENTS.md)

**Mandatory:**
- ✅ uAgents Framework implementation
- ✅ Agentverse deployment
- ✅ Chat Protocol for ASI:One
- ✅ MeTTa Knowledge Graph integration
- ✅ Public GitHub repository
- ✅ 3-5 minute demo video
- ✅ Innovation Lab badges

**Judging Criteria:**
- Functionality & Technical Implementation (25%)
- Use of ASI Alliance Tech (20%)
- Innovation & Creativity (20%)
- Real-World Impact & Usefulness (20%)
- User Experience & Presentation (15%)

---

## 🤝 Contributing

This is a hackathon project. Contributions welcome during development phase.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🔗 Resources

### Official Documentation
- [Fetch.ai uAgents Framework](https://innovationlab.fetch.ai/resources/docs/agent-creation/uagent-creation)
- [Chat Protocol Guide](https://innovationlab.fetch.ai/resources/docs/examples/chat-protocol/asi-compatible-uagents)
- [MeTTa Documentation](https://metta-lang.dev/docs/learn/tutorials/python_use/metta_python_basics.html)
- [Agentverse Platform](https://agentverse.ai/)
- [ASI:One Interface](https://asi1.ai/)

### Community
- [Fetch.ai Discord](https://discord.gg/fetchai)
- [Hackathon Contact](https://t.me/prithvipc)

### Examples
- [Innovation Lab Examples](https://github.com/fetchai/innovation-lab-examples)
- [Past Hackathon Projects](https://innovationlab.fetch.ai/projects)

---

## 📞 Contact

**Developer:** RECTOR
**Project:** ASI Agents Track Submission
**Hackathon:** Cypherpunk 2025

For questions about this project, reach out via [GitHub Issues](issues) or [hackathon contact](https://t.me/prithvipc).

---

## 🙏 Acknowledgments

- Artificial Superintelligence Alliance for organizing this track
- Fetch.ai Innovation Lab for excellent documentation
- SingularityNET for MeTTa knowledge graph tools
- Superteam for hosting the hackathon platform

---

**Built for ASI Agents Track | Cypherpunk Hackathon 2025**
