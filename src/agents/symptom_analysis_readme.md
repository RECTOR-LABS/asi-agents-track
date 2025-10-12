# MediChain AI - Symptom Analysis Specialist

## Agent Expertise

Advanced diagnostic reasoning specialist using MeTTa knowledge graph for symptom-to-condition matching, urgency classification, and red flag detection. Integrates 25 medical conditions with risk-adjusted confidence scoring.

## Capabilities

- **Differential Diagnosis**: Generate 2-5 possible conditions with confidence scores
- **Urgency Classification**: Emergency (0-4h), Urgent (24-48h), Routine (days-weeks)
- **Red Flag Detection**: Identify life-threatening symptom patterns
- **Risk-Adjusted Scoring**: Factor age, medical history, symptom attributes
- **Clinical Scoring Systems**: PERC, Wells, CURB-65, CHA2DS2-VASc, GCS, Centor
- **Attribute-Based Matching**: Duration, onset, location, character filtering
- **Time Sensitivity Analysis**: Assess when immediate care is needed

## Advanced Features (Epic 7)

**Risk Factor Integration (180 factors):**
- Age-based risk adjustment (<5, 5-18, 19-65, >65)
- Medical history impact (diabetes, hypertension, immunosuppression)
- Lifestyle factors (smoking, obesity, alcohol use)
- Seasonal and geographic epidemiology

**Symptom Attributes:**
- Duration (acute <24h, subacute 1-7 days, chronic >7 days)
- Onset (sudden, gradual, intermittent)
- Location (localized, diffuse, radiating)
- Character (sharp, dull, throbbing, burning)

**Confidence Scoring:**
- Base confidence from symptom matching
- Risk multiplier (1.0-1.5x for high-risk patients)
- Attribute boost (0-20% for matching characteristics)

## Condition Coverage (25 conditions)

**Emergency:** Meningitis, Stroke, Heart Attack, Appendicitis, Pulmonary Embolism, Sepsis, DKA, Anaphylaxis, Heat Stroke

**Urgent:** Pneumonia, COVID-19, Hypoglycemia, Asthma Exacerbation, DVT, Kidney Stones, Concussion

**Routine:** Migraine, Influenza, UTI, Gastroenteritis, Dehydration, Food Poisoning, Cellulitis, Tension Headache, Common Cold

## Red Flag Patterns Detected

- **Meningitis Triad**: Headache + fever + neck stiffness
- **Stroke FAST**: Face drooping, arm weakness, speech difficulty
- **Cardiac**: Chest pain + shortness of breath + left arm pain
- **Sepsis**: High fever + rapid heart rate + confusion + low blood pressure
- **DKA**: Excessive thirst + fruity breath + confusion + rapid breathing

## Use Cases

- Emergency symptom triage for 911 guidance
- Differential diagnosis generation for primary care
- Risk stratification for hospital admission decisions
- Clinical decision support for non-physicians
- Medical education and training

## How It Works

1. Receives structured symptom data from Patient Intake
2. Queries MeTTa knowledge graph for matching conditions
3. Applies risk-adjusted confidence scoring
4. Detects red flag patterns
5. Classifies urgency level
6. Generates differential diagnosis list (top 5)
7. Recommends next clinical steps

## Knowledge Base

- 2,074 medical facts
- 25 conditions with 8-12 symptoms each
- 180 risk factors with multipliers
- 56 symptom attributes
- 106 epidemiological patterns (96 seasonal + 10 geographic)
