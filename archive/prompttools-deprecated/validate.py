"""
Prompt validation - structure, frontmatter, and required sections.

This module provides static analysis of prompt files without calling an LLM.
It checks for mandatory YAML frontmatter fields, required Markdown headers,
and common formatting issues.
"""

import fnmatch
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import (
    PREFERRED_FRONTMATTER,
    PREFERRED_SECTIONS,
    REQUIRED_FRONTMATTER,
    REQUIRED_SECTIONS,
    SKIP_PATTERNS,
)
from .parse import extract_body, extract_sections, parse_frontmatter

# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class Issue:
    """A validation issue."""

    level: str  # "error", "warning", "info"
    message: str
    field: Optional[str] = None
    line: Optional[int] = None
    suggestion: Optional[str] = None

    def __str__(self) -> str:
        prefix = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}.get(self.level, "•")
        return f"{prefix} {self.message}"


@dataclass
class ValidationResult:
    """Complete validation result for a single prompt file.

    Attributes:
        file: Path to the validated file.
        issues: List of Issue objects (errors, warnings, info).
        frontmatter: Parsed YAML frontmatter (if any).
        sections: List of detected Markdown section headers.
    """

    file: str
    issues: List[Issue] = field(default_factory=list)
    frontmatter: Dict[str, Any] = field(default_factory=dict)
    sections: List[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Determines if the file meets mandatory requirements (no errors)."""
        return not any(i.level == "error" for i in self.issues)

    @property
    def error_count(self) -> int:
        """Count of blocking structural errors."""
        return sum(1 for i in self.issues if i.level == "error")

    @property
    def warning_count(self) -> int:
        """Count of non-blocking quality warnings."""
        return sum(1 for i in self.issues if i.level == "warning")

    def add_error(self, message: str, **kwargs) -> None:
        self.issues.append(Issue("error", message, **kwargs))

    def add_warning(self, message: str, **kwargs) -> None:
        self.issues.append(Issue("warning", message, **kwargs))

    def add_info(self, message: str, **kwargs) -> None:
        self.issues.append(Issue("info", message, **kwargs))


# =============================================================================
# VALIDATION LOGIC
# =============================================================================


def validate(path: str | Path) -> ValidationResult:
    """Validate a prompt file's structure.

    Checks:
    - Required frontmatter fields
    - Required sections
    - Basic structure issues

    Args:
        path: Path to the prompt file

    Returns:
        ValidationResult with any issues found
    """
    path = Path(path)
    result = ValidationResult(file=str(path))

    # Check file exists
    if not path.exists():
        result.add_error(f"File not found: {path}")
        return result

    # Read content
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        result.add_error(f"Cannot read file: {e}")
        return result

    # Parse frontmatter
    fm = parse_frontmatter(content)
    result.frontmatter = fm

    if not fm:
        result.add_error("No frontmatter found", field="frontmatter")
    else:
        # Check required fields
        for field_name in REQUIRED_FRONTMATTER:
            if field_name not in fm:
                result.add_error(
                    f"Missing required field: {field_name}",
                    field=field_name,
                    suggestion=f"Add '{field_name}:' to frontmatter",
                )

        # Check preferred fields
        for field_name in PREFERRED_FRONTMATTER:
            if field_name not in fm:
                result.add_warning(
                    f"Missing recommended field: {field_name}", field=field_name
                )

        # Check for description or intro
        if not fm.get("description") and not fm.get("intro"):
            result.add_warning(
                "Missing description or intro field", field="description"
            )

    # Parse sections
    sections = extract_sections(content)
    result.sections = sections
    sections_lower = [s.lower() for s in sections]

    # Determine file type (reference guides have different requirements)
    file_type = str(fm.get("type", "")).lower()
    is_reference = file_type in ["reference", "guide", "tutorial"]

    # Check required sections
    for section in REQUIRED_SECTIONS:
        if section.lower() not in sections_lower:
            if is_reference and section.lower() in ["prompt", "variables"]:
                # Reference docs don't need these
                continue
            result.add_error(
                f"Missing required section: {section}",
                field=section,
                suggestion=f"Add '## {section}' section",
            )

    # Check preferred sections
    for section in PREFERRED_SECTIONS:
        if section.lower() not in sections_lower:
            # Accept variations for Example section
            if section.lower() == "example":
                example_variants = ["example", "examples", "usage", "example usage"]
                if any(v in sections_lower for v in example_variants):
                    continue
            result.add_warning(f"Missing recommended section: {section}", field=section)

    # Check body content
    body = extract_body(content)
    if len(body) < 50:
        result.add_warning("Body content is very short (< 50 chars)")

    # Check for common issues
    _check_common_issues(content, result)

    return result


def _check_common_issues(content: str, result: ValidationResult) -> None:
    """Check for common quality issues."""

    # Empty prompt section
    import re

    prompt_match = re.search(r"##\s+Prompt\s*\n+```", content, re.IGNORECASE)
    if prompt_match:
        # Find the code block content
        block_match = re.search(
            r"##\s+Prompt\s*\n+```[^\n]*\n(.*?)```", content, re.IGNORECASE | re.DOTALL
        )
        if block_match and len(block_match.group(1).strip()) < 10:
            result.add_warning("Prompt section appears to be empty or very short")

    # Missing variable definitions
    vars_section = re.search(
        r"##\s+Variables?\s*\n(.*?)(?=##|\Z)", content, re.IGNORECASE | re.DOTALL
    )
    if vars_section and "{{" in content:
        # Count template variables
        template_vars = set(re.findall(r"\{\{(\w+)\}\}", content))
        if template_vars and "|" not in vars_section.group(1):
            result.add_info(
                f"Template variables {template_vars} found but no variable table"
            )

    # Very long lines (readability)
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        if len(line) > 200 and not line.startswith("|"):  # Skip table rows
            result.add_info(f"Line {i} is very long ({len(line)} chars)", line=i)
            break  # Only report first occurrence


def validate_batch(
    paths: List[Path] | Path,
    recursive: bool = True,
) -> Dict[str, ValidationResult]:
    """Validate multiple prompt files.

    Args:
        paths: List of file paths, or a directory to scan
        recursive: If paths is a directory, whether to recurse

    Returns:
        Dict mapping file paths to their ValidationResults
    """
    if isinstance(paths, Path):
        if paths.is_dir():
            pattern = "**/*.md" if recursive else "*.md"
            file_list = list(paths.glob(pattern))
        else:
            file_list = [paths]
    else:
        file_list = [Path(p) for p in paths]

    # Filter out skipped files
    filtered = []
    for f in file_list:
        skip = False
        for pattern in SKIP_PATTERNS:
            if fnmatch.fnmatch(str(f), pattern) or fnmatch.fnmatch(f.name, pattern):
                skip = True
                break
        if not skip:
            filtered.append(f)

    return {str(f): validate(f) for f in filtered}


def print_validation_summary(results: Dict[str, ValidationResult]) -> None:
    """Print a summary of validation results."""
    total = len(results)
    valid = sum(1 for r in results.values() if r.is_valid)
    errors = sum(r.error_count for r in results.values())
    warnings = sum(r.warning_count for r in results.values())

    print(f"\n{'='*50}")
    print(f"Validation Summary: {valid}/{total} files valid")
    print(f"  Errors: {errors}")
    print(f"  Warnings: {warnings}")
    print(f"{'='*50}")

    # Show files with errors
    if errors > 0:
        print("\nFiles with errors:")
        for path, result in results.items():
            if result.error_count > 0:
                print(f"\n  {path}:")
                for issue in result.issues:
                    if issue.level == "error":
                        print(f"    {issue}")
