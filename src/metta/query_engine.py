"""
MeTTa Query Engine - Interface for querying MeTTa knowledge base
"""

from hyperon import MeTTa
from typing import List, Dict, Any, Optional
import os
from pathlib import Path


class MeTTaQueryEngine:
    """Query engine for MeTTa knowledge base."""

    def __init__(self, kb_path: Optional[str] = None):
        """
        Initialize MeTTa query engine.

        Args:
            kb_path: Path to MeTTa knowledge base file (.metta)
        """
        self.metta = MeTTa()

        # Load knowledge base
        if kb_path is None:
            kb_path = os.getenv(
                "METTA_KB_PATH",
                "./data/knowledge_base.metta"
            )

        self.kb_path = Path(kb_path)
        if self.kb_path.exists():
            self._load_knowledge_base()
        else:
            print(f"Warning: Knowledge base not found at {kb_path}")

    def _load_knowledge_base(self):
        """Load MeTTa knowledge base from file."""
        try:
            with open(self.kb_path, 'r') as f:
                kb_content = f.read()
                self.metta.run(kb_content)
            print(f"Successfully loaded knowledge base from {self.kb_path}")
        except Exception as e:
            print(f"Error loading knowledge base: {e}")

    def query(self, query_string: str) -> List[Any]:
        """
        Execute a MeTTa query.

        Args:
            query_string: MeTTa query string

        Returns:
            List of query results
        """
        try:
            results = self.metta.run(query_string)
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            return []

    def find_by_symptom(self, symptom: str) -> List[str]:
        """
        Find conditions associated with a symptom.

        Args:
            symptom: Symptom to search for

        Returns:
            List of conditions
        """
        query = f"!(match &self (has-symptom $condition {symptom}) $condition)"
        results = self.query(query)
        return [str(r) for r in results]

    def find_treatment(self, condition: str) -> List[str]:
        """
        Find treatments for a condition.

        Args:
            condition: Medical condition

        Returns:
            List of treatments
        """
        query = f"!(match &self (has-treatment {condition} $treatment) $treatment)"
        results = self.query(query)
        return [str(r) for r in results]

    def add_fact(self, fact: str) -> bool:
        """
        Add a new fact to the knowledge base.

        Args:
            fact: MeTTa fact to add (e.g., "(has-symptom flu fever)")

        Returns:
            True if successful, False otherwise
        """
        try:
            self.metta.run(fact)
            return True
        except Exception as e:
            print(f"Error adding fact: {e}")
            return False

    def get_all_facts(self, predicate: str) -> List[Any]:
        """
        Get all facts for a specific predicate.

        Args:
            predicate: Predicate name (e.g., "has-symptom")

        Returns:
            List of facts
        """
        query = f"!(match &self ({predicate} $x $y) ($x $y))"
        results = self.query(query)
        return results

    # ========================================
    # Medical-Specific Query Methods
    # ========================================

    def find_emergency_conditions(self) -> List[str]:
        """
        Find all emergency conditions requiring immediate 911 call.

        Returns:
            List of emergency conditions
        """
        query = "!(match &self (has-urgency $condition emergency) $condition)"
        results = self.query(query)
        # Use _parse_metta_list to handle nested list results
        return self._parse_metta_list(results)

    def _parse_metta_list(self, results: List[Any]) -> List[str]:
        """
        Parse MeTTa query results that return as nested lists.

        MeTTa returns results like: [[fever, headache, cough, ...]]
        We need to extract individual atoms as strings.

        Args:
            results: Raw MeTTa query results

        Returns:
            List of individual atom strings
        """
        parsed = []
        for result in results:
            # Result is typically a nested structure
            # Convert to string and parse
            result_str = str(result).strip()

            # Remove outer brackets if present
            if result_str.startswith('[') and result_str.endswith(']'):
                result_str = result_str[1:-1]

            # Split by comma and clean up each item
            items = [item.strip() for item in result_str.split(',')]
            parsed.extend([item for item in items if item])

        return parsed

    def find_symptoms_by_condition(self, condition: str) -> List[str]:
        """
        Find all symptoms for a specific condition.

        Args:
            condition: Medical condition name

        Returns:
            List of symptoms
        """
        query = f"!(match &self (has-symptom {condition} $symptom) $symptom)"
        results = self.query(query)
        # Parse the nested MeTTa list structure
        return self._parse_metta_list(results)

    def find_red_flag_symptoms(self) -> List[str]:
        """
        Find all red flag symptoms indicating serious conditions.

        Returns:
            List of red flag symptoms
        """
        query = "!(match &self (red-flag-symptom $symptom true) $symptom)"
        results = self.query(query)
        return [str(r) for r in results]

    def find_urgency_level(self, condition: str) -> str:
        """
        Get urgency level for a condition.

        Args:
            condition: Medical condition name

        Returns:
            Urgency level (emergency, urgent-24h, routine-care)
        """
        query = f"!(match &self (has-urgency {condition} $urgency) $urgency)"
        results = self.query(query)
        if results:
            # Strip brackets and quotes from result
            urgency = str(results[0]).strip("'[]")
            # Return "unknown" if result is empty after stripping
            return urgency if urgency else "unknown"
        return "unknown"

    def find_severity_level(self, condition: str) -> str:
        """
        Get severity level for a condition.

        Args:
            condition: Medical condition name

        Returns:
            Severity level (critical, urgent, routine)
        """
        query = f"!(match &self (has-severity {condition} $severity) $severity)"
        results = self.query(query)
        if results:
            # Strip brackets and quotes from result
            return str(results[0]).strip("'[]")
        return "unknown"

    def find_differential_diagnoses(self, condition: str) -> List[str]:
        """
        Find differential diagnoses for a condition.

        Args:
            condition: Medical condition name

        Returns:
            List of differential diagnoses
        """
        query = f"!(match &self (differential-from {condition} $other) $other)"
        results = self.query(query)
        return [str(r) for r in results]

    def find_conditions_by_symptoms(self, symptoms: List[str]) -> Dict[str, int]:
        """
        Find conditions matching multiple symptoms with match counts.

        Args:
            symptoms: List of symptom names

        Returns:
            Dictionary mapping conditions to symptom match counts
        """
        condition_matches = {}

        for symptom in symptoms:
            conditions = self.find_by_symptom(symptom)
            # Parse the results (format: "['[condition1, condition2]']")
            for result in conditions:
                # Extract conditions from result string
                result_str = str(result).strip("'[]")
                if result_str:
                    conds = [c.strip() for c in result_str.split(',')]
                    for cond in conds:
                        if cond:
                            condition_matches[cond] = condition_matches.get(cond, 0) + 1

        # Sort by match count (descending)
        return dict(sorted(condition_matches.items(), key=lambda x: x[1], reverse=True))

    def get_treatment_recommendations(self, condition: str) -> List[str]:
        """
        Get treatment recommendations for a condition.

        Args:
            condition: Medical condition name

        Returns:
            List of treatments
        """
        return self.find_treatment(condition)

    def get_required_action(self, condition: str) -> str:
        """
        Get required action for a condition.

        Args:
            condition: Medical condition name

        Returns:
            Required action
        """
        query = f"!(match &self (requires-action {condition} $action) $action)"
        results = self.query(query)
        return str(results[0]) if results else "consult-doctor"

    def check_time_sensitivity(self, condition: str) -> Optional[int]:
        """
        Check time sensitivity for a condition.

        Args:
            condition: Medical condition name

        Returns:
            Hours until critical or None if not time-sensitive
        """
        query = f"!(match &self (time-sensitive {condition} $hours) $hours)"
        results = self.query(query)
        if results:
            try:
                # Extract hours from result
                hours_str = str(results[0]).strip("'[]")
                return int(hours_str) if hours_str.isdigit() else None
            except:
                return None
        return None

    def get_evidence_source(self, treatment: str) -> str:
        """
        Get evidence source for a treatment.

        Args:
            treatment: Treatment name

        Returns:
            Evidence source
        """
        query = f"!(match &self (evidence-source {treatment} $source) $source)"
        results = self.query(query)
        return str(results[0]) if results else "clinical-guidelines"

    def check_contraindication(self, treatment: str, patient_condition: str) -> bool:
        """
        Check if treatment is contraindicated for patient condition.

        Args:
            treatment: Treatment name
            patient_condition: Patient's existing condition

        Returns:
            True if contraindicated, False otherwise
        """
        query = f"!(match &self (contraindication {treatment} {patient_condition}) {treatment})"
        results = self.query(query)
        return len(results) > 0

    def get_all_contraindications(self, treatment: str) -> List[str]:
        """
        Get all contraindications for a treatment.

        Args:
            treatment: Treatment name

        Returns:
            List of contraindicated conditions
        """
        query = f"!(match &self (contraindication {treatment} $condition) $condition)"
        results = self.query(query)
        # Use _parse_metta_list to handle nested list structure
        return self._parse_metta_list(results)

    def get_safety_warning(self, treatment: str) -> str:
        """
        Get safety warning for a treatment.

        Args:
            treatment: Treatment name

        Returns:
            Safety warning text
        """
        query = f"!(match &self (safety-warning {treatment} $warning) $warning)"
        results = self.query(query)
        return str(results[0]).strip('"') if results else ""

    def check_drug_interaction(self, treatment: str, medication: str) -> bool:
        """
        Check if treatment has drug interaction with existing medication.

        Args:
            treatment: Treatment name
            medication: Patient's current medication

        Returns:
            True if interaction exists, False otherwise
        """
        query = f"!(match &self (drug-interaction {treatment} {medication}) {treatment})"
        results = self.query(query)
        return len(results) > 0

    def requires_dose_adjustment(self, treatment: str, condition: str) -> bool:
        """
        Check if treatment requires dose adjustment for patient condition.

        Args:
            treatment: Treatment name
            condition: Patient condition (e.g., kidney-disease, elderly)

        Returns:
            True if dose adjustment needed, False otherwise
        """
        query = f"!(match &self (requires-dose-adjustment {treatment} {condition}) {treatment})"
        results = self.query(query)
        return len(results) > 0

    def find_lab_tests(self, condition: str) -> List[str]:
        """
        Find required lab tests for a condition (EPIC 7 - Phase 1).

        Args:
            condition: Medical condition name

        Returns:
            List of required lab tests
        """
        query = f"!(match &self (requires-lab-test {condition} $test) $test)"
        results = self.query(query)
        return self._parse_metta_list(results)

    def find_imaging_requirements(self, condition: str) -> List[str]:
        """
        Find required imaging for a condition (EPIC 7 - Phase 1).

        Args:
            condition: Medical condition name

        Returns:
            List of required imaging types
        """
        query = f"!(match &self (requires-imaging {condition} $imaging) $imaging)"
        results = self.query(query)
        return self._parse_metta_list(results)

    def get_all_lab_tests(self) -> List[str]:
        """
        Get all lab tests defined in knowledge base (EPIC 7 - Phase 1).

        Returns:
            List of all lab test types
        """
        query = "!(match &self (requires-lab-test $condition $test) $test)"
        results = self.query(query)
        # Return unique tests
        tests = self._parse_metta_list(results)
        return list(set(tests))

    def get_all_imaging(self) -> List[str]:
        """
        Get all imaging types defined in knowledge base (EPIC 7 - Phase 1).

        Returns:
            List of all imaging types
        """
        query = "!(match &self (requires-imaging $condition $imaging) $imaging)"
        results = self.query(query)
        # Return unique imaging types
        imaging_types = self._parse_metta_list(results)
        return list(set(imaging_types))

    def generate_reasoning_chain(
        self,
        symptoms: List[str],
        top_condition: str,
        patient_age: Optional[int] = None,
        patient_risk_factors: Optional[List[str]] = None
    ) -> str:
        """
        Generate human-readable reasoning chain for diagnosis (EPIC 7 - Phase 2 Enhanced).

        Args:
            symptoms: List of symptoms
            top_condition: Top matching condition
            patient_age: Patient age (optional, for risk assessment)
            patient_risk_factors: Patient risk factors from medical history (optional)

        Returns:
            Formatted reasoning chain with risk factor analysis
        """
        reasoning = []
        reasoning.append(f"DIAGNOSTIC REASONING FOR: {top_condition.upper()}")
        reasoning.append("=" * 50)

        # Patient context (EPIC 7 - Phase 2)
        if patient_age:
            reasoning.append(f"\nPATIENT CONTEXT:")
            reasoning.append(f"  Age: {patient_age} years")
            if patient_risk_factors:
                reasoning.append(f"  Risk factors: {', '.join(patient_risk_factors[:5])}")

        # Symptom matching
        condition_symptoms = self.find_symptoms_by_condition(top_condition)
        matched = [s for s in symptoms if s in str(condition_symptoms)]
        reasoning.append(f"\nSYMPTOM MATCHING:")
        reasoning.append(f"  Patient symptoms: {', '.join(symptoms)}")
        reasoning.append(f"  Condition symptoms: {', '.join([str(s) for s in condition_symptoms[:8]])}")
        reasoning.append(f"  Matched: {len(matched)}/{len(symptoms)}")

        # EPIC 7 - Phase 2: Risk Factor Analysis
        risk_factors = self.get_risk_factors(top_condition)
        if risk_factors:
            # Build patient risk factor list for comparison
            patient_factors_list = []
            if patient_age:
                if patient_age < 40:
                    patient_factors_list.append('age-under-40')
                elif patient_age <= 55:
                    patient_factors_list.append('age-40-55')
                elif patient_age <= 70:
                    patient_factors_list.append('age-55-70')
                else:
                    patient_factors_list.extend(['age-over-70', 'age-over-65'])

            if patient_risk_factors:
                patient_factors_list.extend(patient_risk_factors)

            # Calculate risk score
            risk_score = self.calculate_risk_score(top_condition, patient_factors_list)

            # Show top risk factors
            reasoning.append(f"\n⚡ RISK FACTOR ANALYSIS:")
            reasoning.append(f"  Patient risk score: {risk_score:.1f}")

            # Show matched risk factors
            matched_rf = [rf for rf in risk_factors if rf['factor'] in patient_factors_list]
            if matched_rf:
                reasoning.append(f"  Matched risk factors:")
                for rf in matched_rf[:5]:  # Show top 5
                    reasoning.append(f"    - {rf['factor']} (multiplier: {rf['multiplier']:.1f})")
            else:
                reasoning.append(f"  No significant risk factors present")

            # Age-specific risk if available
            if patient_age:
                age_group = 'age-over-70' if patient_age > 70 else f'age-{patient_age//10*10}-{(patient_age//10+1)*10}'
                age_risk = self.get_age_risk(top_condition, age_group)
                if age_risk != 'unknown':
                    reasoning.append(f"  Age-specific risk: {age_risk}")

        # Severity and urgency
        severity = self.find_severity_level(top_condition)
        urgency = self.find_urgency_level(top_condition)
        reasoning.append(f"\nCLASSIFICATION:")
        reasoning.append(f"  Severity: {severity}")
        reasoning.append(f"  Urgency: {urgency}")

        # Time sensitivity
        hours = self.check_time_sensitivity(top_condition)
        if hours:
            reasoning.append(f"  ⏰ Time-sensitive: Treatment needed within {hours} hours")

        # Red flags
        red_flags = self.find_red_flag_symptoms()
        patient_red_flags = [s for s in symptoms if s in str(red_flags)]
        if patient_red_flags:
            reasoning.append(f"\n🚨 RED FLAG SYMPTOMS DETECTED:")
            reasoning.append(f"  {', '.join(patient_red_flags)}")

        # Treatment
        treatments = self.get_treatment_recommendations(top_condition)
        action = self.get_required_action(top_condition)
        reasoning.append(f"\nRECOMMENDED ACTION:")
        reasoning.append(f"  {action}")
        reasoning.append(f"\nTREATMENT OPTIONS:")
        for treatment in treatments[:5]:  # Show top 5 treatments
            source = self.get_evidence_source(treatment)
            reasoning.append(f"  - {treatment} (Evidence: {source})")

        # Differential diagnosis
        differentials = self.find_differential_diagnoses(top_condition)
        if differentials:
            reasoning.append(f"\nDIFFERENTIAL DIAGNOSES TO CONSIDER:")
            reasoning.append(f"  {', '.join([str(d) for d in differentials[:5]])}")

        return "\n".join(reasoning)

    # ========================================
    # EPIC 7 - Phase 2: Risk Factors & Diagnostic Criteria
    # ========================================

    def get_risk_factors(self, condition: str) -> List[Dict[str, Any]]:
        """
        Get all risk factors for a condition with their multipliers (EPIC 7 - Phase 2).

        Args:
            condition: Medical condition name

        Returns:
            List of dictionaries with 'factor' and 'multiplier' keys
        """
        query = f"!(match &self (risk-factor {condition} $factor $multiplier) ($factor $multiplier))"
        results = self.query(query)

        risk_factors = []

        # MeTTa returns [[tuple1, tuple2, ...]] - double nested list
        for result in results:
            # Check if result is itself a list (nested structure)
            if isinstance(result, list):
                # Iterate over the inner list of tuples
                for item in result:
                    item_str = str(item).strip("'[] ")
                    # Remove parentheses
                    item_str = item_str.strip("()")

                    # Split on whitespace
                    parts = item_str.split()

                    if len(parts) >= 2:
                        factor = parts[0].strip()
                        try:
                            multiplier = float(parts[1].strip())
                            risk_factors.append({
                                'factor': factor,
                                'multiplier': multiplier
                            })
                        except (ValueError, IndexError):
                            continue
            else:
                # Handle single tuple (non-nested case)
                result_str = str(result).strip("'[] ()")
                parts = result_str.split()
                if len(parts) >= 2:
                    factor = parts[0].strip()
                    try:
                        multiplier = float(parts[1].strip())
                        risk_factors.append({
                            'factor': factor,
                            'multiplier': multiplier
                        })
                    except (ValueError, IndexError):
                        continue

        # Sort by multiplier (highest risk first)
        return sorted(risk_factors, key=lambda x: x['multiplier'], reverse=True)

    def calculate_risk_score(self, condition: str, patient_factors: List[str]) -> float:
        """
        Calculate risk score for a condition based on patient risk factors (EPIC 7 - Phase 2).

        Args:
            condition: Medical condition name
            patient_factors: List of patient's risk factors (e.g., ['age-over-65', 'diabetes-mellitus'])

        Returns:
            Risk score (sum of multipliers for matched factors)
        """
        all_risk_factors = self.get_risk_factors(condition)

        score = 0.0
        for rf in all_risk_factors:
            if rf['factor'] in patient_factors:
                score += rf['multiplier']

        return round(score, 2)

    def get_age_risk(self, condition: str, age_group: str) -> str:
        """
        Get age-specific risk level for a condition (EPIC 7 - Phase 2).

        Args:
            condition: Medical condition name
            age_group: Age group (e.g., 'age-under-40', 'age-40-55', 'age-55-70', 'age-over-70')

        Returns:
            Risk level (very-high, high, medium, low) or 'unknown'
        """
        query = f"!(match &self (age-risk {condition} {age_group} $risk) $risk)"
        results = self.query(query)

        if results:
            return str(results[0]).strip("'[] ")
        return "unknown"

    def check_diagnostic_criteria(self, condition: str, findings: List[str]) -> Dict[str, Any]:
        """
        Check if patient findings meet diagnostic criteria for a condition (EPIC 7 - Phase 2).

        Args:
            condition: Medical condition name
            findings: List of patient findings (e.g., ['age-under-50', 'heart-rate-under-100'])

        Returns:
            Dictionary with 'criteria_system', 'matched', 'total', and 'interpretation'
        """
        # Get all criteria for this condition
        query = f"!(match &self (diagnostic-criteria {condition} $system $criterion) ($system $criterion))"
        results = self.query(query)

        criteria_by_system = {}

        # MeTTa returns [[tuple1, tuple2, ...]] - double nested list
        for result in results:
            # Check if result is itself a list (nested structure)
            if isinstance(result, list):
                # Iterate over the inner list of tuples
                for item in result:
                    item_str = str(item).strip("'[] ()")

                    # Split on whitespace
                    parts = item_str.split()
                    if len(parts) >= 2:
                        system = parts[0].strip()
                        criterion = parts[1].strip()

                        if system not in criteria_by_system:
                            criteria_by_system[system] = []
                        criteria_by_system[system].append(criterion)
            else:
                # Handle single tuple (non-nested case)
                result_str = str(result).strip("'[] ()")
                parts = result_str.split()
                if len(parts) >= 2:
                    system = parts[0].strip()
                    criterion = parts[1].strip()

                    if system not in criteria_by_system:
                        criteria_by_system[system] = []
                    criteria_by_system[system].append(criterion)

        # Check matches for each system
        results_by_system = {}
        for system, criteria_list in criteria_by_system.items():
            # Match findings - check full match first, then prefix match
            matched = []
            for criterion in criteria_list:
                # Check exact match
                if criterion in findings:
                    matched.append(criterion)
                # Check if finding contains criterion (flexible matching)
                elif any(criterion in finding or finding in criterion for finding in findings):
                    matched.append(criterion)

            results_by_system[system] = {
                'criteria_system': system,
                'matched': len(matched),
                'total': len(criteria_list),
                'matched_criteria': matched,
                'interpretation': self._interpret_diagnostic_criteria(system, len(matched), len(criteria_list))
            }

        return results_by_system

    def _interpret_diagnostic_criteria(self, system: str, matched: int, total: int) -> str:
        """
        Interpret diagnostic criteria results based on scoring system.

        Args:
            system: Diagnostic criteria system name
            matched: Number of matched criteria
            total: Total number of criteria

        Returns:
            Interpretation string
        """
        # PERC rule - all must be negative (0 matches = low risk)
        if system == "perc-rule":
            if matched == 0:
                return "PE risk <2% (PERC negative)"
            else:
                return "PERC positive - consider further testing"

        # Wells score - interpret score
        elif system == "wells-score":
            if matched >= 2:
                return "DVT/PE likely (Wells ≥2)"
            else:
                return "DVT/PE unlikely (Wells <2)"

        # CURB-65 - interpret score (0-1 outpatient, 2 hospital, 3-5 ICU)
        elif system == "curb-65":
            if matched <= 1:
                return "Low severity - outpatient treatment (CURB-65: 0-1)"
            elif matched == 2:
                return "Moderate severity - consider hospitalization (CURB-65: 2)"
            else:
                return "High severity - ICU admission (CURB-65: 3-5)"

        # CHA2DS2-VASc - stroke risk
        elif system == "cha2ds2-vasc":
            if matched == 0:
                return "Very low stroke risk (0 points)"
            elif matched == 1:
                return "Low stroke risk (1 point) - consider anticoagulation"
            else:
                return f"Moderate-high stroke risk ({matched} points) - anticoagulation recommended"

        # Centor score - strep throat likelihood
        elif system == "centor-score":
            if matched <= 1:
                return "Strep unlikely (Centor ≤1) - no antibiotics"
            elif matched <= 3:
                return "Strep possible (Centor 2-3) - consider rapid strep test"
            else:
                return "Strep likely (Centor 4) - empiric antibiotics"

        # GCS - consciousness level
        elif system == "gcs":
            if matched >= 13:
                return "Mild injury (GCS 13-15)"
            elif matched >= 9:
                return "Moderate injury (GCS 9-12)"
            else:
                return "Severe injury (GCS 3-8)"

        # Default interpretation
        else:
            percentage = (matched / total * 100) if total > 0 else 0
            return f"{matched}/{total} criteria met ({percentage:.0f}%)"

    def get_clarifying_questions(self, symptom_category: str) -> List[str]:
        """
        Get clarifying questions for differential diagnosis (EPIC 7 - Phase 2).

        Args:
            symptom_category: Symptom category (e.g., 'chest-pain-differential', 'headache-differential')

        Returns:
            List of clarifying questions
        """
        query = f"!(match &self (clarifying-question {symptom_category} $question) $question)"
        results = self.query(query)

        questions = []
        for result in results:
            # Extract question text (may be in quotes)
            result_str = str(result).strip("'[] ")

            # Handle case where multiple questions come as one result
            # Split by escaped quotes pattern: ", "
            if '", "' in result_str or '\", \"' in result_str:
                # Multiple questions in one result - split them
                parts = result_str.replace('\\"', '"').split('", "')
                for part in parts:
                    question = part.strip('"').strip()
                    if question:
                        questions.append(question)
            else:
                # Single question
                question = result_str.strip('"')
                if question:
                    questions.append(question)

        return questions

    def get_differential_aids(self, condition1: str, condition2: str) -> List[str]:
        """
        Get questions that help differentiate between two conditions (EPIC 7 - Phase 2).

        Args:
            condition1: First condition
            condition2: Second condition

        Returns:
            List of clarifying questions
        """
        # Find questions that help differentiate these conditions
        query = f"!(match &self (helps-differentiate $question {condition1} {condition2}) $question)"
        results = self.query(query)

        questions = []
        for result in results:
            question = str(result).strip("'[] ")
            if question.startswith('"') and question.endswith('"'):
                question = question[1:-1]
            questions.append(question)

        # Also try reverse order
        query_reverse = f"!(match &self (helps-differentiate $question {condition2} {condition1}) $question)"
        results_reverse = self.query(query_reverse)

        for result in results_reverse:
            question = str(result).strip("'[] ")
            if question.startswith('"') and question.endswith('"'):
                question = question[1:-1]
            if question not in questions:
                questions.append(question)

        return questions

    def get_prevalence(self, condition: str, population_group: str) -> Optional[float]:
        """
        Get prevalence of a condition in a population group (EPIC 7 - Phase 2).

        Args:
            condition: Medical condition name
            population_group: Population group (e.g., 'age-under-40', 'female', 'male')

        Returns:
            Prevalence as decimal (e.g., 0.02 = 2%) or None if not found
        """
        query = f"!(match &self (prevalence {condition} {population_group} $rate) $rate)"
        results = self.query(query)

        if results:
            try:
                rate_str = str(results[0]).strip("'[] ")
                return float(rate_str)
            except ValueError:
                return None
        return None

    # ========================================
    # EPIC 7 - Phase 3: Treatment Protocols & Symptom Attributes
    # ========================================

    def get_treatment_protocol(self, condition: str) -> List[Dict[str, Any]]:
        """
        Get step-by-step treatment protocol for a condition (EPIC 7 - Phase 3).

        Args:
            condition: Medical condition name

        Returns:
            List of protocol steps, each with step_number, action, timing, priority
        """
        query = f"!(match &self (treatment-protocol {condition} $step $action $timing $priority) ($step $action $timing $priority))"
        results = self.query(query)

        protocol_steps = []

        # MeTTa returns [[tuple1, tuple2, ...]]
        for result in results:
            if isinstance(result, list):
                for item in result:
                    item_str = str(item).strip("'[] ()")
                    parts = item_str.split()

                    if len(parts) >= 4:
                        try:
                            step_number = int(parts[0])
                            action = parts[1]
                            timing = parts[2]
                            priority = parts[3]

                            protocol_steps.append({
                                'step_number': step_number,
                                'action': action,
                                'timing': timing,
                                'priority': priority
                            })
                        except (ValueError, IndexError):
                            continue

        # Sort by step number
        return sorted(protocol_steps, key=lambda x: x['step_number'])

    def get_protocol_steps(self, condition: str, priority_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get protocol steps with optional priority filtering (EPIC 7 - Phase 3).

        Args:
            condition: Medical condition name
            priority_filter: Optional filter ('critical', 'high', 'medium', 'low')

        Returns:
            Filtered list of protocol steps
        """
        all_steps = self.get_treatment_protocol(condition)

        if priority_filter:
            return [step for step in all_steps if step['priority'] == priority_filter]

        return all_steps

    def get_symptom_attributes(self, symptom: str) -> Dict[str, List[str]]:
        """
        Get all attributes for a symptom (EPIC 7 - Phase 3).

        Args:
            symptom: Symptom name

        Returns:
            Dictionary mapping attribute types to values
        """
        query = f"!(match &self (symptom-attribute {symptom} $attr_type $value) ($attr_type $value))"
        results = self.query(query)

        attributes = {}

        # MeTTa returns [[tuple1, tuple2, ...]]
        for result in results:
            if isinstance(result, list):
                for item in result:
                    item_str = str(item).strip("'[] ()")
                    parts = item_str.split()

                    if len(parts) >= 2:
                        attr_type = parts[0]
                        value = parts[1]

                        if attr_type not in attributes:
                            attributes[attr_type] = []
                        attributes[attr_type].append(value)

        return attributes

    def get_seasonal_prevalence(self, condition: str, month: str) -> float:
        """
        Get seasonal prevalence multiplier for a condition (EPIC 7 - Phase 3).

        Args:
            condition: Medical condition name
            month: Month name (lowercase: january, february, etc.)

        Returns:
            Prevalence multiplier (1.0 = baseline, >1.0 = increased, <1.0 = decreased)
        """
        query = f"!(match &self (seasonal-prevalence {condition} {month} $multiplier) $multiplier)"
        results = self.query(query)

        if results:
            try:
                # Handle nested list structure
                if isinstance(results[0], list):
                    multiplier_str = str(results[0][0]).strip("'[] ")
                else:
                    multiplier_str = str(results[0]).strip("'[] ")
                return float(multiplier_str)
            except (ValueError, IndexError):
                return 1.0  # Baseline

        return 1.0  # Baseline if not found

    def get_geographic_prevalence(self, condition: str, geography: str) -> float:
        """
        Get geographic prevalence multiplier for a condition (EPIC 7 - Phase 3).

        Args:
            condition: Medical condition name
            geography: Geographic descriptor (e.g., 'tropical-climate', 'urban-area')

        Returns:
            Prevalence multiplier (1.0 = baseline)
        """
        query = f"!(match &self (geographic-prevalence {condition} {geography} $multiplier) $multiplier)"
        results = self.query(query)

        if results:
            try:
                # Handle nested list structure
                if isinstance(results[0], list):
                    multiplier_str = str(results[0][0]).strip("'[] ")
                else:
                    multiplier_str = str(results[0]).strip("'[] ")
                return float(multiplier_str)
            except (ValueError, IndexError):
                return 1.0  # Baseline

        return 1.0  # Baseline if not found

    def check_symptom_timing(self, condition: str) -> Optional[str]:
        """
        Check symptom onset timing pattern for a condition (EPIC 7 - Phase 3).

        Args:
            condition: Medical condition name

        Returns:
            Timing pattern (e.g., 'sudden-minutes', 'gradual-hours-to-days') or None
        """
        query = f"!(match &self (symptom-onset-pattern {condition} $pattern) $pattern)"
        results = self.query(query)

        if results:
            # Handle nested list structure
            if isinstance(results[0], list):
                # Check if nested list is not empty
                if len(results[0]) > 0:
                    return str(results[0][0]).strip("'[] ")
                return None
            return str(results[0]).strip("'[] ")

        return None


# Example usage
if __name__ == "__main__":
    # Initialize query engine
    engine = MeTTaQueryEngine()

    # Add some example facts
    engine.add_fact("(has-symptom flu fever)")
    engine.add_fact("(has-symptom flu cough)")
    engine.add_fact("(has-symptom covid fever)")
    engine.add_fact("(has-treatment flu rest)")

    # Query examples
    print("Conditions with fever symptom:")
    print(engine.find_by_symptom("fever"))

    print("\nTreatments for flu:")
    print(engine.find_treatment("flu"))

    print("\nAll symptom facts:")
    print(engine.get_all_facts("has-symptom"))
