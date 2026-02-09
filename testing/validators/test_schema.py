"""Schema compliance tests for the prompt library.

Tests that prompts conform to the defined metadata schema and content
structure requirements.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

# Add parent to path for conftest imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from conftest import load_prompt_file

# =============================================================================
# SCHEMA DEFINITIONS
# =============================================================================

# Canonical schema for prompt frontmatter
PROMPT_SCHEMA = {
    "required": {
        "title": {"type": str, "min_length": 3, "max_length": 100},
        "shortTitle": {"type": str, "min_length": 2, "max_length": 30},
        "intro": {"type": str, "min_length": 10, "max_length": 500},
        "type": {"type": str, "enum": ["how_to", "template", "reference", "guide"]},
        "difficulty": {"type": str, "enum": ["beginner", "intermediate", "advanced"]},
        "audience": {"type": list, "min_items": 1},
        "platforms": {"type": list, "min_items": 1},
        "topics": {"type": list, "min_items": 1},
    },
    "optional": {
        "author": {"type": str},
        "version": {"type": str},
        "lastUpdated": {"type": str},
        "status": {"type": str, "enum": ["draft", "review", "published", "deprecated"]},
        "evalScore": {"type": (int, float)},
        "evalDate": {"type": str},
        "tags": {"type": list},
        "relatedPrompts": {"type": list},
    },
}

# Valid audience values
VALID_AUDIENCES = [
    "developers",
    "architects",
    "managers",
    "analysts",
    "writers",
    "designers",
    "data-scientists",
    "general",
]

# Valid topic values (extensible)
CORE_TOPICS = [
    "code-review",
    "documentation",
    "testing",
    "architecture",
    "security",
    "performance",
    "debugging",
    "refactoring",
    "general",
]


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================


def validate_field_type(value: Any, expected_type: type) -> bool:
    """Validate that a value matches the expected type."""
    if isinstance(expected_type, tuple):
        return isinstance(value, expected_type)
    return isinstance(value, expected_type)


def validate_field_length(value: str, min_len: int = 0, max_len: int = 10000) -> bool:
    """Validate string length constraints."""
    if not isinstance(value, str):
        return False
    return min_len <= len(value) <= max_len


def validate_enum(value: str, allowed_values: List[str]) -> bool:
    """Validate that value is in allowed enum values."""
    return value in allowed_values


def validate_list_items(items: list, min_items: int = 0) -> bool:
    """Validate list has minimum number of items."""
    if not isinstance(items, list):
        return False
    return len(items) >= min_items


def validate_frontmatter(fm: Dict[str, Any]) -> List[str]:
    """Validate frontmatter against schema.

    Returns list of validation errors (empty if valid).
    """
    errors = []

    # Check required fields
    for field, constraints in PROMPT_SCHEMA["required"].items():
        if field not in fm:
            errors.append(f"Missing required field: {field}")
            continue

        value = fm[field]

        # Type check
        if not validate_field_type(value, constraints["type"]):
            errors.append(
                f"Field '{field}' has wrong type: expected {constraints['type'].__name__}"
            )
            continue

        # String length check
        if constraints["type"] == str:
            min_len = constraints.get("min_length", 0)
            max_len = constraints.get("max_length", 10000)
            if not validate_field_length(value, min_len, max_len):
                errors.append(
                    f"Field '{field}' length out of range [{min_len}, {max_len}]"
                )

        # Enum check
        if "enum" in constraints:
            if not validate_enum(value, constraints["enum"]):
                errors.append(f"Field '{field}' has invalid value: {value}")

        # List minimum items check
        if constraints["type"] == list:
            min_items = constraints.get("min_items", 0)
            if not validate_list_items(value, min_items):
                errors.append(f"Field '{field}' needs at least {min_items} items")

    return errors


# =============================================================================
# SCHEMA VALIDATION TESTS
# =============================================================================


class TestSchemaStructure:
    """Tests for schema structure and definitions."""

    def test_schema_has_required_section(self):
        """Test that schema defines required fields."""
        assert "required" in PROMPT_SCHEMA
        assert len(PROMPT_SCHEMA["required"]) > 0

    def test_schema_has_optional_section(self):
        """Test that schema defines optional fields."""
        assert "optional" in PROMPT_SCHEMA

    def test_required_fields_have_types(self):
        """Test that all required fields have type definitions."""
        for field, constraints in PROMPT_SCHEMA["required"].items():
            assert "type" in constraints, f"Field '{field}' missing type definition"

    def test_enum_fields_have_values(self):
        """Test that enum fields have allowed values defined."""
        for section in ["required", "optional"]:
            for field, constraints in PROMPT_SCHEMA[section].items():
                if "enum" in constraints:
                    assert (
                        len(constraints["enum"]) > 0
                    ), f"Field '{field}' has empty enum"


# =============================================================================
# VALIDATION FUNCTION TESTS
# =============================================================================


class TestValidationFunctions:
    """Tests for validation helper functions."""

    def test_validate_field_type_string(self):
        """Test string type validation."""
        assert validate_field_type("test", str)
        assert not validate_field_type(123, str)
        assert not validate_field_type(["list"], str)

    def test_validate_field_type_list(self):
        """Test list type validation."""
        assert validate_field_type(["a", "b"], list)
        assert not validate_field_type("string", list)
        assert not validate_field_type({"dict": 1}, list)

    def test_validate_field_type_tuple(self):
        """Test tuple type validation (for int|float)."""
        assert validate_field_type(5, (int, float))
        assert validate_field_type(5.5, (int, float))
        assert not validate_field_type("5", (int, float))

    def test_validate_field_length(self):
        """Test string length validation."""
        assert validate_field_length("test", 1, 10)
        assert validate_field_length("a", 1, 1)
        assert not validate_field_length("", 1, 10)
        assert not validate_field_length("too long", 1, 5)

    def test_validate_enum(self):
        """Test enum validation."""
        allowed = ["a", "b", "c"]
        assert validate_enum("a", allowed)
        assert validate_enum("c", allowed)
        assert not validate_enum("d", allowed)

    def test_validate_list_items(self):
        """Test list minimum items validation."""
        assert validate_list_items(["a"], 1)
        assert validate_list_items(["a", "b"], 1)
        assert not validate_list_items([], 1)
        assert validate_list_items([], 0)


# =============================================================================
# FRONTMATTER VALIDATION TESTS
# =============================================================================


class TestFrontmatterValidation:
    """Tests for complete frontmatter validation."""

    def test_valid_frontmatter_passes(self, valid_frontmatter):
        """Test that valid frontmatter passes validation."""
        errors = validate_frontmatter(valid_frontmatter)
        assert len(errors) == 0, f"Unexpected errors: {errors}"

    def test_missing_required_field_fails(self):
        """Test that missing required field is detected."""
        incomplete = {
            "title": "Test",
            # Missing other required fields
        }
        errors = validate_frontmatter(incomplete)
        assert len(errors) > 0
        assert any("Missing required field" in e for e in errors)

    def test_wrong_type_fails(self):
        """Test that wrong field type is detected."""
        wrong_type = {
            "title": "Test",
            "shortTitle": "T",
            "intro": "Test intro here.",
            "type": "template",
            "difficulty": "beginner",
            "audience": "developers",  # Should be list
            "platforms": ["copilot"],
            "topics": ["testing"],
        }
        errors = validate_frontmatter(wrong_type)
        assert len(errors) > 0
        assert any("wrong type" in e for e in errors)

    def test_invalid_enum_fails(self):
        """Test that invalid enum value is detected."""
        invalid_enum = {
            "title": "Test Prompt",
            "shortTitle": "Test",
            "intro": "Test intro here.",
            "type": "invalid_type",  # Not in enum
            "difficulty": "beginner",
            "audience": ["developers"],
            "platforms": ["copilot"],
            "topics": ["testing"],
        }
        errors = validate_frontmatter(invalid_enum)
        assert len(errors) > 0
        assert any("invalid value" in e for e in errors)

    def test_empty_list_fails(self):
        """Test that empty required list is detected."""
        empty_list = {
            "title": "Test Prompt",
            "shortTitle": "Test",
            "intro": "Test intro here.",
            "type": "template",
            "difficulty": "beginner",
            "audience": [],  # Empty list
            "platforms": ["copilot"],
            "topics": ["testing"],
        }
        errors = validate_frontmatter(empty_list)
        assert len(errors) > 0
        assert any("at least" in e for e in errors)


# =============================================================================
# CONTENT STRUCTURE TESTS
# =============================================================================


class TestContentStructure:
    """Tests for prompt content structure requirements."""

    def test_prompt_has_heading(self, temp_prompt_file):
        """Test that prompt has at least one heading."""
        _, body = load_prompt_file(temp_prompt_file)
        assert "#" in body, "Prompt should have at least one heading"

    def test_prompt_body_not_empty(self, temp_prompt_file):
        """Test that prompt body is not empty."""
        _, body = load_prompt_file(temp_prompt_file)
        assert len(body.strip()) > 0, "Prompt body should not be empty"

    def test_prompt_reasonable_length(self, temp_prompt_file):
        """Test that prompt has reasonable content length."""
        _, body = load_prompt_file(temp_prompt_file)
        # Should be at least 50 chars but not excessively long
        assert (
            50 <= len(body) <= 50000
        ), f"Prompt body length {len(body)} outside reasonable range"


# =============================================================================
# SCHEMA EXPORT
# =============================================================================

# Export for use by other tools
__all__ = [
    "PROMPT_SCHEMA",
    "VALID_AUDIENCES",
    "CORE_TOPICS",
    "validate_frontmatter",
    "validate_field_type",
    "validate_field_length",
    "validate_enum",
    "validate_list_items",
]
