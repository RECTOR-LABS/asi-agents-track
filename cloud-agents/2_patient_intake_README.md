# MediChain AI - Patient Intake Agent

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## Agent Overview

The **Patient Intake Agent** is the first-line symptom extraction specialist in the MediChain AI system. It uses natural language processing and pattern matching to extract structured symptom data from patient descriptions, performing intelligent clarification when needed.

## Key Features

- **NLP Symptom Extraction**: Pattern matching across 20+ symptom categories
- **Severity Estimation**: Automatic severity scoring (1-10) based on descriptive language
- **Duration Detection**: Extracts temporal information ("for 3 days", "since yesterday")
- **Age Extraction**: Identifies patient age from natural language
- **Intelligent Clarification**: Asks targeted follow-up questions for critical symptoms
- **Session Management**: Tracks multi-turn conversations for complete data gathering

## Capabilities

1. **Symptom Detection Categories**
   - Fever & Temperature (high-fever, fever, chills)
   - Neurological (headache, dizziness, confusion)
   - Respiratory (difficulty-breathing, cough, sore-throat)
   - Gastrointestinal (nausea, vomiting, diarrhea, abdominal-pain)
   - Cardiac & Pain (chest-pain, muscle-pain, joint-pain)
   - Other (rash, fatigue, loss-of-consciousness)

2. **Severity Classification**
   - **High** (8/10): severe, extreme, worst, unbearable, terrible, intense
   - **Medium** (5/10): moderate, significant, bad, strong
   - **Low** (3/10): mild, slight, little bit, somewhat
   - **Default** (5/10): No severity descriptor found

3. **Clarification Logic**
   - Requests symptom details if none detected
   - Asks duration for critical symptoms (chest pain, difficulty breathing)
   - Requests age for fever cases
   - Limits clarification to 2 rounds to avoid loops

## Technical Stack

- **Framework**: Fetch.ai uAgents
- **NLP**: Regex-based pattern matching with keyword dictionaries
- **Message Models**: Pydantic-based inter-agent communication
- **Deployment**: Agentverse Cloud

## Inter-Agent Communication

**Sends To:**
- Coordinator: `agent1qdp74ezv3eas5q60s4650xt97ew5kmyt9de77w2ku55jxys8uq2uk0u440d`

**Receives From:**
- Coordinator (user messages forwarded)

## How It Works

1. Receives `IntakeTextMessage` from Coordinator with patient text
2. Applies pattern matching to extract symptoms
3. Estimates severity from descriptive words
4. Extracts duration and age if present
5. Checks if clarification needed (missing symptoms/critical info)
6. Sends clarification question OR structured `DiagnosticRequest`
7. Coordinator routes to next specialist

## Example Extractions

**Input**: *"I have a severe headache and fever for 3 days"*
**Output**:
- Symptoms: severe-headache (severity: 8), fever (severity: 5)
- Duration: "3 days"
- Age: Not detected

**Input**: *"My 5 year old has a rash and vomiting"*
**Output**:
- Symptoms: rash (severity: 5), vomiting (severity: 5)
- Age: 5
- Duration: Not specified

## Deployment

**Status**: ✅ Deployed to Agentverse
**Address**: `agent1qfxfjs7y6gxa8psr5mzugcg45j46znra4qg0t5mxljjv5g9mx7dw6238e4a`
**Availability**: 24/7 via Agentverse cloud
