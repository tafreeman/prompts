"""
Shared pytest fixtures for the prompts repository testing suite.

This module provides common fixtures for:
- Prompt file discovery and loading
- Temporary file management
- Mock configurations
- Common test data
"""

import os
import sys
import tempfile
from pathlib import Path
from typing import Generator, List, Dict, Any

import pytest
import yaml

# Ensure repository root is in path for imports
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT))


# =============================================================================
# PATH FIXTURES
# =============================================================================

@pytest.fixture
def repo_root() -> Path:
    """Return the repository root directory."""
    return REPO_ROOT


@pytest.fixture
def prompts_dir(repo_root: Path) -> Path:
    """Return the prompts directory."""
    return repo_root / "prompts"


@pytest.fixture
def testing_dir(repo_root: Path) -> Path:
    """Return the testing directory."""
    return repo_root / "testing"


@pytest.fixture
def tools_dir(repo_root: Path) -> Path:
    """Return the tools directory."""
    return repo_root / "tools"


# =============================================================================
# PROMPT DISCOVERY FIXTURES
# =============================================================================

@pytest.fixture
def all_prompt_files(prompts_dir: Path) -> List[Path]:
    """Discover all .md prompt files in the prompts directory."""
    if not prompts_dir.exists():
        return []
    return list(prompts_dir.rglob("*.md"))


@pytest.fixture
def prompt_categories(prompts_dir: Path) -> List[str]:
    """Return list of prompt category directories."""
    if not prompts_dir.exists():
        return []
    return [d.name for d in prompts_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]


# =============================================================================
# TEMPORARY FILE FIXTURES
# =============================================================================

@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory that is cleaned up after the test."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_prompt_file(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a temporary prompt file with valid frontmatter."""
    prompt_path = temp_dir / "test-prompt.md"
    content = """---
title: Test Prompt
shortTitle: Test
intro: A test prompt for unit testing.
type: template
difficulty: beginner
audience:
  - developers
platforms:
  - copilot
topics:
  - testing
author: Test Author
version: "1.0"
---

# Test Prompt

This is a test prompt for unit testing purposes.

## Instructions

1. Do something
2. Do something else

## Output Format

Return a JSON response.
"""
    prompt_path.write_text(content, encoding="utf-8")
    yield prompt_path


@pytest.fixture
def temp_invalid_prompt(temp_dir: Path) -> Generator[Path, None, None]:
    """Create a temporary prompt file with invalid frontmatter (missing required fields)."""
    prompt_path = temp_dir / "invalid-prompt.md"
    content = """---
title: Invalid Prompt
# Missing required fields: shortTitle, intro, type, etc.
---

# Invalid Prompt

This prompt is missing required frontmatter fields.
"""
    prompt_path.write_text(content, encoding="utf-8")
    yield prompt_path


# =============================================================================
# FRONTMATTER FIXTURES
# =============================================================================

@pytest.fixture
def valid_frontmatter() -> Dict[str, Any]:
    """Return valid frontmatter data."""
    return {
        "title": "Test Prompt",
        "shortTitle": "Test",
        "intro": "A test prompt for validation.",
        "type": "template",
        "difficulty": "beginner",
        "audience": ["developers"],
        "platforms": ["copilot"],
        "topics": ["testing"],
        "author": "Test Author",
        "version": "1.0"
    }


@pytest.fixture
def minimal_frontmatter() -> Dict[str, Any]:
    """Return minimal valid frontmatter with only required fields."""
    return {
        "title": "Minimal Prompt",
        "shortTitle": "Min",
        "intro": "Minimal test.",
        "type": "template",
        "difficulty": "beginner",
        "audience": ["developers"],
        "platforms": ["copilot"],
        "topics": ["general"]
    }


# =============================================================================
# MOCK FIXTURES
# =============================================================================

@pytest.fixture
def mock_eval_result() -> Dict[str, Any]:
    """Return a mock evaluation result."""
    return {
        "model": "openai/gpt-4o-mini",
        "run_number": 1,
        "scores": {
            "clarity": 8.0,
            "specificity": 7.5,
            "actionability": 8.0,
            "structure": 7.5,
            "completeness": 8.0,
            "factuality": 9.0,
            "consistency": 8.0,
            "safety": 9.0
        },
        "overall_score": 8.125,
        "grade": "B",
        "passed": True,
        "pass_reason": "All criteria met"
    }


@pytest.fixture
def mock_cross_validation_report() -> Dict[str, Any]:
    """Return a mock cross-validation report."""
    return {
        "prompt_file": "test-prompt.md",
        "total_runs": 4,
        "models_used": ["openai/gpt-4o", "openai/gpt-4o-mini"],
        "score_range": {"min": 7.5, "max": 8.5},
        "variance": 0.5,
        "consensus_passed": True,
        "final_grade": "B"
    }


# =============================================================================
# SCHEMA FIXTURES
# =============================================================================

@pytest.fixture
def frontmatter_schema() -> Dict[str, Any]:
    """Return the expected frontmatter schema."""
    return {
        "required": [
            "title",
            "shortTitle", 
            "intro",
            "type",
            "difficulty",
            "audience",
            "platforms",
            "topics"
        ],
        "optional": [
            "author",
            "version",
            "lastUpdated",
            "status",
            "evalScore",
            "evalDate"
        ],
        "type_values": ["how_to", "template", "reference", "guide"],
        "difficulty_values": ["beginner", "intermediate", "advanced"],
        "platform_values": ["copilot", "chatgpt", "claude", "m365", "gemini"]
    }


# =============================================================================
# HELPER FUNCTIONS (available to tests via import)
# =============================================================================

def parse_frontmatter(content: str) -> Dict[str, Any]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def load_prompt_file(path: Path) -> tuple[Dict[str, Any], str]:
    """Load a prompt file and return (frontmatter, body) tuple."""
    content = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(content)
    
    # Extract body after frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        body = parts[2].strip() if len(parts) >= 3 else ""
    else:
        body = content
    
    return frontmatter, body
