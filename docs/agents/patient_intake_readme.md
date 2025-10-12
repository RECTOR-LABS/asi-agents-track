# MediChain AI - Patient Intake Specialist

## Agent Expertise

Natural language processing specialist for medical symptom extraction and patient data structuring. This agent converts conversational descriptions of health concerns into structured medical data for diagnostic analysis.

## Capabilities

- **Symptom Extraction**: Parse natural language to identify specific medical symptoms
- **Severity Assessment**: Estimate symptom severity from descriptive language (mild, moderate, severe)
- **Duration Tracking**: Extract temporal information (hours, days, weeks)
- **Clarifying Questions**: Intelligently request missing critical information
- **Data Normalization**: Standardize symptom terminology for consistent analysis
- **Input Validation**: Rate limiting and message validation for safety

## Recognized Symptoms (80+ patterns)

**Categories:**
- Fever & Temperature (high fever, chills, sweating)
- Neurological (headache, dizziness, confusion, seizures)
- Respiratory (cough, shortness of breath, wheezing)
- Cardiovascular (chest pain, palpitations, irregular heartbeat)
- Gastrointestinal (nausea, vomiting, diarrhea, abdominal pain)
- Musculoskeletal (joint pain, muscle pain, weakness)
- Dermatological (rash, bruising, skin changes)
- General (fatigue, loss of appetite, weight loss)

## Use Cases

- Initial symptom collection from patients
- Emergency symptom triage
- Follow-up clarification for incomplete information
- Medical history extraction
- Age and demographic data collection

## How to Interact

Describe your symptoms naturally:
- ✅ "I've had a severe headache and high fever for 2 days"
- ✅ "My chest hurts when I breathe, started this morning"
- ✅ "I'm 28 years old with stomach pain and nausea"

The agent will:
1. Extract structured symptom data
2. Ask clarifying questions if needed
3. Forward complete information for diagnostic analysis

## Important Notes

- Supports multi-turn conversations for clarification
- Rate limited to 20 requests per hour for safety
- Maximum message length: 2000 characters
- Requires age for certain condition assessments (fever, cardiac symptoms)
