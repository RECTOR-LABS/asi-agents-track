"""
MediChain AI - Coordinator Agent (Cloud Deployment)
Cloud-ready version with embedded MeTTa knowledge base and all dependencies inlined.

DEPLOYMENT: Copy this entire file to Agentverse Build tab for MediChain Coordinator agent.
"""

from datetime import datetime
from uuid import uuid4
from typing import Dict, Optional, List, Any
from enum import Enum

# Import uagents framework (available in Agentverse)
from uagents import Agent, Context, Protocol, Model
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

# ============================================================================
# AGENT ADDRESSES - Cloud Deployment Configuration
# ============================================================================

# Hard-coded agent addresses for cloud inter-agent communication
PATIENT_INTAKE_ADDRESS = "agent1qfxfjs7y6gxa8psr5mzugcg45j46znra4qg0t5mxljjv5g9mx7dw6238e4a"
SYMPTOM_ANALYSIS_ADDRESS = "agent1q036yw3pwsal2qsrq502k546lyxvnf6wt5l83qfhzhvceg6nm2la7nd6d5n"
TREATMENT_RECOMMENDATION_ADDRESS = "agent1q0q46ztah7cyw4z7gcg3mued9ncnrcvrcqc8kjku3hywqdzp03e36hk5qsl"

# ============================================================================
# MESSAGE MODELS (Inline - no external imports)
# ============================================================================

class UrgencyLevel(str, Enum):
    """Urgency classification for medical conditions"""
    EMERGENCY = "emergency"
    URGENT = "urgent"
    ROUTINE = "routine"


class Symptom(Model):
    """Patient symptom data"""
    name: str
    raw_text: str
    severity: Optional[int] = 5
    duration: Optional[str] = None


class PatientIntakeData(Model):
    """Structured patient intake data"""
    session_id: str
    symptoms: List[Symptom]
    age: Optional[int] = None
    timestamp: datetime
    medical_history: Optional[List[str]] = None
    allergies: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None


class IntakeTextMessage(Model):
    """Message from user to patient intake agent"""
    text: str
    session_id: str


class AgentAcknowledgement(Model):
    """Acknowledgement message from specialist agents"""
    session_id: str
    agent_name: str
    message: str


class DiagnosticRequest(Model):
    """Request for diagnostic analysis"""
    session_id: str
    patient_data: PatientIntakeData
    requesting_agent: str
    analysis_type: str = "symptom_analysis"


class SymptomAnalysisRequestMsg(Model):
    """Request for symptom analysis from coordinator to symptom analysis agent"""
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
# SESSION MANAGEMENT
# ============================================================================

class SessionData:
    """Store data for an active session"""
    def __init__(self, session_id: str, user_address: str):
        self.session_id = session_id
        self.user_address = user_address
        self.started_at = datetime.utcnow()
        self.patient_data: Optional[PatientIntakeData] = None
        self.symptom_analysis_response: Optional[SymptomAnalysisResponseMsg] = None
        self.treatment_response: Optional[TreatmentResponseMsg] = None
        self.messages_history = []

    def add_message(self, role: str, content: str):
        """Add message to history"""
        self.messages_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        })


# Global session store
active_sessions: Dict[str, SessionData] = {}


def get_or_create_session(sender: str) -> SessionData:
    """Get existing session or create new one"""
    if sender not in active_sessions:
        session_id = f"session-{uuid4()}"
        active_sessions[sender] = SessionData(session_id, sender)
    return active_sessions[sender]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    """Create a ChatMessage with text content."""
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

# Initialize the chat protocol
chat_proto = Protocol(spec=chat_protocol_spec)

# Initialize inter-agent protocol
inter_agent_proto = Protocol(name="MediChainProtocol")


# ============================================================================
# CHAT PROTOCOL HANDLERS (ASI:One Interface)
# ============================================================================

@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages from ASI:One users"""
    ctx.logger.info(f"Received chat message from {sender}")

    # Always acknowledge
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        )
    )

    # Get or create session
    session = get_or_create_session(sender)

    # Process each content item
    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started: {session.session_id} with {sender}")
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
            ctx.logger.info(f"Text from {sender}: {item.text}")
            session.add_message("user", item.text)

            # Route to Patient Intake Agent for symptom extraction
            intake_msg = IntakeTextMessage(
                text=item.text,
                session_id=session.session_id
            )

            ctx.logger.info(f"Routing to Patient Intake: {PATIENT_INTAKE_ADDRESS}")
            await ctx.send(PATIENT_INTAKE_ADDRESS, intake_msg)

            # Acknowledge to user
            ack_msg = create_text_chat(
                "Analyzing your symptoms... Please wait a moment."
            )
            await ctx.send(sender, ack_msg)

        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended: {session.session_id}")
            session.add_message("system", "Session ended")

            goodbye_msg = create_text_chat(
                "Thank you for using MediChain AI! Stay healthy! 🌟",
                end_session=True
            )
            await ctx.send(sender, goodbye_msg)

            # Clean up session
            if sender in active_sessions:
                del active_sessions[sender]


@chat_proto.on_message(ChatAcknowledgement)
async def handle_chat_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgements from users"""
    ctx.logger.info(f"Received acknowledgement from {sender}")


# ============================================================================
# INTER-AGENT PROTOCOL HANDLERS
# ============================================================================

@inter_agent_proto.on_message(model=DiagnosticRequest)
async def handle_diagnostic_request(ctx: Context, sender: str, msg: DiagnosticRequest):
    """
    Handle diagnostic requests from Patient Intake Agent
    Route to appropriate specialist agents
    """
    ctx.logger.info(f"Received diagnostic request from {sender}")
    ctx.logger.info(f"Session: {msg.session_id}, Analysis type: {msg.analysis_type}")

    # Find the user session
    user_session = None
    for addr, session in active_sessions.items():
        if session.session_id == msg.session_id:
            user_session = session
            session.patient_data = msg.patient_data
            break

    if not user_session:
        ctx.logger.warning(f"No active session found for {msg.session_id}")
        return

    ctx.logger.info(f"Processing diagnostic request for user: {user_session.user_address}")

    # Prepare symptom analysis request
    symptoms_list = [s.name for s in msg.patient_data.symptoms]
    severity_scores = {s.name: s.severity for s in msg.patient_data.symptoms if s.severity}
    duration_info = {s.name: s.duration for s in msg.patient_data.symptoms if s.duration}

    analysis_request = SymptomAnalysisRequestMsg(
        session_id=msg.session_id,
        symptoms=symptoms_list,
        age=msg.patient_data.age,
        severity_scores=severity_scores if severity_scores else None,
        duration_info=duration_info if duration_info else None,
        medical_history=msg.patient_data.medical_history,
        requesting_agent="medichain-coordinator",
    )

    ctx.logger.info(f"Routing to Symptom Analysis Agent: {SYMPTOM_ANALYSIS_ADDRESS}")
    ctx.logger.info(f"  Symptoms: {symptoms_list}")
    ctx.logger.info(f"  Age: {msg.patient_data.age}")

    # Send to Symptom Analysis Agent
    await ctx.send(SYMPTOM_ANALYSIS_ADDRESS, analysis_request)

    # Acknowledge to user
    ack_msg = create_text_chat("🔬 Performing comprehensive symptom analysis...")
    await ctx.send(user_session.user_address, ack_msg)


@inter_agent_proto.on_message(model=SymptomAnalysisResponseMsg)
async def handle_symptom_analysis_response(ctx: Context, sender: str, msg: SymptomAnalysisResponseMsg):
    """
    Handle symptom analysis response from Symptom Analysis Agent
    Route to Treatment Recommendation Agent for next step
    """
    ctx.logger.info(f"📥 Received symptom analysis response from {sender}")
    ctx.logger.info(f"   Session: {msg.session_id}")
    ctx.logger.info(f"   Urgency: {msg.urgency_level}")

    # Find session
    user_session = None
    for addr, session in active_sessions.items():
        if session.session_id == msg.session_id:
            user_session = session
            session.symptom_analysis_response = msg
            break

    if not user_session:
        ctx.logger.warning(f"No active session for {msg.session_id}")
        return

    # Send analysis results to user
    red_flags_text = ""
    if msg.red_flags:
        red_flags_text = f"\n\n🚨 **RED FLAGS DETECTED:**\n" + "\n".join([f"  • {rf}" for rf in msg.red_flags])

    diff_diagnoses_text = "\n".join([
        f"  {i+1}. {diagnosis} (confidence: {msg.confidence_scores.get(diagnosis, 0.0)*100:.0f}%)"
        for i, diagnosis in enumerate(msg.differential_diagnoses[:5])
    ])

    analysis_text = (
        f"🔬 **Symptom Analysis Complete**\n\n"
        f"**Urgency Level:** {msg.urgency_level.upper()}\n\n"
        f"**Top Differential Diagnoses:**\n{diff_diagnoses_text}"
        f"{red_flags_text}\n\n"
        f"**Recommended Action:** {msg.recommended_next_step}\n\n"
        f"🔄 Fetching treatment recommendations..."
    )

    user_msg = create_text_chat(analysis_text)
    await ctx.send(user_session.user_address, user_msg)

    # Route to Treatment Recommendation Agent
    primary_condition = msg.differential_diagnoses[0] if msg.differential_diagnoses else "unknown"
    alternative_conditions = msg.differential_diagnoses[1:5] if len(msg.differential_diagnoses) > 1 else None

    treatment_request = TreatmentRequestMsg(
        session_id=msg.session_id,
        primary_condition=primary_condition,
        alternative_conditions=alternative_conditions,
        urgency_level=msg.urgency_level,
        patient_age=user_session.patient_data.age if user_session.patient_data else None,
        allergies=user_session.patient_data.allergies if user_session.patient_data else None,
        current_medications=user_session.patient_data.current_medications if user_session.patient_data else None,
        medical_history=user_session.patient_data.medical_history if user_session.patient_data else None,
        requesting_agent="medichain-coordinator",
    )

    ctx.logger.info(f"Routing to Treatment Recommendation Agent: {TREATMENT_RECOMMENDATION_ADDRESS}")

    # Send to Treatment Recommendation Agent
    await ctx.send(TREATMENT_RECOMMENDATION_ADDRESS, treatment_request)


@inter_agent_proto.on_message(model=TreatmentResponseMsg)
async def handle_treatment_response(ctx: Context, sender: str, msg: TreatmentResponseMsg):
    """
    Handle treatment recommendation response from Treatment Recommendation Agent
    Send final comprehensive report to user
    """
    ctx.logger.info(f"📥 Received treatment recommendations from {sender}")

    # Find session
    user_session = None
    for addr, session in active_sessions.items():
        if session.session_id == msg.session_id:
            user_session = session
            session.treatment_response = msg
            break

    if not user_session:
        ctx.logger.warning(f"No active session for {msg.session_id}")
        return

    # Format final comprehensive report
    treatments_text = ""
    for i, treatment in enumerate(msg.treatments[:5], 1):
        evidence = msg.evidence_sources.get(treatment, "No source available")
        contraindications = msg.contraindications.get(treatment, [])

        treatments_text += f"\n  **{i}. {treatment}**\n"
        treatments_text += f"     Evidence: {evidence}\n"
        if contraindications:
            treatments_text += f"     ⚠️ Contraindications: {', '.join(contraindications)}\n"

    # Safety warnings section
    safety_text = ""
    if msg.safety_warnings:
        safety_text = "\n\n🔐 **SAFETY WARNINGS:**\n" + "\n".join([f"  • {w}" for w in msg.safety_warnings])

    # Specialist referral section
    specialist_text = ""
    if msg.specialist_referral:
        specialist_text = f"\n\n👨‍⚕️ **Specialist Referral:** {msg.specialist_referral}"

    # Follow-up section
    followup_text = ""
    if msg.follow_up_timeline:
        followup_text = f"\n\n📅 **Follow-Up:** {msg.follow_up_timeline}"

    # Compile final report
    final_report = (
        f"═══════════════════════════════════\n"
        f"🏥 **MEDICHAIN AI - DIAGNOSTIC REPORT**\n"
        f"═══════════════════════════════════\n\n"
        f"**PRIMARY ASSESSMENT:** {msg.condition.replace('-', ' ').title()}\n\n"
        f"**TREATMENT RECOMMENDATIONS:**{treatments_text}"
        f"{safety_text}"
        f"{specialist_text}"
        f"{followup_text}\n\n"
        f"═══════════════════════════════════\n"
        f"⚠️ **IMPORTANT DISCLAIMER**\n"
        f"═══════════════════════════════════\n"
        f"{msg.medical_disclaimer}\n\n"
        f"Session ID: {msg.session_id}"
    )

    # Send final report to user
    final_msg = create_text_chat(final_report)
    await ctx.send(user_session.user_address, final_msg)

    ctx.logger.info(f"✅ Complete diagnostic report sent to user")


# ============================================================================
# STARTUP & INITIALIZATION
# ============================================================================

@agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize coordinator agent"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("MediChain AI Coordinator Agent (Cloud)")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"Mailbox: Enabled (ASI:One compatible)")
    ctx.logger.info(f"Chat Protocol: Enabled")
    ctx.logger.info("=" * 60)


# Include protocols
agent.include(chat_proto, publish_manifest=True)
agent.include(inter_agent_proto)
