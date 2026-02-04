#!/usr/bin/env python3
"""Validate prompt Markdown files.

This validator checks:
- minimal YAML frontmatter (as used by `prompts/templates/prompt-template.md`)
- presence of required H2 sections (varies slightly by content type)

VS Code task wiring executes this script via `tools/validate_prompts.py`.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

# Accept 'name' as required in minimal frontmatter
REQUIRED_FRONTMATTER = ["name"]
DESCRIPTION_FIELDS = ["description"]

# Valid values for optional enumerated frontmatter fields
VALID_PATTERNS = ["react", "cove", "reflexion", "rag"]
VALID_RESPONSE_FORMATS = ["text", "json_object", "json_schema"]
VALID_DIFFICULTIES = ["beginner", "intermediate", "advanced"]
VALID_TYPES = ["how_to", "reference", "template", "guide"]

# File types that are reference guides (not prompt templates) - exempt from Prompt/Variables requirements
REFERENCE_TYPES = ["reference", "guide", "tutorial"]
# Files that are examples/outputs (not prompts) - exempt from all section requirements
EXAMPLE_FILES = ["example-research-output.md"]


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.search(r"^\s*---\r?\n(.*?)\r?\n---", content, re.DOTALL | re.MULTILINE)
    if match:
        try:
            fm = yaml.safe_load(match.group(1))
            if isinstance(fm, dict):
                return fm
            # Malformed frontmatter (not a mapping)
            return {}
        except yaml.YAMLError:
            return {}
    return {}


def extract_sections(content: str) -> list:
    """Extract H2 section headers from markdown content."""
    return re.findall(r"^## (.+)$", content, re.MULTILINE)


def validate_file(path: Path) -> list:
    """Validate a single prompt file.

    Returns list of issues.
    """
    issues = []
    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Cannot read file: {e}"]

    # Skip example output files
    if path.name in EXAMPLE_FILES:
        return []

    # Check frontmatter
    fm = extract_frontmatter(content)
    if isinstance(fm, list):
        issues.append(
            "Invalid frontmatter: YAML frontmatter is a list, not a dict. "
            "Check for duplicate or malformed frontmatter blocks."
        )
        return issues
    for field in REQUIRED_FRONTMATTER:
        if field not in fm:
            issues.append(f"Missing frontmatter: {field}")
    # Check for description OR intro field
    if not any(field in fm for field in DESCRIPTION_FIELDS):
        issues.append("Missing frontmatter: description")

    # Validate optional enumerated fields if present
    if "pattern" in fm:
        pattern = fm["pattern"]
        if pattern and pattern.lower() not in VALID_PATTERNS:
            issues.append(
                f"Invalid frontmatter: pattern '{pattern}' must be one of: {', '.join(VALID_PATTERNS)}"
            )

    if "response_format" in fm:
        resp_fmt = fm["response_format"]
        if resp_fmt and resp_fmt.lower() not in VALID_RESPONSE_FORMATS:
            issues.append(
                f"Invalid frontmatter: response_format '{resp_fmt}' must be one of: {', '.join(VALID_RESPONSE_FORMATS)}"
            )

    if "difficulty" in fm:
        diff = fm["difficulty"]
        if diff and diff.lower() not in VALID_DIFFICULTIES:
            issues.append(
                f"Invalid frontmatter: difficulty '{diff}' must be one of: {', '.join(VALID_DIFFICULTIES)}"
            )

    # Determine required sections based on file type
    file_type_raw = fm.get("type")
    if file_type_raw is None:
        # Default to 'how_to' for backward compatibility, but surface the missing field
        issues.append("Missing frontmatter: type (defaulting to 'how_to')")
        file_type = "how_to"
    elif isinstance(file_type_raw, str):
        file_type = file_type_raw.lower()
    else:
        issues.append("Invalid frontmatter: type must be a string")
        file_type = "how_to"
    is_reference = isinstance(file_type, str) and file_type in REFERENCE_TYPES

    # Reference guides don't need Prompt/Variables sections
    required_sections = ["Description"]
    if not is_reference:
        required_sections.extend(["Prompt", "Variables"])

    # Check sections
    sections = extract_sections(content)
    sections_lower = [s.lower() for s in sections]

    # Accept various example section names
    example_variants = [
        "example",
        "example usage",
        "usage",
        "example visualization",
        "example visualization (mermaid)",
        "comparative examples",
        "quick reference",
    ]

    for section in required_sections:
        if section not in sections and section.lower() not in sections_lower:
            issues.append(f"Missing section: {section}")

    # Check for example section (accept many variants)
    if not any(variant in sections_lower for variant in example_variants):
        issues.append("Missing section: Example")

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate prompt Markdown files")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all prompt files under prompts/ (default behavior)",
    )
    parser.add_argument(
        "--path",
        type=str,
        default="prompts",
        help="Root path to validate (default: prompts)",
    )
    args = parser.parse_args(argv)

    root = Path(args.path)
    errors = 0
    for path in root.rglob("*.md"):
        if path.name in ["index.md", "README.md"]:
            continue

        issues = validate_file(path)
        if issues:
            print(f"\n{path}:")
            for issue in issues:
                print(f"  - {issue}")
            errors += 1

    print(f"\n{'=' * 50}")
    print(f"Files with issues: {errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
