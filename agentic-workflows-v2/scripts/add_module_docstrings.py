"""Utility: add simple module docstrings to Python files missing them.

Usage:
    python scripts/add_module_docstrings.py --root src/agentic_v2 --preview

This script is conservative: it only prepends a short auto-generated
docstring if the file does not already start with a triple-quoted string.
It writes files in-place unless --preview is set.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

MODULE_HEADER = (
    '"""Auto-generated module docstring.\n\n'
    "This file was updated by scripts/add_module_docstrings.py to ensure a\n"
    "module-level docstring exists for documentation generation and code\n"
    "readability. Replace this text with a more descriptive module docstring.\n"
    '"""\n\n'
)


def has_module_docstring(text: str) -> bool:
    """Return True if file text starts with a triple-quoted string."""
    return bool(re.match(r"^\s*(?:\'\'\'|\"\"\")", text))


def process_file(path: Path, preview: bool = True) -> bool:
    txt = path.read_text(encoding="utf-8")
    if has_module_docstring(txt):
        return False
    new_txt = MODULE_HEADER + txt
    if preview:
        print(f"Would add docstring to: {path}")
    else:
        path.write_text(new_txt, encoding="utf-8")
        print(f"Wrote docstring to: {path}")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", default="src/agentic_v2")
    p.add_argument("--preview", action="store_true", default=False)
    args = p.parse_args()

    root = Path(args.root)
    py_files = list(root.rglob("*.py"))
    changed = 0
    for f in py_files:
        if process_file(f, preview=args.preview):
            changed += 1

    print(f"Processed {len(py_files)} files, would change {changed} files.")


if __name__ == "__main__":
    main()
