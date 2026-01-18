#!/usr/bin/env python3
"""
Reference Validator and Fixer for Prompt Library

This script:
1. Finds and fixes old archive path references (tools/archive -> _archive/tools)
2. Validates that all file/path references in markdown files point to existing files
"""
import re
from pathlib import Path
from typing import List, Tuple

# Mapping of old paths to new paths
PATH_REPLACEMENTS = {
                     "tools/archive/": "_archive/tools/",
                     "testing/archive/": "_archive/testing/",
                     "`tools/archive/`": "`_archive/tools/`",
                     "`testing/archive/`": "`_archive/testing/`",
                     "testing/archive/2025-12-04/": "_archive/testing/2025-12-04/",
                     "`testing/archive/2025-12-04/`": "`_archive/testing/2025-12-04/`",
                     }

# File extensions to check
EXTENSIONS = {".md", ".py", ".yaml", ".yml", ".json"}

# Directories to skip entirely
SKIP_DIRS = {"_archive", ".git", "node_modules", "__pycache__", ".venv", ".gemini"}

# Regex patterns to find file references in markdown
REFERENCE_PATTERNS = [
                      r'\[([^\]]+)\]\(([^)]+)\)',  # [text](path)
    r'`([^`]+\.(md|py|yaml|yml|json))`',  # `path.ext`
]


def find_and_fix_old_paths(root_dir: str, dry_run: bool = True) -> List[Tuple[Path, List[str]]]:
    """Find and optionally fix invalid archive references."""
    root = Path(root_dir)
    files_with_issues = []

    for filepath in root.rglob("*"):
        if filepath.is_dir():
            continue
        if any(skip in filepath.parts for skip in SKIP_DIRS):
            continue
        if filepath.suffix not in EXTENSIONS:
            continue

        try:
            content = filepath.read_text(encoding='utf-8')
            issues = []

            for old, new in PATH_REPLACEMENTS.items():
                if old in content:
                    issues.append(f"  Replace: '{old}' -> '{new}'")
                    content = content.replace(old, new)

            if issues:
                files_with_issues.append((filepath, issues))
                if not dry_run:
                    filepath.write_text(content, encoding='utf-8')
                    print(f"✅ Fixed: {filepath}")
                else:
                    print(f"⚠️  Would fix: {filepath}")
                    for issue in issues:
                        print(issue)

        except Exception as e:
            print(f"❌ Error: {filepath}: {e}")

    return files_with_issues


def validate_references(root_dir: str) -> List[Tuple[Path, str, str]]:
    """Validate that all file references in markdown point to existing files."""
    root = Path(root_dir).resolve()
    broken_refs = []

    for filepath in root.rglob("*.md"):
        if any(skip in filepath.parts for skip in SKIP_DIRS):
            continue

        try:
            content = filepath.read_text(encoding='utf-8')
            file_dir = filepath.parent

            # Find markdown links [text](path)
            for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', content):
                link_text, link_path = match.groups()

                # Skip external URLs and anchors
                if link_path.startswith(('http://', 'https://', '#', 'mailto:')):
                    continue

                # Remove anchor from path
                clean_path = link_path.split('#')[0]
                if not clean_path:
                    continue

                # Resolve relative path
                if clean_path.startswith('/'):
                    target = root / clean_path.lstrip('/')
                else:
                    target = (file_dir / clean_path).resolve()

                # Check if target exists
                if not target.exists():
                    broken_refs.append((filepath, link_path, link_text))

            # Find backtick file references `path/to/file.ext`
            for match in re.finditer(r'`([^`]*(?:\.md|\.py|\.yaml|\.yml|\.json))`', content):
                ref_path = match.group(1)

                # Skip if it looks like code, not a path
                if ' ' in ref_path or ref_path.startswith(('$', '-', '{')):
                    continue

                # Resolve path
                if ref_path.startswith('/'):
                    target = root / ref_path.lstrip('/')
                else:
                    target = (file_dir / ref_path).resolve()

                # Also try from repo root
                root_target = root / ref_path

                if not target.exists() and not root_target.exists():
                    # Check if it's an _archive reference that exists
                    if not (root / ref_path.replace('tools/archive/', '_archive/tools/')).exists():
                        if not (root / ref_path.replace('testing/archive/', '_archive/testing/')).exists():
                            broken_refs.append((filepath, ref_path, "backtick re"))

        except Exception as e:
            print(f"❌ Error reading {filepath}: {e}")

    return broken_refs


def main():
    import sys

    print("=" * 60)
    print("REFERENCE VALIDATOR AND FIXER")
    print("=" * 60)

    dry_run = "--fix" not in sys.argv
    validate_only = "--validate" in sys.argv

    if validate_only:
        print("\n📋 VALIDATING REFERENCES...\n")
        broken = validate_references(".")

        if broken:
            print(f"\n❌ Found {len(broken)} broken references:\n")
            for filepath, ref, text in broken:
                print(f"  {filepath}")
                print(f"    -> {ref} ({text})")
        else:
            print("✅ All references valid!")
        return

    print("\n📋 CHECKING FOR OLD ARCHIVE PATHS...\n")
    if dry_run:
        print("(DRY RUN - Use --fix to apply changes)\n")

    issues = find_and_fix_old_paths(".", dry_run=dry_run)

    print(f"\n{'='*60}")
    print(f"Files with old paths: {len(issues)}")

    if not dry_run or not issues:
        print("\n📋 VALIDATING ALL REFERENCES...\n")
        broken = validate_references(".")

        if broken:
            print(f"\n⚠️  Found {len(broken)} broken references:\n")
            for filepath, ref, text in broken[:20]:  # Show first 20
                print(f"  {filepath.relative_to(Path('.').resolve())}")
                print(f"    -> {ref}")
            if len(broken) > 20:
                print(f"  ... and {len(broken) - 20} more")
        else:
            print("✅ All references valid!")


if __name__ == "__main__":
    main()
