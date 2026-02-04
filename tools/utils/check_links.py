#!/usr/bin/env python3
"""Check for broken internal links in markdown files."""

import re
import sys
from pathlib import Path


def check_links(path: Path) -> list:
    """Check internal links in a markdown file.

    Returns broken links.
    """
    broken = []
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return []

    # Find markdown links (including those with anchors)
    links = re.findall(r"\[([^\]]+)\]\(([^)]+\.md(?:#[^)]*)?)\)", content)

    for text, link in links:
        if link.startswith("http"):
            continue

        # Remove anchor if present
        link_path = link.split("#")[0]

        # Resolve relative path
        target = (path.parent / link_path).resolve()
        if not target.exists():
            broken.append((text, link))

    return broken


def main():
    errors = 0
    for path in Path("prompts").rglob("*.md"):
        broken = check_links(path)
        if broken:
            print(f"\n{path}:")
            for text, link in broken:
                print(f"  - [{text}]({link})")
            errors += len(broken)

    print(f"\n{'='*50}")
    print(f"Total broken links: {errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
