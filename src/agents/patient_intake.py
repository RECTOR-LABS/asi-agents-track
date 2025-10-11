"""
Patient Intake Agent - Extracts and structures patient symptom data
MediChain AI - ASI Agents Track Hackathon
"""

from uagents import Agent, Context, Model, Protocol
from uagents.setup import fund_agent_if_low
import os
import re
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

# Import our message protocols
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.protocols import (
    Symptom,
    PatientIntakeData,
    DiagnosticRequest,
    AgentAcknowledgement,
    IntakeTextMessage,
)

# Load environment variables
load_dotenv()


# ============================================================================
# Patient Intake Agent Configuration
# ============================================================================

agent = Agent(
    name="medichain-patient-intake",
    seed=os.getenv("AGENT_SEED", "patient_intake_seed_dev") + "_intake",
    mailbox=True,  # Enable Agentverse mailbox for ASI:One discoverability
    publish_agent_details=True,  # Publish agent details for better discoverability
)

# Create protocol for inter-agent communication
inter_agent_proto = Protocol(name="PatientIntakeProtocol")


# ============================================================================
# Symptom Extraction & Normalization
# ============================================================================

# Common symptom keywords for pattern matching (expandable)
# Ordered from most specific to least specific (check longer phrases first)
SYMPTOM_KEYWORDS = {
    # Fever & Temperature - specific variants first
    "high-fever": ["high fever", "very high temperature", "burning up with fever"],
    "fever": ["fever", "high temperature", "temp", "hot"],
    "chills": ["chills", "shivering", "shaking", "cold"],

    # Head & Neurological - specific variants first
    "severe-headache": ["severe headache", "terrible headache", "worst headache", "intense headache"],
    "headache": ["headache", "head pain", "head hurts", "migraine", "head ache"],
    "dizziness": ["dizzy", "lightheaded", "vertigo", "spinning"],
    "confusion": ["confused", "disoriented", "foggy", "can't think"],

    # Neck symptoms - multiple variations
    "neck-stiffness": ["neck is very stiff", "neck is stiff", "very stiff neck", "extremely stiff neck"],
    "stiff-neck": ["stiff neck", "neck stiff", "can't move neck", "neck hurts to move"],

    # Respiratory
    "difficulty-breathing": ["difficulty breathing", "hard to breathe", "can't breathe well"],
    "shortness-of-breath": ["short of breath", "can't breathe", "breathless", "gasping"],
    "cough": ["cough", "coughing", "hacking"],
    "sore-throat": ["sore throat", "throat pain", "hurts to swallow"],

    # Gastrointestinal
    "nausea": ["nausea", "nauseous", "queasy", "sick to stomach"],
    "vomiting": ["vomiting", "throwing up", "vomit", "puking"],
    "diarrhea": ["diarrhea", "loose stool", "runny stool"],
    "abdominal-pain": ["stomach pain", "abdominal pain", "belly pain", "stomach ache"],

    # Muscular & Pain
    "chest-pain": ["chest pain", "chest hurts", "chest pressure"],
    "muscle-pain": ["muscle pain", "body aches", "sore muscles", "aching"],
    "joint-pain": ["joint pain", "joints hurt", "stiff joints"],

    # Skin
    "rash": ["rash", "skin rash", "spots", "bumps"],

    # Energy & Consciousness
    "fatigue": ["tired", "fatigue", "exhausted", "weakness", "weak"],
    "loss-of-consciousness": ["passed out", "fainted", "blacked out", "unconscious"],
}

# Severity indicators
SEVERITY_HIGH = ["severe", "extreme", "worst", "unbearable", "terrible", "intense"]
SEVERITY_MEDIUM = ["moderate", "significant", "bad", "strong"]
SEVERITY_LOW = ["mild", "slight", "little bit", "somewhat"]


class SymptomExtractor:
    """Extracts and normalizes symptoms from natural language text"""

    @staticmethod
    def extract_symptoms(text: str) -> List[Symptom]:
        """
        Extract symptoms from user text

        Returns list of Symptom objects with normalized names
        """
        text_lower = text.lower()
        symptoms = []

        # Find matching symptoms
        for symptom_name, keywords in SYMPTOM_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Estimate severity based on descriptors
                    severity = SymptomExtractor._estimate_severity(text_lower)

                    # Extract duration if present
                    duration = SymptomExtractor._extract_duration(text_lower)

                    symptom = Symptom(
                        name=symptom_name,
                        raw_text=keyword,
                        severity=severity,
                        duration=duration,
                    )
                    symptoms.append(symptom)
                    break  # Only match once per symptom type

        return symptoms

    @staticmethod
    def _estimate_severity(text: str) -> int:
        """Estimate severity 1-10 based on descriptive words"""
        if any(word in text for word in SEVERITY_HIGH):
            return 8
        elif any(word in text for word in SEVERITY_MEDIUM):
            return 5
        elif any(word in text for word in SEVERITY_LOW):
            return 3
        else:
            return 5  # Default moderate

    @staticmethod
    def _extract_duration(text: str) -> Optional[str]:
        """Extract duration information from text"""
        # Pattern: "for X days/hours/weeks"
        duration_pattern = r'for\s+(\d+)\s+(day|days|hour|hours|week|weeks)'
        match = re.search(duration_pattern, text)
        if match:
            return f"{match.group(1)} {match.group(2)}"

        # Pattern: "X days/hours ago"
        ago_pattern = r'(\d+)\s+(day|days|hour|hours|week|weeks)\s+ago'
        match = re.search(ago_pattern, text)
        if match:
            return f"{match.group(1)} {match.group(2)}"

        # Check for keywords
        if "yesterday" in text:
            return "1 day"
        if "this morning" in text or "today" in text:
            return "hours"
        if "this week" in text:
            return "days"

        return None

    @staticmethod
    def extract_age(text: str) -> Optional[int]:
        """Extract age from text"""
        # Pattern: "I am X years old" or "X year old"
        age_pattern = r'(\d+)\s*(year|years|yr|yrs)\s*old'
        match = re.search(age_pattern, text.lower())
        if match:
            return int(match.group(1))
        return None


# ============================================================================
# Message Handlers
# ============================================================================

# Session tracking for follow-up questions
session_context: Dict[str, Dict] = {}

# Rate limiting configuration
rate_limit_store: Dict[str, List[datetime]] = {}
MAX_REQUESTS_PER_HOUR = 20
MAX_MESSAGE_LENGTH = 2000


def check_rate_limit(sender: str) -> bool:
    """Check if sender has exceeded rate limit"""
    now = datetime.utcnow()

    # Initialize or clean up old requests
    if sender not in rate_limit_store:
        rate_limit_store[sender] = []

    # Remove requests older than 1 hour
    rate_limit_store[sender] = [
        t for t in rate_limit_store[sender]
        if (now - t).total_seconds() < 3600
    ]

    # Check if under limit
    if len(rate_limit_store[sender]) >= MAX_REQUESTS_PER_HOUR:
        return False

    # Add current request
    rate_limit_store[sender].append(now)
    return True


def validate_input(text: str) -> Optional[str]:
    """
    Validate input message
    Returns error message if invalid, None if valid
    """
    if not text or len(text.strip()) == 0:
        return "Empty message received. Please describe your symptoms."

    if len(text) > MAX_MESSAGE_LENGTH:
        return f"Message too long ({len(text)} characters). Please keep messages under {MAX_MESSAGE_LENGTH} characters."

    # Basic sanity check - must contain at least some alphabetic characters
    if not any(c.isalpha() for c in text):
        return "Please describe your symptoms using text."

    return None


def needs_clarification(symptoms: List[Symptom], age: Optional[int], text: str) -> Optional[str]:
    """
    Determine if clarification is needed and return appropriate question
    Returns None if all necessary data is present
    """
    if not symptoms:
        return ("I didn't detect any specific symptoms. Could you describe what you're experiencing?\n\n"
                "Examples:\n"
                "• 'I have a fever and headache'\n"
                "• 'My stomach hurts and I feel nauseous'\n"
                "• 'I'm having chest pain and shortness of breath'")

    # Check for critical symptoms without duration
    critical_symptoms = ["chest_pain", "shortness_of_breath", "confusion", "loss_of_consciousness"]
    critical_without_duration = [s for s in symptoms if s.name in critical_symptoms and not s.duration]

    if critical_without_duration:
        symptom_names = ', '.join([s.name.replace('_', ' ') for s in critical_without_duration])
        return (f"You mentioned {symptom_names}. This could be important.\n\n"
                f"How long have you been experiencing this? (e.g., '2 hours', '3 days')")

    # Check if age is missing for fever cases (important for diagnosis)
    has_fever = any(s.name == "fever" for s in symptoms)
    if has_fever and not age:
        return ("I see you have a fever. Your age helps with accurate assessment.\n\n"
                "How old are you?")

    # Check for symptoms without severity on second pass
    symptoms_without_severity = [s for s in symptoms if not s.severity or s.severity == 5]
    if len(symptoms_without_severity) > 0 and len(symptoms) <= 2:
        # Only ask for severity if we have few symptoms
        symptom_name = symptoms_without_severity[0].name.replace('_', ' ')
        return (f"How would you describe the severity of your {symptom_name}?\n\n"
                f"• Mild (1-3)\n"
                f"• Moderate (4-6)\n"
                f"• Severe (7-10)")

    return None


@inter_agent_proto.on_message(model=IntakeTextMessage)
async def handle_intake_message(ctx: Context, sender: str, msg: IntakeTextMessage):
    """
    Process incoming patient symptom descriptions
    Extract structured data and send to coordinator with clarifying questions
    """
    ctx.logger.info(f"Received intake message from {sender}")
    ctx.logger.info(f"Session: {msg.session_id}")
    ctx.logger.info(f"Text: {msg.text}")

    # Rate limiting check
    if not check_rate_limit(sender):
        ctx.logger.warning(f"Rate limit exceeded for {sender}")
        response = AgentAcknowledgement(
            session_id=msg.session_id,
            agent_name="patient_intake",
            message=(
                "⚠️ Too many requests. You've exceeded the rate limit of "
                f"{MAX_REQUESTS_PER_HOUR} requests per hour.\n\n"
                "Please wait a moment before sending more messages.\n\n"
                "If you're experiencing a medical emergency, please call emergency services immediately."
            )
        )
        await ctx.send(sender, response)
        return

    # Input validation
    validation_error = validate_input(msg.text)
    if validation_error:
        ctx.logger.warning(f"Input validation failed for {sender}: {validation_error}")
        response = AgentAcknowledgement(
            session_id=msg.session_id,
            agent_name="patient_intake",
            message=validation_error
        )
        await ctx.send(sender, response)
        return

    # Track session context
    if msg.session_id not in session_context:
        session_context[msg.session_id] = {
            "messages": [],
            "clarification_count": 0
        }

    session_context[msg.session_id]["messages"].append(msg.text)
    session_context[msg.session_id]["clarification_count"] += 1

    # Extract symptoms from text
    symptoms = SymptomExtractor.extract_symptoms(msg.text)

    # Extract age if mentioned
    age = SymptomExtractor.extract_age(msg.text)

    # Check if we need clarification
    clarification = needs_clarification(symptoms, age, msg.text)

    # Skip clarification for HTTP sessions (one-shot diagnostic)
    is_http_session = msg.session_id.startswith("http-")

    # Limit clarification attempts to 2 to avoid endless loops
    max_clarifications = 2
    if clarification and not is_http_session and session_context[msg.session_id]["clarification_count"] <= max_clarifications:
        ctx.logger.info(f"Requesting clarification for session {msg.session_id}")
        response = AgentAcknowledgement(
            session_id=msg.session_id,
            agent_name="patient_intake",
            message=clarification
        )
        await ctx.send(sender, response)
        return

    # If no symptoms after max clarifications, provide helpful message
    if not symptoms:
        ctx.logger.warning(f"No symptoms extracted after {max_clarifications} attempts")
        response = AgentAcknowledgement(
            session_id=msg.session_id,
            agent_name="patient_intake",
            message=("I'm having trouble identifying specific symptoms from your description. "
                    "For the most accurate assessment, please consult a healthcare provider directly.\n\n"
                    "If this is an emergency, please call emergency services immediately.")
        )
        await ctx.send(sender, response)
        return

    # Structure patient data with complete information
    patient_data = PatientIntakeData(
        session_id=msg.session_id,
        symptoms=symptoms,
        age=age,
        timestamp=datetime.utcnow()
    )

    ctx.logger.info(f"✅ Complete patient data extracted:")
    ctx.logger.info(f"   Symptoms: {[s.name for s in symptoms]}")
    ctx.logger.info(f"   Age: {age}")
    ctx.logger.info(f"   Session messages: {len(session_context[msg.session_id]['messages'])}")

    # Send structured acknowledgement
    symptom_list = ', '.join([s.name.replace('_', ' ') for s in symptoms])
    severity_info = ', '.join([f"{s.name.replace('_', ' ')} (severity {s.severity}/10)"
                               for s in symptoms if s.severity])

    ack_message = (
        f"✅ Information received:\n\n"
        f"Symptoms: {symptom_list}\n"
        f"{severity_info if severity_info else ''}\n"
        f"{'Age: ' + str(age) if age else 'Age: Not provided'}\n\n"
        f"Analyzing your symptoms..."
    )

    ack = AgentAcknowledgement(
        session_id=msg.session_id,
        agent_name="patient_intake",
        message=ack_message
    )
    await ctx.send(sender, ack)

    # Create diagnostic request for coordinator
    diagnostic_request = DiagnosticRequest(
        session_id=msg.session_id,
        patient_data=patient_data,
        requesting_agent="patient_intake",
        analysis_type="symptom_analysis"
    )

    # Send to coordinator (get address from env)
    coordinator_addr = os.getenv("COORDINATOR_ADDRESS")
    if coordinator_addr and coordinator_addr != "agent1q...":
        ctx.logger.info(f"📤 Sending diagnostic request to coordinator: {coordinator_addr[:20]}...")
        await ctx.send(coordinator_addr, diagnostic_request)
    else:
        ctx.logger.warning("Coordinator address not configured in .env")


@agent.on_event("startup")
async def startup(ctx: Context):
    """Log agent startup information"""
    ctx.logger.info(f"Patient Intake Agent started!")
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"Agent name: {agent.name}")
    ctx.logger.info(f"Mailbox: Enabled (ASI:One compatible)")
    ctx.logger.info(f"Ready to extract patient symptoms")


# Include the inter-agent protocol
agent.include(inter_agent_proto)


if __name__ == "__main__":
    agent.run()
