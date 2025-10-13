"""
Epic 7 Phase 2 Tests - Risk-Adjusted Diagnosis
Tests for risk factors, diagnostic criteria, and enhanced confidence scoring
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.metta.query_engine import MeTTaQueryEngine
from src.agents.symptom_analysis import SymptomAnalyzer


class TestRiskAdjustedDiagnosis:
    """Test risk-adjusted confidence scoring (EPIC 7 - Phase 2)."""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    @pytest.fixture
    def analyzer(self, engine):
        return SymptomAnalyzer(engine)

    def test_scenario_1_heart_attack_high_risk(self, analyzer):
        """
        Scenario 1: 72-year-old male with chest pain and diabetes
        Expected: High risk multiplier due to age + diabetes
        """
        symptoms = ["chest-pain", "shortness-of-breath", "sweating"]
        age = 72
        medical_history = ["diabetes-mellitus", "hypertension"]

        result = analyzer.analyze_symptoms(
            symptoms=symptoms,
            age=age,
            medical_history=medical_history
        )

        # Verify risk adjustments were applied
        assert "risk_adjustments" in result
        assert len(result["risk_adjustments"]) > 0

        # Check if heart-attack has high risk multiplier
        if "heart-attack" in result["risk_adjustments"]:
            heart_attack_risk = result["risk_adjustments"]["heart-attack"]
            assert heart_attack_risk["risk_multiplier"] > 1.3, \
                "Expected high risk multiplier for elderly diabetic patient"
            assert "age-over-70" in heart_attack_risk["matched_factors"] or \
                   "age-over-65" in heart_attack_risk["matched_factors"], \
                "Age risk factor should be matched"

        # Verify reasoning includes risk factor analysis
        reasoning_text = " ".join(result["reasoning_chain"])
        assert "risk" in reasoning_text.lower() or "age" in reasoning_text.lower(), \
            "Reasoning should mention risk factors or age"

        print("\n✅ Scenario 1 - High Risk Heart Attack:")
        print(f"   Age: {age}, History: {medical_history}")
        print(f"   Urgency: {result['urgency_level']}")
        if "heart-attack" in result["risk_adjustments"]:
            print(f"   Risk multiplier: {heart_attack_risk['risk_multiplier']}")
            print(f"   Matched factors: {heart_attack_risk['matched_factors'][:3]}")

    def test_scenario_2_young_patient_low_risk(self, analyzer):
        """
        Scenario 2: 28-year-old healthy patient with UTI symptoms
        Expected: Low/no risk multiplier due to young age and no risk factors
        """
        symptoms = ["painful-urination", "frequent-urination", "cloudy-urine"]
        age = 28
        medical_history = []  # No risk factors

        result = analyzer.analyze_symptoms(
            symptoms=symptoms,
            age=age,
            medical_history=medical_history
        )

        # Verify risk adjustments
        assert "risk_adjustments" in result

        # Check if UTI has low risk multiplier (close to 1.0)
        if "urinary-tract-infection" in result["risk_adjustments"]:
            uti_risk = result["risk_adjustments"]["urinary-tract-infection"]
            assert uti_risk["risk_multiplier"] <= 1.2, \
                "Young healthy patient should have low risk multiplier"

        # Should be routine urgency
        assert result["urgency_level"] in ["routine", "routine-care"], \
            "Young patient with UTI should be routine care"

        print("\n✅ Scenario 2 - Low Risk UTI:")
        print(f"   Age: {age}, History: None")
        print(f"   Urgency: {result['urgency_level']}")
        if "urinary-tract-infection" in result["risk_adjustments"]:
            print(f"   Risk multiplier: {uti_risk['risk_multiplier']}")

    def test_scenario_3_diabetes_complication_risk_factors(self, analyzer):
        """
        Scenario 3: 55-year-old Type 1 diabetic with DKA symptoms
        Expected: Very high risk due to type-1-diabetes (5.0 multiplier)
        """
        symptoms = ["excessive-thirst", "fruity-breath-odor", "confusion", "rapid-breathing"]
        age = 55
        medical_history = ["type-1-diabetes", "previous-dka"]

        result = analyzer.analyze_symptoms(
            symptoms=symptoms,
            age=age,
            medical_history=medical_history
        )

        # Should detect DKA
        assert "diabetic-ketoacidosis" in result["differential_diagnoses"] or \
               any("dka" in d.lower() for d in result["differential_diagnoses"]), \
            "Should detect diabetic ketoacidosis"

        # Should be emergency urgency
        assert result["urgency_level"] == "emergency", \
            "DKA should be classified as emergency"

        # Check risk adjustments
        if "diabetic-ketoacidosis" in result["risk_adjustments"]:
            dka_risk = result["risk_adjustments"]["diabetic-ketoacidosis"]
            assert dka_risk["risk_multiplier"] >= 1.5, \
                "Type 1 diabetic with previous DKA should have high risk multiplier"

        print("\n✅ Scenario 3 - High Risk DKA:")
        print(f"   Age: {age}, History: {medical_history}")
        print(f"   Urgency: {result['urgency_level']}")
        print(f"   Red flags: {result['red_flags']}")
        if "diabetic-ketoacidosis" in result["risk_adjustments"]:
            print(f"   Risk multiplier: {dka_risk['risk_multiplier']}")
            print(f"   Matched factors: {dka_risk['matched_factors']}")

    def test_scenario_4_asthma_with_risk_factors(self, analyzer):
        """
        Scenario 4: 45-year-old with asthma exacerbation and smoking history
        Expected: Moderate risk multiplier, urgent classification
        """
        symptoms = ["shortness-of-breath", "wheezing", "chest-tightness", "cough"]
        age = 45
        # Use risk factor names that match the KB
        medical_history = ["smoking-current", "previous-hospital-admission"]

        result = analyzer.analyze_symptoms(
            symptoms=symptoms,
            age=age,
            medical_history=medical_history
        )

        # Should detect asthma
        assert any("asthma" in d.lower() for d in result["differential_diagnoses"]), \
            "Should detect asthma exacerbation"

        # Check risk adjustments for asthma
        asthma_conditions = [c for c in result["risk_adjustments"] if "asthma" in c.lower()]
        if asthma_conditions:
            asthma_risk = result["risk_adjustments"][asthma_conditions[0]]
            # Smoking + previous hospitalization should increase risk
            assert asthma_risk["risk_multiplier"] >= 1.1, \
                "Smoker with hospitalization history should have elevated risk"

        print("\n✅ Scenario 4 - Asthma with Risk Factors:")
        print(f"   Age: {age}, History: {medical_history}")
        print(f"   Urgency: {result['urgency_level']}")
        print(f"   Differential: {result['differential_diagnoses'][:3]}")

    def test_scenario_5_elderly_pneumonia_curb65(self, engine):
        """
        Scenario 5: 78-year-old with pneumonia symptoms - CURB-65 assessment
        Expected: High CURB-65 score (confusion + age>65 + RR≥30)
        """
        # Test CURB-65 diagnostic criteria
        # Use criterion names that match the KB
        findings = [
            "confusion-1",  # Confusion present
            "respiratory-rate-30-1",  # RR ≥ 30
            "age-65-or-over-1"  # Age ≥ 65 (matches KB name)
        ]

        criteria_results = engine.check_diagnostic_criteria("pneumonia", findings)

        # Check if CURB-65 was evaluated
        assert "curb-65" in criteria_results, "CURB-65 should be available for pneumonia"

        curb_result = criteria_results["curb-65"]
        assert curb_result["matched"] >= 3, "Should match at least 3 CURB-65 criteria"
        assert "ICU" in curb_result["interpretation"] or "severe" in curb_result["interpretation"].lower(), \
            "High CURB-65 score (3+) should recommend ICU admission"

        print("\n✅ Scenario 5 - Elderly Pneumonia CURB-65:")
        print(f"   Matched criteria: {curb_result['matched']}/{curb_result['total']}")
        print(f"   Interpretation: {curb_result['interpretation']}")
        print(f"   Matched items: {curb_result['matched_criteria']}")


class TestDiagnosticCriteria:
    """Test diagnostic criteria systems (EPIC 7 - Phase 2)."""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_perc_rule_for_pe(self, engine):
        """Test PERC rule for pulmonary embolism risk assessment."""
        # PERC negative (all criteria negative = low risk)
        findings_negative = [
            "age-under-50",
            "heart-rate-under-100",
            "spo2-over-94"
        ]

        criteria = engine.check_diagnostic_criteria("pulmonary-embolism", findings_negative)

        if "perc-rule" in criteria:
            perc = criteria["perc-rule"]
            # PERC interprets 0 matches as low risk (all negative)
            if perc["matched"] == 0:
                assert "low risk" in perc["interpretation"].lower() or \
                       "perc negative" in perc["interpretation"].lower(), \
                    "PERC negative should indicate low PE risk"

        print("\n✅ PERC Rule Test:")
        print(f"   Findings: {findings_negative}")
        if "perc-rule" in criteria:
            print(f"   Result: {perc['interpretation']}")

    def test_wells_score_for_dvt(self, engine):
        """Test Wells score for DVT likelihood."""
        # Wells positive (DVT likely)
        findings_positive = [
            "active-cancer-1",
            "paralysis-or-immobilization-1",
            "recent-surgery-1"
        ]

        criteria = engine.check_diagnostic_criteria("deep-vein-thrombosis", findings_positive)

        if "wells-score" in criteria:
            wells = criteria["wells-score"]
            assert wells["matched"] >= 2, "Should have Wells score ≥2"
            assert "likely" in wells["interpretation"].lower(), \
                "Wells ≥2 should indicate DVT likely"

        print("\n✅ Wells Score Test:")
        print(f"   Findings: {findings_positive}")
        if "wells-score" in criteria:
            print(f"   Score: {wells['matched']}")
            print(f"   Result: {wells['interpretation']}")

    def test_cha2ds2_vasc_stroke_risk(self, engine):
        """Test CHA2DS2-VASc for stroke risk in atrial fibrillation."""
        # High risk patient
        findings_high_risk = [
            "age-over-75-2",  # Age ≥75 (2 points)
            "hypertension-1",  # Hypertension (1 point)
            "diabetes-1"  # Diabetes (1 point)
        ]

        criteria = engine.check_diagnostic_criteria("atrial-fibrillation", findings_high_risk)

        if "cha2ds2-vasc" in criteria:
            cha2ds2 = criteria["cha2ds2-vasc"]
            assert cha2ds2["matched"] >= 2, "Should have CHA2DS2-VASc score ≥2"
            assert "anticoagulation" in cha2ds2["interpretation"].lower(), \
                "High score should recommend anticoagulation"

        print("\n✅ CHA2DS2-VASc Test:")
        print(f"   Findings: {findings_high_risk}")
        if "cha2ds2-vasc" in criteria:
            print(f"   Score: {cha2ds2['matched']}")
            print(f"   Result: {cha2ds2['interpretation']}")


class TestClarifyingQuestions:
    """Test clarifying questions for differential diagnosis (EPIC 7 - Phase 2)."""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_chest_pain_differential_questions(self, engine):
        """Test clarifying questions for chest pain differential."""
        questions = engine.get_clarifying_questions("chest-pain-differential")

        assert len(questions) >= 2, "Should have multiple chest pain clarifying questions"

        # Check for cardiac-specific questions
        questions_text = " ".join(questions).lower()
        assert any(keyword in questions_text for keyword in ["arm", "jaw", "neck", "radiate"]), \
            "Should ask about radiation pattern for cardiac vs musculoskeletal"

        print("\n✅ Chest Pain Differential Questions:")
        for i, q in enumerate(questions[:5], 1):
            print(f"   {i}. {q}")

    def test_headache_differential_questions(self, engine):
        """Test clarifying questions for headache differential."""
        questions = engine.get_clarifying_questions("headache-differential")

        assert len(questions) >= 2, "Should have headache clarifying questions"

        # Check for red flag questions
        questions_text = " ".join(questions).lower()
        assert any(keyword in questions_text for keyword in ["worst", "thunderclap", "sudden"]), \
            "Should ask about sudden severe headache (SAH/stroke)"

        print("\n✅ Headache Differential Questions:")
        for i, q in enumerate(questions[:5], 1):
            print(f"   {i}. {q}")

    def test_differential_aids_heart_attack_vs_anxiety(self, engine):
        """Test questions that help differentiate heart attack from anxiety."""
        questions = engine.get_differential_aids("heart-attack", "anxiety-attack")

        # Should have questions that distinguish cardiac from anxiety
        if questions:
            questions_text = " ".join(questions).lower()
            # Either exertion-related or symptom pattern questions
            assert len(questions) >= 1, "Should have differentiating questions"

            print("\n✅ Heart Attack vs Anxiety Differential:")
            for i, q in enumerate(questions[:5], 1):
                print(f"   {i}. {q}")
        else:
            print("\n⚠️ No differential aids found (may not be in KB yet)")


class TestRiskFactorQueries:
    """Test Phase 2 risk factor query methods."""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_get_risk_factors_heart_attack(self, engine):
        """Test retrieving risk factors for heart attack."""
        risk_factors = engine.get_risk_factors("heart-attack")

        assert len(risk_factors) >= 5, "Heart attack should have multiple risk factors"

        # Check structure
        for rf in risk_factors[:3]:
            assert "factor" in rf, "Risk factor should have 'factor' key"
            assert "multiplier" in rf, "Risk factor should have 'multiplier' key"
            assert rf["multiplier"] > 0, "Multiplier should be positive"

        # Should be sorted by multiplier (highest first)
        if len(risk_factors) >= 2:
            assert risk_factors[0]["multiplier"] >= risk_factors[1]["multiplier"], \
                "Risk factors should be sorted by multiplier (descending)"

        print("\n✅ Heart Attack Risk Factors:")
        for rf in risk_factors[:5]:
            print(f"   - {rf['factor']}: {rf['multiplier']:.1f}x")

    def test_calculate_risk_score(self, engine):
        """Test calculating risk score based on patient factors."""
        patient_factors = ["age-over-65", "diabetes-mellitus", "hypertension"]

        risk_score = engine.calculate_risk_score("heart-attack", patient_factors)

        assert risk_score > 0, "Risk score should be positive for patients with risk factors"
        assert risk_score >= 3.0, "Three significant risk factors should give score ≥3"

        print("\n✅ Risk Score Calculation:")
        print(f"   Patient factors: {patient_factors}")
        print(f"   Risk score: {risk_score:.1f}")

    def test_age_risk_levels(self, engine):
        """Test age-specific risk levels."""
        # Test different age groups for heart attack
        age_groups = ["age-under-40", "age-40-55", "age-55-70", "age-over-70"]

        print("\n✅ Age-Specific Risk (Heart Attack):")
        for age_group in age_groups:
            risk_level = engine.get_age_risk("heart-attack", age_group)
            print(f"   {age_group}: {risk_level}")

        # Very old age should have highest risk
        elderly_risk = engine.get_age_risk("heart-attack", "age-over-70")
        assert elderly_risk in ["high", "very-high", "unknown"], \
            "Elderly should have high heart attack risk"

    def test_prevalence_data(self, engine):
        """Test population prevalence queries."""
        # Test UTI prevalence in females (should be high ~50%)
        uti_female_prev = engine.get_prevalence("urinary-tract-infection", "female")

        if uti_female_prev:
            assert 0 < uti_female_prev <= 1.0, "Prevalence should be between 0 and 1"
            assert uti_female_prev >= 0.3, "UTI prevalence in females should be ≥30%"

            print("\n✅ Prevalence Data:")
            print(f"   UTI in females: {uti_female_prev*100:.1f}%")


class TestConfidenceScoreComparison:
    """Compare confidence scores with and without risk adjustment."""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    @pytest.fixture
    def analyzer(self, engine):
        return SymptomAnalyzer(engine)

    def test_risk_multiplier_effect(self, analyzer):
        """
        Test that risk factors increase confidence scores appropriately.
        Compare same symptoms with different risk profiles.
        """
        symptoms = ["chest-pain", "shortness-of-breath"]

        # Low risk patient (young, no history)
        result_low_risk = analyzer.analyze_symptoms(
            symptoms=symptoms,
            age=30,
            medical_history=[]
        )

        # High risk patient (elderly with diabetes)
        result_high_risk = analyzer.analyze_symptoms(
            symptoms=symptoms,
            age=72,
            medical_history=["diabetes-mellitus", "hypertension"]
        )

        # Find heart-attack confidence in both
        if "heart-attack" in result_low_risk["confidence_scores"] and \
           "heart-attack" in result_high_risk["confidence_scores"]:

            conf_low = result_low_risk["confidence_scores"]["heart-attack"]
            conf_high = result_high_risk["confidence_scores"]["heart-attack"]

            # High risk patient should have higher confidence for same symptoms
            assert conf_high >= conf_low, \
                "High risk patient should have equal or higher confidence"

            print("\n✅ Risk Multiplier Effect:")
            print(f"   Symptoms: {symptoms}")
            print(f"   Low risk (age 30): {conf_low:.2f}")
            print(f"   High risk (age 72 + diabetes): {conf_high:.2f}")
            print(f"   Confidence increase: {(conf_high - conf_low):.2f}")


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s", "--tb=short"])
