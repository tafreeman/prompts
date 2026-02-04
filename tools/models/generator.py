from typing import Dict

from tools.llm.llm_client import LLMClient


class Generator:
    """Model-agnostic generator wrapper."""

    def __init__(self, model_name: str, temperature: float = 0.7):
        self.model_name = model_name
        self.temperature = temperature

    def generate_draft(
        self, category: str, use_case: str, variables: Dict[str, str]
    ) -> str:
        """Generates a draft prompt or code based on inputs."""
        prompt = self._build_generation_prompt(category, use_case, variables)
        return LLMClient.generate_text(self.model_name, prompt)

    def _build_generation_prompt(
        self, category: str, use_case: str, variables: Dict[str, str]
    ) -> str:
        """Constructs the prompt for the generator model."""
        return f"""
You are an expert prompt engineer creating a Tier 1 prompt for the {category} category.

**Task**: Create a comprehensive prompt for: {use_case}

**Variables**:
{variables}

**Output Format**: Complete markdown file.
"""
