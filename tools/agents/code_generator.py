from typing import Dict, Any
from dataclasses import dataclass

# Support both relative imports (when used as package) and absolute imports (when run directly)
try:
    from .models import Generator, Reviewer, Refiner
    from .config import default_config, Config
except ImportError:
    from models import Generator, Reviewer, Refiner
    from config import default_config, Config


@dataclass
class PromptGenerationResult:
    draft: str
    review: Dict[str, Any]
    final: str
    metadata: Dict[str, Any]


class UniversalCodeGenerator:
    """
    Generates high-quality code/prompts/docs using a three-step workflow with flexible model selection.
    """

    def __init__(self, config: Config = default_config):
        self.config = config
        self.generator = Generator(
            model_name=config.models.generator_model,
            temperature=config.models.generator_temp
        )
        self.reviewer = Reviewer(
            model_name=config.models.reviewer_model,
            temperature=config.models.reviewer_temp
        )
        self.refiner = Refiner(
            model_name=config.models.refiner_model,
            temperature=config.models.refiner_temp
        )

    def generate(
        self,
        category: str,
        use_case: str,
        variables: Dict[str, str],
        target_tier: int = 1,
        auto_refine: bool = True
    ) -> PromptGenerationResult:
        """
        Generate a prompt with optional multi-model review.
        """
        # Step 1: Generate draft
        draft = self.generator.generate_draft(category, use_case, variables)

        # Step 2: External review
        review = self.reviewer.review_draft(draft)

        # Step 3: Refine (if score < 85 or auto_refine enabled)
        # Note: In a real scenario, we might check review['score']
        if auto_refine or review.get("score", 0) < 85:
            final = self.refiner.refine_draft(draft, review)
        else:
            final = draft

        return PromptGenerationResult(
            draft=draft,
            review=review,
            final=final,
            metadata=self._extract_metadata(final)
        )

    def _extract_metadata(self, content: str) -> Dict[str, Any]:
        """
        Extracts metadata from the generated content (e.g., YAML frontmatter).
        Placeholder implementation.
        """
        return {"version": "1.0", "generator": "UniversalCodeGenerator"}
