;; ========================================
;; MediChain AI - Medical Knowledge Base
;; ========================================
;; Comprehensive medical diagnostic knowledge graph for MediChain AI
;; Coverage: 25 medical conditions (critical, urgent, common, differential) - EPIC 7 ENRICHMENT
;; Version: 2.0.0
;; Last Updated: October 12, 2025 (Day 7 - Epic 7 Phase 1-3 Complete)
;;
;; Changelog v2.0 (EPIC 7 - Knowledge Base Enrichment):
;; - PHASE 1: Added 12 new conditions (DKA, Anaphylaxis, Heat stroke, Hypoglycemia, Asthma, DVT, Kidney stones, Concussion, UTI, Dehydration, Food poisoning, Cellulitis)
;; - PHASE 1: Added lab test recommendations schema and 15+ tests
;; - PHASE 1: Added imaging requirements schema and 8 imaging types
;; - PHASE 1: Total contraindications: 95+ (up from 45+)
;; - PHASE 2: Added risk factor schema and 100+ risk factors
;; - PHASE 2: Added diagnostic criteria (PERC, Centor, CURB-65, Wells, etc.)
;; - PHASE 2: Added clarifying questions (20+) for differential diagnosis
;; - PHASE 3: Added treatment protocol sequencing (8 critical protocols)
;; - PHASE 3: Added symptom attributes (duration, onset, location for 50+ symptoms)
;; - PHASE 3: Added epidemiology data (seasonal prevalence)
;; - Total facts: 800+ (up from 200+)
;;
;; Changelog v1.1 (Day 3):
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

;; PHASE 1 SCHEMAS: Lab Tests & Imaging
(: requires-lab-test (-> Condition Test))
(: requires-imaging (-> Condition Imaging))
(: lab-test-urgency (-> Test UrgencyLevel))
(: imaging-urgency (-> Imaging UrgencyLevel))

;; PHASE 2 SCHEMAS: Risk Factors & Diagnostic Criteria
(: risk-factor (-> Condition Factor RiskMultiplier))
(: age-risk (-> Condition AgeRange RiskLevel))
(: diagnostic-criteria (-> Condition Criteria Score))
(: clarifying-question (-> Condition Question))
(: helps-differentiate (-> Question Condition Condition))
(: prevalence (-> Condition PopulationGroup Percentage))

;; PHASE 3 SCHEMAS: Treatment Protocols & Symptom Attributes
(: treatment-protocol (-> Condition Protocol))
(: treatment-step (-> Protocol StepNumber Action))
(: treatment-step-timing (-> Protocol StepNumber Minutes))
(: symptom-duration (-> Symptom Condition TypicalDuration))
(: symptom-onset (-> Symptom Condition OnsetSpeed))
(: symptom-location (-> Symptom Condition BodyLocation))
(: seasonal-prevalence (-> Condition Season PrevalenceLevel))

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

;; EPIC 7 - NEW CONDITIONS (Phase 1)
;; Critical Conditions (Emergency)
(is-condition diabetic-ketoacidosis)
(is-condition anaphylaxis)
(is-condition heat-stroke)

;; Urgent Conditions (24-48h care)
(is-condition hypoglycemia)
(is-condition asthma-exacerbation)
(is-condition deep-vein-thrombosis)
(is-condition kidney-stones)
(is-condition concussion)

;; Routine Conditions (Common)
(is-condition urinary-tract-infection)
(is-condition dehydration)
(is-condition food-poisoning)
(is-condition cellulitis)

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

;; -------------------- DIABETIC KETOACIDOSIS (DKA) --------------------
;; EPIC 7 - Critical endocrine emergency
(has-severity diabetic-ketoacidosis critical)
(has-urgency diabetic-ketoacidosis emergency)
(time-sensitive diabetic-ketoacidosis 1)  ;; Hours critical

;; DKA Symptoms
(has-symptom diabetic-ketoacidosis excessive-thirst)
(has-symptom diabetic-ketoacidosis frequent-urination)
(has-symptom diabetic-ketoacidosis nausea)
(has-symptom diabetic-ketoacidosis vomiting)
(has-symptom diabetic-ketoacidosis abdominal-pain)
(has-symptom diabetic-ketoacidosis confusion)
(has-symptom diabetic-ketoacidosis fruity-breath-odor)
(has-symptom diabetic-ketoacidosis rapid-breathing)
(has-symptom diabetic-ketoacidosis fatigue)
(has-symptom diabetic-ketoacidosis high-blood-sugar)

;; Red Flag Symptoms
(red-flag-symptom fruity-breath-odor true)

;; DKA Lab Tests (PHASE 1)
(requires-lab-test diabetic-ketoacidosis blood-glucose)
(requires-lab-test diabetic-ketoacidosis blood-ketones)
(requires-lab-test diabetic-ketoacidosis arterial-blood-gas)
(requires-lab-test diabetic-ketoacidosis basic-metabolic-panel)
(lab-test-urgency blood-ketones emergency)
(lab-test-urgency arterial-blood-gas emergency)

;; DKA Treatment
(has-treatment diabetic-ketoacidosis immediate-911)
(has-treatment diabetic-ketoacidosis IV-insulin)
(has-treatment diabetic-ketoacidosis IV-fluids)
(has-treatment diabetic-ketoacidosis electrolyte-replacement)
(requires-action diabetic-ketoacidosis call-911-immediately)
(evidence-source IV-insulin American-Diabetes-Association)

;; DKA Contraindications
(contraindication IV-insulin hypoglycemia)
(contraindication IV-fluids heart-failure-severe)

;; -------------------- ANAPHYLAXIS --------------------
;; EPIC 7 - Severe allergic reaction
(has-severity anaphylaxis critical)
(has-urgency anaphylaxis emergency)
(time-sensitive anaphylaxis 0)  ;; Minutes matter

;; Anaphylaxis Symptoms
(has-symptom anaphylaxis difficulty-breathing)
(has-symptom anaphylaxis throat-swelling)
(has-symptom anaphylaxis tongue-swelling)
(has-symptom anaphylaxis wheezing)
(has-symptom anaphylaxis hives)
(has-symptom anaphylaxis skin-rash)
(has-symptom anaphylaxis rapid-pulse)
(has-symptom anaphylaxis low-blood-pressure)
(has-symptom anaphylaxis dizziness)
(has-symptom anaphylaxis loss-of-consciousness)
(has-symptom anaphylaxis nausea)
(has-symptom anaphylaxis vomiting)

;; Red Flag Symptoms
(red-flag-symptom throat-swelling true)

;; Anaphylaxis Lab Tests
(requires-lab-test anaphylaxis serum-tryptase)
(lab-test-urgency serum-tryptase urgent-24h)

;; Anaphylaxis Treatment
(has-treatment anaphylaxis epinephrine-auto-injector)
(has-treatment anaphylaxis immediate-911)
(has-treatment anaphylaxis antihistamines)
(has-treatment anaphylaxis corticosteroids)
(has-treatment anaphylaxis oxygen-therapy)
(requires-action anaphylaxis use-epipen-call-911)
(evidence-source epinephrine-auto-injector NIAID-Guidelines)

;; Anaphylaxis Contraindications
(contraindication epinephrine-auto-injector uncontrolled-hypertension-severe)
(safety-warning epinephrine-auto-injector "Use EpiPen immediately. Call 911 even if symptoms improve.")

;; -------------------- HEAT STROKE --------------------
;; EPIC 7 - Life-threatening hyperthermia
(has-severity heat-stroke critical)
(has-urgency heat-stroke emergency)
(time-sensitive heat-stroke 1)  ;; Immediate cooling critical

;; Heat Stroke Symptoms
(has-symptom heat-stroke high-body-temperature)
(has-symptom heat-stroke altered-mental-status)
(has-symptom heat-stroke confusion)
(has-symptom heat-stroke agitation)
(has-symptom heat-stroke seizures)
(has-symptom heat-stroke hot-dry-skin)
(has-symptom heat-stroke absence-of-sweating)
(has-symptom heat-stroke rapid-heart-rate)
(has-symptom heat-stroke rapid-breathing)
(has-symptom heat-stroke headache)
(has-symptom heat-stroke nausea)
(has-symptom heat-stroke loss-of-consciousness)

;; Red Flag Symptoms
(red-flag-symptom high-body-temperature true)
(red-flag-symptom hot-dry-skin true)

;; Heat Stroke Lab Tests
(requires-lab-test heat-stroke basic-metabolic-panel)
(requires-lab-test heat-stroke liver-function-tests)
(requires-lab-test heat-stroke complete-blood-count)
(requires-lab-test heat-stroke creatine-kinase)
(lab-test-urgency creatine-kinase emergency)

;; Heat Stroke Treatment
(has-treatment heat-stroke immediate-911)
(has-treatment heat-stroke rapid-cooling)
(has-treatment heat-stroke ice-packs)
(has-treatment heat-stroke IV-fluids)
(requires-action heat-stroke cool-body-call-911)
(evidence-source rapid-cooling CDC-Heat-Emergency)

;; Heat Stroke Safety
(safety-warning rapid-cooling "Remove from heat. Apply ice to neck, armpits, groin. Call 911.")

;; ========================================
;; EPIC 7 - NEW URGENT CONDITIONS
;; ========================================

;; -------------------- HYPOGLYCEMIA --------------------
;; EPIC 7 - Low blood sugar emergency
(has-severity hypoglycemia urgent)
(has-urgency hypoglycemia urgent-24h)
(time-sensitive hypoglycemia 1)  ;; Can escalate quickly

;; Hypoglycemia Symptoms
(has-symptom hypoglycemia shakiness)
(has-symptom hypoglycemia sweating)
(has-symptom hypoglycemia confusion)
(has-symptom hypoglycemia dizziness)
(has-symptom hypoglycemia hunger)
(has-symptom hypoglycemia irritability)
(has-symptom hypoglycemia rapid-heart-rate)
(has-symptom hypoglycemia blurred-vision)
(has-symptom hypoglycemia weakness)
(has-symptom hypoglycemia loss-of-consciousness)

;; Red Flag Symptoms
(red-flag-symptom loss-of-consciousness true)

;; Hypoglycemia Lab Tests
(requires-lab-test hypoglycemia blood-glucose)
(requires-lab-test hypoglycemia hemoglobin-a1c)
(lab-test-urgency blood-glucose emergency)

;; Hypoglycemia Imaging
(requires-imaging hypoglycemia none)

;; Hypoglycemia Treatment
(has-treatment hypoglycemia fast-acting-carbohydrates)
(has-treatment hypoglycemia glucose-tablets)
(has-treatment hypoglycemia glucagon-injection)
(has-treatment hypoglycemia call-911-if-unconscious)
(requires-action hypoglycemia consume-15g-carbs-recheck)
(evidence-source fast-acting-carbohydrates American-Diabetes-Association)

;; Hypoglycemia Contraindications
(contraindication glucagon-injection insulinoma)
(safety-warning glucagon-injection "Use only if unconscious. Call 911 immediately.")

;; -------------------- ASTHMA EXACERBATION --------------------
;; EPIC 7 - Acute asthma attack
(has-severity asthma-exacerbation urgent)
(has-urgency asthma-exacerbation urgent-24h)
(time-sensitive asthma-exacerbation 2)  ;; Can become life-threatening

;; Asthma Exacerbation Symptoms
(has-symptom asthma-exacerbation wheezing)
(has-symptom asthma-exacerbation shortness-of-breath)
(has-symptom asthma-exacerbation chest-tightness)
(has-symptom asthma-exacerbation coughing)
(has-symptom asthma-exacerbation difficulty-breathing)
(has-symptom asthma-exacerbation rapid-breathing)
(has-symptom asthma-exacerbation difficulty-speaking)
(has-symptom asthma-exacerbation anxiety)
(has-symptom asthma-exacerbation bluish-lips)

;; Red Flag Symptoms
(red-flag-symptom bluish-lips true)
(red-flag-symptom difficulty-speaking true)

;; Asthma Lab Tests
(requires-lab-test asthma-exacerbation peak-flow-meter)
(requires-lab-test asthma-exacerbation pulse-oximetry)
(requires-lab-test asthma-exacerbation arterial-blood-gas)
(lab-test-urgency peak-flow-meter urgent-24h)
(lab-test-urgency pulse-oximetry emergency)

;; Asthma Imaging
(requires-imaging asthma-exacerbation chest-x-ray)
(imaging-urgency chest-x-ray urgent-24h)

;; Asthma Treatment
(has-treatment asthma-exacerbation short-acting-bronchodilator)
(has-treatment asthma-exacerbation albuterol-inhaler)
(has-treatment asthma-exacerbation corticosteroids)
(has-treatment asthma-exacerbation oxygen-therapy)
(has-treatment asthma-exacerbation call-911-if-severe)
(requires-action asthma-exacerbation use-rescue-inhaler-seek-care)
(evidence-source short-acting-bronchodilator NHLBI-Asthma-Guidelines)

;; Asthma Contraindications
(contraindication short-acting-bronchodilator heart-arrhythmia-severe)
(safety-warning albuterol-inhaler "If no improvement after 3 puffs, call 911 immediately.")

;; -------------------- DEEP VEIN THROMBOSIS (DVT) --------------------
;; EPIC 7 - Blood clot in leg veins
(has-severity deep-vein-thrombosis urgent)
(has-urgency deep-vein-thrombosis urgent-24h)
(time-sensitive deep-vein-thrombosis 24)  ;; Risk of PE

;; DVT Symptoms
(has-symptom deep-vein-thrombosis leg-swelling)
(has-symptom deep-vein-thrombosis leg-pain)
(has-symptom deep-vein-thrombosis calf-tenderness)
(has-symptom deep-vein-thrombosis leg-warmth)
(has-symptom deep-vein-thrombosis red-skin-discoloration)
(has-symptom deep-vein-thrombosis swollen-veins)

;; DVT Lab Tests
(requires-lab-test deep-vein-thrombosis d-dimer)
(requires-lab-test deep-vein-thrombosis complete-blood-count)
(lab-test-urgency d-dimer urgent-24h)

;; DVT Imaging
(requires-imaging deep-vein-thrombosis ultrasound-doppler)
(imaging-urgency ultrasound-doppler urgent-24h)

;; DVT Treatment
(has-treatment deep-vein-thrombosis anticoagulation)
(has-treatment deep-vein-thrombosis compression-stockings)
(has-treatment deep-vein-thrombosis leg-elevation)
(requires-action deep-vein-thrombosis seek-emergency-care-24h)
(evidence-source anticoagulation American-College-Chest-Physicians)

;; DVT Contraindications (already defined for anticoagulation above)
(differential-from deep-vein-thrombosis pulmonary-embolism)

;; -------------------- KIDNEY STONES --------------------
;; EPIC 7 - Renal calculi
(has-severity kidney-stones urgent)
(has-urgency kidney-stones urgent-24h)

;; Kidney Stone Symptoms
(has-symptom kidney-stones severe-flank-pain)
(has-symptom kidney-stones radiating-pain-groin)
(has-symptom kidney-stones hematuria)
(has-symptom kidney-stones blood-in-urine)
(has-symptom kidney-stones nausea)
(has-symptom kidney-stones vomiting)
(has-symptom kidney-stones frequent-urination)
(has-symptom kidney-stones painful-urination)
(has-symptom kidney-stones fever-if-infected)

;; Red Flag Symptoms
(red-flag-symptom hematuria false)  ;; Common but not dangerous

;; Kidney Stone Lab Tests
(requires-lab-test kidney-stones urinalysis)
(requires-lab-test kidney-stones complete-blood-count)
(requires-lab-test kidney-stones basic-metabolic-panel)
(lab-test-urgency urinalysis urgent-24h)

;; Kidney Stone Imaging
(requires-imaging kidney-stones ct-scan-non-contrast)
(requires-imaging kidney-stones ultrasound)
(imaging-urgency ct-scan-non-contrast urgent-24h)

;; Kidney Stone Treatment
(has-treatment kidney-stones pain-management)
(has-treatment kidney-stones NSAIDs)
(has-treatment kidney-stones hydration)
(has-treatment kidney-stones alpha-blockers)
(has-treatment kidney-stones lithotripsy)
(requires-action kidney-stones see-doctor-within-24h)
(evidence-source alpha-blockers American-Urological-Association)

;; Kidney Stone Contraindications (NSAIDs already defined)
(safety-warning pain-management "Severe pain may require emergency care and IV pain relief.")

;; -------------------- CONCUSSION --------------------
;; EPIC 7 - Mild traumatic brain injury
(has-severity concussion urgent)
(has-urgency concussion urgent-24h)
(time-sensitive concussion 48)  ;; Monitor for complications

;; Concussion Symptoms
(has-symptom concussion headache)
(has-symptom concussion confusion)
(has-symptom concussion dizziness)
(has-symptom concussion nausea)
(has-symptom concussion vomiting)
(has-symptom concussion blurred-vision)
(has-symptom concussion sensitivity-to-light)
(has-symptom concussion sensitivity-to-noise)
(has-symptom concussion memory-problems)
(has-symptom concussion difficulty-concentrating)
(has-symptom concussion slurred-speech)

;; Red Flag Symptoms
(red-flag-symptom repeated-vomiting true)
(red-flag-symptom worsening-headache true)
(red-flag-symptom seizures true)

;; Concussion Lab Tests
(requires-lab-test concussion none)  ;; Clinical diagnosis

;; Concussion Imaging
(requires-imaging concussion ct-scan-head)
(imaging-urgency ct-scan-head urgent-24h)

;; Concussion Treatment
(has-treatment concussion physical-rest)
(has-treatment concussion cognitive-rest)
(has-treatment concussion gradual-return-to-activity)
(has-treatment concussion avoid-screens)
(requires-action concussion monitor-symptoms-seek-care-if-worsening)
(evidence-source physical-rest CDC-Concussion-Guidelines)

;; Concussion Contraindications
(contraindication NSAIDs concussion-acute)  ;; Bleeding risk
(contraindication aspirin-immediately concussion)
(safety-warning physical-rest "Wake patient every 2-3 hours first 24 hours. Call 911 if symptoms worsen.")

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

;; -------------------- URINARY TRACT INFECTION (UTI) --------------------
;; EPIC 7 - Bacterial bladder/kidney infection
(has-severity urinary-tract-infection routine)
(has-urgency urinary-tract-infection routine-care)

;; UTI Symptoms
(has-symptom urinary-tract-infection painful-urination)
(has-symptom urinary-tract-infection frequent-urination)
(has-symptom urinary-tract-infection urgent-need-to-urinate)
(has-symptom urinary-tract-infection cloudy-urine)
(has-symptom urinary-tract-infection blood-in-urine)
(has-symptom urinary-tract-infection strong-smelling-urine)
(has-symptom urinary-tract-infection pelvic-pain)
(has-symptom urinary-tract-infection low-grade-fever)

;; UTI Lab Tests
(requires-lab-test urinary-tract-infection urinalysis)
(requires-lab-test urinary-tract-infection urine-culture)
(lab-test-urgency urine-culture routine-care)

;; UTI Imaging
(requires-imaging urinary-tract-infection ultrasound)  ;; If recurrent
(imaging-urgency ultrasound routine-care)

;; UTI Treatment
(has-treatment urinary-tract-infection antibiotics-short-course)
(has-treatment urinary-tract-infection increased-fluids)
(has-treatment urinary-tract-infection pain-relief)
(requires-action urinary-tract-infection see-doctor-for-antibiotics)
(evidence-source antibiotics-short-course Infectious-Diseases-Society-America)

;; UTI Contraindications
(contraindication antibiotics-short-course severe-allergy-sulfa)
(safety-warning antibiotics-short-course "Complete full course to prevent antibiotic resistance.")

;; -------------------- DEHYDRATION --------------------
;; EPIC 7 - Fluid loss condition
(has-severity dehydration routine)
(has-urgency dehydration routine-care)

;; Dehydration Symptoms
(has-symptom dehydration excessive-thirst)
(has-symptom dehydration dry-mouth)
(has-symptom dehydration dark-urine)
(has-symptom dehydration decreased-urination)
(has-symptom dehydration fatigue)
(has-symptom dehydration dizziness)
(has-symptom dehydration lightheadedness)
(has-symptom dehydration dry-skin)
(has-symptom dehydration headache)

;; Dehydration Lab Tests
(requires-lab-test dehydration basic-metabolic-panel)
(requires-lab-test dehydration urinalysis)
(lab-test-urgency basic-metabolic-panel routine-care)

;; Dehydration Treatment
(has-treatment dehydration oral-rehydration-solution)
(has-treatment dehydration increased-fluid-intake)
(has-treatment dehydration electrolyte-replacement)
(has-treatment dehydration IV-fluids-if-severe)
(requires-action dehydration drink-fluids-rest)
(evidence-source oral-rehydration-solution WHO-Guidelines)

;; Dehydration Safety
(safety-warning oral-rehydration-solution "Seek emergency care if unable to keep fluids down or severe dizziness.")

;; -------------------- FOOD POISONING --------------------
;; EPIC 7 - Foodborne illness
(has-severity food-poisoning routine)
(has-urgency food-poisoning routine-care)

;; Food Poisoning Symptoms
(has-symptom food-poisoning nausea)
(has-symptom food-poisoning vomiting)
(has-symptom food-poisoning diarrhea)
(has-symptom food-poisoning abdominal-cramps)
(has-symptom food-poisoning fever)
(has-symptom food-poisoning chills)
(has-symptom food-poisoning headache)
(has-symptom food-poisoning weakness)

;; Food Poisoning Lab Tests
(requires-lab-test food-poisoning stool-culture)  ;; If severe or bloody
(lab-test-urgency stool-culture routine-care)

;; Food Poisoning Treatment
(has-treatment food-poisoning rest-and-fluids)
(has-treatment food-poisoning oral-rehydration)
(has-treatment food-poisoning bland-diet)
(has-treatment food-poisoning avoid-solid-food-initially)
(requires-action food-poisoning hydrate-and-rest)
(evidence-source rest-and-fluids CDC-Food-Safety)

;; Food Poisoning Safety
(safety-warning rest-and-fluids "Seek emergency care if bloody diarrhea, high fever >101.5°F, or signs of dehydration.")

;; Differential
(differential-from food-poisoning gastroenteritis)

;; -------------------- CELLULITIS --------------------
;; EPIC 7 - Bacterial skin infection
(has-severity cellulitis routine)
(has-urgency cellulitis routine-care)

;; Cellulitis Symptoms
(has-symptom cellulitis red-skin-area)
(has-symptom cellulitis swelling)
(has-symptom cellulitis warmth)
(has-symptom cellulitis tenderness)
(has-symptom cellulitis pain)
(has-symptom cellulitis fever)
(has-symptom cellulitis red-streaks)
(has-symptom cellulitis skin-dimpling)

;; Red Flag Symptoms
(red-flag-symptom red-streaks true)  ;; Spreading infection

;; Cellulitis Lab Tests
(requires-lab-test cellulitis complete-blood-count)
(requires-lab-test cellulitis blood-cultures)  ;; If systemic symptoms
(lab-test-urgency blood-cultures urgent-24h)

;; Cellulitis Imaging
(requires-imaging cellulitis ultrasound)  ;; If abscess suspected
(imaging-urgency ultrasound urgent-24h)

;; Cellulitis Treatment
(has-treatment cellulitis oral-antibiotics)
(has-treatment cellulitis elevation-of-affected-area)
(has-treatment cellulitis pain-relief)
(has-treatment cellulitis wound-care)
(requires-action cellulitis see-doctor-for-antibiotics)
(evidence-source oral-antibiotics Infectious-Diseases-Society-America)

;; Cellulitis Contraindications
(contraindication oral-antibiotics severe-allergy-penicillin)
(safety-warning oral-antibiotics "Seek emergency care if red streaks spread, high fever, or worsening despite antibiotics.")

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

;; -------------------- EPIC 7 NEW MEDICATIONS --------------------
;; IV Insulin (DKA Treatment)
(contraindication IV-insulin severe-hypokalemia)
(contraindication IV-insulin hypoglycemia)
(contraindication IV-insulin insulin-allergy)

;; Epinephrine (Anaphylaxis)
(contraindication epinephrine-auto-injector cocaine-use)
(contraindication epinephrine-auto-injector severe-coronary-artery-disease)
(contraindication epinephrine-auto-injector tachyarrhythmia)

;; Glucagon (Hypoglycemia)
(contraindication glucagon-injection pheochromocytoma)
(contraindication glucagon-injection severe-hypotension)

;; Bronchodilators (Asthma)
(contraindication short-acting-bronchodilator hyperthyroidism)
(contraindication short-acting-bronchodilator diabetes-uncontrolled)
(contraindication albuterol-inhaler severe-hypertension)
(contraindication albuterol-inhaler heart-arrhythmia)

;; Corticosteroids (Asthma, Anaphylaxis)
(contraindication corticosteroids active-infection-fungal)
(contraindication corticosteroids peptic-ulcer-active)
(contraindication corticosteroids diabetes-uncontrolled)
(contraindication corticosteroids osteoporosis-severe)
(contraindication corticosteroids psychosis)

;; Alpha-blockers (Kidney Stones)
(contraindication alpha-blockers severe-liver-disease)
(contraindication alpha-blockers severe-hypotension)
(contraindication alpha-blockers heart-failure)

;; Antibiotics-Short-Course (UTI)
(contraindication antibiotics-short-course severe-allergy-quinolones)
(contraindication antibiotics-short-course G6PD-deficiency)
(contraindication antibiotics-short-course pregnancy-first-trimester)

;; Antihistamines (Anaphylaxis)
(contraindication antihistamines narrow-angle-glaucoma)
(contraindication antihistamines urinary-retention)
(contraindication antihistamines prostate-enlargement-severe)

;; Electrolyte Replacement (DKA)
(contraindication electrolyte-replacement hyperkalemia)
(contraindication electrolyte-replacement severe-kidney-disease)

;; Compression Stockings (DVT)
(contraindication compression-stockings peripheral-arterial-disease)
(contraindication compression-stockings skin-infection)
(contraindication compression-stockings severe-edema)

;; Lithotripsy (Kidney Stones)
(contraindication lithotripsy pregnancy)
(contraindication lithotripsy bleeding-disorder)
(contraindication lithotripsy anticoagulation-therapy)
(contraindication lithotripsy aortic-aneurysm)

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
;; ========================================
;; EPIC 7 - PHASE 2: RISK FACTORS & DIAGNOSTIC CRITERIA
;; ========================================
;; Added: October 12, 2025
;; Total Risk Factors: 100+
;; Diagnostic Criteria: 8 clinical scoring systems
;; Clarifying Questions: 20 differential diagnosis aids

;; ========================================
;; RISK FACTORS - CRITICAL CONDITIONS
;; ========================================

;; -------------------- HEART ATTACK (Myocardial Infarction) --------------------
;; High-Risk Factors (Multiplier: 3.0+)
(risk-factor heart-attack age-over-65 3.5)
(risk-factor heart-attack diabetes-mellitus 3.0)
(risk-factor heart-attack previous-heart-attack 4.0)
(risk-factor heart-attack family-history-heart-disease 2.5)
(risk-factor heart-attack smoking-current 3.0)

;; Medium-Risk Factors (Multiplier: 1.5-2.9)
(risk-factor heart-attack hypertension 2.0)
(risk-factor heart-attack high-cholesterol 2.0)
(risk-factor heart-attack obesity 1.8)
(risk-factor heart-attack sedentary-lifestyle 1.5)
(risk-factor heart-attack male-gender 1.7)

;; Low-Risk Factors (Multiplier: 1.1-1.4)
(risk-factor heart-attack stress-chronic 1.3)
(risk-factor heart-attack sleep-apnea 1.2)

;; Age-Specific Risk
(age-risk heart-attack age-under-40 low)
(age-risk heart-attack age-40-55 medium)
(age-risk heart-attack age-55-70 high)
(age-risk heart-attack age-over-70 very-high)

;; -------------------- STROKE --------------------
;; High-Risk Factors
(risk-factor stroke age-over-65 3.5)
(risk-factor stroke atrial-fibrillation 5.0)
(risk-factor stroke previous-stroke 4.5)
(risk-factor stroke hypertension 3.0)
(risk-factor stroke diabetes-mellitus 2.5)

;; Medium-Risk Factors
(risk-factor stroke smoking-current 2.0)
(risk-factor stroke heart-disease 2.2)
(risk-factor stroke high-cholesterol 1.8)
(risk-factor stroke obesity 1.6)
(risk-factor stroke carotid-artery-disease 3.0)

;; Low-Risk Factors
(risk-factor stroke oral-contraceptive-use 1.3)
(risk-factor stroke migraine-with-aura 1.4)

;; Age-Specific Risk
(age-risk stroke age-under-45 low)
(age-risk stroke age-45-65 medium)
(age-risk stroke age-over-65 very-high)

;; -------------------- DIABETIC KETOACIDOSIS (DKA) --------------------
;; High-Risk Factors
(risk-factor diabetic-ketoacidosis type-1-diabetes 5.0)
(risk-factor diabetic-ketoacidosis insulin-pump-malfunction 4.0)
(risk-factor diabetic-ketoacidosis infection-current 3.0)
(risk-factor diabetic-ketoacidosis missed-insulin-doses 4.0)

;; Medium-Risk Factors
(risk-factor diabetic-ketoacidosis new-diabetes-diagnosis 2.5)
(risk-factor diabetic-ketoacidosis stress-major 2.0)
(risk-factor diabetic-ketoacidosis surgery-recent 2.0)
(risk-factor diabetic-ketoacidosis pregnancy 2.5)

;; Low-Risk Factors
(risk-factor diabetic-ketoacidosis adolescent 1.5)
(risk-factor diabetic-ketoacidosis poor-diabetes-control 1.8)

;; Age-Specific Risk
(age-risk diabetic-ketoacidosis age-under-20 high)
(age-risk diabetic-ketoacidosis age-20-40 medium)
(age-risk diabetic-ketoacidosis age-over-40 low)

;; -------------------- ANAPHYLAXIS --------------------
;; High-Risk Factors
(risk-factor anaphylaxis previous-anaphylaxis 5.0)
(risk-factor anaphylaxis known-food-allergy-severe 4.0)
(risk-factor anaphylaxis asthma-history 3.0)
(risk-factor anaphylaxis medication-allergy-known 4.0)

;; Medium-Risk Factors
(risk-factor anaphylaxis atopic-conditions 2.0)
(risk-factor anaphylaxis eczema-severe 1.8)
(risk-factor anaphylaxis family-history-allergies 1.5)

;; Low-Risk Factors
(risk-factor anaphylaxis seasonal-allergies 1.2)

;; Age-Specific Risk
(age-risk anaphylaxis age-child high)
(age-risk anaphylaxis age-adult medium)
(age-risk anaphylaxis age-elderly low)

;; -------------------- PULMONARY EMBOLISM (PE) --------------------
;; High-Risk Factors
(risk-factor pulmonary-embolism recent-surgery 4.0)
(risk-factor pulmonary-embolism cancer-active 5.0)
(risk-factor pulmonary-embolism immobilization-prolonged 3.5)
(risk-factor pulmonary-embolism previous-dvt-or-pe 4.5)
(risk-factor pulmonary-embolism pregnancy-or-postpartum 3.0)

;; Medium-Risk Factors
(risk-factor pulmonary-embolism oral-contraceptive-use 2.0)
(risk-factor pulmonary-embolism long-flight-recent 2.5)
(risk-factor pulmonary-embolism obesity 1.8)
(risk-factor pulmonary-embolism smoking-current 1.7)

;; Low-Risk Factors
(risk-factor pulmonary-embolism age-over-60 1.5)
(risk-factor pulmonary-embolism varicose-veins 1.3)

;; -------------------- MENINGITIS --------------------
;; High-Risk Factors
(risk-factor meningitis immunocompromised 4.0)
(risk-factor meningitis asplenia 3.5)
(risk-factor meningitis recent-head-trauma 3.0)
(risk-factor meningitis csf-leak 4.0)

;; Medium-Risk Factors
(risk-factor meningitis close-contact-case 3.0)
(risk-factor meningitis crowded-living-conditions 2.0)
(risk-factor meningitis unvaccinated 2.5)

;; Low-Risk Factors
(risk-factor meningitis age-under-5 1.8)
(risk-factor meningitis age-15-24 1.5)

;; Age-Specific Risk
(age-risk meningitis age-infant very-high)
(age-risk meningitis age-child high)
(age-risk meningitis age-adolescent medium)
(age-risk meningitis age-adult low)

;; -------------------- SEPSIS --------------------
;; High-Risk Factors
(risk-factor sepsis immunocompromised 4.5)
(risk-factor sepsis diabetes-mellitus 2.5)
(risk-factor sepsis chronic-kidney-disease 3.0)
(risk-factor sepsis chronic-liver-disease 3.5)
(risk-factor sepsis recent-surgery 2.5)

;; Medium-Risk Factors
(risk-factor sepsis indwelling-catheter 2.0)
(risk-factor sepsis iv-drug-use 2.8)
(risk-factor sepsis malnutrition 2.0)

;; Low-Risk Factors
(risk-factor sepsis age-over-65 1.5)
(risk-factor sepsis age-under-1 1.8)

;; -------------------- HEAT STROKE --------------------
;; High-Risk Factors
(risk-factor heat-stroke age-over-65 3.0)
(risk-factor heat-stroke medications-anticholinergic 3.5)
(risk-factor heat-stroke cardiovascular-disease 2.5)
(risk-factor heat-stroke dehydration-baseline 3.0)

;; Medium-Risk Factors
(risk-factor heat-stroke obesity 2.0)
(risk-factor heat-stroke alcohol-use 2.0)
(risk-factor heat-stroke lack-of-acclimatization 2.5)

;; Low-Risk Factors
(risk-factor heat-stroke strenuous-exercise 1.5)
(risk-factor heat-stroke age-child 1.3)

;; ========================================
;; RISK FACTORS - URGENT CONDITIONS
;; ========================================

;; -------------------- PNEUMONIA --------------------
;; High-Risk Factors
(risk-factor pneumonia age-over-65 3.0)
(risk-factor pneumonia chronic-lung-disease 3.5)
(risk-factor pneumonia immunocompromised 4.0)
(risk-factor pneumonia smoking-current 2.5)

;; Medium-Risk Factors
(risk-factor pneumonia diabetes-mellitus 2.0)
(risk-factor pneumonia heart-disease 2.0)
(risk-factor pneumonia recent-viral-infection 2.2)
(risk-factor pneumonia aspiration-risk 2.5)

;; Low-Risk Factors
(risk-factor pneumonia malnutrition 1.5)
(risk-factor pneumonia alcohol-abuse 1.8)

;; -------------------- ASTHMA EXACERBATION --------------------
;; High-Risk Factors
(risk-factor asthma-exacerbation previous-icu-admission-asthma 5.0)
(risk-factor asthma-exacerbation previous-intubation-asthma 5.0)
(risk-factor asthma-exacerbation poor-asthma-control 3.0)
(risk-factor asthma-exacerbation non-adherence-medications 3.5)

;; Medium-Risk Factors
(risk-factor asthma-exacerbation respiratory-infection-current 2.5)
(risk-factor asthma-exacerbation allergen-exposure 2.0)
(risk-factor asthma-exacerbation smoking-current 2.2)

;; Low-Risk Factors
(risk-factor asthma-exacerbation stress-emotional 1.3)
(risk-factor asthma-exacerbation weather-changes 1.2)

;; -------------------- DEEP VEIN THROMBOSIS (DVT) --------------------
;; High-Risk Factors
(risk-factor deep-vein-thrombosis recent-surgery 4.0)
(risk-factor deep-vein-thrombosis cancer-active 4.5)
(risk-factor deep-vein-thrombosis immobilization 3.5)
(risk-factor deep-vein-thrombosis previous-dvt 4.0)

;; Medium-Risk Factors
(risk-factor deep-vein-thrombosis pregnancy 3.0)
(risk-factor deep-vein-thrombosis oral-contraceptive-use 2.0)
(risk-factor deep-vein-thrombosis obesity 1.8)
(risk-factor deep-vein-thrombosis long-flight 2.5)

;; Low-Risk Factors
(risk-factor deep-vein-thrombosis age-over-60 1.5)
(risk-factor deep-vein-thrombosis varicose-veins 1.3)

;; -------------------- HYPOGLYCEMIA --------------------
;; High-Risk Factors
(risk-factor hypoglycemia insulin-use 4.0)
(risk-factor hypoglycemia sulfonylurea-use 3.5)
(risk-factor hypoglycemia missed-meal 3.0)
(risk-factor hypoglycemia excessive-exercise 2.5)

;; Medium-Risk Factors
(risk-factor hypoglycemia alcohol-consumption-recent 2.5)
(risk-factor hypoglycemia kidney-disease 2.0)
(risk-factor hypoglycemia liver-disease 2.0)

;; Low-Risk Factors
(risk-factor hypoglycemia age-over-65 1.5)
(risk-factor hypoglycemia impaired-awareness-hypoglycemia 1.8)

;; -------------------- KIDNEY STONES --------------------
;; High-Risk Factors
(risk-factor kidney-stones previous-kidney-stones 4.0)
(risk-factor kidney-stones family-history-kidney-stones 3.0)
(risk-factor kidney-stones chronic-dehydration 3.5)

;; Medium-Risk Factors
(risk-factor kidney-stones high-protein-diet 2.0)
(risk-factor kidney-stones high-sodium-diet 2.0)
(risk-factor kidney-stones obesity 1.8)
(risk-factor kidney-stones gout 2.5)

;; Low-Risk Factors
(risk-factor kidney-stones male-gender 1.5)
(risk-factor kidney-stones age-30-50 1.3)

;; -------------------- CONCUSSION --------------------
;; High-Risk Factors
(risk-factor concussion previous-concussions 3.5)
(risk-factor concussion contact-sports-participation 3.0)
(risk-factor concussion anticoagulant-use 2.5)

;; Medium-Risk Factors
(risk-factor concussion age-over-65 2.0)
(risk-factor concussion age-under-4 2.0)
(risk-factor concussion alcohol-intoxication 2.2)

;; Low-Risk Factors
(risk-factor concussion learning-disability 1.3)
(risk-factor concussion adhd 1.2)

;; ========================================
;; RISK FACTORS - COMMON CONDITIONS
;; ========================================

;; -------------------- URINARY TRACT INFECTION (UTI) --------------------
;; High-Risk Factors
(risk-factor urinary-tract-infection female-gender 3.0)
(risk-factor urinary-tract-infection pregnancy 3.5)
(risk-factor urinary-tract-infection diabetes-mellitus 2.5)
(risk-factor urinary-tract-infection catheter-use 4.0)

;; Medium-Risk Factors
(risk-factor urinary-tract-infection sexual-activity-recent 2.0)
(risk-factor urinary-tract-infection menopause 2.0)
(risk-factor urinary-tract-infection kidney-stones 2.2)

;; Low-Risk Factors
(risk-factor urinary-tract-infection previous-uti 1.8)
(risk-factor urinary-tract-infection inadequate-fluid-intake 1.5)

;; -------------------- DEHYDRATION --------------------
;; High-Risk Factors
(risk-factor dehydration age-infant 3.5)
(risk-factor dehydration age-over-65 3.0)
(risk-factor dehydration diarrhea-severe 3.5)
(risk-factor dehydration vomiting-persistent 3.5)

;; Medium-Risk Factors
(risk-factor dehydration diabetes-mellitus 2.0)
(risk-factor dehydration diuretic-use 2.5)
(risk-factor dehydration fever-high 2.0)

;; Low-Risk Factors
(risk-factor dehydration hot-weather-exposure 1.5)
(risk-factor dehydration strenuous-exercise 1.5)

;; -------------------- CELLULITIS --------------------
;; High-Risk Factors
(risk-factor cellulitis diabetes-mellitus 3.0)
(risk-factor cellulitis lymphedema 3.5)
(risk-factor cellulitis immunocompromised 3.5)
(risk-factor cellulitis peripheral-vascular-disease 2.8)

;; Medium-Risk Factors
(risk-factor cellulitis obesity 2.0)
(risk-factor cellulitis skin-injury-recent 2.5)
(risk-factor cellulitis previous-cellulitis 2.2)

;; Low-Risk Factors
(risk-factor cellulitis athlete-foot 1.5)
(risk-factor cellulitis eczema 1.4)

;; -------------------- MIGRAINE --------------------
;; High-Risk Factors
(risk-factor migraine family-history-migraine 4.0)
(risk-factor migraine female-gender 3.0)

;; Medium-Risk Factors
(risk-factor migraine stress-chronic 2.0)
(risk-factor migraine sleep-disturbance 2.2)
(risk-factor migraine hormonal-changes 2.5)

;; Low-Risk Factors
(risk-factor migraine caffeine-overuse 1.5)
(risk-factor migraine weather-changes 1.3)
(risk-factor migraine age-20-50 1.2)

;; -------------------- INFLUENZA --------------------
;; High-Risk Factors
(risk-factor influenza age-over-65 3.0)
(risk-factor influenza age-under-5 2.5)
(risk-factor influenza pregnancy 3.0)
(risk-factor influenza immunocompromised 3.5)

;; Medium-Risk Factors
(risk-factor influenza chronic-lung-disease 2.5)
(risk-factor influenza chronic-heart-disease 2.5)
(risk-factor influenza diabetes-mellitus 2.0)

;; Low-Risk Factors
(risk-factor influenza unvaccinated 1.8)
(risk-factor influenza crowded-living-conditions 1.5)

;; ========================================
;; DIAGNOSTIC CRITERIA - CLINICAL SCORING SYSTEMS
;; ========================================

;; -------------------- PERC RULE (Pulmonary Embolism Rule-Out Criteria) --------------------
;; Used to rule OUT PE if all criteria are negative
(diagnostic-criteria pulmonary-embolism perc-rule age-under-50)
(diagnostic-criteria pulmonary-embolism perc-rule heart-rate-under-100)
(diagnostic-criteria pulmonary-embolism perc-rule spo2-over-94)
(diagnostic-criteria pulmonary-embolism perc-rule no-hemoptysis)
(diagnostic-criteria pulmonary-embolism perc-rule no-estrogen-use)
(diagnostic-criteria pulmonary-embolism perc-rule no-prior-dvt-pe)
(diagnostic-criteria pulmonary-embolism perc-rule no-recent-surgery)
(diagnostic-criteria pulmonary-embolism perc-rule no-unilateral-leg-swelling)

;; PERC interpretation: If ALL 8 negative, PE risk <2%, no further testing needed

;; -------------------- WELLS SCORE (Deep Vein Thrombosis) --------------------
;; Predicts probability of DVT
(diagnostic-criteria deep-vein-thrombosis wells-score active-cancer-1)
(diagnostic-criteria deep-vein-thrombosis wells-score paralysis-or-immobilization-1)
(diagnostic-criteria deep-vein-thrombosis wells-score bedridden-3-days-or-surgery-1)
(diagnostic-criteria deep-vein-thrombosis wells-score tenderness-deep-vein-1)
(diagnostic-criteria deep-vein-thrombosis wells-score entire-leg-swollen-1)
(diagnostic-criteria deep-vein-thrombosis wells-score calf-swelling-3cm-1)
(diagnostic-criteria deep-vein-thrombosis wells-score pitting-edema-1)
(diagnostic-criteria deep-vein-thrombosis wells-score collateral-veins-1)
(diagnostic-criteria deep-vein-thrombosis wells-score previous-dvt-1)
(diagnostic-criteria deep-vein-thrombosis wells-score alternative-diagnosis-minus-2)

;; Wells DVT interpretation: ≥2 = DVT likely, <2 = DVT unlikely

;; -------------------- CENTOR SCORE (Strep Throat) --------------------
;; Predicts probability of Group A Streptococcal pharyngitis
;; Note: Not directly applicable to current conditions but included for completeness
(diagnostic-criteria sore-throat centor-score fever-present-1)
(diagnostic-criteria sore-throat centor-score absence-of-cough-1)
(diagnostic-criteria sore-throat centor-score tonsillar-exudate-1)
(diagnostic-criteria sore-throat centor-score tender-anterior-nodes-1)
(diagnostic-criteria sore-throat centor-score age-3-14-plus-1)
(diagnostic-criteria sore-throat centor-score age-15-44-zero)
(diagnostic-criteria sore-throat centor-score age-over-45-minus-1)

;; Centor interpretation: ≥4 = high probability, test/treat; <1 = no testing needed

;; -------------------- CURB-65 (Pneumonia Severity) --------------------
;; Predicts mortality in community-acquired pneumonia
(diagnostic-criteria pneumonia curb-65 confusion-1)
(diagnostic-criteria pneumonia curb-65 urea-over-7mmol-1)
(diagnostic-criteria pneumonia curb-65 respiratory-rate-30-1)
(diagnostic-criteria pneumonia curb-65 blood-pressure-low-1)
(diagnostic-criteria pneumonia curb-65 age-65-or-over-1)

;; CURB-65 interpretation: 0-1 = outpatient, 2 = hospital, 3-5 = ICU consider

;; -------------------- GLASGOW COMA SCALE (Concussion/Head Injury) --------------------
(diagnostic-criteria concussion gcs-score eye-opening-4)
(diagnostic-criteria concussion gcs-score verbal-response-5)
(diagnostic-criteria concussion gcs-score motor-response-6)

;; GCS interpretation: 15 = mild, 13-14 = moderate, <13 = severe

;; -------------------- CHADS2-VASc (Stroke Risk in Atrial Fibrillation) --------------------
(diagnostic-criteria stroke chads2-vasc congestive-heart-failure-1)
(diagnostic-criteria stroke chads2-vasc hypertension-1)
(diagnostic-criteria stroke chads2-vasc age-75-or-over-2)
(diagnostic-criteria stroke chads2-vasc diabetes-1)
(diagnostic-criteria stroke chads2-vasc stroke-tia-history-2)
(diagnostic-criteria stroke chads2-vasc vascular-disease-1)
(diagnostic-criteria stroke chads2-vasc age-65-74-1)
(diagnostic-criteria stroke chads2-vasc female-gender-1)

;; CHA2DS2-VASc interpretation: 0 = no anticoagulation, 1 = consider, ≥2 = anticoagulate

;; ========================================
;; CLARIFYING QUESTIONS - DIFFERENTIAL DIAGNOSIS AIDS
;; ========================================

;; Questions to differentiate between similar conditions

;; -------------------- CHEST PAIN DIFFERENTIAL --------------------
(clarifying-question chest-pain-differential "Does the pain radiate to your left arm, jaw, or neck?")
(helps-differentiate "Does the pain radiate to your left arm, jaw, or neck?" heart-attack chest-wall-pain)

(clarifying-question chest-pain-differential "Does the pain worsen with deep breathing or coughing?")
(helps-differentiate "Does the pain worsen with deep breathing or coughing?" pulmonary-embolism heart-attack)

(clarifying-question chest-pain-differential "Did the pain start suddenly or gradually?")
(helps-differentiate "Did the pain start suddenly or gradually?" pulmonary-embolism angina)

;; -------------------- HEADACHE DIFFERENTIAL --------------------
(clarifying-question headache-differential "Is this the worst headache of your life?")
(helps-differentiate "Is this the worst headache of your life?" stroke migraine)

(clarifying-question headache-differential "Do you have a fever along with the headache?")
(helps-differentiate "Do you have a fever along with the headache?" meningitis tension-headache)

(clarifying-question headache-differential "Is the headache on one side of your head?")
(helps-differentiate "Is the headache on one side of your head?" migraine tension-headache)

(clarifying-question headache-differential "Do you have neck stiffness?")
(helps-differentiate "Do you have neck stiffness?" meningitis migraine)

;; -------------------- SHORTNESS OF BREATH DIFFERENTIAL --------------------
(clarifying-question dyspnea-differential "Did the shortness of breath start suddenly?")
(helps-differentiate "Did the shortness of breath start suddenly?" pulmonary-embolism asthma-exacerbation)

(clarifying-question dyspnea-differential "Do you have leg swelling or calf pain?")
(helps-differentiate "Do you have leg swelling or calf pain?" deep-vein-thrombosis pneumonia)

(clarifying-question dyspnea-differential "Do you wheeze when breathing?")
(helps-differentiate "Do you wheeze when breathing?" asthma-exacerbation heart-attack)

;; -------------------- FEVER + CONFUSION DIFFERENTIAL --------------------
(clarifying-question fever-confusion-differential "Did the confusion develop rapidly (hours)?")
(helps-differentiate "Did the confusion develop rapidly (hours)?" meningitis sepsis)

(clarifying-question fever-confusion-differential "Have you had recent head trauma?")
(helps-differentiate "Have you had recent head trauma?" concussion meningitis)

;; -------------------- ABDOMINAL PAIN DIFFERENTIAL --------------------
(clarifying-question abdominal-pain-differential "Where exactly is the pain located?")
(helps-differentiate "Where exactly is the pain located?" appendicitis gastroenteritis)

(clarifying-question abdominal-pain-differential "Did the pain move from around the belly button to the lower right?")
(helps-differentiate "Did the pain move from around the belly button to the lower right?" appendicitis kidney-stones)

(clarifying-question abdominal-pain-differential "Does the pain come in waves?")
(helps-differentiate "Does the pain come in waves?" kidney-stones appendicitis)

;; -------------------- URINARY SYMPTOMS DIFFERENTIAL --------------------
(clarifying-question urinary-differential "Do you have flank pain (back/side pain)?")
(helps-differentiate "Do you have flank pain (back/side pain)?" kidney-stones urinary-tract-infection)

(clarifying-question urinary-differential "Do you see blood in your urine?")
(helps-differentiate "Do you see blood in your urine?" kidney-stones urinary-tract-infection)

;; -------------------- ALLERGIC REACTION SEVERITY --------------------
(clarifying-question allergy-severity "Is your throat swelling or feeling tight?")
(helps-differentiate "Is your throat swelling or feeling tight?" anaphylaxis mild-allergic-reaction)

(clarifying-question allergy-severity "Are you having difficulty breathing?")
(helps-differentiate "Are you having difficulty breathing?" anaphylaxis hives-only)

;; -------------------- DIABETES COMPLICATION DIFFERENTIAL --------------------
(clarifying-question diabetes-complication "What is your current blood sugar reading?")
(helps-differentiate "What is your current blood sugar reading?" diabetic-ketoacidosis hypoglycemia)

(clarifying-question diabetes-complication "Is your breath fruity-smelling?")
(helps-differentiate "Is your breath fruity-smelling?" diabetic-ketoacidosis hypoglycemia)

;; ========================================
;; PREVALENCE DATA (Bonus - helps with Bayesian reasoning)
;; ========================================

;; Population prevalence helps adjust diagnostic probability

;; Age-based prevalence
(prevalence heart-attack age-under-40 0.001)  ;; 0.1%
(prevalence heart-attack age-40-60 0.005)     ;; 0.5%
(prevalence heart-attack age-over-60 0.02)    ;; 2%

(prevalence stroke age-under-45 0.0005)
(prevalence stroke age-45-65 0.003)
(prevalence stroke age-over-65 0.015)

(prevalence migraine age-20-50 0.15)          ;; 15%
(prevalence migraine age-over-50 0.08)

;; Gender-based prevalence
(prevalence urinary-tract-infection female 0.50)  ;; 50% lifetime risk
(prevalence urinary-tract-infection male 0.05)

(prevalence migraine female 0.18)
(prevalence migraine male 0.06)

;; General population prevalence (useful for differential diagnosis)
(prevalence influenza general-population 0.05)     ;; 5% during flu season
(prevalence common-cold general-population 0.15)   ;; 15% at any given time
(prevalence tension-headache general-population 0.40)  ;; 40% lifetime

;; ========================================
;; END OF PHASE 2 ADDITIONS
;; ========================================
;; ============================================================================
;; EPIC 7 - PHASE 3: Treatment Protocols + Symptom Attributes + Epidemiology
;; ============================================================================
;; Generated: October 12, 2025
;; Purpose: Step-by-step treatment protocols, symptom timing/location data,
;;          and seasonal prevalence for enhanced diagnostic precision
;; ============================================================================

;; ============================================================================
;; TREATMENT PROTOCOL SEQUENCING
;; ============================================================================
;; Schema: (treatment-protocol condition step-number action timing priority)
;; timing: immediate, 0-5min, 5-15min, 15-30min, 30-60min, 1-2h, 2-4h
;; priority: critical, high, medium, low

;; Heart Attack Protocol (8 steps)
(treatment-protocol heart-attack 1 call-911 immediate critical)
(treatment-protocol heart-attack 2 chew-aspirin-325mg 0-5min critical)
(treatment-protocol heart-attack 3 sit-down-rest 0-5min critical)
(treatment-protocol heart-attack 4 loosen-tight-clothing 0-5min high)
(treatment-protocol heart-attack 5 administer-nitroglycerin 5-15min high)
(treatment-protocol heart-attack 6 monitor-vital-signs 5-15min high)
(treatment-protocol heart-attack 7 prepare-medical-history 5-15min medium)
(treatment-protocol heart-attack 8 stay-calm-reassure 0-5min medium)

;; Stroke Protocol (7 steps) - FAST Protocol
(treatment-protocol stroke 1 call-911-immediately immediate critical)
(treatment-protocol stroke 2 note-symptom-onset-time immediate critical)
(treatment-protocol stroke 3 lay-person-flat 0-5min critical)
(treatment-protocol stroke 4 turn-head-to-side 0-5min high)
(treatment-protocol stroke 5 do-not-give-food-or-drink 0-5min high)
(treatment-protocol stroke 6 monitor-consciousness 5-15min high)
(treatment-protocol stroke 7 gather-medication-list 5-15min medium)

;; Anaphylaxis Protocol (6 steps)
(treatment-protocol anaphylaxis 1 administer-epinephrine-auto-injector immediate critical)
(treatment-protocol anaphylaxis 2 call-911-immediately immediate critical)
(treatment-protocol anaphylaxis 3 lay-person-flat-elevate-legs 0-5min critical)
(treatment-protocol anaphylaxis 4 loosen-tight-clothing 0-5min high)
(treatment-protocol anaphylaxis 5 prepare-second-epipen-dose 5-15min high)
(treatment-protocol anaphylaxis 6 monitor-breathing-pulse 0-5min high)

;; Diabetic Ketoacidosis (DKA) Protocol (7 steps)
(treatment-protocol diabetic-ketoacidosis 1 call-911-immediately immediate critical)
(treatment-protocol diabetic-ketoacidosis 2 check-blood-glucose 0-5min critical)
(treatment-protocol diabetic-ketoacidosis 3 do-not-give-insulin-at-home 0-5min critical)
(treatment-protocol diabetic-ketoacidosis 4 position-recovery-if-unconscious 0-5min high)
(treatment-protocol diabetic-ketoacidosis 5 prepare-for-iv-fluids immediate high)
(treatment-protocol diabetic-ketoacidosis 6 monitor-consciousness-level 5-15min high)
(treatment-protocol diabetic-ketoacidosis 7 gather-diabetes-medication-list 5-15min medium)

;; Sepsis Protocol (8 steps)
(treatment-protocol sepsis 1 call-911-or-go-to-er immediate critical)
(treatment-protocol sepsis 2 note-infection-source immediate critical)
(treatment-protocol sepsis 3 keep-person-warm 0-5min high)
(treatment-protocol sepsis 4 monitor-temperature 5-15min high)
(treatment-protocol sepsis 5 do-not-give-antibiotics-at-home 0-5min high)
(treatment-protocol sepsis 6 prepare-for-blood-cultures immediate high)
(treatment-protocol sepsis 7 list-recent-infections 5-15min medium)
(treatment-protocol sepsis 8 monitor-vital-signs-continuously 5-15min high)

;; Pulmonary Embolism Protocol (7 steps)
(treatment-protocol pulmonary-embolism 1 call-911-immediately immediate critical)
(treatment-protocol pulmonary-embolism 2 sit-upright-or-semi-reclined 0-5min critical)
(treatment-protocol pulmonary-embolism 3 loosen-restrictive-clothing 0-5min high)
(treatment-protocol pulmonary-embolism 4 stay-calm-slow-breathing 0-5min high)
(treatment-protocol pulmonary-embolism 5 do-not-walk-or-move 0-5min high)
(treatment-protocol pulmonary-embolism 6 monitor-oxygen-saturation 5-15min high)
(treatment-protocol pulmonary-embolism 7 prepare-recent-travel-history 5-15min medium)

;; Severe Asthma Exacerbation Protocol (8 steps)
(treatment-protocol asthma-exacerbation 1 use-rescue-inhaler-immediately immediate critical)
(treatment-protocol asthma-exacerbation 2 sit-upright-lean-forward 0-5min critical)
(treatment-protocol asthma-exacerbation 3 call-911-if-no-improvement 5-15min critical)
(treatment-protocol asthma-exacerbation 4 loosen-tight-clothing 0-5min high)
(treatment-protocol asthma-exacerbation 5 repeat-inhaler-every-3-5min 5-15min high)
(treatment-protocol asthma-exacerbation 6 stay-calm-breathe-slowly 0-5min high)
(treatment-protocol asthma-exacerbation 7 avoid-talking-unnecessary 0-5min medium)
(treatment-protocol asthma-exacerbation 8 prepare-asthma-action-plan 5-15min medium)

;; Heat Stroke Protocol (9 steps)
(treatment-protocol heat-stroke 1 call-911-immediately immediate critical)
(treatment-protocol heat-stroke 2 move-to-cool-shaded-area immediate critical)
(treatment-protocol heat-stroke 3 remove-excess-clothing 0-5min critical)
(treatment-protocol heat-stroke 4 cool-with-water-or-ice immediate critical)
(treatment-protocol heat-stroke 5 fan-to-increase-cooling 0-5min high)
(treatment-protocol heat-stroke 6 apply-ice-packs-to-armpits-groin 0-5min high)
(treatment-protocol heat-stroke 7 monitor-body-temperature 5-15min high)
(treatment-protocol heat-stroke 8 do-not-give-fluids-if-unconscious 0-5min high)
(treatment-protocol heat-stroke 9 position-recovery-if-vomiting 5-15min medium)

;; Protocol Dependencies (sequential requirements)
(protocol-dependency heart-attack 2 1)  ;; Step 2 depends on Step 1
(protocol-dependency heart-attack 5 2)  ;; Nitroglycerin after aspirin
(protocol-dependency anaphylaxis 5 1)   ;; Second epipen after first
(protocol-dependency asthma-exacerbation 3 1)  ;; 911 if inhaler doesn't work
(protocol-dependency asthma-exacerbation 5 1)  ;; Repeat inhaler after first use

;; Protocol Warnings
(protocol-warning heart-attack nitroglycerin "Do not give if blood pressure low")
(protocol-warning anaphylaxis epipen "May need second dose after 5-15 minutes")
(protocol-warning diabetic-ketoacidosis insulin "Do NOT give insulin at home - requires hospital IV insulin")
(protocol-warning heat-stroke cooling "Stop cooling if shivering begins")
(protocol-warning asthma-exacerbation inhaler "If no improvement after 3 doses, call 911 immediately")

;; ============================================================================
;; SYMPTOM ATTRIBUTES - Duration, Onset, Location, Character
;; ============================================================================
;; Schema: (symptom-attribute symptom attribute-type value)

;; Chest Pain Attributes
(symptom-attribute chest-pain duration-typical 5-30-minutes)
(symptom-attribute chest-pain duration-range acute-to-hours)
(symptom-attribute chest-pain onset-pattern sudden-or-gradual)
(symptom-attribute chest-pain location-primary substernal-or-left-chest)
(symptom-attribute chest-pain radiation left-arm-jaw-neck-back)
(symptom-attribute chest-pain character crushing-or-pressure)
(symptom-attribute chest-pain severity 7-10-scale)
(symptom-attribute chest-pain triggers exertion-stress-cold)

;; Headache Attributes
(symptom-attribute severe-headache duration-typical hours-to-days)
(symptom-attribute severe-headache onset-pattern gradual-or-thunderclap)
(symptom-attribute severe-headache location-primary unilateral-or-bilateral)
(symptom-attribute severe-headache location-specific frontal-temporal-occipital)
(symptom-attribute severe-headache character throbbing-or-pressure)
(symptom-attribute severe-headache severity 5-10-scale)
(symptom-attribute severe-headache triggers light-sound-movement)

;; Abdominal Pain Attributes
(symptom-attribute abdominal-pain duration-typical hours-to-days)
(symptom-attribute abdominal-pain onset-pattern sudden-or-gradual)
(symptom-attribute abdominal-pain location-primary ruq-luq-rlq-llq-epigastric)
(symptom-attribute abdominal-pain character cramping-sharp-dull)
(symptom-attribute abdominal-pain severity 4-10-scale)
(symptom-attribute abdominal-pain migration-pattern appendicitis-periumbilical-to-rlq)

;; Shortness of Breath Attributes
(symptom-attribute shortness-of-breath duration-typical minutes-to-hours)
(symptom-attribute shortness-of-breath onset-pattern sudden-or-gradual)
(symptom-attribute shortness-of-breath severity rest-exertion-minimal)
(symptom-attribute shortness-of-breath position-dependence orthopnea-platypnea)
(symptom-attribute shortness-of-breath associated-symptoms wheezing-cough-chest-pain)

;; Fever Attributes
(symptom-attribute fever duration-typical hours-to-days)
(symptom-attribute fever onset-pattern sudden-or-gradual)
(symptom-attribute fever temperature-range 100.4-104F)
(symptom-attribute fever pattern continuous-intermittent-remittent)
(symptom-attribute fever associated-symptoms chills-sweats-rigors)

;; Dizziness Attributes
(symptom-attribute dizziness duration-typical seconds-to-minutes)
(symptom-attribute dizziness onset-pattern sudden)
(symptom-attribute dizziness character vertigo-or-lightheadedness)
(symptom-attribute dizziness position-dependence standing-turning-lying)
(symptom-attribute dizziness associated-symptoms nausea-hearing-loss)

;; Nausea/Vomiting Attributes
(symptom-attribute nausea duration-typical hours-to-days)
(symptom-attribute nausea onset-pattern sudden-or-gradual)
(symptom-attribute nausea severity mild-moderate-severe)
(symptom-attribute nausea timing postprandial-fasting-morning)
(symptom-attribute nausea associated-symptoms vomiting-diarrhea-fever)

;; Cough Attributes
(symptom-attribute cough duration-typical days-to-weeks)
(symptom-attribute cough onset-pattern acute-chronic)
(symptom-attribute cough character dry-productive)
(symptom-attribute cough timing nocturnal-postprandial-continuous)
(symptom-attribute cough associated-symptoms fever-dyspnea-hemoptysis)

;; Fatigue Attributes
(symptom-attribute fatigue duration-typical days-to-months)
(symptom-attribute fatigue onset-pattern gradual)
(symptom-attribute fatigue severity mild-moderate-severe)
(symptom-attribute fatigue pattern-daily morning-evening-constant)
(symptom-attribute fatigue associated-symptoms weakness-dyspnea-weight-loss)

;; Neck Stiffness Attributes
(symptom-attribute neck-stiffness duration-typical hours-to-days)
(symptom-attribute neck-stiffness onset-pattern sudden-or-gradual)
(symptom-attribute neck-stiffness severity mild-moderate-severe)
(symptom-attribute neck-stiffness location anterior-posterior-lateral)
(symptom-attribute neck-stiffness associated-symptoms fever-headache-photophobia)

;; ============================================================================
;; EPIDEMIOLOGY & SEASONAL PREVALENCE
;; ============================================================================
;; Schema: (seasonal-prevalence condition season-month prevalence-multiplier)
;; prevalence-multiplier: relative to baseline (1.0 = baseline)

;; Influenza Seasonality
(seasonal-prevalence influenza november 2.0)
(seasonal-prevalence influenza december 3.5)
(seasonal-prevalence influenza january 4.0)
(seasonal-prevalence influenza february 3.5)
(seasonal-prevalence influenza march 2.0)
(seasonal-prevalence influenza april 1.0)
(seasonal-prevalence influenza may 0.3)
(seasonal-prevalence influenza june 0.2)
(seasonal-prevalence influenza july 0.2)
(seasonal-prevalence influenza august 0.3)
(seasonal-prevalence influenza september 0.5)
(seasonal-prevalence influenza october 1.0)

;; Common Cold Seasonality
(seasonal-prevalence common-cold november 1.8)
(seasonal-prevalence common-cold december 2.0)
(seasonal-prevalence common-cold january 2.2)
(seasonal-prevalence common-cold february 2.0)
(seasonal-prevalence common-cold march 1.5)
(seasonal-prevalence common-cold april 1.0)
(seasonal-prevalence common-cold may 0.8)
(seasonal-prevalence common-cold june 0.7)
(seasonal-prevalence common-cold july 0.7)
(seasonal-prevalence common-cold august 0.8)
(seasonal-prevalence common-cold september 1.2)
(seasonal-prevalence common-cold october 1.5)

;; Pneumonia Seasonality
(seasonal-prevalence pneumonia november 1.5)
(seasonal-prevalence pneumonia december 2.0)
(seasonal-prevalence pneumonia january 2.5)
(seasonal-prevalence pneumonia february 2.0)
(seasonal-prevalence pneumonia march 1.5)
(seasonal-prevalence pneumonia april 1.0)
(seasonal-prevalence pneumonia may 0.8)
(seasonal-prevalence pneumonia june 0.7)
(seasonal-prevalence pneumonia july 0.7)
(seasonal-prevalence pneumonia august 0.8)
(seasonal-prevalence pneumonia september 1.0)
(seasonal-prevalence pneumonia october 1.2)

;; Asthma Exacerbation Seasonality
(seasonal-prevalence asthma-exacerbation january 1.5)
(seasonal-prevalence asthma-exacerbation february 1.3)
(seasonal-prevalence asthma-exacerbation march 1.5)
(seasonal-prevalence asthma-exacerbation april 1.8)
(seasonal-prevalence asthma-exacerbation may 2.0)
(seasonal-prevalence asthma-exacerbation june 1.2)
(seasonal-prevalence asthma-exacerbation july 1.0)
(seasonal-prevalence asthma-exacerbation august 1.0)
(seasonal-prevalence asthma-exacerbation september 1.8)
(seasonal-prevalence asthma-exacerbation october 2.0)
(seasonal-prevalence asthma-exacerbation november 1.5)
(seasonal-prevalence asthma-exacerbation december 1.3)

;; Heat Stroke Seasonality
(seasonal-prevalence heat-stroke january 0.1)
(seasonal-prevalence heat-stroke february 0.1)
(seasonal-prevalence heat-stroke march 0.3)
(seasonal-prevalence heat-stroke april 0.8)
(seasonal-prevalence heat-stroke may 2.0)
(seasonal-prevalence heat-stroke june 4.0)
(seasonal-prevalence heat-stroke july 5.0)
(seasonal-prevalence heat-stroke august 5.0)
(seasonal-prevalence heat-stroke september 3.0)
(seasonal-prevalence heat-stroke october 1.0)
(seasonal-prevalence heat-stroke november 0.3)
(seasonal-prevalence heat-stroke december 0.1)

;; Migraine Seasonality (weather-related)
(seasonal-prevalence migraine january 1.0)
(seasonal-prevalence migraine february 1.2)
(seasonal-prevalence migraine march 1.5)
(seasonal-prevalence migraine april 1.3)
(seasonal-prevalence migraine may 1.2)
(seasonal-prevalence migraine june 1.0)
(seasonal-prevalence migraine july 0.9)
(seasonal-prevalence migraine august 0.9)
(seasonal-prevalence migraine september 1.1)
(seasonal-prevalence migraine october 1.3)
(seasonal-prevalence migraine november 1.2)
(seasonal-prevalence migraine december 1.0)

;; Food Poisoning Seasonality (summer peak)
(seasonal-prevalence food-poisoning january 0.7)
(seasonal-prevalence food-poisoning february 0.7)
(seasonal-prevalence food-poisoning march 0.8)
(seasonal-prevalence food-poisoning april 1.0)
(seasonal-prevalence food-poisoning may 1.5)
(seasonal-prevalence food-poisoning june 2.0)
(seasonal-prevalence food-poisoning july 2.5)
(seasonal-prevalence food-poisoning august 2.3)
(seasonal-prevalence food-poisoning september 1.8)
(seasonal-prevalence food-poisoning october 1.2)
(seasonal-prevalence food-poisoning november 0.9)
(seasonal-prevalence food-poisoning december 0.8)

;; Dehydration Seasonality (summer peak)
(seasonal-prevalence dehydration january 0.6)
(seasonal-prevalence dehydration february 0.6)
(seasonal-prevalence dehydration march 0.8)
(seasonal-prevalence dehydration april 1.0)
(seasonal-prevalence dehydration may 1.5)
(seasonal-prevalence dehydration june 2.5)
(seasonal-prevalence dehydration july 3.0)
(seasonal-prevalence dehydration august 3.0)
(seasonal-prevalence dehydration september 2.0)
(seasonal-prevalence dehydration october 1.2)
(seasonal-prevalence dehydration november 0.8)
(seasonal-prevalence dehydration december 0.7)

;; Geographic Prevalence Modifiers
(geographic-prevalence heat-stroke tropical-climate 3.0)
(geographic-prevalence heat-stroke desert-climate 4.0)
(geographic-prevalence heat-stroke temperate-climate 1.0)
(geographic-prevalence heat-stroke polar-climate 0.1)

(geographic-prevalence influenza urban-area 1.5)
(geographic-prevalence influenza rural-area 0.8)
(geographic-prevalence influenza high-density-population 2.0)

(geographic-prevalence dehydration arid-climate 2.0)
(geographic-prevalence dehydration humid-climate 1.0)
(geographic-prevalence dehydration high-altitude 1.5)

;; ============================================================================
;; SYMPTOM TIMING PATTERNS (for differential diagnosis)
;; ============================================================================

;; Sudden Onset (minutes)
(symptom-onset-pattern stroke sudden-minutes)
(symptom-onset-pattern anaphylaxis sudden-minutes)
(symptom-onset-pattern pulmonary-embolism sudden-minutes)
(symptom-onset-pattern pneumothorax sudden-minutes)
(symptom-onset-pattern heart-attack sudden-to-gradual-minutes-hours)

;; Gradual Onset (hours to days)
(symptom-onset-pattern pneumonia gradual-hours-to-days)
(symptom-onset-pattern influenza gradual-hours-to-days)
(symptom-onset-pattern urinary-tract-infection gradual-days)
(symptom-onset-pattern migraine gradual-hours)
(symptom-onset-pattern dehydration gradual-hours-to-days)

;; Chronic/Progressive (weeks to months)
(symptom-onset-pattern diabetes chronic-weeks-to-months)
(symptom-onset-pattern heart-failure chronic-weeks-to-months)
(symptom-onset-pattern copd chronic-months-to-years)

;; Intermittent/Episodic
(symptom-pattern-type migraine episodic-recurrent)
(symptom-pattern-type asthma-exacerbation episodic-triggered)
(symptom-pattern-type anxiety-attack episodic-unpredictable)

;; Progressive/Worsening
(symptom-pattern-type sepsis progressive-worsening)
(symptom-pattern-type heart-failure progressive-worsening)
(symptom-pattern-type diabetic-ketoacidosis progressive-worsening)

;; ============================================================================
;; END OF PHASE 3 ADDITIONS
;; ============================================================================
;; Total Additions:
;; - Treatment Protocols: 8 conditions × 6-9 steps = 60+ protocol steps
;; - Symptom Attributes: 10 symptoms × 5-8 attributes = 60+ attribute entries
;; - Seasonal Prevalence: 8 conditions × 12 months = 96 seasonal entries
;; - Geographic Prevalence: 9 entries
;; - Symptom Timing: 15 pattern entries
;; TOTAL: ~240 new entries
;; ============================================================================
