# ASI Agents Track - Hackathon Project

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

**Hackathon:** Cypherpunk - ASI Agents Track
**Sponsor:** Artificial Superintelligence Alliance
**Deadline:** October 31, 2025
**Prize Pool:** $20,000 USDC

---

## 🎯 Project Overview

> **Note:** This is a template setup for the ASI Agents Track hackathon. Update this section with your actual project description once you've chosen your problem domain.

[Brief description of what your agent system does - 2-3 sentences]

**Problem Statement:** [What problem does this solve?]

**Solution:** [How do your agents solve it?]

**Impact:** [What's the real-world benefit?]

---

## 🏗️ Architecture

### Agent System

- **Coordinator Agent** - [Description and address]
- **Specialist Agent 1** - [Description and address]
- **Specialist Agent 2** - [Description and address]
- **Specialist Agent 3** - [Description and address]

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
python src/agents/specialist_1.py
python src/agents/specialist_2.py
python src/agents/specialist_3.py
```

3. Test via ASI:One interface: [https://asi1.ai/](https://asi1.ai/)

---

## 📋 Agent Details

### Coordinator Agent
- **Name:** [Agent Name]
- **Address:** `agent1...` (will be updated after deployment)
- **Role:** Routes user requests to appropriate specialist agents
- **Chat Protocol:** ✅ Enabled

### Specialist Agent 1
- **Name:** [Agent Name]
- **Address:** `agent1...` (will be updated after deployment)
- **Role:** [Specific domain expertise]
- **MeTTa Integration:** ✅ Yes

### Specialist Agent 2
- **Name:** [Agent Name]
- **Address:** `agent1...` (will be updated after deployment)
- **Role:** [Specific domain expertise]
- **MeTTa Integration:** ✅ Yes

### Specialist Agent 3
- **Name:** [Agent Name]
- **Address:** `agent1...` (will be updated after deployment)
- **Role:** [Specific domain expertise]
- **MeTTa Integration:** ✅ Yes

---

## 🧠 MeTTa Knowledge Graph

Our MeTTa knowledge graph contains:

- **[Domain]:** [Number] entries with [relationship types]
- **Evidence Sources:** [CDC, WHO, research papers, etc.]
- **Query Capabilities:** [Types of queries supported]

Example query:
```python
# [Show example MeTTa query relevant to your domain]
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
├── docs/
│   └── architecture.md
├── resources/                       # Hackathon resources
│   ├── hackathon-original.md       # Original content backup
│   ├── hackathon-analysis.md       # Strategic analysis
│   └── official-docs/              # Reference documentation
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── TRACK-REQUIREMENTS.md           # Submission checklist
└── TIMELINE.md                     # Development timeline
```

---

## 🛠️ Development Roadmap

Track progress in [TIMELINE.md](TIMELINE.md)

- [x] Week 1: Foundation - Basic agents and Chat Protocol
- [ ] Week 2: Advanced - MeTTa integration and polish
- [ ] Week 3: Demo - Video production and testing
- [ ] Week 4: Submission - Final review and submit

See detailed milestones in [TIMELINE.md](TIMELINE.md)

---

## 🏆 Hackathon Requirements

All requirements tracked in [TRACK-REQUIREMENTS.md](TRACK-REQUIREMENTS.md)

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
