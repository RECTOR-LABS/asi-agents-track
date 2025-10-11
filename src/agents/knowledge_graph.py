"""
Knowledge Graph Agent - MeTTa-powered diagnostic reasoning
MediChain AI - ASI Agents Track Hackathon
"""

from uagents import Agent, Context, Model, Protocol
from uagents.setup import fund_agent_if_low
import os
import sys
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from dotenv import load_dotenv

# Import our message protocols
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.protocols import (
    DiagnosticRequest,
    DiagnosticResponse,
    PossibleCondition,
    AgentAcknowledgement,
    UrgencyLevel,
    ConfidenceLevel,
)

# Import MeTTa Query Engine
from src.metta.query_engine import MeTTaQueryEngine

# Load environment variables
load_dotenv()


# ============================================================================
# Knowledge Graph Agent Configuration
# ============================================================================

agent = Agent(
    name="medichain-knowledge-graph",
    seed=os.getenv("AGENT_SEED", "knowledge_graph_seed_dev") + "_kg",
    port=8003,  # Use different port (8000=coordinator, 8001=patient_intake, 8002=in use)
    mailbox=True,  # Enable Agentverse mailbox for inter-agent communication
    publish_agent_details=True,  # Publish agent details for discoverability
)

# Create protocol for inter-agent communication
knowledge_proto = Protocol(name="KnowledgeGraphProtocol")


# ============================================================================
# MeTTa Query Engine Integration
# ============================================================================

# Initialize MeTTa query engine (singleton)
metta_engine: Optional[MeTTaQueryEngine] = None


def get_metta_engine() -> MeTTaQueryEngine:
    """Get or initialize MeTTa query engine"""
    global metta_engine
    if metta_engine is None:
        metta_engine = MeTTaQueryEngine()
    return metta_engine


# ============================================================================
# Diagnostic Reasoning Logic
# ============================================================================

class DiagnosticReasoner:
    """Implements multi-hop reasoning and diagnostic logic using MeTTa KB"""

    def __init__(self, engine: MeTTaQueryEngine):
        self.engine = engine

    def analyze_symptoms(
        self,
        symptom_names: List[str],
        patient_age: Optional[int] = None,
        patient_conditions: Optional[List[str]] = None
    ) -> Dict:
        """
        Perform comprehensive diagnostic analysis

        Returns:
            Dictionary with:
            - ranked_conditions: List of (condition, confidence_score) tuples
            - emergency_flags: List of emergency conditions detected
            - reasoning: Detailed reasoning for top conditions
            - red_flags: List of red flag symptoms detected
            - recommendations: Treatment and action recommendations
        """
        # Step 1: Multi-symptom matching with scoring
        symptom_names_normalized = [s.replace('_', '-') for s in symptom_names]
        condition_matches = self.engine.find_conditions_by_symptoms(symptom_names_normalized)

        # Step 2: Rank conditions by match count (confidence)
        total_symptoms = len(symptom_names_normalized)
        ranked = []
        for condition, match_count in condition_matches.items():
            confidence = (match_count / total_symptoms) * 100 if total_symptoms > 0 else 0
            ranked.append((condition, match_count, confidence))

        # Sort by match count descending, then by urgency
        ranked.sort(key=lambda x: x[1], reverse=True)

        # Step 3: Check for emergency conditions
        emergency_conditions = self.engine.find_emergency_conditions()
        emergency_flags = [
            cond for cond, _, _ in ranked
            if cond in str(emergency_conditions)
        ]

        # Step 4: Detect red flag symptoms
        all_red_flags = self.engine.find_red_flag_symptoms()
        detected_red_flags = [
            symptom for symptom in symptom_names_normalized
            if symptom in str(all_red_flags)
        ]

        # Step 5: Generate reasoning for top 3 conditions
        reasoning_chains = {}
        for condition, match_count, confidence in ranked[:3]:
            reasoning = self.engine.generate_reasoning_chain(
                symptom_names_normalized,
                condition
            )
            reasoning_chains[condition] = reasoning

        # Step 6: Get treatment recommendations with safety checks
        recommendations = {}
        for condition, _, _ in ranked[:3]:
            treatments = self.engine.get_treatment_recommendations(condition)
            action = self.engine.get_required_action(condition)
            severity = self.engine.find_severity_level(condition)
            urgency = self.engine.find_urgency_level(condition)

            # Check contraindications if patient conditions provided
            safe_treatments = []
            contraindication_warnings = []

            for treatment in treatments:
                treatment_str = str(treatment).strip("'[]")
                is_safe = True

                if patient_conditions:
                    for patient_condition in patient_conditions:
                        if self.engine.check_contraindication(treatment_str, patient_condition):
                            is_safe = False
                            contraindication_warnings.append(
                                f"{treatment_str} contraindicated for {patient_condition}"
                            )

                if is_safe:
                    # Get safety warning
                    safety_warning = self.engine.get_safety_warning(treatment_str)
                    safe_treatments.append({
                        "treatment": treatment_str,
                        "evidence": self.engine.get_evidence_source(treatment_str),
                        "safety_warning": safety_warning
                    })

            recommendations[condition] = {
                "action": str(action),
                "treatments": safe_treatments,
                "severity": str(severity),
                "urgency": str(urgency),
                "contraindication_warnings": contraindication_warnings,
                "time_sensitive_hours": self.engine.check_time_sensitivity(condition)
            }

        # Step 7: Multi-hop reasoning - check differential diagnoses
        differential_diagnoses = {}
        for condition, _, _ in ranked[:3]:
            diffs = self.engine.find_differential_diagnoses(condition)
            if diffs:
                differential_diagnoses[condition] = [str(d) for d in diffs]

        return {
            "ranked_conditions": ranked,
            "emergency_flags": emergency_flags,
            "red_flags": detected_red_flags,
            "reasoning_chains": reasoning_chains,
            "recommendations": recommendations,
            "differential_diagnoses": differential_diagnoses,
            "total_conditions_matched": len(ranked)
        }

    def handle_uncertainty(self, ranked_conditions: List[Tuple], threshold: int = 2) -> str:
        """
        Generate message when dealing with multiple possible diagnoses

        Args:
            ranked_conditions: List of (condition, match_count, confidence) tuples
            threshold: Minimum match count to consider condition viable

        Returns:
            Human-readable uncertainty message
        """
        viable_conditions = [c for c in ranked_conditions if c[1] >= threshold]

        if len(viable_conditions) == 0:
            return ("⚠️ UNCERTAIN DIAGNOSIS\n\n"
                   "Based on the symptoms provided, I cannot confidently identify a specific condition. "
                   "Please seek medical attention for a proper evaluation.")

        if len(viable_conditions) == 1:
            return (f"✅ PRIMARY DIAGNOSIS\n\n"
                   f"Based on symptom analysis, {viable_conditions[0][0]} is the most likely condition "
                   f"(confidence: {viable_conditions[0][2]:.0f}%).")

        # Multiple viable conditions
        condition_list = '\n'.join([
            f"  {i+1}. {cond[0]} (confidence: {cond[2]:.0f}%, {cond[1]} symptom matches)"
            for i, cond in enumerate(viable_conditions[:3])
        ])

        return (f"⚠️ MULTIPLE POSSIBLE DIAGNOSES\n\n"
               f"Your symptoms match multiple conditions:\n\n"
               f"{condition_list}\n\n"
               f"A healthcare provider can perform additional tests to determine the exact diagnosis.")


# ============================================================================
# Message Handlers
# ============================================================================

@knowledge_proto.on_message(model=DiagnosticRequest)
async def handle_diagnostic_request(ctx: Context, sender: str, msg: DiagnosticRequest):
    """
    Process diagnostic request using MeTTa knowledge graph
    Perform multi-hop reasoning and return comprehensive analysis
    """
    ctx.logger.info(f"📊 Received diagnostic request from {sender}")
    ctx.logger.info(f"   Session: {msg.session_id}")
    ctx.logger.info(f"   Requesting agent: {msg.requesting_agent}")
    ctx.logger.info(f"   Analysis type: {msg.analysis_type}")

    # Extract symptom names from patient data
    symptom_names = [symptom.name for symptom in msg.patient_data.symptoms]
    ctx.logger.info(f"   Symptoms to analyze: {symptom_names}")

    # Initialize MeTTa engine
    engine = get_metta_engine()
    reasoner = DiagnosticReasoner(engine)

    # Perform diagnostic analysis
    ctx.logger.info("🧠 Performing MeTTa-powered diagnostic reasoning...")
    analysis = reasoner.analyze_symptoms(
        symptom_names=symptom_names,
        patient_age=msg.patient_data.age
    )

    ctx.logger.info(f"   ✅ Analysis complete: {analysis['total_conditions_matched']} conditions matched")

    # Generate uncertainty message if needed
    uncertainty_message = reasoner.handle_uncertainty(analysis['ranked_conditions'])
    ctx.logger.info(f"   Uncertainty assessment: {uncertainty_message.split(chr(10))[0]}")

    # Prepare diagnostic results using PossibleCondition model
    possible_conditions = []
    reasoning_chain = []

    # Top condition (primary diagnosis)
    if analysis['ranked_conditions']:
        top_condition = analysis['ranked_conditions'][0]
        condition_name = top_condition[0]
        match_count = top_condition[1]
        confidence_pct = top_condition[2]

        # Get recommendation details
        rec = analysis['recommendations'].get(condition_name, {})

        # Format reasoning chain
        reasoning_text = analysis['reasoning_chains'].get(condition_name, "")
        reasoning_chain.append(reasoning_text)

        # Determine confidence level
        if confidence_pct >= 80:
            conf_level = ConfidenceLevel.HIGH
        elif confidence_pct >= 50:
            conf_level = ConfidenceLevel.MEDIUM
        else:
            conf_level = ConfidenceLevel.LOW

        # Extract matching symptom names
        matching_symptoms = [s.replace('-', '_') for s in symptom_names]

        # Build primary result
        primary_result = PossibleCondition(
            condition_name=condition_name,
            confidence=confidence_pct / 100.0,  # Convert to 0-1 range
            confidence_level=conf_level,
            matching_symptoms=matching_symptoms[:match_count],
            reasoning=f"{uncertainty_message}\n\nSeverity: {rec.get('severity', 'unknown')}\nAction: {rec.get('action', 'consult-doctor')}",
            metta_query_used=f"find_conditions_by_symptoms({symptom_names_normalized})"
        )
        possible_conditions.append(primary_result)

        ctx.logger.info(f"   Primary diagnosis: {condition_name} ({confidence_pct:.0f}% confidence)")

        # Add secondary diagnoses (differential)
        for condition, match_count, confidence_pct in analysis['ranked_conditions'][1:3]:
            if match_count >= 1:  # At least 1 symptom match
                if confidence_pct >= 60:
                    conf_level = ConfidenceLevel.MEDIUM
                else:
                    conf_level = ConfidenceLevel.LOW

                secondary_result = PossibleCondition(
                    condition_name=condition,
                    confidence=confidence_pct / 100.0,
                    confidence_level=conf_level,
                    matching_symptoms=matching_symptoms[:match_count],
                    reasoning=f"Alternative diagnosis with {match_count} symptom matches",
                    metta_query_used=f"differential_diagnosis({condition})"
                )
                possible_conditions.append(secondary_result)

    # Determine urgency level
    if analysis['emergency_flags'] or analysis['red_flags']:
        urgency = UrgencyLevel.EMERGENCY
    elif possible_conditions and possible_conditions[0].confidence >= 0.7:
        # Check if top condition is urgent
        top_cond_name = possible_conditions[0].condition_name
        rec = analysis['recommendations'].get(top_cond_name, {})
        urgency_str = str(rec.get('urgency', 'routine')).strip("[]'")

        if 'emergency' in urgency_str:
            urgency = UrgencyLevel.EMERGENCY
        elif 'urgent' in urgency_str:
            urgency = UrgencyLevel.URGENT
        else:
            urgency = UrgencyLevel.ROUTINE
    else:
        urgency = UrgencyLevel.ROUTINE

    # Build diagnostic response
    response = DiagnosticResponse(
        session_id=msg.session_id,
        possible_conditions=possible_conditions,
        urgency_level=urgency,
        red_flags=analysis['red_flags'],
        reasoning_chain=reasoning_chain if reasoning_chain else ["MeTTa knowledge graph analysis performed"],
        responding_agent="knowledge_graph"
    )

    ctx.logger.info(f"📤 Sending diagnostic response back to {sender}")
    await ctx.send(sender, response)

    # Also send acknowledgement for transparency
    if urgency == UrgencyLevel.EMERGENCY:
        ack_msg = "🚨 EMERGENCY DETECTED - Immediate medical attention required!"
    else:
        ack_msg = f"✅ Diagnostic analysis complete ({len(possible_conditions)} possible conditions identified)"

    ack = AgentAcknowledgement(
        session_id=msg.session_id,
        agent_name="knowledge_graph",
        message=ack_msg
    )
    await ctx.send(sender, ack)


@agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent and MeTTa engine on startup"""
    ctx.logger.info(f"🧠 Knowledge Graph Agent started!")
    ctx.logger.info(f"   Agent address: {agent.address}")
    ctx.logger.info(f"   Agent name: {agent.name}")
    ctx.logger.info(f"   Mailbox: Enabled")

    # Initialize MeTTa engine
    try:
        engine = get_metta_engine()
        ctx.logger.info(f"   ✅ MeTTa Query Engine initialized")
        ctx.logger.info(f"   Knowledge base loaded: 13 conditions, 200+ facts")
        ctx.logger.info(f"   Query methods available: 21")
        ctx.logger.info(f"   Ready for diagnostic reasoning!")
    except Exception as e:
        ctx.logger.error(f"   ❌ Failed to initialize MeTTa engine: {e}")


# Include the knowledge graph protocol
agent.include(knowledge_proto)


if __name__ == "__main__":
    agent.run()
