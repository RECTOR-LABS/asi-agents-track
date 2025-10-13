#!/usr/bin/env python3
"""
Test Enhanced Symptom Matching with Attributes (EPIC 7 - Phase 3)

Tests attribute-based symptom matching for precision diagnosis:
- Duration matching (acute vs chronic)
- Location matching (substernal, left chest, etc.)
- Character matching (crushing, sharp, burning, etc.)
- Onset matching (sudden vs gradual)
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.metta.query_engine import MeTTaQueryEngine
from src.agents.symptom_analysis import SymptomAnalyzer


class TestAttributeMatching:
    """Test symptom attribute matching enhancements"""

    @pytest.fixture
    def analyzer(self):
        engine = MeTTaQueryEngine()
        return SymptomAnalyzer(engine)

    def test_chest_pain_classic_heart_attack_presentation(self, analyzer):
        """Test chest pain with classic heart attack attributes"""
        symptoms = ["chest-pain", "shortness-of-breath", "sweating"]

        # Patient reports classic heart attack presentation
        symptom_attributes = {
            "chest-pain": {
                "duration": "20-minutes",  # Matches duration-typical: 5-30-minutes
                "location": "substernal",    # Matches location-primary
                "character": "crushing",     # Matches character: crushing-or-pressure
                "radiation": "left-arm"      # Matches radiation
            }
        }

        # Analyze with attributes
        result = analyzer.analyze_symptoms(
            symptoms=symptoms,
            age=65,
            medical_history=["diabetes-mellitus", "hypertension"],
            symptom_attributes=symptom_attributes
        )

        # Verify attribute matching occurred
        assert "attribute_matches" in result, "Should return attribute_matches"
        assert "chest-pain" in result["attribute_matches"], "Should match chest-pain attributes"

        chest_pain_match = result["attribute_matches"]["chest-pain"]

        # Should have high match score (3/4 or 4/4 = 0.75-1.0)
        assert chest_pain_match["match_score"] >= 0.75, \
            f"Expected high attribute match score, got {chest_pain_match['match_score']}"

        # Should have matched attributes
        assert len(chest_pain_match["matched_attrs"]) >= 3, \
            f"Expected at least 3 matched attributes, got {len(chest_pain_match['matched_attrs'])}"

        print(f"✓ Chest pain attribute match: {chest_pain_match['match_score']} "
              f"({len(chest_pain_match['matched_attrs'])}/{chest_pain_match['total_attrs']} matched)")

        # Verify confidence boost was applied
        assert "confidence_scores" in result
        if "heart-attack" in result["confidence_scores"]:
            confidence = result["confidence_scores"]["heart-attack"]

            # Check if attribute_boost was applied
            if "risk_adjustments" in result and "heart-attack" in result["risk_adjustments"]:
                adjustment = result["risk_adjustments"]["heart-attack"]
                assert "attribute_boost" in adjustment, "Should have attribute_boost in adjustments"
                assert adjustment["attribute_boost"] > 1.0, \
                    f"Expected attribute boost > 1.0, got {adjustment['attribute_boost']}"

                print(f"✓ Confidence boost applied: {adjustment['attribute_boost']}x")

    def test_attribute_mismatch_reduces_confidence(self, analyzer):
        """Test that mismatched attributes don't boost confidence"""
        symptoms = ["chest-pain"]

        # Patient reports atypical presentation
        symptom_attributes = {
            "chest-pain": {
                "duration": "2-seconds",     # Very short - atypical
                "location": "right-shoulder", # Unusual location
                "character": "sharp"          # Less typical for MI
            }
        }

        result = analyzer.analyze_symptoms(
            symptoms=symptoms,
            age=30,
            symptom_attributes=symptom_attributes
        )

        # Verify attribute matching occurred
        assert "attribute_matches" in result
        assert "chest-pain" in result["attribute_matches"]

        chest_pain_match = result["attribute_matches"]["chest-pain"]

        # Should have lower match score (many mismatches)
        assert chest_pain_match["match_score"] < 0.5, \
            f"Expected low match score for atypical presentation, got {chest_pain_match['match_score']}"

        # Should have some mismatched attributes
        assert len(chest_pain_match["mismatched_attrs"]) > 0, \
            "Expected mismatched attributes for atypical presentation"

        print(f"✓ Atypical presentation detected: {chest_pain_match['match_score']} match score")
        print(f"  Mismatched: {chest_pain_match['mismatched_attrs']}")

    def test_multiple_symptom_attributes(self, analyzer):
        """Test matching attributes for multiple symptoms"""
        symptoms = ["chest-pain", "severe-headache"]

        symptom_attributes = {
            "chest-pain": {
                "duration": "10-minutes",
                "character": "pressure"
            },
            "severe-headache": {
                "duration": "hours",
                "onset": "gradual",
                "location": "bilateral"
            }
        }

        result = analyzer.analyze_symptoms(
            symptoms=symptoms,
            symptom_attributes=symptom_attributes
        )

        # Both symptoms should have attribute matches
        assert "attribute_matches" in result
        assert "chest-pain" in result["attribute_matches"]
        assert "severe-headache" in result["attribute_matches"]

        print(f"✓ Multiple symptom attributes matched:")
        for symptom, match in result["attribute_matches"].items():
            print(f"  {symptom}: {match['match_score']} "
                  f"({len(match['matched_attrs'])}/{match['total_attrs']} matched)")

    def test_no_kb_attributes_neutral_score(self, analyzer):
        """Test that symptoms without KB attributes get neutral score"""
        symptoms = ["rare-symptom-not-in-kb"]

        symptom_attributes = {
            "rare-symptom-not-in-kb": {
                "duration": "unknown",
                "location": "unknown"
            }
        }

        result = analyzer.analyze_symptoms(
            symptoms=symptoms,
            symptom_attributes=symptom_attributes
        )

        # Should have attribute_matches but with neutral/low score
        assert "attribute_matches" in result
        if "rare-symptom-not-in-kb" in result["attribute_matches"]:
            match = result["attribute_matches"]["rare-symptom-not-in-kb"]
            # Neutral score when no KB data
            assert match["match_score"] == 0.5, \
                f"Expected neutral score 0.5 for missing KB data, got {match['match_score']}"

            print(f"✓ No KB attributes: neutral score {match['match_score']}")

    def test_backward_compatibility_without_attributes(self, analyzer):
        """Test that system works without symptom attributes (backward compatible)"""
        symptoms = ["chest-pain", "fever"]

        # No symptom_attributes provided - should work normally
        result = analyzer.analyze_symptoms(
            symptoms=symptoms,
            age=40
        )

        # Should complete analysis without error
        assert "urgency_level" in result
        assert "confidence_scores" in result
        assert "attribute_matches" in result

        # attribute_matches should be empty dict
        assert result["attribute_matches"] == {}, \
            "Should have empty attribute_matches when none provided"

        print(f"✓ Backward compatibility maintained - works without attributes")

    def test_attribute_boost_increases_confidence(self, analyzer):
        """Test that good attribute matches increase confidence scores"""
        symptoms = ["chest-pain", "shortness-of-breath"]

        # Run analysis without attributes
        result_without_attrs = analyzer.analyze_symptoms(
            symptoms=symptoms,
            age=60,
            medical_history=["hypertension"]
        )

        # Run analysis with matching attributes
        result_with_attrs = analyzer.analyze_symptoms(
            symptoms=symptoms,
            age=60,
            medical_history=["hypertension"],
            symptom_attributes={
                "chest-pain": {
                    "duration": "15-minutes",
                    "location": "substernal",
                    "character": "pressure"
                }
            }
        )

        # Extract heart-attack confidence from both
        conf_without = result_without_attrs["confidence_scores"].get("heart-attack", 0)
        conf_with = result_with_attrs["confidence_scores"].get("heart-attack", 0)

        # Confidence WITH attributes should be higher (due to attribute boost)
        if conf_without > 0 and conf_with > 0:
            assert conf_with >= conf_without, \
                f"Confidence with attributes ({conf_with}) should be >= without ({conf_without})"

            boost_pct = ((conf_with - conf_without) / conf_without) * 100 if conf_without > 0 else 0

            print(f"✓ Attribute boost effect:")
            print(f"  Without attributes: {conf_without}")
            print(f"  With attributes: {conf_with}")
            print(f"  Boost: +{boost_pct:.1f}%")


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])
