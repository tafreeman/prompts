#!/usr/bin/env python3
"""
Test all model providers to ensure encoding and connectivity work correctly.
"""

import sys
import os
from pathlib import Path

# Ensure the tools package is importable
sys.path.insert(0, str(Path(__file__).parents[2]))

from tools.llm.llm_client import LLMClient

# UTF-8 setup for Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def _test_model(model_name: str, prompt: str = "Say 'Hello World' in exactly 2 words.") -> dict:
    """Internal helper to test a single model. Returns a dict for reporting.
    This function is not a pytest test itself to avoid fixture resolution issues.
    """
    try:
        response = LLMClient.generate_text(model_name, prompt, max_tokens=50)
        success = bool(response and not response.startswith("Error") and "error" not in response.lower()[:100])
        return {
            "model": model_name,
            "status": "✅ OK" if success else "⚠️ RESPONSE",
            "response": response[:100] if response else "No response",
            "error": None,
        }
    except Exception as e:
        return {
            "model": model_name,
            "status": "❌ ERROR",
            "response": None,
            "error": str(e)[:100],
        }

def main():
    print("="*60)
    print("MODEL PROVIDER TEST")
    print("="*60)
    
    # Test models (ordered by typical availability)
    # Simplified model list for CI – only test local models that are guaranteed to exist.
    test_models = [
        ("local:phi4mini", "Local ONNX (Phi-4)"),
        ("local:mistral", "Local ONNX (Mistral)"),
    ]
    
    results = []
    for model, description in test_models:
        print(f"\nTesting {description}...")
        print(f"  Model: {model}")
        result = test_model(model)
        results.append(result)
        print(f"  Status: {result['status']}")
        if result['error']:
            print(f"  Error: {result['error']}")
        elif result['response']:
            print(f"  Response: {result['response'][:60]}...")
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    ok_count = sum(1 for r in results if r['status'] == "✅ OK")
    warn_count = sum(1 for r in results if r['status'] == "⚠️ RESPONSE")
    error_count = sum(1 for r in results if r['status'] == "❌ ERROR")
    
    print(f"✅ Working:    {ok_count}/{len(results)}")
    print(f"⚠️ Partial:    {warn_count}/{len(results)}")
    print(f"❌ Errors:     {error_count}/{len(results)}")
    
    print("\nWorking Models:")
    for r in results:
        if r['status'] == "✅ OK":
            print(f"  • {r['model']}")
    
    if error_count > 0:
        print("\nFailed Models:")
        for r in results:
            if r['status'] == "❌ ERROR":
                print(f"  • {r['model']}: {r['error']}")
    
    return 0 if ok_count > 0 else 1

if __name__ == "__main__":
    sys.exit(main())
