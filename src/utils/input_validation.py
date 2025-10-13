"""
Input Validation Module for MediChain AI
Validates user input and provides appropriate guidance for edge cases
"""

import re
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of input validation"""
    is_valid: bool
    reason: str
    confidence: float
    guidance_message: Optional[str] = None


class InputValidator:
    """Validates medical input and detects edge cases"""

    def __init__(self):
        # CRITICAL: Emergency keywords
        self.emergency_keywords = [
            'can\'t breathe', 'cannot breathe', 'difficulty breathing', 'shortness of breath',
            'gasping', 'gasping for air', 'suffocating', 'can barely breathe',
            'chest pain', 'crushing pain', 'heart attack',
            'severe bleeding', 'bleeding heavily', 'won\'t stop bleeding',
            'unconscious', 'passed out', 'collapsed',
            'seizure', 'seizing', 'convulsing',
            'overdose', 'took too many', 'swallowed pills',
            'stroke', 'face drooping', 'arm weakness', 'speech difficulty',
            'severe burn', 'burned badly',
            'choking', 'can\'t swallow',
            'severe allergic reaction', 'throat swelling',
        ]

        # CRITICAL: Mental health crisis keywords
        self.crisis_keywords = [
            'suicide', 'suicidal', 'kill myself', 'end my life',
            'self harm', 'self-harm', 'hurt myself', 'cutting myself',
            'no reason to live', 'want to die', 'better off dead',
            'end it all', 'can\'t go on',
        ]

        # Prescription-related keywords
        self.prescription_keywords = [
            'prescribe', 'prescription', 'give me', 'need antibiotics',
            'need medication', 'can you write', 'need pills',
            'need medicine', 'get me some',
        ]

        # Greeting keywords
        self.greeting_keywords = [
            'hello', 'hi', 'hey', 'greetings', 'good morning',
            'good evening', 'good afternoon', 'how are you',
            'what\'s up', 'sup', 'yo', 'hiya',
        ]

        # Off-topic keywords
        self.off_topic_keywords = [
            'weather', 'news', 'stock', 'sport', 'game', 'movie',
            'music', 'recipe', 'travel', 'hotel', 'flight',
            'restaurant', 'food', 'politics', 'election',
        ]

        # Meta/system questions
        self.meta_keywords = [
            'how do you work', 'what can you do', 'who made you',
            'who are you', 'what are you', 'are you real',
            'are you ai', 'are you a bot', 'help', 'instructions',
            'how to use', 'what is this',
        ]

        # Symptom keywords (from patient_intake patterns)
        self.symptom_keywords = [
            'pain', 'ache', 'fever', 'temperature', 'headache', 'nausea',
            'vomiting', 'diarrhea', 'cough', 'shortness', 'breathing', 'dizzy',
            'fatigue', 'tired', 'weakness', 'swelling', 'rash', 'itch', 'bleeding',
            'chest', 'stomach', 'abdomen', 'throat', 'back', 'joint', 'muscle',
            'sick', 'ill', 'hurt', 'sore', 'burn', 'bleed', 'swollen',
            'cramp', 'spasm', 'numbness', 'tingling', 'inflammation',
        ]

        # Temporal patterns
        self.temporal_patterns = [
            'day', 'week', 'hour', 'month', 'year', 'since',
            'started', 'began', 'ago', 'yesterday', 'last',
            'morning', 'night', 'today', 'earlier',
        ]

        # Severity indicators
        self.severity_keywords = [
            'severe', 'mild', 'moderate', 'extreme', 'terrible',
            'bad', 'intense', 'sharp', 'dull', 'throbbing',
            'unbearable', 'excruciating', 'slight', 'minor',
        ]

        # Pet/animal indicators
        self.pet_keywords = [
            'my dog', 'my cat', 'my pet', 'my puppy', 'my kitten',
            'our dog', 'our cat', 'his dog', 'her cat',
            'animal', 'veterinary', 'vet',
        ]

        # Proxy indicators (symptoms for others)
        # Possessive + relationship patterns
        self.proxy_possessive = ['my', 'his', 'her', 'our', 'their']
        self.proxy_relationships = [
            'child', 'daughter', 'son', 'baby', 'kid', 'infant', 'toddler',
            'mom', 'dad', 'mother', 'father', 'parent',
            'wife', 'husband', 'spouse', 'partner',
            'friend', 'sister', 'brother', 'sibling',
            'grandmother', 'grandfather', 'grandma', 'grandpa',
        ]
        self.proxy_phrase_keywords = [
            'he has', 'she has', 'they have', 'he is', 'she is',
        ]

        # Session history indicators
        self.history_keywords = [
            'yesterday you', 'last time', 'last week', 'last month',
            'you told me', 'you said', 'you mentioned',
            'earlier you', 'before you', 'previously you',
            'previous session', 'remember when', 'do you remember',
            'from our last', 'our conversation', 'we talked',
            'what did we', 'what did you',
        ]

    def validate(self, text: str) -> ValidationResult:
        """
        Main validation method - checks all scenarios
        Returns ValidationResult with guidance if needed
        """
        if not text or not text.strip():
            return ValidationResult(
                is_valid=False,
                reason="empty_input",
                confidence=1.0,
                guidance_message=self._get_guidance("empty_input")
            )

        text_lower = text.lower().strip()
        words = text_lower.split()

        # CRITICAL 1: Check for emergencies
        if self._contains_keywords(text_lower, self.emergency_keywords):
            return ValidationResult(
                is_valid=False,
                reason="emergency",
                confidence=1.0,
                guidance_message=self._get_guidance("emergency")
            )

        # CRITICAL 2: Check for mental health crisis
        if self._contains_keywords(text_lower, self.crisis_keywords):
            return ValidationResult(
                is_valid=False,
                reason="mental_health_crisis",
                confidence=1.0,
                guidance_message=self._get_guidance("mental_health_crisis")
            )

        # CRITICAL 3: Check for prescription requests
        if self._contains_keywords(text_lower, self.prescription_keywords):
            return ValidationResult(
                is_valid=False,
                reason="prescription_request",
                confidence=0.9,
                guidance_message=self._get_guidance("prescription_request")
            )

        # IMPORTANT 4: Check for pet symptoms
        if self._contains_keywords(text_lower, self.pet_keywords):
            return ValidationResult(
                is_valid=False,
                reason="pet_symptoms",
                confidence=0.95,
                guidance_message=self._get_guidance("pet_symptoms")
            )

        # IMPORTANT 5: Check for proxy symptoms (child, family member)
        is_proxy = self._is_proxy_symptom(text_lower)
        if is_proxy:
            # This is actually VALID but needs special handling
            has_symptoms = self._contains_keywords(text_lower, self.symptom_keywords)
            if has_symptoms:
                return ValidationResult(
                    is_valid=True,
                    reason="proxy_symptoms",
                    confidence=0.85,
                    guidance_message=None  # Will process but with pediatric caution
                )
            else:
                return ValidationResult(
                    is_valid=False,
                    reason="proxy_symptoms_vague",
                    confidence=0.7,
                    guidance_message=self._get_guidance("proxy_symptoms_vague")
                )

        # IMPORTANT 6: Check for session history questions
        if self._contains_keywords(text_lower, self.history_keywords):
            return ValidationResult(
                is_valid=False,
                reason="session_history",
                confidence=0.85,
                guidance_message=self._get_guidance("session_history")
            )

        # Check for greeting
        is_greeting = len(words) <= 3 and self._contains_keywords(text_lower, self.greeting_keywords)
        if is_greeting:
            return ValidationResult(
                is_valid=False,
                reason="greeting",
                confidence=1.0,
                guidance_message=self._get_guidance("greeting")
            )

        # Check for meta questions
        if self._contains_keywords(text_lower, self.meta_keywords):
            return ValidationResult(
                is_valid=False,
                reason="meta_question",
                confidence=0.9,
                guidance_message=self._get_guidance("meta_question")
            )

        # Check for off-topic
        if self._contains_keywords(text_lower, self.off_topic_keywords):
            return ValidationResult(
                is_valid=False,
                reason="off_topic",
                confidence=0.8,
                guidance_message=self._get_guidance("off_topic")
            )

        # Check for gibberish/testing
        if self._is_gibberish(text_lower):
            return ValidationResult(
                is_valid=False,
                reason="gibberish",
                confidence=0.7,
                guidance_message=self._get_guidance("gibberish")
            )

        # Check for medical content validity
        has_symptoms = self._contains_keywords(text_lower, self.symptom_keywords)
        has_duration = self._contains_keywords(text_lower, self.temporal_patterns)
        has_severity = self._contains_keywords(text_lower, self.severity_keywords)
        has_age = self._has_age_info(text_lower)

        # Calculate completeness score
        completeness_score = sum([
            has_symptoms * 0.4,  # 40% weight
            has_duration * 0.2,  # 20% weight
            has_age * 0.2,       # 20% weight
            has_severity * 0.2   # 20% weight
        ])

        # Must have at least symptoms to be valid
        if has_symptoms:
            if completeness_score >= 0.4:
                return ValidationResult(
                    is_valid=True,
                    reason="valid_medical_input",
                    confidence=completeness_score
                )
            else:
                # Has symptoms but incomplete
                return ValidationResult(
                    is_valid=True,
                    reason="valid_but_incomplete",
                    confidence=completeness_score,
                    guidance_message=None  # Will process but may ask for more details
                )

        # Check if it's just too vague
        if len(words) < 5:
            return ValidationResult(
                is_valid=False,
                reason="too_vague",
                confidence=0.7,
                guidance_message=self._get_guidance("too_vague")
            )

        # Default: insufficient medical information
        return ValidationResult(
            is_valid=False,
            reason="insufficient_info",
            confidence=0.5,
            guidance_message=self._get_guidance("insufficient_info")
        )

    def _contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """Check if text contains any of the keywords"""
        return any(keyword in text for keyword in keywords)

    def _is_proxy_symptom(self, text: str) -> bool:
        """
        Check if user is describing symptoms for someone else
        Detects patterns like: "my daughter", "his mom", "she has"
        """
        # Check phrase patterns first
        if self._contains_keywords(text, self.proxy_phrase_keywords):
            return True

        # Check for possessive + relationship combination
        has_possessive = any(poss in text for poss in self.proxy_possessive)
        has_relationship = any(rel in text for rel in self.proxy_relationships)

        return has_possessive and has_relationship

    def _has_age_info(self, text: str) -> bool:
        """Check if text contains age information"""
        if 'age' in text or 'years old' in text or 'year old' in text:
            return True
        # Check for age patterns like "28", "I'm 35", "age 42"
        age_pattern = re.search(r'\b(?:age\s*)?(\d{1,3})\s*(?:years?\s*old|y\.?o\.?|yrs?)?\b', text)
        return age_pattern is not None

    def _is_gibberish(self, text: str) -> bool:
        """Detect gibberish or testing input"""
        # Check for repeated characters
        if re.search(r'(.)\1{4,}', text):  # Same char repeated 5+ times
            return True

        # Check for common test patterns
        test_patterns = ['test', 'asdf', 'qwerty', '123', 'abc']
        if any(pattern * 2 in text for pattern in test_patterns):
            return True

        # Check for very low vowel ratio (gibberish often has few vowels)
        vowels = sum(1 for char in text if char in 'aeiou')
        consonants = sum(1 for char in text if char.isalpha() and char not in 'aeiou')
        if consonants > 0 and vowels / (vowels + consonants) < 0.15:
            return True

        return False

    def _get_guidance(self, reason: str) -> str:
        """Get appropriate guidance message based on validation failure reason"""

        base_template = (
            "To help analyze your health concerns, please describe:\n"
            "• Your symptoms (e.g., fever, headache, chest pain, nausea)\n"
            "• When they started (duration: hours, days, weeks)\n"
            "• Severity (mild, moderate, severe)\n"
            "• Your age\n\n"
            "Example: \"I have a severe headache and high fever for 2 days. I'm 28 years old.\"\n\n"
            "⚠️ For emergencies (chest pain, difficulty breathing, severe bleeding), call 911 immediately."
        )

        guidance_templates = {
            "emergency": (
                "🚨 **EMERGENCY DETECTED** 🚨\n\n"
                "Based on your symptoms, this may be a medical emergency.\n\n"
                "⚠️ **CALL 911 IMMEDIATELY** or go to the nearest emergency room.\n\n"
                "**DO NOT WAIT** for my analysis. Get emergency help NOW.\n\n"
                "**While waiting for emergency services:**\n"
                "• Stay calm, sit or lie down\n"
                "• Don't drive yourself\n"
                "• Have someone stay with you\n"
                "• Note your symptoms to tell paramedics\n\n"
                "**This is time-sensitive. Please get immediate medical attention.**"
            ),

            "mental_health_crisis": (
                "🆘 **I'm concerned about your safety.**\n\n"
                "If you're having thoughts of self-harm, please reach out for immediate support:\n\n"
                "📞 **National Suicide Prevention Lifeline:** 988 (call or text)\n"
                "📞 **Crisis Text Line:** Text HOME to 741741\n"
                "📞 **Emergency:** 911\n\n"
                "**You don't have to face this alone.** Help is available 24/7.\n\n"
                "I'm a medical diagnostic tool and cannot provide mental health crisis support, "
                "but trained counselors at these numbers can help you right now.\n\n"
                "**Your life matters. Please call one of these numbers.**"
            ),

            "prescription_request": (
                "⚠️ **I cannot prescribe medications.**\n\n"
                "I'm an AI diagnostic assistant, not a licensed physician. \n\n"
                "**I can:**\n"
                "✅ Analyze your symptoms\n"
                "✅ Suggest possible conditions\n"
                "✅ Recommend evidence-based treatments (general guidance)\n\n"
                "**I CANNOT:**\n"
                "❌ Prescribe medications\n"
                "❌ Write prescriptions\n"
                "❌ Provide medical advice as a substitute for doctors\n\n"
                "**For prescription medications, you must:**\n"
                "1. Schedule appointment with licensed doctor\n"
                "2. Get proper examination\n"
                "3. Receive prescription from physician\n\n"
                "Would you like to describe your symptoms so I can provide general information about your condition?"
            ),

            "pet_symptoms": (
                "I specialize in **human health** and cannot provide veterinary advice.\n\n"
                "For your pet's symptoms, please:\n"
                "📞 Contact your veterinarian\n"
                "📞 Emergency vet clinic (if after hours)\n"
                "🔍 Search for \"emergency vet near me\"\n\n"
                "Pet health issues can be serious and require professional veterinary care.\n\n"
                "If you have **personal health concerns**, I'm here to help! Please describe your symptoms."
            ),

            "proxy_symptoms_vague": (
                "I understand you're concerned about someone else's health.\n\n"
                "⚠️ **IMPORTANT FOR CHILDREN:**\n"
                "Children, especially young ones, can deteriorate quickly. When in doubt, "
                "contact your pediatrician or seek immediate care.\n\n"
                + base_template +
                "\n\nPlease provide:\n"
                "• Person's age (especially important for children)\n"
                "• Specific symptoms\n"
                "• Duration\n"
                "• Severity"
            ),

            "session_history": (
                "I don't have access to previous conversations or session history.\n\n"
                "Each chat session is independent for privacy and security reasons.\n\n"
                "If you'd like a fresh assessment, please describe:\n"
                "• Your current symptoms\n"
                "• How long you've had them\n"
                "• Any changes since last time\n"
                "• Any treatments you've tried\n\n"
                "Example: \"I still have the headache from yesterday. It's now day 3, and it's getting worse. "
                "I tried ibuprofen but it didn't help. I'm 28 years old.\"\n\n"
                "⚠️ If your symptoms are worsening or not improving, consider seeing a doctor."
            ),

            "greeting": (
                "Hello! I'm MediChain AI, your medical diagnostic assistant. 👋\n\n"
                + base_template
            ),

            "meta_question": (
                "I'm **MediChain AI**, an AI-powered medical diagnostic assistant using MeTTa knowledge graphs.\n\n"
                "**I can help you:**\n"
                "✅ Analyze your symptoms\n"
                "✅ Assess urgency levels\n"
                "✅ Provide differential diagnoses\n"
                "✅ Recommend evidence-based treatments\n\n"
                + base_template
            ),

            "off_topic": (
                "I specialize in medical symptom analysis and health assessments.\n\n"
                "For other topics, I recommend using a general-purpose AI assistant.\n\n"
                + base_template
            ),

            "gibberish": (
                "I didn't understand that message.\n\n"
                "I'm MediChain AI, a medical diagnostic assistant.\n\n"
                "If you're testing the system: ✅ I'm working!\n\n"
                "If you need medical help, please describe your symptoms clearly:\n"
                + base_template
            ),

            "too_vague": (
                "I need more specific information to help you effectively.\n\n"
                + base_template
            ),

            "insufficient_info": (
                "I need more details about your symptoms to provide accurate analysis.\n\n"
                + base_template
            ),

            "empty_input": (
                "I didn't receive any message content.\n\n"
                + base_template
            ),
        }

        return guidance_templates.get(reason, base_template)


# Singleton instance
_validator = InputValidator()

def validate_input(text: str) -> ValidationResult:
    """
    Validate user input and return result with guidance if needed

    Args:
        text: User's input text

    Returns:
        ValidationResult with is_valid flag and guidance_message if needed
    """
    return _validator.validate(text)
