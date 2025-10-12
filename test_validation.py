"""Quick test script for input validation module"""

from src.utils.input_validation import validate_input


def test_scenario(description: str, text: str):
    """Test a validation scenario and print results"""
    print(f"\n{'='*60}")
    print(f"TEST: {description}")
    print(f"{'='*60}")
    print(f"Input: '{text}'")
    print()

    result = validate_input(text)

    print(f"✅ Valid: {result.is_valid}")
    print(f"📊 Reason: {result.reason}")
    print(f"🎯 Confidence: {result.confidence:.2f}")

    if result.guidance_message:
        print(f"\n📝 Guidance Message:")
        print("-" * 60)
        print(result.guidance_message)


if __name__ == "__main__":
    print("=" * 60)
    print("MEDICHAIN AI - INPUT VALIDATION TEST SUITE")
    print("=" * 60)

    # CRITICAL: Emergency scenarios
    test_scenario(
        "Emergency: Chest pain",
        "I have severe chest pain and I can't breathe properly"
    )

    test_scenario(
        "Emergency: Severe bleeding",
        "I'm bleeding heavily and can't stop it"
    )

    # CRITICAL: Mental health crisis
    test_scenario(
        "Mental health crisis: Suicide",
        "I want to kill myself, I can't take this anymore"
    )

    # CRITICAL: Prescription requests
    test_scenario(
        "Prescription request",
        "Can you prescribe me some antibiotics for my infection?"
    )

    # IMPORTANT: Proxy symptoms (children)
    test_scenario(
        "Proxy symptoms: Child",
        "My 5-year-old daughter has a high fever and won't stop crying"
    )

    # IMPORTANT: Session history
    test_scenario(
        "Session history question",
        "What did we talk about last week?"
    )

    # NICE-TO-HAVE: Greetings
    test_scenario(
        "Greeting",
        "Hey there! How are you doing?"
    )

    # NICE-TO-HAVE: Gibberish
    test_scenario(
        "Gibberish/testing",
        "asdfasdf test test 123"
    )

    # NICE-TO-HAVE: Pet symptoms
    test_scenario(
        "Pet symptoms",
        "My dog has been vomiting all morning"
    )

    # VALID: Actual medical symptoms
    test_scenario(
        "Valid symptoms",
        "I have a severe headache and fever for 2 days, and now my neck feels stiff"
    )

    test_scenario(
        "Valid symptoms: Brief",
        "headache, fever, nausea"
    )

    print("\n" + "=" * 60)
    print("TEST SUITE COMPLETE")
    print("=" * 60)
