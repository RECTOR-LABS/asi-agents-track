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

    def add_fact(self, fact: str):
        """
        Add a new fact to the knowledge base.

        Args:
            fact: MeTTa fact to add (e.g., "(has-symptom flu fever)")
        """
        try:
            self.metta.run(fact)
        except Exception as e:
            print(f"Error adding fact: {e}")

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
        return [str(r) for r in results]

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
        return [str(r) for r in results]

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
        return str(results[0]) if results else "unknown"

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
        return str(results[0]) if results else "unknown"

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
        return [str(r) for r in results]

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

    def generate_reasoning_chain(self, symptoms: List[str], top_condition: str) -> str:
        """
        Generate human-readable reasoning chain for diagnosis.

        Args:
            symptoms: List of symptoms
            top_condition: Top matching condition

        Returns:
            Formatted reasoning chain
        """
        reasoning = []
        reasoning.append(f"DIAGNOSTIC REASONING FOR: {top_condition.upper()}")
        reasoning.append("=" * 50)

        # Symptom matching
        condition_symptoms = self.find_symptoms_by_condition(top_condition)
        matched = [s for s in symptoms if s in str(condition_symptoms)]
        reasoning.append(f"\nSYMPTOM MATCHING:")
        reasoning.append(f"  Patient symptoms: {', '.join(symptoms)}")
        reasoning.append(f"  Condition symptoms: {', '.join([str(s) for s in condition_symptoms])}")
        reasoning.append(f"  Matched: {len(matched)}/{len(symptoms)}")

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
        for treatment in treatments:
            source = self.get_evidence_source(treatment)
            reasoning.append(f"  - {treatment} (Evidence: {source})")

        # Differential diagnosis
        differentials = self.find_differential_diagnoses(top_condition)
        if differentials:
            reasoning.append(f"\nDIFFERENTIAL DIAGNOSES TO CONSIDER:")
            reasoning.append(f"  {', '.join([str(d) for d in differentials])}")

        return "\n".join(reasoning)


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
