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
)

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
        self.treatment_response: Optional[TreatmentResponse] = None
        self.messages_history = []

    def add_message(self, role: str, content: str):
        """Add message to history"""
        self.messages_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow()
        })


# Global session store (in production, use persistent storage)
active_sessions: Dict[str, SessionData] = {}


def get_or_create_session(sender: str) -> SessionData:
    """Get existing session or create new one"""
    if sender not in active_sessions:
        session_id = f"session-{uuid4()}"
        active_sessions[sender] = SessionData(session_id, sender)
    return active_sessions[sender]


# ============================================================================
# Coordinator Agent Initialization
# ============================================================================

agent = Agent(
    name="medichain-coordinator",
    seed=os.getenv("AGENT_SEED", "coordinator_seed_phrase"),
    port=8001,  # Local inspector port (different from patient_intake's 8000)
    mailbox=True,  # Enable Agentverse mailbox for ASI:One discoverability
    publish_agent_details=True,  # Publish agent details for better discoverability
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

    # TODO: Route to specialist agents (Knowledge Graph, Symptom Analysis)
    # For now, create a simple response

    symptoms_list = [s.name.replace('_', ' ') for s in msg.patient_data.symptoms]

    response_text = (
        f"📋 Symptom Analysis Complete\n\n"
        f"Symptoms detected: {', '.join(symptoms_list)}\n"
        f"Number of symptoms: {len(msg.patient_data.symptoms)}\n\n"
        f"⚠️ Next steps:\n"
        f"- Specialist agents are being configured\n"
        f"- Full diagnostic analysis coming soon\n"
        f"- For urgent symptoms, seek immediate medical care\n\n"
        f"Session ID: {msg.session_id}"
    )

    # Send response to user
    user_msg = create_text_chat(response_text)
    await ctx.send(user_session.user_address, user_msg)


@inter_agent_proto.on_message(model=DiagnosticResponse)
async def handle_diagnostic_response(ctx: Context, sender: str, msg: DiagnosticResponse):
    """Handle diagnostic responses from specialist agents"""
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
    ctx.logger.info("=" * 60)


# Include protocols
agent.include(chat_proto, publish_manifest=True)
agent.include(inter_agent_proto)


if __name__ == "__main__":
    agent.run()
