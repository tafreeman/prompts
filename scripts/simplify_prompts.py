#!/usr/bin/env python3
"""
Stream S Simplification Script - Removes changelog sections and deprecated fields.
Part of the prompt library simplification effort (ANALYSIS_TODO.md Stream S).
"""

import re
import sys
from pathlib import Path
from typing import Tuple

# Configuration
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
GET_STARTED_DIR = Path(__file__).parent.parent / "get-started"
CONCEPTS_DIR = Path(__file__).parent.parent / "concepts"


def remove_changelog_section(content: str) -> Tuple[str, bool]:
    """
    Remove ## Changelog section and everything after it.
    Returns (modified_content, was_changed).
    """
    # Match ## Changelog (with optional leading spaces) and everything after
    patterns = [
        r'\n## Changelog\s*\n.*$',           # Standard ## Changelog
        r'\n### Changelog\s*\n.*$',          # ### Changelog variant
        r'\n# Changelog\s*\n.*$',            # # Changelog variant
    ]
    
    original = content
    for pattern in patterns:
        content = re.sub(pattern, '\n', content, flags=re.DOTALL)
    
    # Clean up trailing whitespace
    content = content.rstrip() + '\n'
    
    return content, content != original


def remove_deprecated_fields(content: str) -> Tuple[str, bool]:
    """
    Remove deprecated frontmatter fields: estimatedTime, technique.
    Returns (modified_content, was_changed).
    """
    original = content
    
    # Remove technique: field line (with any value)
    content = re.sub(r'^technique:\s*"[^"]*"\s*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^technique:\s*[^\n]*\n', '', content, flags=re.MULTILINE)
    
    # Remove estimatedTime: field line (with any value)
    content = re.sub(r'^estimatedTime:\s*"[^"]*"\s*\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^estimatedTime:\s*[^\n]*\n', '', content, flags=re.MULTILINE)
    
    return content, content != original


def process_file_s1(filepath: Path, dry_run: bool = False) -> bool:
    """Process a single file for S1, removing changelog. Returns True if changed."""
    try:
        content = filepath.read_text(encoding='utf-8')
        new_content, changed = remove_changelog_section(content)
        
        if changed and not dry_run:
            filepath.write_text(new_content, encoding='utf-8')
            print(f"  ✓ Changelog removed: {filepath}")
        elif changed:
            print(f"  [DRY-RUN] Would remove changelog: {filepath}")
        
        return changed
    except Exception as e:
        print(f"  ✗ Error processing {filepath}: {e}")
        return False


def process_file_s2(filepath: Path, dry_run: bool = False) -> bool:
    """Process a single file for S2, removing deprecated fields. Returns True if changed."""
    try:
        content = filepath.read_text(encoding='utf-8')
        new_content, changed = remove_deprecated_fields(content)
        
        if changed and not dry_run:
            filepath.write_text(new_content, encoding='utf-8')
            print(f"  ✓ Deprecated fields removed: {filepath}")
        elif changed:
            print(f"  [DRY-RUN] Would remove deprecated fields: {filepath}")
        
        return changed
    except Exception as e:
        print(f"  ✗ Error processing {filepath}: {e}")
        return False


def run_s1(dry_run: bool = False):
    """Run S1: Remove Changelog Sections."""
    print("=" * 60)
    print("Stream S1: Remove Changelog Sections")
    print("=" * 60)
    
    if dry_run:
        print("DRY RUN MODE - No files will be modified\n")
    
    # Find all markdown files in prompts/
    md_files = list(PROMPTS_DIR.rglob("*.md"))
    
    print(f"Found {len(md_files)} markdown files to process.\n")
    
    changed_count = 0
    for filepath in sorted(md_files):
        if process_file_s1(filepath, dry_run):
            changed_count += 1
    
    print("\n" + "=" * 60)
    print(f"S1 Results: {changed_count}/{len(md_files)} files {'would be ' if dry_run else ''}modified")
    print("=" * 60)


def run_s2(dry_run: bool = False):
    """Run S2: Remove deprecated fields from frontmatter."""
    print("\n" + "=" * 60)
    print("Stream S2: Remove Deprecated Fields (estimatedTime, technique)")
    print("=" * 60)
    
    if dry_run:
        print("DRY RUN MODE - No files will be modified\n")
    
    # Find all markdown files across all content directories
    md_files = []
    for dir_path in [PROMPTS_DIR, GET_STARTED_DIR, CONCEPTS_DIR]:
        if dir_path.exists():
            md_files.extend(dir_path.rglob("*.md"))
    
    print(f"Found {len(md_files)} markdown files to process.\n")
    
    changed_count = 0
    for filepath in sorted(md_files):
        if process_file_s2(filepath, dry_run):
            changed_count += 1
    
    print("\n" + "=" * 60)
    print(f"S2 Results: {changed_count}/{len(md_files)} files {'would be ' if dry_run else ''}modified")
    print("=" * 60)


def main():
    """Main entry point."""
    dry_run = '--dry-run' in sys.argv
    task = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 'all'
    
    if task in ['s1', 'all']:
        run_s1(dry_run)
    
    if task in ['s2', 'all']:
        run_s2(dry_run)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
