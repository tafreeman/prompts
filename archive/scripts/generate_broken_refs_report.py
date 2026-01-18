#!/usr/bin/env python3
"""Generate CSV report of broken file references in the repository."""
import csv
import re
from pathlib import Path
from typing import List, Tuple

# Directories to skip
SKIP_DIRS = {"_archive", ".git", "node_modules", "__pycache__", ".venv", ".gemini", "archive"}

# Placeholder patterns to ignore (these are examples, not real refs)
PLACEHOLDERS = [
                "path/to/", "example", "your-", "<", "{", "prompt.md", "file.",
                "template", "folder/", "directory/"
                ]


def is_placeholder(path: str) -> bool:
    """Check if a path looks like a placeholder/example."""
    return any(p in path.lower() for p in PLACEHOLDERS)


def validate_references(root_dir: str) -> List[Tuple[str, str, str, str, str]]:
    """
    Scan all markdown files and validate references.

    Returns: List of (source_file, reference, link_text, status, issue_type)
    """
    root = Path(root_dir).resolve()
    results = []

    for filepath in root.rglob("*.md"):
        # Skip excluded directories
        if any(skip in filepath.parts for skip in SKIP_DIRS):
            continue

        rel_filepath = str(filepath.relative_to(root))

        try:
            content = filepath.read_text(encoding='utf-8', errors='ignore')

            # Find all markdown links [text](path)
            for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', content):
                link_text, link_path = match.groups()

                # Skip external URLs
                if link_path.startswith(('http://', 'https://', 'mailto:')):
                    continue

                # Skip internal anchors
                if link_path.startswith('#'):
                    continue

                # Skip web routes (absolute paths without file extensions)
                if link_path.startswith('/') and not any(link_path.endswith(ext) for ext in ['.md', '.py', '.yaml', '.yml', '.json']):
                    continue

                # Remove anchor from path
                clean_path = link_path.split('#')[0]
                if not clean_path:
                    continue

                # Skip placeholders
                if is_placeholder(clean_path):
                    results.append((rel_filepath, link_path, link_text, "SKIP", "Placeholder/Example"))
                    continue

                # Only validate paths that look like files
                if not any(clean_path.endswith(ext) for ext in ['.md', '.py', '.yaml', '.yml', '.json', '.txt']):
                    continue

                # Check for old archive references
                if 'tools/archive/' in clean_path or 'testing/archive/' in clean_path:
                    results.append((rel_filepath, link_path, link_text, "FIXABLE", "Old archive path"))
                    continue

                # Resolve relative path
                if clean_path.startswith('/'):
                    target = root / clean_path.lstrip('/')
                else:
                    target = (filepath.parent / clean_path).resolve()

                # Also try from repo root
                root_target = root / clean_path

                # Check if file exists
                if target.exists() or root_target.exists():
                    results.append((rel_filepath, link_path, link_text, "OK", "File exists"))
                else:
                    results.append((rel_filepath, link_path, link_text, "BROKEN", "File not found"))

        except Exception as e:
            results.append((rel_filepath, "", "", "ERROR", f"Error reading file: {e}"))

    return results


def main():
    print("Scanning repository for file references...")

    results = validate_references(".")

    # Categorize results
    ok = [r for r in results if r[3] == "OK"]
    broken = [r for r in results if r[3] == "BROKEN"]
    fixable = [r for r in results if r[3] == "FIXABLE"]
    skipped = [r for r in results if r[3] == "SKIP"]
    errors = [r for r in results if r[3] == "ERROR"]

    print(f"\n{'='*60}")
    print("RESULTS:")
    print(f"  ✅ Valid references: {len(ok)}")
    print(f"  ❌ Broken references: {len(broken)}")
    print(f"  🔧 Auto-fixable (old paths): {len(fixable)}")
    print(f"  ⏭️  Skipped (placeholders): {len(skipped)}")
    print(f"  ⚠️  Errors: {len(errors)}")
    print(f"{'='*60}\n")

    # Write detailed CSV
    output_file = "broken_references_report.csv"
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Source File", "Reference", "Link Text", "Status", "Issue Type"])

        # Write broken first (highest priority)
        for row in sorted(broken):
            writer.writerow(row)

        # Then fixable
        for row in sorted(fixable):
            writer.writerow(row)

        # Then errors
        for row in sorted(errors):
            writer.writerow(row)

        # Finally OK and skipped for reference
        for row in sorted(ok):
            writer.writerow(row)
        for row in sorted(skipped):
            writer.writerow(row)

    print(f"📄 Full report written to: {output_file}")

    # Show top broken references
    if broken:
        print("\n🔍 Sample of broken references:")
        for source, ref, text, status, issue in broken[:15]:
            print(f"  {source}")
            print(f"    -> {ref}")
        if len(broken) > 15:
            print(f"  ... and {len(broken) - 15} more (see CSV)")

    if fixable:
        print("\n🔧 Auto-fixable references (run fix_archive_refs.py --fix):")
        for source, ref, text, status, issue in fixable[:10]:
            print(f"  {source}: {ref}")


if __name__ == "__main__":
    main()
