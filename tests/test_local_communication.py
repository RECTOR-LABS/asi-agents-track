"""
Test local agent-to-agent communication
Run both coordinator and patient_intake agents first in separate terminals
"""

import asyncio
from uagents import Agent, Context
from uagents_core.contrib.protocols.chat import (
    ChatMessage,
    StartSessionContent,
    TextContent,
    ChatAcknowledgement,
)
from datetime import datetime
from uuid import uuid4
import os
import sys

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def create_chat_message(text: str, start_session: bool = False) -> ChatMessage:
    """Helper to create chat messages"""
    content = []
    if start_session:
        content.append(StartSessionContent(type="start_session"))
    content.append(TextContent(type="text", text=text))

    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )


async def test_communication():
    """Test sending message to coordinator"""

    # Create a test client agent
    test_agent = Agent(
        name="test_client",
        seed="test_client_seed_12345",
        port=8999,
    )

    coordinator_addr = "agent1qwukpkhx9m6595wvfy953unajptrl2rpx95zynucfxam4s7u0qz2je6h70q"

    @test_agent.on_event("startup")
    async def send_test_message(ctx: Context):
        """Send test message to coordinator"""
        print("=" * 60)
        print("Testing Local Agent Communication")
        print("=" * 60)
        print(f"Test Client Address: {test_agent.address}")
        print(f"Coordinator Address: {coordinator_addr}")
        print("")

        # Wait a moment for startup
        await asyncio.sleep(1)

        # Start session
        print("Sending StartSession message...")
        start_msg = create_chat_message("", start_session=True)
        await ctx.send(coordinator_addr, start_msg)

        # Wait for response
        await asyncio.sleep(2)

        # Send symptom description
        print("Sending symptom description...")
        symptom_msg = create_chat_message(
            "I have a severe fever and bad headache for 3 days. I am 35 years old."
        )
        await ctx.send(coordinator_addr, symptom_msg)

        print("")
        print("Messages sent! Check coordinator and patient_intake logs.")
        print("=" * 60)

        # Wait for responses
        await asyncio.sleep(5)

    # Handle acknowledgements
    @test_agent.on_message(model=ChatAcknowledgement)
    async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
        print(f"✅ Received acknowledgement from {sender[:20]}...")

    # Handle responses
    @test_agent.on_message(model=ChatMessage)
    async def handle_response(ctx: Context, sender: str, msg: ChatMessage):
        print(f"\n📨 Response from {sender[:20]}...")
        for item in msg.content:
            if isinstance(item, TextContent):
                print(f"   {item.text[:100]}...")

    # Run test agent
    test_agent.run()


if __name__ == "__main__":
    print("\n⚠️  IMPORTANT: Make sure coordinator and patient_intake agents are running!")
    print("   Terminal 1: python src/agents/coordinator.py")
    print("   Terminal 2: python src/agents/patient_intake.py")
    print("   Terminal 3: python tests/test_local_communication.py (this script)")
    print("")
    input("Press Enter when agents are ready...")
    print("")

    try:
        asyncio.run(test_communication())
    except KeyboardInterrupt:
        print("\nTest stopped by user")
