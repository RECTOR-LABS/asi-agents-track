"""
Integration Tests for Agent Communication Workflows
Tests end-to-end diagnostic flows and inter-agent messaging
"""
import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
from src.protocols.messages import (
    Symptom,
    PatientIntakeData,
    DiagnosticRequest,
    DiagnosticResponse,
    PossibleCondition,
    AgentAcknowledgement,
    UrgencyLevel,
    ConfidenceLevel,
    IntakeTextMessage,
)
from src.agents.patient_intake import SymptomExtractor, needs_clarification
from src.metta.query_engine import MeTTaQueryEngine


@pytest.mark.integration
class TestPatientIntakeToKnowledgeGraph:
    """Test Patient Intake → Knowledge Graph Agent flow"""

    def test_diagnostic_request_creation(self):
        """Test creating a diagnostic request from patient intake"""
        # Simulate patient intake extracting symptoms
        text = "I have a severe fever and headache for 3 days. I'm 45 years old."
        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        # Create patient intake data
        patient_data = PatientIntakeData(
            session_id="test-session-123",
            symptoms=symptoms,
            age=age,
            timestamp=datetime.utcnow()
        )

        # Create diagnostic request
        diagnostic_request = DiagnosticRequest(
            session_id="test-session-123",
            patient_data=patient_data,
            requesting_agent="patient_intake",
            analysis_type="symptom_analysis"
        )

        # Verify request structure
        assert diagnostic_request.session_id == "test-session-123"
        assert diagnostic_request.requesting_agent == "patient_intake"
        assert diagnostic_request.analysis_type == "symptom_analysis"
        assert len(diagnostic_request.patient_data.symptoms) > 0
        assert diagnostic_request.patient_data.age == 45

    def test_diagnostic_response_structure(self):
        """Test diagnostic response structure from Knowledge Graph"""
        # Create sample diagnostic response
        conditions = [
            PossibleCondition(
                condition_name="meningitis",
                confidence=0.85,
                confidence_level=ConfidenceLevel.HIGH,
                matching_symptoms=["fever", "severe-headache"],
                reasoning="High fever with severe headache matches meningitis presentation",
                metta_query_used="find_conditions_by_symptoms(['fever', 'severe-headache'])"
            ),
            PossibleCondition(
                condition_name="influenza",
                confidence=0.65,
                confidence_level=ConfidenceLevel.MEDIUM,
                matching_symptoms=["fever", "headache"],
                reasoning="Common flu symptoms present",
                metta_query_used="differential_diagnosis(meningitis)"
            )
        ]

        response = DiagnosticResponse(
            session_id="test-session-123",
            possible_conditions=conditions,
            urgency_level=UrgencyLevel.EMERGENCY,
            red_flags=["severe-headache"],
            reasoning_chain=["MeTTa analysis performed", "Emergency condition detected"],
            responding_agent="knowledge_graph"
        )

        # Verify response structure
        assert response.session_id == "test-session-123"
        assert len(response.possible_conditions) == 2
        assert response.urgency_level == UrgencyLevel.EMERGENCY
        assert "severe-headache" in response.red_flags
        assert response.responding_agent == "knowledge_graph"

    def test_end_to_end_diagnostic_flow(self):
        """Test complete flow: Intake → MeTTa Query → Response"""
        # Step 1: Patient Intake extracts symptoms
        text = "I have fever, headache, and stiff neck. I'm 30 years old."
        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        assert len(symptoms) >= 3
        symptom_names = [s.name for s in symptoms]
        assert "fever" in symptom_names
        assert age == 30

        # Step 2: Create patient intake data
        patient_data = PatientIntakeData(
            session_id="test-flow-456",
            symptoms=symptoms,
            age=age,
            timestamp=datetime.utcnow()
        )

        # Step 3: Query MeTTa KB (simulating Knowledge Graph Agent)
        engine = MeTTaQueryEngine()
        symptom_names_normalized = [s.replace('_', '-') for s in symptom_names]
        condition_matches = engine.find_conditions_by_symptoms(symptom_names_normalized)

        # Should find meningitis with high confidence (3 symptom matches)
        assert len(condition_matches) > 0
        assert "meningitis" in [str(c) for c in condition_matches.keys()]

        # Step 4: Check urgency
        urgency = engine.find_urgency_level("meningitis")
        assert urgency == "emergency"

        # Step 5: Generate reasoning
        reasoning = engine.generate_reasoning_chain(symptom_names_normalized, "meningitis")
        assert reasoning is not None
        assert len(reasoning) > 0
        assert "meningitis" in reasoning.lower()


@pytest.mark.integration
class TestCoordinatorRouting:
    """Test Coordinator Agent routing logic"""

    def test_route_to_patient_intake(self):
        """Test routing user text to patient intake agent"""
        # Simulate user message
        user_message = IntakeTextMessage(
            session_id="test-routing-789",
            text="I have a headache and fever"
        )

        # Verify message structure for routing
        assert user_message.session_id == "test-routing-789"
        assert user_message.text is not None
        assert len(user_message.text) > 0

    def test_route_diagnostic_request(self):
        """Test routing diagnostic request from intake to knowledge graph"""
        # Create diagnostic request
        symptoms = [
            Symptom(name="fever", raw_text="fever", severity=8, duration="2 days"),
            Symptom(name="cough", raw_text="cough", severity=6, duration="3 days"),
        ]

        patient_data = PatientIntakeData(
            session_id="test-diagnostic-routing",
            symptoms=symptoms,
            age=35,
            timestamp=datetime.utcnow()
        )

        diagnostic_request = DiagnosticRequest(
            session_id="test-diagnostic-routing",
            patient_data=patient_data,
            requesting_agent="patient_intake",
            analysis_type="symptom_analysis"
        )

        # Verify routing metadata
        assert diagnostic_request.requesting_agent == "patient_intake"
        assert diagnostic_request.analysis_type in ["symptom_analysis", "treatment_recommendation"]


@pytest.mark.integration
class TestMessageProtocols:
    """Test message protocol adherence"""

    def test_agent_acknowledgement_structure(self):
        """Test AgentAcknowledgement message structure"""
        ack = AgentAcknowledgement(
            session_id="test-ack-001",
            agent_name="patient_intake",
            message="Symptoms received and analyzed"
        )

        assert ack.session_id == "test-ack-001"
        assert ack.agent_name == "patient_intake"
        assert ack.message is not None

    def test_symptom_model_validation(self):
        """Test Symptom model validation"""
        # Valid symptom
        symptom = Symptom(
            name="fever",
            raw_text="high fever",
            severity=8,
            duration="3 days"
        )

        assert symptom.name == "fever"
        assert symptom.severity == 8
        assert symptom.duration == "3 days"

    def test_patient_intake_data_validation(self):
        """Test PatientIntakeData model validation"""
        symptoms = [
            Symptom(name="fever", raw_text="fever", severity=7, duration="2 days")
        ]

        patient_data = PatientIntakeData(
            session_id="test-validation-123",
            symptoms=symptoms,
            age=45,
            timestamp=datetime.utcnow()
        )

        assert patient_data.session_id == "test-validation-123"
        assert len(patient_data.symptoms) == 1
        assert patient_data.age == 45
        assert patient_data.timestamp is not None

    def test_possible_condition_confidence_levels(self):
        """Test PossibleCondition confidence level mapping"""
        # High confidence
        high_conf = PossibleCondition(
            condition_name="meningitis",
            confidence=0.95,
            confidence_level=ConfidenceLevel.HIGH,
            matching_symptoms=["fever", "headache", "stiff-neck"],
            reasoning="All key symptoms present",
            metta_query_used="test_query"
        )

        assert high_conf.confidence >= 0.8
        assert high_conf.confidence_level == ConfidenceLevel.HIGH

        # Medium confidence
        med_conf = PossibleCondition(
            condition_name="influenza",
            confidence=0.65,
            confidence_level=ConfidenceLevel.MEDIUM,
            matching_symptoms=["fever", "cough"],
            reasoning="Some symptoms match",
            metta_query_used="test_query"
        )

        assert 0.5 <= med_conf.confidence < 0.8
        assert med_conf.confidence_level == ConfidenceLevel.MEDIUM

        # Low confidence
        low_conf = PossibleCondition(
            condition_name="common-cold",
            confidence=0.35,
            confidence_level=ConfidenceLevel.LOW,
            matching_symptoms=["cough"],
            reasoning="Minimal symptom match",
            metta_query_used="test_query"
        )

        assert low_conf.confidence < 0.5
        assert low_conf.confidence_level == ConfidenceLevel.LOW


@pytest.mark.integration
class TestErrorHandling:
    """Test error handling in agent communication"""

    def test_empty_symptom_list_handling(self):
        """Test handling empty symptom list"""
        symptoms = []
        age = 30
        text = "I don't feel well"

        # Should require clarification
        clarification = needs_clarification(symptoms, age, text)
        assert clarification is not None
        assert "didn't detect any specific symptoms" in clarification

    def test_missing_age_for_fever(self):
        """Test handling fever without age information"""
        symptoms = [
            Symptom(name="fever", raw_text="fever", severity=8, duration="2 days")
        ]
        age = None
        text = "I have a fever"

        # Should ask for age
        clarification = needs_clarification(symptoms, age, text)
        assert clarification is not None
        assert "age" in clarification.lower()

    def test_invalid_metta_query_handling(self):
        """Test MeTTa query engine handles invalid input gracefully"""
        engine = MeTTaQueryEngine()

        # Empty symptom
        results = engine.find_by_symptom("")
        assert isinstance(results, list)

        # None symptom
        results = engine.find_by_symptom(None)
        assert isinstance(results, list)

        # Invalid condition
        urgency = engine.find_urgency_level("nonexistent-condition")
        assert urgency == "unknown"

    def test_diagnostic_response_with_no_conditions(self):
        """Test diagnostic response when no conditions are found"""
        # Empty conditions list
        response = DiagnosticResponse(
            session_id="test-empty-response",
            possible_conditions=[],
            urgency_level=UrgencyLevel.ROUTINE,
            red_flags=[],
            reasoning_chain=["No matching conditions found in knowledge base"],
            responding_agent="knowledge_graph"
        )

        assert len(response.possible_conditions) == 0
        assert response.urgency_level == UrgencyLevel.ROUTINE
        assert len(response.reasoning_chain) > 0


@pytest.mark.integration
class TestMedicalScenarios:
    """Test complete medical scenarios end-to-end"""

    def test_emergency_meningitis_scenario(self):
        """Test emergency meningitis scenario detection"""
        # User describes meningitis symptoms
        text = "I have a severe headache, high fever, stiff neck, and feel confused. I'm 28 years old."

        # Extract symptoms
        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "fever" in symptom_names
        assert any("headache" in s for s in symptom_names)
        assert any("neck" in s or "stiff" in s for s in symptom_names)
        assert "confusion" in symptom_names
        assert age == 28

        # Query MeTTa
        engine = MeTTaQueryEngine()
        symptom_names_normalized = [s.replace('_', '-') for s in symptom_names]
        conditions = engine.find_conditions_by_symptoms(symptom_names_normalized)

        # Should identify meningitis
        assert "meningitis" in [str(c) for c in conditions.keys()]

        # Check urgency
        urgency = engine.find_urgency_level("meningitis")
        assert urgency == "emergency"

        # Check severity
        severity = engine.find_severity_level("meningitis")
        assert severity == "critical"

        # Check red flags
        red_flags = engine.find_red_flag_symptoms()
        assert len(red_flags) > 0

    def test_routine_cold_scenario(self):
        """Test routine common cold scenario"""
        text = "I have a runny nose and mild cough. I'm 25 years old."

        # Extract symptoms
        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "cough" in symptom_names
        assert age == 25

        # Query MeTTa
        engine = MeTTaQueryEngine()
        symptom_names_normalized = [s.replace('_', '-') for s in symptom_names]
        conditions = engine.find_conditions_by_symptoms(symptom_names_normalized)

        # Should find some condition
        assert len(conditions) > 0

        # Common cold should be routine
        if "common-cold" in [str(c) for c in conditions.keys()]:
            urgency = engine.find_urgency_level("common-cold")
            assert "routine" in urgency.lower()

    def test_urgent_pneumonia_scenario(self):
        """Test urgent pneumonia scenario"""
        text = "I've had a bad cough for 5 days, fever around 102°F, and difficulty breathing. I'm 50 years old."

        # Extract symptoms
        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "cough" in symptom_names
        assert "fever" in symptom_names
        assert "difficulty-breathing" in symptom_names or "shortness-of-breath" in symptom_names
        assert age == 50

        # Query MeTTa
        engine = MeTTaQueryEngine()
        symptom_names_normalized = [s.replace('_', '-') for s in symptom_names]
        conditions = engine.find_conditions_by_symptoms(symptom_names_normalized)

        # Should find conditions with respiratory symptoms
        assert len(conditions) > 0

        # Pneumonia should be urgent
        if "pneumonia" in [str(c) for c in conditions.keys()]:
            urgency = engine.find_urgency_level("pneumonia")
            assert "urgent" in urgency.lower()
