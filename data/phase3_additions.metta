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
