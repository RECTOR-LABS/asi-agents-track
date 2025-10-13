"""
Epic 7 Phase 1 Tests - Knowledge Base Enrichment
Tests for 12 new conditions, lab tests, and imaging requirements
"""

import pytest
from src.metta.query_engine import MeTTaQueryEngine


class TestEpic7NewConditions:
    """Test all 12 new conditions are properly defined."""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_critical_conditions_added(self, engine):
        """Test 3 new critical conditions: DKA, Anaphylaxis, Heat Stroke."""
        # DKA
        dka_symptoms = engine.find_symptoms_by_condition("diabetic-ketoacidosis")
        assert len(dka_symptoms) >= 8, "DKA should have at least 8 symptoms"
        assert any("fruity-breath-odor" in str(s) for s in dka_symptoms), "DKA missing fruity breath odor"

        dka_urgency = engine.find_urgency_level("diabetic-ketoacidosis")
        assert dka_urgency == "emergency", "DKA should be emergency"

        # Anaphylaxis
        ana_symptoms = engine.find_symptoms_by_condition("anaphylaxis")
        assert len(ana_symptoms) >= 10, "Anaphylaxis should have at least 10 symptoms"
        assert any("throat-swelling" in str(s) for s in ana_symptoms), "Anaphylaxis missing throat swelling"

        ana_treatments = engine.find_treatment("anaphylaxis")
        assert any("epinephrine" in str(t) for t in ana_treatments), "Anaphylaxis should have epinephrine"

        # Heat Stroke
        heat_symptoms = engine.find_symptoms_by_condition("heat-stroke")
        assert len(heat_symptoms) >= 10, "Heat stroke should have at least 10 symptoms"
        assert any("hot-dry-skin" in str(s) for s in heat_symptoms), "Heat stroke missing hot dry skin"

    def test_urgent_conditions_added(self, engine):
        """Test 5 new urgent conditions."""
        urgent_conditions = [
            "hypoglycemia",
            "asthma-exacerbation",
            "deep-vein-thrombosis",
            "kidney-stones",
            "concussion"
        ]

        for condition in urgent_conditions:
            symptoms = engine.find_symptoms_by_condition(condition)
            assert len(symptoms) >= 6, f"{condition} should have at least 6 symptoms"

            urgency = engine.find_urgency_level(condition)
            assert urgency == "urgent-24h", f"{condition} should be urgent-24h"

    def test_routine_conditions_added(self, engine):
        """Test 4 new routine conditions."""
        routine_conditions = [
            "urinary-tract-infection",
            "dehydration",
            "food-poisoning",
            "cellulitis"
        ]

        for condition in routine_conditions:
            symptoms = engine.find_symptoms_by_condition(condition)
            assert len(symptoms) >= 5, f"{condition} should have at least 5 symptoms"

            urgency = engine.find_urgency_level(condition)
            assert urgency == "routine-care", f"{condition} should be routine-care"


class TestLabTestQueries:
    """Test lab test query methods (Epic 7 Phase 1)."""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_find_lab_tests_dka(self, engine):
        """Test finding lab tests for DKA."""
        tests = engine.find_lab_tests("diabetic-ketoacidosis")
        assert len(tests) >= 4, "DKA should have at least 4 lab tests"

        tests_str = str(tests).lower()
        assert "blood-glucose" in tests_str or "glucose" in tests_str, "DKA missing blood glucose test"
        assert "blood-ketones" in tests_str or "ketones" in tests_str, "DKA missing blood ketones"
        assert "arterial-blood-gas" in tests_str or "abg" in tests_str, "DKA missing ABG"

    def test_find_lab_tests_asthma(self, engine):
        """Test finding lab tests for asthma exacerbation."""
        tests = engine.find_lab_tests("asthma-exacerbation")
        assert len(tests) >= 2, "Asthma should have at least 2 lab tests"
        assert any("pulse-oximetry" in str(t) for t in tests), "Asthma missing pulse oximetry"

    def test_find_lab_tests_uti(self, engine):
        """Test finding lab tests for UTI."""
        tests = engine.find_lab_tests("urinary-tract-infection")
        assert len(tests) >= 2, "UTI should have at least 2 lab tests"
        assert any("urinalysis" in str(t) for t in tests), "UTI missing urinalysis"
        assert any("urine-culture" in str(t) for t in tests), "UTI missing urine culture"

    def test_get_all_lab_tests(self, engine):
        """Test getting all lab tests from KB."""
        all_tests = engine.get_all_lab_tests()
        assert len(all_tests) >= 15, "Should have at least 15 unique lab tests"

        # Check for specific critical tests (flexible matching)
        tests_str = str(all_tests).lower()
        assert "blood-glucose" in tests_str or "glucose" in tests_str, "Missing blood glucose in all tests"
        assert "complete-blood-count" in tests_str or "cbc" in tests_str, "Missing CBC in all tests"
        assert "urinalysis" in tests_str, "Missing urinalysis in all tests"


class TestImagingQueries:
    """Test imaging query methods (Epic 7 Phase 1)."""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_find_imaging_asthma(self, engine):
        """Test finding imaging for asthma."""
        imaging = engine.find_imaging_requirements("asthma-exacerbation")
        assert len(imaging) >= 1, "Asthma should have imaging requirements"
        assert any("chest-x-ray" in str(i) for i in imaging), "Asthma missing chest X-ray"

    def test_find_imaging_dvt(self, engine):
        """Test finding imaging for DVT."""
        imaging = engine.find_imaging_requirements("deep-vein-thrombosis")
        assert len(imaging) >= 1, "DVT should have imaging requirements"
        assert any("ultrasound-doppler" in str(i) for i in imaging), "DVT missing ultrasound"

    def test_find_imaging_kidney_stones(self, engine):
        """Test finding imaging for kidney stones."""
        imaging = engine.find_imaging_requirements("kidney-stones")
        assert len(imaging) >= 2, "Kidney stones should have multiple imaging options"

        imaging_str = str(imaging).lower()
        assert "ct-scan" in imaging_str or "ct" in imaging_str, "Kidney stones missing CT scan"

    def test_find_imaging_concussion(self, engine):
        """Test finding imaging for concussion."""
        imaging = engine.find_imaging_requirements("concussion")
        assert len(imaging) >= 1, "Concussion should have imaging requirements"

        imaging_str = str(imaging).lower()
        # Flexible matching for CT scan of head (ct-scan-head, head-ct, ct-head, etc.)
        assert ("ct" in imaging_str and "head" in imaging_str) or "ct-scan-head" in imaging_str, \
               "Concussion missing head CT scan"

    def test_get_all_imaging(self, engine):
        """Test getting all imaging types from KB."""
        all_imaging = engine.get_all_imaging()
        assert len(all_imaging) >= 6, "Should have at least 6 unique imaging types"

        # Check for specific critical imaging (flexible matching)
        imaging_str = str(all_imaging).lower()
        has_ct = "ct-scan" in imaging_str or "ct" in imaging_str
        has_ultrasound = "ultrasound" in imaging_str
        assert has_ct or has_ultrasound, "Missing critical imaging types (CT or ultrasound)"


class TestContraindications:
    """Test contraindications for Epic 7 medications."""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_dka_contraindications(self, engine):
        """Test DKA treatment contraindications."""
        iv_insulin_contras = engine.get_all_contraindications("IV-insulin")
        assert len(iv_insulin_contras) >= 2, "IV insulin should have contraindications"
        assert any("hypoglycemia" in str(c) for c in iv_insulin_contras), "IV insulin missing hypoglycemia contraindication"

    def test_anaphylaxis_contraindications(self, engine):
        """Test epinephrine contraindications."""
        epi_contras = engine.get_all_contraindications("epinephrine-auto-injector")
        assert len(epi_contras) >= 2, "Epinephrine should have contraindications"

    def test_asthma_contraindications(self, engine):
        """Test bronchodilator contraindications."""
        bronch_contras = engine.get_all_contraindications("short-acting-bronchodilator")
        assert len(bronch_contras) >= 2, "Bronchodilators should have contraindications"

    def test_total_contraindications_count(self, engine):
        """Test total contraindications exceed 80 target."""
        # Query all contraindications
        query = "!(match &self (contraindication $treatment $condition) ($treatment $condition))"
        results = engine.query(query)

        # Handle nested list structure - count tuples inside
        total_count = 0
        if results and len(results) > 0:
            if isinstance(results[0], list):
                total_count = len(results[0])  # Count tuples in nested list
            else:
                total_count = len(results)

        assert total_count >= 80, f"Should have at least 80 contraindications, found {total_count}"


class TestMedicalScenarios:
    """Test real-world medical scenarios for Epic 7 conditions."""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_scenario_dka_emergency(self, engine):
        """Scenario: Patient with DKA symptoms."""
        symptoms = ["excessive-thirst", "fruity-breath-odor", "confusion", "rapid-breathing"]

        # Find matching conditions
        matches = engine.find_conditions_by_symptoms(symptoms)
        assert "diabetic-ketoacidosis" in matches, "DKA should match these symptoms"

        # Verify urgency
        urgency = engine.find_urgency_level("diabetic-ketoacidosis")
        assert urgency == "emergency", "DKA should be emergency"

        # Verify treatments
        treatments = engine.find_treatment("diabetic-ketoacidosis")
        assert any("immediate-911" in str(t) for t in treatments), "DKA treatment should include 911"

    def test_scenario_anaphylaxis_epipen(self, engine):
        """Scenario: Patient with anaphylaxis needs EpiPen."""
        symptoms = ["throat-swelling", "difficulty-breathing", "hives"]

        matches = engine.find_conditions_by_symptoms(symptoms)
        assert "anaphylaxis" in matches, "Anaphylaxis should match these symptoms"

        treatments = engine.find_treatment("anaphylaxis")
        assert any("epinephrine" in str(t) for t in treatments), "Should recommend EpiPen"

        # Check time sensitivity (if defined in KB)
        time_hours = engine.check_time_sensitivity("anaphylaxis")
        if time_hours is not None:
            assert time_hours == 0, "Anaphylaxis should be immediate (0 hours)"

    def test_scenario_uti_antibiotics(self, engine):
        """Scenario: Patient with UTI symptoms."""
        symptoms = ["painful-urination", "frequent-urination", "cloudy-urine"]

        matches = engine.find_conditions_by_symptoms(symptoms)
        assert "urinary-tract-infection" in matches, "UTI should match these symptoms"

        # Verify lab tests
        tests = engine.find_lab_tests("urinary-tract-infection")
        assert any("urinalysis" in str(t) for t in tests), "UTI should require urinalysis"

        treatments = engine.find_treatment("urinary-tract-infection")
        assert any("antibiotics" in str(t) for t in treatments), "UTI should include antibiotics"

    def test_scenario_kidney_stones_imaging(self, engine):
        """Scenario: Patient with kidney stone needs imaging."""
        symptoms = ["severe-flank-pain", "hematuria", "nausea"]

        matches = engine.find_conditions_by_symptoms(symptoms)
        assert "kidney-stones" in matches, "Kidney stones should match"

        # Verify imaging requirements
        imaging = engine.find_imaging_requirements("kidney-stones")
        assert len(imaging) >= 2, "Kidney stones should have imaging options"
        assert any("ct-scan" in str(i) for i in imaging), "Should include CT scan"

    def test_scenario_concussion_monitoring(self, engine):
        """Scenario: Patient with concussion needs monitoring."""
        symptoms = ["headache", "confusion", "dizziness", "vomiting"]

        matches = engine.find_conditions_by_symptoms(symptoms)
        assert "concussion" in matches, "Concussion should match"

        treatments = engine.find_treatment("concussion")
        treatments_str = str(treatments).lower()
        assert "physical-rest" in treatments_str or "rest" in treatments_str, "Should recommend rest"

        # Check time sensitivity for monitoring (if defined in KB)
        time_hours = engine.check_time_sensitivity("concussion")
        if time_hours is not None:
            assert time_hours == 48, "Concussion should be monitored for 48 hours"


class TestRedFlagSymptoms:
    """Test new red flag symptoms from Epic 7."""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_dka_red_flags(self, engine):
        """Test DKA red flag symptoms."""
        red_flags = engine.find_red_flag_symptoms()
        red_flags_str = str(red_flags).lower()
        assert "fruity-breath-odor" in red_flags_str or "fruity breath" in red_flags_str, \
               "Fruity breath odor should be red flag"

    def test_anaphylaxis_red_flags(self, engine):
        """Test anaphylaxis red flag symptoms."""
        red_flags = engine.find_red_flag_symptoms()
        red_flags_str = str(red_flags).lower()
        assert "throat-swelling" in red_flags_str or "throat swelling" in red_flags_str, \
               "Throat swelling should be red flag"

    def test_heat_stroke_red_flags(self, engine):
        """Test heat stroke red flag symptoms."""
        red_flags = engine.find_red_flag_symptoms()
        red_flags_str = str(red_flags).lower()
        assert "hot-dry-skin" in red_flags_str or "hot dry skin" in red_flags_str, \
               "Hot dry skin should be red flag"

    def test_asthma_red_flags(self, engine):
        """Test asthma red flag symptoms."""
        red_flags = engine.find_red_flag_symptoms()
        red_flags_str = str(red_flags).lower()
        assert "bluish-lips" in red_flags_str or "bluish lips" in red_flags_str or "cyanosis" in red_flags_str, \
               "Bluish lips should be red flag"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
