"""
Reliable messaging utilities for agent communication
Includes retry logic, queuing, and error handling
"""

import asyncio
from typing import Any, Optional, Callable
from datetime import datetime
from uagents import Context, Model


class MessageRetryConfig:
    """Configuration for message retry behavior"""
    def __init__(
        self,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        backoff_multiplier: float = 2.0,
        timeout: float = 10.0
    ):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.backoff_multiplier = backoff_multiplier
        self.timeout = timeout


async def send_with_retry(
    ctx: Context,
    destination: str,
    message: Model,
    config: Optional[MessageRetryConfig] = None,
    on_failure: Optional[Callable] = None
) -> bool:
    """
    Send message with automatic retry on failure

    Args:
        ctx: Agent context
        destination: Destination agent address
        message: Message to send
        config: Retry configuration (uses defaults if None)
        on_failure: Optional callback on final failure

    Returns:
        True if message sent successfully, False otherwise
    """
    if config is None:
        config = MessageRetryConfig()

    current_delay = config.retry_delay
    last_error = None

    for attempt in range(config.max_retries + 1):
        try:
            ctx.logger.info(
                f"Sending message to {destination[:20]}... (attempt {attempt + 1}/{config.max_retries + 1})"
            )

            # Send message with timeout
            await asyncio.wait_for(
                ctx.send(destination, message),
                timeout=config.timeout
            )

            ctx.logger.info(f"✅ Message sent successfully to {destination[:20]}...")
            return True

        except asyncio.TimeoutError as e:
            last_error = e
            ctx.logger.warning(
                f"⏱️ Timeout sending to {destination[:20]}... (attempt {attempt + 1})"
            )

        except Exception as e:
            last_error = e
            ctx.logger.warning(
                f"❌ Error sending to {destination[:20]}...: {str(e)[:100]} (attempt {attempt + 1})"
            )

        # Don't sleep after last attempt
        if attempt < config.max_retries:
            ctx.logger.info(f"Retrying in {current_delay}s...")
            await asyncio.sleep(current_delay)
            current_delay *= config.backoff_multiplier

    # All retries failed
    ctx.logger.error(
        f"🚫 Failed to send message to {destination[:20]}... after {config.max_retries + 1} attempts"
    )

    if on_failure:
        try:
            await on_failure(ctx, destination, message, last_error)
        except Exception as e:
            ctx.logger.error(f"Error in failure callback: {e}")

    return False


class MessageQueue:
    """
    Simple message queue for managing outgoing messages
    Useful for rate limiting and batch processing
    """

    def __init__(self, max_size: int = 100):
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=max_size)
        self.stats = {
            "queued": 0,
            "sent": 0,
            "failed": 0
        }

    async def enqueue(self, destination: str, message: Model, priority: int = 5):
        """
        Add message to queue

        Args:
            destination: Target agent address
            message: Message to send
            priority: Priority (1=highest, 10=lowest)
        """
        item = {
            "destination": destination,
            "message": message,
            "priority": priority,
            "queued_at": datetime.utcnow()
        }

        await self.queue.put(item)
        self.stats["queued"] += 1

    async def process_queue(
        self,
        ctx: Context,
        retry_config: Optional[MessageRetryConfig] = None
    ):
        """
        Process all messages in queue

        Args:
            ctx: Agent context
            retry_config: Retry configuration for each message
        """
        ctx.logger.info(f"Processing message queue ({self.queue.qsize()} messages)...")

        while not self.queue.empty():
            try:
                item = await self.queue.get()

                success = await send_with_retry(
                    ctx,
                    item["destination"],
                    item["message"],
                    retry_config
                )

                if success:
                    self.stats["sent"] += 1
                else:
                    self.stats["failed"] += 1

            except Exception as e:
                ctx.logger.error(f"Error processing queue item: {e}")
                self.stats["failed"] += 1

        ctx.logger.info(
            f"Queue processed: {self.stats['sent']} sent, {self.stats['failed']} failed"
        )

    def get_stats(self):
        """Get queue statistics"""
        return self.stats.copy()


# Agent discovery helpers
class AgentRegistry:
    """
    Simple registry for tracking known agents and their addresses
    In production, this could be backed by a database
    """

    def __init__(self):
        self.agents = {}

    def register(self, agent_name: str, address: str, capabilities: list = None):
        """Register an agent"""
        self.agents[agent_name] = {
            "address": address,
            "capabilities": capabilities or [],
            "registered_at": datetime.utcnow(),
            "last_seen": datetime.utcnow()
        }

    def get_address(self, agent_name: str) -> Optional[str]:
        """Get agent address by name"""
        agent = self.agents.get(agent_name)
        if agent:
            agent["last_seen"] = datetime.utcnow()
            return agent["address"]
        return None

    def find_by_capability(self, capability: str) -> list:
        """Find agents with specific capability"""
        return [
            {"name": name, "address": data["address"]}
            for name, data in self.agents.items()
            if capability in data.get("capabilities", [])
        ]

    def list_all(self) -> dict:
        """List all registered agents"""
        return self.agents.copy()


# Global registry instance
agent_registry = AgentRegistry()


# Convenience function for agent registration
def register_agent(name: str, address: str, capabilities: list = None):
    """Register agent in global registry"""
    agent_registry.register(name, address, capabilities)


def discover_agent(name: str) -> Optional[str]:
    """Discover agent address by name"""
    return agent_registry.get_address(name)
