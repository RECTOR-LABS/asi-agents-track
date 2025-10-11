"""
MediChain AI - Coordinator Agent with HTTP Bridge (Queue-based)
Hybrid agent: uAgents protocol + FastAPI HTTP server for web interface

This version uses asyncio.Queue for communication between FastAPI and uAgent.
Both run in the same event loop without threading issues.

Architecture:
  - FastAPI server (port 8080) for HTTP requests
  - uAgent (mailbox) for ASI:One and inter-agent communication
  - asyncio.Queue for request/response between HTTP and agent
  - uAgent periodic task processes HTTP requests from queue
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4
import asyncio
import os
import sys
from typing import Dict, Optional
import uvicorn
import threading

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
    DiagnosticRequest,
    SymptomAnalysisRequestMsg,
    TreatmentRequestMsg,
)

from dotenv import load_dotenv
load_dotenv()


# ============================================================================
# Request/Response Queues
# ============================================================================

# Queue for HTTP requests → uAgent
request_queue = asyncio.Queue()

# Store pending HTTP requests and their responses
pending_requests: Dict[str, dict] = {}


# ============================================================================
# FastAPI HTTP Server
# ============================================================================

app = FastAPI(title="MediChain AI Coordinator")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",
        "https://*.rectorspace.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DiagnoseRequest(BaseModel):
    message: str


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": "medichain-coordinator",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/diagnose")
async def diagnose(request: DiagnoseRequest):
    """
    Main diagnostic endpoint for web interface
    """
    if not request.message or not request.message.strip():
        raise HTTPException(status_code=400, detail="Missing or empty 'message' field")

    user_message = request.message.strip()

    # Create HTTP session
    http_session_id = f"http-{uuid4()}"

    # Store request
    pending_requests[http_session_id] = {
        "status": "processing",
        "started_at": datetime.now(),
        "message": user_message,
        "response": None
    }

    # Put request in queue for uAgent to process
    await request_queue.put({
        "session_id": http_session_id,
        "message": user_message
    })

    print(f"[HTTP] Queued request: {http_session_id}", flush=True)

    # Wait for response (with timeout)
    timeout = 30  # 30 seconds
    start_time = asyncio.get_event_loop().time()

    while True:
        if pending_requests[http_session_id]["status"] == "completed":
            response_data = pending_requests[http_session_id]["response"]
            # Clean up
            del pending_requests[http_session_id]
            return response_data

        # Check timeout
        if asyncio.get_event_loop().time() - start_time > timeout:
            del pending_requests[http_session_id]
            raise HTTPException(
                status_code=504,
                detail="The diagnostic process took too long. Please try again."
            )

        # Yield control to allow other tasks to run
        await asyncio.sleep(0.1)


# ============================================================================
# uAgent Setup
# ============================================================================

agent = Agent(
    name="medichain-coordinator",
    seed=os.getenv("AGENT_SEED", "coordinator_seed_phrase"),
    port=8001,
    mailbox=True,  # Enable mailbox for Agentverse
    publish_agent_details=True,  # Enable for discoverability
)

inter_agent_proto = Protocol(name="MediChainProtocol")

# Session storage
active_sessions: Dict[str, dict] = {}


# ============================================================================
# HTTP Request Processing (Queue-based)
# ============================================================================

@agent.on_interval(period=0.5)  # Check queue every 500ms
async def process_http_queue(ctx: Context):
    """Process HTTP requests from queue"""
    try:
        # Non-blocking queue check
        if not request_queue.empty():
            request_data = await asyncio.wait_for(request_queue.get(), timeout=0.1)

            session_id = request_data["session_id"]
            user_message = request_data["message"]

            ctx.logger.info(f"[HTTP] Processing queued request: {session_id}")

            # Create session
            active_sessions[session_id] = {
                "session_id": session_id,
                "user_address": f"http-user-{session_id}",
                "started_at": datetime.now(),
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
                    "message": "Patient Intake Agent address not configured."
                }
                return

            # Send to Patient Intake
            intake_msg = IntakeTextMessage(
                text=user_message,
                session_id=session_id
            )

            ctx.logger.info(f"[HTTP] Routing to Patient Intake: {patient_intake_addr}")
            await ctx.send(patient_intake_addr, intake_msg)

    except asyncio.TimeoutError:
        pass  # Queue is empty, continue
    except Exception as e:
        ctx.logger.error(f"[HTTP] Error processing queue: {e}")


# ============================================================================
# Inter-Agent Protocol Handlers
# ============================================================================

@inter_agent_proto.on_message(model=SymptomAnalysisResponseMsg)
async def handle_symptom_analysis_http(ctx: Context, sender: str, msg: SymptomAnalysisResponseMsg):
    """Handle symptom analysis response"""
    session_id = msg.session_id

    # Check if this is HTTP session
    if session_id not in pending_requests:
        return

    ctx.logger.info(f"[HTTP] Received symptom analysis for {session_id}")

    # Store in session
    if session_id in active_sessions:
        active_sessions[session_id]["symptom_analysis_response"] = msg

    # Route to Treatment Agent
    treatment_agent_addr = os.getenv("TREATMENT_RECOMMENDATION_ADDRESS")

    if not treatment_agent_addr or treatment_agent_addr == "agent1q...":
        pending_requests[session_id]["status"] = "completed"
        pending_requests[session_id]["response"] = {
            "error": "Agent not configured",
            "message": "Treatment Recommendation Agent not configured"
        }
        return

    # Request treatment recommendations
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
        requesting_agent="medichain-coordinator-queue",
    )

    ctx.logger.info(f"[HTTP] Routing to Treatment Agent: {treatment_agent_addr}")
    await ctx.send(treatment_agent_addr, treatment_request)


@inter_agent_proto.on_message(model=TreatmentResponseMsg)
async def handle_treatment_response_http(ctx: Context, sender: str, msg: TreatmentResponseMsg):
    """Handle treatment response - complete HTTP request"""
    session_id = msg.session_id

    # Check if this is HTTP session
    if session_id not in pending_requests:
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
        "timestamp": datetime.now().isoformat(),
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
        await asyncio.sleep(60)
        if session_id in active_sessions:
            del active_sessions[session_id]

    asyncio.create_task(cleanup_session())


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
        requesting_agent="medichain-coordinator-queue",
    )

    ctx.logger.info(f"[HTTP] Routing to Symptom Analysis: {symptom_analysis_addr}")
    await ctx.send(symptom_analysis_addr, analysis_request)


# Include protocols
agent.include(inter_agent_proto)


# ============================================================================
# Startup & Main
# ============================================================================

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("=" * 60)
    ctx.logger.info("MediChain AI Coordinator (Queue-based Bridge)")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"HTTP server: http://0.0.0.0:8080 (FastAPI)")
    ctx.logger.info(f"Mailbox: Enabled (ASI:One compatible)")
    ctx.logger.info("=" * 60)


def run_agent():
    """Run uAgent in separate thread"""
    agent.run()


def run_fastapi():
    """Run FastAPI server"""
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )


if __name__ == "__main__":
    print("🚀 Starting MediChain Coordinator with Queue-based Bridge...")
    print("   - uAgent: Mailbox + ASI:One (background thread)")
    print("   - HTTP: Port 8080 (FastAPI, main thread)")
    print("")

    # Start uAgent in background thread
    agent_thread = threading.Thread(target=run_agent, daemon=True)
    agent_thread.start()

    # Wait for agent to initialize
    import time
    time.sleep(3)

    print("✅ uAgent started")
    print("🌐 Starting FastAPI server...")

    # Run FastAPI in main thread
    run_fastapi()
