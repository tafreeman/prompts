#!/usr/bin/env python3
"""Add minimal frontmatter (name, description) to all Markdown prompts under prompts/.

This script is idempotent: it will skip files that already have both name and description
in the frontmatter. It extracts title/intro/description from existing frontmatter when
available, or falls back to the filename and first paragraph of the body.
"""
import re
from pathlib import Path
import yaml


FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def extract_first_paragraph(body: str) -> str:
    # strip leading headings and whitespace
    body = body.lstrip('\n')
    # remove leading ATX headings
    body = re.sub(r"^#+ .*\n", "", body)
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip()]
    return paragraphs[0] if paragraphs else ''


def make_name_from_filename(path: Path) -> str:
    return path.stem.replace('-', ' ').replace('_', ' ').title()


def process_file(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    m = FM_RE.match(text)
    if m:
        fm_text, body = m.group(1), m.group(2)
        try:
            fm = yaml.safe_load(fm_text) or {}
        except Exception:
            fm = {}
    else:
        fm = {}
        body = text

    name = fm.get('name') or fm.get('title') or make_name_from_filename(path)
    desc = fm.get('description') or fm.get('intro')
    if isinstance(desc, list):
        desc = ' '.join(desc)
    if not desc:
        # try to use first paragraph of body
        desc = extract_first_paragraph(body)
    # sanitize: drop lines that look like embedded metadata (e.g., "name: ..." at top of body)
    if desc:
        desc_lines = [ln for ln in desc.splitlines() if not re.match(r'^(name|description|title)\s*:', ln, re.I)]
        desc = ' '.join(desc_lines).strip()
    if not desc:
        desc = f'A prompt for {name.lower()} tasks.'
    desc = ' '.join(desc.split())[:200]

    # If file already has name and description present in frontmatter, skip
    if m and 'name' in fm and ('description' in fm or 'intro' in fm):
        return False

    new_fm = f"---\nname: {name}\ndescription: {desc}\n---\n\n"
    new_text = new_fm + body.lstrip('\n')
    path.write_text(new_text, encoding='utf-8')
    return True


def main():
    root = Path(__file__).resolve().parents[2] / 'prompts'
    md_files = list(root.rglob('*.md'))
    changed = 0
    for p in md_files:
        try:
            if process_file(p):
                print(f'Updated: {p.relative_to(root.parent)}')
                changed += 1
        except Exception as e:
            print(f'Error processing {p}: {e}')
    print(f'Finished. Files updated: {changed}/{len(md_files)}')


if __name__ == '__main__':
    main()
