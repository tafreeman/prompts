import json
from typing import Any, Dict

from tools.llm.llm_client import LLMClient


class Refiner:
    """Model-agnostic refiner wrapper."""

    def __init__(self, model_name: str, temperature: float = 0.5):
        self.model_name = model_name
        self.temperature = temperature

    def refine_draft(self, draft_content: str, review_feedback: Dict[str, Any]) -> str:
        """Refines the draft based on review feedback."""
        prompt = self._build_refinement_prompt(draft_content, review_feedback)
        return LLMClient.generate_text(self.model_name, prompt)

    def _build_refinement_prompt(
        self, draft_content: str, review_feedback: Dict[str, Any]
    ) -> str:
        """Constructs the prompt for the refiner model."""
        feedback_str = json.dumps(review_feedback, indent=2)

        return f"""
You are an expert code refiner. Your task is to improve the following draft to meet Tier 1 quality standards based on the provided review feedback.

**Original Draft**:
{draft_content}

**Review Feedback**:
{feedback_str}

**Instructions**:
1. Address ALL "weaknesses" and "suggestions" listed in the feedback.
2. Maintain the strengths identified.
3. Ensure the final output is a complete, valid file (Markdown/Python/etc.).
4. Do not include explanations or conversational text in the output, just the refined content.

**Goal**: The refined content should score 95+ on the quality rubric.
"""
