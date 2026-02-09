import os
import sys
from pathlib import Path

import pytest

# Add project root to path for imports
ROOT_DIR = Path(__file__).parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.agents.code_generator import UniversalCodeGenerator

# Skip if required API keys are not available
# Accept either GOOGLE_API_KEY or GEMINI_API_KEY for Google
SKIP_REASON = (
    "Requires GOOGLE_API_KEY/GEMINI_API_KEY and ANTHROPIC_API_KEY environment variables"
)
requires_api_keys = pytest.mark.skipif(
    not (
        (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"))
        and os.getenv("ANTHROPIC_API_KEY")
    ),
    reason=SKIP_REASON,
)


@requires_api_keys
def test_generator():
    """Integration test for UniversalCodeGenerator - requires API keys."""
    print("Initializing UniversalCodeGenerator...")
    generator = UniversalCodeGenerator()

    category = "business"
    use_case = "Project Budget Tracker"
    variables = {"project_name": "New HQ Build", "budget": "$50M"}

    print(f"\nTesting generation for: {use_case}")
    result = generator.generate(category, use_case, variables)

    print("\n--- Result ---")
    print(f"Draft: {result.draft[:100]}..." if result.draft else "Draft: None")
    print(f"Review Score: {result.review.get('score', 'N/A')}")
    print(f"Refined: {result.final[:100]}..." if result.final else "Refined: None")

    # LLM output is non-deterministic - just verify we got responses
    assert result.draft is not None, "Expected draft response"
    assert result.final is not None, "Expected final response"
    assert isinstance(
        result.review.get("score"), (int, float)
    ), "Expected numeric review score"
    print("\n✅ Test Passed!")


if __name__ == "__main__":
    test_generator()
