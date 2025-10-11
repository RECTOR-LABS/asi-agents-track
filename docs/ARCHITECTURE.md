# MediChain AI - System Architecture

**Document Version:** 1.0
**Last Updated:** October 10, 2024
**Project:** ASI Agents Track Hackathon Submission

---

## Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [Agent System Design](#agent-system-design)
3. [Communication Flow](#communication-flow)
4. [Data Models](#data-models)
5. [MeTTa Knowledge Graph](#metta-knowledge-graph)
6. [Deployment Architecture](#deployment-architecture)
7. [Technology Stack](#technology-stack)

---

## High-Level Architecture

MediChain AI implements a **coordinator-specialist multi-agent architecture** with transparent MeTTa-powered reasoning.

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE LAYER                        │
│                                                                      │
│  ┌───────────────┐              ┌──────────────────┐               │
│  │  ASI:One UI   │◄────────────►│ Agentverse Chat  │               │
│  │ (asi1.ai)     │              │   Interface      │               │
│  └───────────────┘              └──────────────────┘               │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Chat Protocol
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        COORDINATOR LAYER                             │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │          Coordinator Agent (Port 8000)                       │   │
│  │  - Chat Protocol handler                                     │   │
│  │  - Session management                                        │   │
│  │  - Request routing logic                                     │   │
│  │  - Response aggregation                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                   │              │              │
                   │              │              │
    ┌──────────────┤              │              ├──────────────┐
    │              │              │              │              │
    ▼              ▼              ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       SPECIALIST AGENT LAYER                         │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │ Patient      │  │ Knowledge    │  │ Symptom      │             │
│  │ Intake       │  │ Graph        │  │ Analysis     │             │
│  │ (Port 8001)  │  │ (Port 8003)  │  │ (Port 8004)  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│                                                                      │
│  ┌──────────────────────────────┐                                  │
│  │ Treatment Recommendation     │                                   │
│  │ (Port 8005)                  │                                   │
│  └──────────────────────────────┘                                  │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ MeTTa Queries
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      KNOWLEDGE BASE LAYER                            │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │          MeTTa Knowledge Base (v1.1)                         │   │
│  │  - 13 Medical conditions                                     │   │
│  │  - 200+ Medical facts                                        │   │
│  │  - 45+ Contraindications                                     │   │
│  │  - 10+ Relationship types                                    │   │
│  │  - Evidence sources (CDC, WHO, AHA, Johns Hopkins)          │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │          MeTTa Query Engine (21 methods)                     │   │
│  │  - Symptom-condition matching                                │   │
│  │  - Safety validation (contraindications, interactions)       │   │
│  │  - Reasoning chain generation                                │   │
│  │  - Differential diagnosis                                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Agent System Design

### 1. Coordinator Agent

**Address:** `agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q`
**Port:** 8000
**Role:** Central routing hub with Chat Protocol support

**Responsibilities:**
- Handle incoming user messages via ASI:One
- Manage conversation sessions (StartSession, EndSession)
- Route requests to appropriate specialist agents
- Aggregate responses from multiple agents
- Format final response for user

**Key Features:**
- Chat Protocol implementation (`ChatMessage`, `ChatAcknowledgement`)
- Session state management
- Multi-agent coordination
- Error handling and fallback responses

**Message Flow:**
```
User → ASI:One → Coordinator → [Specialist Agents] → Coordinator → ASI:One → User
```

---

### 2. Patient Intake Agent

**Address:** `agent1qgr8ga84fyjsy478ctvzp3zf5r8rw9nulzmrl9w0l3x83suxuzt6zjq29y2`
**Port:** 8001
**Role:** Natural Language Processing for symptom extraction

**Responsibilities:**
- Extract symptoms from free-text input
- Normalize symptom names to MeTTa format
- Estimate severity from descriptive keywords
- Extract duration and temporal information
- Extract patient demographics (age, gender)
- Identify need for clarifying questions

**NLP Pipeline:**
```
Raw Text Input
    │
    ├─► Symptom Extraction (regex + keyword matching)
    │   • 50+ symptom patterns
    │   • Handles specific variants (e.g., "severe-headache" vs "headache")
    │
    ├─► Severity Estimation
    │   • High severity: "severe", "unbearable", "worst ever" → 8/10
    │   • Medium severity: "moderate", "significant", "bad" → 5/10
    │   • Low severity: "mild", "slight", "little" → 3/10
    │
    ├─► Duration Extraction
    │   • "for X days/hours/weeks"
    │   • "X days ago"
    │   • Keywords: "yesterday", "this morning", "this week"
    │
    ├─► Age Extraction
    │   • "X years old" pattern
    │   • "X yr/yrs old" abbreviation
    │
    └─► Clarification Check
        • Missing critical info (age for fever)
        • No symptoms detected
        • Critical symptoms without duration
```

**Data Output:**
- `PatientIntakeData` with structured symptoms
- Each symptom includes: name, severity, duration, raw_text

---

### 3. Knowledge Graph Agent

**Address:** `agent1qdjy30exkpc0zxu6p8urwnllg9fygj27h3nzksq9twmqcsyundvckavn6v6`
**Port:** 8003
**Role:** MeTTa-powered diagnostic reasoning with transparent explanation

**Responsibilities:**
- Query MeTTa knowledge base for condition matching
- Calculate confidence scores based on symptom overlap
- Generate reasoning chains showing diagnostic logic
- Provide differential diagnoses
- Handle uncertainty and missing information

**Diagnostic Process:**
```
Symptom List Input
    │
    ├─► Multi-Symptom Query
    │   • For each symptom: find_by_symptom(symptom)
    │   • Count matches per condition
    │   • Sort by match count (descending)
    │
    ├─► Confidence Calculation
    │   • High (80-100%): 3+ symptoms matched
    │   • Medium (50-79%): 2 symptoms matched
    │   • Low (0-49%): 1 symptom matched
    │
    ├─► Reasoning Chain Generation
    │   • Symptom matching analysis
    │   • Severity and urgency classification
    │   • Time sensitivity check
    │   • Red flag detection
    │   • Treatment options with evidence
    │   • Differential diagnoses
    │
    └─► Safety Validation
        • Check contraindications
        • Drug interaction detection
        • Dose adjustment requirements
```

**MeTTa Integration:**
- 21 query methods (12 medical-specific, 4 safety, 5 base)
- Multi-hop reasoning for complex queries
- Handles nested knowledge relationships

---

### 4. Symptom Analysis Agent

**Address:** `agent1qdxqnfmu735ren2geq9f3n8ehdk43lvm9x0vxswv6xj6a5hn40yfqv0ar42`
**Port:** 8004
**Role:** Urgency assessment and red flag detection

**Responsibilities:**
- Classify urgency level (EMERGENCY, URGENT, ROUTINE)
- Detect red flag symptoms requiring immediate care
- Implement clinical protocols (Meningitis triad, Stroke FAST)
- Age-based risk adjustment
- Confidence-based urgency thresholds

**Urgency Classification:**
```
Symptom Set + Top Condition
    │
    ├─► Emergency Detection
    │   • Check urgency_level == "emergency" in MeTTa
    │   • Red flag symptom detection
    │   • Clinical protocols:
    │     - Meningitis triad: fever + severe-headache + stiff-neck
    │     - Stroke FAST: weakness + speech + face-droop
    │     - Cardiac: chest-pain + arm-numbness + shortness-of-breath
    │
    ├─► Confidence-Based Thresholds
    │   • High confidence (80%+): Use MeTTa urgency directly
    │   • Medium confidence (50-79%): Escalate if 2+ red flags
    │   • Low confidence (<50%): Default to URGENT if any red flag
    │
    ├─► Age Risk Adjustment
    │   • Age <5 or >65 with fever → escalate urgency
    │   • Elderly confusion → always URGENT minimum
    │   • Pediatric fever → parent guidance required
    │
    └─► Action Recommendation
        • EMERGENCY: "Call 911 immediately"
        • URGENT: "Seek medical attention within 24 hours"
        • ROUTINE: "Monitor symptoms, contact doctor if worsening"
```

---

### 5. Treatment Recommendation Agent

**Address:** `agent1qg9m6r976jq4lj64qfnp679qu8lu4jzcy06y09mf7ta4l2sm8uq9qfqrc9v`
**Port:** 8005
**Role:** Evidence-based treatment recommendations with safety validation

**Responsibilities:**
- Retrieve treatments from MeTTa knowledge base
- Link evidence sources (CDC, WHO, AHA, Johns Hopkins)
- Validate safety (contraindications, drug interactions)
- Check dose adjustment requirements
- Map specialist referral recommendations

**Treatment Pipeline:**
```
Condition + Patient Context
    │
    ├─► Treatment Retrieval
    │   • Query: find_treatment(condition)
    │   • Get all treatment options
    │
    ├─► Evidence Source Linking
    │   • Query: get_evidence_source(treatment)
    │   • Sources: CDC, WHO, AHA, Johns Hopkins, Mayo Clinic
    │
    ├─► Safety Validation (45+ checks)
    │   • Contraindication check: check_contraindication(treatment, patient_condition)
    │   • Drug interaction: check_drug_interaction(treatment, current_meds)
    │   • Dose adjustment: requires_dose_adjustment(treatment, patient_factors)
    │   • Safety warnings: get_safety_warning(treatment)
    │
    ├─► Specialist Referral Mapping
    │   • Emergency: Emergency Medicine
    │   • Urgent: Internal Medicine, Family Practice
    │   • Specialist: Neurology, Cardiology, ID, Pulmonology, GI
    │
    └─► Medical Disclaimer
        • "This is preliminary guidance"
        • "Consult qualified healthcare provider"
        • "Call 911 for emergencies"
```

---

## Communication Flow

### End-to-End Diagnostic Workflow

```
┌─────────┐
│  User   │ "I have a severe headache, high fever,
│ (ASI:1) │  and stiff neck. I'm 28 years old."
└────┬────┘
     │ ChatMessage (TextContent)
     ▼
┌─────────────────┐
│  Coordinator    │ Step 1: Receive and route
│   Agent         │
└────┬────────────┘
     │ IntakeTextMessage
     ▼
┌─────────────────┐
│ Patient Intake  │ Step 2: Extract symptoms
│     Agent       │ - fever (severity: 8, duration: None)
│                 │ - severe-headache (severity: 8)
│                 │ - stiff-neck (severity: 5)
│                 │ - age: 28
└────┬────────────┘
     │ PatientIntakeData
     ▼
┌─────────────────┐
│ Knowledge Graph │ Step 3: Diagnostic reasoning
│     Agent       │ - Query MeTTa: find_conditions_by_symptoms()
│                 │ - Results: meningitis (3 matches)
│                 │ - Confidence: HIGH (75%)
│                 │ - Reasoning chain: "3/3 key symptoms match"
└────┬────────────┘
     │ DiagnosticResponse
     ├──────────────────────────────────────────┐
     │                                           │
     ▼                                           ▼
┌─────────────────┐                   ┌─────────────────┐
│ Symptom         │ Step 4A: Urgency  │ Treatment       │ Step 4B:
│ Analysis Agent  │ - Meningitis triad│ Recommendation  │ Evidence
│                 │   detected        │     Agent       │
│                 │ - EMERGENCY       │ - IV antibiotics│
│                 │ - "Call 911"      │ - CDC source    │
└────┬────────────┘                   └────┬────────────┘
     │ UrgencyAnalysisResult                │ TreatmentResponse
     └──────────────┬───────────────────────┘
                    ▼
            ┌─────────────────┐
            │  Coordinator    │ Step 5: Aggregate responses
            │     Agent       │
            └────┬────────────┘
                 │ ChatMessage (TextContent)
                 ▼
            ┌─────────┐
            │  User   │ "⚠️ EMERGENCY - Call 911
            │ (ASI:1) │  Possible: Meningitis (HIGH confidence)
            └─────────┘  Symptoms match classic triad..."
```

### Message Types and Protocols

#### Chat Protocol (ASI:One Interface)
```python
# Incoming from user
ChatMessage {
    content: [
        StartSessionContent | TextContent | EndSessionContent
    ]
}

# Response to user
ChatMessage {
    content: [
        TextContent(text: "diagnostic response...")
    ]
}

# Acknowledgement (required for every message)
ChatAcknowledgement {
    session_id: str
    agent_name: str
    message: str
}
```

#### Inter-Agent Messages
```python
# Patient Intake Data
PatientIntakeData {
    session_id: str
    symptoms: List[Symptom]
    age: Optional[int]
    timestamp: datetime
}

# Diagnostic Request
DiagnosticRequest {
    session_id: str
    patient_data: PatientIntakeData
    requesting_agent: str
    analysis_type: str
}

# Diagnostic Response
DiagnosticResponse {
    session_id: str
    possible_conditions: List[PossibleCondition]
    urgency_level: UrgencyLevel
    red_flags: List[str]
    reasoning_chain: List[str]
    responding_agent: str
}

# Urgency Analysis Result
UrgencyAnalysisResult {
    session_id: str
    urgency_level: UrgencyLevel  # EMERGENCY, URGENT, ROUTINE
    confidence: float
    red_flags_detected: List[str]
    reasoning: str
    action_required: str
}

# Treatment Response
TreatmentResponse {
    session_id: str
    condition: str
    treatments: List[Treatment]
    contraindications: List[str]
    safety_warnings: List[str]
    specialist_referral: str
    medical_disclaimer: str
}
```

---

## Data Models

### Core Entities

#### Symptom
```python
class Symptom(BaseModel):
    name: str              # Normalized symptom name (e.g., "fever", "severe-headache")
    raw_text: str          # Original text from user input
    severity: int          # 1-10 scale (1=mild, 10=severe)
    duration: Optional[str]  # e.g., "3 days", "2 hours"
```

#### PossibleCondition
```python
class PossibleCondition(BaseModel):
    condition_name: str
    confidence: float                    # 0.0 to 1.0
    confidence_level: ConfidenceLevel    # HIGH, MEDIUM, LOW
    matching_symptoms: List[str]
    reasoning: str                       # Human-readable explanation
    metta_query_used: str                # MeTTa query that produced this result
```

#### Treatment
```python
class Treatment(BaseModel):
    name: str
    evidence_source: str                 # CDC, WHO, AHA, etc.
    contraindications: List[str]
    safety_warning: Optional[str]
    requires_dose_adjustment: List[str]  # Conditions requiring dose adjustment
```

### Enumerations

```python
class UrgencyLevel(str, Enum):
    EMERGENCY = "emergency"      # Call 911 immediately
    URGENT = "urgent"            # Seek care within 24 hours
    ROUTINE = "routine"          # Monitor, contact doctor if worsening

class ConfidenceLevel(str, Enum):
    HIGH = "high"      # 80-100%
    MEDIUM = "medium"  # 50-79%
    LOW = "low"        # 0-49%
```

---

## MeTTa Knowledge Graph

### Schema Structure

```metta
;; Type definitions
(: has-symptom (-> Condition Symptom))
(: has-treatment (-> Condition Treatment))
(: has-urgency (-> Condition UrgencyLevel))
(: has-severity (-> Condition SeverityLevel))
(: red-flag-symptom (-> Symptom Bool))
(: differential-from (-> Condition Condition))
(: time-sensitive (-> Condition Hours))
(: contraindication (-> Treatment Condition))
(: drug-interaction (-> Treatment Medication))
(: requires-dose-adjustment (-> Treatment Condition))
(: evidence-source (-> Treatment Source))
(: safety-warning (-> Treatment WarningText))
```

### Example Facts

```metta
;; Meningitis knowledge
(has-symptom meningitis fever)
(has-symptom meningitis severe-headache)
(has-symptom meningitis stiff-neck)
(has-symptom meningitis non-blanching-rash)
(has-symptom meningitis confusion)

(has-urgency meningitis emergency)
(has-severity meningitis critical)
(time-sensitive meningitis 6)  ; 6 hours until critical

(red-flag-symptom severe-headache true)
(red-flag-symptom stiff-neck true)
(red-flag-symptom non-blanching-rash true)

(has-treatment meningitis iv-antibiotics)
(has-treatment meningitis supportive-care)

(evidence-source iv-antibiotics CDC)
(contraindication iv-antibiotics penicillin-allergy)
(safety-warning iv-antibiotics "Immediate hospital administration required")

(differential-from meningitis pneumonia)
(differential-from meningitis influenza)
```

### Query Examples

```metta
;; Find conditions with fever
!(match &self (has-symptom $condition fever) $condition)

;; Find emergency conditions
!(match &self (has-urgency $condition emergency) $condition)

;; Find treatments for meningitis
!(match &self (has-treatment meningitis $treatment) $treatment)

;; Check contraindications for aspirin
!(match &self (contraindication aspirin $condition) $condition)

;; Find differential diagnoses for meningitis
!(match &self (differential-from meningitis $other) $other)
```

### Knowledge Base Statistics

- **13 Medical Conditions:**
  - Critical (6): Meningitis, Stroke, Heart Attack, Appendicitis, Pulmonary Embolism, Sepsis
  - Urgent (2): Pneumonia, COVID-19
  - Common (5): Migraine, Influenza, Gastroenteritis, Tension Headache, Common Cold

- **200+ Facts:** Symptoms, treatments, urgency levels, evidence sources
- **45+ Contraindications:** Comprehensive safety validation
- **10+ Relationship Types:** Complex medical knowledge modeling

---

## Deployment Architecture

### Agentverse Deployment

```
┌─────────────────────────────────────────────────────────────────┐
│                      Agentverse Cloud                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Agent Runtime Environment                              │    │
│  │                                                         │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │    │
│  │  │ Agent 1  │  │ Agent 2  │  │ Agent 3  │  ...       │    │
│  │  │ (mailbox)│  │ (mailbox)│  │ (mailbox)│            │    │
│  │  └──────────┘  └──────────┘  └──────────┘            │    │
│  │                                                         │    │
│  │  Each agent:                                           │    │
│  │  • Unique address (agent1q...)                         │    │
│  │  • Mailbox for internet connectivity                   │    │
│  │  • Published protocols (Chat Protocol for coordinator) │    │
│  │  • Environment variables (.env configuration)          │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Agent Discovery & Routing                              │    │
│  │  • Agent registry                                       │    │
│  │  • Protocol matching                                    │    │
│  │  • Message routing                                      │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  ASI:One Integration                                    │    │
│  │  • Chat Protocol support                                │    │
│  │  • Agent search and discovery                           │    │
│  │  • Session management                                   │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS
                            │
                            ▼
                    ┌──────────────┐
                    │  Users via   │
                    │   ASI:One    │
                    │  (asi1.ai)   │
                    └──────────────┘
```

### Local Development Environment

```
Developer Machine
├── Terminal 1: Coordinator Agent (port 8000)
│   └── python src/agents/coordinator.py
├── Terminal 2: Patient Intake Agent (port 8001)
│   └── python src/agents/patient_intake.py
├── Terminal 3: Knowledge Graph Agent (port 8003)
│   └── python src/agents/knowledge_graph.py
├── Terminal 4: Symptom Analysis Agent (port 8004)
│   └── python src/agents/symptom_analysis.py
├── Terminal 5: Treatment Recommendation Agent (port 8005)
│   └── python src/agents/treatment_recommendation.py
└── Terminal 6: Test Suite
    └── pytest tests/

All agents connect to Agentverse via mailbox=True
Data file: ./data/knowledge_base.metta (loaded locally)
Logs: /tmp/{agent_name}_mailbox.log
```

---

## Technology Stack

### Agent Framework
- **uAgents (0.12.0+):** Fetch.ai's agent framework
- **uagents-core (0.1.0+):** Core protocols and message handling
- **Chat Protocol:** ASI:One compatible messaging

### Knowledge Graph
- **hyperon (0.1.0+):** SingularityNET's MeTTa implementation
- **MeTTa Language:** Logic programming for medical knowledge

### Development Tools
- **Python 3.9+**
- **Pydantic:** Data validation and message models
- **pytest:** Testing framework (109 tests)
- **pytest-cov:** Code coverage reporting
- **pytest-asyncio:** Async test support

### Deployment
- **Agentverse:** Cloud agent hosting
- **Mailbox:** Internet connectivity for agents
- **ASI:One:** User interface platform

### Infrastructure
- **Git/GitHub:** Version control
- **Virtual Environment:** Isolated Python dependencies
- **Environment Variables:** Configuration management (.env)

---

## Performance Characteristics

### Response Times
- **Patient Intake NLP:** <1 second
- **MeTTa Query:** 1-2 seconds
- **Full Diagnostic Flow:** 3-5 seconds end-to-end
- **Test Suite Execution:** 3.47 seconds (109 tests)

### Scalability
- **Concurrent Sessions:** 10+ simultaneous users (local testing)
- **Agent Scaling:** Horizontal scaling via Agentverse
- **Knowledge Base:** 13 conditions, expandable to 100+ without performance impact

### Reliability
- **Test Coverage:** 84% core components, 100% protocols
- **Error Handling:** Try-catch blocks in all agents
- **Fallback Responses:** Default responses when MeTTa queries fail
- **Zero Critical Bugs:** Found in 109 comprehensive tests

---

## Security & Privacy

### Data Handling
- **No PHI Storage:** All data processed in-memory, not persisted
- **Session Isolation:** Each session independent, no cross-contamination
- **No Authentication Required:** Demonstration project, no user accounts

### Medical Disclaimer
- **Educational Purpose Only:** NOT for actual medical use
- **No Clinical Validation:** Has not been tested in clinical settings
- **User Warning:** Every response includes disclaimer and 911 guidance

### API Security
- **Agentverse API Keys:** Required for deployment, stored in .env (gitignored)
- **Agent Addresses:** Public, no authentication (demonstration project)
- **No Sensitive Data:** Knowledge base contains only public medical information

---

## Future Architecture Enhancements

### Potential Improvements
1. **Enhanced NER:** SpaCy/Transformers for better symptom extraction
2. **Conversation Memory:** Redis for multi-turn diagnostic conversations
3. **Knowledge Base Expansion:** 50+ conditions, 1000+ facts
4. **Clinical Validation:** Testing with medical professionals
5. **User Profiles:** Basic demographic storage for better recommendations
6. **API Gateway:** RESTful API for third-party integrations
7. **Analytics Dashboard:** Usage metrics, accuracy tracking
8. **Multi-Language Support:** I18n for global accessibility

---

**Document Maintained By:** RECTOR
**Project Repository:** https://github.com/RECTOR-LABS/asi-agents-track
**Last Architecture Review:** October 10, 2024
