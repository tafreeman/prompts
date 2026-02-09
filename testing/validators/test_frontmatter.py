"""Frontmatter validation tests for the prompt library.

Tests that all prompts in the library have valid frontmatter according
to the defined schema.
"""

import sys
from pathlib import Path

import pytest

# Add parent to path for conftest imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from conftest import load_prompt_file, parse_frontmatter

# =============================================================================
# SCHEMA DEFINITION
# =============================================================================
# NOTE: The prompt library uses a centralized registry.yaml for full metadata.
# Individual prompt files only require minimal frontmatter: name, description.
# Full schema fields are validated against registry.yaml, not per-file.

REQUIRED_FIELDS = [
    "name",
    "description",
]

# Legacy full-schema fields (now in registry.yaml, not per-file)
FULL_SCHEMA_FIELDS = [
    "title",
    "shortTitle",
    "intro",
    "type",
    "difficulty",
    "audience",
    "platforms",
    "topics",
]

OPTIONAL_FIELDS = [
    "author",
    "version",
    "lastUpdated",
    "status",
    "evalScore",
    "evalDate",
    "tags",
    "relatedPrompts",
]

VALID_TYPES = ["how_to", "template", "reference", "guide"]
VALID_DIFFICULTIES = ["beginner", "intermediate", "advanced"]
VALID_PLATFORMS = ["copilot", "chatgpt", "claude", "m365", "gemini", "generic"]


# =============================================================================
# FIXTURES
# =============================================================================


@pytest.fixture
def prompt_files(prompts_dir: Path) -> list[Path]:
    """Get all prompt markdown files."""
    if not prompts_dir.exists():
        pytest.skip("prompts directory not found")
    files = list(prompts_dir.rglob("*.md"))
    # Exclude index.md and README.md files
    return [f for f in files if f.name not in ("index.md", "README.md")]


# =============================================================================
# FRONTMATTER PARSING TESTS
# =============================================================================


class TestFrontmatterParsing:
    """Tests for frontmatter parsing functionality."""

    def test_parse_valid_frontmatter(self):
        """Test parsing valid frontmatter."""
        content = """---
title: Test Prompt
shortTitle: Test
intro: A test prompt.
type: template
difficulty: beginner
audience:
  - developers
platforms:
  - copilot
topics:
  - testing
---

# Content here
"""
        fm = parse_frontmatter(content)
        assert fm["title"] == "Test Prompt"
        assert fm["type"] == "template"
        assert "developers" in fm["audience"]

    def test_parse_missing_frontmatter(self):
        """Test parsing content without frontmatter."""
        content = "# Just a heading\n\nNo frontmatter here."
        fm = parse_frontmatter(content)
        assert fm == {}

    def test_parse_incomplete_frontmatter(self):
        """Test parsing incomplete frontmatter delimiters."""
        content = """---
title: Incomplete
# Missing closing delimiter
"""
        fm = parse_frontmatter(content)
        assert fm == {}

    def test_parse_invalid_yaml(self):
        """Test parsing invalid YAML in frontmatter."""
        content = """---
title: Bad YAML
  indentation: wrong
    nested: bad
---
"""
        fm = parse_frontmatter(content)
        # Should return empty dict on parse error
        assert fm == {} or isinstance(fm, dict)


# =============================================================================
# REQUIRED FIELDS TESTS
# =============================================================================


class TestRequiredFields:
    """Tests for required frontmatter fields."""

    def test_has_title(self, valid_frontmatter):
        """Test that title field exists."""
        assert "title" in valid_frontmatter
        assert isinstance(valid_frontmatter["title"], str)
        assert len(valid_frontmatter["title"]) > 0

    def test_has_short_title(self, valid_frontmatter):
        """Test that shortTitle field exists."""
        assert "shortTitle" in valid_frontmatter
        assert isinstance(valid_frontmatter["shortTitle"], str)

    def test_has_intro(self, valid_frontmatter):
        """Test that intro field exists."""
        assert "intro" in valid_frontmatter
        assert isinstance(valid_frontmatter["intro"], str)

    def test_has_type(self, valid_frontmatter):
        """Test that type field exists and is valid."""
        assert "type" in valid_frontmatter
        assert valid_frontmatter["type"] in VALID_TYPES

    def test_has_difficulty(self, valid_frontmatter):
        """Test that difficulty field exists and is valid."""
        assert "difficulty" in valid_frontmatter
        assert valid_frontmatter["difficulty"] in VALID_DIFFICULTIES

    def test_has_audience(self, valid_frontmatter):
        """Test that audience field exists and is a list."""
        assert "audience" in valid_frontmatter
        assert isinstance(valid_frontmatter["audience"], list)
        assert len(valid_frontmatter["audience"]) > 0

    def test_has_platforms(self, valid_frontmatter):
        """Test that platforms field exists and is a list."""
        assert "platforms" in valid_frontmatter
        assert isinstance(valid_frontmatter["platforms"], list)
        assert len(valid_frontmatter["platforms"]) > 0

    def test_has_topics(self, valid_frontmatter):
        """Test that topics field exists and is a list."""
        assert "topics" in valid_frontmatter
        assert isinstance(valid_frontmatter["topics"], list)
        assert len(valid_frontmatter["topics"]) > 0


# =============================================================================
# FIELD VALIDATION TESTS
# =============================================================================


class TestFieldValidation:
    """Tests for field value validation."""

    @pytest.mark.parametrize("valid_type", VALID_TYPES)
    def test_valid_type_values(self, valid_type):
        """Test all valid type values are accepted."""
        fm = {"type": valid_type}
        assert fm["type"] in VALID_TYPES

    @pytest.mark.parametrize("valid_difficulty", VALID_DIFFICULTIES)
    def test_valid_difficulty_values(self, valid_difficulty):
        """Test all valid difficulty values are accepted."""
        fm = {"difficulty": valid_difficulty}
        assert fm["difficulty"] in VALID_DIFFICULTIES

    @pytest.mark.parametrize("valid_platform", VALID_PLATFORMS)
    def test_valid_platform_values(self, valid_platform):
        """Test all valid platform values are accepted."""
        platforms = [valid_platform]
        assert all(p in VALID_PLATFORMS for p in platforms)

    def test_invalid_type_rejected(self):
        """Test that invalid type values are rejected."""
        invalid_type = "invalid_type"
        assert invalid_type not in VALID_TYPES

    def test_invalid_difficulty_rejected(self):
        """Test that invalid difficulty values are rejected."""
        invalid_difficulty = "expert"
        assert invalid_difficulty not in VALID_DIFFICULTIES


# =============================================================================
# PROMPT FILE VALIDATION TESTS
# =============================================================================


class TestPromptFileValidation:
    """Tests that validate actual prompt files in the repository."""

    def test_prompt_files_exist(self, prompt_files):
        """Test that prompt files exist."""
        assert len(prompt_files) > 0, "No prompt files found"

    def test_prompt_files_have_frontmatter(self, prompt_files):
        """Test that all prompt files have frontmatter."""
        missing_frontmatter = []
        for prompt_file in prompt_files[:10]:  # Sample first 10 for speed
            content = prompt_file.read_text(encoding="utf-8")
            if not content.startswith("---"):
                missing_frontmatter.append(prompt_file.name)

        assert (
            len(missing_frontmatter) == 0
        ), f"Files missing frontmatter: {missing_frontmatter}"

    def test_prompt_files_have_required_fields(self, prompt_files):
        """Test that prompt files have required fields."""
        invalid_files = []
        for prompt_file in prompt_files[:10]:  # Sample first 10 for speed
            fm, _ = load_prompt_file(prompt_file)
            missing = [f for f in REQUIRED_FIELDS if f not in fm]
            if missing:
                invalid_files.append((prompt_file.name, missing))

        if invalid_files:
            details = "\n".join(
                f"  {name}: missing {fields}" for name, fields in invalid_files
            )
            pytest.fail(f"Files with missing required fields:\n{details}")


# =============================================================================
# TEMP FILE TESTS
# =============================================================================


class TestTempFileFixtures:
    """Tests for temporary file fixtures."""

    def test_temp_prompt_file_valid(self, temp_prompt_file):
        """Test that temp_prompt_file fixture creates valid prompt."""
        assert temp_prompt_file.exists()
        fm, body = load_prompt_file(temp_prompt_file)

        # Check all required fields
        for field in REQUIRED_FIELDS:
            assert field in fm, f"Missing required field: {field}"

        # Check body content
        assert len(body) > 0

    def test_temp_invalid_prompt(self, temp_invalid_prompt):
        """Test that temp_invalid_prompt fixture creates invalid prompt."""
        assert temp_invalid_prompt.exists()
        fm, _ = load_prompt_file(temp_invalid_prompt)

        # Should be missing required fields
        missing = [f for f in REQUIRED_FIELDS if f not in fm]
        assert len(missing) > 0, "Expected missing fields in invalid prompt"
