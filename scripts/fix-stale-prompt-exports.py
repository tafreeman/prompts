"""Remove exported prompt constants whose .md files no longer exist.

Usage:
    python scripts/fix-stale-prompt-exports.py [--dry-run]

After prompts were deleted (d921ba0f), their constants in __init__.py
became dangling references. This script removes them.
"""

import argparse
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
INIT_FILE = ROOT / "agentic-workflows-v2" / "agentic_v2" / "prompts" / "__init__.py"
PROMPTS_DIR = ROOT / "agentic-workflows-v2" / "agentic_v2" / "prompts"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not INIT_FILE.exists():
        print(f"File not found: {INIT_FILE}")
        return

    text = INIT_FILE.read_text(encoding="utf-8")

    # Find all NAME = "name" constant assignments
    pattern = re.compile(r'^([A-Z_]+)\s*=\s*["\'](\w+)["\']', re.MULTILINE)
    to_remove = []

    for match in pattern.finditer(text):
        const_name = match.group(1)
        prompt_name = match.group(2)
        md_file = PROMPTS_DIR / f"{prompt_name}.md"
        if not md_file.exists():
            to_remove.append((const_name, prompt_name, match.group(0)))

    if not to_remove:
        print("All exported prompt constants have corresponding .md files.")
        return

    verb = "Would remove" if args.dry_run else "Removing"
    print(f"{verb} {len(to_remove)} stale constant(s):")
    for const_name, prompt_name, line in to_remove:
        print(f'  {const_name} = "{prompt_name}"  (no {prompt_name}.md)')

    if not args.dry_run:
        new_text = text
        for _, _, line in to_remove:
            new_text = new_text.replace(line + "\n", "")

        # Also remove from __all__ if present
        for const_name, _, _ in to_remove:
            # Remove "CONST_NAME", from __all__ list
            new_text = re.sub(
                rf'^\s*"{const_name}",?\s*\n',
                "",
                new_text,
                flags=re.MULTILINE,
            )
            new_text = re.sub(
                rf"^\s*'{const_name}',?\s*\n",
                "",
                new_text,
                flags=re.MULTILINE,
            )

        # Clean up double blank lines
        new_text = re.sub(r"\n{3,}", "\n\n", new_text)

        INIT_FILE.write_text(new_text, encoding="utf-8")
        print(f"\nUpdated {INIT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
