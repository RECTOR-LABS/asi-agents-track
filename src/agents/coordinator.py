"""
Coordinator Agent - Main routing agent with Chat Protocol for ASI:One
Enhanced with session management and multi-agent routing
"""

from datetime import datetime
from uuid import uuid4, UUID
from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)
import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Import message protocols
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.protocols import (
    DiagnosticRequest,
    DiagnosticResponse,
    TreatmentResponse,
    FinalDiagnosticReport,
    PatientIntakeData,
    IntakeTextMessage,
    AgentAcknowledgementMsg,  # CRITICAL FIX: Mailbox-compatible clarification handler
    # Epic 3: Symptom Analysis & Treatment Recommendation
    SymptomAnalysisRequestMsg,
    SymptomAnalysisResponseMsg,
    TreatmentRequestMsg,
    TreatmentResponseMsg,
)

# Import input validation
from src.utils.input_validation import validate_input

# Load environment variables
load_dotenv()


# ============================================================================
# Session Management
# ============================================================================

class SessionData:
    """Store data for an active session"""
    def __init__(self, session_id: str, user_address: str):
        self.session_id = session_id
        self.user_address = user_address
        self.started_at = datetime.utcnow()
        self.patient_data: Optional[PatientIntakeData] = None
        self.diagnostic_response: Optional[DiagnosticResponse] = None
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


# Global session store (in production, use persistent storage like Redis)
# TODO: Implement persistent storage for production deployment
active_sessions: Dict[str, SessionData] = {}

# Session cleanup configuration
SESSION_TIMEOUT_SECONDS = 7200  # 2 hours


def get_or_create_session(sender: str) -> SessionData:
    """Get existing session or create new one"""
    if sender not in active_sessions:
        session_id = f"session-{uuid4()}"
        active_sessions[sender] = SessionData(session_id, sender)
    return active_sessions[sender]


def cleanup_expired_sessions(ctx: Context):
    """Remove expired sessions to prevent memory leaks"""
    now = datetime.utcnow()
    expired_addresses = []

    for addr, session in active_sessions.items():
        session_age = (now - session.started_at).total_seconds()
        if session_age > SESSION_TIMEOUT_SECONDS:
            expired_addresses.append(addr)
            ctx.logger.info(f"Session expired for {addr}: {session.session_id} (age: {session_age/3600:.1f} hours)")

    # Remove expired sessions
    for addr in expired_addresses:
        del active_sessions[addr]

    if expired_addresses:
        ctx.logger.info(f"Cleaned up {len(expired_addresses)} expired sessions")

    return len(expired_addresses)


# ============================================================================
# Coordinator Agent Initialization
# ============================================================================

# README path for ASI:One discoverability
AGENT_README_PATH = os.path.join(os.path.dirname(__file__), "coordinator_readme.md")

agent = Agent(
    name="medichain-coordinator",
    seed=os.getenv("AGENT_SEED", "coordinator_seed_phrase"),
    port=8001,  # Local inspector port (different from patient_intake's 8000)
    mailbox=True,  # Enable Agentverse mailbox for ASI:One discoverability
    publish_agent_details=True,  # Publish agent details for better discoverability
    readme_path=AGENT_README_PATH,  # README for ASI:One agent discovery
)

# Initialize the chat protocol
chat_proto = Protocol(spec=chat_protocol_spec)

# Initialize inter-agent protocol
inter_agent_proto = Protocol(name="MediChainProtocol")


# ============================================================================
# Utility Functions
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
# Chat Protocol Handlers (ASI:One Interface)
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

            # ============================================================
            # INPUT VALIDATION - Handle edge cases before routing
            # ============================================================
            validation = validate_input(item.text)

            if not validation.is_valid:
                # Log validation failure
                ctx.logger.info(
                    f"❌ Input validation failed: {validation.reason} "
                    f"(confidence: {validation.confidence:.2f})"
                )

                # Send appropriate guidance message
                guidance_msg = create_text_chat(validation.guidance_message)
                await ctx.send(sender, guidance_msg)

                # Don't route to patient intake - validation handled the response
                return

            # Input is valid - log and proceed with normal routing
            ctx.logger.info(
                f"✅ Input validation passed: {validation.reason} "
                f"(confidence: {validation.confidence:.2f})"
            )

            # Route to Patient Intake Agent for symptom extraction
            patient_intake_addr = os.getenv("PATIENT_INTAKE_ADDRESS")

            if not patient_intake_addr or patient_intake_addr == "agent1q...":
                # Patient Intake not configured, send friendly message
                ctx.logger.warning("Patient Intake Agent address not configured")

                response = create_text_chat(
                    f"I've received your message: '{item.text}'\n\n"
                    "Note: Agent communication is being configured. "
                    "For now, I'm processing your symptoms directly.\n\n"
                    "Your symptoms will be analyzed shortly..."
                )
                await ctx.send(sender, response)
            else:
                # Send to Patient Intake agent
                intake_msg = IntakeTextMessage(
                    text=item.text,
                    session_id=session.session_id
                )

                ctx.logger.info(f"Routing to Patient Intake: {patient_intake_addr}")
                await ctx.send(patient_intake_addr, intake_msg)

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
# Inter-Agent Protocol Handlers
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
    ctx.logger.info(f"Active sessions: {list(active_sessions.keys())}")
    ctx.logger.info(f"Looking for session_id: {msg.session_id}")

    for addr, session in active_sessions.items():
        ctx.logger.info(f"Checking session: {session.session_id} for address: {addr}")
        if session.session_id == msg.session_id:
            user_session = session
            session.patient_data = msg.patient_data
            ctx.logger.info(f"✅ Found matching session!")
            break

    if not user_session:
        ctx.logger.warning(f"No active session found for {msg.session_id}")
        ctx.logger.warning(f"Available sessions: {[(addr, s.session_id) for addr, s in active_sessions.items()]}")
        return

    ctx.logger.info(f"Processing diagnostic request for user: {user_session.user_address}")

    # Route to Symptom Analysis Agent
    symptom_analysis_addr = os.getenv("SYMPTOM_ANALYSIS_ADDRESS")

    if not symptom_analysis_addr or symptom_analysis_addr == "agent1q...":
        ctx.logger.warning("Symptom Analysis Agent address not configured")

        # Fallback response
        symptoms_list = [s.name.replace('_', ' ') for s in msg.patient_data.symptoms]
        response_text = (
            f"📋 Symptom Analysis\n\n"
            f"Symptoms detected: {', '.join(symptoms_list)}\n\n"
            f"⚠️ Symptom Analysis Agent not yet configured.\n"
            f"Please configure SYMPTOM_ANALYSIS_ADDRESS in .env file.\n\n"
            f"Session ID: {msg.session_id}"
        )
        user_msg = create_text_chat(response_text)
        await ctx.send(user_session.user_address, user_msg)
        return

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

    ctx.logger.info(f"Routing to Symptom Analysis Agent: {symptom_analysis_addr}")
    ctx.logger.info(f"  Symptoms: {symptoms_list}")
    ctx.logger.info(f"  Age: {msg.patient_data.age}")

    # Send to Symptom Analysis Agent
    await ctx.send(symptom_analysis_addr, analysis_request)

    # Acknowledge to user
    ack_msg = create_text_chat("🔬 Performing comprehensive symptom analysis...")
    await ctx.send(user_session.user_address, ack_msg)


@inter_agent_proto.on_message(model=AgentAcknowledgementMsg)
async def handle_agent_acknowledgement(ctx: Context, sender: str, msg: AgentAcknowledgementMsg):
    """
    CRITICAL FIX: Handle acknowledgements and clarification requests from specialist agents
    Forward clarification questions to the user via Chat Protocol
    Uses mailbox-compatible Model (AgentAcknowledgementMsg) for inter-agent communication
    """
    ctx.logger.info(f"📨 Received acknowledgement from {msg.agent_name}")
    ctx.logger.info(f"   Session: {msg.session_id}")
    ctx.logger.info(f"   Message: {msg.message[:100]}...")

    # Find the user session
    user_session = None
    for addr, session in active_sessions.items():
        if session.session_id == msg.session_id:
            user_session = session
            break

    if not user_session:
        ctx.logger.warning(f"No active session for {msg.session_id}")
        return

    # Forward the message to the user via Chat Protocol
    user_msg = create_text_chat(msg.message)
    await ctx.send(user_session.user_address, user_msg)
    ctx.logger.info(f"✅ Forwarded acknowledgement to user")


@inter_agent_proto.on_message(model=DiagnosticResponse)
async def handle_diagnostic_response(ctx: Context, sender: str, msg: DiagnosticResponse):
    """Handle diagnostic responses from Knowledge Graph Agent (Legacy)"""
    ctx.logger.info(f"Received diagnostic response from {sender}")

    # Find session
    user_session = None
    for addr, session in active_sessions.items():
        if session.session_id == msg.session_id:
            user_session = session
            session.diagnostic_response = msg
            break

    if not user_session:
        ctx.logger.warning(f"No active session for {msg.session_id}")
        return

    # Format and send to user
    conditions_text = "\n".join([
        f"  {i+1}. {c.condition_name} ({c.confidence_level.value} confidence - {c.confidence*100:.0f}%)"
        for i, c in enumerate(msg.possible_conditions)
    ])

    response_text = (
        f"🔬 Diagnostic Analysis\n\n"
        f"Urgency Level: {msg.urgency_level.value.upper()}\n\n"
        f"Possible Conditions:\n{conditions_text}\n\n"
        f"{'⚠️ RED FLAGS: ' + ', '.join(msg.red_flags) if msg.red_flags else ''}\n\n"
        f"Agent: {msg.responding_agent}"
    )

    user_msg = create_text_chat(response_text)
    await ctx.send(user_session.user_address, user_msg)


@inter_agent_proto.on_message(model=SymptomAnalysisResponseMsg)
async def handle_symptom_analysis_response(ctx: Context, sender: str, msg: SymptomAnalysisResponseMsg):
    """
    Handle symptom analysis response from Symptom Analysis Agent
    Route to Treatment Recommendation Agent for next step
    """
    ctx.logger.info(f"📥 Received symptom analysis response from {sender}")
    ctx.logger.info(f"   Session: {msg.session_id}")
    ctx.logger.info(f"   Urgency: {msg.urgency_level}")
    ctx.logger.info(f"   Red flags: {len(msg.red_flags)}")
    ctx.logger.info(f"   Differential diagnoses: {len(msg.differential_diagnoses)}")

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
    ctx.logger.info("📤 Sending symptom analysis results to user")

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
    treatment_agent_addr = os.getenv("TREATMENT_RECOMMENDATION_ADDRESS")

    if not treatment_agent_addr or treatment_agent_addr == "agent1q...":
        ctx.logger.warning("Treatment Recommendation Agent address not configured")

        fallback_text = (
            "⚠️ Treatment Recommendation Agent not yet configured.\n"
            "Please configure TREATMENT_RECOMMENDATION_ADDRESS in .env file."
        )
        fallback_msg = create_text_chat(fallback_text)
        await ctx.send(user_session.user_address, fallback_msg)
        return

    # Prepare treatment request
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

    ctx.logger.info(f"Routing to Treatment Recommendation Agent: {treatment_agent_addr}")
    ctx.logger.info(f"  Primary condition: {primary_condition}")
    ctx.logger.info(f"  Urgency: {msg.urgency_level}")

    # Send to Treatment Recommendation Agent
    await ctx.send(treatment_agent_addr, treatment_request)


@inter_agent_proto.on_message(model=TreatmentResponseMsg)
async def handle_treatment_response(ctx: Context, sender: str, msg: TreatmentResponseMsg):
    """
    Handle treatment recommendation response from Treatment Recommendation Agent
    Send final comprehensive report to user
    """
    ctx.logger.info(f"📥 Received treatment recommendations from {sender}")
    ctx.logger.info(f"   Session: {msg.session_id}")
    ctx.logger.info(f"   Condition: {msg.condition}")
    ctx.logger.info(f"   Treatments: {len(msg.treatments)}")
    ctx.logger.info(f"   Contraindications: {sum(len(v) for v in msg.contraindications.values())}")
    ctx.logger.info(f"   Safety warnings: {len(msg.safety_warnings)}")

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
    ctx.logger.info("📤 Sending final diagnostic report to user")

    # Treatment recommendations section
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
    ctx.logger.info(f"   Report length: {len(final_report)} characters")


# ============================================================================
# Startup & Initialization
# ============================================================================

@agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize coordinator agent"""
    ctx.logger.info("=" * 60)
    ctx.logger.info("MediChain AI Coordinator Agent")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"Agent name: {agent.name}")
    ctx.logger.info(f"Mailbox: Enabled (ASI:One compatible)")
    ctx.logger.info(f"Chat Protocol: Enabled")
    ctx.logger.info(f"Session cleanup: Every hour (timeout: {SESSION_TIMEOUT_SECONDS/3600:.1f} hours)")
    ctx.logger.info("=" * 60)


@agent.on_interval(period=3600)  # Run every hour
async def periodic_session_cleanup(ctx: Context):
    """Periodically clean up expired sessions"""
    cleaned = cleanup_expired_sessions(ctx)
    ctx.logger.info(f"Periodic cleanup: {len(active_sessions)} active sessions, {cleaned} cleaned up")


# Include protocols
agent.include(chat_proto, publish_manifest=True)
agent.include(inter_agent_proto)


if __name__ == "__main__":
    agent.run()
