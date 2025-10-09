;; MeTTa Knowledge Base Template
;; This is a starter template - expand based on your chosen domain

;; Example: Medical Knowledge Graph
;; Replace with your domain-specific knowledge

;; Define relationships
(: has-symptom (-> Entity Symptom))
(: has-cause (-> Condition Cause))
(: has-treatment (-> Condition Treatment))
(: severity (-> Symptom SeverityLevel))

;; Example knowledge entries
;; Format: (has-symptom condition symptom)
;; (has-symptom flu fever)
;; (has-symptom flu cough)
;; (has-symptom flu fatigue)

;; TODO: Add your domain-specific knowledge here
;; Examples:
;; - Medical: conditions, symptoms, treatments
;; - Logistics: routes, warehouses, constraints
;; - Finance: instruments, risks, strategies
;; - Education: topics, prerequisites, resources

;; Example queries you can run:
;; (match &self (has-symptom $condition fever) $condition)
;; (match &self (has-treatment $condition $treatment) ($condition $treatment))
