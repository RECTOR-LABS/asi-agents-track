"""
MediChain AI - Patient Intake Agent (Cloud Deployment - PATCHED v5)
Ultra-simplified message models (no nested types) to avoid schema digest mismatch.

DEPLOYMENT: Replace the existing patient_intake agent.py with this patched version.
"""

from datetime import datetime
from typing import List, Dict, Optional
import re
import json

# Import uagents framework
from uagents import Agent, Context, Model

# ============================================================================
# AGENT ADDRESSES
# ============================================================================

COORDINATOR_ADDRESS = "agent1qdp74ezv3eas5q60s4650xt97ew5kmyt9de77w2ku55jxys8uq2uk0u440d"

# ============================================================================
# MESSAGE MODELS - Ultra-simplified (no nested types)
# ============================================================================

class IntakeTextMessage(Model):
    """Message from coordinator - ULTRA SIMPLE"""
    text: str
    session_id: str


class AgentAcknowledgement(Model):
    """Acknowledgement message - ULTRA SIMPLE"""
    session_id: str
    agent_name: str
    message: str


class DiagnosticRequest(Model):
    """Diagnostic request - serialized as JSON string"""
    session_id: str
    patient_data_json: str  # JSON serialized PatientIntakeData
    requesting_agent: str
    analysis_type: str


# ============================================================================
# INTERNAL DATA STRUCTURES (not used in inter-agent messages)
# ============================================================================

class Symptom:
    """Internal symptom representation"""
    def __init__(self, name: str, raw_text: str, severity: int = 5, duration: Optional[str] = None):
        self.name = name
        self.raw_text = raw_text
        self.severity = severity
        self.duration = duration

    def to_dict(self):
        return {
            "name": self.name,
            "raw_text": self.raw_text,
            "severity": self.severity,
            "duration": self.duration
        }


# ============================================================================
# SYMPTOM EXTRACTION
# ============================================================================

SYMPTOM_KEYWORDS = {
    "high-fever": ["high fever", "very high temperature", "burning up with fever"],
    "fever": ["fever", "high temperature", "temp", "hot"],
    "chills": ["chills", "shivering", "shaking", "cold"],
    "severe-headache": ["severe headache", "terrible headache", "worst headache", "intense headache"],
    "headache": ["headache", "head pain", "head hurts", "migraine", "head ache"],
    "dizziness": ["dizzy", "lightheaded", "vertigo", "spinning"],
    "confusion": ["confused", "disoriented", "foggy", "can't think"],
    "neck-stiffness": ["neck is very stiff", "neck is stiff", "very stiff neck", "extremely stiff neck"],
    "stiff-neck": ["stiff neck", "neck stiff", "can't move neck", "neck hurts to move"],
    "difficulty-breathing": ["difficulty breathing", "hard to breathe", "can't breathe well"],
    "shortness-of-breath": ["short of breath", "can't breathe", "breathless", "gasping"],
    "cough": ["cough", "coughing", "hacking"],
    "sore-throat": ["sore throat", "throat pain", "hurts to swallow"],
    "nausea": ["nausea", "nauseous", "queasy", "sick to stomach"],
    "vomiting": ["vomiting", "throwing up", "vomit", "puking"],
    "diarrhea": ["diarrhea", "loose stool", "runny stool"],
    "abdominal-pain": ["stomach pain", "abdominal pain", "belly pain", "stomach ache"],
    "chest-pain": ["chest pain", "chest hurts", "chest pressure"],
    "muscle-pain": ["muscle pain", "body aches", "sore muscles", "aching"],
    "joint-pain": ["joint pain", "joints hurt", "stiff joints"],
    "rash": ["rash", "skin rash", "spots", "bumps"],
    "fatigue": ["tired", "fatigue", "exhausted", "weakness", "weak"],
    "loss-of-consciousness": ["passed out", "fainted", "blacked out", "unconscious"],
}

SEVERITY_HIGH = ["severe", "extreme", "worst", "unbearable", "terrible", "intense"]
SEVERITY_MEDIUM = ["moderate", "significant", "bad", "strong"]
SEVERITY_LOW = ["mild", "slight", "little bit", "somewhat"]


class SymptomExtractor:
    @staticmethod
    def extract_symptoms(text: str) -> List[Symptom]:
        text_lower = text.lower()
        symptoms = []

        for symptom_name, keywords in SYMPTOM_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    severity = SymptomExtractor._estimate_severity(text_lower)
                    duration = SymptomExtractor._extract_duration(text_lower)
                    symptom = Symptom(
                        name=symptom_name,
                        raw_text=keyword,
                        severity=severity,
                        duration=duration,
                    )
                    symptoms.append(symptom)
                    break

        return symptoms

    @staticmethod
    def _estimate_severity(text: str) -> int:
        if any(word in text for word in SEVERITY_HIGH):
            return 8
        elif any(word in text for word in SEVERITY_MEDIUM):
            return 5
        elif any(word in text for word in SEVERITY_LOW):
            return 3
        else:
            return 5

    @staticmethod
    def _extract_duration(text: str) -> Optional[str]:
        duration_pattern = r'for\s+(\d+)\s+(day|days|hour|hours|week|weeks)'
        match = re.search(duration_pattern, text)
        if match:
            return f"{match.group(1)} {match.group(2)}"

        ago_pattern = r'(\d+)\s+(day|days|hour|hours|week|weeks)\s+ago'
        match = re.search(ago_pattern, text)
        if match:
            return f"{match.group(1)} {match.group(2)}"

        if "yesterday" in text:
            return "1 day"
        if "this morning" in text or "today" in text:
            return "hours"
        if "this week" in text:
            return "days"

        return None

    @staticmethod
    def extract_age(text: str) -> Optional[int]:
        age_pattern = r'(\d+)\s*(year|years|yr|yrs)\s*old'
        match = re.search(age_pattern, text.lower())
        if match:
            return int(match.group(1))
        return None


# ============================================================================
# SESSION TRACKING
# ============================================================================

session_context: Dict[str, Dict] = {}


def needs_clarification(symptoms: List[Symptom], age: Optional[int], text: str) -> Optional[str]:
    if not symptoms:
        return ("I didn't detect any specific symptoms. Could you describe what you're experiencing?\n\n"
                "Examples:\n"
                "• 'I have a fever and headache'\n"
                "• 'My stomach hurts and I feel nauseous'\n"
                "• 'I'm having chest pain and shortness of breath'")

    critical_symptoms = ["chest-pain", "shortness-of-breath", "confusion", "loss-of-consciousness"]
    critical_without_duration = [s for s in symptoms if s.name in critical_symptoms and not s.duration]

    if critical_without_duration:
        symptom_names = ', '.join([s.name.replace('_', ' ') for s in critical_without_duration])
        return (f"You mentioned {symptom_names}. This could be important.\n\n"
                f"How long have you been experiencing this? (e.g., '2 hours', '3 days')")

    has_fever = any(s.name == "fever" for s in symptoms)
    if has_fever and not age:
        return ("I see you have a fever. Your age helps with accurate assessment.\n\n"
                "How old are you?")

    return None


# ============================================================================
# AGENT INITIALIZATION
# ============================================================================

agent = Agent()


# ============================================================================
# MESSAGE HANDLER
# ============================================================================

@agent.on_message(model=IntakeTextMessage)
async def handle_intake_message(ctx: Context, sender: str, msg: IntakeTextMessage):
    """Process incoming patient symptom descriptions"""
    ctx.logger.info(f"✅ [PATCH v5] Received intake message from {sender}")
    ctx.logger.info(f"   Session: {msg.session_id}")
    ctx.logger.info(f"   Text: {msg.text}")

    # Track session
    if msg.session_id not in session_context:
        session_context[msg.session_id] = {
            "messages": [],
            "clarification_count": 0
        }

    session_context[msg.session_id]["messages"].append(msg.text)
    session_context[msg.session_id]["clarification_count"] += 1

    # Extract symptoms
    symptoms = SymptomExtractor.extract_symptoms(msg.text)
    age = SymptomExtractor.extract_age(msg.text)

    # Check clarification
    clarification = needs_clarification(symptoms, age, msg.text)

    max_clarifications = 2
    if clarification and session_context[msg.session_id]["clarification_count"] <= max_clarifications:
        ctx.logger.info(f"Requesting clarification")
        response = AgentAcknowledgement(
            session_id=msg.session_id,
            agent_name="patient_intake",
            message=clarification
        )
        await ctx.send(sender, response)
        return

    # No symptoms
    if not symptoms:
        ctx.logger.warning(f"No symptoms extracted")
        response = AgentAcknowledgement(
            session_id=msg.session_id,
            agent_name="patient_intake",
            message=("I'm having trouble identifying specific symptoms. "
                    "Please consult a healthcare provider.\n\n"
                    "If this is an emergency, call emergency services.")
        )
        await ctx.send(sender, response)
        return

    # Build patient data
    patient_data = {
        "session_id": msg.session_id,
        "symptoms": [s.to_dict() for s in symptoms],
        "age": age,
        "timestamp": datetime.utcnow().isoformat(),
        "medical_history": None,
        "allergies": None,
        "current_medications": None
    }

    ctx.logger.info(f"✅ Extracted patient data:")
    ctx.logger.info(f"   Symptoms: {[s.name for s in symptoms]}")
    ctx.logger.info(f"   Age: {age}")

    # Send acknowledgement
    symptom_list = ', '.join([s.name.replace('_', ' ').replace('-', ' ') for s in symptoms])

    ack_message = (
        f"✅ Information received:\n\n"
        f"Symptoms: {symptom_list}\n"
        f"{'Age: ' + str(age) if age else 'Age: Not provided'}\n\n"
        f"Analyzing your symptoms..."
    )

    ack = AgentAcknowledgement(
        session_id=msg.session_id,
        agent_name="patient_intake",
        message=ack_message
    )
    await ctx.send(sender, ack)

    # Send diagnostic request with JSON serialization
    diagnostic_request = DiagnosticRequest(
        session_id=msg.session_id,
        patient_data_json=json.dumps(patient_data),
        requesting_agent="patient_intake",
        analysis_type="symptom_analysis"
    )

    ctx.logger.info(f"📤 Sending diagnostic request to coordinator")
    await ctx.send(COORDINATOR_ADDRESS, diagnostic_request)


# ============================================================================
# STARTUP
# ============================================================================

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("=" * 60)
    ctx.logger.info("MediChain AI - Patient Intake Agent (PATCH v5)")
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"Agent address: {agent.address}")
    ctx.logger.info(f"Message handling: Ultra-simplified models (no nesting)")
    ctx.logger.info(f"Ready to extract patient symptoms")
    ctx.logger.info("=" * 60)
