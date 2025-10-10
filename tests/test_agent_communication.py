"""
Test Agent Communication - Verify Coordinator → Patient Intake flow
"""

import asyncio
import os
import sys
from datetime import datetime
from uuid import uuid4

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from uagents import Agent, Context
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    ChatAcknowledgement,
    StartSessionContent,
    TextContent,
)
from src.protocols.messages import AgentAcknowledgement
from dotenv import load_dotenv

load_dotenv()


def test_agent_communication():
    """Test that coordinator receives and routes messages to patient intake"""

    # Create test user agent
    test_agent = Agent(
        name="test-user",
        seed="test_user_seed_12345",
        port=8002
    )

    coordinator_address = os.getenv("COORDINATOR_ADDRESS")
    patient_intake_address = os.getenv("PATIENT_INTAKE_ADDRESS")

    print("=" * 60)
    print("Agent Communication Test")
    print("=" * 60)
    print(f"Test Agent: {test_agent.address}")
    print(f"Coordinator: {coordinator_address}")
    print(f"Patient Intake: {patient_intake_address}")
    print("=" * 60)

    # Track responses
    responses = []

    @test_agent.on_message(model=ChatMessage)
    async def handle_chat_response(ctx: Context, sender: str, msg: ChatMessage):
        """Handle chat responses from coordinator"""
        print(f"\n✅ Received ChatMessage from {sender[:20]}...")
        for content in msg.content:
            if hasattr(content, 'text'):
                print(f"   Message: {content.text[:100]}...")
                responses.append(content.text)

        # Send acknowledgement
        await ctx.send(sender, ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        ))

    @test_agent.on_message(model=ChatAcknowledgement)
    async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
        """Handle acknowledgements"""
        print(f"\n✅ Received ChatAcknowledgement from {sender[:20]}...")

    @test_agent.on_message(model=AgentAcknowledgement)
    async def handle_agent_ack(ctx: Context, sender: str, msg: AgentAcknowledgement):
        """Handle agent acknowledgements"""
        print(f"\n✅ Received AgentAcknowledgement from {sender[:20]}...")
        print(f"   Agent: {msg.agent_name}")
        print(f"   Message: {msg.message[:100]}...")
        responses.append(msg.message)

    @test_agent.on_event("startup")
    async def send_test_messages(ctx: Context):
        """Send test messages to coordinator"""
        print("\n🚀 Starting test sequence...")

        # Wait for agents to be ready
        await asyncio.sleep(2)

        # Test 1: Start session
        print("\n📤 Test 1: Sending StartSession...")
        start_msg = ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[StartSessionContent(type="start-session")]
        )
        await ctx.send(coordinator_address, start_msg)
        await asyncio.sleep(2)

        # Test 2: Send symptom text
        print("\n📤 Test 2: Sending symptom description...")
        symptom_msg = ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=[TextContent(
                type="text",
                text="I have a severe headache and fever for 2 days. I'm 35 years old."
            )]
        )
        await ctx.send(coordinator_address, symptom_msg)
        await asyncio.sleep(5)

        # Test 3: Check responses
        print("\n📊 Test Results:")
        print(f"   Total responses received: {len(responses)}")
        for i, response in enumerate(responses, 1):
            print(f"   {i}. {response[:80]}...")

        if len(responses) >= 2:
            print("\n✅ SUCCESS: Agent communication working!")
        else:
            print("\n⚠️  WARNING: Expected at least 2 responses")

        print("\n" + "=" * 60)
        print("Test complete. Press Ctrl+C to exit.")

    # Run test agent
    test_agent.run()


if __name__ == "__main__":
    print("\nBismillah - Testing MediChain AI agent communication\n")
    try:
        test_agent_communication()
    except KeyboardInterrupt:
        print("\n\nTest interrupted. Exiting...")
