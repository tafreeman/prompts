import json
import os
from typing import Any, Dict

from tools.llm.llm_client import LLMClient


class Reviewer:
    """Model-agnostic reviewer wrapper."""

    def __init__(self, model_name: str, temperature: float = 0.0):
        self.model_name = model_name
        self.temperature = temperature
        self.rubric = self._load_rubric()

    def _load_rubric(self) -> Dict[str, Any]:
        """Loads the quality standards rubric."""
        rubric_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "rubrics",
            "quality_standards.json",
        )
        try:
            with open(rubric_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Rubric not found at {rubric_path}. Using default.")
            return {}

    def review_draft(self, draft_content: str) -> Dict[str, Any]:
        """Reviews the draft content and returns a quality score and
        feedback."""
        prompt = self._build_review_prompt(draft_content)
        response_text = LLMClient.generate_text(self.model_name, prompt)

        # In a real implementation, we'd parse the JSON response from the LLM.
        # For now, we'll return the mock response if the LLM returns a placeholder string.
        if (
            "[Gemini Response]" in response_text
            or "[Claude Response]" in response_text
            or "[GPT Response]" in response_text
        ):
            return {
                "score": 88,
                "tier": 2,
                "strengths": ["Excellent structure", "Comprehensive description"],
                "weaknesses": ["Tip #4 is generic", "Example lacks ROI calculation"],
                "suggestions": [
                    "Make Tip #4 specific to Azure cost alerts",
                    "Add 3-year ROI table to example",
                ],
            }

        # Try to parse actual JSON response
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {"score": 0, "error": "Failed to parse review response"}

    def _build_review_prompt(self, draft_content: str) -> str:
        """Constructs the prompt for the reviewer model using the loaded
        rubric."""
        criteria_text = json.dumps(self.rubric.get("criteria", []), indent=2)

        return f"""
You are a quality assurance reviewer evaluating a prompt against Tier 1 standards.

**Prompt to Review**:
{draft_content}

**Evaluation Criteria**:
{criteria_text}

**Task**: 
1. Score each criterion (0-Max Points)
2. Calculate total score (0-100)
3. Identify specific strengths and weaknesses
4. Provide actionable suggestions for improvement

**Output Format**: JSON with score, strengths, weaknesses, suggestions.
"""
