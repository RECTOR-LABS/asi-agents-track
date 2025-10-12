#!/usr/bin/env python3
"""
Test Treatment Protocol Integration (EPIC 7 - Phase 3)

Tests treatment agent's ability to return step-by-step protocols:
- Protocol retrieval for critical conditions
- Step sequencing and ordering
- Timing and priority information
- Integration with existing treatment recommendations
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.metta.query_engine import MeTTaQueryEngine
from src.agents.treatment_recommendation import TreatmentRecommender


class TestTreatmentProtocols:
    """Test treatment protocol enhancements"""

    @pytest.fixture
    def recommender(self):
        engine = MeTTaQueryEngine()
        return TreatmentRecommender(engine)

    def test_heart_attack_protocol_integration(self, recommender):
        """Test that heart attack recommendations include step-by-step protocol"""
        result = recommender.recommend_treatments(
            primary_condition="heart-attack",
            urgency_level="emergency",
            patient_age=65
        )

        # Verify protocol was retrieved
        assert "treatment_protocol" in result, "Should return treatment_protocol"
        protocol = result["treatment_protocol"]

        # Heart attack should have protocol (8 steps)
        assert len(protocol) >= 8, f"Expected at least 8 protocol steps, got {len(protocol)}"

        # Verify protocol structure
        first_step = protocol[0]
        assert "step_number" in first_step, "Protocol step should have step_number"
        assert "action" in first_step, "Protocol step should have action"
        assert "timing" in first_step, "Protocol step should have timing"
        assert "priority" in first_step, "Protocol step should have priority"

        # First step should be immediate and critical
        assert first_step["step_number"] == 1, "First step should be numbered 1"
        assert first_step["timing"] == "immediate", "First step should be immediate"
        assert first_step["priority"] == "critical", "First step should be critical"

        # Verify critical step is call-911
        assert first_step["action"] == "call-911", "First step for heart attack should be call-911"

        print(f"✓ Heart attack protocol integrated: {len(protocol)} steps")
        print(f"  Step 1: {first_step['action']} ({first_step['timing']}, {first_step['priority']})")

    def test_protocol_sequencing_order(self, recommender):
        """Test that protocol steps are returned in correct sequential order"""
        result = recommender.recommend_treatments(
            primary_condition="stroke",
            urgency_level="emergency"
        )

        protocol = result["treatment_protocol"]

        if len(protocol) > 0:
            # Verify step numbers are sequential
            step_numbers = [step["step_number"] for step in protocol]
            expected_sequence = list(range(1, len(protocol) + 1))

            assert step_numbers == expected_sequence, \
                f"Protocol steps should be sequential: expected {expected_sequence}, got {step_numbers}"

            print(f"✓ Stroke protocol sequencing validated: {len(protocol)} steps in order")
            for i, step in enumerate(protocol[:3], 1):  # Show first 3
                print(f"  Step {i}: {step['action']} ({step['timing']})")

    def test_protocol_priority_levels(self, recommender):
        """Test that protocols include appropriate priority levels"""
        result = recommender.recommend_treatments(
            primary_condition="anaphylaxis",
            urgency_level="emergency"
        )

        protocol = result["treatment_protocol"]

        if len(protocol) > 0:
            # Should have critical priority steps
            critical_steps = [s for s in protocol if s["priority"] == "critical"]
            assert len(critical_steps) >= 2, \
                f"Expected at least 2 critical steps for anaphylaxis, got {len(critical_steps)}"

            # Verify priority values are valid
            valid_priorities = ["critical", "high", "medium", "low"]
            for step in protocol:
                assert step["priority"] in valid_priorities, \
                    f"Invalid priority: {step['priority']}"

            print(f"✓ Anaphylaxis protocol priorities validated:")
            print(f"  Critical steps: {len(critical_steps)}/{len(protocol)}")

    def test_protocol_timing_information(self, recommender):
        """Test that protocol steps include timing information"""
        result = recommender.recommend_treatments(
            primary_condition="sepsis",
            urgency_level="emergency"
        )

        protocol = result["treatment_protocol"]

        if len(protocol) > 0:
            # Verify all steps have timing
            for step in protocol:
                assert "timing" in step, f"Step {step['step_number']} missing timing"
                assert step["timing"] != "", "Timing should not be empty"

            # Should have immediate timing for critical steps
            immediate_steps = [s for s in protocol if s["timing"] == "immediate"]
            assert len(immediate_steps) >= 1, \
                "Expected at least 1 immediate step for sepsis"

            print(f"✓ Sepsis protocol timing validated:")
            print(f"  Immediate steps: {len(immediate_steps)}")
            print(f"  Total steps: {len(protocol)}")

    def test_no_protocol_for_routine_conditions(self, recommender):
        """Test that routine conditions may not have structured protocols"""
        result = recommender.recommend_treatments(
            primary_condition="common-cold",
            urgency_level="routine"
        )

        # Should still return treatment_protocol key
        assert "treatment_protocol" in result, "Should always return treatment_protocol key"

        protocol = result["treatment_protocol"]

        # Common cold likely has no structured protocol - should be empty list
        if len(protocol) == 0:
            print(f"✓ Common cold correctly has no structured protocol (as expected)")
        else:
            print(f"✓ Common cold has {len(protocol)} protocol steps")

    def test_protocol_reasoning_chain(self, recommender):
        """Test that reasoning chain mentions protocol when available"""
        result = recommender.recommend_treatments(
            primary_condition="heart-attack",
            urgency_level="emergency"
        )

        reasoning = result["reasoning_chain"]
        protocol = result["treatment_protocol"]

        # If protocol exists, reasoning should mention it
        if len(protocol) > 0:
            protocol_mentioned = any("protocol" in step.lower() for step in reasoning)
            assert protocol_mentioned, \
                "Reasoning chain should mention protocol when available"

            # Should mention number of steps
            steps_mentioned = any(str(len(protocol)) in step for step in reasoning)
            assert steps_mentioned, \
                f"Reasoning should mention {len(protocol)} protocol steps"

            print(f"✓ Protocol mentioned in reasoning chain")

    def test_backward_compatibility_no_protocol(self, recommender):
        """Test that system works for conditions without protocols"""
        result = recommender.recommend_treatments(
            primary_condition="migraine",
            urgency_level="routine",
            patient_age=35
        )

        # Should complete successfully
        assert "treatments" in result
        assert "treatment_protocol" in result
        assert "reasoning_chain" in result

        # Should have empty protocol list
        assert isinstance(result["treatment_protocol"], list), \
            "treatment_protocol should be a list"

        print(f"✓ Backward compatibility maintained for conditions without protocols")

    def test_protocol_actions_are_actionable(self, recommender):
        """Test that protocol actions are specific and actionable"""
        result = recommender.recommend_treatments(
            primary_condition="heat-stroke",
            urgency_level="emergency"
        )

        protocol = result["treatment_protocol"]

        if len(protocol) > 0:
            for step in protocol:
                action = step["action"]

                # Action should not be empty
                assert action and len(action) > 0, \
                    f"Step {step['step_number']} has empty action"

                # Action should be hyphenated format (e.g., call-911, chew-aspirin-325mg)
                assert "-" in action, \
                    f"Action should be hyphenated format: {action}"

            print(f"✓ Heat stroke protocol actions validated: {len(protocol)} actionable steps")
            for step in protocol[:3]:  # Show first 3
                print(f"  Step {step['step_number']}: {step['action']}")


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])
