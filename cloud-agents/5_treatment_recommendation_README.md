# MediChain AI - Treatment Recommendation Agent

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## Agent Overview

The **Treatment Recommendation Agent** is the evidence-based treatment specialist in the MediChain AI system. It uses MeTTa knowledge graphs to provide treatment recommendations with comprehensive safety validation, including contraindication checking, drug interaction warnings, and specialist referral guidance.

## Key Features

- **Embedded MeTTa Knowledge Base**: 585 lines of medical knowledge including treatments and safety data
- **Evidence-Based Treatments**: Treatments linked to CDC, WHO, and medical guidelines
- **Comprehensive Contraindication Checking**: 45+ contraindications across all treatments
- **Drug Interaction Validation**: Checks interactions with current medications
- **Allergy Alerts**: Cross-references treatments with patient allergies
- **Age-Specific Safety**: Pediatric and geriatric contraindications
- **Specialist Referral Recommendations**: Appropriate specialist type based on condition
- **Follow-Up Timeline**: Time-sensitive care scheduling
- **Safety Warnings**: Treatment-specific warnings from knowledge base
- **Fallback Mode**: Rule-based logic if hyperon (MeTTa) package unavailable

## Capabilities

1. **Treatment Lookup**
   - Emergency treatments (immediate-911, aspirin-immediately, tPA-within-3-hours)
   - Hospital treatments (antibiotics, antivirals, surgical-appendectomy)
   - Home care (rest-and-fluids, oral-rehydration, symptom-management)

2. **Safety Validation**
   - **Contraindications**: Disease-based (kidney-disease, bleeding-disorder, pregnancy)
   - **Age-Based**: Pediatric (age-under-18), Geriatric (age-over-65)
   - **Medical History**: Existing conditions that contraindicate treatments
   - **Dose Adjustment**: Conditions requiring modified dosing

3. **Drug Interaction Checking**
   - anticoagulation + aspirin → Increased bleeding risk
   - NSAIDs + anticoagulation → Increased bleeding risk
   - antiviral-paxlovid + statins → Metabolism interaction
   - antibiotics + oral-contraceptives → Reduced effectiveness

4. **Allergy Screening**
   - Cross-references treatment ingredients with patient allergies
   - Flags potential allergen exposure
   - Checks drug class allergies (e.g., penicillin allergy → all penicillin-based antibiotics)

5. **Specialist Referral Map**
   - Meningitis → Neurologist or Infectious Disease (ER immediately)
   - Stroke → Neurologist (ER - time is brain)
   - Heart Attack → Cardiologist (ER - call 911)
   - Pneumonia → Pulmonologist or Primary Care
   - Migraine → Neurologist
   - COVID-19 → Primary Care or Infectious Disease

## Technical Stack

- **Framework**: Fetch.ai uAgents
- **Knowledge Graph**: hyperon (MeTTa) - with rule-based fallback
- **Safety Checks**: Multi-layer validation (contraindications + interactions + allergies)
- **Message Models**: Pydantic-based inter-agent communication
- **Deployment**: Agentverse Cloud

## Inter-Agent Communication

**Receives From:**
- Coordinator: `agent1qdp74ezv3eas5q60s4650xt97ew5kmyt9de77w2ku55jxys8uq2uk0u440d`

**Sends To:**
- Coordinator (treatment response)

## How It Works

1. Receives `TreatmentRequestMsg` from Coordinator
2. Queries MeTTa KB for evidence-based treatments
3. Retrieves evidence sources (CDC, WHO, medical guidelines)
4. Checks contraindications (disease-based, age-based, medical history)
5. Validates drug interactions with current medications
6. Screens for allergy conflicts
7. Retrieves treatment-specific safety warnings from MeTTa
8. Recommends specialist type based on condition and urgency
9. Determines follow-up timeline (immediate / 24h / 1-2 weeks)
10. Returns `TreatmentResponseMsg` with complete recommendations

## Example Recommendation

**Input**:
- Condition: meningitis
- Urgency: emergency
- Patient Age: 25
- Medical History: None
- Allergies: None

**Output**:
- **Treatments**:
  1. immediate-911
  2. emergency-antibiotics
  3. hospital-admission
- **Evidence Sources**:
  - immediate-911: CDC-Guidelines
  - emergency-antibiotics: Clinical guidelines
  - hospital-admission: Clinical guidelines
- **Contraindications**:
  - emergency-antibiotics: [severe-allergy-penicillin]
- **Safety Warnings**:
  - "Do not drive yourself. Call ambulance."
  - "Inform provider of all allergies before administration"
- **Specialist Referral**: Neurologist or Infectious Disease Specialist (ER immediately)
- **Follow-Up**: Immediate (ER visit required)

## Safety Features

**Multi-Layer Validation:**
1. **Level 1**: MeTTa contraindication lookup (disease-based)
2. **Level 2**: Age-based screening (pediatric/geriatric)
3. **Level 3**: Medical history cross-reference
4. **Level 4**: Drug interaction checking
5. **Level 5**: Allergy screening
6. **Level 6**: Dose adjustment warnings

**Medical Disclaimer:**
Every response includes a comprehensive medical disclaimer stating that recommendations are AI-powered preliminary guidance and NOT medical advice. Users must consult licensed healthcare professionals before starting any treatment.

## Deployment

**Status**: ✅ Deployed to Agentverse
**Address**: `agent1q0q46ztah7cyw4z7gcg3mued9ncnrcvrcqc8kjku3hywqdzp03e36hk5qsl`
**Availability**: 24/7 via Agentverse cloud
**MeTTa Requirement**: Uses fallback if hyperon package unavailable
