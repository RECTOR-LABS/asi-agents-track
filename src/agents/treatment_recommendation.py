"""
Treatment Recommendation Agent - MediChain AI
Epic 3, Story 3.2: Specialized Treatment Agent

Purpose: Provide evidence-based treatment recommendations with comprehensive safety checks
Features:
- Treatment lookup from MeTTa knowledge base
- Evidence source linking (CDC, WHO, medical guidelines)
- Comprehensive contraindication checking
- Drug interaction validation
- Specialist referral recommendations
- Medical disclaimers and safety warnings

Port: 8005
"""

import os
import sys
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv

# Add project root to path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from uagents import Agent, Context, Protocol
from src.protocols import (
    TreatmentRequestMsg,
    TreatmentResponseMsg,
)
from src.metta.query_engine import MeTTaQueryEngine

# Load environment variables
load_dotenv()

# Agent configuration
AGENT_NAME = "medichain-treatment-recommendation"
AGENT_PORT = 8005
# Generate unique seed based on agent name to ensure unique address
BASE_SEED = os.getenv("AGENT_SEED", "default_seed_phrase_change_me")
AGENT_SEED = f"{BASE_SEED}_treatment_recommendation"

# README path for ASI:One discoverability
AGENT_README_PATH = os.path.join(os.path.dirname(__file__), "treatment_recommendation_readme.md")

# Initialize agent with mailbox
agent = Agent(
    name=AGENT_NAME,
    port=AGENT_PORT,
    seed=AGENT_SEED,
    mailbox=True,
    publish_agent_details=True,
    readme_path=AGENT_README_PATH,  # README for ASI:One agent discovery
)

# Initialize MeTTa query engine (singleton pattern)
metta_engine = None


def get_metta_engine() -> MeTTaQueryEngine:
    """Get or create MeTTa engine instance (singleton)"""
    global metta_engine
    if metta_engine is None:
        metta_engine = MeTTaQueryEngine()
    return metta_engine


# ============================================================================
# Treatment Recommendation Core Logic
# ============================================================================

class TreatmentRecommender:
    """
    Core treatment recommendation logic with MeTTa integration
    Provides evidence-based treatments with comprehensive safety validation
    """

    def __init__(self, metta_engine: MeTTaQueryEngine):
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
        """
        Main recommendation method - orchestrates all treatment recommendation steps (EPIC 7 - Phase 3 Enhanced)

        Returns dict with:
        - treatments: List[str]
        - treatment_protocol: List[Dict] (EPIC 7 - Phase 3) - Step-by-step protocol with timing
        - evidence_sources: Dict[str, str]
        - contraindications: Dict[str, List[str]]
        - safety_warnings: List[str]
        - specialist_referral: Optional[str]
        - follow_up_timeline: Optional[str]
        - reasoning_chain: List[str]
        """
        reasoning_chain = []
        reasoning_chain.append(f"💊 Generating treatment recommendations for: {primary_condition}")

        # Step 1: Get treatment recommendations from MeTTa
        reasoning_chain.append("🔍 Querying MeTTa knowledge base for evidence-based treatments...")
        treatments = self.get_treatments_for_condition(primary_condition)

        if not treatments:
            reasoning_chain.append("⚠️ No specific treatments found in knowledge base")
            treatments = [f"Consult healthcare provider for {primary_condition} treatment"]

        reasoning_chain.append(f"📋 Found {len(treatments)} treatment options")

        # Step 2: Get treatment protocol (EPIC 7 - Phase 3)
        treatment_protocol = self.get_treatment_protocol(primary_condition)
        if treatment_protocol:
            critical_steps = [s for s in treatment_protocol if s['priority'] == 'critical']
            reasoning_chain.append(f"📋 Retrieved treatment protocol: {len(treatment_protocol)} steps ({len(critical_steps)} critical)")
        else:
            reasoning_chain.append("📋 No structured protocol available for this condition")

        # Step 3: Get evidence sources
        reasoning_chain.append("📚 Retrieving evidence sources (CDC, WHO, medical guidelines)...")
        evidence_sources = self.get_evidence_sources(treatments)

        # Step 4: Check contraindications
        reasoning_chain.append("⚕️ Performing safety validation...")
        contraindications = self.check_all_contraindications(
            treatments, patient_age, medical_history
        )

        # Step 5: Check drug interactions
        safety_warnings = self.check_drug_interactions(
            treatments, current_medications, allergies
        )

        if contraindications:
            reasoning_chain.append(f"⚠️ Contraindications found for {sum(len(v) for v in contraindications.values())} treatments")

        if safety_warnings:
            reasoning_chain.append(f"⚠️ {len(safety_warnings)} safety warnings identified")

        # Step 6: Recommend specialist referral if needed
        specialist = self.recommend_specialist(primary_condition, urgency_level)
        if specialist:
            reasoning_chain.append(f"🏥 Specialist referral recommended: {specialist}")

        # Step 7: Determine follow-up timeline
        follow_up = self.determine_follow_up_timeline(urgency_level, primary_condition)
        reasoning_chain.append(f"📅 Follow-up timeline: {follow_up}")

        # Add treatment-specific safety warnings from MeTTa
        for treatment in treatments:
            metta_warnings = self.get_treatment_safety_warnings(treatment)
            safety_warnings.extend(metta_warnings)

        return {
            "treatments": treatments,
            "treatment_protocol": treatment_protocol,  # EPIC 7 - Phase 3
            "evidence_sources": evidence_sources,
            "contraindications": contraindications,
            "safety_warnings": list(set(safety_warnings)),  # Remove duplicates
            "specialist_referral": specialist,
            "follow_up_timeline": follow_up,
            "reasoning_chain": reasoning_chain,
        }

    def get_treatments_for_condition(self, condition: str) -> List[str]:
        """
        Query MeTTa for recommended treatments for the condition
        Returns list of treatment descriptions
        """
        # Normalize condition name for MeTTa query
        condition_normalized = condition.lower().replace(" ", "-")

        # Query MeTTa for treatments
        treatments = self.metta.get_treatment_recommendations(condition_normalized)

        if not treatments:
            return []

        # treatments is a list of treatment names
        return treatments

    def get_treatment_protocol(self, condition: str) -> List[Dict]:
        """
        Get step-by-step treatment protocol for critical conditions (EPIC 7 - Phase 3)

        Returns list of protocol steps with timing and priority:
        [
            {
                'step_number': 1,
                'action': 'call-911',
                'timing': 'immediate',
                'priority': 'critical'
            },
            ...
        ]
        """
        # Normalize condition name for MeTTa query
        condition_normalized = condition.lower().replace(" ", "-")

        # Query MeTTa for treatment protocol
        protocol_steps = self.metta.get_treatment_protocol(condition_normalized)

        if not protocol_steps:
            return []

        # Sort by step number to ensure correct order
        protocol_steps.sort(key=lambda x: x['step_number'])

        return protocol_steps

    def get_evidence_sources(self, treatments: List[str]) -> Dict[str, str]:
        """
        Get evidence source URLs for each treatment
        Links to CDC, WHO, medical guidelines
        """
        evidence_sources = {}

        for treatment in treatments:
            # Normalize treatment name for query
            treatment_normalized = treatment.lower().replace(" ", "-")

            # Query MeTTa for evidence source
            source = self.metta.get_evidence_source(treatment_normalized)

            if source:
                evidence_sources[treatment] = source
            else:
                # Default to general medical reference
                evidence_sources[treatment] = "Clinical guidelines (consult healthcare provider)"

        return evidence_sources

    def check_all_contraindications(
        self,
        treatments: List[str],
        patient_age: Optional[int] = None,
        medical_history: Optional[List[str]] = None,
    ) -> Dict[str, List[str]]:
        """
        Check contraindications for all treatments
        Returns dict of treatment -> list of contraindications
        """
        all_contraindications = {}

        for treatment in treatments:
            contraindications = []

            # Normalize treatment name
            treatment_normalized = treatment.lower().replace(" ", "-")

            # Query MeTTa for all contraindications
            metta_contraindications = self.metta.get_all_contraindications(treatment_normalized)
            contraindications.extend(metta_contraindications)

            # Age-based contraindications
            if patient_age is not None:
                if patient_age < 18:
                    # Check for pediatric contraindications
                    if "age-under-18" in metta_contraindications:
                        contraindications.append("Not approved for pediatric use")
                elif patient_age >= 65:
                    # Check for geriatric cautions
                    if "age-over-65" in metta_contraindications:
                        contraindications.append("Use with caution in elderly patients")

            # Medical history contraindications
            if medical_history:
                for condition in medical_history:
                    condition_normalized = condition.lower().replace(" ", "-")
                    if condition_normalized in metta_contraindications:
                        contraindications.append(f"Contraindicated with {condition}")

            # Check if dose adjustment needed
            if medical_history:
                for condition in medical_history:
                    condition_normalized = condition.lower().replace(" ", "-")
                    requires_adjustment = self.metta.requires_dose_adjustment(
                        treatment_normalized, condition_normalized
                    )
                    if requires_adjustment:
                        contraindications.append(f"Dose adjustment required for {condition}")

            # Only add to dict if contraindications exist
            if contraindications:
                all_contraindications[treatment] = contraindications

        return all_contraindications

    def check_drug_interactions(
        self,
        treatments: List[str],
        current_medications: Optional[List[str]] = None,
        allergies: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Check for drug-drug interactions and allergy conflicts
        Returns list of safety warnings
        """
        warnings = []

        # Check drug interactions
        if current_medications:
            for treatment in treatments:
                treatment_normalized = treatment.lower().replace(" ", "-")

                for medication in current_medications:
                    medication_normalized = medication.lower().replace(" ", "-")

                    # Query MeTTa for drug interaction
                    has_interaction = self.metta.check_drug_interaction(
                        treatment_normalized, medication_normalized
                    )

                    if has_interaction:
                        warnings.append(
                            f"⚠️ Drug interaction: {treatment} may interact with {medication}"
                        )

        # Check allergies
        if allergies:
            for treatment in treatments:
                treatment_lower = treatment.lower()

                for allergy in allergies:
                    allergy_lower = allergy.lower()

                    # Check if treatment contains allergen
                    if allergy_lower in treatment_lower:
                        warnings.append(
                            f"🚫 ALLERGY ALERT: {treatment} may contain {allergy} - Patient is allergic!"
                        )

                    # Check common allergen classes
                    if "penicillin" in allergy_lower and "antibiotic" in treatment_lower:
                        warnings.append(
                            f"⚠️ Caution: Patient has penicillin allergy. Verify {treatment} safety."
                        )

        return warnings

    def get_treatment_safety_warnings(self, treatment: str) -> List[str]:
        """
        Get safety warnings specific to the treatment from MeTTa
        """
        treatment_normalized = treatment.lower().replace(" ", "-")

        # Query MeTTa for safety warnings
        warning_text = self.metta.get_safety_warning(treatment_normalized)

        if warning_text:
            return [warning_text]

        return []

    def recommend_specialist(
        self, condition: str, urgency_level: str
    ) -> Optional[str]:
        """
        Recommend specialist type based on condition and urgency
        Returns specialist name or None
        """
        # Map conditions to specialists
        specialist_map = {
            "meningitis": "Neurologist or Infectious Disease Specialist (ER immediately)",
            "stroke": "Neurologist (ER immediately - time is brain)",
            "heart-attack": "Cardiologist (ER immediately - call 911)",
            "myocardial-infarction": "Cardiologist (ER immediately - call 911)",
            "appendicitis": "General Surgeon (ER immediately)",
            "pulmonary-embolism": "Pulmonologist or Emergency Medicine (ER immediately)",
            "sepsis": "Infectious Disease Specialist (ER immediately)",
            "pneumonia": "Pulmonologist or Primary Care Physician",
            "migraine": "Neurologist",
            "tension-headache": "Primary Care Physician or Neurologist",
            "covid-19": "Primary Care Physician or Infectious Disease Specialist",
            "influenza": "Primary Care Physician",
            "gastroenteritis": "Gastroenterologist or Primary Care Physician",
            "common-cold": "Primary Care Physician (if symptoms worsen)",
        }

        condition_normalized = condition.lower().replace(" ", "-")

        # Get specialist recommendation
        specialist = specialist_map.get(condition_normalized)

        # For emergency conditions, always recommend ER
        if urgency_level == "emergency":
            if specialist:
                return specialist
            return "Emergency Department immediately"

        return specialist

    def determine_follow_up_timeline(
        self, urgency_level: str, condition: str
    ) -> str:
        """
        Determine appropriate follow-up timeline based on urgency and condition
        """
        if urgency_level == "emergency":
            return "Immediate (ER visit required)"

        elif urgency_level == "urgent":
            # Check time-sensitivity from MeTTa
            time_critical_hours = self.metta.check_time_sensitivity(condition)
            if time_critical_hours and time_critical_hours <= 24:
                return f"Within {time_critical_hours} hours"
            return "Within 24 hours"

        else:  # routine
            return "1-2 weeks (or sooner if symptoms worsen)"


# ============================================================================
# Agent Protocol Handlers
# ============================================================================

# Create inter-agent protocol
treatment_recommendation_proto = Protocol(name="TreatmentRecommendationProtocol")


@treatment_recommendation_proto.on_message(model=TreatmentRequestMsg)
async def handle_treatment_request(
    ctx: Context, sender: str, msg: TreatmentRequestMsg
):
    """
    Handle treatment recommendation request from coordinator
    Performs comprehensive treatment analysis with safety validation
    """
    ctx.logger.info(f"📥 Received treatment recommendation request from {sender}")
    ctx.logger.info(f"   Session ID: {msg.session_id}")
    ctx.logger.info(f"   Primary condition: {msg.primary_condition}")
    ctx.logger.info(f"   Urgency: {msg.urgency_level}")
    ctx.logger.info(f"   Patient age: {msg.patient_age}")

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

        # Log results
        ctx.logger.info(f"✅ Recommendations generated!")
        ctx.logger.info(f"   Treatments: {len(recommendations['treatments'])}")
        ctx.logger.info(f"   Contraindications: {sum(len(v) for v in recommendations['contraindications'].values())}")
        ctx.logger.info(f"   Safety warnings: {len(recommendations['safety_warnings'])}")
        ctx.logger.info(f"   Specialist referral: {recommendations['specialist_referral']}")

        # Log reasoning chain
        ctx.logger.info("📋 Reasoning chain:")
        for step in recommendations["reasoning_chain"]:
            ctx.logger.info(f"   {step}")

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
            responding_agent=AGENT_NAME,
        )

        # Send response back to coordinator
        ctx.logger.info(f"📤 Sending treatment recommendations to {sender}")
        await ctx.send(sender, response)

    except Exception as e:
        ctx.logger.error(f"❌ Error during treatment recommendation: {str(e)}")
        ctx.logger.error(f"   Error type: {type(e).__name__}")

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
            responding_agent=AGENT_NAME,
        )
        await ctx.send(sender, error_response)


# Include protocol in agent
agent.include(treatment_recommendation_proto)


# ============================================================================
# Agent Lifecycle Events
# ============================================================================

@agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent on startup"""
    ctx.logger.info("=" * 70)
    ctx.logger.info(f"💊 {AGENT_NAME.upper()} - STARTING")
    ctx.logger.info("=" * 70)
    ctx.logger.info(f"📍 Agent Address: {agent.address}")
    ctx.logger.info(f"🌐 Port: {AGENT_PORT}")
    ctx.logger.info(f"📬 Mailbox: Enabled")
    ctx.logger.info("=" * 70)

    # Preload MeTTa engine
    ctx.logger.info("📚 Preloading MeTTa knowledge base...")
    try:
        metta = get_metta_engine()
        ctx.logger.info(f"✅ MeTTa engine ready")

        # Test query
        conditions_count = len(metta.query("(match &self (is-condition $c) $c)"))
        ctx.logger.info(f"✅ Knowledge base loaded: {conditions_count} conditions")
    except Exception as e:
        ctx.logger.error(f"❌ Failed to load MeTTa engine: {str(e)}")

    ctx.logger.info("🚀 Treatment Recommendation Agent is READY")
    ctx.logger.info("=" * 70)


@agent.on_event("shutdown")
async def shutdown(ctx: Context):
    """Cleanup on shutdown"""
    ctx.logger.info("=" * 70)
    ctx.logger.info(f"🛑 {AGENT_NAME.upper()} - SHUTTING DOWN")
    ctx.logger.info("=" * 70)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print(f"💊 MEDICHAIN AI - TREATMENT RECOMMENDATION AGENT")
    print("=" * 70)
    print(f"📍 Agent Name: {AGENT_NAME}")
    print(f"🌐 Port: {AGENT_PORT}")
    print(f"📬 Mailbox: Enabled")
    print("=" * 70)
    print()
    print("🔗 After agent starts, create mailbox via Agentverse Inspector:")
    print(f"   1. Copy inspector URL from logs")
    print(f"   2. Open in browser and click 'Connect'")
    print(f"   3. Select 'Mailbox' and click 'OK, got it'")
    print()
    print("✨ Starting agent...")
    print("=" * 70)

    agent.run()
