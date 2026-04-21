"""Fix broken relative import paths in presentation/src/components/.

Usage:
    python scripts/fix-presentation-imports.py [--dry-run]

The code quality audit found 42 .tsx files importing from "../hooks/useTheme.js"
when the correct path varies by component depth. This script:
1. Finds all .tsx/.ts files importing useTheme with wrong relative paths
2. Resolves the correct relative path to the actual hooks directory
3. Updates the import statement
"""

import argparse
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRESENTATION_SRC = ROOT / "presentation" / "src"

# Known hook files and their actual locations
HOOKS_DIR = PRESENTATION_SRC / "components" / "hooks"  # Check if this exists
ALT_HOOKS_DIR = PRESENTATION_SRC / "hooks"  # Alternative location


def find_hooks_dir() -> pathlib.Path | None:
    """Find where useTheme actually lives."""
    for candidate in [HOOKS_DIR, ALT_HOOKS_DIR]:
        if candidate.exists():
            for f in candidate.iterdir():
                if "useTheme" in f.name:
                    return candidate
    # Search more broadly
    for f in PRESENTATION_SRC.rglob("useTheme.*"):
        return f.parent
    return None


def compute_relative_path(from_file: pathlib.Path, to_dir: pathlib.Path) -> str:
    """Compute relative import path from a file to a directory."""
    from_dir = from_file.parent
    try:
        rel = to_dir.relative_to(from_dir)
        return "./" + str(rel).replace("\\", "/")
    except ValueError:
        # Need to go up
        parts_from = from_dir.parts
        parts_to = to_dir.parts
        # Find common prefix
        common = 0
        for a, b in zip(parts_from, parts_to):
            if a == b:
                common += 1
            else:
                break
        ups = len(parts_from) - common
        downs = parts_to[common:]
        rel = "/".join([".."] * ups + list(downs))
        return rel


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    hooks_dir = find_hooks_dir()
    if hooks_dir is None:
        print("ERROR: Could not find useTheme hook file anywhere in presentation/src/")
        print("Searched: presentation/src/components/hooks/, presentation/src/hooks/")
        return

    print(f"Found hooks at: {hooks_dir.relative_to(ROOT)}")

    # Find all files with potentially wrong hook imports
    import_pattern = re.compile(
        r"""(from\s+["'])(\.\.?/[^"']*hooks/useTheme[^"']*)(["'])"""
    )

    fixed = []
    for ext in ("*.tsx", "*.ts", "*.jsx", "*.js"):
        for filepath in PRESENTATION_SRC.rglob(ext):
            if "node_modules" in filepath.parts:
                continue

            text = filepath.read_text(encoding="utf-8", errors="replace")
            matches = list(import_pattern.finditer(text))
            if not matches:
                continue

            new_text = text
            for match in matches:
                old_path = match.group(2)
                # Compute correct relative path
                correct_rel = compute_relative_path(filepath, hooks_dir)
                # Extract filename from old import
                filename = pathlib.PurePosixPath(old_path).name
                new_path = f"{correct_rel}/{filename}"

                if old_path != new_path:
                    new_text = new_text.replace(
                        f"{match.group(1)}{old_path}{match.group(3)}",
                        f"{match.group(1)}{new_path}{match.group(3)}",
                    )
                    fixed.append(
                        (
                            str(filepath.relative_to(ROOT)),
                            old_path,
                            new_path,
                        )
                    )

            if new_text != text and not args.dry_run:
                filepath.write_text(new_text, encoding="utf-8")

    if fixed:
        verb = "Would fix" if args.dry_run else "Fixed"
        print(f"\n{verb} {len(fixed)} import(s):")
        for filepath, old, new in sorted(fixed):
            print(f"  {filepath}")
            print(f"    {old} -> {new}")
    else:
        print("All hook imports look correct.")


if __name__ == "__main__":
    main()
