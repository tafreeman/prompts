import asyncio
import os
import sys
from unittest.mock import patch

import pytest

# Add src to path
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../multiagent-workflows/src")
    ),
)

from multiagent_workflows.server.run_manager import ItemScore, _judge_with_llm

# Mock LLM response with the expected JSON structure
MOCK_LLM_RESPONSE = """
```json
{
    "breakdown": {
        "Correctness": 9,
        "Code Quality": 8,
        "Completeness": 10,
        "Robustness": 8
    },
    "total_score": 87.5,
    "passed": true,
    "feedback": "The solution is functionally correct and handles edge cases well. Code quality is good but could use minor refactoring."
}
```
"""

MOCK_FAIL_RESPONSE = """
{
    "breakdown": {
        "Correctness": 4,
        "Code Quality": 5
    },
    "total_score": 45.0,
    "passed": false,
    "feedback": "Code fails to meet requirements."
}
"""


@pytest.mark.asyncio
async def test_judge_with_llm_parsing():
    """Test that _judge_with_llm correctly parses the LLM response."""

    # Mock LLMClient
    with patch(
        "tools.llm.llm_client.LLMClient.generate_text", return_value=MOCK_LLM_RESPONSE
    ) as mock_generate:

        task_desc = "Write a function to calculate fibonacci numbers."
        gold = "def fib(n): return n if n <= 1 else fib(n-1) + fib(n-2)"
        actual = "def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)"

        # We need to ensure rubrics are loaded or mocked if _get_rubric_text is called
        # The function _judge_with_llm calls _get_rubric_text internally.
        # We can let it run if rubrics.yaml exists, or mock _get_rubric_text

        score: ItemScore = await asyncio.to_thread(
            _judge_with_llm,
            model="gh:openai/gpt-4o",
            task_desc=task_desc,
            gold=gold,
            actual=actual,
            workflow_id="fullstack",
        )

        assert score is not None
        assert score.normalized_similarity == 87.5
        assert score.similarity == 0.875
        assert score.breakdown["Correctness"] == 9
        assert score.breakdown["Completeness"] == 10
        assert score.total_score == 87.5
        print(
            f"✅ Parsing successful: Score {score.total_score}, Breakdown {score.breakdown}"
        )


@pytest.mark.asyncio
async def test_judge_with_llm_failure_parsing():
    """Test handling of failed/low score response."""

    with patch(
        "tools.llm.llm_client.LLMClient.generate_text", return_value=MOCK_FAIL_RESPONSE
    ):

        score: ItemScore = await asyncio.to_thread(
            _judge_with_llm,
            model="gh:openai/gpt-4o",
            task_desc="Task",
            gold="Gold",
            actual="Bad",
            workflow_id="fullstack",
        )

        assert score.normalized_similarity == 45.0
        assert score.breakdown["Correctness"] == 4
        print(f"✅ Failure parsing successful: Score {score.total_score}")


if __name__ == "__main__":
    # Manually run the async tests if executed as script
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print("Running test_judge_with_llm_parsing...")
    loop.run_until_complete(test_judge_with_llm_parsing())
    print("Running test_judge_with_llm_failure_parsing...")
    loop.run_until_complete(test_judge_with_llm_failure_parsing())
    print("All tests passed!")
