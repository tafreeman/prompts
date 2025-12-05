#!/usr/bin/env python3
"""Validate prompt files for required sections and frontmatter."""

import re
import sys
from pathlib import Path
import yaml

REQUIRED_SECTIONS = ['Description', 'Prompt', 'Variables', 'Example']
REQUIRED_FRONTMATTER = ['title', 'description']

def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.search(r'^\s*---\r?\n(.*?)\r?\n---', content, re.DOTALL | re.MULTILINE)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return {}
    return {}

def extract_sections(content: str) -> list:
    """Extract H2 section headers from markdown content."""
    return re.findall(r'^## (.+)$', content, re.MULTILINE)

def validate_file(path: Path) -> list:
    """Validate a single prompt file. Returns list of issues."""
    issues = []
    try:
        content = path.read_text(encoding='utf-8')
    except Exception as e:
        return [f"Cannot read file: {e}"]
    
    # Check frontmatter
    fm = extract_frontmatter(content)
    for field in REQUIRED_FRONTMATTER:
        if field not in fm:
            issues.append(f"Missing frontmatter: {field}")
    
    # Check sections
    sections = extract_sections(content)
    sections_lower = [s.lower() for s in sections]
    for section in REQUIRED_SECTIONS:
        if section not in sections and section.lower() not in sections_lower:
            issues.append(f"Missing section: {section}")
    
    return issues

def main():
    errors = 0
    for path in Path("prompts").rglob("*.md"):
        if path.name in ['index.md', 'README.md']:
            continue
        
        issues = validate_file(path)
        if issues:
            print(f"\n{path}:")
            for issue in issues:
                print(f"  - {issue}")
            errors += 1
    
    print(f"\n{'='*50}")
    print(f"Files with issues: {errors}")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
