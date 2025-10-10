"""
Test Knowledge Graph Agent directly
Run this to send a DiagnosticRequest to the Knowledge Graph Agent
"""

from uagents import Agent, Context
from src.protocols import DiagnosticRequest, PatientIntakeData, ExtractedSymptom
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Create test agent
test_agent = Agent(
    name="test-client",
    seed="test_client_seed_123",
    port=8010,  # Different port
)


@test_agent.on_event("startup")
async def send_test_request(ctx: Context):
    """Send a test diagnostic request to Knowledge Graph Agent"""

    knowledge_graph_address = os.getenv("KNOWLEDGE_GRAPH_ADDRESS")

    if not knowledge_graph_address:
        ctx.logger.error("KNOWLEDGE_GRAPH_ADDRESS not found in .env")
        return

    ctx.logger.info(f"🧪 Sending test diagnostic request to {knowledge_graph_address}")

    # Test Case 1: Meningitis (should detect emergency)
    test_symptoms = [
        ExtractedSymptom(name="fever", severity=9, duration="2 days"),
        ExtractedSymptom(name="severe-headache", severity=10, duration="2 days"),
        ExtractedSymptom(name="stiff-neck", severity=8, duration="1 day"),
        ExtractedSymptom(name="non-blanching-rash", severity=7, duration="4 hours"),
    ]

    patient_data = PatientIntakeData(
        symptoms=test_symptoms,
        age=25,
        raw_text="I have severe headache, high fever, stiff neck, and a rash that doesn't fade when pressed"
    )

    diagnostic_request = DiagnosticRequest(
        session_id="test-session-123",
        patient_data=patient_data,
        requesting_agent="test_client",
        analysis_type="full_diagnostic"
    )

    ctx.logger.info("📤 Sending DiagnosticRequest...")
    await ctx.send(knowledge_graph_address, diagnostic_request)
    ctx.logger.info("✅ Request sent! Waiting for response...")


@test_agent.on_message(model=dict)
async def handle_response(ctx: Context, sender: str, msg: dict):
    """Handle any response from Knowledge Graph Agent"""
    ctx.logger.info(f"📥 Received response from {sender}:")
    ctx.logger.info(f"   Response type: {type(msg)}")
    ctx.logger.info(f"   Response content: {msg}")


if __name__ == "__main__":
    print("🧪 Knowledge Graph Agent Test Client")
    print("=" * 60)
    print(f"Target: {os.getenv('KNOWLEDGE_GRAPH_ADDRESS')}")
    print("Test case: Meningitis symptoms (emergency scenario)")
    print("=" * 60)
    print()

    test_agent.run()
