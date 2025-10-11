"""
MediChain AI - Treatment Recommendation Agent (Cloud Deployment)
Cloud-ready version with embedded MeTTa knowledge base for treatment lookup and safety validation.

DEPLOYMENT: Copy this entire file to Agentverse Build tab for MediChain Treatment agent.

NOTE: This agent requires the 'hyperon' package. If not available in Agentverse,
it will use fallback rule-based logic.
"""

from datetime import datetime
from typing import List, Dict, Optional

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

class TreatmentRequestMsg(Model):
    """Request for treatment recommendations"""
    session_id: str
    primary_condition: str
    alternative_conditions: Optional[List[str]] = None
    urgency_level: str
    patient_age: Optional[int] = None
    allergies: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None
    medical_history: Optional[List[str]] = None
    requesting_agent: str


class TreatmentResponseMsg(Model):
    """Response from treatment recommendation agent"""
    session_id: str
    condition: str
    treatments: List[str]
    evidence_sources: Dict[str, str]
    contraindications: Dict[str, List[str]]
    safety_warnings: List[str]
    specialist_referral: Optional[str] = None
    follow_up_timeline: Optional[str] = None
    medical_disclaimer: str
    responding_agent: str


# ============================================================================
# EMBEDDED MeTTa KNOWLEDGE BASE (v1.1 - SAME AS SYMPTOM ANALYSIS)
# ============================================================================

# NOTE: Same 585-line KB - reused for treatment/contraindication lookup
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

(is-condition meningitis)
(is-condition stroke)
(is-condition heart-attack)
(is-condition myocardial-infarction)
(is-condition appendicitis)
(is-condition pulmonary-embolism)
(is-condition sepsis)
(is-condition pneumonia)
(is-condition covid-19)
(is-condition migraine)
(is-condition influenza)
(is-condition gastroenteritis)
(is-condition tension-headache)
(is-condition common-cold)

;; ========================================
;; TREATMENTS & CONTRAINDICATIONS
;; ========================================

;; MENINGITIS
(has-treatment meningitis immediate-911)
(has-treatment meningitis emergency-antibiotics)
(has-treatment meningitis hospital-admission)
(requires-action meningitis call-911-immediately)
(contraindication emergency-antibiotics severe-allergy-penicillin)

;; STROKE
(has-treatment stroke immediate-911)
(has-treatment stroke tPA-within-3-hours)
(requires-action stroke call-911-note-time)
(contraindication tPA-within-3-hours recent-surgery)
(contraindication tPA-within-3-hours active-bleeding)
(contraindication tPA-within-3-hours bleeding-disorder)
(safety-warning tPA-within-3-hours "3-hour window critical. Note symptom start time.")

;; HEART ATTACK
(has-treatment heart-attack immediate-911)
(has-treatment heart-attack aspirin-immediately)
(has-treatment heart-attack cardiac-catheterization)
(requires-action heart-attack chew-aspirin-call-911)
(contraindication aspirin-immediately bleeding-disorder)
(contraindication aspirin-immediately active-bleeding)
(contraindication aspirin-immediately aspirin-allergy)
(contraindication aspirin-immediately age-under-18)
(safety-warning aspirin-immediately "Chew, don't swallow whole. Call 911 immediately.")

;; APPENDICITIS
(has-treatment appendicitis emergency-department-evaluation)
(has-treatment appendicitis surgical-appendectomy)
(has-treatment appendicitis antibiotics)
(requires-action appendicitis seek-emergency-care)

;; PULMONARY EMBOLISM
(has-treatment pulmonary-embolism immediate-911)
(has-treatment pulmonary-embolism anticoagulation)
(has-treatment pulmonary-embolism thrombolysis)
(contraindication anticoagulation active-bleeding)
(contraindication anticoagulation recent-surgery)
(contraindication anticoagulation bleeding-disorder)
(contraindication anticoagulation pregnancy-concern)
(safety-warning anticoagulation "High bleeding risk. Avoid contact sports.")

;; SEPSIS
(has-treatment sepsis immediate-911)
(has-treatment sepsis broad-spectrum-antibiotics)
(has-treatment sepsis IV-fluids)
(requires-action sepsis emergency-department-immediately)

;; PNEUMONIA
(has-treatment pneumonia antibiotics-bacterial)
(has-treatment pneumonia antivirals-viral)
(has-treatment pneumonia rest-and-fluids)
(has-treatment pneumonia oxygen-therapy)
(requires-action pneumonia see-doctor-within-24h)
(contraindication antibiotics-bacterial severe-allergy-penicillin)
(contraindication antibiotics severe-liver-disease)
(contraindication antibiotics severe-kidney-disease)
(requires-dose-adjustment antibiotics kidney-disease)

;; MIGRAINE
(has-treatment migraine triptans)
(has-treatment migraine NSAIDs)
(has-treatment migraine rest-dark-room)
(has-treatment migraine preventive-medications)
(requires-action migraine schedule-doctor-appointment)
(contraindication triptans heart-disease)
(contraindication triptans uncontrolled-hypertension)
(contraindication triptans pregnancy)
(contraindication NSAIDs kidney-disease)
(contraindication NSAIDs stomach-ulcers)
(contraindication NSAIDs heart-failure)
(contraindication NSAIDs pregnancy-third-trimester)
(requires-dose-adjustment NSAIDs elderly)

;; INFLUENZA
(has-treatment influenza antiviral-medications)
(has-treatment influenza rest-and-fluids)
(has-treatment influenza symptom-management)
(has-treatment influenza fever-reducers)
(requires-action influenza rest-at-home)
(contraindication antiviral-medications kidney-disease)
(contraindication antiviral-medications severe-asthma)
(requires-dose-adjustment antivirals kidney-disease)
(safety-warning rest-and-fluids "Monitor for worsening symptoms. Seek care if deteriorating.")

;; COVID-19
(has-treatment covid-19 isolation)
(has-treatment covid-19 antiviral-paxlovid)
(has-treatment covid-19 rest-and-fluids)
(has-treatment covid-19 oxygen-if-severe)
(requires-action covid-19 get-tested-isolate)
(contraindication antiviral-paxlovid severe-kidney-disease)
(contraindication antiviral-paxlovid severe-liver-disease)
(contraindication antiviral-paxlovid drug-interaction-statins)
(drug-interaction antiviral-paxlovid statins)

;; GASTROENTERITIS
(has-treatment gastroenteritis oral-rehydration)
(has-treatment gastroenteritis rest)
(has-treatment gastroenteritis bland-diet)
(requires-action gastroenteritis hydrate-and-rest)

;; TENSION HEADACHE
(has-treatment tension-headache over-counter-pain-relievers)
(has-treatment tension-headache stress-management)
(has-treatment tension-headache muscle-relaxation)
(requires-action tension-headache self-care)

;; COMMON COLD
(has-treatment common-cold rest)
(has-treatment common-cold fluids)
(has-treatment common-cold symptom-relief)
(requires-action common-cold self-care-at-home)
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
    """Simplified MeTTa query engine for cloud deployment"""

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
        """Initialize fallback knowledge base"""
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
# AGENT INITIALIZATION
# ============================================================================

agent = Agent()

# Create inter-agent protocol
treatment_recommendation_proto = Protocol(name="TreatmentRecommendationProtocol")

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

@treatment_recommendation_proto.on_message(model=TreatmentRequestMsg)
async def handle_treatment_request(ctx: Context, sender: str, msg: TreatmentRequestMsg):
    """Handle treatment recommendation request"""
    ctx.logger.info(f"📥 Received treatment recommendation request from {sender}")
    ctx.logger.info(f"   Session ID: {msg.session_id}")
    ctx.logger.info(f"   Primary condition: {msg.primary_condition}")

    try:
        # Initialize recommender
        metta = get_metta_engine()
        recommender = TreatmentRecommender(metta)

        # Generate recommendations
        ctx.logger.info("💊 Generating treatment recommendations...")
        recommendations = recommender.recommend_treatments(
            primary_condition=msg.primary_condition,
            alternative_conditions=msg.alternative_conditions,
            urgency_level=msg.urgency_level,
            patient_age=msg.patient_age,
            allergies=msg.allergies,
            current_medications=msg.current_medications,
            medical_history=msg.medical_history,
        )

        ctx.logger.info(f"✅ Recommendations generated!")

        # Medical disclaimer
        disclaimer = (
            "⚠️ IMPORTANT MEDICAL DISCLAIMER: This is an AI-powered preliminary "
            "treatment recommendation based on medical knowledge graphs. This is NOT "
            "a prescription or medical advice. Always consult a licensed healthcare "
            "professional before starting any treatment. Do not use this information "
            "to diagnose or treat any medical condition."
        )

        # Create response
        response = TreatmentResponseMsg(
            session_id=msg.session_id,
            condition=msg.primary_condition,
            treatments=recommendations["treatments"],
            evidence_sources=recommendations["evidence_sources"],
            contraindications=recommendations["contraindications"],
            safety_warnings=recommendations["safety_warnings"],
            specialist_referral=recommendations["specialist_referral"],
            follow_up_timeline=recommendations["follow_up_timeline"],
            medical_disclaimer=disclaimer,
            responding_agent="medichain-treatment-recommendation",
        )

        # Send response
        ctx.logger.info(f"📤 Sending treatment recommendations to {sender}")
        await ctx.send(sender, response)

    except Exception as e:
        ctx.logger.error(f"❌ Error during treatment recommendation: {str(e)}")

        # Send error response
        error_response = TreatmentResponseMsg(
            session_id=msg.session_id,
            condition=msg.primary_condition,
            treatments=["Unable to generate recommendations. Please consult healthcare provider."],
            evidence_sources={},
            contraindications={},
            safety_warnings=[f"Error occurred: {str(e)}"],
            specialist_referral="Healthcare Provider",
            follow_up_timeline="As soon as possible",
            medical_disclaimer="Error occurred during recommendation generation. Consult healthcare provider.",
            responding_agent="medichain-treatment-recommendation",
        )
        await ctx.send(sender, error_response)


# Include protocol
agent.include(treatment_recommendation_proto)


# ============================================================================
# STARTUP & INITIALIZATION
# ============================================================================

@agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent on startup"""
    ctx.logger.info("=" * 70)
    ctx.logger.info("MediChain AI - Treatment Recommendation Agent (Cloud)")
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

    ctx.logger.info("🚀 Treatment Recommendation Agent is READY")
    ctx.logger.info("=" * 70)
