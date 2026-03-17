"""Replace bare print() calls with structured logging in production code.

Usage:
    python scripts/fix-print-to-logging.py [--dry-run]

Only targets agentic_v2/ source (not tests, not tools/).
Adds `import logging` and `logger = logging.getLogger(__name__)` if missing.
Converts print(x) -> logger.info(x), print(f"...") -> logger.info("...").

Manual review recommended after running — some prints (CLI output, code_execution
sandbox stdout) are intentional.
"""

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "agentic-workflows-v2" / "agentic_v2"
SKIP_DIRS = {"__pycache__", ".venv", "tests"}

# Files where print() is intentional (CLI output, sandbox execution)
SKIP_FILES = {
    "cli/main.py",
    "tools/builtin/code_execution.py",
}


def should_skip(path: pathlib.Path) -> bool:
    rel = path.relative_to(SOURCE_DIR)
    if str(rel).replace("\\", "/") in SKIP_FILES:
        return True
    return any(part in SKIP_DIRS for part in path.parts)


def has_logging_import(text: str) -> bool:
    return bool(re.search(r"^import logging|^from logging import", text, re.MULTILINE))


def has_logger_def(text: str) -> bool:
    return bool(re.search(r"^logger\s*=\s*logging\.getLogger", text, re.MULTILINE))


def add_logging_boilerplate(text: str) -> str:
    """Add import logging and logger definition after the last top-level import."""
    lines = text.split("\n")
    last_import_idx = 0
    for i, line in enumerate(lines):
        if re.match(r"^(import |from )", line):
            last_import_idx = i

    additions = []
    if not has_logging_import(text):
        additions.append("import logging")
    if not has_logger_def(text):
        additions.append("logger = logging.getLogger(__name__)")

    if additions:
        insert_at = last_import_idx + 1
        lines[insert_at:insert_at] = [""] + additions + [""]

    return "\n".join(lines)


def convert_prints(text: str) -> str:
    """Convert print(...) to logger.info(...)."""
    # Simple print(x) -> logger.info(x)
    return re.sub(r"(\s*)print\(", r"\1logger.info(", text)


def fix_file(path: pathlib.Path, dry_run: bool) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")

    if not re.search(r"^\s*print\(", text, re.MULTILINE):
        return False

    new_text = convert_prints(text)
    new_text = add_logging_boilerplate(new_text)

    if new_text != text:
        if not dry_run:
            path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    modified = []
    for path in SOURCE_DIR.rglob("*.py"):
        if should_skip(path):
            continue
        if fix_file(path, args.dry_run):
            modified.append(path.relative_to(ROOT))

    if modified:
        verb = "Would fix" if args.dry_run else "Fixed"
        print(f"{verb} {len(modified)} file(s):")
        for p in sorted(modified):
            print(f"  {p}")
        print("\nWARNING: Review changes manually -- some print() calls may be intentional.")
    else:
        print("No bare print() calls found in production code.")


if __name__ == "__main__":
    main()
