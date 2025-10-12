# MediChain AI - Knowledge Graph Engine

## Agent Expertise

MeTTa-powered medical knowledge graph engine providing symbolic reasoning for 25 medical conditions. Handles complex diagnostic queries with 2,074 medical facts, 180 risk factors, and advanced clinical intelligence.

## Capabilities

- **Symbolic Reasoning**: MeTTa-based logical inference for medical diagnosis
- **Knowledge Graph Queries**: 34 query methods for medical data retrieval
- **Multi-Hop Reasoning**: Chain symptoms → conditions → treatments → specialists
- **Confidence Scoring**: Probabilistic reasoning with risk adjustment
- **Reasoning Chain Generation**: Transparent, explainable diagnostic logic
- **Temporal Reasoning**: Time-sensitive condition detection
- **Uncertainty Handling**: Multiple possible diagnoses with confidence levels

## Knowledge Base Statistics (Epic 7 Complete)

- **Conditions**: 25 (9 emergency, 7 urgent, 9 routine)
- **Medical Facts**: 2,074 (was 624) - **+232% growth**
- **Risk Factors**: 180 with multipliers (new in Epic 7)
- **Treatment Protocols**: 60 steps for 8 critical conditions (new in Epic 7)
- **Symptom Attributes**: 56 attributes for 10 symptoms (new in Epic 7)
- **Epidemiological Patterns**: 106 (96 seasonal + 10 geographic)
- **Contraindications**: 83+
- **Query Methods**: 34 (was 21) - **+13 new methods**

## Query Methods (34 total)

**Basic Queries (5 methods):**
- Find by symptom
- Find treatments
- Find urgency level
- Add facts dynamically
- Get all facts

**Medical-Specific (12 methods):**
- Emergency condition detection
- Red flag symptoms
- Differential diagnosis
- Reasoning chain generation
- Contraindications
- Drug interactions
- Dose adjustments
- Safety warnings
- Time sensitivity checking
- Specialist referrals
- Follow-up timelines
- Medical history risk factors

**Lab & Imaging (4 methods - Epic 7):**
- Find lab tests for condition
- Find imaging requirements
- Get all lab tests
- Get all imaging types

**Risk Assessment (7 methods - Epic 7):**
- Get risk factors for condition
- Calculate risk score
- Get risk factor multipliers
- Apply clinical scoring systems
- Get symptom attributes
- Filter by symptom attributes
- Age-based risk adjustment

**Treatment Protocols (6 methods - Epic 7):**
- Get treatment protocol steps
- Get protocol timing
- Get protocol priorities
- Sequence protocol steps
- Get seasonal epidemiology
- Get geographic epidemiology

## Advanced Features

**Clinical Scoring Systems:**
- PERC Score (Pulmonary Embolism Rule-out Criteria)
- Wells Score (DVT/PE probability)
- CURB-65 (Pneumonia severity)
- CHA2DS2-VASc (Stroke risk in AFib)
- Glasgow Coma Scale (Consciousness level)
- Centor Score (Strep throat probability)

**Risk-Adjusted Confidence Scoring:**
```
final_confidence = base_confidence × risk_multiplier × (1 + attribute_boost)

where:
- base_confidence: symptom matching (0.0-1.0)
- risk_multiplier: risk factor impact (1.0-1.5)
- attribute_boost: symptom attribute matching (0-0.20)
```

**Epidemiological Intelligence:**
- Seasonal patterns (96 factors): flu in winter, heat stroke in summer
- Geographic patterns (10 factors): malaria in tropics, altitude sickness in mountains

## Use Cases

- Diagnostic reasoning engine for symptom analysis
- Treatment protocol retrieval
- Safety validation (contraindications, interactions)
- Risk stratification (age, medical history)
- Clinical decision support
- Medical knowledge retrieval
- Reasoning transparency (explainable AI)

## Knowledge Graph Schema

**Core Relationships:**
- `(has-symptom condition symptom)`
- `(has-treatment condition treatment)`
- `(has-urgency condition level)`
- `(red-flag-symptom symptom)`
- `(contraindication treatment condition)`
- `(risk-factor condition factor multiplier)`
- `(treatment-protocol-step condition step priority timing)`
- `(symptom-attribute symptom attribute value)`
- `(seasonal-epidemiology condition season multiplier)`
- `(geographic-epidemiology condition location multiplier)`

## Integration

This agent powers:
- **Symptom Analysis Agent**: Diagnostic queries and risk assessment
- **Treatment Recommendation Agent**: Treatment protocols and safety validation
- **Coordinator Agent**: Knowledge retrieval orchestration

## Technical Details

- **Engine**: Hyperon MeTTa (Python interface)
- **Query Language**: MeTTa symbolic expressions
- **Reasoning**: Forward chaining, backward chaining, abduction
- **Performance**: <100ms average query time
- **Scalability**: 2,074 facts, extensible to 10,000+

## Example Queries

```metta
; Find all emergency conditions
!(match &self (has-urgency $cond emergency) $cond)

; Get symptoms for meningitis
!(match &self (has-symptom meningitis $symptom) $symptom)

; Find treatments for DKA
!(match &self (has-treatment diabetic-ketoacidosis $treatment) $treatment)

; Get risk factors for stroke with multipliers
!(match &self (risk-factor stroke $factor $multiplier) ($factor $multiplier))

; Get treatment protocol steps for anaphylaxis
!(match &self (treatment-protocol-step anaphylaxis $step $priority $timing)
    ($step $priority $timing))
```

## Evidence-Based Foundation

All medical facts sourced from:
- Centers for Disease Control and Prevention (CDC)
- World Health Organization (WHO)
- American Heart Association (AHA)
- Johns Hopkins Medicine
- Mayo Clinic
- UpToDate
- National Institutes of Health (NIH)
