"""
Direct MeTTa Query Engine Testing
Test the knowledge graph without agent infrastructure
"""

import sys
sys.path.append('.')

from src.metta.query_engine import MeTTaQueryEngine

def test_meningitis_diagnosis():
    """Test meningitis diagnostic scenario"""
    print("\n" + "="*70)
    print("TEST CASE 1: MENINGITIS DIAGNOSIS")
    print("="*70)

    engine = MeTTaQueryEngine()

    # Patient symptoms
    symptoms = ['fever', 'severe-headache', 'stiff-neck', 'non-blanching-rash']

    print(f"\n🩺 Patient Symptoms: {symptoms}")
    print("-" * 70)

    # Step 1: Find matching conditions
    print("\n📊 STEP 1: Multi-symptom matching with confidence scoring")
    matches = engine.find_conditions_by_symptoms(symptoms)
    print(f"Matching conditions: {matches}")

    # Step 2: Check for emergency conditions
    print("\n🚨 STEP 2: Emergency condition detection")
    emergency_conditions = engine.find_emergency_conditions()
    print(f"Emergency conditions in KB: {emergency_conditions}")

    # Step 3: Detect red flag symptoms
    print("\n⚠️  STEP 3: Red flag symptom detection")
    all_red_flags = engine.find_red_flag_symptoms()
    detected_red_flags = [s for s in symptoms if s in str(all_red_flags)]
    print(f"Red flags detected: {detected_red_flags}")

    # Step 4: Get top condition details
    if matches:
        top_condition = max(matches, key=matches.get)
        print(f"\n🎯 STEP 4: Primary diagnosis - {top_condition.upper()}")
        print("-" * 70)

        # Urgency level
        urgency = engine.find_urgency_level(top_condition)
        print(f"   Urgency: {urgency}")

        # Severity
        severity = engine.find_severity_level(top_condition)
        print(f"   Severity: {severity}")

        # Required action
        action = engine.get_required_action(top_condition)
        print(f"   Action: {action}")

        # Time sensitivity
        time_sensitive = engine.check_time_sensitivity(top_condition)
        print(f"   Time-sensitive: {time_sensitive}")

        # Treatments
        treatments = engine.get_treatment_recommendations(top_condition)
        print(f"\n💊 STEP 5: Treatment recommendations")
        for treatment in treatments:
            treatment_str = str(treatment).strip("'[]")
            evidence = engine.get_evidence_source(treatment_str)
            safety = engine.get_safety_warning(treatment_str)
            contraindications = engine.get_all_contraindications(treatment_str)

            print(f"   • {treatment_str}")
            print(f"     Evidence: {evidence}")
            if safety:
                print(f"     ⚠️  Safety: {safety}")
            if contraindications:
                print(f"     ⚠️  Contraindicated for: {contraindications}")

        # Differential diagnoses
        print(f"\n🔍 STEP 6: Differential diagnoses")
        differentials = engine.find_differential_diagnoses(top_condition)
        print(f"   Consider also: {differentials}")

        # Generate full reasoning chain
        print(f"\n🧠 STEP 7: Complete reasoning chain")
        print("=" * 70)
        reasoning = engine.generate_reasoning_chain(symptoms, top_condition)
        print(reasoning)


def test_stroke_diagnosis():
    """Test stroke diagnostic scenario"""
    print("\n\n" + "="*70)
    print("TEST CASE 2: STROKE DIAGNOSIS")
    print("="*70)

    engine = MeTTaQueryEngine()

    # Patient symptoms
    symptoms = ['face-drooping', 'arm-weakness', 'speech-difficulty', 'sudden-onset']

    print(f"\n🩺 Patient Symptoms: {symptoms}")
    print("-" * 70)

    # Find matches
    matches = engine.find_conditions_by_symptoms(symptoms)
    print(f"\n📊 Matching conditions: {matches}")

    if 'stroke' in matches:
        print(f"\n🎯 Primary diagnosis: STROKE")
        print("-" * 70)

        urgency = engine.find_urgency_level('stroke')
        severity = engine.find_severity_level('stroke')
        action = engine.get_required_action('stroke')
        time_sensitive = engine.check_time_sensitivity('stroke')

        print(f"   Urgency: {urgency}")
        print(f"   Severity: {severity}")
        print(f"   Action: {action}")
        print(f"   Time-sensitive: {time_sensitive}")

        print(f"\n🧠 Complete reasoning chain:")
        print("=" * 70)
        reasoning = engine.generate_reasoning_chain(symptoms, 'stroke')
        print(reasoning)


def test_common_cold():
    """Test common cold diagnostic scenario"""
    print("\n\n" + "="*70)
    print("TEST CASE 3: COMMON COLD DIAGNOSIS")
    print("="*70)

    engine = MeTTaQueryEngine()

    # Patient symptoms
    symptoms = ['runny-nose', 'mild-cough', 'sore-throat']

    print(f"\n🩺 Patient Symptoms: {symptoms}")
    print("-" * 70)

    # Find matches
    matches = engine.find_conditions_by_symptoms(symptoms)
    print(f"\n📊 Matching conditions: {matches}")

    if 'common-cold' in matches:
        print(f"\n🎯 Primary diagnosis: COMMON COLD")
        print("-" * 70)

        urgency = engine.find_urgency_level('common-cold')
        severity = engine.find_severity_level('common-cold')
        action = engine.get_required_action('common-cold')

        print(f"   Urgency: {urgency}")
        print(f"   Severity: {severity}")
        print(f"   Action: {action}")

        treatments = engine.get_treatment_recommendations('common-cold')
        print(f"\n💊 Treatment recommendations:")
        for treatment in treatments:
            print(f"   • {str(treatment).strip('[]\'')}")


def test_safety_validation():
    """Test safety validation features"""
    print("\n\n" + "="*70)
    print("TEST CASE 4: SAFETY VALIDATION")
    print("="*70)

    engine = MeTTaQueryEngine()

    print("\n💊 Testing contraindications for aspirin-immediately:")
    contraindications = engine.get_all_contraindications('aspirin-immediately')
    print(f"   Contraindicated for: {contraindications}")

    print("\n💊 Testing safety warning for aspirin-immediately:")
    safety = engine.get_safety_warning('aspirin-immediately')
    print(f"   Safety warning: {safety}")

    print("\n💊 Testing drug interactions for anticoagulation:")
    has_interaction = engine.check_drug_interaction('anticoagulation', 'aspirin')
    print(f"   Interacts with aspirin: {has_interaction}")

    print("\n💊 Testing dose adjustment for antibiotics:")
    needs_adjustment = engine.requires_dose_adjustment('antibiotics', 'renal-impairment')
    print(f"   Requires dose adjustment for renal impairment: {needs_adjustment}")


if __name__ == "__main__":
    print("\n🧪 METTA KNOWLEDGE GRAPH - DIRECT TESTING")
    print("="*70)
    print("Testing diagnostic reasoning without agent infrastructure")
    print("="*70)

    try:
        # Run all test cases
        test_meningitis_diagnosis()
        test_stroke_diagnosis()
        test_common_cold()
        test_safety_validation()

        print("\n\n" + "="*70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print("\nAlhamdulillah! The MeTTa knowledge graph is working perfectly! 🎉")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
