#!/usr/bin/env python3
"""
Epic 7 Phase 3 Test Suite - Treatment Protocols, Symptom Attributes, Epidemiology

Tests new features:
1. Treatment protocol sequencing (step-by-step protocols)
2. Symptom attribute filtering (duration, onset, location)
3. Seasonal prevalence adjustments
4. Geographic prevalence adjustments
5. Symptom timing patterns
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.metta.query_engine import MeTTaQueryEngine


class TestTreatmentProtocols:
    """Test treatment protocol sequencing and retrieval"""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_heart_attack_protocol_complete_sequence(self, engine):
        """Test heart attack protocol has all 8 steps in correct order"""
        protocol = engine.get_treatment_protocol("heart-attack")

        # Should have 8 steps total
        assert len(protocol) >= 8, f"Expected at least 8 protocol steps, got {len(protocol)}"

        # Verify steps are ordered correctly (step_number should be sequential)
        step_numbers = [step['step_number'] for step in protocol]
        assert step_numbers == sorted(step_numbers), "Protocol steps should be ordered by step_number"

        # Verify critical steps are present
        actions = [step['action'] for step in protocol]
        assert 'call-911' in actions, "Critical: call-911 should be in protocol"
        assert 'chew-aspirin-325mg' in actions, "Critical: aspirin should be in protocol"

        # Verify first step is immediate and critical
        first_step = protocol[0]
        assert first_step['timing'] == 'immediate', "First step should be immediate"
        assert first_step['priority'] == 'critical', "First step should be critical priority"

        print(f"✓ Heart attack protocol validated: {len(protocol)} steps")

    def test_sepsis_protocol_timing_accuracy(self, engine):
        """Test sepsis protocol has correct timing information"""
        protocol = engine.get_treatment_protocol("sepsis")

        # Should have multiple steps (sepsis has 8 steps)
        assert len(protocol) >= 7, f"Expected at least 7 protocol steps for sepsis"

        # Check that timing information is present
        for step in protocol:
            assert 'timing' in step, f"Step {step['step_number']} missing timing"
            assert 'priority' in step, f"Step {step['step_number']} missing priority"
            assert 'action' in step, f"Step {step['step_number']} missing action"

        # Verify priority levels are valid
        valid_priorities = ['critical', 'high', 'medium', 'low']
        priorities = [step['priority'] for step in protocol]
        for priority in priorities:
            assert priority in valid_priorities, f"Invalid priority: {priority}"

        print(f"✓ Sepsis protocol timing validated: {len(protocol)} steps")

    def test_protocol_priority_filtering(self, engine):
        """Test filtering protocol steps by priority level"""
        # Get all heart attack steps
        all_steps = engine.get_treatment_protocol("heart-attack")

        # Get only critical priority steps
        critical_steps = engine.get_protocol_steps("heart-attack", priority_filter="critical")

        # Critical steps should be subset of all steps
        assert len(critical_steps) <= len(all_steps), "Critical steps should be subset"
        assert len(critical_steps) >= 2, "Should have at least 2 critical steps"

        # All filtered steps should be critical
        for step in critical_steps:
            assert step['priority'] == 'critical', f"Filtered step should be critical: {step}"

        print(f"✓ Protocol filtering validated: {len(critical_steps)}/{len(all_steps)} critical steps")

    def test_multiple_condition_protocols(self, engine):
        """Test that protocols exist for multiple critical conditions"""
        critical_conditions = [
            "heart-attack",
            "stroke",
            "pulmonary-embolism",
            "meningitis",
            "pneumonia",
            "anaphylaxis",
            "heat-stroke",
            "sepsis"
        ]

        protocols_found = 0
        for condition in critical_conditions:
            protocol = engine.get_treatment_protocol(condition)
            if len(protocol) > 0:
                protocols_found += 1
                print(f"  ✓ {condition}: {len(protocol)} steps")

        # Should have protocols for at least 6 conditions
        assert protocols_found >= 6, \
            f"Expected protocols for at least 6 conditions, found {protocols_found}"

        print(f"✓ Multiple condition protocols validated: {protocols_found}/{len(critical_conditions)}")


class TestSymptomAttributes:
    """Test symptom attribute retrieval and filtering"""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_chest_pain_attributes_comprehensive(self, engine):
        """Test chest pain has comprehensive attributes for differential diagnosis"""
        attributes = engine.get_symptom_attributes("chest-pain")

        # Should have multiple attribute types
        assert len(attributes) > 0, "Chest pain should have attributes"

        # Check for key attribute categories
        expected_categories = ['duration', 'onset', 'location', 'character', 'radiation']
        found_categories = set()

        for attr_type, values in attributes.items():
            for category in expected_categories:
                if category in attr_type:
                    found_categories.add(category)

        # Should have at least 3 of these categories
        assert len(found_categories) >= 3, \
            f"Expected at least 3 attribute categories, found: {found_categories}"

        print(f"✓ Chest pain attributes validated: {len(attributes)} attributes, "
              f"{len(found_categories)} categories")

    def test_fever_attributes_for_pattern_recognition(self, engine):
        """Test fever attributes help identify patterns"""
        attributes = engine.get_symptom_attributes("fever")

        # Should have onset and duration information
        assert len(attributes) > 0, "Fever should have attributes"

        # Check that attributes are structured correctly
        for attr_type, values in attributes.items():
            assert isinstance(values, list), f"Attribute values should be list: {attr_type}"
            assert len(values) > 0, f"Attribute should have values: {attr_type}"

        print(f"✓ Fever attributes validated: {len(attributes)} attributes")

    def test_multiple_symptom_attributes(self, engine):
        """Test that multiple symptoms have attribute metadata"""
        symptoms = [
            "chest-pain",
            "fever",
            "headache",
            "shortness-of-breath",
            "abdominal-pain"
        ]

        symptoms_with_attributes = 0
        total_attributes = 0

        for symptom in symptoms:
            attributes = engine.get_symptom_attributes(symptom)
            if len(attributes) > 0:
                symptoms_with_attributes += 1
                total_attributes += len(attributes)
                print(f"  ✓ {symptom}: {len(attributes)} attributes")

        # Should have attributes for at least 4 symptoms
        assert symptoms_with_attributes >= 4, \
            f"Expected attributes for at least 4 symptoms, found {symptoms_with_attributes}"

        print(f"✓ Multiple symptom attributes validated: "
              f"{symptoms_with_attributes}/{len(symptoms)} symptoms, "
              f"{total_attributes} total attributes")


class TestSeasonalPrevalence:
    """Test seasonal prevalence adjustments for conditions"""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_influenza_winter_peak(self, engine):
        """Test influenza has high prevalence in winter months"""
        # Peak winter months
        winter_months = ["january", "february", "december"]

        winter_multipliers = []
        for month in winter_months:
            multiplier = engine.get_seasonal_prevalence("influenza", month)
            winter_multipliers.append(multiplier)
            print(f"  Influenza in {month}: {multiplier}x")

        # Winter should have elevated prevalence (> 1.0)
        max_winter = max(winter_multipliers)
        assert max_winter >= 3.0, \
            f"Expected winter peak >= 3.0x, got {max_winter}x"

        # Compare to summer month
        summer_multiplier = engine.get_seasonal_prevalence("influenza", "july")
        assert summer_multiplier < max_winter, \
            "Winter prevalence should be higher than summer"

        print(f"✓ Influenza seasonal pattern validated: winter peak {max_winter}x, "
              f"summer {summer_multiplier}x")

    def test_heat_stroke_summer_peak(self, engine):
        """Test heat stroke peaks in summer months"""
        # Peak summer months
        summer_months = ["june", "july", "august"]

        summer_multipliers = []
        for month in summer_months:
            multiplier = engine.get_seasonal_prevalence("heat-stroke", month)
            summer_multipliers.append(multiplier)
            print(f"  Heat stroke in {month}: {multiplier}x")

        # Summer should have very high prevalence
        max_summer = max(summer_multipliers)
        assert max_summer >= 4.0, \
            f"Expected summer peak >= 4.0x, got {max_summer}x"

        # Compare to winter month
        winter_multiplier = engine.get_seasonal_prevalence("heat-stroke", "january")
        assert winter_multiplier < max_summer, \
            "Summer prevalence should be much higher than winter"

        print(f"✓ Heat stroke seasonal pattern validated: summer peak {max_summer}x, "
              f"winter {winter_multiplier}x")

    def test_baseline_prevalence(self, engine):
        """Test that baseline prevalence is 1.0 when no data"""
        # Test a condition/month combination that should return baseline
        multiplier = engine.get_seasonal_prevalence("heart-attack", "march")

        # Heart attack should be relatively stable year-round (close to 1.0)
        assert 0.8 <= multiplier <= 1.5, \
            f"Expected baseline prevalence ~1.0, got {multiplier}"

        print(f"✓ Baseline prevalence validated: heart-attack in march = {multiplier}x")

    def test_multiple_conditions_seasonal_patterns(self, engine):
        """Test that multiple conditions have seasonal data"""
        test_cases = [
            ("influenza", "january", 3.0),    # Winter peak
            ("heat-stroke", "july", 4.0),     # Summer peak
            ("pneumonia", "december", 2.0),   # Winter increase
        ]

        patterns_validated = 0
        for condition, month, expected_min in test_cases:
            multiplier = engine.get_seasonal_prevalence(condition, month)
            if multiplier >= expected_min:
                patterns_validated += 1
                print(f"  ✓ {condition} in {month}: {multiplier}x (>= {expected_min}x)")
            else:
                print(f"  ⚠ {condition} in {month}: {multiplier}x (expected >= {expected_min}x)")

        # Should validate at least 2 patterns
        assert patterns_validated >= 2, \
            f"Expected at least 2 seasonal patterns validated, got {patterns_validated}"

        print(f"✓ Seasonal patterns validated: {patterns_validated}/{len(test_cases)}")


class TestGeographicPrevalence:
    """Test geographic prevalence adjustments"""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_heat_stroke_geographic_prevalence(self, engine):
        """Test heat stroke has high prevalence in hot climates"""
        desert_multiplier = engine.get_geographic_prevalence("heat-stroke", "desert-climate")

        # Should have very high prevalence in desert
        assert desert_multiplier >= 3.0, \
            f"Expected desert heat-stroke prevalence >= 3.0x, got {desert_multiplier}x"

        # Compare to temperate regions
        temperate_multiplier = engine.get_geographic_prevalence("heat-stroke", "temperate-climate")
        assert temperate_multiplier < desert_multiplier, \
            "Desert prevalence should be higher than temperate"

        print(f"✓ Heat stroke geographic pattern validated: desert {desert_multiplier}x, "
              f"temperate {temperate_multiplier}x")

    def test_influenza_urban_prevalence(self, engine):
        """Test influenza prevalence in urban areas"""
        # Test influenza in different population densities
        urban_multiplier = engine.get_geographic_prevalence("influenza", "urban-area")

        # Should be elevated in urban areas
        assert urban_multiplier >= 1.3, \
            f"Expected influenza in urban areas >= 1.3x, got {urban_multiplier}x"

        # Compare to rural
        rural_multiplier = engine.get_geographic_prevalence("influenza", "rural-area")
        assert rural_multiplier < urban_multiplier, \
            "Urban prevalence should be higher than rural"

        print(f"✓ Influenza geographic pattern validated: urban {urban_multiplier}x, "
              f"rural {rural_multiplier}x")


class TestSymptomTimingPatterns:
    """Test symptom onset timing pattern recognition"""

    @pytest.fixture
    def engine(self):
        return MeTTaQueryEngine()

    def test_heart_attack_timing_pattern(self, engine):
        """Test heart attack symptom timing recognition"""
        timing = engine.check_symptom_timing("heart-attack")

        # Should have timing information
        assert timing is not None, "Heart attack should have timing pattern"

        # Should indicate acute onset
        timing_lower = timing.lower()
        assert any(keyword in timing_lower for keyword in ['acute', 'sudden', 'minutes']), \
            f"Expected acute timing pattern, got: {timing}"

        print(f"✓ Heart attack timing validated: {timing}")

    def test_pneumonia_timing_pattern(self, engine):
        """Test pneumonia has gradual onset pattern"""
        timing = engine.check_symptom_timing("pneumonia")

        # Should have timing information
        assert timing is not None, "Pneumonia should have timing pattern"

        # Should indicate gradual progression over hours to days
        timing_lower = timing.lower()
        assert any(keyword in timing_lower for keyword in ['gradual', 'hours', 'days']), \
            f"Expected gradual timing pattern, got: {timing}"

        print(f"✓ Pneumonia timing validated: {timing}")


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])
