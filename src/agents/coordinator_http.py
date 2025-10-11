"""
MediChain AI - Coordinator Agent with HTTP Bridge
Hybrid agent: uAgents protocol + Flask HTTP server for web interface

This wrapper adds HTTP endpoint functionality to the existing coordinator agent,
enabling web browsers to interact with the multi-agent system.

Architecture:
  - Flask server (port 8080) for HTTP requests
  - uAgent (mailbox) for ASI:One and inter-agent communication
  - Both run in parallel using threading
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from uuid import uuid4
import threading
import asyncio
import os
import sys
from typing import Dict, Optional
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)
from src.protocols import (
    IntakeTextMessage,
    SymptomAnalysisResponseMsg,
    TreatmentResponseMsg,
)

from dotenv import load_dotenv
load_dotenv()


# ============================================================================
# Flask HTTP Server
# ============================================================================

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "https://*.vercel.app", "https://*.rectorspace.com"])

# Store pending HTTP requests and their responses
pending_requests: Dict[str, dict] = {}


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "agent": "medichain-coordinator",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/api/diagnose', methods=['POST'])
def diagnose():
    """
    Main diagnostic endpoint for web interface

    Request body:
    {
        "message": "I have a severe headache and fever"
    }

    Response:
    {
        "session_id": "session-uuid",
        "status": "completed",
        "report": {...}
    }
    """
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' field"}), 400

        user_message = data['message']

        # Create HTTP session
        http_session_id = f"http-{uuid4()}"

        # Store request (will be populated by agent handlers)
        pending_requests[http_session_id] = {
            "status": "processing",
            "started_at": datetime.utcnow(),
            "message": user_message,
            "response": None
        }

        # Trigger agent processing in background
        # We'll use the agent's event loop
        app.logger.info(f"[DEBUG] Scheduling HTTP request: {http_session_id}")
        app.logger.info(f"[DEBUG] Agent loop: {agent_loop}")
        app.logger.info(f"[DEBUG] Agent context: {agent_context}")

        if agent_loop is None:
            app.logger.error("[DEBUG] Agent loop is None!")
            return jsonify({
                "error": "Agent not ready",
                "message": "Agent event loop not initialized"
            }), 503

        future = asyncio.run_coroutine_threadsafe(
            process_http_request(http_session_id, user_message),
            agent_loop
        )
        app.logger.info(f"[DEBUG] Coroutine scheduled, future: {future}")

        # Wait for response (with timeout)
        timeout = 30  # 30 seconds
        start_time = time.time()

        while time.time() - start_time < timeout:
            if pending_requests[http_session_id]["status"] == "completed":
                response_data = pending_requests[http_session_id]["response"]
                # Clean up
                del pending_requests[http_session_id]
                return jsonify(response_data)

            time.sleep(0.1)  # Poll every 100ms

        # Timeout
        del pending_requests[http_session_id]
        return jsonify({
            "error": "Request timeout",
            "message": "The diagnostic process took too long. Please try again."
        }), 504

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================================
# uAgent Setup (from coordinator.py)
# ============================================================================

agent = Agent(
    name="medichain-coordinator",
    seed=os.getenv("AGENT_SEED", "coordinator_seed_phrase"),
    port=8001,
    mailbox=False,  # Disabled for local HTTP testing
    publish_agent_details=False,  # Disabled for local testing
)

chat_proto = Protocol(spec=chat_protocol_spec)
inter_agent_proto = Protocol(name="MediChainProtocol")

# Session storage
active_sessions: Dict[str, dict] = {}

# Global agent context (set during startup)
agent_context: Optional[Context] = None


def create_text_chat(text: str, end_session: bool = False) -> ChatMessage:
    """Create a ChatMessage with text content"""
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end_session"))
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )


# ============================================================================
# HTTP Request Processing Logic
# ============================================================================

async def process_http_request(session_id: str, user_message: str):
    """Process HTTP request through multi-agent flow"""
    global agent_context

    print(f"[PROCESS_HTTP] Started processing: {session_id}", flush=True)

    if agent_context is None:
        print(f"[PROCESS_HTTP] Agent context is None!", flush=True)
        pending_requests[session_id]["status"] = "completed"
        pending_requests[session_id]["response"] = {
            "error": "Agent not ready",
            "message": "Agent context not initialized. Please wait and try again."
        }
        return

    ctx = agent_context
    print(f"[PROCESS_HTTP] Got context: {type(ctx)}", flush=True)

    # Create session
    active_sessions[session_id] = {
        "session_id": session_id,
        "user_address": f"http-user-{session_id}",
        "started_at": datetime.utcnow(),
        "patient_data": None,
        "symptom_analysis_response": None,
        "treatment_response": None,
        "messages_history": []
    }

    # Route to Patient Intake
    patient_intake_addr = os.getenv("PATIENT_INTAKE_ADDRESS")

    if not patient_intake_addr or patient_intake_addr == "agent1q...":
        # No patient intake configured - return error
        pending_requests[session_id]["status"] = "completed"
        pending_requests[session_id]["response"] = {
            "error": "Agent not configured",
            "message": "Patient Intake Agent address not configured. Please set PATIENT_INTAKE_ADDRESS environment variable."
        }
        return

    # Send to Patient Intake
    intake_msg = IntakeTextMessage(
        text=user_message,
        session_id=session_id
    )

    ctx.logger.info(f"[HTTP] Processing request: {session_id}")
    ctx.logger.info(f"[HTTP] Routing to Patient Intake: {patient_intake_addr}")

    await ctx.send(patient_intake_addr, intake_msg)


# ============================================================================
# Inter-Agent Protocol Handlers (Collect Responses)
# ============================================================================

@inter_agent_proto.on_message(model=SymptomAnalysisResponseMsg)
async def handle_symptom_analysis_http(ctx: Context, sender: str, msg: SymptomAnalysisResponseMsg):
    """Handle symptom analysis response - store for HTTP session"""
    session_id = msg.session_id

    # Check if this is HTTP session
    if session_id not in pending_requests:
        # Not an HTTP request, ignore (will be handled by normal chat handler)
        return

    ctx.logger.info(f"[HTTP] Received symptom analysis for {session_id}")

    # Store in session
    if session_id in active_sessions:
        active_sessions[session_id]["symptom_analysis_response"] = msg

    # Route to Treatment Agent
    treatment_agent_addr = os.getenv("TREATMENT_RECOMMENDATION_ADDRESS")

    if not treatment_agent_addr or treatment_agent_addr == "agent1q...":
        # No treatment agent - return partial response
        pending_requests[session_id]["status"] = "completed"
        pending_requests[session_id]["response"] = {
            "error": "Agent not configured",
            "message": "Treatment Recommendation Agent not configured",
            "partial_analysis": {
                "urgency_level": msg.urgency_level,
                "red_flags": msg.red_flags,
                "differential_diagnoses": msg.differential_diagnoses,
                "confidence_scores": msg.confidence_scores
            }
        }
        return

    # Request treatment recommendations
    from src.protocols import TreatmentRequestMsg

    primary_condition = msg.differential_diagnoses[0] if msg.differential_diagnoses else "unknown"
    alternative_conditions = msg.differential_diagnoses[1:5] if len(msg.differential_diagnoses) > 1 else None

    session = active_sessions.get(session_id)
    patient_data = session.get("patient_data") if session else None

    treatment_request = TreatmentRequestMsg(
        session_id=session_id,
        primary_condition=primary_condition,
        alternative_conditions=alternative_conditions,
        urgency_level=msg.urgency_level,
        patient_age=patient_data.age if patient_data else None,
        allergies=patient_data.allergies if patient_data else None,
        current_medications=patient_data.current_medications if patient_data else None,
        medical_history=patient_data.medical_history if patient_data else None,
        requesting_agent="medichain-coordinator-http",
    )

    ctx.logger.info(f"[HTTP] Routing to Treatment Agent: {treatment_agent_addr}")
    await ctx.send(treatment_agent_addr, treatment_request)


@inter_agent_proto.on_message(model=TreatmentResponseMsg)
async def handle_treatment_response_http(ctx: Context, sender: str, msg: TreatmentResponseMsg):
    """Handle treatment response - complete HTTP request"""
    session_id = msg.session_id

    # Check if this is HTTP session
    if session_id not in pending_requests:
        # Not an HTTP request, ignore
        return

    ctx.logger.info(f"[HTTP] Received treatment recommendations for {session_id}")

    # Store in session
    if session_id in active_sessions:
        active_sessions[session_id]["treatment_response"] = msg

    # Build complete response
    session = active_sessions.get(session_id)
    symptom_analysis = session.get("symptom_analysis_response") if session else None

    response_data = {
        "session_id": session_id,
        "status": "completed",
        "timestamp": datetime.utcnow().isoformat(),
        "analysis": {
            "urgency_level": symptom_analysis.urgency_level if symptom_analysis else "unknown",
            "red_flags": symptom_analysis.red_flags if symptom_analysis else [],
            "differential_diagnoses": symptom_analysis.differential_diagnoses if symptom_analysis else [],
            "confidence_scores": symptom_analysis.confidence_scores if symptom_analysis else {},
            "recommended_action": symptom_analysis.recommended_next_step if symptom_analysis else "Consult healthcare provider"
        },
        "treatment": {
            "condition": msg.condition,
            "treatments": msg.treatments,
            "evidence_sources": msg.evidence_sources,
            "contraindications": msg.contraindications,
            "safety_warnings": msg.safety_warnings,
            "specialist_referral": msg.specialist_referral,
            "follow_up_timeline": msg.follow_up_timeline,
            "medical_disclaimer": msg.medical_disclaimer
        }
    }

    # Complete HTTP request
    pending_requests[session_id]["status"] = "completed"
    pending_requests[session_id]["response"] = response_data

    ctx.logger.info(f"[HTTP] Request completed: {session_id}")

    # Clean up session after delay
    async def cleanup_session():
        await asyncio.sleep(60)  # Keep for 1 minute
        if session_id in active_sessions:
            del active_sessions[session_id]

    asyncio.create_task(cleanup_session())


# Import and include all handlers from original coordinator.py
# (chat protocol handlers, diagnostic request handlers, etc.)
from src.protocols import DiagnosticRequest

@inter_agent_proto.on_message(model=DiagnosticRequest)
async def handle_diagnostic_request(ctx: Context, sender: str, msg: DiagnosticRequest):
    """Handle diagnostic requests from Patient Intake"""
    session_id = msg.session_id

    ctx.logger.info(f"[HTTP] Received diagnostic request for {session_id}")

    # Store patient data
    if session_id in active_sessions:
        active_sessions[session_id]["patient_data"] = msg.patient_data

    # Route to Symptom Analysis
    symptom_analysis_addr = os.getenv("SYMPTOM_ANALYSIS_ADDRESS")

    if not symptom_analysis_addr or symptom_analysis_addr == "agent1q...":
        if session_id in pending_requests:
            pending_requests[session_id]["status"] = "completed"
            pending_requests[session_id]["response"] = {
                "error": "Agent not configured",
                "message": "Symptom Analysis Agent not configured"
            }
        return

    # Prepare symptom analysis request
    from src.protocols import SymptomAnalysisRequestMsg

    symptoms_list = [s.name for s in msg.patient_data.symptoms]
    severity_scores = {s.name: s.severity for s in msg.patient_data.symptoms if s.severity}
    duration_info = {s.name: s.duration for s in msg.patient_data.symptoms if s.duration}

    analysis_request = SymptomAnalysisRequestMsg(
        session_id=session_id,
        symptoms=symptoms_list,
        age=msg.patient_data.age,
        severity_scores=severity_scores if severity_scores else None,
        duration_info=duration_info if duration_info else None,
        medical_history=msg.patient_data.medical_history,
        requesting_agent="medichain-coordinator-http",
    )

    ctx.logger.info(f"[HTTP] Routing to Symptom Analysis: {symptom_analysis_addr}")
    await ctx.send(symptom_analysis_addr, analysis_request)


# ============================================================================
# Chat Protocol Handlers (for ASI:One - keep original functionality)
# ============================================================================

@chat_proto.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle ASI:One chat messages (original functionality preserved)"""
    # Import original handler logic here if needed
    # For now, just acknowledge
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        )
    )
    ctx.logger.info(f"[ASI:One] Received chat message from {sender}")


# Include protocols
# Note: Chat Protocol disabled for local HTTP testing (enable for ASI:One deployment)
# agent.include(chat_proto, publish_manifest=True)
agent.include(inter_agent_proto)


# ============================================================================
# Startup & Main
# ============================================================================

@agent.on_event("startup")
async def startup(ctx: Context):
    global agent_context
    agent_context = ctx  # Store context for HTTP handlers

    ctx.logger.info("=" * 60)
    ctx.logger.info("MediChain AI Coordinator (HTTP Bridge Enabled)")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"HTTP server: http://0.0.0.0:8080")
    ctx.logger.info(f"Mailbox: Enabled (ASI:One compatible)")
    ctx.logger.info("=" * 60)


# Global event loop reference
agent_loop = None


def run_agent():
    """Run uAgent in background thread"""
    global agent_loop
    agent_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(agent_loop)
    agent.run()


def run_flask():
    """Run Flask HTTP server"""
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == "__main__":
    print("🚀 Starting MediChain Coordinator with HTTP Bridge...")
    print("   - uAgent: Mailbox + ASI:One")
    print("   - HTTP: Port 8080")
    print("")

    # Start uAgent in background thread
    agent_thread = threading.Thread(target=run_agent, daemon=True)
    agent_thread.start()

    # Wait for agent to initialize
    time.sleep(2)

    print("✅ uAgent started")
    print("🌐 Starting HTTP server...")

    # Start Flask in main thread
    run_flask()
