#!/usr/bin/env python3
"""Test all available models and report which ones work."""

from dotenv import load_dotenv

load_dotenv("d:/source/prompts/.env")

import sys

sys.path.insert(0, ".")

from core.llm_client import LLMClient

# All models to test
all_models = [
    # Local ONNX models
    ("local:phi4", "Phi-4 Mini (3.8B)", "Local ONNX"),
    ("local:phi3.5", "Phi-3.5 Mini (3.8B)", "Local ONNX"),
    ("local:phi3", "Phi-3 Mini (3.8B)", "Local ONNX"),
    ("local:phi3-medium", "Phi-3 Medium (14B)", "Local ONNX"),
    ("local:mistral", "Mistral 7B Instruct", "Local ONNX"),
    # GitHub Models
    ("gh:gpt-4o", "GPT-4o", "GitHub Models"),
    ("gh:gpt-4o-mini", "GPT-4o Mini", "GitHub Models"),
    # Azure AI Foundry
    ("azure-foundry:0:mistral-medium-2505", "Mistral Medium 2505", "Azure AI Foundry"),
]

print()
print("WORKING MODEL OPTIONS")
print("=" * 70)
print(f"{'Model ID':<45} {'Name':<20} Status")
print("-" * 70)

working = []
for model_id, name, provider in all_models:
    try:
        resp = LLMClient.generate_text(model_id, "Hi", max_tokens=10)
        if resp and not resp.startswith("Error"):
            status = "OK"
            working.append((model_id, name, provider))
        else:
            status = "FAIL"
    except Exception:
        status = "FAIL"
    print(f"{model_id:<45} {name:<20} {status}")

print()
print(f"Total working: {len(working)}/{len(all_models)}")
print()
print("WORKING MODELS SUMMARY:")
print("-" * 70)
for model_id, name, provider in working:
    print(f"  {model_id}")
