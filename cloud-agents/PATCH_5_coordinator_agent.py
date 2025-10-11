"""
MediChain AI - Coordinator Agent (Cloud Deployment - PATCHED v5)
Ultra-simplified message models (no nested types) to match Patient Intake v5.

DEPLOYMENT: Replace the existing coordinator agent.py with this patched version.
"""

from datetime import datetime
from uuid import uuid4
from typing import Dict, Optional, List
import json

# Import uagents framework
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
# AGENT ADDRESSES
# ============================================================================

PATIENT_INTAKE_ADDRESS = "agent1qfxfjs7y6gxa8psr5mzugcg45j46znra4qg0t5mxljjv5g9mx7dw6238e4a"
SYMPTOM_ANALYSIS_ADDRESS = "agent1q036yw3pwsal2qsrq502k546lyxvnf6wt5l83qfhzhvceg6nm2la7nd6d5n"
TREATMENT_RECOMMENDATION_ADDRESS = "agent1q0q46ztah7cyw4z7gcg3mued9ncnrcvrcqc8kjku3hywqdzp03e36hk5qsl"

# ============================================================================
# MESSAGE MODELS - Ultra-simplified (matching Patient Intake v5)
# ============================================================================

class IntakeTextMessage(Model):
    """Message to patient intake - ULTRA SIMPLE"""
    text: str
    session_id: str


class AgentAcknowledgement(Model):
    """Acknowledgement from agents - ULTRA SIMPLE"""
    session_id: str
    agent_name: str
    message: str


class DiagnosticRequest(Model):
    """Diagnostic request with JSON serialization"""
    session_id: str
    patient_data_json: str  # JSON string instead of nested Model
    requesting_agent: str
    analysis_type: str


class SymptomAnalysisRequestMsg(Model):
    """Request for symptom analysis"""
    session_id: str
    symptoms: List[str]
    age: Optional[int] = None
    severity_scores: Optional[Dict[str, int]] = None
    duration_info: Optional[Dict[str, str]] = None
    medical_history: Optional[List[str]] = None
    requesting_agent: str


class SymptomAnalysisResponseMsg(Model):
    """Response from symptom analysis"""
    session_id: str
    urgency_level: str
    red_flags: List[str]
    differential_diagnoses: List[str]
    confidence_scores: Dict[str, float]
    reasoning_chain: List[str]
    recommended_next_step: str
    responding_agent: str


class TreatmentRequestMsg(Model):
    """Request for treatment"""
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
    """Response from treatment"""
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
    def __init__(self, session_id: str, user_address: str):
        self.session_id = session_id
        self.user_address = user_address
        self.started_at = datetime.utcnow()
        self.patient_data: Optional[dict] = None
        self.symptom_analysis_response: Optional[SymptomAnalysisResponseMsg] = None
        self.treatment_response: Optional[TreatmentResponseMsg] = None
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


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

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


# ============================================================================
# CHAT PROTOCOL HANDLERS
# ============================================================================

@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle chat messages from ASI:One users"""
    ctx.logger.info(f"📨 [PATCH v5] Received chat message")

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

            intake_msg = IntakeTextMessage(
                text=item.text,
                session_id=session.session_id
            )

            ctx.logger.info(f"📤 Routing to Patient Intake: {PATIENT_INTAKE_ADDRESS}")
            await ctx.send(PATIENT_INTAKE_ADDRESS, intake_msg)

            ack_msg = create_text_chat("Analyzing your symptoms... Please wait a moment.")
            await ctx.send(sender, ack_msg)

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
# INTER-AGENT MESSAGE HANDLERS
# ============================================================================

@agent.on_message(model=AgentAcknowledgement)
async def handle_agent_acknowledgement(ctx: Context, sender: str, msg: AgentAcknowledgement):
    """Handle acknowledgements from Patient Intake"""
    ctx.logger.info(f"✅ [v5] Acknowledgement from {msg.agent_name}")
    ctx.logger.info(f"   Session: {msg.session_id}")

    user_session = None
    for addr, session in active_sessions.items():
        if session.session_id == msg.session_id:
            user_session = session
            break

    if not user_session:
        ctx.logger.warning(f"No active session for {msg.session_id}")
        return

    user_msg = create_text_chat(msg.message)
    await ctx.send(user_session.user_address, user_msg)


@agent.on_message(model=DiagnosticRequest)
async def handle_diagnostic_request(ctx: Context, sender: str, msg: DiagnosticRequest):
    """Handle diagnostic requests from Patient Intake (JSON deserialization)"""
    ctx.logger.info(f"📥 [v5] Diagnostic request from {sender}")
    ctx.logger.info(f"   Session: {msg.session_id}")

    user_session = None
    for addr, session in active_sessions.items():
        if session.session_id == msg.session_id:
            user_session = session
            break

    if not user_session:
        ctx.logger.warning(f"No active session for {msg.session_id}")
        return

    # Deserialize JSON patient data
    try:
        patient_data = json.loads(msg.patient_data_json)
        user_session.patient_data = patient_data
    except json.JSONDecodeError as e:
        ctx.logger.error(f"Failed to parse patient_data_json: {e}")
        return

    # Extract symptoms
    symptoms = patient_data.get("symptoms", [])
    symptoms_list = [s["name"] for s in symptoms]
    severity_scores = {s["name"]: s["severity"] for s in symptoms if s.get("severity")}
    duration_info = {s["name"]: s["duration"] for s in symptoms if s.get("duration")}

    analysis_request = SymptomAnalysisRequestMsg(
        session_id=msg.session_id,
        symptoms=symptoms_list,
        age=patient_data.get("age"),
        severity_scores=severity_scores if severity_scores else None,
        duration_info=duration_info if duration_info else None,
        medical_history=patient_data.get("medical_history"),
        requesting_agent="medichain-coordinator",
    )

    ctx.logger.info(f"📤 Routing to Symptom Analysis: {SYMPTOM_ANALYSIS_ADDRESS}")
    ctx.logger.info(f"   Symptoms: {symptoms_list}")

    await ctx.send(SYMPTOM_ANALYSIS_ADDRESS, analysis_request)

    ack_msg = create_text_chat("🔬 Performing comprehensive symptom analysis...")
    await ctx.send(user_session.user_address, ack_msg)


@agent.on_message(model=SymptomAnalysisResponseMsg)
async def handle_symptom_analysis_response(ctx: Context, sender: str, msg: SymptomAnalysisResponseMsg):
    """Handle symptom analysis response"""
    ctx.logger.info(f"📥 Symptom analysis from {sender}")
    ctx.logger.info(f"   Urgency: {msg.urgency_level}")

    user_session = None
    for addr, session in active_sessions.items():
        if session.session_id == msg.session_id:
            user_session = session
            session.symptom_analysis_response = msg
            break

    if not user_session:
        ctx.logger.warning(f"No active session for {msg.session_id}")
        return

    red_flags_text = ""
    if msg.red_flags:
        red_flags_text = f"\n\n🚨 **RED FLAGS:**\n" + "\n".join([f"  • {rf}" for rf in msg.red_flags])

    diff_diagnoses_text = "\n".join([
        f"  {i+1}. {diagnosis} (confidence: {msg.confidence_scores.get(diagnosis, 0.0)*100:.0f}%)"
        for i, diagnosis in enumerate(msg.differential_diagnoses[:5])
    ])

    analysis_text = (
        f"🔬 **Symptom Analysis Complete**\n\n"
        f"**Urgency:** {msg.urgency_level.upper()}\n\n"
        f"**Differential Diagnoses:**\n{diff_diagnoses_text}"
        f"{red_flags_text}\n\n"
        f"**Next Step:** {msg.recommended_next_step}\n\n"
        f"🔄 Fetching treatment recommendations..."
    )

    user_msg = create_text_chat(analysis_text)
    await ctx.send(user_session.user_address, user_msg)

    primary_condition = msg.differential_diagnoses[0] if msg.differential_diagnoses else "unknown"
    alternative_conditions = msg.differential_diagnoses[1:5] if len(msg.differential_diagnoses) > 1 else None

    treatment_request = TreatmentRequestMsg(
        session_id=msg.session_id,
        primary_condition=primary_condition,
        alternative_conditions=alternative_conditions,
        urgency_level=msg.urgency_level,
        patient_age=user_session.patient_data.get("age") if user_session.patient_data else None,
        allergies=user_session.patient_data.get("allergies") if user_session.patient_data else None,
        current_medications=user_session.patient_data.get("current_medications") if user_session.patient_data else None,
        medical_history=user_session.patient_data.get("medical_history") if user_session.patient_data else None,
        requesting_agent="medichain-coordinator",
    )

    ctx.logger.info(f"📤 Routing to Treatment: {TREATMENT_RECOMMENDATION_ADDRESS}")
    await ctx.send(TREATMENT_RECOMMENDATION_ADDRESS, treatment_request)


@agent.on_message(model=TreatmentResponseMsg)
async def handle_treatment_response(ctx: Context, sender: str, msg: TreatmentResponseMsg):
    """Handle treatment recommendations"""
    ctx.logger.info(f"📥 Treatment recommendations from {sender}")

    user_session = None
    for addr, session in active_sessions.items():
        if session.session_id == msg.session_id:
            user_session = session
            session.treatment_response = msg
            break

    if not user_session:
        ctx.logger.warning(f"No active session for {msg.session_id}")
        return

    treatments_text = ""
    for i, treatment in enumerate(msg.treatments[:5], 1):
        evidence = msg.evidence_sources.get(treatment, "No source")
        contraindications = msg.contraindications.get(treatment, [])

        treatments_text += f"\n  **{i}. {treatment}**\n"
        treatments_text += f"     Evidence: {evidence}\n"
        if contraindications:
            treatments_text += f"     ⚠️ Contraindications: {', '.join(contraindications)}\n"

    safety_text = ""
    if msg.safety_warnings:
        safety_text = "\n\n🔐 **SAFETY WARNINGS:**\n" + "\n".join([f"  • {w}" for w in msg.safety_warnings])

    specialist_text = ""
    if msg.specialist_referral:
        specialist_text = f"\n\n👨‍⚕️ **Specialist:** {msg.specialist_referral}"

    followup_text = ""
    if msg.follow_up_timeline:
        followup_text = f"\n\n📅 **Follow-Up:** {msg.follow_up_timeline}"

    final_report = (
        f"═══════════════════════════════════\n"
        f"🏥 **MEDICHAIN AI - DIAGNOSTIC REPORT**\n"
        f"═══════════════════════════════════\n\n"
        f"**PRIMARY ASSESSMENT:** {msg.condition.replace('-', ' ').title()}\n\n"
        f"**TREATMENTS:**{treatments_text}"
        f"{safety_text}"
        f"{specialist_text}"
        f"{followup_text}\n\n"
        f"═══════════════════════════════════\n"
        f"⚠️ **DISCLAIMER**\n"
        f"═══════════════════════════════════\n"
        f"{msg.medical_disclaimer}\n\n"
        f"Session: {msg.session_id}"
    )

    final_msg = create_text_chat(final_report)
    await ctx.send(user_session.user_address, final_msg)

    ctx.logger.info(f"✅ Complete diagnostic report sent")


# ============================================================================
# STARTUP
# ============================================================================

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("=" * 60)
    ctx.logger.info("MediChain AI Coordinator (PATCH v5)")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"Chat Protocol: Enabled (ASI:One)")
    ctx.logger.info(f"Inter-Agent: Ultra-simplified models (no nesting)")
    ctx.logger.info("=" * 60)


# Include chat protocol
agent.include(chat_proto, publish_manifest=True)
