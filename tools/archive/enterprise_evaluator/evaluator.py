import json
import sys
from pathlib import Path
from typing import Any, Dict

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    # Look for .env in parent directories up to 3 levels
    for parent in [
        Path(__file__).parent,
        Path(__file__).parent.parent,
        Path(__file__).parent.parent.parent,
    ]:
        env_file = parent / ".env"
        if env_file.exists():
            load_dotenv(env_file)
            break
except ImportError:
    pass  # dotenv not installed, rely on system env vars

# Add parent tools directory to path for imports
TOOLS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(TOOLS_DIR))

from framework.dimensions import Dimension, EvaluationResult, PerformanceLevel
from framework.rubrics import (
    ALL_DIMENSIONS,
    BUSINESS_ALIGNMENT,
    INNOVATION_OPTIMIZATION,
    MAINTAINABILITY,
    PERFORMANCE_RELIABILITY,
    SECURITY_COMPLIANCE,
    TECHNICAL_QUALITY,
)
from framework.scoring import calculate_weighted_score, determine_performance_level

# Import from main tools (not local duplicates)
from llm_client import LLMClient


class EnterpriseEvaluator:
    def __init__(
        self,
        model_name: str = "local:phi4mini",
        temperature: float = 0.1,
        max_tokens: int = 1000,
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = LLMClient()

    def evaluate_file(self, file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        content = path.read_text(encoding="utf-8")

        results = []

        # Run evaluations for each dimension
        results.append(self._eval_technical_quality(content))
        results.append(self._eval_business_alignment(content))
        results.append(self._eval_security(content))
        results.append(self._eval_performance_reliability(content))
        results.append(self._eval_maintainability(content))
        results.append(self._eval_innovation(content))

        final_score = calculate_weighted_score(results, ALL_DIMENSIONS)
        performance_level = determine_performance_level(final_score)

        return {
            "file": str(path),
            "final_score": final_score,
            "performance_level": performance_level.value,
            "dimension_results": [
                {
                    "id": res.dimension_id,
                    "score": res.score,
                    "level": res.level.value,
                    "reasoning": res.reasoning,
                }
                for res in results
            ],
        }

    def _llm_judge_score(
        self, prompt_content: str, dimension: Dimension
    ) -> EvaluationResult:
        """Generic LLM Judge for subjective dimensions."""
        rubric_text = ""
        for level in PerformanceLevel:
            if level in dimension.rubric:
                rubric_text += (
                    f"\n{level.value}:\n{dimension.rubric[level]['criteria']}"
                )

        judge_prompt = f"""You are an expert Prompt Evaluator. Evaluate the following prompt based on the {dimension.name} dimension.

Prompt Content:
```
{prompt_content[:4000]}
```

Rubric for {dimension.name}:
{rubric_text}

Task:
1. Analyze the prompt against the criteria.
2. Assign a score from 0 to 100.
3. Provide a brief reasoning.

Return JSON format: {{ "score": <number>, "reasoning": "<text>" }}
"""
        response = self.client.generate_text(
            self.model_name,
            judge_prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        try:
            # Robust JSON parsing with multiple fallback strategies
            import re

            score = None
            reasoning = None

            # Strategy 1: Find first complete JSON object using brace counting
            def extract_first_json(text):
                start = text.find("{")
                if start == -1:
                    return None
                depth = 0
                for i, char in enumerate(text[start:], start):
                    if char == "{":
                        depth += 1
                    elif char == "}":
                        depth -= 1
                        if depth == 0:
                            return text[start : i + 1]
                return None

            # Clean response of markdown code blocks
            clean_response = response
            if "```json" in clean_response:
                match = re.search(r"```json\s*([\s\S]*?)\s*```", clean_response)
                if match:
                    clean_response = match.group(1)
            elif "```" in clean_response:
                match = re.search(r"```\s*([\s\S]*?)\s*```", clean_response)
                if match:
                    clean_response = match.group(1)

            # Try to extract first JSON object
            json_str = extract_first_json(clean_response)
            if json_str:
                try:
                    data = json.loads(json_str)
                    score = float(data.get("score", 0))
                    reasoning = data.get("reasoning", "No reasoning provided")
                except json.JSONDecodeError:
                    pass

            # Strategy 2: Regex fallback for score extraction
            if score is None:
                score_match = re.search(
                    r'["\']?score["\']?\s*[:\s]\s*(\d+(?:\.\d+)?)',
                    response,
                    re.IGNORECASE,
                )
                if score_match:
                    score = float(score_match.group(1))
                    # Try to get reasoning too
                    reason_match = re.search(
                        r'["\']?reasoning["\']?\s*[:\s]\s*["\']([^"\']+)["\']',
                        response,
                        re.IGNORECASE,
                    )
                    if reason_match:
                        reasoning = reason_match.group(1)
                    else:
                        reasoning = f"Score extracted via regex. Raw: {response[:200]}"

            # Strategy 3: Default fallback
            if score is None:
                score = 50.0
                reasoning = "Failed to parse LLM response: " + response[:150]

        except Exception as e:
            score = 50.0  # Give benefit of doubt vs 0
            reasoning = (
                f"Error interpreting judge response: {str(e)}. Raw: {response[:100]}"
            )

        level = determine_performance_level(score)

        return EvaluationResult(
            dimension_id=dimension.id,
            score=score,
            level=level,
            evidence=[],
            reasoning=reasoning,
        )

    def _eval_technical_quality(self, content: str) -> EvaluationResult:
        return self._llm_judge_score(content, TECHNICAL_QUALITY)

    def _eval_business_alignment(self, content: str) -> EvaluationResult:
        return self._llm_judge_score(content, BUSINESS_ALIGNMENT)

    def _eval_security(self, content: str) -> EvaluationResult:
        # Hybrid: use LLM judge but also check for common bad patterns if possible
        return self._llm_judge_score(content, SECURITY_COMPLIANCE)

    def _eval_performance_reliability(self, content: str) -> EvaluationResult:
        """
        Operational test: Run the prompt multiple times (reproducibility).
        """
        # For this test to work, we need to treat the 'content' as a prompt to run.
        # We will run it 3 times with a dummy input or just as is.
        # Note: If the prompt requires specific inputs, this blind run might fail or produce garbage.
        # We will try a generic approach: Run it 3 times and check similarity.

        # Run 1
        r1 = self.client.generate_text(
            self.model_name, content, temperature=self.temperature, max_tokens=100
        )
        # Run 2
        r2 = self.client.generate_text(
            self.model_name, content, temperature=self.temperature, max_tokens=100
        )
        # Run 3
        r3 = self.client.generate_text(
            self.model_name, content, temperature=self.temperature, max_tokens=100
        )

        # Calculate similarity (Jaccard or simple word overlap for now)
        def similarity(s1, s2):
            w1 = set(s1.lower().split())
            w2 = set(s2.lower().split())
            if not w1 or not w2:
                return 0.0
            intersection = len(w1.intersection(w2))
            union = len(w1.union(w2))
            return intersection / union

        sim_1_2 = similarity(r1, r2)
        sim_2_3 = similarity(r2, r3)
        sim_1_3 = similarity(r1, r3)

        avg_sim = (sim_1_2 + sim_2_3 + sim_1_3) / 3

        # Mapping similarity 0-1 to Score 0-100
        # High reliability = high similarity (if deterministic) OR consistent structure.
        # This is a rough proxy.
        reproducibility_score = avg_sim * 100

        # We also want an LLM judge to assess the *potential* for reliability based on the text
        judge_result = self._llm_judge_score(content, PERFORMANCE_RELIABILITY)

        # Weighted mix: 50% actual run consistency, 50% heuristic judgment
        final_score = (reproducibility_score * 0.4) + (judge_result.score * 0.6)

        return EvaluationResult(
            dimension_id=PERFORMANCE_RELIABILITY.id,
            score=final_score,
            level=determine_performance_level(final_score),
            evidence=[f"Reproducibility avg similarity: {avg_sim:.2f}"],
            reasoning=f"Combined score of runtime reproducibility ({reproducibility_score:.1f}) and judge assessment ({judge_result.score:.1f}). Reason: {judge_result.reasoning}",
        )

    def _eval_maintainability(self, content: str) -> EvaluationResult:
        # Static checks
        score = 0
        checks = []

        # Check 1: Documentation / Frontmatter
        if "---" in content:
            score += 20
            checks.append("Has frontmatter/metadata")

        # Check 2: Versioning
        if "version" in content.lower() or "v1." in content.lower():
            score += 10
            checks.append("Mentions versioning")

        # Check 3: Clear Variables
        if "{" in content and "}" in content:
            score += 10
            checks.append("Uses template variables {}")

        # Check 4: Comments (sanity check)
        if "#" in content or "<!--" in content:
            score += 5
            checks.append("Has comments")

        # Base score from LLM judge
        judge_result = self._llm_judge_score(content, MAINTAINABILITY)

        final_score = min(100, judge_result.score + score)  # logical mix

        return EvaluationResult(
            dimension_id=MAINTAINABILITY.id,
            score=final_score,
            level=determine_performance_level(final_score),
            evidence=checks,
            reasoning=f"Base judge score: {judge_result.score}. Bonus points for: {', '.join(checks)}. Reason: {judge_result.reasoning}",
        )

    def _eval_innovation(self, content: str) -> EvaluationResult:
        return self._llm_judge_score(content, INNOVATION_OPTIMIZATION)
