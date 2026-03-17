"""Add missing __init__.py files to Python package directories.

Usage:
    python scripts/fix-missing-init.py [--dry-run]

Scans agentic-workflows-v2/agentic_v2/ and tools/src/ for directories
that contain .py files but lack __init__.py. Creates empty __init__.py
files where needed.
"""

import argparse
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {"__pycache__", ".venv", ".venv314", "node_modules", ".git", "storybook-static"}

SCAN_DIRS = [
    ROOT / "agentic-workflows-v2" / "agentic_v2",
    ROOT / "tools" / "src",
    ROOT / "agentic-v2-eval" / "agentic_v2_eval",
]


def should_skip(path: pathlib.Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    created = []
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for dirpath in sorted(scan_dir.rglob("*")):
            if not dirpath.is_dir():
                continue
            if should_skip(dirpath):
                continue

            # Check if directory contains .py files
            py_files = list(dirpath.glob("*.py"))
            init_file = dirpath / "__init__.py"

            if py_files and not init_file.exists():
                if not args.dry_run:
                    init_file.write_text("")
                created.append(init_file.relative_to(ROOT))

    if created:
        verb = "Would create" if args.dry_run else "Created"
        print(f"{verb} {len(created)} __init__.py file(s):")
        for p in sorted(created):
            print(f"  {p}")
    else:
        print("All Python package directories have __init__.py.")


if __name__ == "__main__":
    main()
