"""Fix stale counts in CLAUDE.md by scanning actual codebase.

Usage:
    python scripts/fix-claudemd-counts.py [--dry-run]

Scans for actual workflow definitions, persona files, tool modules,
and source line counts, then updates CLAUDE.md to match reality.
"""

import argparse
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
CLAUDE_MD = ROOT / "CLAUDE.md"

PROMPTS_DIR = ROOT / "agentic-workflows-v2" / "agentic_v2" / "prompts"
WORKFLOWS_DIR = ROOT / "agentic-workflows-v2" / "agentic_v2" / "workflows" / "definitions"
TOOLS_DIR = ROOT / "agentic-workflows-v2" / "agentic_v2" / "tools" / "builtin"
SOURCE_DIR = ROOT / "agentic-workflows-v2" / "agentic_v2"


def count_files(directory: pathlib.Path, ext: str) -> int:
    """Count files with given extension, excluding __init__.py."""
    if not directory.exists():
        return 0
    return len([
        f for f in directory.glob(f"*{ext}")
        if f.name != "__init__.py" and f.name != "__pycache__"
    ])


def count_source_lines(directory: pathlib.Path) -> int:
    """Count total lines in .py files under directory."""
    if not directory.exists():
        return 0
    total = 0
    for f in directory.rglob("*.py"):
        if "__pycache__" in f.parts or ".venv" in f.parts:
            continue
        try:
            total += len(f.read_text(encoding="utf-8", errors="replace").splitlines())
        except OSError:
            continue
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not CLAUDE_MD.exists():
        print(f"Not found: {CLAUDE_MD}")
        return

    text = CLAUDE_MD.read_text(encoding="utf-8")

    # Count actuals
    persona_count = count_files(PROMPTS_DIR, ".md")
    workflow_count = count_files(WORKFLOWS_DIR, ".yaml")
    tool_count = count_files(TOOLS_DIR, ".py")
    source_lines = count_source_lines(SOURCE_DIR)
    source_k = round(source_lines / 100) * 100  # Round to nearest 100

    print(f"Actual counts:")
    print(f"  Personas:   {persona_count} .md files")
    print(f"  Workflows:  {workflow_count} .yaml files")
    print(f"  Tools:      {tool_count} .py modules")
    print(f"  Source:     ~{source_lines:,} lines (~{source_k:,})")

    replacements = []

    # Fix persona count: "24 agent persona definitions"
    old = re.search(r"(\d+) agent persona definitions", text)
    if old and int(old.group(1)) != persona_count:
        replacements.append((
            old.group(0),
            f"{persona_count} agent persona definitions",
            f"personas: {old.group(1)} -> {persona_count}",
        ))

    # Fix workflow count: "12 YAML workflow definitions"
    old = re.search(r"(\d+) YAML workflow definitions", text)
    if old and int(old.group(1)) != workflow_count:
        replacements.append((
            old.group(0),
            f"{workflow_count} YAML workflow definitions",
            f"workflows: {old.group(1)} -> {workflow_count}",
        ))

    # Fix tool count: "11 built-in tool modules"
    old = re.search(r"(\d+) built-in tool modules", text)
    if old and int(old.group(1)) != tool_count:
        replacements.append((
            old.group(0),
            f"{tool_count} built-in tool modules",
            f"tools: {old.group(1)} -> {tool_count}",
        ))

    # Fix source line count: "~30,600 lines" or similar
    old = re.search(r"~[\d,]+ lines", text)
    if old:
        old_num = int(old.group(0).replace("~", "").replace(",", "").replace(" lines", ""))
        if abs(old_num - source_lines) > 1000:  # Only fix if >1000 lines off
            replacements.append((
                old.group(0),
                f"~{source_k:,} lines",
                f"source: ~{old_num:,} -> ~{source_k:,}",
            ))

    if not replacements:
        print("\nAll CLAUDE.md counts are already accurate.")
        return

    verb = "Would update" if args.dry_run else "Updating"
    print(f"\n{verb} {len(replacements)} count(s):")
    for old_str, new_str, desc in replacements:
        print(f"  {desc}")
        print(f"    \"{old_str}\" -> \"{new_str}\"")

    if not args.dry_run:
        for old_str, new_str, _ in replacements:
            text = text.replace(old_str, new_str)
        CLAUDE_MD.write_text(text, encoding="utf-8")
        print(f"\nUpdated {CLAUDE_MD.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
