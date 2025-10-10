"""
Comprehensive Unit Tests for MeTTa Query Engine
Tests all 21 query methods with medical knowledge base
"""
import pytest
from src.metta.query_engine import MeTTaQueryEngine


@pytest.fixture
def query_engine():
    """Fixture to create a MeTTa query engine instance"""
    return MeTTaQueryEngine()


@pytest.mark.unit
@pytest.mark.metta
class TestMeTTaQueryEngineBasics:
    """Test basic query engine functionality"""

    def test_engine_initialization(self, query_engine):
        """Test that engine initializes successfully"""
        assert query_engine is not None
        assert query_engine.metta is not None

    def test_add_fact(self, query_engine):
        """Test adding a new fact to knowledge base"""
        result = query_engine.add_fact("(test-fact test-subject test-object)")
        assert result is True

    def test_query_basic(self, query_engine):
        """Test basic MeTTa query execution"""
        results = query_engine.query("!(match &self (has-symptom $condition fever) $condition)")
        assert results is not None
        assert len(results) > 0


@pytest.mark.unit
@pytest.mark.metta
class TestSymptomQueries:
    """Test symptom-related query methods"""

    def test_find_by_symptom_fever(self, query_engine):
        """Test finding conditions by fever symptom"""
        results = query_engine.find_by_symptom("fever")
        assert len(results) > 0
        assert any("flu" in str(c).lower() or "influenza" in str(c).lower() for c in results)

    def test_find_by_symptom_headache(self, query_engine):
        """Test finding conditions by headache symptom"""
        results = query_engine.find_by_symptom("headache")
        assert len(results) > 0
        # Plain 'headache' symptom exists in influenza and covid-19
        assert any("influenza" in str(c).lower() or "covid" in str(c).lower() for c in results)

    def test_find_by_symptom_nonexistent(self, query_engine):
        """Test finding conditions by non-existent symptom"""
        results = query_engine.find_by_symptom("nonexistent-symptom")
        assert isinstance(results, list)

    def test_find_symptoms_by_condition(self, query_engine):
        """Test finding symptoms for a specific condition"""
        symptoms = query_engine.find_symptoms_by_condition("meningitis")
        assert len(symptoms) > 0
        # Meningitis should have fever, headache, neck-stiffness
        symptoms_lower = [str(s).lower() for s in symptoms]
        assert any("fever" in s for s in symptoms_lower)
        assert any("headache" in s for s in symptoms_lower)

    def test_find_conditions_by_symptoms(self, query_engine):
        """Test multi-symptom matching with confidence scoring"""
        symptoms = ["fever", "headache", "neck-stiffness"]
        results = query_engine.find_conditions_by_symptoms(symptoms)
        assert isinstance(results, dict)
        assert len(results) > 0
        # Meningitis should have high confidence with these symptoms
        assert "meningitis" in [str(c).lower() for c in results.keys()]


@pytest.mark.unit
@pytest.mark.metta
class TestTreatmentQueries:
    """Test treatment-related query methods"""

    def test_find_treatment(self, query_engine):
        """Test finding treatments for a condition"""
        treatments = query_engine.find_treatment("influenza")
        assert len(treatments) > 0
        # Should include rest, fluids, etc.

    def test_get_treatment_recommendations(self, query_engine):
        """Test getting comprehensive treatment recommendations"""
        treatments = query_engine.get_treatment_recommendations("influenza")
        assert isinstance(treatments, list)
        assert len(treatments) > 0

    def test_get_evidence_source(self, query_engine):
        """Test getting evidence source for a treatment"""
        source = query_engine.get_evidence_source("rest")
        assert source is not None
        # Should return a source or "Unknown"


@pytest.mark.unit
@pytest.mark.metta
class TestUrgencyAndSeverity:
    """Test urgency and severity classification"""

    def test_find_emergency_conditions(self, query_engine):
        """Test finding emergency-level conditions"""
        emergency_conditions = query_engine.find_emergency_conditions()
        assert len(emergency_conditions) > 0
        # Should include meningitis, stroke, heart-attack
        emergency_lower = [str(c).lower() for c in emergency_conditions]
        assert "meningitis" in emergency_lower

    def test_find_urgency_level_emergency(self, query_engine):
        """Test urgency level for emergency condition"""
        urgency = query_engine.find_urgency_level("meningitis")
        assert urgency == "emergency"

    def test_find_urgency_level_urgent(self, query_engine):
        """Test urgency level for urgent condition"""
        urgency = query_engine.find_urgency_level("pneumonia")
        # Pneumonia is marked as urgent-24h in KB
        assert "urgent" in urgency.lower() or urgency == "emergency"

    def test_find_urgency_level_routine(self, query_engine):
        """Test urgency level for routine condition"""
        urgency = query_engine.find_urgency_level("common-cold")
        # Common cold is marked as routine-care in KB
        assert "routine" in urgency.lower()

    def test_find_severity_level(self, query_engine):
        """Test severity level classification"""
        severity = query_engine.find_severity_level("meningitis")
        assert severity in ["critical", "high", "severe"]


@pytest.mark.unit
@pytest.mark.metta
class TestRedFlagsAndSafety:
    """Test red flag detection and safety validation"""

    def test_find_red_flag_symptoms(self, query_engine):
        """Test finding red flag symptoms"""
        red_flags = query_engine.find_red_flag_symptoms()
        assert len(red_flags) > 0
        # Should include non-blanching-rash, chest-pain, etc.
        red_flags_lower = [str(rf).lower() for rf in red_flags]
        assert any("rash" in rf for rf in red_flags_lower)

    def test_get_required_action_emergency(self, query_engine):
        """Test required action for emergency condition"""
        action = query_engine.get_required_action("meningitis")
        assert action is not None
        assert "911" in action or "ER" in action or "emergency" in action.lower()

    def test_check_time_sensitivity(self, query_engine):
        """Test time sensitivity checking"""
        time_critical = query_engine.check_time_sensitivity("meningitis")
        assert time_critical is not None
        # Meningitis should be very time-sensitive (1-2 hours)


@pytest.mark.unit
@pytest.mark.metta
class TestContraindications:
    """Test contraindication and safety checking"""

    def test_get_all_contraindications(self, query_engine):
        """Test getting contraindications for a treatment"""
        contras = query_engine.get_all_contraindications("aspirin")
        assert isinstance(contras, list)
        # Aspirin should have contraindications (age, allergies, etc.)

    def test_get_safety_warning(self, query_engine):
        """Test getting safety warnings for treatments"""
        warning = query_engine.get_safety_warning("aspirin")
        assert warning is not None

    def test_check_drug_interaction(self, query_engine):
        """Test drug interaction checking"""
        interaction = query_engine.check_drug_interaction("aspirin", "warfarin")
        # Should return True if interaction exists
        assert isinstance(interaction, (bool, str))

    def test_requires_dose_adjustment(self, query_engine):
        """Test dose adjustment requirements"""
        needs_adjustment = query_engine.requires_dose_adjustment("aspirin", "age-over-65")
        assert isinstance(needs_adjustment, bool)


@pytest.mark.unit
@pytest.mark.metta
class TestDifferentialDiagnosis:
    """Test differential diagnosis functionality"""

    def test_find_differential_diagnoses(self, query_engine):
        """Test finding differential diagnoses"""
        differentials = query_engine.find_differential_diagnoses("meningitis")
        assert isinstance(differentials, list)
        # Should include similar conditions like encephalitis, migraine

    def test_generate_reasoning_chain(self, query_engine):
        """Test generating reasoning chains"""
        symptoms = ["fever", "headache", "neck-stiffness"]
        reasoning = query_engine.generate_reasoning_chain(symptoms, "meningitis")
        assert reasoning is not None
        assert len(reasoning) > 0
        # Should explain the diagnostic logic


@pytest.mark.unit
@pytest.mark.metta
class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_empty_symptom(self, query_engine):
        """Test handling empty symptom"""
        results = query_engine.find_by_symptom("")
        assert isinstance(results, list)

    def test_none_symptom(self, query_engine):
        """Test handling None symptom"""
        results = query_engine.find_by_symptom(None)
        assert isinstance(results, list)

    def test_empty_condition(self, query_engine):
        """Test handling empty condition"""
        treatments = query_engine.find_treatment("")
        assert isinstance(treatments, list)

    def test_invalid_condition(self, query_engine):
        """Test handling invalid condition"""
        urgency = query_engine.find_urgency_level("nonexistent-condition")
        # Should return "unknown" for non-existent conditions
        assert urgency == "unknown"

    def test_empty_symptoms_list(self, query_engine):
        """Test multi-symptom matching with empty list"""
        results = query_engine.find_conditions_by_symptoms([])
        assert isinstance(results, dict)
        assert len(results) == 0

    def test_get_all_facts(self, query_engine):
        """Test retrieving all facts for a predicate"""
        facts = query_engine.get_all_facts("has-symptom")
        assert isinstance(facts, list)
        assert len(facts) > 0
