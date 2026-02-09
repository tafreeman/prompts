#!/usr/bin/env python3
"""Fix MD060: Add spaces around table pipes."""

import re
from pathlib import Path


def fix_table_spacing(content: str) -> tuple:
    """Fix table pipe spacing."""
    changes = 0

    # Pattern: Fix separator rows like |-------|
    pattern = re.compile(r"\|(-+)\|")
    new_content, count = pattern.subn(r"| \1 |", content)
    changes += count

    return new_content, changes


def main():
    repo_root = Path(__file__).parent.parent.parent
    md_files = list(repo_root.glob("**/*.md"))
    excluded = {".venv", "node_modules", ".git", "__pycache__", "_archive"}
    md_files = [f for f in md_files if not any(e in f.parts for e in excluded)]

    total_changes = 0
    files_changed = 0

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
            new_content, changes = fix_table_spacing(content)

            if changes > 0:
                md_file.write_text(new_content, encoding="utf-8")
                total_changes += changes
                files_changed += 1
                print(f"✓ {md_file.relative_to(repo_root)}: {changes} fixes")
        except Exception as e:
            print(f"✗ {md_file.relative_to(repo_root)}: Error - {e}")

    print(f"\n{'='*60}")
    print(f"Total: {total_changes} table spacing issues fixed in {files_changed} files")
    return 0


if __name__ == "__main__":
    exit(main())
