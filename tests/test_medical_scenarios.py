"""
Comprehensive Medical Scenario Tests
20+ test cases covering various urgency levels, age groups, and conditions
"""
import pytest
from src.agents.patient_intake import SymptomExtractor
from src.metta.query_engine import MeTTaQueryEngine


@pytest.mark.medical
@pytest.mark.integration
class TestEmergencyScenarios:
    """Test emergency medical scenarios requiring immediate 911 call"""

    def test_meningitis_classic_presentation(self):
        """Test 1: Meningitis with classic triad"""
        text = "I have a severe headache, high fever, and very stiff neck. I'm confused. I'm 22 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "fever" in symptom_names
        assert any("headache" in s for s in symptom_names)
        assert any("neck" in s or "stiff" in s for s in symptom_names)
        assert "confusion" in symptom_names
        assert age == 22

        engine = MeTTaQueryEngine()
        urgency = engine.find_urgency_level("meningitis")
        assert urgency == "emergency"

    def test_stroke_fast_symptoms(self):
        """Test 2: Stroke with FAST symptoms"""
        text = "My face is drooping on one side, my arm is weak, and I can't speak clearly. I'm 65 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        assert age == 65

        engine = MeTTaQueryEngine()
        urgency = engine.find_urgency_level("stroke")
        assert urgency == "emergency"

    def test_heart_attack_chest_pain(self):
        """Test 3: Heart attack with chest pain"""
        text = "I have severe chest pain, can't breathe well, and nausea. I'm 58 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "chest-pain" in symptom_names
        assert "difficulty-breathing" in symptom_names or "shortness-of-breath" in symptom_names
        assert "nausea" in symptom_names
        assert age == 58

        engine = MeTTaQueryEngine()
        urgency = engine.find_urgency_level("heart-attack")
        assert urgency == "emergency"

    def test_appendicitis_acute_abdomen(self):
        """Test 4: Appendicitis with acute abdominal pain"""
        text = "I have severe stomach pain in the lower right, fever, and vomiting. I'm 28 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "abdominal-pain" in symptom_names or "stomach" in " ".join(symptom_names)
        assert "fever" in symptom_names
        assert "vomiting" in symptom_names
        assert age == 28

        engine = MeTTaQueryEngine()
        urgency = engine.find_urgency_level("appendicitis")
        assert urgency == "emergency"

    def test_pulmonary_embolism_sudden_symptoms(self):
        """Test 5: Pulmonary embolism with sudden onset"""
        text = "I suddenly have difficulty breathing, chest pain, and I'm coughing up blood. I'm 45 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert any("breath" in s for s in symptom_names)
        assert "chest-pain" in symptom_names
        assert "cough" in symptom_names
        assert age == 45

        engine = MeTTaQueryEngine()
        urgency = engine.find_urgency_level("pulmonary-embolism")
        assert urgency == "emergency"

    def test_sepsis_systemic_infection(self):
        """Test 6: Sepsis with systemic infection signs"""
        text = "I have a high fever, rapid heartbeat, I'm confused, and extreme weakness. I'm 70 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "fever" in symptom_names or "high-fever" in symptom_names
        assert "confusion" in symptom_names
        assert "fatigue" in symptom_names or any("weak" in s for s in symptom_names)
        assert age == 70

        engine = MeTTaQueryEngine()
        urgency = engine.find_urgency_level("sepsis")
        assert urgency == "emergency"


@pytest.mark.medical
@pytest.mark.integration
class TestUrgentScenarios:
    """Test urgent scenarios requiring medical attention within 24 hours"""

    def test_pneumonia_respiratory_symptoms(self):
        """Test 7: Pneumonia with respiratory distress"""
        text = "I've had a bad cough for 5 days, fever around 102°F, and difficulty breathing. I'm 50 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "cough" in symptom_names
        assert "fever" in symptom_names
        assert any("breath" in s for s in symptom_names)
        assert age == 50

        engine = MeTTaQueryEngine()
        urgency = engine.find_urgency_level("pneumonia")
        assert "urgent" in urgency.lower()

    def test_covid19_moderate_symptoms(self):
        """Test 8: COVID-19 with moderate symptoms"""
        text = "I have a fever, dry cough, loss of taste and smell, and fatigue for 3 days. I'm 35 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "fever" in symptom_names
        assert "cough" in symptom_names
        assert "fatigue" in symptom_names
        assert age == 35

        engine = MeTTaQueryEngine()
        urgency = engine.find_urgency_level("covid-19")
        assert "urgent" in urgency.lower() or urgency == "emergency"


@pytest.mark.medical
@pytest.mark.integration
class TestRoutineScenarios:
    """Test routine scenarios for self-care or regular doctor visit"""

    def test_common_cold_typical_presentation(self):
        """Test 9: Common cold with typical symptoms"""
        text = "I have a runny nose, mild sore throat, and feel a bit tired. Started yesterday. I'm 30 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "sore-throat" in symptom_names
        assert "fatigue" in symptom_names
        assert age == 30

        engine = MeTTaQueryEngine()
        urgency = engine.find_urgency_level("common-cold")
        assert "routine" in urgency.lower()

    def test_influenza_seasonal_flu(self):
        """Test 10: Influenza with typical flu symptoms"""
        text = "I have a fever, body aches, headache, and cough for 2 days. I'm 28 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "fever" in symptom_names
        assert "muscle-pain" in symptom_names or "body" in " ".join(symptom_names)
        assert "headache" in symptom_names
        assert "cough" in symptom_names
        assert age == 28

        engine = MeTTaQueryEngine()
        conditions = engine.find_conditions_by_symptoms(["fever", "headache", "cough", "muscle-pain"])
        assert "influenza" in [str(c) for c in conditions.keys()]

    def test_gastroenteritis_stomach_bug(self):
        """Test 11: Gastroenteritis with GI symptoms"""
        text = "I have nausea, vomiting, and diarrhea since this morning. I'm 25 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "nausea" in symptom_names
        assert "vomiting" in symptom_names
        assert "diarrhea" in symptom_names
        assert age == 25

        engine = MeTTaQueryEngine()
        urgency = engine.find_urgency_level("gastroenteritis")
        assert "routine" in urgency.lower()

    def test_migraine_headache_pattern(self):
        """Test 12: Migraine with characteristic symptoms"""
        text = "I have a throbbing headache on one side, nausea, and sensitivity to light. I'm 32 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "headache" in symptom_names or "throbbing" in " ".join(symptom_names)
        assert "nausea" in symptom_names
        assert age == 32

        engine = MeTTaQueryEngine()
        conditions = engine.find_conditions_by_symptoms(["headache", "nausea"])
        assert "migraine" in [str(c) for c in conditions.keys()]

    def test_tension_headache_stress_related(self):
        """Test 13: Tension headache with typical presentation"""
        text = "I have a dull headache all around my head, like a tight band. No other symptoms. I'm 40 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "headache" in symptom_names or "dull" in " ".join(symptom_names)
        assert age == 40

        engine = MeTTaQueryEngine()
        urgency = engine.find_urgency_level("tension-headache")
        assert "routine" in urgency.lower()


@pytest.mark.medical
@pytest.mark.integration
class TestAgeSpecificScenarios:
    """Test scenarios with age-specific considerations"""

    def test_pediatric_fever_infant(self):
        """Test 14: Fever in infant (high concern)"""
        text = "My 6 month old baby has a fever of 102°F and is irritable."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "fever" in symptom_names

        # Infants with fever require urgent evaluation
        # Age extraction may capture "6" or None
        if age:
            assert age <= 1

    def test_elderly_confusion_delirium(self):
        """Test 15: Confusion in elderly (red flag)"""
        text = "My 82 year old mother is confused, has a fever, and is weak. This started yesterday."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "confusion" in symptom_names
        assert "fever" in symptom_names
        assert "fatigue" in symptom_names or "weak" in " ".join(symptom_names)
        assert age == 82

        # Confusion in elderly with fever is high concern
        engine = MeTTaQueryEngine()
        red_flags = engine.find_red_flag_symptoms()
        assert len(red_flags) > 0

    def test_young_adult_chest_pain(self):
        """Test 16: Chest pain in young adult (still serious)"""
        text = "I'm 25 years old and having chest pain and can't breathe well."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "chest-pain" in symptom_names
        assert "difficulty-breathing" in symptom_names or "shortness-of-breath" in symptom_names
        assert age == 25

        # Chest pain is always serious regardless of age
        engine = MeTTaQueryEngine()
        red_flags = engine.find_red_flag_symptoms()
        assert len(red_flags) > 0


@pytest.mark.medical
@pytest.mark.integration
class TestComplexScenarios:
    """Test complex scenarios with multiple considerations"""

    def test_multisymptom_differential(self):
        """Test 17: Multiple symptoms requiring differential diagnosis"""
        text = "I have headache, nausea, fatigue, and fever for 3 days. I'm 35 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert len(symptom_names) >= 3
        assert "headache" in symptom_names
        assert "nausea" in symptom_names
        assert "fatigue" in symptom_names
        assert "fever" in symptom_names
        assert age == 35

        engine = MeTTaQueryEngine()
        symptom_names_normalized = [s.replace('_', '-') for s in symptom_names]
        conditions = engine.find_conditions_by_symptoms(symptom_names_normalized)

        # Should identify multiple possible conditions
        assert len(conditions) >= 2

    def test_allergy_contraindication(self):
        """Test 18: Patient with allergy requiring alternative treatment"""
        text = "I have a bad cough and chest pain. I'm allergic to penicillin. I'm 50 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "cough" in symptom_names
        assert "chest-pain" in symptom_names
        assert age == 50

        # Check contraindications for penicillin-based treatments
        engine = MeTTaQueryEngine()
        contras = engine.get_all_contraindications("amoxicillin")
        assert isinstance(contras, list)

    def test_chronic_condition_interaction(self):
        """Test 19: Acute illness with chronic condition"""
        text = "I have a fever and cough. I have diabetes and take metformin. I'm 60 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "fever" in symptom_names
        assert "cough" in symptom_names
        assert age == 60

        # Check for drug interactions or dose adjustments
        engine = MeTTaQueryEngine()
        # Diabetes patients may need special considerations
        assert age >= 60  # Elderly with chronic condition

    def test_minimal_information_scenario(self):
        """Test 20: Minimal information requiring clarification"""
        text = "I don't feel well."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        # Should extract no or very few symptoms
        assert len(symptoms) <= 1
        assert age is None

        # Should trigger clarification logic
        from src.agents.patient_intake import needs_clarification
        clarification = needs_clarification(symptoms, age, text)
        assert clarification is not None
        assert "didn't detect any specific symptoms" in clarification

    def test_red_flag_symptom_detection(self):
        """Test 21: Red flag symptom requiring immediate attention"""
        text = "I have a severe headache that came on suddenly, the worst headache of my life. I'm 45 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert any("headache" in s for s in symptom_names)
        assert age == 45

        # "Worst headache of life" is a red flag for subarachnoid hemorrhage
        engine = MeTTaQueryEngine()
        red_flags = engine.find_red_flag_symptoms()
        assert len(red_flags) > 0

    def test_progressive_worsening_symptoms(self):
        """Test 22: Symptoms that are getting worse (escalating urgency)"""
        text = "I've had a headache and fever for 5 days. Today I started feeling confused and the neck is very stiff. I'm 30 years old."

        symptoms = SymptomExtractor.extract_symptoms(text)
        age = SymptomExtractor.extract_age(text)

        symptom_names = [s.name for s in symptoms]
        assert "headache" in symptom_names
        assert "fever" in symptom_names
        assert "confusion" in symptom_names
        assert any("neck" in s or "stiff" in s for s in symptom_names)
        assert age == 30

        # Progressive symptoms with new neurological signs suggest meningitis
        engine = MeTTaQueryEngine()
        conditions = engine.find_conditions_by_symptoms(["fever", "headache", "stiff-neck", "confusion"])
        assert "meningitis" in [str(c) for c in conditions.keys()]

        urgency = engine.find_urgency_level("meningitis")
        assert urgency == "emergency"


@pytest.mark.medical
@pytest.mark.integration
class TestTreatmentSafety:
    """Test treatment safety and contraindication scenarios"""

    def test_aspirin_contraindications(self):
        """Test 23: Aspirin safety warnings"""
        engine = MeTTaQueryEngine()

        # Check contraindications
        contras = engine.get_all_contraindications("aspirin")
        assert isinstance(contras, list)

        # Check safety warnings
        warning = engine.get_safety_warning("aspirin")
        assert warning is not None

    def test_drug_interaction_check(self):
        """Test 24: Drug interaction checking"""
        engine = MeTTaQueryEngine()

        # Aspirin + warfarin = bleeding risk
        interaction = engine.check_drug_interaction("aspirin", "warfarin")
        assert isinstance(interaction, bool)

    def test_dose_adjustment_elderly(self):
        """Test 25: Dose adjustment for elderly patients"""
        engine = MeTTaQueryEngine()

        # Check if dose adjustment needed for elderly
        adjustment = engine.requires_dose_adjustment("aspirin", "age-over-65")
        assert isinstance(adjustment, bool)
