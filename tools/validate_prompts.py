#!/usr/bin/env python3
"""Validate prompt files for required sections and frontmatter."""

import re
import sys
from pathlib import Path
import yaml

# Required sections for standard prompt templates
REQUIRED_SECTIONS = ['Description', 'Prompt', 'Variables', 'Example']
# Accept 'intro' as equivalent to 'description' in frontmatter
REQUIRED_FRONTMATTER = ['title']
DESCRIPTION_FIELDS = ['description', 'intro']  # Either field satisfies the requirement

# File types that are reference guides (not prompt templates) - exempt from Prompt/Variables requirements
REFERENCE_TYPES = ['reference', 'guide', 'tutorial']
# Files that are examples/outputs (not prompts) - exempt from all section requirements
EXAMPLE_FILES = ['example-research-output.md']

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
    
    # Skip example output files
    if path.name in EXAMPLE_FILES:
        return []
    
    # Check frontmatter
    fm = extract_frontmatter(content)
    for field in REQUIRED_FRONTMATTER:
        if field not in fm:
            issues.append(f"Missing frontmatter: {field}")
    
    # Check for description OR intro field
    if not any(field in fm for field in DESCRIPTION_FIELDS):
        issues.append(f"Missing frontmatter: description or intro")
    
    # Determine required sections based on file type
    file_type = fm.get('type', 'how_to').lower()
    is_reference = file_type in REFERENCE_TYPES
    
    # Reference guides don't need Prompt/Variables sections
    required_sections = ['Description']
    if not is_reference:
        required_sections.extend(['Prompt', 'Variables'])
    
    # Check sections
    sections = extract_sections(content)
    sections_lower = [s.lower() for s in sections]
    
    # Accept various example section names
    example_variants = ['example', 'example usage', 'usage', 'example visualization', 'example visualization (mermaid)', 
                       'comparative examples', 'quick reference']
    
    for section in required_sections:
        if section not in sections and section.lower() not in sections_lower:
            issues.append(f"Missing section: {section}")
    
    # Check for example section (accept many variants)
    if not any(variant in sections_lower for variant in example_variants):
        issues.append(f"Missing section: Example")
    
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
