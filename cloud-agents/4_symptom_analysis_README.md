# MediChain AI - Symptom Analysis Agent

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## Agent Overview

The **Symptom Analysis Agent** is the diagnostic reasoning specialist in the MediChain AI system. It uses MeTTa knowledge graphs to analyze symptom patterns, assess urgency levels, detect red flags, and generate differential diagnoses with confidence scoring.

## Key Features

- **Embedded MeTTa Knowledge Base**: 585 lines of medical knowledge (13 conditions, 200+ facts)
- **Red Flag Detection**: Identifies life-threatening symptom combinations
- **Urgency Classification**: Emergency / Urgent / Routine triage
- **Differential Diagnosis**: Generates 2-5 ranked hypotheses with confidence scores
- **Multi-Hop Reasoning**: Uses MeTTa queries for transparent diagnostic logic
- **Age-Based Risk Adjustment**: Escalates urgency for high-risk populations (< 5 or > 65 years)
- **Fallback Mode**: Rule-based logic if hyperon (MeTTa) package unavailable

## Capabilities

1. **Red Flag Detection**
   - Meningitis triad: severe headache + fever + neck stiffness
   - Stroke FAST: face drooping, arm weakness, speech difficulty
   - Cardiac emergencies: chest pain, radiating arm/jaw pain
   - Critical symptoms: coughing blood, altered mental status

2. **Urgency Assessment Thresholds**
   - **Emergency**: Confidence > 50% AND (critical urgency OR time-sensitive < 6h)
   - **Urgent**: Confidence > 30% AND (urgent urgency OR time-sensitive < 48h)
   - **Routine**: Everything else

3. **Confidence Scoring**
   - Symptom match ratio: (matched symptoms / total condition symptoms)
   - Severity weighting: Adjusts based on patient-reported severity (1-10)
   - Final confidence: 0.0 - 1.0 scale (0-100%)

4. **Reasoning Chain**
   - Transparent step-by-step diagnostic logic
   - Symptom matching details
   - Urgency assessment rationale
   - Recommended action justification

## MeTTa Knowledge Base Coverage

**13 Medical Conditions:**
- **Critical (6)**: Meningitis, Stroke, Heart Attack, Appendicitis, Pulmonary Embolism, Sepsis
- **Urgent (2)**: Pneumonia, COVID-19
- **Common (5)**: Migraine, Influenza, Gastroenteritis, Tension Headache, Common Cold

**200+ Medical Facts:**
- Symptom-condition mappings
- Urgency classifications
- Time-sensitivity data (hours until critical)
- Red flag indicators
- Differential diagnosis relationships

## Technical Stack

- **Framework**: Fetch.ai uAgents
- **Knowledge Graph**: hyperon (MeTTa) - with rule-based fallback
- **Reasoning**: Multi-hop knowledge graph queries
- **Message Models**: Pydantic-based inter-agent communication
- **Deployment**: Agentverse Cloud

## Inter-Agent Communication

**Receives From:**
- Coordinator: `agent1qdp74ezv3eas5q60s4650xt97ew5kmyt9de77w2ku55jxys8uq2uk0u440d`

**Sends To:**
- Coordinator (analysis response)

## How It Works

1. Receives `SymptomAnalysisRequestMsg` from Coordinator
2. Detects red flag symptoms (critical warnings)
3. Queries MeTTa KB for condition matches
4. Calculates confidence scores (symptom match + severity weighting)
5. Assesses urgency level (emergency/urgent/routine)
6. Generates differential diagnoses (top 2-5 ranked)
7. Determines recommended action (911/24h appointment/routine care)
8. Returns `SymptomAnalysisResponseMsg` with complete assessment

## Example Analysis

**Input Symptoms**: fever, severe-headache, stiff-neck

**Analysis Output**:
- **Urgency**: EMERGENCY
- **Red Flags**: Meningitis triad (headache + fever + neck stiffness)
- **Differential Diagnoses**:
  1. meningitis (confidence: 60%)
  2. influenza (confidence: 40%)
  3. pneumonia (confidence: 20%)
- **Reasoning Chain**:
  - Analyzing 3 symptoms: fever, severe-headache, stiff-neck
  - RED FLAGS DETECTED: Meningitis triad
  - Found 8 potential conditions
  - Urgency Assessment: EMERGENCY
  - Top differential diagnoses: meningitis, influenza, pneumonia
- **Recommended Action**: 🚨 EMERGENCY: Call 911 or go to ER immediately. Red flags detected.

## Deployment

**Status**: ✅ Deployed to Agentverse
**Address**: `agent1q036yw3pwsal2qsrq502k546lyxvnf6wt5l83qfhzhvceg6nm2la7nd6d5n`
**Availability**: 24/7 via Agentverse cloud
**MeTTa Requirement**: Uses fallback if hyperon package unavailable
