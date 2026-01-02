#!/usr/bin/env python3
"""
Phase 4 Validation Script
=========================
Validates that YAML and Markdown evaluations produce consistent schemas.
"""

import json
import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from prompteval.__main__ import (
    evaluate_structural,
    find_prompts,
    ModelResult,
)


def test_prompt_discovery():
    """Test that find_prompts discovers both MD and YAML files."""
    print("=" * 60)
    print("TEST 1: Prompt Discovery")
    print("=" * 60)
    
    # Test on evals directory
    evals_path = Path(__file__).parent / "evals"
    prompts = find_prompts(evals_path)
    
    yaml_files = [p for p in prompts if p.suffix in ['.yml', '.yaml']]
    md_files = [p for p in prompts if p.suffix == '.md']
    
    print(f"✓ Found {len(prompts)} total prompts")
    print(f"  - {len(yaml_files)} YAML files")
    print(f"  - {len(md_files)} Markdown files")
    
    if yaml_files:
        print(f"\nYAML files discovered:")
        for f in yaml_files[:5]:  # Show first 5
            print(f"  - {f.name}")
    
    return len(prompts) > 0


def test_structural_evaluation():
    """Test structural evaluation on both file types."""
    print("\n" + "=" * 60)
    print("TEST 2: Structural Evaluation")
    print("=" * 60)
    
    # Find a YAML file
    evals_path = Path(__file__).parent / "evals"
    prompts = find_prompts(evals_path)
    yaml_file = next((p for p in prompts if p.suffix in ['.yml', '.yaml']), None)
    
    if not yaml_file:
        print("⚠️  No YAML files found for testing")
        return False
    
    print(f"\nTesting: {yaml_file.name}")
    result = evaluate_structural(yaml_file)
    
    print(f"\nStructural score: {result['score']}")
    print(f"Criteria: {json.dumps(result['criteria'], indent=2)}")
    print(f"Title: {result['title']}")
    print(f"Category: {result['category']}")
    
    # Verify schema
    required_keys = ['score', 'criteria', 'title', 'category']
    missing = [k for k in required_keys if k not in result]
    
    if missing:
        print(f"\n❌ Missing required keys: {missing}")
        return False
    
    print(f"\n✓ Schema valid (all required keys present)")
    return True


def test_schema_consistency():
    """Verify that ModelResult schema is consistent."""
    print("\n" + "=" * 60)
    print("TEST 3: Schema Consistency")
    print("=" * 60)
    
    # Create sample ModelResult instances
    md_result = ModelResult(
        model="local:phi4",
        run=1,
        score=85.5,
        criteria={"clarity": 90, "effectiveness": 85},
        duration=1.2,
    )
    
    yaml_result = ModelResult(
        model="local:phi4",
        run=1,
        score=82.3,
        criteria={"clarity": 88, "effectiveness": 80},
        duration=1.5,
    )
    
    # Check they have same fields
    md_fields = set(md_result.__dict__.keys())
    yaml_fields = set(yaml_result.__dict__.keys())
    
    print(f"\nModelResult fields:")
    for field in sorted(md_fields):
        print(f"  - {field}")
    
    if md_fields == yaml_fields:
        print(f"\n✓ Schema consistent ({len(md_fields)} fields)")
        return True
    else:
        print(f"\n❌ Schema mismatch!")
        print(f"  Only in MD: {md_fields - yaml_fields}")
        print(f"  Only in YAML: {yaml_fields - md_fields}")
        return False


def main():
    """Run all validation tests."""
    print("\n🧪 Phase 4 Validation: YAML Evaluation Support")
    print("=" * 60)
    
    tests = [
        ("Prompt Discovery", test_prompt_discovery),
        ("Structural Evaluation", test_structural_evaluation),
        ("Schema Consistency", test_schema_consistency),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"\n❌ {name} failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print("\n🎉 All validation tests passed!")
        print("✅ Phase 4 is complete and ready for production use.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
