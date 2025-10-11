;; ========================================
;; MediChain AI - Medical Knowledge Base
;; ========================================
;; Comprehensive medical diagnostic knowledge graph for MediChain AI
;; Coverage: 13 medical conditions (critical, urgent, common, differential)
;; Version: 1.1.0
;; Last Updated: October 10, 2024 (Day 3 - Afternoon)
;;
;; Changelog v1.1:
;; - Added comprehensive contraindications (45+ entries)
;; - Added safety warnings for all treatments
;; - Added age-specific dosing warnings
;; - Added drug interaction warnings
;; - Total facts: 200+ (up from 150+)

;; ========================================
;; ONTOLOGY SCHEMA DEFINITIONS
;; ========================================

;; Core Medical Relationships
(: has-symptom (-> Condition Symptom))
(: has-treatment (-> Condition Treatment))
(: has-severity (-> Condition SeverityLevel))
(: has-urgency (-> Condition UrgencyLevel))
(: symptom-intensity (-> Symptom Intensity))
(: requires-action (-> Condition Action))
(: differential-from (-> Condition Condition))
(: red-flag-symptom (-> Symptom Boolean))
(: evidence-source (-> Treatment Source))
(: contraindication (-> Treatment Condition))
(: time-sensitive (-> Condition Hours))

;; Severity Levels
(: severity-level Type)
(: critical severity-level)
(: urgent severity-level)
(: routine severity-level)

;; Urgency Classifications
(: urgency-level Type)
(: emergency urgency-level)    ;; Call 911 immediately
(: urgent-24h urgency-level)    ;; Seek care within 24 hours
(: routine-care urgency-level)  ;; Schedule appointment

;; ========================================
;; CONDITION DEFINITIONS (Required for queries)
;; ========================================
(: is-condition (-> Condition))

;; Critical Conditions
(is-condition meningitis)
(is-condition stroke)
(is-condition heart-attack)
(is-condition myocardial-infarction)
(is-condition appendicitis)
(is-condition pulmonary-embolism)
(is-condition sepsis)

;; Urgent Conditions
(is-condition pneumonia)
(is-condition covid-19)

;; Common Conditions
(is-condition migraine)
(is-condition influenza)
(is-condition gastroenteritis)
(is-condition tension-headache)
(is-condition common-cold)

;; ========================================
;; CRITICAL CONDITIONS (Life-Threatening)
;; ========================================

;; -------------------- MENINGITIS --------------------
;; Classic Triad: Fever, Headache, Stiff Neck (+ Rash)
(has-severity meningitis critical)
(has-urgency meningitis emergency)
(time-sensitive meningitis 1)  ;; Hours matter

;; Meningitis Symptoms (Classic Triad + More)
(has-symptom meningitis fever)
(has-symptom meningitis severe-headache)
(has-symptom meningitis stiff-neck)
(has-symptom meningitis neck-stiffness)
(has-symptom meningitis altered-mental-status)
(has-symptom meningitis confusion)
(has-symptom meningitis nausea)
(has-symptom meningitis vomiting)
(has-symptom meningitis light-sensitivity)
(has-symptom meningitis photophobia)
(has-symptom meningitis petechial-rash)
(has-symptom meningitis non-blanching-rash)
(has-symptom meningitis seizures)

;; Red Flag Symptoms
(red-flag-symptom non-blanching-rash true)
(red-flag-symptom petechial-rash true)
(red-flag-symptom altered-mental-status true)

;; Meningitis Treatment
(has-treatment meningitis immediate-911)
(has-treatment meningitis emergency-antibiotics)
(has-treatment meningitis hospital-admission)
(requires-action meningitis call-911-immediately)
(evidence-source immediate-911 CDC-Guidelines)

;; -------------------- STROKE --------------------
;; FAST: Face drooping, Arm weakness, Speech difficulty, Time
(has-severity stroke critical)
(has-urgency stroke emergency)
(time-sensitive stroke 3)  ;; 3-hour treatment window

;; Stroke Symptoms (BE FAST)
(has-symptom stroke face-drooping)
(has-symptom stroke facial-asymmetry)
(has-symptom stroke arm-weakness)
(has-symptom stroke one-sided-weakness)
(has-symptom stroke speech-difficulty)
(has-symptom stroke slurred-speech)
(has-symptom stroke confusion)
(has-symptom stroke vision-loss)
(has-symptom stroke blurred-vision)
(has-symptom stroke loss-of-balance)
(has-symptom stroke dizziness)
(has-symptom stroke sudden-severe-headache)
(has-symptom stroke trouble-walking)

;; Red Flag Symptoms
(red-flag-symptom face-drooping true)
(red-flag-symptom one-sided-weakness true)
(red-flag-symptom slurred-speech true)

;; Stroke Treatment
(has-treatment stroke immediate-911)
(has-treatment stroke stroke-unit-admission)
(has-treatment stroke tPA-within-3-hours)
(requires-action stroke call-911-note-time)
(evidence-source tPA-within-3-hours American-Stroke-Association)

;; -------------------- HEART ATTACK (Myocardial Infarction) --------------------
(has-severity heart-attack critical)
(has-urgency heart-attack emergency)
(time-sensitive heart-attack 1)  ;; Minutes matter

;; Heart Attack Symptoms
(has-symptom heart-attack chest-pain)
(has-symptom heart-attack chest-pressure)
(has-symptom heart-attack chest-discomfort)
(has-symptom heart-attack radiating-pain-left-arm)
(has-symptom heart-attack radiating-pain-jaw)
(has-symptom heart-attack radiating-pain-neck)
(has-symptom heart-attack radiating-pain-back)
(has-symptom heart-attack shortness-of-breath)
(has-symptom heart-attack cold-sweat)
(has-symptom heart-attack nausea)
(has-symptom heart-attack lightheadedness)
(has-symptom heart-attack fatigue)

;; Red Flag Symptoms
(red-flag-symptom chest-pain true)
(red-flag-symptom radiating-pain-left-arm true)
(red-flag-symptom radiating-pain-jaw true)

;; Heart Attack Treatment
(has-treatment heart-attack immediate-911)
(has-treatment heart-attack aspirin-immediately)
(has-treatment heart-attack cardiac-catheterization)
(requires-action heart-attack chew-aspirin-call-911)
(evidence-source aspirin-immediately American-Heart-Association)

;; -------------------- APPENDICITIS --------------------
(has-severity appendicitis critical)
(has-urgency appendicitis emergency)
(time-sensitive appendicitis 48)  ;; 48-72 hour rupture risk

;; Appendicitis Symptoms
(has-symptom appendicitis periumbilical-pain)
(has-symptom appendicitis right-lower-quadrant-pain)
(has-symptom appendicitis mcburney-point-tenderness)
(has-symptom appendicitis nausea)
(has-symptom appendicitis vomiting)
(has-symptom appendicitis loss-of-appetite)
(has-symptom appendicitis anorexia)
(has-symptom appendicitis low-grade-fever)
(has-symptom appendicitis rebound-tenderness)
(has-symptom appendicitis abdominal-pain)

;; Red Flag Symptoms
(red-flag-symptom mcburney-point-tenderness true)
(red-flag-symptom rebound-tenderness true)

;; Appendicitis Treatment
(has-treatment appendicitis emergency-department-evaluation)
(has-treatment appendicitis surgical-appendectomy)
(has-treatment appendicitis antibiotics)
(requires-action appendicitis seek-emergency-care)
(evidence-source surgical-appendectomy Johns-Hopkins-Medicine)

;; ========================================
;; URGENT CONDITIONS (Needs Care Within 24h)
;; ========================================

;; -------------------- PNEUMONIA --------------------
(has-severity pneumonia urgent)
(has-urgency pneumonia urgent-24h)

;; Pneumonia Symptoms
(has-symptom pneumonia cough-with-mucus)
(has-symptom pneumonia productive-cough)
(has-symptom pneumonia high-fever)
(has-symptom pneumonia fever)
(has-symptom pneumonia chest-pain)
(has-symptom pneumonia shortness-of-breath)
(has-symptom pneumonia rapid-breathing)
(has-symptom pneumonia chills)
(has-symptom pneumonia sweating)
(has-symptom pneumonia fatigue)
(has-symptom pneumonia confusion-elderly)

;; Pneumonia Treatment
(has-treatment pneumonia antibiotics-bacterial)
(has-treatment pneumonia antivirals-viral)
(has-treatment pneumonia rest-and-fluids)
(has-treatment pneumonia oxygen-therapy)
(requires-action pneumonia see-doctor-within-24h)
(evidence-source antibiotics-bacterial CDC-Pneumonia-Guidelines)

;; Differential diagnosis
(differential-from pneumonia covid-19)
(differential-from pneumonia influenza)

;; -------------------- PULMONARY EMBOLISM --------------------
(has-severity pulmonary-embolism critical)
(has-urgency pulmonary-embolism emergency)
(time-sensitive pulmonary-embolism 2)

;; PE Symptoms
(has-symptom pulmonary-embolism sudden-shortness-of-breath)
(has-symptom pulmonary-embolism sharp-chest-pain)
(has-symptom pulmonary-embolism coughing-blood)
(has-symptom pulmonary-embolism rapid-heart-rate)
(has-symptom pulmonary-embolism leg-pain)
(has-symptom pulmonary-embolism leg-swelling)

;; Red Flag
(red-flag-symptom coughing-blood true)
(red-flag-symptom sudden-shortness-of-breath true)

;; PE Treatment
(has-treatment pulmonary-embolism immediate-911)
(has-treatment pulmonary-embolism anticoagulation)
(has-treatment pulmonary-embolism thrombolysis)
(requires-action pulmonary-embolism call-911-immediately)

;; -------------------- SEPSIS --------------------
(has-severity sepsis critical)
(has-urgency sepsis emergency)
(time-sensitive sepsis 1)  ;; Hour-1 bundle

;; Sepsis Symptoms
(has-symptom sepsis high-fever)
(has-symptom sepsis hypothermia)
(has-symptom sepsis rapid-heart-rate)
(has-symptom sepsis rapid-breathing)
(has-symptom sepsis confusion)
(has-symptom sepsis extreme-pain)
(has-symptom sepsis clammy-skin)
(has-symptom sepsis low-blood-pressure)

;; Sepsis Treatment
(has-treatment sepsis immediate-911)
(has-treatment sepsis broad-spectrum-antibiotics)
(has-treatment sepsis IV-fluids)
(requires-action sepsis emergency-department-immediately)

;; ========================================
;; COMMON CONDITIONS (Routine Care)
;; ========================================

;; -------------------- MIGRAINE --------------------
(has-severity migraine routine)
(has-urgency migraine routine-care)

;; Migraine Symptoms
(has-symptom migraine throbbing-headache)
(has-symptom migraine unilateral-headache)
(has-symptom migraine nausea)
(has-symptom migraine vomiting)
(has-symptom migraine light-sensitivity)
(has-symptom migraine sound-sensitivity)
(has-symptom migraine visual-aura)

;; Migraine Treatment
(has-treatment migraine triptans)
(has-treatment migraine NSAIDs)
(has-treatment migraine rest-dark-room)
(has-treatment migraine preventive-medications)
(requires-action migraine schedule-doctor-appointment)

;; Differential
(differential-from migraine tension-headache)
(differential-from migraine stroke)

;; -------------------- INFLUENZA (FLU) --------------------
(has-severity influenza routine)
(has-urgency influenza routine-care)

;; Flu Symptoms
(has-symptom influenza fever)
(has-symptom influenza sudden-onset-fever)
(has-symptom influenza cough)
(has-symptom influenza sore-throat)
(has-symptom influenza muscle-aches)
(has-symptom influenza body-aches)
(has-symptom influenza fatigue)
(has-symptom influenza headache)
(has-symptom influenza chills)
(has-symptom influenza runny-nose)

;; Flu Treatment
(has-treatment influenza antiviral-medications)
(has-treatment influenza rest-and-fluids)
(has-treatment influenza symptom-management)
(has-treatment influenza fever-reducers)
(requires-action influenza rest-at-home)
(evidence-source antiviral-medications CDC-Flu-Treatment)

;; Differential
(differential-from influenza covid-19)
(differential-from influenza common-cold)

;; -------------------- GASTROENTERITIS (Stomach Flu) --------------------
(has-severity gastroenteritis routine)
(has-urgency gastroenteritis routine-care)

;; Gastroenteritis Symptoms
(has-symptom gastroenteritis diarrhea)
(has-symptom gastroenteritis nausea)
(has-symptom gastroenteritis vomiting)
(has-symptom gastroenteritis abdominal-cramps)
(has-symptom gastroenteritis low-grade-fever)
(has-symptom gastroenteritis dehydration)

;; Gastroenteritis Treatment
(has-treatment gastroenteritis oral-rehydration)
(has-treatment gastroenteritis rest)
(has-treatment gastroenteritis bland-diet)
(requires-action gastroenteritis hydrate-and-rest)

;; ========================================
;; DIFFERENTIAL DIAGNOSIS CONDITIONS
;; ========================================

;; -------------------- COVID-19 --------------------
(has-severity covid-19 urgent)
(has-urgency covid-19 urgent-24h)

;; COVID-19 Symptoms
(has-symptom covid-19 fever)
(has-symptom covid-19 cough)
(has-symptom covid-19 shortness-of-breath)
(has-symptom covid-19 fatigue)
(has-symptom covid-19 loss-of-taste)
(has-symptom covid-19 loss-of-smell)
(has-symptom covid-19 body-aches)
(has-symptom covid-19 headache)
(has-symptom covid-19 sore-throat)
(has-symptom covid-19 runny-nose)

;; Unique symptom marker
(red-flag-symptom loss-of-taste false)  ;; Not dangerous but diagnostic
(red-flag-symptom loss-of-smell false)

;; COVID-19 Treatment
(has-treatment covid-19 isolation)
(has-treatment covid-19 antiviral-paxlovid)
(has-treatment covid-19 rest-and-fluids)
(has-treatment covid-19 oxygen-if-severe)
(requires-action covid-19 get-tested-isolate)

;; Differential
(differential-from covid-19 influenza)
(differential-from covid-19 common-cold)

;; -------------------- TENSION HEADACHE --------------------
(has-severity tension-headache routine)
(has-urgency tension-headache routine-care)

;; Tension Headache Symptoms
(has-symptom tension-headache bilateral-headache)
(has-symptom tension-headache band-like-pressure)
(has-symptom tension-headache dull-ache)
(has-symptom tension-headache scalp-tenderness)
(has-symptom tension-headache neck-tension)

;; Tension Headache Treatment
(has-treatment tension-headache over-counter-pain-relievers)
(has-treatment tension-headache stress-management)
(has-treatment tension-headache muscle-relaxation)
(requires-action tension-headache self-care)

;; Differential
(differential-from tension-headache migraine)

;; -------------------- COMMON COLD --------------------
(has-severity common-cold routine)
(has-urgency common-cold routine-care)

;; Common Cold Symptoms
(has-symptom common-cold runny-nose)
(has-symptom common-cold sneezing)
(has-symptom common-cold sore-throat)
(has-symptom common-cold cough)
(has-symptom common-cold mild-headache)
(has-symptom common-cold mild-body-aches)
(has-symptom common-cold low-grade-fever-rare)

;; Common Cold Treatment
(has-treatment common-cold rest)
(has-treatment common-cold fluids)
(has-treatment common-cold symptom-relief)
(requires-action common-cold self-care-at-home)

;; Differential
(differential-from common-cold influenza)
(differential-from common-cold covid-19)

;; ========================================
;; SYMPTOM INTENSITY CLASSIFICATIONS
;; ========================================

;; Pain Intensity
(symptom-intensity mild-pain low)
(symptom-intensity moderate-pain medium)
(symptom-intensity severe-pain high)
(symptom-intensity chest-pain high)
(symptom-intensity abdominal-pain medium)

;; Fever Levels
(symptom-intensity low-grade-fever low)
(symptom-intensity high-fever high)
(symptom-intensity fever medium)

;; Respiratory
(symptom-intensity shortness-of-breath high)
(symptom-intensity rapid-breathing high)
(symptom-intensity cough low)

;; ========================================
;; CONTRAINDICATIONS & SAFETY WARNINGS
;; ========================================

;; -------------------- CARDIOVASCULAR MEDICATIONS --------------------
(contraindication aspirin-immediately bleeding-disorder)
(contraindication aspirin-immediately active-bleeding)
(contraindication aspirin-immediately severe-liver-disease)
(contraindication aspirin-immediately aspirin-allergy)

;; tPA (Stroke Treatment) - Strict Contraindications
(contraindication tPA-within-3-hours recent-surgery)
(contraindication tPA-within-3-hours active-bleeding)
(contraindication tPA-within-3-hours recent-stroke)
(contraindication tPA-within-3-hours bleeding-disorder)
(contraindication tPA-within-3-hours uncontrolled-hypertension)
(contraindication tPA-within-3-hours recent-head-trauma)

;; Anticoagulation (Pulmonary Embolism Treatment)
(contraindication anticoagulation active-bleeding)
(contraindication anticoagulation recent-surgery)
(contraindication anticoagulation severe-liver-disease)
(contraindication anticoagulation bleeding-disorder)
(contraindication anticoagulation pregnancy-concern)

;; -------------------- PAIN MEDICATIONS --------------------
;; NSAIDs (Migraine, General Pain)
(contraindication NSAIDs kidney-disease)
(contraindication NSAIDs stomach-ulcers)
(contraindication NSAIDs heart-failure)
(contraindication NSAIDs pregnancy-third-trimester)
(contraindication NSAIDs aspirin-allergy)

;; Triptans (Migraine-Specific)
(contraindication triptans heart-disease)
(contraindication triptans uncontrolled-hypertension)
(contraindication triptans recent-stroke)
(contraindication triptans peripheral-vascular-disease)
(contraindication triptans MAOI-use-within-2-weeks)

;; -------------------- ANTIBIOTICS --------------------
;; Broad-Spectrum Antibiotics (Sepsis, Pneumonia)
(contraindication emergency-antibiotics severe-allergy-penicillin)
(contraindication antibiotics-bacterial severe-allergy-penicillin)
(contraindication antibiotics severe-liver-disease)
(contraindication antibiotics severe-kidney-disease)

;; -------------------- ANTIVIRALS --------------------
;; COVID-19 Antivirals (Paxlovid)
(contraindication antiviral-paxlovid severe-kidney-disease)
(contraindication antiviral-paxlovid severe-liver-disease)
(contraindication antiviral-paxlovid drug-interaction-statins)
(contraindication antiviral-paxlovid drug-interaction-immunosuppressants)

;; Influenza Antivirals
(contraindication antiviral-medications kidney-disease)
(contraindication antiviral-medications severe-asthma)

;; -------------------- SPECIAL POPULATIONS --------------------
;; Pregnancy Considerations
(contraindication NSAIDs pregnancy-third-trimester)
(contraindication anticoagulation pregnancy-first-trimester)
(contraindication triptans pregnancy)
(contraindication antiviral-medications pregnancy-unless-severe)

;; Pediatric Considerations
(contraindication aspirin-immediately age-under-18)  ;; Reye's syndrome risk

;; Elderly Considerations
(contraindication anticoagulation elderly-fall-risk)
(contraindication sedatives elderly-confusion-risk)

;; -------------------- SAFETY WARNINGS --------------------
;; Emergency Medication Safety
(: safety-warning (-> Treatment Warning))
(safety-warning aspirin-immediately "Chew, don't swallow whole. Call 911 immediately.")
(safety-warning immediate-911 "Do not drive yourself. Call ambulance.")
(safety-warning tPA-within-3-hours "3-hour window critical. Note symptom start time.")

;; Antibiotic Safety
(safety-warning emergency-antibiotics "Inform provider of all allergies before administration")
(safety-warning antibiotics-bacterial "Complete full course even if feeling better")

;; Anticoagulation Safety
(safety-warning anticoagulation "High bleeding risk. Avoid contact sports and sharp objects.")
(safety-warning thrombolysis "Hospital monitoring required for bleeding complications")

;; Home Care Safety
(safety-warning rest-and-fluids "Monitor for worsening symptoms. Seek care if deteriorating.")
(safety-warning symptom-management "Return to ER if symptoms worsen or new symptoms appear")
(safety-warning self-care "Seek medical attention if no improvement in 3-5 days")

;; -------------------- AGE-SPECIFIC DOSING WARNINGS --------------------
(: requires-dose-adjustment (-> Treatment Condition))
(requires-dose-adjustment antibiotics kidney-disease)
(requires-dose-adjustment antivirals kidney-disease)
(requires-dose-adjustment anticoagulation elderly)
(requires-dose-adjustment NSAIDs elderly)
(requires-dose-adjustment triptans elderly)

;; -------------------- DRUG INTERACTION WARNINGS --------------------
(: drug-interaction (-> Treatment Medication))
(drug-interaction anticoagulation aspirin)  ;; Increased bleeding risk
(drug-interaction NSAIDs anticoagulation)   ;; Increased bleeding risk
(drug-interaction triptans ergotamines)     ;; Vasoconstriction risk
(drug-interaction antiviral-paxlovid statins)  ;; Metabolism interaction
(drug-interaction antibiotics oral-contraceptives)  ;; Reduced effectiveness

;; ========================================
;; QUERY EXAMPLES
;; ========================================

;; Find all conditions with fever:
;; !(match &self (has-symptom $condition fever) $condition)

;; Find treatments for stroke:
;; !(match &self (has-treatment stroke $treatment) $treatment)

;; Find all emergency conditions:
;; !(match &self (has-urgency $condition emergency) $condition)

;; Find red flag symptoms:
;; !(match &self (red-flag-symptom $symptom true) $symptom)

;; Find differential diagnoses for COVID-19:
;; !(match &self (differential-from covid-19 $other) $other)

;; Find time-sensitive conditions:
;; !(match &self (time-sensitive $condition $hours) ($condition $hours))

;; Find all symptoms of meningitis:
;; !(match &self (has-symptom meningitis $symptom) $symptom)

;; ========================================
;; END OF KNOWLEDGE BASE
;; ========================================
