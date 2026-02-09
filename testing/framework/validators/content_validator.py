"""Content Validator for Prompt Templates.

Validates content quality of prompts, including:
- Writing quality and clarity
- Appropriate content length
- Best practices adherence
- Content completeness
"""

import logging
import re
from typing import Any, Dict, List, Optional

from .base_validator import BaseValidator

logger = logging.getLogger(__name__)


class ContentValidator(BaseValidator):
    """Validates content quality of prompt templates.

    Checks for:
    - Writing quality (grammar indicators, clarity)
    - Appropriate length and structure
    - Best practices adherence
    - Required content sections
    - Placeholder completeness
    """

    # Recommended sections for a complete prompt
    RECOMMENDED_SECTIONS = [
        "description",
        "purpose",
        "prompt",
        "example",
        "usage",
        "tips",
    ]

    # Minimum content lengths (in words)
    MIN_LENGTHS = {
        "title": 3,
        "description": 10,
        "prompt": 20,
        "example": 15,
    }

    # Maximum recommended lengths
    MAX_LENGTHS = {
        "title": 15,
        "description": 200,
        "prompt": 2000,
    }

    # Patterns indicating incomplete content
    PLACEHOLDER_PATTERNS = [
        r"\[TODO\]",
        r"\[PLACEHOLDER\]",
        r"\[INSERT.*?\]",
        r"\[ADD.*?\]",
        r"\[YOUR.*?\]",
        r"XXX",
        r"FIXME",
        r"TBD",
        r"lorem ipsum",
    ]

    # Words/phrases indicating low-quality content
    WEAK_LANGUAGE = [
        "stuff",
        "things",
        "whatever",
        "etc.",
        "and so on",
        "basically",
        "actually",
        "really",
        "very",
        "just",
    ]

    # Strong action verbs for prompts
    STRONG_VERBS = [
        "analyze",
        "create",
        "design",
        "develop",
        "evaluate",
        "generate",
        "implement",
        "review",
        "transform",
        "validate",
        "summarize",
        "extract",
        "identify",
        "compare",
        "explain",
    ]

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize content validator with configuration."""
        super().__init__(config)
        self.strict_mode = config.get("strict_mode", False) if config else False
        self.min_quality_score = config.get("min_quality_score", 0.6) if config else 0.6

    async def validate(self, output: Any, expected: Optional[Any] = None) -> bool:
        """Validate content quality of prompt.

        Args:
            output: The prompt content to validate
            expected: Optional expected content requirements

        Returns:
            bool: True if content quality is acceptable, False otherwise
        """
        self.clear_messages()

        if not output:
            self.add_error("No content provided for content validation")
            return False

        content = str(output)
        is_valid = True

        # Check for placeholders
        placeholders = self._find_placeholders(content)
        if placeholders:
            for placeholder in placeholders:
                self.add_error(
                    f"Incomplete content: placeholder found - '{placeholder}'"
                )
            is_valid = False

        # Validate content sections
        sections_valid = self._validate_sections(content)
        if not sections_valid and self.strict_mode:
            is_valid = False

        # Check content length
        length_valid = self._validate_length(content)
        if not length_valid and self.strict_mode:
            is_valid = False

        # Check writing quality
        quality_score = self._calculate_quality_score(content)
        if quality_score < self.min_quality_score:
            self.add_warning(
                f"Content quality score ({quality_score:.2f}) below threshold ({self.min_quality_score})"
            )
            if self.strict_mode:
                is_valid = False

        # Check for best practices
        self._check_best_practices(content)

        # Validate against expected requirements
        if expected and isinstance(expected, dict):
            if not self._validate_expected(content, expected):
                is_valid = False

        return is_valid

    def _find_placeholders(self, content: str) -> List[str]:
        """Find incomplete placeholders in content."""
        placeholders = []

        for pattern in self.PLACEHOLDER_PATTERNS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            placeholders.extend(matches)

        return placeholders

    def _validate_sections(self, content: str) -> bool:
        """Validate presence of recommended sections."""
        is_valid = True
        content_lower = content.lower()

        found_sections = []
        missing_sections = []

        for section in self.RECOMMENDED_SECTIONS:
            # Check for section heading or mention
            pattern = rf"##?\s*{section}|{section}\s*:"
            if re.search(pattern, content_lower):
                found_sections.append(section)
            else:
                missing_sections.append(section)

        # Must have at least prompt section
        if "prompt" not in found_sections:
            self.add_error("Missing required 'Prompt' section")
            is_valid = False

        # Warn about missing recommended sections
        critical_sections = ["description", "example"]
        for section in critical_sections:
            if section in missing_sections:
                self.add_warning(f"Missing recommended section: '{section}'")

        return is_valid

    def _validate_length(self, content: str) -> bool:
        """Validate content length is appropriate."""
        is_valid = True

        # Extract different parts
        body = self._extract_body(content)
        word_count = len(body.split())

        # Check minimum length
        if word_count < 50:
            self.add_warning(
                f"Content may be too short ({word_count} words). Consider adding more detail."
            )

        # Check maximum length
        if word_count > 3000:
            self.add_warning(
                f"Content may be too long ({word_count} words). Consider breaking into sections."
            )

        # Check prompt section length specifically
        prompt_match = re.search(
            r"##?\s*Prompt\s*\n+```[\w]*\n(.*?)```", content, re.DOTALL | re.IGNORECASE
        )
        if prompt_match:
            prompt_words = len(prompt_match.group(1).split())
            if prompt_words < self.MIN_LENGTHS["prompt"]:
                self.add_warning(
                    f"Prompt section may be too short ({prompt_words} words)"
                )
            elif prompt_words > self.MAX_LENGTHS["prompt"]:
                self.add_warning(
                    f"Prompt section may be too long ({prompt_words} words)"
                )

        return is_valid

    def _extract_body(self, content: str) -> str:
        """Extract the body after frontmatter."""
        match = re.match(r"^---\s*\n.*?\n---\s*\n", content, re.DOTALL)
        if match:
            return content[match.end() :]
        return content

    def _calculate_quality_score(self, content: str) -> float:
        """Calculate a quality score for the content."""
        score = 0.7  # Start with baseline
        content_lower = content.lower()

        # Penalize weak language
        weak_count = sum(1 for word in self.WEAK_LANGUAGE if word in content_lower)
        score -= min(0.2, weak_count * 0.03)

        # Reward strong action verbs
        strong_count = sum(1 for verb in self.STRONG_VERBS if verb in content_lower)
        score += min(0.2, strong_count * 0.04)

        # Check for structure
        has_headings = bool(re.search(r"^##?\s+\w+", content, re.MULTILINE))
        has_lists = bool(re.search(r"^\s*[-*]\s+", content, re.MULTILINE))
        has_code = bool(re.search(r"```", content))

        if has_headings:
            score += 0.05
        if has_lists:
            score += 0.05
        if has_code:
            score += 0.05

        # Check for examples
        if "example" in content_lower and (has_code or re.search(r">\s+", content)):
            score += 0.1

        # Check sentence variety (rough heuristic)
        sentences = re.split(r"[.!?]+", content)
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(
                sentences
            )
            if 10 <= avg_sentence_length <= 25:
                score += 0.05
            elif avg_sentence_length < 5 or avg_sentence_length > 40:
                score -= 0.05

        return max(0.0, min(1.0, score))

    def _check_best_practices(self, content: str) -> None:
        """Check adherence to prompt engineering best practices."""
        content_lower = content.lower()

        # Check for role/persona definition
        role_patterns = ["you are", "act as", "role:", "persona:", "as a"]
        has_role = any(p in content_lower for p in role_patterns)
        if not has_role:
            self.add_warning("Consider adding a role/persona definition for the AI")

        # Check for output format specification
        format_patterns = [
            "output format",
            "response format",
            "return as",
            "format:",
            "respond in",
        ]
        has_format = any(p in content_lower for p in format_patterns)
        if not has_format:
            self.add_warning("Consider specifying the expected output format")

        # Check for constraints/boundaries
        constraint_patterns = [
            "do not",
            "don't",
            "avoid",
            "must",
            "should",
            "constraint",
            "limit",
        ]
        has_constraints = any(p in content_lower for p in constraint_patterns)
        if not has_constraints:
            self.add_warning(
                "Consider adding constraints or boundaries for the response"
            )

        # Check for examples
        if "example" not in content_lower and "```" not in content:
            self.add_warning("Consider adding examples to improve prompt clarity")

    def _validate_expected(self, content: str, expected: Dict) -> bool:
        """Validate content against expected requirements."""
        is_valid = True
        content_lower = content.lower()

        # Check required keywords
        required_keywords = expected.get("required_keywords", [])
        for keyword in required_keywords:
            if keyword.lower() not in content_lower:
                self.add_error(f"Missing required keyword: '{keyword}'")
                is_valid = False

        # Check forbidden patterns
        forbidden = expected.get("forbidden_patterns", [])
        for pattern in forbidden:
            if re.search(pattern, content, re.IGNORECASE):
                self.add_error(f"Content contains forbidden pattern: '{pattern}'")
                is_valid = False

        # Check minimum sections
        required_sections = expected.get("required_sections", [])
        for section in required_sections:
            if not re.search(rf"##?\s*{section}", content, re.IGNORECASE):
                self.add_error(f"Missing required section: '{section}'")
                is_valid = False

        return is_valid

    def get_content_analysis(self, content: str) -> Dict[str, Any]:
        """Get a comprehensive content analysis.

        Returns a dictionary with content properties and metrics.
        """
        body = self._extract_body(content)

        # Calculate various metrics
        word_count = len(body.split())
        sentence_count = len(re.split(r"[.!?]+", body))
        paragraph_count = len(re.split(r"\n\n+", body))

        # Count weak/strong language
        content_lower = content.lower()
        weak_count = sum(1 for word in self.WEAK_LANGUAGE if word in content_lower)
        strong_count = sum(1 for verb in self.STRONG_VERBS if verb in content_lower)

        # Find sections
        sections = re.findall(r"^##?\s+(.+)$", content, re.MULTILINE)

        # Check for various elements
        has_role = any(p in content_lower for p in ["you are", "act as", "role:"])
        has_format = any(
            p in content_lower for p in ["output format", "response format"]
        )
        has_examples = "example" in content_lower
        has_constraints = any(p in content_lower for p in ["do not", "avoid", "must"])

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "paragraph_count": paragraph_count,
            "quality_score": self._calculate_quality_score(content),
            "weak_language_count": weak_count,
            "strong_verb_count": strong_count,
            "sections": sections,
            "placeholders_found": self._find_placeholders(content),
            "has_role_definition": has_role,
            "has_format_specification": has_format,
            "has_examples": has_examples,
            "has_constraints": has_constraints,
            "best_practices_adherence": {
                "role": has_role,
                "format": has_format,
                "examples": has_examples,
                "constraints": has_constraints,
            },
        }
