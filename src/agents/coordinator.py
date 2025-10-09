"""
Coordinator Agent - Main routing agent with Chat Protocol for ASI:One
"""

from datetime import datetime
from uuid import uuid4
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
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the coordinator agent
agent = Agent(
    name="coordinator",
    seed=os.getenv("AGENT_SEED", "coordinator_seed_phrase"),
    port=8000,
)

# Initialize the chat protocol with the standard chat spec
chat_proto = Protocol(spec=chat_protocol_spec)


# Utility function to wrap plain text into a ChatMessage
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


# Handle incoming chat messages
@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming chat messages from ASI:One or other agents."""
    ctx.logger.info(f"Received message from {sender}")

    # Always send back an acknowledgement when a message is received
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        )
    )

    # Process each content item inside the chat message
    for item in msg.content:
        # Marks the start of a chat session
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started with {sender}")
            welcome_msg = create_text_chat(
                "Hello! I'm the Coordinator Agent. How can I help you today?"
            )
            await ctx.send(sender, welcome_msg)

        # Handles plain text messages (from another agent or ASI:One)
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Text message from {sender}: {item.text}")

            # TODO: Add your routing logic here
            # This is where you'll route requests to specialist agents
            # based on the user's message content

            # Example routing logic (replace with your implementation):
            user_message = item.text.lower()

            if "help" in user_message or "hello" in user_message:
                response = create_text_chat(
                    "I'm here to help! I can route your requests to specialist agents. "
                    "What would you like to know about?"
                )
            else:
                # Route to specialist agents based on message content
                # For now, just echo back
                response = create_text_chat(
                    f"I received your message: '{item.text}'. "
                    f"I'll route this to the appropriate specialist agent."
                )

            await ctx.send(sender, response)

        # Marks the end of a chat session
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended with {sender}")
            goodbye_msg = create_text_chat(
                "Thank you for using our service! Goodbye!",
                end_session=True
            )
            await ctx.send(sender, goodbye_msg)

        # Catches anything unexpected
        else:
            ctx.logger.info(f"Received unexpected content type from {sender}")


# Handle acknowledgements for messages this agent has sent out
@chat_proto.on_message(ChatAcknowledgement)
async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    """Handle acknowledgements from other agents."""
    ctx.logger.info(
        f"Received acknowledgement from {sender} for message {msg.acknowledged_msg_id}"
    )


# Startup event
@agent.on_event("startup")
async def startup(ctx: Context):
    """Log agent startup information."""
    ctx.logger.info(f"Coordinator Agent started!")
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"Agent name: {agent.name}")


# Include the chat protocol and publish the manifest to Agentverse
agent.include(chat_proto, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
