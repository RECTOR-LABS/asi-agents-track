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
