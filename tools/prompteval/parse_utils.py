"""
Parsing utilities for JSON, YAML, and Markdown extraction.

This module provides parsing functions previously in prompttools.parse.
Consolidated here as part of the tools/ unification.
"""

import re
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# =============================================================================
# RESULT CLASSES (migrated from prompttools.evaluate)
# =============================================================================

@dataclass
class EvalResult:
    """Result from evaluating a single prompt."""
    file: str
    score: float
    grade: str
    passed: bool
    criteria: Dict[str, float] = field(default_factory=dict)
    improvements: List[str] = field(default_factory=list)
    model: str = ""
    method: str = ""
    tier: int = 1
    duration: float = 0.0
    error: Optional[str] = None
    
    @property
    def is_error(self) -> bool:
        return self.error is not None


@dataclass
class BatchResult:
    """Result from evaluating multiple prompts."""
    results: List["EvalResult"] = field(default_factory=list)
    total: int = 0
    passed: int = 0
    failed: int = 0
    errors: int = 0
    avg_score: float = 0.0
    duration: float = 0.0
    
    def summary(self) -> str:
        return f"{self.passed}/{self.total} passed ({self.avg_score:.1f} avg)"


# =============================================================================
# GRADE CONVERSION
# =============================================================================

def get_grade(score: float) -> str:
    """Convert score to letter grade.

    Supports both 0..10 and 0..100 scales.
    """
    try:
        s = float(score)
    except Exception:
        return "F"

    # If it looks like a 0..10 rubric score, convert to percent.
    pct = (s / 10.0) * 100.0 if 0.0 <= s <= 10.0 else s

    if pct >= 90:
        return "A"
    if pct >= 80:
        return "B"
    if pct >= 70:
        return "C"
    if pct >= 60:
        return "D"
    return "F"

# Alias for backward compatibility
_get_grade = get_grade


# =============================================================================
# YAML FRONTMATTER
# =============================================================================

def parse_frontmatter(content: str) -> Dict[str, Any]:
    """
    Extract YAML frontmatter from markdown content.
    
    Args:
        content: Full markdown content
        
    Returns:
        Dict of frontmatter fields, empty dict if none found
    """
    match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    
    try:
        import yaml
        return yaml.safe_load(match.group(1)) or {}
    except Exception:
        # Fallback: simple key: value parsing
        result = {}
        for line in match.group(1).split('\n'):
            if ':' in line:
                key, _, value = line.partition(':')
                result[key.strip()] = value.strip().strip('"\'')
        return result


def extract_body(content: str) -> str:
    """
    Extract body content after frontmatter.
    
    Args:
        content: Full markdown content
        
    Returns:
        Body content without frontmatter
    """
    body = re.sub(r'^---\s*\n.*?\n---\s*\n?', '', content, flags=re.DOTALL)
    return body.strip()


# =============================================================================
# MARKDOWN SECTIONS
# =============================================================================

def extract_sections(content: str) -> List[str]:
    """
    Extract H2 section headers from markdown.
    
    Args:
        content: Markdown content
        
    Returns:
        List of section names (without ##)
    """
    return re.findall(r'^##\s+(.+)$', content, re.MULTILINE)


def get_section_content(content: str, section_name: str) -> Optional[str]:
    """
    Get content of a specific section.
    
    Args:
        content: Markdown content
        section_name: Name of section to extract
        
    Returns:
        Section content, or None if not found
    """
    pattern = rf'^##\s+{re.escape(section_name)}\s*\n(.*?)(?=^##\s+|\Z)'
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else None


# =============================================================================
# JSON EXTRACTION
# =============================================================================

def extract_json(text: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON from text with multiple fallback strategies.
    
    Handles:
    - Clean JSON
    - JSON wrapped in markdown code blocks
    - JSON with trailing commas
    - JSON mixed with other text
    
    Args:
        text: Text potentially containing JSON
        
    Returns:
        Parsed JSON dict, or None if extraction fails
    """
    if not text:
        return None
    
    # Strategy 1: Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Strategy 2: Extract from markdown code block
    code_block = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.DOTALL)
    if code_block:
        try:
            return json.loads(code_block.group(1))
        except json.JSONDecodeError:
            pass
    
    # Strategy 3: Find JSON object by brace matching
    json_obj = _extract_by_braces(text)
    if json_obj:
        try:
            return json.loads(json_obj)
        except json.JSONDecodeError:
            # Try fixing common issues
            fixed = _fix_json(json_obj)
            try:
                return json.loads(fixed)
            except json.JSONDecodeError:
                pass
    
    # Strategy 4: Try parsing just the first line as JSON
    first_line = text.strip().split('\n')[0]
    try:
        return json.loads(first_line)
    except json.JSONDecodeError:
        pass
    
    return None


def extract_json_array(text: str) -> Optional[List[Any]]:
    """
    Extract a JSON array from text.
    
    Args:
        text: Text potentially containing JSON array
        
    Returns:
        Parsed list, or None if extraction fails
    """
    if not text:
        return None
    
    start = text.find('[')
    if start == -1:
        return None
    
    depth = 0
    for i, char in enumerate(text[start:], start):
        if char == '[':
            depth += 1
        elif char == ']':
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[start:i+1])
                except json.JSONDecodeError:
                    return None
    
    return None


def _extract_by_braces(text: str) -> Optional[str]:
    """Extract JSON object by matching braces."""
    start = text.find('{')
    if start == -1:
        return None
    
    depth = 0
    in_string = False
    escape = False
    
    for i, char in enumerate(text[start:], start):
        if escape:
            escape = False
            continue
        if char == '\\':
            escape = True
            continue
        if char == '"' and not escape:
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    
    return None


def _fix_json(json_str: str) -> str:
    """Attempt to fix common JSON issues."""
    # Remove trailing commas
    fixed = re.sub(r',\s*([}\]])', r'\1', json_str)
    # Fix single quotes
    fixed = fixed.replace("'", '"')
    # Remove comments
    fixed = re.sub(r'//.*$', '', fixed, flags=re.MULTILINE)
    return fixed


# =============================================================================
# SCORE EXTRACTION
# =============================================================================

def extract_score(text: str) -> Optional[float]:
    """
    Extract a numeric score from text.
    
    Looks for patterns like:
    - "score": 85
    - Score: 7.5/10
    - 85/100
    - **Score**: 8
    
    Args:
        text: Text containing a score
        
    Returns:
        Score as float (0-100 scale), or None if not found
    """
    # Try JSON first
    data = extract_json(text)
    if data and isinstance(data, dict):
        for key in ['score', 'overall_score', 'total_score', 'rating']:
            if key in data:
                val = data[key]
                if isinstance(val, (int, float)):
                    return val * 10 if val <= 10 else val
    
    # Pattern: score of X or X/100
    patterns = [
        r'(?:score|rating)[:\s]+(\d+(?:\.\d+)?)\s*(?:/\s*100)?',
        r'(\d+(?:\.\d+)?)\s*/\s*100',
        r'(\d+(?:\.\d+)?)\s*/\s*10',
        r'\*\*(?:score|rating)\*\*[:\s]+(\d+(?:\.\d+)?)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            score = float(match.group(1))
            if '/10' in pattern or score <= 10:
                score *= 10
            return min(100, max(0, score))
    
    return None


def extract_criteria_scores(text: str) -> Dict[str, float]:
    """
    Extract individual criteria scores from evaluation response.
    
    Args:
        text: Evaluation response text
        
    Returns:
        Dict mapping criteria names to scores
    """
    # Try JSON first
    data = extract_json(text)
    if data and isinstance(data, dict):
        for key in ['criteria', 'scores', 'dimensions']:
            if key in data and isinstance(data[key], dict):
                return {k: float(v) for k, v in data[key].items() 
                        if isinstance(v, (int, float))}
        
        criteria = {}
        for key, value in data.items():
            if isinstance(value, (int, float)) and key not in ['score', 'overall_score']:
                criteria[key] = float(value)
        if criteria:
            return criteria
    
    # Fallback: regex patterns
    scores = {}
    pattern = r'(?:^|\n)\s*[-*]?\s*\**(\w+(?:\s+\w+)?)\**\s*:\s*(\d+(?:\.\d+)?)'
    for match in re.finditer(pattern, text, re.IGNORECASE):
        name = match.group(1).lower().strip()
        score = float(match.group(2))
        if score <= 10:
            score *= 10
        scores[name] = score
    
    return scores
