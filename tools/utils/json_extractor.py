"""
JSON Extraction Utilities
=========================

Robust JSON extraction from LLM responses with multiple fallback strategies.
This module consolidates JSON parsing logic that was duplicated across:
- local_model.py
- prompteval/__main__.py
- prompteval/core.py
- tools_ecosystem_evaluator.py

Usage:
    from tools.utils.json_extractor import extract_json, extract_first_json_object

    response = llm.generate(...)
    json_data = extract_json(response)
    if json_data is None:
        print("Failed to parse JSON")

Author: Prompts Library Team
Version: 1.0.0
"""

import json
import re
from typing import Any, Dict, List, Optional


def extract_json(text: str) -> Optional[Dict[str, Any]]:
    """Extract JSON from LLM response with multiple fallback strategies.

    Handles common LLM output issues:
    - JSON wrapped in markdown code blocks
    - Trailing commas
    - Single quotes instead of double quotes
    - Unquoted keys
    - JSON embedded in conversational text

    Args:
        text: Raw LLM response text

    Returns:
        Parsed JSON dictionary, or None if extraction fails
    """
    if not text or not text.strip():
        return None

    original_text = text
    text = text.strip()

    # Strategy 1: Remove markdown code blocks
    text = _strip_markdown_fences(text)

    # Strategy 2: Try to unescape quoted JSON strings
    text = _unescape_json_string(text)

    # Strategy 3: Find and parse JSON object
    json_result = _extract_json_object(text)
    if json_result is not None:
        return json_result

    # Strategy 4: Try with cleanups
    json_result = _try_parse_with_cleanups(text)
    if json_result is not None:
        return json_result

    # Strategy 5: Extract with regex for specific patterns
    json_result = _extract_with_regex(original_text)
    if json_result is not None:
        return json_result

    return None


def extract_first_json_object(text: str) -> Optional[Dict[str, Any]]:
    """Extract the first JSON object from text using brace counting.

    This is useful when the model outputs JSON mixed with other text.

    Args:
        text: Raw text that may contain JSON

    Returns:
        First valid JSON object found, or None
    """
    text = _strip_markdown_fences(text)
    return _extract_json_object(text)


def extract_json_array(text: str) -> Optional[List[Any]]:
    """Extract a JSON array from text.

    Args:
        text: Raw text that may contain a JSON array

    Returns:
        Parsed JSON array, or None
    """
    if not text:
        return None

    text = _strip_markdown_fences(text)

    # Find first [ and matching ]
    start = text.find("[")
    if start == -1:
        return None

    depth = 0
    in_string = False
    escape = False

    for i in range(start, len(text)):
        char = text[i]

        if escape:
            escape = False
            continue

        if char == "\\":
            escape = True
            continue

        if char == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                json_str = text[start : i + 1]
                return _try_parse(json_str)

    return None


def extract_scores_from_text(text: str) -> Dict[str, float]:
    """Extract numeric scores from semi-structured text.

    Handles patterns like:
    - "clarity: 8.5"
    - "clarity": 8.5
    - clarity = 8.5
    - **8.5** for clarity

    Args:
        text: Text containing score data

    Returns:
        Dictionary of extracted scores
    """
    scores = {}

    # Common score field names
    fields = [
        "clarity",
        "specificity",
        "actionability",
        "structure",
        "completeness",
        "safety",
        "coherence",
        "effectiveness",
        "relevance",
        "reusability",
        "simplicity",
        "examples",
        "overall",
        "score",
        "total",
    ]

    for field in fields:
        # Try multiple patterns
        patterns = [
            rf'["\']?{field}["\']?\s*[:=]\s*(\d+(?:\.\d+)?)',  # field: 8.5
            rf"{field}\s+(?:is|score|rating)?\s*[:=]?\s*(\d+(?:\.\d+)?)",  # field is 8.5
            rf"\*\*(\d+(?:\.\d+)?)\*\*\s*(?:for\s+)?{field}",  # **8.5** for field
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    scores[field] = float(match.group(1))
                    break
                except ValueError:
                    continue

    return scores


# =============================================================================
# INTERNAL HELPERS
# =============================================================================


def _strip_markdown_fences(text: str) -> str:
    """Remove markdown code fences from text."""
    # Pattern for ```json ... ``` or ``` ... ```
    if "```json" in text:
        match = re.search(r"```json\s*([\s\S]*?)\s*```", text)
        if match:
            return match.group(1)

    if "```" in text:
        match = re.search(r"```\s*([\s\S]*?)\s*```", text)
        if match:
            return match.group(1)

    return text


def _unescape_json_string(text: str) -> str:
    """Unescape a potentially quoted/escaped JSON string."""
    stripped = text.strip()

    # If wrapped in quotes, try to unquote
    if (stripped.startswith('"') and stripped.endswith('"')) or (
        stripped.startswith("'") and stripped.endswith("'")
    ):
        try:
            unquoted = json.loads(stripped)
            if isinstance(unquoted, str) and "{" in unquoted:
                return unquoted
        except Exception:
            pass

    # Handle escaped quotes
    if '\\"' in text or "\\n" in text:
        try:
            unescaped = text.encode().decode("unicode_escape")
            if "{" in unescaped:
                return unescaped
        except Exception:
            pass

    return text


def _extract_json_object(text: str) -> Optional[Dict[str, Any]]:
    """Extract JSON object using brace counting."""
    start = text.find("{")
    if start == -1:
        return None

    depth = 0
    in_string = False
    escape = False

    for i in range(start, len(text)):
        char = text[i]

        if escape:
            escape = False
            continue

        if char == "\\":
            escape = True
            continue

        if char == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                json_str = text[start : i + 1]
                result = _try_parse(json_str)
                if result is not None:
                    return result
                # Try with cleanups
                result = _try_parse_with_cleanups(json_str)
                if result is not None:
                    return result
                # Keep looking for next object
                return _extract_json_object(text[i + 1 :])

    return None


def _try_parse(json_str: str) -> Optional[Dict[str, Any]]:
    """Attempt to parse JSON string."""
    try:
        result = json.loads(json_str)
        if isinstance(result, dict):
            return result
    except json.JSONDecodeError:
        pass
    return None


def _try_parse_with_cleanups(json_str: str) -> Optional[Dict[str, Any]]:
    """Try parsing with various cleanup transformations."""
    cleanups = [
        lambda s: s,  # Try as-is first
        lambda s: re.sub(r",\s*([}\]])", r"\1", s),  # Remove trailing commas
        lambda s: s.replace("'", '"'),  # Single to double quotes
        lambda s: re.sub(r"(\w+):", r'"\1":', s),  # Quote unquoted keys
        lambda s: " ".join(s.split()),  # Collapse whitespace
        lambda s: s.replace("\n", " ").replace("\r", ""),  # Remove newlines
    ]

    for cleanup in cleanups:
        try:
            cleaned = cleanup(json_str)
            result = json.loads(cleaned)
            if isinstance(result, dict):
                return result
        except Exception:
            continue

    # Try combining cleanups
    try:
        cleaned = json_str
        for cleanup in cleanups[1:]:  # Skip identity
            cleaned = cleanup(cleaned)
        result = json.loads(cleaned)
        if isinstance(result, dict):
            return result
    except Exception:
        pass

    return None


def _extract_with_regex(text: str) -> Optional[Dict[str, Any]]:
    """Last-resort regex-based extraction for common patterns."""
    # Try to find JSON with "scores" key
    patterns = [
        r'\{[^{}]*"scores"[^{}]*\{[^{}]*\}[^{}]*\}',
        r'\{[^{}]*"score"[^{}]*\}',
        r'\{[^{}]*"overall"[^{}]*\}',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result = _try_parse_with_cleanups(match.group())
            if result is not None:
                return result

    return None


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "extract_json",
    "extract_first_json_object",
    "extract_json_array",
    "extract_scores_from_text",
]
