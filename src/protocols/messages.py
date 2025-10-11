"""
Message Models for Inter-Agent Communication
MediChain AI - ASI Agents Track Hackathon
"""

from uagents import Model
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime


# ============================================================================
# Enums for Classification
# ============================================================================

class UrgencyLevel(str, Enum):
    """Classification of medical urgency"""
    EMERGENCY = "emergency"  # Life-threatening, immediate ER
    URGENT = "urgent"        # Medical attention within 24 hours
    ROUTINE = "routine"      # Can schedule regular appointment


class ConfidenceLevel(str, Enum):
    """Confidence in diagnostic assessment"""
    HIGH = "high"      # >80% confidence
    MEDIUM = "medium"  # 50-80% confidence
    LOW = "low"        # <50% confidence


# ============================================================================
# Inter-Agent Communication Models
# ============================================================================

class IntakeTextMessage(Model):
    """Simple text message for patient intake from coordinator"""
    text: str
    session_id: str


# ============================================================================
# Symptom Data Models
# ============================================================================

class Symptom(BaseModel):
    """Individual symptom with metadata"""
    name: str = Field(..., description="Normalized symptom name")
    raw_text: str = Field(..., description="Original user description")
    severity: Optional[int] = Field(None, ge=1, le=10, description="Severity 1-10")
    duration: Optional[str] = Field(None, description="How long symptom present")
    frequency: Optional[str] = Field(None, description="How often it occurs")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "fever",
                "raw_text": "I have a really high temperature",
                "severity": 8,
                "duration": "3 days",
                "frequency": "constant"
            }
        }


class PatientIntakeData(BaseModel):
    """Structured patient symptom data from intake agent"""
    session_id: str = Field(..., description="Unique session identifier")
    symptoms: List[Symptom] = Field(..., description="List of symptoms")
    age: Optional[int] = Field(None, ge=0, le=150)
    medical_history: Optional[List[str]] = Field(None, description="Relevant medical history")
    allergies: Optional[List[str]] = Field(None, description="Known allergies")
    current_medications: Optional[List[str]] = Field(None, description="Current medications")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session-123-456",
                "symptoms": [
                    {"name": "fever", "raw_text": "high temperature", "severity": 8}
                ],
                "age": 35,
                "allergies": ["penicillin"]
            }
        }


# ============================================================================
# Diagnostic Request/Response Models
# ============================================================================

class DiagnosticRequest(BaseModel):
    """Request for diagnostic analysis from coordinator to specialists"""
    session_id: str
    patient_data: PatientIntakeData
    requesting_agent: str = Field(..., description="Agent making the request")
    analysis_type: str = Field(..., description="Type of analysis needed")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PossibleCondition(BaseModel):
    """A possible medical condition with confidence"""
    condition_name: str
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence 0-1")
    confidence_level: ConfidenceLevel
    matching_symptoms: List[str] = Field(..., description="Symptoms that match")
    reasoning: str = Field(..., description="Why this condition suspected")
    metta_query_used: Optional[str] = Field(None, description="MeTTa query for transparency")


class DiagnosticResponse(BaseModel):
    """Response from diagnostic agent (Knowledge Graph or Symptom Analysis)"""
    session_id: str
    possible_conditions: List[PossibleCondition]
    urgency_level: UrgencyLevel
    red_flags: List[str] = Field(default=[], description="Critical warning symptoms")
    reasoning_chain: List[str] = Field(..., description="Step-by-step reasoning")
    responding_agent: str = Field(..., description="Agent providing response")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Treatment Request/Response Models
# ============================================================================

class TreatmentRequest(BaseModel):
    """Request for treatment recommendations"""
    session_id: str
    diagnosed_condition: str = Field(..., description="Primary suspected condition")
    patient_data: PatientIntakeData
    urgency_level: UrgencyLevel
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class TreatmentRecommendation(BaseModel):
    """Individual treatment recommendation"""
    treatment_type: str = Field(..., description="Type (medication, procedure, lifestyle)")
    description: str
    evidence_source: Optional[str] = Field(None, description="CDC/WHO guideline link")
    contraindications: List[str] = Field(default=[], description="When NOT to use")
    priority: int = Field(..., ge=1, le=5, description="Priority 1=highest")


class TreatmentResponse(BaseModel):
    """Response from treatment recommendation agent"""
    session_id: str
    condition: str
    recommendations: List[TreatmentRecommendation]
    specialist_referral: Optional[str] = Field(None, description="Specialist to see")
    follow_up_timeline: Optional[str] = Field(None, description="When to follow up")
    medical_disclaimer: str = Field(
        default="This is NOT medical advice. Consult a licensed healthcare provider."
    )
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Aggregated Response for User
# ============================================================================

class FinalDiagnosticReport(BaseModel):
    """Final aggregated report from coordinator to user"""
    session_id: str

    # Symptom summary
    symptoms_analyzed: List[str]

    # Assessment
    urgency_level: UrgencyLevel
    primary_conditions: List[PossibleCondition]

    # Recommendations
    immediate_actions: List[str] = Field(..., description="What to do right now")
    treatment_recommendations: List[TreatmentRecommendation]
    specialist_referral: Optional[str] = None

    # Transparency
    reasoning_summary: str = Field(..., description="Plain language explanation")
    metta_reasoning_chain: List[str] = Field(default=[], description="MeTTa queries used")

    # Safety
    red_flags: List[str] = Field(default=[])
    disclaimer: str = Field(
        default="⚠️ IMPORTANT: This is an AI-powered preliminary assessment, "
                "NOT a medical diagnosis. Always consult a licensed healthcare "
                "professional for medical advice."
    )

    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Acknowledgement Messages
# ============================================================================

class AgentAcknowledgement(BaseModel):
    """Generic acknowledgement from agent"""
    session_id: str
    agent_name: str
    message: str = Field(default="Request received and processing")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorMessage(BaseModel):
    """Error message from agent"""
    session_id: str
    agent_name: str
    error_type: str
    error_details: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Epic 3: uAgents.Model Wrappers for Mailbox Communication
# ============================================================================

class SymptomAnalysisRequestMsg(Model):
    """
    Mailbox-compatible request for Symptom Analysis Agent
    Wraps patient intake data for inter-agent communication
    """
    session_id: str
    symptoms: List[str]  # Simplified symptom names
    age: Optional[int]
    severity_scores: Optional[Dict[str, int]]  # symptom -> severity (1-10)
    duration_info: Optional[Dict[str, str]]  # symptom -> duration
    medical_history: Optional[List[str]]
    requesting_agent: str


class SymptomAnalysisResponseMsg(Model):
    """
    Mailbox-compatible response from Symptom Analysis Agent
    Contains urgency assessment and differential diagnoses
    """
    session_id: str
    urgency_level: str  # "emergency" | "urgent" | "routine"
    red_flags: List[str]
    differential_diagnoses: List[str]  # condition names
    confidence_scores: Dict[str, float]  # condition -> confidence (0-1)
    reasoning_chain: List[str]
    recommended_next_step: str
    responding_agent: str


class TreatmentRequestMsg(Model):
    """
    Mailbox-compatible request for Treatment Recommendation Agent
    """
    session_id: str
    primary_condition: str
    alternative_conditions: Optional[List[str]]
    urgency_level: str
    patient_age: Optional[int]
    allergies: Optional[List[str]]
    current_medications: Optional[List[str]]
    medical_history: Optional[List[str]]
    requesting_agent: str


class TreatmentResponseMsg(Model):
    """
    Mailbox-compatible response from Treatment Recommendation Agent
    Contains evidence-based treatment recommendations with safety checks
    """
    session_id: str
    condition: str
    treatments: List[str]  # Treatment descriptions
    evidence_sources: Dict[str, str]  # treatment -> source URL
    contraindications: Dict[str, List[str]]  # treatment -> contraindication list
    safety_warnings: List[str]
    specialist_referral: Optional[str]
    follow_up_timeline: Optional[str]
    medical_disclaimer: str
    responding_agent: str
