#!/usr/bin/env python3
"""
Debug MeTTa query parsing
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.metta.query_engine import MeTTaQueryEngine

def main():
    engine = MeTTaQueryEngine()

    print("=" * 70)
    print("DEBUG: Raw MeTTa Query Results")
    print("=" * 70)

    # Test 1: Risk factors for heart-attack
    print("\n1. Risk Factors Query:")
    query = "!(match &self (risk-factor heart-attack $factor $multiplier) ($factor $multiplier))"
    print(f"   Query: {query}")
    results = engine.query(query)
    print(f"   Raw results: {results}")
    print(f"   Results type: {type(results)}")
    print(f"   Results length: {len(results)}")

    if results:
        print(f"   First result: {results[0]}")
        print(f"   First result type: {type(results[0])}")
        print(f"   First result str: '{str(results[0])}'")

    # Test processed results
    processed = engine.get_risk_factors("heart-attack")
    print(f"   Processed results: {processed}")

    # Test 2: Diagnostic criteria for pneumonia
    print("\n2. Diagnostic Criteria Query:")
    query = "!(match &self (diagnostic-criteria pneumonia $system $criterion) ($system $criterion))"
    print(f"   Query: {query}")
    results = engine.query(query)
    print(f"   Raw results: {results}")
    print(f"   Results length: {len(results)}")

    if results:
        print(f"   First result: {results[0]}")
        print(f"   First result str: '{str(results[0])}'")

    # Test 3: Clarifying questions
    print("\n3. Clarifying Questions Query:")
    query = "!(match &self (clarifying-question chest-pain-differential $question) $question)"
    print(f"   Query: {query}")
    results = engine.query(query)
    print(f"   Raw results: {results}")
    print(f"   Results length: {len(results)}")

    if results:
        print(f"   First result: {results[0]}")
        print(f"   First result type: {type(results[0])}")

    # Test processed
    processed = engine.get_clarifying_questions("chest-pain-differential")
    print(f"   Processed: {processed}")

    # Test 4: Simple existence check
    print("\n4. Check if risk-factor exists in KB:")
    query = "!(match &self (risk-factor $c $f $m) $c)"
    results = engine.query(query)
    print(f"   Conditions with risk factors: {results[:5] if results else 'None'}")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
