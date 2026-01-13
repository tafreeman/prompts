#!/usr/bin/env python3
"""
Test all model providers to ensure encoding and connectivity work correctly.
"""

import sys
import os
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent))

from llm_client import LLMClient

# UTF-8 setup for Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

def test_model(model_name: str, prompt: str = "Say 'Hello World' in exactly 2 words.") -> dict:
    """Test a single model."""
    try:
        response = LLMClient.generate_text(model_name, prompt, max_tokens=50)
        success = bool(response and not response.startswith("Error") and "error" not in response.lower()[:100])
        return {
            "model": model_name,
            "status": "✅ OK" if success else "⚠️ RESPONSE",
            "response": response[:100] if response else "No response",
            "error": None
        }
    except Exception as e:
        return {
            "model": model_name,
            "status": "❌ ERROR",
            "response": None,
            "error": str(e)[:100]
        }

def main():
    print("="*60)
    print("MODEL PROVIDER TEST")
    print("="*60)
    
    # Test models (ordered by typical availability)
    test_models = [
        # Local ONNX (Always available if installed)
        ("local:phi4mini", "Local ONNX (Phi-4)"),
        ("local:mistral", "Local ONNX (Mistral)"),
        
        # Ollama (Available if running)
        ("ollama:phi4-reasoning", "Ollama (Phi-4 Reasoning)"),
        ("ollama:deepseek-r1:14b", "Ollama (DeepSeek-R1)"),
        ("ollama:qwen2.5-coder:14b", "Ollama (Qwen2.5 Coder)"),
        
        # Windows AI (NPU-accelerated, Windows 11 only)
        ("windows-ai:phi-silica", "Windows AI (Phi Silica)"),
        
        # GitHub Models (Requires GITHUB_TOKEN)
        ("gh:gpt-4o-mini", "GitHub Models (GPT-4o-mini)"),
        ("gh:gpt-4.1", "GitHub Models (GPT-4.1)"),
        
        # Azure Foundry (Requires AZURE_FOUNDRY_API_KEY + endpoints)
        ("azure-foundry:1", "Azure Foundry (Endpoint 1)"),
        
        # Remote APIs (Require explicit --allow-remote)
        # Uncommented these to test if PROMPTEVAL_ALLOW_REMOTE=1
        # ("openai:gpt-4o-mini", "OpenAI (GPT-4o-mini)"),
        # ("gemini:gemini-pro", "Google Gemini"),
        # ("claude:claude-3-5-sonnet-20241022", "Anthropic Claude"),
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
