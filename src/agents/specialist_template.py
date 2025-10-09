"""
Specialist Agent Template - Use this as a base for creating specialist agents
"""

from datetime import datetime
from uuid import uuid4
from uagents import Agent, Context, Protocol, Model
from uagents.setup import fund_agent_if_low
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Define message models for inter-agent communication
class QueryRequest(Model):
    """Request from coordinator to specialist."""
    query: str
    context: dict = {}


class QueryResponse(Model):
    """Response from specialist to coordinator."""
    result: str
    confidence: float = 1.0
    reasoning: str = ""


# Initialize the specialist agent
agent = Agent(
    name="specialist_template",  # Change this name
    seed=os.getenv("AGENT_SEED", "specialist_seed_phrase"),  # Use unique seed
    port=8001,  # Change port for each specialist
)

# Get coordinator address from environment
COORDINATOR_ADDRESS = os.getenv("COORDINATOR_ADDRESS", "")


# Handle query requests from coordinator
@agent.on_message(model=QueryRequest)
async def handle_query(ctx: Context, sender: str, msg: QueryRequest):
    """Process query from coordinator agent."""
    ctx.logger.info(f"Received query from {sender}: {msg.query}")

    # TODO: Implement your specialist logic here
    # This is where you'll:
    # 1. Process the query
    # 2. Query MeTTa knowledge base if needed
    # 3. Apply domain-specific logic
    # 4. Return results

    # Example response:
    result = f"Processed query: {msg.query}"
    reasoning = "This is a template response. Replace with actual logic."

    response = QueryResponse(
        result=result,
        confidence=0.8,
        reasoning=reasoning
    )

    await ctx.send(sender, response)


# Startup event
@agent.on_event("startup")
async def startup(ctx: Context):
    """Log agent startup information."""
    ctx.logger.info(f"Specialist Agent started!")
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"Agent name: {agent.name}")

    # Register with coordinator if address is available
    if COORDINATOR_ADDRESS:
        ctx.logger.info(f"Coordinator address: {COORDINATOR_ADDRESS}")
        # TODO: Send registration message to coordinator
    else:
        ctx.logger.warning("Coordinator address not set in environment")


# Periodic health check
@agent.on_interval(period=60.0)
async def health_check(ctx: Context):
    """Periodic health check."""
    ctx.logger.info(f"{agent.name} is running - Health check OK")


if __name__ == "__main__":
    agent.run()
