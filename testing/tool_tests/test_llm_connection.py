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

from tools.llm.llm_client import LLMClient  # noqa: E402


def _load_repo_env() -> None:
    """Best-effort load of the repo .env.

    Does not overwrite existing environment variables.
    """
    env_path = ROOT_DIR / ".env"
    if not env_path.exists():
        return
    try:
        from dotenv import load_dotenv

        load_dotenv(env_path, override=False)
    except Exception:
        # No dependency, or parse failure; ignore.
        return


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
        response = LLMClient.generate_text(
            model_name,
            "Say 'Hello' in one word.",
        )
        print(f"[SUCCESS] Response: {response.strip()}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")


def main():
    print("LLM Connection Tester")
    print("=====================")

    _load_repo_env()

    # Gemini: pick an available model for this key.
    gemini_available = LLMClient.list_gemini_models()
    if gemini_available:
        print(f"Gemini models discovered: {len(gemini_available)}")
    gemini_model = (
        LLMClient._pick_preferred_model(
            gemini_available,
            [
                "gemini-2.0-flash",
                "gemini-2.0-flash-lite",
                "gemini-1.5-flash",
                "gemini-1.5-pro",
            ],
        )
        or (gemini_available[0] if gemini_available else "gemini-1.5-pro")
    )
    _check_provider("gemini", gemini_model)

    # Claude: Anthropic doesn't provide a simple model listing in this tool;
    # keep a reasonable default.
    _check_provider("claude", "claude-3-sonnet-20240229")

    # OpenAI: list models accessible to this key and pick a sensible default.
    openai_available = LLMClient.list_openai_models()
    if openai_available:
        print(f"OpenAI models discovered: {len(openai_available)}")
    openai_model = (
        LLMClient._pick_preferred_model(
            openai_available,
            [
                "gpt-4o-mini",
                "gpt-4.1-mini",
                "gpt-4o",
                "gpt-4.1",
                "gpt-3.5-turbo",
            ],
        )
        or (openai_available[0] if openai_available else "gpt-4o-mini")
    )
    _check_provider("gpt", openai_model)

    print("\nDone.")


if __name__ == "__main__":
    main()
