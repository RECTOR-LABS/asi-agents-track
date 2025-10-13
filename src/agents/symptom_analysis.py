"""
Symptom Analysis Agent - MediChain AI
Epic 3, Story 3.1: Specialized Diagnostic Agent

Purpose: Analyze symptom patterns to assess urgency and generate differential diagnoses
Features:
- Symptom pattern matching with MeTTa knowledge base
- Urgency classification (Emergency/Urgent/Routine)
- Differential diagnosis hypothesis generation (2-5 possibilities)
- Red flag symptom detection (life-threatening conditions)
- Multi-hop reasoning with confidence scoring

Port: 8004
"""

import os
import sys
from typing import List, Dict, Tuple, Optional
from dotenv import load_dotenv

# Add project root to path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from uagents import Agent, Context, Protocol
from src.protocols import (
    SymptomAnalysisRequestMsg,
    SymptomAnalysisResponseMsg,
)
from src.metta.query_engine import MeTTaQueryEngine

# Load environment variables
load_dotenv()

# Agent configuration
AGENT_NAME = "medichain-symptom-analysis"
AGENT_PORT = 8004
# Generate unique seed based on agent name to ensure unique address
BASE_SEED = os.getenv("AGENT_SEED", "default_seed_phrase_change_me")
AGENT_SEED = f"{BASE_SEED}_symptom_analysis"

# README path for ASI:One discoverability
AGENT_README_PATH = os.path.join(os.path.dirname(__file__), "symptom_analysis_readme.md")

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
# Symptom Analysis Core Logic
# ============================================================================

class SymptomAnalyzer:
    """
    Core symptom analysis logic with MeTTa integration
    Performs pattern matching, urgency assessment, and differential diagnosis
    """

    def __init__(self, metta_engine: MeTTaQueryEngine):
        self.metta = metta_engine

    def analyze_symptoms(
        self,
        symptoms: List[str],
        age: Optional[int] = None,
        severity_scores: Optional[Dict[str, int]] = None,
        medical_history: Optional[List[str]] = None,
        symptom_attributes: Optional[Dict[str, Dict[str, str]]] = None,
    ) -> Dict:
        """
        Main analysis method - orchestrates all symptom analysis steps

        Args:
            symptoms: List of symptom names
            age: Patient age (optional)
            severity_scores: Severity ratings for symptoms (optional)
            medical_history: Patient medical history (optional)
            symptom_attributes: EPIC 7 Phase 3 - Symptom characteristics (optional)
                Format: {
                    "chest-pain": {
                        "duration": "5-30-minutes",
                        "location": "substernal",
                        "character": "crushing",
                        "radiation": "left-arm"
                    }
                }

        Returns dict with:
        - urgency_level: str
        - red_flags: List[str]
        - differential_diagnoses: List[str]
        - confidence_scores: Dict[str, float]
        - risk_adjustments: Dict[str, Dict] (EPIC 7 - Phase 2)
        - attribute_matches: Dict[str, Dict] (EPIC 7 - Phase 3)
        - reasoning_chain: List[str]
        - recommended_next_step: str
        """
        reasoning_chain = []
        reasoning_chain.append(f"🔬 Analyzing {len(symptoms)} symptoms: {', '.join(symptoms)}")

        # Patient risk profile for EPIC 7 Phase 2
        if age:
            reasoning_chain.append(f"👤 Patient age: {age} years")
        if medical_history:
            reasoning_chain.append(f"📋 Medical history: {', '.join(medical_history)}")

        # Step 1: Detect red flags immediately
        red_flags = self.detect_red_flags(symptoms)
        if red_flags:
            reasoning_chain.append(f"⚠️ RED FLAGS DETECTED: {', '.join(red_flags)}")

        # Step 2: Match symptom attributes (EPIC 7 - Phase 3)
        attribute_matches = {}
        if symptom_attributes:
            reasoning_chain.append("🎯 Matching symptom attributes for precision diagnosis...")
            attribute_matches = self._match_symptom_attributes(symptom_attributes)

            # Log attribute match summary
            high_quality_matches = sum(1 for m in attribute_matches.values() if m['match_score'] >= 0.7)
            if high_quality_matches > 0:
                reasoning_chain.append(f"✓ High-quality attribute matches: {high_quality_matches}/{len(attribute_matches)}")

        # Step 3: Find matching conditions
        reasoning_chain.append("🔍 Querying MeTTa knowledge base for matching conditions...")
        condition_matches = self.find_matching_conditions(symptoms)
        reasoning_chain.append(f"📊 Found {len(condition_matches)} potential conditions")

        # Step 4: Calculate confidence scores with risk adjustment (EPIC 7 - Phase 2 + 3)
        confidence_scores, risk_adjustments = self.calculate_confidence_scores(
            symptoms, condition_matches, severity_scores, age, medical_history, attribute_matches
        )

        # Add risk-adjusted reasoning
        high_risk_conditions = [
            cond for cond, adjustment in risk_adjustments.items()
            if adjustment.get('risk_multiplier', 1.0) > 1.5
        ]
        if high_risk_conditions:
            reasoning_chain.append(f"⚡ Risk factors detected for: {', '.join(high_risk_conditions[:3])}")

        # Step 5: Assess urgency level
        urgency_level = self.assess_urgency(
            condition_matches, red_flags, confidence_scores, age
        )
        reasoning_chain.append(f"🚨 Urgency Assessment: {urgency_level.upper()}")

        # Step 6: Generate differential diagnoses (top 2-5)
        differential_diagnoses = self.generate_differential_diagnoses(
            confidence_scores, max_count=5
        )
        reasoning_chain.append(f"🎯 Top differential diagnoses: {', '.join(differential_diagnoses[:3])}")

        # Step 7: Recommend next step based on urgency
        recommended_next_step = self.recommend_action(urgency_level, red_flags)
        reasoning_chain.append(f"💡 Recommendation: {recommended_next_step}")

        return {
            "urgency_level": urgency_level,
            "red_flags": red_flags,
            "differential_diagnoses": differential_diagnoses,
            "confidence_scores": confidence_scores,
            "risk_adjustments": risk_adjustments,  # EPIC 7 - Phase 2
            "attribute_matches": attribute_matches,  # EPIC 7 - Phase 3
            "reasoning_chain": reasoning_chain,
            "recommended_next_step": recommended_next_step,
        }

    def detect_red_flags(self, symptoms: List[str]) -> List[str]:
        """
        Detect critical warning symptoms that require immediate attention
        Uses MeTTa to query for red flag symptoms
        """
        red_flags = []

        # Query MeTTa for red flag symptoms
        all_red_flags = self.metta.find_red_flag_symptoms()

        # Check if any patient symptoms match red flags
        for symptom in symptoms:
            symptom_normalized = symptom.lower().replace(" ", "-").replace("_", "-")
            if symptom_normalized in all_red_flags:
                red_flags.append(symptom)

        # Pattern matching for critical combinations
        symptom_set = set(s.lower() for s in symptoms)

        # Meningitis triad: severe headache + fever + neck stiffness/stiff neck
        normalized_symptom_set = set(s.replace(" ", "-") for s in symptom_set)
        has_headache = any(s in normalized_symptom_set for s in ["severe-headache", "headache"])
        has_fever = "fever" in normalized_symptom_set or "high-fever" in normalized_symptom_set
        has_stiff_neck = any(s in normalized_symptom_set for s in ["neck-stiffness", "stiff-neck", "neck-pain"])

        if has_headache and has_fever and has_stiff_neck:
            red_flags.append("Meningitis triad (headache + fever + neck stiffness)")

        # Stroke FAST: face drooping, arm weakness, speech difficulty
        stroke_symptoms = ["face-drooping", "arm-weakness", "speech-difficulty", "sudden-weakness"]
        if any(s.replace(" ", "-") in stroke_symptoms for s in symptom_set):
            red_flags.append("Stroke warning signs (FAST protocol)")

        # Cardiac symptoms
        if "chest-pain" in [s.replace(" ", "-") for s in symptom_set]:
            red_flags.append("Chest pain (potential cardiac emergency)")

        return red_flags

    def find_matching_conditions(self, symptoms: List[str]) -> List[str]:
        """
        Find medical conditions that match the given symptoms
        Uses MeTTa multi-symptom matching
        """
        # Normalize symptoms for MeTTa query
        normalized_symptoms = [
            s.lower().replace(" ", "-").replace("_", "-") for s in symptoms
        ]

        # Query MeTTa for conditions matching these symptoms
        # Returns dict: {'condition': match_count, ...}
        results = self.metta.find_conditions_by_symptoms(normalized_symptoms)

        # Extract condition names from dictionary keys
        conditions = list(results.keys()) if results else []

        return conditions

    def calculate_confidence_scores(
        self,
        symptoms: List[str],
        conditions: List[str],
        severity_scores: Optional[Dict[str, int]] = None,
        age: Optional[int] = None,
        medical_history: Optional[List[str]] = None,
        attribute_matches: Optional[Dict[str, Dict]] = None,
    ) -> Tuple[Dict[str, float], Dict[str, Dict]]:
        """
        Calculate confidence score for each possible condition (EPIC 7 - Phase 2+3 Enhanced)
        Based on symptom match percentage, severity weighting, RISK FACTORS, and ATTRIBUTE MATCHING

        Args:
            attribute_matches: Dict mapping symptoms to their attribute match details
                Format: {symptom: {match_score: 0.8, matched_attrs: [...], total_attrs: N}}

        Returns:
            Tuple of (confidence_scores, risk_adjustments)
            - confidence_scores: Dict[condition, final_confidence]
            - risk_adjustments: Dict[condition, {risk_multiplier, matched_factors, base_confidence, attribute_boost}]
        """
        confidence_scores = {}
        risk_adjustments = {}

        for condition in conditions:
            # Get all symptoms for this condition from MeTTa
            condition_symptoms = self.metta.find_symptoms_by_condition(condition)

            if not condition_symptoms:
                confidence_scores[condition] = 0.0
                risk_adjustments[condition] = {
                    'risk_multiplier': 1.0,
                    'matched_factors': [],
                    'base_confidence': 0.0
                }
                continue

            # Calculate base match score (% of condition symptoms present)
            normalized_patient_symptoms = set(
                s.lower().replace(" ", "-") for s in symptoms
            )
            matched_symptoms = normalized_patient_symptoms.intersection(
                set(condition_symptoms)
            )
            match_ratio = len(matched_symptoms) / len(condition_symptoms)

            # Apply severity weighting if available
            severity_weight = 1.0
            if severity_scores:
                avg_severity = sum(
                    severity_scores.get(s, 5) for s in matched_symptoms
                ) / max(len(matched_symptoms), 1)
                severity_weight = 0.5 + (avg_severity / 20.0)  # 0.5-1.0 range

            # Base confidence before adjustments
            base_confidence = match_ratio * severity_weight

            # EPIC 7 - Phase 2: Calculate risk multiplier
            risk_multiplier, matched_risk_factors = self._calculate_risk_multiplier(
                condition, age, medical_history
            )

            # EPIC 7 - Phase 3: Apply attribute matching boost
            attribute_boost = 1.0
            if attribute_matches:
                # Calculate average attribute match score for matched symptoms
                matched_symptom_scores = []
                for symptom in matched_symptoms:
                    if symptom in attribute_matches:
                        matched_symptom_scores.append(attribute_matches[symptom]['match_score'])

                if matched_symptom_scores:
                    avg_attr_match = sum(matched_symptom_scores) / len(matched_symptom_scores)
                    # Boost confidence by 0-20% based on attribute match quality
                    attribute_boost = 1.0 + (avg_attr_match * 0.2)

            # Apply all adjustments (capped at 0.99 to avoid overconfidence)
            final_confidence = min(base_confidence * risk_multiplier * attribute_boost, 0.99)
            confidence_scores[condition] = round(final_confidence, 2)

            # Track adjustment details
            risk_adjustments[condition] = {
                'risk_multiplier': round(risk_multiplier, 2),
                'matched_factors': matched_risk_factors,
                'base_confidence': round(base_confidence, 2),
                'attribute_boost': round(attribute_boost, 2)  # EPIC 7 - Phase 3
            }

        return confidence_scores, risk_adjustments

    def _calculate_risk_multiplier(
        self,
        condition: str,
        age: Optional[int] = None,
        medical_history: Optional[List[str]] = None,
    ) -> Tuple[float, List[str]]:
        """
        Calculate risk multiplier based on patient risk factors (EPIC 7 - Phase 2)

        Returns:
            Tuple of (risk_multiplier, matched_risk_factors)
            - risk_multiplier: 1.0 (no risk) to 2.5+ (very high risk)
            - matched_risk_factors: List of matched risk factor names
        """
        # Get all risk factors for this condition from KB
        risk_factors_data = self.metta.get_risk_factors(condition)

        if not risk_factors_data:
            return 1.0, []  # No risk factors defined

        # Build patient risk factor list
        patient_risk_factors = []

        # Add age-based risk factors
        if age:
            if age < 40:
                patient_risk_factors.append('age-under-40')
            elif age <= 55:
                patient_risk_factors.append('age-40-55')
            elif age <= 70:
                patient_risk_factors.append('age-55-70')
            else:
                patient_risk_factors.extend(['age-over-70', 'age-over-65'])

        # Add medical history risk factors (normalize)
        if medical_history:
            normalized_history = [
                h.lower().replace(" ", "-").replace("_", "-") for h in medical_history
            ]
            patient_risk_factors.extend(normalized_history)

        # Calculate risk score from matched factors
        matched_factors = []
        total_risk_score = 0.0

        for rf in risk_factors_data:
            factor_name = rf['factor']
            multiplier = rf['multiplier']

            # Check if patient has this risk factor
            if factor_name in patient_risk_factors:
                matched_factors.append(factor_name)
                total_risk_score += multiplier

        # Convert risk score to multiplier (1.0 = no additional risk, 2.5+ = very high risk)
        if total_risk_score == 0:
            risk_multiplier = 1.0  # No additional risk
        elif total_risk_score < 3.0:
            risk_multiplier = 1.0 + (total_risk_score / 10.0)  # 1.0-1.3 (low risk)
        elif total_risk_score < 6.0:
            risk_multiplier = 1.3 + (total_risk_score / 8.0)  # 1.3-2.0 (medium risk)
        else:
            risk_multiplier = 2.0 + (total_risk_score / 10.0)  # 2.0-2.5+ (high risk)

        return risk_multiplier, matched_factors

    def _match_symptom_attributes(
        self,
        patient_attributes: Dict[str, Dict[str, str]]
    ) -> Dict[str, Dict]:
        """
        Match patient-reported symptom attributes against knowledge base (EPIC 7 - Phase 3)

        Args:
            patient_attributes: Patient-reported symptom characteristics
                Format: {
                    "chest-pain": {
                        "duration": "5-30-minutes",
                        "location": "substernal",
                        "character": "crushing"
                    }
                }

        Returns:
            Dict mapping symptoms to match details:
            {
                symptom: {
                    'match_score': 0.8,  # 0.0-1.0
                    'matched_attrs': ['duration-typical', 'location-primary'],
                    'mismatched_attrs': ['character'],
                    'total_attrs': 3
                }
            }
        """
        match_results = {}

        for symptom, patient_attrs in patient_attributes.items():
            # Normalize symptom name
            symptom_normalized = symptom.lower().replace(" ", "-").replace("_", "-")

            # Get KB attributes for this symptom
            kb_attributes = self.metta.get_symptom_attributes(symptom_normalized)

            if not kb_attributes:
                # No KB attributes available for this symptom
                match_results[symptom_normalized] = {
                    'match_score': 0.5,  # Neutral score when no KB data
                    'matched_attrs': [],
                    'mismatched_attrs': [],
                    'total_attrs': 0,
                    'note': 'No KB attributes available'
                }
                continue

            # Match patient attributes against KB attributes
            matched_attrs = []
            mismatched_attrs = []

            for attr_key, patient_value in patient_attrs.items():
                # Normalize patient value
                patient_value_normalized = patient_value.lower().replace(" ", "-").replace("_", "-")

                # Find matching KB attribute types (e.g., "duration-typical", "location-primary")
                attr_matched = False
                for kb_attr_type, kb_values in kb_attributes.items():
                    # Check if attribute type matches (e.g., "duration" in "duration-typical")
                    if attr_key.lower() in kb_attr_type.lower():
                        # Check if patient value matches any KB value for this attribute
                        for kb_value in kb_values:
                            kb_value_normalized = kb_value.lower()

                            # Flexible matching: check substring or exact match
                            if (patient_value_normalized in kb_value_normalized or
                                kb_value_normalized in patient_value_normalized or
                                patient_value_normalized == kb_value_normalized):
                                matched_attrs.append(kb_attr_type)
                                attr_matched = True
                                break

                        if attr_matched:
                            break

                if not attr_matched:
                    mismatched_attrs.append(attr_key)

            # Calculate match score
            total_patient_attrs = len(patient_attrs)
            if total_patient_attrs > 0:
                match_score = len(matched_attrs) / total_patient_attrs
            else:
                match_score = 0.0

            match_results[symptom_normalized] = {
                'match_score': round(match_score, 2),
                'matched_attrs': matched_attrs,
                'mismatched_attrs': mismatched_attrs,
                'total_attrs': total_patient_attrs
            }

        return match_results

    def assess_urgency(
        self,
        conditions: List[str],
        red_flags: List[str],
        confidence_scores: Dict[str, float],
        age: Optional[int] = None,
    ) -> str:
        """
        Assess urgency level: emergency, urgent, or routine
        Based on red flags, condition severity, and confidence

        Urgency Thresholds:
        - Emergency: confidence > 0.5 AND (critical urgency OR time-sensitive < 6h)
        - Urgent: confidence > 0.3 AND (urgent urgency OR time-sensitive < 48h)
        - Routine: everything else
        """
        # Immediate emergency if red flags present
        if red_flags:
            return "emergency"

        # Check urgency level of top conditions from MeTTa
        emergency_conditions = self.metta.find_emergency_conditions()

        # Track highest urgency found
        highest_urgency = "routine"

        for condition, confidence in confidence_scores.items():
            # High confidence threshold for emergency (50%+)
            if confidence > 0.5:
                # Query urgency level from MeTTa
                urgency = self.metta.find_urgency_level(condition)

                if urgency == "emergency" or condition in emergency_conditions:
                    return "emergency"

                # Check time sensitivity for high-confidence conditions
                time_sensitive = self.metta.check_time_sensitivity(condition)
                if time_sensitive and time_sensitive <= 6:  # <6 hours critical
                    return "emergency"

                if urgency == "urgent-24h":
                    highest_urgency = "urgent"

            # Medium confidence threshold for urgent (30%+)
            elif confidence > 0.3:
                urgency = self.metta.find_urgency_level(condition)

                if urgency == "emergency" or condition in emergency_conditions:
                    highest_urgency = "urgent"  # Downgrade to urgent due to medium confidence
                elif urgency == "urgent-24h":
                    highest_urgency = "urgent"

                # Check time sensitivity for medium-confidence conditions
                time_sensitive = self.metta.check_time_sensitivity(condition)
                if time_sensitive and time_sensitive <= 48:  # <48 hours urgent
                    if highest_urgency == "routine":
                        highest_urgency = "urgent"

        # Age-based risk adjustment
        if age:
            if age < 5 or age > 65:
                # Higher risk groups - escalate urgency one level
                if any(confidence > 0.4 for confidence in confidence_scores.values()):
                    if highest_urgency == "routine":
                        highest_urgency = "urgent"

        return highest_urgency

    def generate_differential_diagnoses(
        self, confidence_scores: Dict[str, float], max_count: int = 5
    ) -> List[str]:
        """
        Generate list of differential diagnoses ranked by confidence
        Returns top 2-5 most likely conditions
        """
        # Sort by confidence descending
        sorted_conditions = sorted(
            confidence_scores.items(), key=lambda x: x[1], reverse=True
        )

        # Get top conditions with confidence > 0.2
        differential = [
            condition
            for condition, confidence in sorted_conditions[:max_count]
            if confidence > 0.2
        ]

        # Ensure at least 2 diagnoses if possible
        if len(differential) < 2 and len(sorted_conditions) >= 2:
            differential = [c for c, _ in sorted_conditions[:2]]

        return differential

    def recommend_action(self, urgency_level: str, red_flags: List[str]) -> str:
        """
        Recommend immediate action based on urgency assessment
        """
        if urgency_level == "emergency":
            if red_flags:
                return "🚨 EMERGENCY: Call 911 or go to ER immediately. Red flags detected."
            return "🚨 EMERGENCY: Seek immediate medical attention at ER."

        elif urgency_level == "urgent":
            return "⚠️ URGENT: Schedule medical appointment within 24 hours."

        else:  # routine
            return "📋 ROUTINE: Schedule appointment with primary care physician."


# ============================================================================
# Agent Protocol Handlers
# ============================================================================

# Create inter-agent protocol
symptom_analysis_proto = Protocol(name="SymptomAnalysisProtocol")


@symptom_analysis_proto.on_message(model=SymptomAnalysisRequestMsg)
async def handle_symptom_analysis_request(
    ctx: Context, sender: str, msg: SymptomAnalysisRequestMsg
):
    """
    Handle symptom analysis request from coordinator
    Performs comprehensive symptom analysis and returns assessment
    """
    ctx.logger.info(f"📥 Received symptom analysis request from {sender}")
    ctx.logger.info(f"   Session ID: {msg.session_id}")
    ctx.logger.info(f"   Symptoms: {msg.symptoms}")
    ctx.logger.info(f"   Patient age: {msg.age}")

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

        # Log results
        ctx.logger.info(f"✅ Analysis complete!")
        ctx.logger.info(f"   Urgency: {analysis_result['urgency_level'].upper()}")
        ctx.logger.info(f"   Red flags: {len(analysis_result['red_flags'])}")
        ctx.logger.info(f"   Differential diagnoses: {len(analysis_result['differential_diagnoses'])}")

        # Log reasoning chain
        ctx.logger.info("📋 Reasoning chain:")
        for step in analysis_result["reasoning_chain"]:
            ctx.logger.info(f"   {step}")

        # Create response
        response = SymptomAnalysisResponseMsg(
            session_id=msg.session_id,
            urgency_level=analysis_result["urgency_level"],
            red_flags=analysis_result["red_flags"],
            differential_diagnoses=analysis_result["differential_diagnoses"],
            confidence_scores=analysis_result["confidence_scores"],
            reasoning_chain=analysis_result["reasoning_chain"],
            recommended_next_step=analysis_result["recommended_next_step"],
            responding_agent=AGENT_NAME,
        )

        # Send response back to coordinator
        ctx.logger.info(f"📤 Sending analysis response to {sender}")
        await ctx.send(sender, response)

    except Exception as e:
        ctx.logger.error(f"❌ Error during symptom analysis: {str(e)}")
        ctx.logger.error(f"   Error type: {type(e).__name__}")

        # Send error response
        error_response = SymptomAnalysisResponseMsg(
            session_id=msg.session_id,
            urgency_level="routine",  # Safe default
            red_flags=[],
            differential_diagnoses=[],
            confidence_scores={},
            reasoning_chain=[f"Error occurred during analysis: {str(e)}"],
            recommended_next_step="Unable to complete analysis. Please consult healthcare provider.",
            responding_agent=AGENT_NAME,
        )
        await ctx.send(sender, error_response)


# Include protocol in agent
agent.include(symptom_analysis_proto)


# ============================================================================
# Agent Lifecycle Events
# ============================================================================

@agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent on startup"""
    ctx.logger.info("=" * 70)
    ctx.logger.info(f"🏥 {AGENT_NAME.upper()} - STARTING")
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

    ctx.logger.info("🚀 Symptom Analysis Agent is READY")
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
    print(f"🏥 MEDICHAIN AI - SYMPTOM ANALYSIS AGENT")
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
