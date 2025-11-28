#!/usr/bin/env python3
"""
Test LLM Connection
Verifies that the LLMClient can connect to the configured providers.
"""

import os
from llm_client import LLMClient


def test_provider(provider_name, model_name):
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

    test_provider("gemini", "gemini-1.5-pro")
    test_provider("claude", "claude-3-sonnet-20240229")
    test_provider("gpt", "gpt-4")

    print("\nDone.")


if __name__ == "__main__":
    main()
