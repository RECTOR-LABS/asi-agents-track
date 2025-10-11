# MediChain AI - Coordinator Agent

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## Agent Overview

The **Coordinator Agent** is the central routing hub of the MediChain AI multi-agent diagnostic system. It orchestrates communication between the user and specialized diagnostic agents, managing session state and aggregating results into comprehensive medical assessments.

## Key Features

- **ASI:One Chat Protocol**: Full integration with ASI:One interface for natural language interaction
- **Session Management**: Maintains conversation context and patient data across multiple agent interactions
- **Multi-Agent Orchestration**: Routes requests to:
  - Patient Intake Agent (symptom extraction)
  - Symptom Analysis Agent (urgency assessment)
  - Treatment Recommendation Agent (evidence-based treatments)
- **Comprehensive Reporting**: Aggregates specialist responses into unified diagnostic reports
- **Real-time Updates**: Streams progress updates to users during analysis

## Capabilities

1. **User Interface**
   - Welcome messaging and session initialization
   - Natural language symptom intake
   - Progress notifications
   - Final report generation

2. **Routing Logic**
   - Intelligent message routing to specialist agents
   - Session-based request correlation
   - Response aggregation

3. **Report Compilation**
   - Symptom analysis summary
   - Differential diagnoses ranking
   - Treatment recommendations with evidence
   - Safety warnings and contraindications
   - Specialist referral guidance

## Technical Stack

- **Framework**: Fetch.ai uAgents
- **Protocol**: ASI:One Chat Protocol (ChatMessage, StartSession, EndSession)
- **Message Models**: Pydantic-based inter-agent communication
- **Deployment**: Agentverse Cloud

## Inter-Agent Communication

**Connected Agents:**
- Patient Intake: `agent1qfxfjs7y6gxa8psr5mzugcg45j46znra4qg0t5mxljjv5g9mx7dw6238e4a`
- Symptom Analysis: `agent1q036yw3pwsal2qsrq502k546lyxvnf6wt5l83qfhzhvceg6nm2la7nd6d5n`
- Treatment Recommendation: `agent1q0q46ztah7cyw4z7gcg3mued9ncnrcvrcqc8kjku3hywqdzp03e36hk5qsl`

## How It Works

1. User initiates chat session via ASI:One
2. Coordinator sends welcome message
3. User describes symptoms in natural language
4. Coordinator routes to Patient Intake for extraction
5. Receives structured symptom data
6. Routes to Symptom Analysis for urgency assessment
7. Receives differential diagnoses and red flags
8. Routes to Treatment Recommendation for evidence-based guidance
9. Compiles comprehensive report
10. Delivers final assessment to user

## Medical Disclaimer

This agent provides **preliminary health information only** and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals for medical concerns.

## Deployment

**Status**: ✅ Deployed to Agentverse
**Address**: `agent1qdp74ezv3eas5q60s4650xt97ew5kmyt9de77w2ku55jxys8uq2uk0u440d`
**Availability**: 24/7 via Agentverse cloud
**Access**: https://chat.agentverse.ai/ or https://asi1.ai/
