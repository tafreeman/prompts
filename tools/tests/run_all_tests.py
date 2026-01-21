#!/usr/bin/env python3
"""
Run all tests in the tools/tests directory

This script discovers and runs all test files, providing a summary report.
"""

import sys
import subprocess
from pathlib import Path

def run_tests():
    """Run all tests and report results"""
    
    tests_dir = Path(__file__).parent
    test_files = sorted(tests_dir.glob("test_*.py"))
    
    if not test_files:
        print("❌ No test files found!")
        return 1
    
    print("=" * 70)
    print("TOOLS TEST SUITE")
    print("=" * 70)
    print(f"\nFound {len(test_files)} test file(s):\n")
    
    for test_file in test_files:
        print(f"  • {test_file.name}")
    
    print("\n" + "=" * 70)
    print("RUNNING TESTS")
    print("=" * 70 + "\n")
    
    results = []
    
    for test_file in test_files:
        print(f"\n{'='*70}")
        print(f"Testing: {test_file.name}")
        print("="*70)
        
        try:
            # Run pytest on the test file
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            success = result.returncode == 0
            results.append({
                "file": test_file.name,
                "success": success,
                "returncode": result.returncode
            })
            
            # Print output
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
            
            if success:
                print(f"\n✅ {test_file.name} PASSED")
            else:
                print(f"\n⚠️  {test_file.name} FAILED (some tests may have failed or been skipped)")
                
        except subprocess.TimeoutExpired:
            print(f"\n⏱️  {test_file.name} TIMEOUT")
            results.append({
                "file": test_file.name,
                "success": False,
                "returncode": -1
            })
        except Exception as e:
            print(f"\n❌ {test_file.name} ERROR: {e}")
            results.append({
                "file": test_file.name,
                "success": False,
                "returncode": -1
            })
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for r in results if r["success"])
    failed = len(results) - passed
    
    print(f"\n✅ Passed: {passed}/{len(results)}")
    print(f"❌ Failed: {failed}/{len(results)}")
    
    if passed == len(results):
        print("\n🎉 All test files passed!")
    
    print("\nDetails:")
    for result in results:
        status = "✅ PASS" if result["success"] else "❌ FAIL"
        print(f"  {status}  {result['file']}")
    
    print("\n" + "=" * 70)
    
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(run_tests())
