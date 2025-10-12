"""
Protocol definitions for MediChain AI multi-agent system
"""

from .messages import (
    # Enums
    UrgencyLevel,
    ConfidenceLevel,

    # Inter-agent communication
    IntakeTextMessage,

    # Symptom models
    Symptom,
    PatientIntakeData,

    # Diagnostic models
    DiagnosticRequest,
    PossibleCondition,
    DiagnosticResponse,

    # Treatment models
    TreatmentRequest,
    TreatmentRecommendation,
    TreatmentResponse,

    # Final report
    FinalDiagnosticReport,

    # Utility messages
    AgentAcknowledgement,
    ErrorMessage,

    # Epic 3: Mailbox communication models
    SymptomAnalysisRequestMsg,
    SymptomAnalysisResponseMsg,
    TreatmentRequestMsg,
    TreatmentResponseMsg,
    AgentAcknowledgementMsg,  # Mailbox-compatible acknowledgement
)

__all__ = [
    "UrgencyLevel",
    "ConfidenceLevel",
    "IntakeTextMessage",
    "Symptom",
    "PatientIntakeData",
    "DiagnosticRequest",
    "PossibleCondition",
    "DiagnosticResponse",
    "TreatmentRequest",
    "TreatmentRecommendation",
    "TreatmentResponse",
    "FinalDiagnosticReport",
    "AgentAcknowledgement",
    "ErrorMessage",
    "SymptomAnalysisRequestMsg",
    "SymptomAnalysisResponseMsg",
    "TreatmentRequestMsg",
    "TreatmentResponseMsg",
    "AgentAcknowledgementMsg",
]
