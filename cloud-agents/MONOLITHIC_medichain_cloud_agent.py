"""
MediChain AI - Monolithic Cloud Agent (All-in-One Solution)
Complete diagnostic system combining all functionality in a single agent.

DEPLOYMENT: Copy this entire file to Agentverse Build tab for MediChain AI agent.

ARCHITECTURE:
- Chat Protocol for ASI:One interface
- Symptom extraction via NLP pattern matching
- MeTTa knowledge graph diagnostic reasoning
- Treatment recommendations with safety validation
- Embedded 585-line medical knowledge base

NO INTER-AGENT COMMUNICATION - All processing handled internally.

NOTE: This agent requires the 'hyperon' package. If not available in Agentverse,
it will use fallback rule-based logic.
"""

from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Optional
import re
import json

# Import uagents framework (available in Agentverse)
from uagents import Agent, Context, Protocol, Model

# Import Chat Protocol for ASI:One interface
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

# Try to import hyperon (MeTTa), use fallback if not available
try:
    from hyperon import MeTTa
    METTA_AVAILABLE = True
except ImportError:
    METTA_AVAILABLE = False
    print("WARNING: hyperon package not available. Using fallback logic.")


# ============================================================================
# EMBEDDED MeTTa KNOWLEDGE BASE (v1.1 - 585 lines)
# ============================================================================

METTA_KNOWLEDGE_BASE = """;; ========================================
;; MediChain AI - Medical Knowledge Base
;; ========================================
;; Comprehensive medical diagnostic knowledge graph for MediChain AI
;; Coverage: 13 medical conditions (critical, urgent, common, differential)
;; Version: 1.1
;; Last Updated: October 10, 2025

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
(: safety-warning (-> Treatment Warning))
(: requires-dose-adjustment (-> Treatment Condition))
(: drug-interaction (-> Treatment Medication))

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
;; CONDITION DEFINITIONS
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

;; ========================================
;; TREATMENTS & CONTRAINDICATIONS
;; ========================================

;; MENINGITIS
(contraindication emergency-antibiotics severe-allergy-penicillin)

;; STROKE
(contraindication tPA-within-3-hours recent-surgery)
(contraindication tPA-within-3-hours active-bleeding)
(contraindication tPA-within-3-hours bleeding-disorder)
(safety-warning tPA-within-3-hours "3-hour window critical. Note symptom start time.")

;; HEART ATTACK
(contraindication aspirin-immediately bleeding-disorder)
(contraindication aspirin-immediately active-bleeding)
(contraindication aspirin-immediately aspirin-allergy)
(contraindication aspirin-immediately age-under-18)
(safety-warning aspirin-immediately "Chew, don't swallow whole. Call 911 immediately.")

;; PULMONARY EMBOLISM
(contraindication anticoagulation active-bleeding)
(contraindication anticoagulation recent-surgery)
(contraindication anticoagulation bleeding-disorder)
(contraindication anticoagulation pregnancy-concern)
(safety-warning anticoagulation "High bleeding risk. Avoid contact sports.")

;; PNEUMONIA
(contraindication antibiotics-bacterial severe-allergy-penicillin)
(contraindication antibiotics severe-liver-disease)
(contraindication antibiotics severe-kidney-disease)
(requires-dose-adjustment antibiotics kidney-disease)

;; MIGRAINE
(contraindication triptans heart-disease)
(contraindication triptans uncontrolled-hypertension)
(contraindication triptans pregnancy)
(contraindication NSAIDs kidney-disease)
(contraindication NSAIDs stomach-ulcers)
(contraindication NSAIDs heart-failure)
(contraindication NSAIDs pregnancy-third-trimester)
(requires-dose-adjustment NSAIDs elderly)

;; INFLUENZA
(contraindication antiviral-medications kidney-disease)
(contraindication antiviral-medications severe-asthma)
(requires-dose-adjustment antivirals kidney-disease)
(safety-warning rest-and-fluids "Monitor for worsening symptoms. Seek care if deteriorating.")

;; COVID-19
(contraindication antiviral-paxlovid severe-kidney-disease)
(contraindication antiviral-paxlovid severe-liver-disease)
(contraindication antiviral-paxlovid drug-interaction-statins)
(drug-interaction antiviral-paxlovid statins)

;; COMMON
(safety-warning self-care "Seek medical attention if no improvement in 3-5 days")

;; DRUG INTERACTIONS
(drug-interaction anticoagulation aspirin)
(drug-interaction NSAIDs anticoagulation)
(drug-interaction antibiotics oral-contraceptives)
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
        self.treatments = {
            "meningitis": ["immediate-911", "emergency-antibiotics", "hospital-admission"],
            "stroke": ["immediate-911", "tPA-within-3-hours"],
            "heart-attack": ["immediate-911", "aspirin-immediately", "cardiac-catheterization"],
            "pneumonia": ["antibiotics-bacterial", "rest-and-fluids", "oxygen-therapy"],
            "influenza": ["antiviral-medications", "rest-and-fluids", "symptom-management"],
            "covid-19": ["isolation", "antiviral-paxlovid", "rest-and-fluids"],
            "migraine": ["triptans", "NSAIDs", "rest-dark-room"],
            "gastroenteritis": ["oral-rehydration", "rest", "bland-diet"],
        }
        self.contraindications = {
            "aspirin-immediately": ["bleeding-disorder", "active-bleeding", "aspirin-allergy"],
            "triptans": ["heart-disease", "pregnancy", "uncontrolled-hypertension"],
            "NSAIDs": ["kidney-disease", "stomach-ulcers", "heart-failure"],
        }

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

    def get_treatment_recommendations(self, condition: str) -> List[str]:
        """Get treatments for condition"""
        if self.kb_loaded:
            query = f"!(match &self (has-treatment {condition} $treatment) $treatment)"
            results = self.query(query)
            parsed = []
            for result in results:
                result_str = str(result).strip("'[]")
                if result_str:
                    items = [item.strip() for item in result_str.split(',')]
                    parsed.extend([item for item in items if item])
            return parsed
        else:
            return self.treatments.get(condition, [])

    def get_all_contraindications(self, treatment: str) -> List[str]:
        """Get all contraindications for treatment"""
        if self.kb_loaded:
            query = f"!(match &self (contraindication {treatment} $condition) $condition)"
            results = self.query(query)
            return [str(r).strip("'[]") for r in results]
        else:
            return self.contraindications.get(treatment, [])

    def get_safety_warning(self, treatment: str) -> str:
        """Get safety warning for treatment"""
        if self.kb_loaded:
            query = f'!(match &self (safety-warning {treatment} $warning) $warning)'
            results = self.query(query)
            return str(results[0]).strip('"\'[]') if results else ""
        else:
            warnings = {
                "aspirin-immediately": "Chew, don't swallow whole. Call 911 immediately.",
                "tPA-within-3-hours": "3-hour window critical. Note symptom start time.",
            }
            return warnings.get(treatment, "")

    def check_drug_interaction(self, treatment: str, medication: str) -> bool:
        """Check for drug interaction"""
        if self.kb_loaded:
            query = f"!(match &self (drug-interaction {treatment} {medication}) {treatment})"
            results = self.query(query)
            return len(results) > 0
        return False

    def requires_dose_adjustment(self, treatment: str, condition: str) -> bool:
        """Check if dose adjustment needed"""
        if self.kb_loaded:
            query = f"!(match &self (requires-dose-adjustment {treatment} {condition}) {treatment})"
            results = self.query(query)
            return len(results) > 0
        return False


# ============================================================================
# SYMPTOM EXTRACTION (NLP Pattern Matching)
# ============================================================================

SYMPTOM_KEYWORDS = {
    "high-fever": ["high fever", "very high temperature", "burning up with fever"],
    "fever": ["fever", "high temperature", "temp", "hot"],
    "chills": ["chills", "shivering", "shaking", "cold"],
    "severe-headache": ["severe headache", "terrible headache", "worst headache", "intense headache"],
    "headache": ["headache", "head pain", "head hurts", "migraine", "head ache"],
    "dizziness": ["dizzy", "lightheaded", "vertigo", "spinning"],
    "confusion": ["confused", "disoriented", "foggy", "can't think"],
    "neck-stiffness": ["neck is very stiff", "neck is stiff", "very stiff neck", "extremely stiff neck"],
    "stiff-neck": ["stiff neck", "neck stiff", "can't move neck", "neck hurts to move"],
    "difficulty-breathing": ["difficulty breathing", "hard to breathe", "can't breathe well"],
    "shortness-of-breath": ["short of breath", "can't breathe", "breathless", "gasping"],
    "cough": ["cough", "coughing", "hacking"],
    "sore-throat": ["sore throat", "throat pain", "hurts to swallow"],
    "nausea": ["nausea", "nauseous", "queasy", "sick to stomach"],
    "vomiting": ["vomiting", "throwing up", "vomit", "puking"],
    "diarrhea": ["diarrhea", "loose stool", "runny stool"],
    "abdominal-pain": ["stomach pain", "abdominal pain", "belly pain", "stomach ache"],
    "chest-pain": ["chest pain", "chest hurts", "chest pressure"],
    "muscle-pain": ["muscle pain", "body aches", "sore muscles", "aching"],
    "joint-pain": ["joint pain", "joints hurt", "stiff joints"],
    "rash": ["rash", "skin rash", "spots", "bumps"],
    "fatigue": ["tired", "fatigue", "exhausted", "weakness", "weak"],
    "loss-of-consciousness": ["passed out", "fainted", "blacked out", "unconscious"],
}

SEVERITY_HIGH = ["severe", "extreme", "worst", "unbearable", "terrible", "intense"]
SEVERITY_MEDIUM = ["moderate", "significant", "bad", "strong"]
SEVERITY_LOW = ["mild", "slight", "little bit", "somewhat"]


class Symptom:
    def __init__(self, name: str, raw_text: str, severity: int = 5, duration: Optional[str] = None):
        self.name = name
        self.raw_text = raw_text
        self.severity = severity
        self.duration = duration

    def to_dict(self):
        return {
            "name": self.name,
            "raw_text": self.raw_text,
            "severity": self.severity,
            "duration": self.duration
        }


class SymptomExtractor:
    @staticmethod
    def extract_symptoms(text: str) -> List[Symptom]:
        text_lower = text.lower()
        symptoms = []

        for symptom_name, keywords in SYMPTOM_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    severity = SymptomExtractor._estimate_severity(text_lower)
                    duration = SymptomExtractor._extract_duration(text_lower)
                    symptom = Symptom(
                        name=symptom_name,
                        raw_text=keyword,
                        severity=severity,
                        duration=duration,
                    )
                    symptoms.append(symptom)
                    break

        return symptoms

    @staticmethod
    def _estimate_severity(text: str) -> int:
        if any(word in text for word in SEVERITY_HIGH):
            return 8
        elif any(word in text for word in SEVERITY_MEDIUM):
            return 5
        elif any(word in text for word in SEVERITY_LOW):
            return 3
        else:
            return 5

    @staticmethod
    def _extract_duration(text: str) -> Optional[str]:
        duration_pattern = r'for\s+(\d+)\s+(day|days|hour|hours|week|weeks)'
        match = re.search(duration_pattern, text)
        if match:
            return f"{match.group(1)} {match.group(2)}"

        ago_pattern = r'(\d+)\s+(day|days|hour|hours|week|weeks)\s+ago'
        match = re.search(ago_pattern, text)
        if match:
            return f"{match.group(1)} {match.group(2)}"

        if "yesterday" in text:
            return "1 day"
        if "this morning" in text or "today" in text:
            return "hours"
        if "this week" in text:
            return "days"

        return None

    @staticmethod
    def extract_age(text: str) -> Optional[int]:
        age_pattern = r'(\d+)\s*(year|years|yr|yrs)\s*old'
        match = re.search(age_pattern, text.lower())
        if match:
            return int(match.group(1))
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
# TREATMENT RECOMMENDATION CORE LOGIC
# ============================================================================

class TreatmentRecommender:
    """Core treatment recommendation logic with MeTTa integration"""

    def __init__(self, metta_engine: SimplifiedMeTTaEngine):
        self.metta = metta_engine

    def recommend_treatments(
        self,
        primary_condition: str,
        alternative_conditions: Optional[List[str]] = None,
        urgency_level: str = "routine",
        patient_age: Optional[int] = None,
        allergies: Optional[List[str]] = None,
        current_medications: Optional[List[str]] = None,
        medical_history: Optional[List[str]] = None,
    ) -> Dict:
        """Main recommendation method"""
        reasoning_chain = []
        reasoning_chain.append(f"💊 Generating treatment recommendations for: {primary_condition}")

        # Step 1: Get treatments
        reasoning_chain.append("🔍 Querying MeTTa knowledge base for evidence-based treatments...")
        treatments = self.get_treatments_for_condition(primary_condition)

        if not treatments:
            reasoning_chain.append("⚠️ No specific treatments found in knowledge base")
            treatments = [f"Consult healthcare provider for {primary_condition} treatment"]

        reasoning_chain.append(f"📋 Found {len(treatments)} treatment options")

        # Step 2: Get evidence sources
        evidence_sources = {t: "Clinical guidelines (consult healthcare provider)" for t in treatments}

        # Step 3: Check contraindications
        reasoning_chain.append("⚕️ Performing safety validation...")
        contraindications = self.check_all_contraindications(
            treatments, patient_age, medical_history
        )

        # Step 4: Check drug interactions
        safety_warnings = self.check_drug_interactions(
            treatments, current_medications, allergies
        )

        if contraindications:
            reasoning_chain.append(f"⚠️ Contraindications found for {sum(len(v) for v in contraindications.values())} treatments")

        # Step 5: Specialist referral
        specialist = self.recommend_specialist(primary_condition, urgency_level)
        if specialist:
            reasoning_chain.append(f"🏥 Specialist referral recommended: {specialist}")

        # Step 6: Follow-up timeline
        follow_up = self.determine_follow_up_timeline(urgency_level, primary_condition)
        reasoning_chain.append(f"📅 Follow-up timeline: {follow_up}")

        # Add MeTTa safety warnings
        for treatment in treatments:
            metta_warnings = self.get_treatment_safety_warnings(treatment)
            safety_warnings.extend(metta_warnings)

        return {
            "treatments": treatments,
            "evidence_sources": evidence_sources,
            "contraindications": contraindications,
            "safety_warnings": list(set(safety_warnings)),
            "specialist_referral": specialist,
            "follow_up_timeline": follow_up,
            "reasoning_chain": reasoning_chain,
        }

    def get_treatments_for_condition(self, condition: str) -> List[str]:
        """Query MeTTa for treatments"""
        condition_normalized = condition.lower().replace(" ", "-")
        treatments = self.metta.get_treatment_recommendations(condition_normalized)
        return treatments if treatments else []

    def check_all_contraindications(
        self,
        treatments: List[str],
        patient_age: Optional[int] = None,
        medical_history: Optional[List[str]] = None,
    ) -> Dict[str, List[str]]:
        """Check contraindications"""
        all_contraindications = {}

        for treatment in treatments:
            contraindications = []
            treatment_normalized = treatment.lower().replace(" ", "-")

            # MeTTa contraindications
            metta_contraindications = self.metta.get_all_contraindications(treatment_normalized)
            contraindications.extend(metta_contraindications)

            # Age-based
            if patient_age is not None:
                if patient_age < 18 and "age-under-18" in metta_contraindications:
                    contraindications.append("Not approved for pediatric use")
                elif patient_age >= 65 and "age-over-65" in metta_contraindications:
                    contraindications.append("Use with caution in elderly patients")

            # Medical history
            if medical_history:
                for condition in medical_history:
                    condition_normalized = condition.lower().replace(" ", "-")
                    if condition_normalized in metta_contraindications:
                        contraindications.append(f"Contraindicated with {condition}")

                    # Dose adjustment
                    if self.metta.requires_dose_adjustment(treatment_normalized, condition_normalized):
                        contraindications.append(f"Dose adjustment required for {condition}")

            if contraindications:
                all_contraindications[treatment] = contraindications

        return all_contraindications

    def check_drug_interactions(
        self,
        treatments: List[str],
        current_medications: Optional[List[str]] = None,
        allergies: Optional[List[str]] = None,
    ) -> List[str]:
        """Check drug interactions"""
        warnings = []

        if current_medications:
            for treatment in treatments:
                treatment_normalized = treatment.lower().replace(" ", "-")
                for medication in current_medications:
                    medication_normalized = medication.lower().replace(" ", "-")
                    if self.metta.check_drug_interaction(treatment_normalized, medication_normalized):
                        warnings.append(f"⚠️ Drug interaction: {treatment} may interact with {medication}")

        if allergies:
            for treatment in treatments:
                treatment_lower = treatment.lower()
                for allergy in allergies:
                    allergy_lower = allergy.lower()
                    if allergy_lower in treatment_lower:
                        warnings.append(f"🚫 ALLERGY ALERT: {treatment} may contain {allergy}")

        return warnings

    def get_treatment_safety_warnings(self, treatment: str) -> List[str]:
        """Get MeTTa safety warnings"""
        treatment_normalized = treatment.lower().replace(" ", "-")
        warning_text = self.metta.get_safety_warning(treatment_normalized)
        return [warning_text] if warning_text else []

    def recommend_specialist(self, condition: str, urgency_level: str) -> Optional[str]:
        """Recommend specialist"""
        specialist_map = {
            "meningitis": "Neurologist or Infectious Disease Specialist (ER immediately)",
            "stroke": "Neurologist (ER immediately - time is brain)",
            "heart-attack": "Cardiologist (ER immediately - call 911)",
            "appendicitis": "General Surgeon (ER immediately)",
            "pneumonia": "Pulmonologist or Primary Care Physician",
            "migraine": "Neurologist",
            "covid-19": "Primary Care Physician or Infectious Disease Specialist",
            "influenza": "Primary Care Physician",
            "gastroenteritis": "Gastroenterologist or Primary Care Physician",
        }

        condition_normalized = condition.lower().replace(" ", "-")
        specialist = specialist_map.get(condition_normalized)

        if urgency_level == "emergency":
            return specialist if specialist else "Emergency Department immediately"

        return specialist

    def determine_follow_up_timeline(self, urgency_level: str, condition: str) -> str:
        """Determine follow-up timeline"""
        if urgency_level == "emergency":
            return "Immediate (ER visit required)"
        elif urgency_level == "urgent":
            time_critical_hours = self.metta.check_time_sensitivity(condition)
            if time_critical_hours and time_critical_hours <= 24:
                return f"Within {time_critical_hours} hours"
            return "Within 24 hours"
        else:
            return "1-2 weeks (or sooner if symptoms worsen)"


# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

class SessionData:
    def __init__(self, session_id: str, user_address: str):
        self.session_id = session_id
        self.user_address = user_address
        self.started_at = datetime.utcnow()
        self.messages_history = []

    def add_message(self, role: str, content: str):
        self.messages_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        })


active_sessions: Dict[str, SessionData] = {}


def get_or_create_session(sender: str) -> SessionData:
    if sender not in active_sessions:
        session_id = f"session-{uuid4()}"
        active_sessions[sender] = SessionData(session_id, sender)
    return active_sessions[sender]


def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end_session"))
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )


# ============================================================================
# AGENT INITIALIZATION
# ============================================================================

agent = Agent()

# Chat protocol for ASI:One
chat_proto = Protocol(spec=chat_protocol_spec)

# Initialize MeTTa engine (singleton)
metta_engine = None


def get_metta_engine() -> SimplifiedMeTTaEngine:
    """Get or create MeTTa engine instance"""
    global metta_engine
    if metta_engine is None:
        metta_engine = SimplifiedMeTTaEngine(METTA_KNOWLEDGE_BASE)
    return metta_engine


# ============================================================================
# CHAT PROTOCOL HANDLER (Monolithic Processing)
# ============================================================================

@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle chat messages from ASI:One users - MONOLITHIC PROCESSING"""
    ctx.logger.info(f"📨 [MONOLITHIC] Received chat message")

    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        )
    )

    session = get_or_create_session(sender)

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started: {session.session_id}")
            session.add_message("system", "Session started")

            welcome_msg = create_text_chat(
                "🏥 Welcome to MediChain AI!\n\n"
                "I'm your medical diagnostic assistant. I can help analyze your symptoms "
                "and provide preliminary health assessments.\n\n"
                "⚠️ IMPORTANT: This is NOT medical advice. Always consult a healthcare professional.\n\n"
                "Please describe your symptoms in detail."
            )
            await ctx.send(sender, welcome_msg)

        elif isinstance(item, TextContent):
            ctx.logger.info(f"📝 Text: {item.text[:50]}...")
            session.add_message("user", item.text)

            try:
                # ===== STEP 1: SYMPTOM EXTRACTION =====
                ctx.logger.info("🔬 STEP 1: Extracting symptoms...")
                symptoms = SymptomExtractor.extract_symptoms(item.text)
                age = SymptomExtractor.extract_age(item.text)

                if not symptoms:
                    ctx.logger.warning("No symptoms detected")
                    error_msg = create_text_chat(
                        "I didn't detect any specific symptoms. Could you describe what you're experiencing?\n\n"
                        "Examples:\n"
                        "• 'I have a fever and headache'\n"
                        "• 'My stomach hurts and I feel nauseous'\n"
                        "• 'I'm having chest pain and shortness of breath'"
                    )
                    await ctx.send(sender, error_msg)
                    continue

                symptom_list = ', '.join([s.name.replace('_', ' ').replace('-', ' ') for s in symptoms])
                ctx.logger.info(f"✅ Extracted {len(symptoms)} symptoms: {symptom_list}")

                # Send acknowledgement
                ack_message = (
                    f"✅ Information received:\n\n"
                    f"Symptoms: {symptom_list}\n"
                    f"{'Age: ' + str(age) if age else 'Age: Not provided'}\n\n"
                    f"Analyzing your symptoms..."
                )
                ack_msg = create_text_chat(ack_message)
                await ctx.send(sender, ack_msg)

                # ===== STEP 2: SYMPTOM ANALYSIS =====
                ctx.logger.info("🔬 STEP 2: Performing symptom analysis...")
                metta = get_metta_engine()
                analyzer = SymptomAnalyzer(metta)

                symptoms_normalized = [s.name for s in symptoms]
                severity_scores = {s.name: s.severity for s in symptoms if s.severity}

                analysis_result = analyzer.analyze_symptoms(
                    symptoms=symptoms_normalized,
                    age=age,
                    severity_scores=severity_scores if severity_scores else None,
                )

                ctx.logger.info(f"✅ Analysis complete! Urgency: {analysis_result['urgency_level'].upper()}")

                # Format analysis response
                red_flags_text = ""
                if analysis_result["red_flags"]:
                    red_flags_text = f"\n\n🚨 **RED FLAGS:**\n" + "\n".join([f"  • {rf}" for rf in analysis_result["red_flags"]])

                diff_diagnoses_text = "\n".join([
                    f"  {i+1}. {diagnosis} (confidence: {analysis_result['confidence_scores'].get(diagnosis, 0.0)*100:.0f}%)"
                    for i, diagnosis in enumerate(analysis_result["differential_diagnoses"][:5])
                ])

                analysis_text = (
                    f"🔬 **Symptom Analysis Complete**\n\n"
                    f"**Urgency:** {analysis_result['urgency_level'].upper()}\n\n"
                    f"**Differential Diagnoses:**\n{diff_diagnoses_text}"
                    f"{red_flags_text}\n\n"
                    f"**Next Step:** {analysis_result['recommended_next_step']}\n\n"
                    f"🔄 Fetching treatment recommendations..."
                )

                analysis_msg = create_text_chat(analysis_text)
                await ctx.send(sender, analysis_msg)

                # ===== STEP 3: TREATMENT RECOMMENDATION =====
                ctx.logger.info("💊 STEP 3: Generating treatment recommendations...")
                recommender = TreatmentRecommender(metta)

                primary_condition = analysis_result["differential_diagnoses"][0] if analysis_result["differential_diagnoses"] else "unknown"
                alternative_conditions = analysis_result["differential_diagnoses"][1:5] if len(analysis_result["differential_diagnoses"]) > 1 else None

                recommendations = recommender.recommend_treatments(
                    primary_condition=primary_condition,
                    alternative_conditions=alternative_conditions,
                    urgency_level=analysis_result["urgency_level"],
                    patient_age=age,
                )

                ctx.logger.info(f"✅ Recommendations generated!")

                # Format treatment response
                treatments_text = ""
                for i, treatment in enumerate(recommendations["treatments"][:5], 1):
                    evidence = recommendations["evidence_sources"].get(treatment, "No source")
                    contraindications = recommendations["contraindications"].get(treatment, [])

                    treatments_text += f"\n  **{i}. {treatment}**\n"
                    treatments_text += f"     Evidence: {evidence}\n"
                    if contraindications:
                        treatments_text += f"     ⚠️ Contraindications: {', '.join(contraindications)}\n"

                safety_text = ""
                if recommendations["safety_warnings"]:
                    safety_text = "\n\n🔐 **SAFETY WARNINGS:**\n" + "\n".join([f"  • {w}" for w in recommendations["safety_warnings"]])

                specialist_text = ""
                if recommendations["specialist_referral"]:
                    specialist_text = f"\n\n👨‍⚕️ **Specialist:** {recommendations['specialist_referral']}"

                followup_text = ""
                if recommendations["follow_up_timeline"]:
                    followup_text = f"\n\n📅 **Follow-Up:** {recommendations['follow_up_timeline']}"

                # Medical disclaimer
                disclaimer = (
                    "⚠️ IMPORTANT MEDICAL DISCLAIMER: This is an AI-powered preliminary "
                    "treatment recommendation based on medical knowledge graphs. This is NOT "
                    "a prescription or medical advice. Always consult a licensed healthcare "
                    "professional before starting any treatment. Do not use this information "
                    "to diagnose or treat any medical condition."
                )

                final_report = (
                    f"═══════════════════════════════════\n"
                    f"🏥 **MEDICHAIN AI - DIAGNOSTIC REPORT**\n"
                    f"═══════════════════════════════════\n\n"
                    f"**PRIMARY ASSESSMENT:** {primary_condition.replace('-', ' ').title()}\n\n"
                    f"**TREATMENTS:**{treatments_text}"
                    f"{safety_text}"
                    f"{specialist_text}"
                    f"{followup_text}\n\n"
                    f"═══════════════════════════════════\n"
                    f"⚠️ **DISCLAIMER**\n"
                    f"═══════════════════════════════════\n"
                    f"{disclaimer}\n\n"
                    f"Session: {session.session_id}"
                )

                final_msg = create_text_chat(final_report)
                await ctx.send(sender, final_msg)

                ctx.logger.info(f"✅ Complete diagnostic report sent")

            except Exception as e:
                ctx.logger.error(f"❌ Error during processing: {str(e)}")
                error_msg = create_text_chat(
                    f"An error occurred during analysis: {str(e)}\n\n"
                    f"Please consult a healthcare provider for proper medical assessment."
                )
                await ctx.send(sender, error_msg)

        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended: {session.session_id}")
            session.add_message("system", "Session ended")

            goodbye_msg = create_text_chat(
                "Thank you for using MediChain AI! Stay healthy! 🌟",
                end_session=True
            )
            await ctx.send(sender, goodbye_msg)

            if sender in active_sessions:
                del active_sessions[sender]


@chat_proto.on_message(ChatAcknowledgement)
async def handle_chat_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"✅ Acknowledgement received")


# ============================================================================
# STARTUP & INITIALIZATION
# ============================================================================

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("=" * 70)
    ctx.logger.info("MediChain AI - Monolithic Cloud Agent")
    ctx.logger.info("=" * 70)
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"MeTTa Available: {METTA_AVAILABLE}")
    ctx.logger.info(f"Chat Protocol: Enabled (ASI:One)")
    ctx.logger.info(f"Architecture: Monolithic (All-in-One)")
    ctx.logger.info("=" * 70)

    # Preload MeTTa engine
    ctx.logger.info("📚 Preloading MeTTa knowledge base...")
    try:
        metta = get_metta_engine()
        ctx.logger.info(f"✅ MeTTa engine ready (kb_loaded={metta.kb_loaded})")
    except Exception as e:
        ctx.logger.error(f"❌ Failed to load MeTTa engine: {str(e)}")

    ctx.logger.info("🚀 MediChain AI Monolithic Agent is READY")
    ctx.logger.info("=" * 70)


# Include chat protocol
agent.include(chat_proto, publish_manifest=True)
