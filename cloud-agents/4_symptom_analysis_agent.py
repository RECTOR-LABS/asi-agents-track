"""
MediChain AI - Symptom Analysis Agent (Cloud Deployment)
Cloud-ready version with embedded MeTTa knowledge base and integrated query engine.

DEPLOYMENT: Copy this entire file to Agentverse Build tab for MediChain Symptom Analysis agent.

NOTE: This agent requires the 'hyperon' package. If not available in Agentverse,
it will use fallback rule-based logic.
"""

from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum

# Import uagents framework (available in Agentverse)
from uagents import Agent, Context, Protocol, Model

# Try to import hyperon (MeTTa), use fallback if not available
try:
    from hyperon import MeTTa
    METTA_AVAILABLE = True
except ImportError:
    METTA_AVAILABLE = False
    print("WARNING: hyperon package not available. Using fallback logic.")

# ============================================================================
# AGENT ADDRESSES - Cloud Deployment Configuration
# ============================================================================

COORDINATOR_ADDRESS = "agent1qdp74ezv3eas5q60s4650xt97ew5kmyt9de77w2ku55jxys8uq2uk0u440d"

# ============================================================================
# MESSAGE MODELS (Inline - no external imports)
# ============================================================================

class SymptomAnalysisRequestMsg(Model):
    """Request for symptom analysis from coordinator"""
    session_id: str
    symptoms: List[str]
    age: Optional[int] = None
    severity_scores: Optional[Dict[str, int]] = None
    duration_info: Optional[Dict[str, str]] = None
    medical_history: Optional[List[str]] = None
    requesting_agent: str


class SymptomAnalysisResponseMsg(Model):
    """Response from symptom analysis agent"""
    session_id: str
    urgency_level: str
    red_flags: List[str]
    differential_diagnoses: List[str]
    confidence_scores: Dict[str, float]
    reasoning_chain: List[str]
    recommended_next_step: str
    responding_agent: str


# ============================================================================
# EMBEDDED MeTTa KNOWLEDGE BASE (v1.1 - 585 lines)
# ============================================================================

METTA_KNOWLEDGE_BASE = """;; ========================================
;; MediChain AI - Medical Knowledge Base
;; ========================================
;; Comprehensive medical diagnostic knowledge graph for MediChain AI
;; Coverage: 13 medical conditions (critical, urgent, common, differential)
;; Version: 1.1
;; Last Updated: October 10, 2025 (Day 3 - Afternoon)

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
(: emergency urgency-level)
(: urgent-24h urgency-level)
(: routine-care urgency-level)

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
(has-severity meningitis critical)
(has-urgency meningitis emergency)
(time-sensitive meningitis 1)

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

(red-flag-symptom non-blanching-rash true)
(red-flag-symptom petechial-rash true)
(red-flag-symptom altered-mental-status true)

(has-treatment meningitis immediate-911)
(has-treatment meningitis emergency-antibiotics)
(has-treatment meningitis hospital-admission)
(requires-action meningitis call-911-immediately)

;; -------------------- STROKE --------------------
(has-severity stroke critical)
(has-urgency stroke emergency)
(time-sensitive stroke 3)

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

(red-flag-symptom face-drooping true)
(red-flag-symptom one-sided-weakness true)
(red-flag-symptom slurred-speech true)

(has-treatment stroke immediate-911)
(has-treatment stroke stroke-unit-admission)
(has-treatment stroke tPA-within-3-hours)
(requires-action stroke call-911-note-time)

;; -------------------- HEART ATTACK --------------------
(has-severity heart-attack critical)
(has-urgency heart-attack emergency)
(time-sensitive heart-attack 1)

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

(red-flag-symptom chest-pain true)
(red-flag-symptom radiating-pain-left-arm true)
(red-flag-symptom radiating-pain-jaw true)

(has-treatment heart-attack immediate-911)
(has-treatment heart-attack aspirin-immediately)
(has-treatment heart-attack cardiac-catheterization)
(requires-action heart-attack chew-aspirin-call-911)

;; -------------------- APPENDICITIS --------------------
(has-severity appendicitis critical)
(has-urgency appendicitis emergency)
(time-sensitive appendicitis 48)

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

(red-flag-symptom mcburney-point-tenderness true)
(red-flag-symptom rebound-tenderness true)

(has-treatment appendicitis emergency-department-evaluation)
(has-treatment appendicitis surgical-appendectomy)
(has-treatment appendicitis antibiotics)
(requires-action appendicitis seek-emergency-care)

;; ========================================
;; URGENT CONDITIONS
;; ========================================

;; -------------------- PNEUMONIA --------------------
(has-severity pneumonia urgent)
(has-urgency pneumonia urgent-24h)

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

(has-treatment pneumonia antibiotics-bacterial)
(has-treatment pneumonia antivirals-viral)
(has-treatment pneumonia rest-and-fluids)
(has-treatment pneumonia oxygen-therapy)
(requires-action pneumonia see-doctor-within-24h)

(differential-from pneumonia covid-19)
(differential-from pneumonia influenza)

;; -------------------- PULMONARY EMBOLISM --------------------
(has-severity pulmonary-embolism critical)
(has-urgency pulmonary-embolism emergency)
(time-sensitive pulmonary-embolism 2)

(has-symptom pulmonary-embolism sudden-shortness-of-breath)
(has-symptom pulmonary-embolism sharp-chest-pain)
(has-symptom pulmonary-embolism coughing-blood)
(has-symptom pulmonary-embolism rapid-heart-rate)
(has-symptom pulmonary-embolism leg-pain)
(has-symptom pulmonary-embolism leg-swelling)

(red-flag-symptom coughing-blood true)
(red-flag-symptom sudden-shortness-of-breath true)

(has-treatment pulmonary-embolism immediate-911)
(has-treatment pulmonary-embolism anticoagulation)
(has-treatment pulmonary-embolism thrombolysis)
(requires-action pulmonary-embolism call-911-immediately)

;; -------------------- SEPSIS --------------------
(has-severity sepsis critical)
(has-urgency sepsis emergency)
(time-sensitive sepsis 1)

(has-symptom sepsis high-fever)
(has-symptom sepsis hypothermia)
(has-symptom sepsis rapid-heart-rate)
(has-symptom sepsis rapid-breathing)
(has-symptom sepsis confusion)
(has-symptom sepsis extreme-pain)
(has-symptom sepsis clammy-skin)
(has-symptom sepsis low-blood-pressure)

(has-treatment sepsis immediate-911)
(has-treatment sepsis broad-spectrum-antibiotics)
(has-treatment sepsis IV-fluids)
(requires-action sepsis emergency-department-immediately)

;; ========================================
;; COMMON CONDITIONS
;; ========================================

;; -------------------- MIGRAINE --------------------
(has-severity migraine routine)
(has-urgency migraine routine-care)

(has-symptom migraine throbbing-headache)
(has-symptom migraine unilateral-headache)
(has-symptom migraine nausea)
(has-symptom migraine vomiting)
(has-symptom migraine light-sensitivity)
(has-symptom migraine sound-sensitivity)
(has-symptom migraine visual-aura)

(has-treatment migraine triptans)
(has-treatment migraine NSAIDs)
(has-treatment migraine rest-dark-room)
(has-treatment migraine preventive-medications)
(requires-action migraine schedule-doctor-appointment)

(differential-from migraine tension-headache)
(differential-from migraine stroke)

;; -------------------- INFLUENZA --------------------
(has-severity influenza routine)
(has-urgency influenza routine-care)

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

(has-treatment influenza antiviral-medications)
(has-treatment influenza rest-and-fluids)
(has-treatment influenza symptom-management)
(has-treatment influenza fever-reducers)
(requires-action influenza rest-at-home)

(differential-from influenza covid-19)
(differential-from influenza common-cold)

;; -------------------- GASTROENTERITIS --------------------
(has-severity gastroenteritis routine)
(has-urgency gastroenteritis routine-care)

(has-symptom gastroenteritis diarrhea)
(has-symptom gastroenteritis nausea)
(has-symptom gastroenteritis vomiting)
(has-symptom gastroenteritis abdominal-cramps)
(has-symptom gastroenteritis low-grade-fever)
(has-symptom gastroenteritis dehydration)

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

(red-flag-symptom loss-of-taste false)
(red-flag-symptom loss-of-smell false)

(has-treatment covid-19 isolation)
(has-treatment covid-19 antiviral-paxlovid)
(has-treatment covid-19 rest-and-fluids)
(has-treatment covid-19 oxygen-if-severe)
(requires-action covid-19 get-tested-isolate)

(differential-from covid-19 influenza)
(differential-from covid-19 common-cold)

;; -------------------- TENSION HEADACHE --------------------
(has-severity tension-headache routine)
(has-urgency tension-headache routine-care)

(has-symptom tension-headache bilateral-headache)
(has-symptom tension-headache band-like-pressure)
(has-symptom tension-headache dull-ache)
(has-symptom tension-headache scalp-tenderness)
(has-symptom tension-headache neck-tension)

(has-treatment tension-headache over-counter-pain-relievers)
(has-treatment tension-headache stress-management)
(has-treatment tension-headache muscle-relaxation)
(requires-action tension-headache self-care)

(differential-from tension-headache migraine)

;; -------------------- COMMON COLD --------------------
(has-severity common-cold routine)
(has-urgency common-cold routine-care)

(has-symptom common-cold runny-nose)
(has-symptom common-cold sneezing)
(has-symptom common-cold sore-throat)
(has-symptom common-cold cough)
(has-symptom common-cold mild-headache)
(has-symptom common-cold mild-body-aches)
(has-symptom common-cold low-grade-fever-rare)

(has-treatment common-cold rest)
(has-treatment common-cold fluids)
(has-treatment common-cold symptom-relief)
(requires-action common-cold self-care-at-home)

(differential-from common-cold influenza)
(differential-from common-cold covid-19)
"""


# ============================================================================
# SIMPLIFIED MeTTa QUERY ENGINE (Cloud Version)
# ============================================================================

class SimplifiedMeTTaEngine:
    """
    Simplified MeTTa query engine for cloud deployment
    Loads knowledge base from embedded string
    """

    def __init__(self, kb_string: str):
        """Initialize with embedded knowledge base"""
        if METTA_AVAILABLE:
            self.metta = MeTTa()
            self.metta.run(kb_string)
            self.kb_loaded = True
        else:
            self.kb_loaded = False
            # Use fallback knowledge base (simplified dict-based)
            self._init_fallback_kb()

    def _init_fallback_kb(self):
        """Initialize fallback rule-based knowledge base if MeTTa not available"""
        # Simplified condition-symptom mapping for fallback
        self.condition_symptoms = {
            "meningitis": ["fever", "severe-headache", "stiff-neck", "neck-stiffness", "confusion", "nausea", "vomiting"],
            "stroke": ["face-drooping", "arm-weakness", "speech-difficulty", "slurred-speech", "confusion", "dizziness"],
            "heart-attack": ["chest-pain", "shortness-of-breath", "radiating-pain-left-arm"],
            "pneumonia": ["cough", "fever", "chest-pain", "shortness-of-breath", "chills", "fatigue"],
            "influenza": ["fever", "cough", "sore-throat", "muscle-aches", "body-aches", "fatigue", "headache", "chills"],
            "covid-19": ["fever", "cough", "shortness-of-breath", "fatigue", "loss-of-taste", "loss-of-smell"],
            "migraine": ["headache", "nausea", "vomiting", "light-sensitivity"],
            "gastroenteritis": ["diarrhea", "nausea", "vomiting", "abdominal-pain"],
        }
        self.urgency_map = {
            "meningitis": "emergency",
            "stroke": "emergency",
            "heart-attack": "emergency",
            "pneumonia": "urgent",
            "influenza": "routine",
            "covid-19": "urgent",
            "migraine": "routine",
            "gastroenteritis": "routine",
        }
        self.red_flags = ["chest-pain", "face-drooping", "stiff-neck", "neck-stiffness", "altered-mental-status",
                          "shortness-of-breath", "coughing-blood"]

    def query(self, query_string: str):
        """Execute MeTTa query or fallback"""
        if self.kb_loaded:
            return self.metta.run(query_string)
        return []

    def find_conditions_by_symptoms(self, symptoms: List[str]) -> Dict[str, int]:
        """Find conditions matching symptoms"""
        if self.kb_loaded:
            # Use MeTTa queries
            condition_matches = {}
            for symptom in symptoms:
                query = f"!(match &self (has-symptom $condition {symptom}) $condition)"
                results = self.query(query)
                for result in results:
                    result_str = str(result).strip("'[]")
                    if result_str:
                        conds = [c.strip() for c in result_str.split(',')]
                        for cond in conds:
                            if cond:
                                condition_matches[cond] = condition_matches.get(cond, 0) + 1
            return dict(sorted(condition_matches.items(), key=lambda x: x[1], reverse=True))
        else:
            # Fallback: simple matching
            matches = {}
            for cond, cond_symptoms in self.condition_symptoms.items():
                match_count = sum(1 for s in symptoms if s in cond_symptoms)
                if match_count > 0:
                    matches[cond] = match_count
            return dict(sorted(matches.items(), key=lambda x: x[1], reverse=True))

    def find_urgency_level(self, condition: str) -> str:
        """Get urgency level"""
        if self.kb_loaded:
            query = f"!(match &self (has-urgency {condition} $urgency) $urgency)"
            results = self.query(query)
            if results:
                return str(results[0]).strip("'[]")
            return "unknown"
        else:
            return self.urgency_map.get(condition, "routine")

    def find_red_flag_symptoms(self) -> List[str]:
        """Get all red flag symptoms"""
        if self.kb_loaded:
            query = "!(match &self (red-flag-symptom $symptom true) $symptom)"
            results = self.query(query)
            return [str(r).strip("'[]") for r in results]
        else:
            return self.red_flags

    def find_symptoms_by_condition(self, condition: str) -> List[str]:
        """Get all symptoms for condition"""
        if self.kb_loaded:
            query = f"!(match &self (has-symptom {condition} $symptom) $symptom)"
            results = self.query(query)
            parsed = []
            for result in results:
                result_str = str(result).strip("'[]")
                if result_str:
                    items = [item.strip() for item in result_str.split(',')]
                    parsed.extend([item for item in items if item])
            return parsed
        else:
            return self.condition_symptoms.get(condition, [])

    def check_time_sensitivity(self, condition: str) -> Optional[int]:
        """Get time sensitivity in hours"""
        if self.kb_loaded:
            query = f"!(match &self (time-sensitive {condition} $hours) $hours)"
            results = self.query(query)
            if results:
                try:
                    hours_str = str(results[0]).strip("'[]")
                    return int(hours_str) if hours_str.isdigit() else None
                except:
                    return None
        return None


# ============================================================================
# SYMPTOM ANALYSIS CORE LOGIC
# ============================================================================

class SymptomAnalyzer:
    """Core symptom analysis logic with MeTTa integration"""

    def __init__(self, metta_engine: SimplifiedMeTTaEngine):
        self.metta = metta_engine

    def analyze_symptoms(
        self,
        symptoms: List[str],
        age: Optional[int] = None,
        severity_scores: Optional[Dict[str, int]] = None,
        medical_history: Optional[List[str]] = None,
    ) -> Dict:
        """
        Main analysis method

        Returns dict with:
        - urgency_level: str
        - red_flags: List[str]
        - differential_diagnoses: List[str]
        - confidence_scores: Dict[str, float]
        - reasoning_chain: List[str]
        - recommended_next_step: str
        """
        reasoning_chain = []
        reasoning_chain.append(f"🔬 Analyzing {len(symptoms)} symptoms: {', '.join(symptoms)}")

        # Step 1: Detect red flags
        red_flags = self.detect_red_flags(symptoms)
        if red_flags:
            reasoning_chain.append(f"⚠️ RED FLAGS DETECTED: {', '.join(red_flags)}")

        # Step 2: Find matching conditions
        reasoning_chain.append("🔍 Querying MeTTa knowledge base for matching conditions...")
        condition_matches = self.find_matching_conditions(symptoms)
        reasoning_chain.append(f"📊 Found {len(condition_matches)} potential conditions")

        # Step 3: Calculate confidence scores
        confidence_scores = self.calculate_confidence_scores(
            symptoms, condition_matches, severity_scores
        )

        # Step 4: Assess urgency
        urgency_level = self.assess_urgency(
            condition_matches, red_flags, confidence_scores, age
        )
        reasoning_chain.append(f"🚨 Urgency Assessment: {urgency_level.upper()}")

        # Step 5: Generate differential diagnoses
        differential_diagnoses = self.generate_differential_diagnoses(
            confidence_scores, max_count=5
        )
        reasoning_chain.append(f"🎯 Top differential diagnoses: {', '.join(differential_diagnoses[:3])}")

        # Step 6: Recommend action
        recommended_next_step = self.recommend_action(urgency_level, red_flags)
        reasoning_chain.append(f"💡 Recommendation: {recommended_next_step}")

        return {
            "urgency_level": urgency_level,
            "red_flags": red_flags,
            "differential_diagnoses": differential_diagnoses,
            "confidence_scores": confidence_scores,
            "reasoning_chain": reasoning_chain,
            "recommended_next_step": recommended_next_step,
        }

    def detect_red_flags(self, symptoms: List[str]) -> List[str]:
        """Detect critical warning symptoms"""
        red_flags = []
        all_red_flags = self.metta.find_red_flag_symptoms()

        for symptom in symptoms:
            symptom_normalized = symptom.lower().replace(" ", "-").replace("_", "-")
            if symptom_normalized in all_red_flags:
                red_flags.append(symptom)

        # Pattern matching for critical combinations
        symptom_set = set(s.lower().replace(" ", "-").replace("_", "-") for s in symptoms)

        # Meningitis triad
        if {"severe-headache", "fever", "neck-stiffness"}.issubset(symptom_set) or \
           {"severe-headache", "fever", "stiff-neck"}.issubset(symptom_set):
            red_flags.append("Meningitis triad (headache + fever + neck stiffness)")

        # Stroke FAST
        if "face-drooping" in symptom_set or "arm-weakness" in symptom_set or "slurred-speech" in symptom_set:
            red_flags.append("Stroke warning signs (FAST protocol)")

        # Cardiac
        if "chest-pain" in symptom_set:
            red_flags.append("Chest pain (potential cardiac emergency)")

        return red_flags

    def find_matching_conditions(self, symptoms: List[str]) -> List[str]:
        """Find medical conditions matching symptoms"""
        normalized_symptoms = [
            s.lower().replace(" ", "-").replace("_", "-") for s in symptoms
        ]
        results = self.metta.find_conditions_by_symptoms(normalized_symptoms)
        return list(results.keys()) if results else []

    def calculate_confidence_scores(
        self,
        symptoms: List[str],
        conditions: List[str],
        severity_scores: Optional[Dict[str, int]] = None,
    ) -> Dict[str, float]:
        """Calculate confidence score for each condition"""
        confidence_scores = {}

        for condition in conditions:
            condition_symptoms = self.metta.find_symptoms_by_condition(condition)

            if not condition_symptoms:
                confidence_scores[condition] = 0.0
                continue

            normalized_patient_symptoms = set(
                s.lower().replace(" ", "-").replace("_", "-") for s in symptoms
            )
            matched_symptoms = normalized_patient_symptoms.intersection(
                set(condition_symptoms)
            )
            match_ratio = len(matched_symptoms) / len(condition_symptoms)

            # Apply severity weighting
            severity_weight = 1.0
            if severity_scores:
                avg_severity = sum(
                    severity_scores.get(s, 5) for s in matched_symptoms
                ) / max(len(matched_symptoms), 1)
                severity_weight = 0.5 + (avg_severity / 20.0)

            confidence = min(match_ratio * severity_weight, 1.0)
            confidence_scores[condition] = round(confidence, 2)

        return confidence_scores

    def assess_urgency(
        self,
        conditions: List[str],
        red_flags: List[str],
        confidence_scores: Dict[str, float],
        age: Optional[int] = None,
    ) -> str:
        """Assess urgency level"""
        if red_flags:
            return "emergency"

        highest_urgency = "routine"

        for condition, confidence in confidence_scores.items():
            if confidence > 0.5:
                urgency = self.metta.find_urgency_level(condition)

                if urgency == "emergency" or condition in ["meningitis", "stroke", "heart-attack"]:
                    return "emergency"

                time_sensitive = self.metta.check_time_sensitivity(condition)
                if time_sensitive and time_sensitive <= 6:
                    return "emergency"

                if urgency == "urgent-24h":
                    highest_urgency = "urgent"

            elif confidence > 0.3:
                urgency = self.metta.find_urgency_level(condition)
                if urgency == "emergency":
                    highest_urgency = "urgent"
                elif urgency == "urgent-24h":
                    highest_urgency = "urgent"

        # Age-based risk adjustment
        if age and (age < 5 or age > 65):
            if any(confidence > 0.4 for confidence in confidence_scores.values()):
                if highest_urgency == "routine":
                    highest_urgency = "urgent"

        return highest_urgency

    def generate_differential_diagnoses(
        self, confidence_scores: Dict[str, float], max_count: int = 5
    ) -> List[str]:
        """Generate differential diagnoses"""
        sorted_conditions = sorted(
            confidence_scores.items(), key=lambda x: x[1], reverse=True
        )

        differential = [
            condition
            for condition, confidence in sorted_conditions[:max_count]
            if confidence > 0.2
        ]

        if len(differential) < 2 and len(sorted_conditions) >= 2:
            differential = [c for c, _ in sorted_conditions[:2]]

        return differential

    def recommend_action(self, urgency_level: str, red_flags: List[str]) -> str:
        """Recommend immediate action"""
        if urgency_level == "emergency":
            if red_flags:
                return "🚨 EMERGENCY: Call 911 or go to ER immediately. Red flags detected."
            return "🚨 EMERGENCY: Seek immediate medical attention at ER."
        elif urgency_level == "urgent":
            return "⚠️ URGENT: Schedule medical appointment within 24 hours."
        else:
            return "📋 ROUTINE: Schedule appointment with primary care physician."


# ============================================================================
# AGENT INITIALIZATION
# ============================================================================

agent = Agent()

# Create inter-agent protocol
symptom_analysis_proto = Protocol(name="SymptomAnalysisProtocol")

# Initialize MeTTa engine (singleton)
metta_engine = None


def get_metta_engine() -> SimplifiedMeTTaEngine:
    """Get or create MeTTa engine instance"""
    global metta_engine
    if metta_engine is None:
        metta_engine = SimplifiedMeTTaEngine(METTA_KNOWLEDGE_BASE)
    return metta_engine


# ============================================================================
# MESSAGE HANDLERS
# ============================================================================

@symptom_analysis_proto.on_message(model=SymptomAnalysisRequestMsg)
async def handle_symptom_analysis_request(
    ctx: Context, sender: str, msg: SymptomAnalysisRequestMsg
):
    """Handle symptom analysis request from coordinator"""
    ctx.logger.info(f"📥 Received symptom analysis request from {sender}")
    ctx.logger.info(f"   Session ID: {msg.session_id}")
    ctx.logger.info(f"   Symptoms: {msg.symptoms}")

    try:
        # Initialize analyzer
        metta = get_metta_engine()
        analyzer = SymptomAnalyzer(metta)

        # Perform analysis
        ctx.logger.info("🔬 Starting symptom analysis...")
        analysis_result = analyzer.analyze_symptoms(
            symptoms=msg.symptoms,
            age=msg.age,
            severity_scores=msg.severity_scores,
            medical_history=msg.medical_history,
        )

        ctx.logger.info(f"✅ Analysis complete!")
        ctx.logger.info(f"   Urgency: {analysis_result['urgency_level'].upper()}")

        # Create response
        response = SymptomAnalysisResponseMsg(
            session_id=msg.session_id,
            urgency_level=analysis_result["urgency_level"],
            red_flags=analysis_result["red_flags"],
            differential_diagnoses=analysis_result["differential_diagnoses"],
            confidence_scores=analysis_result["confidence_scores"],
            reasoning_chain=analysis_result["reasoning_chain"],
            recommended_next_step=analysis_result["recommended_next_step"],
            responding_agent="medichain-symptom-analysis",
        )

        # Send response
        ctx.logger.info(f"📤 Sending analysis response to {sender}")
        await ctx.send(sender, response)

    except Exception as e:
        ctx.logger.error(f"❌ Error during symptom analysis: {str(e)}")

        # Send error response
        error_response = SymptomAnalysisResponseMsg(
            session_id=msg.session_id,
            urgency_level="routine",
            red_flags=[],
            differential_diagnoses=[],
            confidence_scores={},
            reasoning_chain=[f"Error occurred during analysis: {str(e)}"],
            recommended_next_step="Unable to complete analysis. Please consult healthcare provider.",
            responding_agent="medichain-symptom-analysis",
        )
        await ctx.send(sender, error_response)


# Include protocol
agent.include(symptom_analysis_proto)


# ============================================================================
# STARTUP & INITIALIZATION
# ============================================================================

@agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent on startup"""
    ctx.logger.info("=" * 70)
    ctx.logger.info("MediChain AI - Symptom Analysis Agent (Cloud)")
    ctx.logger.info("=" * 70)
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"MeTTa Available: {METTA_AVAILABLE}")

    # Preload MeTTa engine
    ctx.logger.info("📚 Preloading MeTTa knowledge base...")
    try:
        metta = get_metta_engine()
        ctx.logger.info(f"✅ MeTTa engine ready ({metta.kb_loaded})")
    except Exception as e:
        ctx.logger.error(f"❌ Failed to load MeTTa engine: {str(e)}")

    ctx.logger.info("🚀 Symptom Analysis Agent is READY")
    ctx.logger.info("=" * 70)
