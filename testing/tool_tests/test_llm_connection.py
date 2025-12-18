#!/usr/bin/env python3
"""
Test LLM Connection
Verifies that the LLMClient can connect to the configured providers.
"""

import os
import sys
from pathlib import Path

# Add project root to path for imports
ROOT_DIR = Path(__file__).parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.llm_client import LLMClient


def _check_provider(provider_name, model_name):
    print(f"\nTesting {provider_name} ({model_name})...")

    # Check for API key first
    env_var = f"{provider_name.upper()}_API_KEY"
    if provider_name == "gpt":
        env_var = "OPENAI_API_KEY"

    if not os.getenv(env_var):
        print(f"[SKIP] {env_var} not set.")
        return

    try:
        response = LLMClient.generate_text(model_name, "Say 'Hello' in one word.")
        print(f"[SUCCESS] Response: {response.strip()}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")


def main():
    print("LLM Connection Tester")
    print("=====================")

    _check_provider("gemini", "gemini-1.5-pro")
    _check_provider("claude", "claude-3-sonnet-20240229")
    _check_provider("gpt", "gpt-4")

    print("\nDone.")


if __name__ == "__main__":
    main()
