#!/usr/bin/env python3
"""
Cleanup script for prompt files:
  - Ensures only a single YAML frontmatter block at the top (with name, description)
  - Removes duplicate/malformed frontmatter blocks
  - Removes stray 'name:'/'description:' lines outside the frontmatter
  - Normalizes to minimal frontmatter
"""

import re
from pathlib import Path

import yaml

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def extract_minimal_fm(text, path):
    m = FM_RE.match(text)
    fm = {}
    if m:
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except Exception:
            fm = {}
        body = text[m.end() :]
    else:
        body = text
    # Remove any stray 'name:' or 'description:' lines at the top of the body
    body = re.sub(r"^(name|description)\s*:[^\n]*\n", "", body, flags=re.I | re.M)
    # Remove any additional frontmatter blocks in the body
    body = re.sub(r"^---.*?---\s*\n", "", body, flags=re.DOTALL | re.M)
    # Compose minimal frontmatter
    name = (
        fm.get("name")
        or fm.get("title")
        or path.stem.replace("-", " ").replace("_", " ").title()
    )
    desc = fm.get("description") or fm.get("intro")
    if isinstance(desc, list):
        desc = " ".join(desc)
    if not desc:
        # Try to use first paragraph of body
        paras = [p.strip() for p in body.split("\n\n") if p.strip()]
        desc = paras[0] if paras else f"A prompt for {name.lower()} tasks."
    desc = " ".join(desc.split())[:200]
    return name, desc, body.lstrip("\n")


def process_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    name, desc, body = extract_minimal_fm(text, path)
    new_fm = f"---\nname: {name}\ndescription: {desc}\n---\n\n"
    new_text = new_fm + body
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    root = Path(__file__).resolve().parents[2] / "prompts"
    md_files = list(root.rglob("*.md"))
    changed = 0
    for p in md_files:
        try:
            if process_file(p):
                print(f"Cleaned: {p.relative_to(root.parent)}")
                changed += 1
        except Exception as e:
            print(f"Error processing {p}: {e}")
    print(f"Cleanup complete. Files cleaned: {changed}/{len(md_files)}")


if __name__ == "__main__":
    main()
