# Getting Started with ASI Agents Track

**Welcome to your ASI Agents Track hackathon workspace!** This guide will help you get up and running quickly.

---

## 📁 What's Been Set Up

Your workspace includes:

✅ **Comprehensive Documentation**
- `hackathon-original.md` - Complete hackathon details backup
- `hackathon-analysis.md` - Strategic analysis and winning approach
- `TRACK-REQUIREMENTS.md` - Complete submission checklist
- `TIMELINE.md` - Day-by-day development plan (22 days)
- `README.md` - Project documentation template

✅ **Project Structure**
- `/src/agents/` - Coordinator and specialist agent templates
- `/src/metta/` - MeTTa query engine for knowledge graphs
- `/data/` - MeTTa knowledge base file
- `/tests/` - Test files (pytest)
- `/resources/` - Hackathon reference materials

✅ **Starter Code**
- Coordinator agent with Chat Protocol (ASI:One compatible)
- Specialist agent template
- MeTTa integration boilerplate
- Python requirements and configuration

✅ **Development Tools**
- Virtual environment setup script
- Environment variable template (.env.example)
- Git ignore configuration
- MIT License

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Run Setup Script
```bash
cd ~/local-dev/asi-agents-track
./setup.sh
```

This will:
- Create Python virtual environment
- Install all dependencies (uAgents, MeTTa, etc.)
- Create .env configuration file
- Set up project directories

### Step 2: Configure Environment
```bash
nano .env
```

Add your Agentverse API key:
```env
AGENTVERSE_API_KEY=your_actual_api_key
AGENT_SEED=your_unique_seed_phrase
```

Get your API key from: https://agentverse.ai/

### Step 3: Test Coordinator Agent
```bash
python src/agents/coordinator.py
```

You should see:
```
Coordinator Agent started!
Agent address: agent1q...
Agent name: coordinator
```

### Step 4: Test ASI:One Integration

1. Deploy your coordinator agent to Agentverse
2. Visit https://asi1.ai/
3. Search for your agent
4. Start chatting!

---

## 📖 Essential Reading (30 Minutes)

Before you start coding, read these in order:

### 1. Strategic Analysis (15 min)
```bash
cat hackathon-analysis.md
```
**Key insights:**
- Recommended project: MediChain AI (healthcare diagnostics)
- Top 3 scoring opportunities
- Technical feasibility assessment
- Competitive differentiation strategies

### 2. Requirements Checklist (10 min)
```bash
cat TRACK-REQUIREMENTS.md
```
**Critical items:**
- All mandatory technical requirements
- Submission checklist (code, video, badges)
- Judging criteria optimization guide
- Prize terms and conditions

### 3. Development Timeline (5 min)
```bash
cat TIMELINE.md
```
**22-day plan:**
- Week 1: Foundation (agents + Chat Protocol)
- Week 2: Advanced (MeTTa + polish)
- Week 3: Demo video + testing
- Week 4: Submission + buffer

---

## 🎯 Day 1 Goals (Today - 4 Hours)

Based on TIMELINE.md, your Day 1 goals are:

### ✅ Environment Setup (1 hour)
- [x] Project workspace created
- [ ] Run `./setup.sh` to install dependencies
- [ ] Configure `.env` with Agentverse credentials
- [ ] Verify Python 3.9+ installed

### ✅ Learn uAgents Basics (1.5 hours)
- [ ] Read [uAgents Quickstart](https://innovationlab.fetch.ai/resources/docs/agent-creation/uagent-creation)
- [ ] Run coordinator agent locally
- [ ] Understand agent lifecycle (startup, messages, intervals)
- [ ] Test agent communication basics

### ✅ MeTTa Introduction (1 hour)
- [ ] Read [MeTTa Python Basics](https://metta-lang.dev/docs/learn/tutorials/python_use/metta_python_basics.html)
- [ ] Run `python src/metta/query_engine.py` example
- [ ] Understand MeTTa query syntax
- [ ] Experiment with adding facts

### ✅ Evening Check (30 min)
- [ ] Can you create and run a simple agent? ✅
- [ ] Do you understand Chat Protocol structure?
- [ ] Can you query MeTTa knowledge base?

---

## 📚 Key Resources

### Official Documentation
- **uAgents:** https://innovationlab.fetch.ai/resources/docs/agent-creation/uagent-creation
- **Chat Protocol:** https://innovationlab.fetch.ai/resources/docs/examples/chat-protocol/asi-compatible-uagents
- **MeTTa:** https://metta-lang.dev/docs/learn/tutorials/python_use/metta_python_basics.html
- **Agentverse:** https://agentverse.ai/
- **ASI:One:** https://asi1.ai/

### Code Examples
- **Innovation Lab Examples:** https://github.com/fetchai/innovation-lab-examples
- **Past Hackathon Projects:** https://innovationlab.fetch.ai/projects
- **MeTTa + Fetch.ai Integration:** https://github.com/fetchai/innovation-lab-examples/tree/main/web3/singularity-net-metta

### Community Support
- **Discord:** https://discord.gg/fetchai
- **Telegram:** https://t.me/prithvipc

---

## 🗺️ Project Workflow

### Typical Development Flow

1. **Design Phase**
   - Choose problem domain (healthcare, logistics, finance, etc.)
   - Design agent architecture (coordinator + specialists)
   - Plan MeTTa knowledge graph structure

2. **Development Phase**
   - Implement agents one by one
   - Test locally before deploying
   - Build MeTTa knowledge base incrementally
   - Integrate Chat Protocol for ASI:One

3. **Testing Phase**
   - Unit tests for core logic
   - End-to-end testing via ASI:One
   - Edge case handling
   - Performance optimization

4. **Documentation Phase**
   - Update README with agent details
   - Add architecture diagrams
   - Document setup instructions
   - Create troubleshooting guide

5. **Demo Phase**
   - Script demo video (3-5 minutes)
   - Record and edit professional video
   - Upload to YouTube
   - Add link to README

6. **Submission Phase**
   - Review TRACK-REQUIREMENTS.md checklist
   - Verify all requirements met
   - Test from clean deployment
   - Submit on time!

---

## 💡 Pro Tips

### Agent Development
- **Start simple:** Get 1 agent working before building complex systems
- **Test early:** Deploy to Agentverse early to catch issues
- **Log everything:** Comprehensive logging saves debugging time
- **Handle errors:** Graceful error handling impresses judges

### MeTTa Integration
- **Start small:** 5-10 facts first, then expand
- **Test queries:** Verify each query works before building on it
- **Document structure:** Clear knowledge graph documentation is key
- **Show reasoning:** Transparent MeTTa reasoning is a differentiator

### Hackathon Strategy
- **Follow TIMELINE.md:** Day-by-day plan prevents rushed work
- **Use TRACK-REQUIREMENTS.md:** Review checklist weekly
- **Read hackathon-analysis.md:** Contains winning strategies
- **Buffer time:** Keep 2-day buffer before deadline

### Common Pitfalls to Avoid
- ❌ Skipping Chat Protocol (required for ASI:One)
- ❌ Superficial MeTTa integration (needs depth)
- ❌ Poor documentation (15% of judging criteria)
- ❌ Broken demo video (make backup recordings)
- ❌ Missing Innovation Lab badges (required)

---

## 🔍 Troubleshooting

### "Module not found" errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Agent won't start
```bash
# Check Python version (needs 3.9+)
python3 --version

# Check for port conflicts
# Try different port in agent initialization
```

### MeTTa import errors
```bash
# Install hyperon separately
pip install hyperon

# Check installation
python -c "import hyperon; print('MeTTa OK')"
```

### Agentverse deployment issues
- Verify API key in `.env` is correct
- Check agent has unique seed phrase
- Ensure no port conflicts
- Review Agentverse logs for errors

---

## 📋 Daily Workflow

**Recommended routine:**

### Morning (2 hours - Deep Work)
1. Review day's milestone in TIMELINE.md
2. Tackle most complex task first
3. Focus on core development

### Evening (2 hours - Testing & Docs)
1. Test what you built
2. Update documentation
3. Commit to GitHub
4. Plan next day's tasks

### Weekly Checkpoint
1. Review week's success criteria
2. Assess if on track
3. Adjust plan if needed
4. Celebrate progress! Alhamdulillah!

---

## 🎯 Success Checklist

### Week 1 (Oct 9-15)
- [ ] Environment setup complete
- [ ] 4 agents running locally
- [ ] Chat Protocol working via ASI:One
- [ ] Basic MeTTa integration (5-10 facts)
- [ ] All agents deployed to Agentverse

### Week 2 (Oct 16-22)
- [ ] Deep MeTTa integration (20-30 facts)
- [ ] Transparent reasoning visible
- [ ] Advanced multi-agent coordination
- [ ] Production-ready code quality
- [ ] Comprehensive documentation

### Week 3 (Oct 23-29)
- [ ] Professional demo video (3-5 min)
- [ ] Comprehensive testing complete
- [ ] All bugs fixed
- [ ] Ready for submission

### Week 4 (Oct 30-31)
- [ ] Submission completed
- [ ] All requirements verified
- [ ] Agents running and accessible
- [ ] Waiting for results!

---

## 🚨 Emergency Contacts

**Technical Issues:**
- Fetch.ai Discord: https://discord.gg/fetchai
- Hackathon Contact: https://t.me/prithvipc

**Hackathon Platform:**
- Superteam Earn: https://earn.superteam.fun/listing/asi-agents-track

---

## 🙏 Final Notes

**Remember:**
- You have 22 days - use TIMELINE.md to stay on track
- Quality > Quantity - 10 well-modeled conditions beats 50 superficial ones
- The analysis recommends **MediChain AI** (healthcare) as top project
- You have a strategic roadmap - follow it!

**From your CLAUDE.md:**
- Focus on building what needs to be built, not rushing
- 100% working standard - no half-implementations
- Trust there is sufficient time to deliver excellent work
- Build thoroughly, ship confidently

---

**Bismillah! Start your engines! May Allah grant you tawfeeq and success! 🚀**

**Your next command:**
```bash
./setup.sh
```

Then review hackathon-analysis.md for your winning strategy!

---

**Questions?** Review the documentation or reach out to the community!
