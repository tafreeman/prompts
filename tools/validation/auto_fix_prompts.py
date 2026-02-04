#!/usr/bin/env python3
"""Auto-fix prompt files to add missing frontmatter keys and sections.

This script is conservative: it preserves existing content and only inserts
missing frontmatter keys and missing top-level sections with clearly marked
TODO placeholders so humans can review and improve later.

Run from repo root:
    python tools/validation/auto_fix_prompts.py --dry-run
    python tools/validation/auto_fix_prompts.py
"""

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = ROOT / "prompts"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
HEADING_RE = re.compile(
    r"^##\s+(Description|Prompt|Variables|Example)\b", re.IGNORECASE | re.MULTILINE
)
BRACKET_VAR_RE = re.compile(r"\[([^\]\n]+)\]")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, content: str, dry_run: bool):
    if dry_run:
        print(f"[dry-run] would write: {path}")
        return
    path.write_text(content, encoding="utf-8")


def ensure_frontmatter(text: str, filename: str):
    m = FRONTMATTER_RE.match(text)
    if m:
        fm = m.group(1)
        body = text[m.end() :]
        # parse simple key: value lines
        keys = {
            k.strip(): v.strip()
            for k, v in (line.split(":", 1) for line in fm.splitlines() if ":" in line)
        }
        changed = False
        if "name" not in keys:
            fm = fm + f"\nname: {filename}\n"
            changed = True
        if "description" not in keys:
            fm = fm + "\ndescription: 'AUTO-GENERATED: brief description required'\n"
            changed = True
        if "type" not in keys:
            fm = fm + "\ntype: how_to\n"
            changed = True
        if changed:
            new_text = "---\n" + fm.strip() + "\n---\n" + body
            return new_text, True
        return text, False
    else:
        # create basic frontmatter (quote description so YAML is valid)
        fm = f"---\nname: {filename}\ndescription: 'AUTO-GENERATED: brief description required'\ntype: how_to\n---\n\n"
        return fm + text, True


def has_heading(text: str, heading: str) -> bool:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\\b", re.IGNORECASE | re.MULTILINE
    )
    return bool(pattern.search(text))


def extract_first_codeblock_or_para(text: str) -> str:
    # Look for first fenced code block
    code_m = re.search(r"```(?:\w+)?\n(.*?)\n```", text, re.DOTALL)
    if code_m:
        return code_m.group(0)
    # otherwise take first non-empty paragraph after frontmatter
    parts = text.strip().splitlines()
    para_lines = []
    for line in parts:
        if line.strip() == "":
            if para_lines:
                break
            continue
        if line.startswith("#"):
            continue
        para_lines.append(line)
        if len(para_lines) >= 5:
            break
    if para_lines:
        return "\n".join(para_lines)
    return ""


def build_variables_section(text: str):
    vars_found = BRACKET_VAR_RE.findall(text)
    if not vars_found:
        return "## Variables\n\n_No bracketed variables detected._\n\n"
    rows = ["| Variable | Description |", "|---|---|"]
    for v in sorted(set(vars_found)):
        rows.append(f"| `[{v}]` | AUTO-GENERATED: describe `{v}` |")
    return "## Variables\n\n" + "\n".join(rows) + "\n\n"


def process_file(path: Path, dry_run: bool) -> bool:
    filename = path.stem
    orig = read(path)
    cur = orig
    changed = False

    cur, fm_changed = ensure_frontmatter(cur, filename)
    changed = changed or fm_changed

    # Ensure Description
    if not has_heading(cur, "Description"):
        desc = ""
        # try to reuse frontmatter description if present
        m = FRONTMATTER_RE.match(cur)
        if m:
            fm = m.group(1)
            desc_line = None
            for line in fm.splitlines():
                if line.strip().startswith("description:"):
                    desc_line = line.split(":", 1)[1].strip()
                    break
            if desc_line and "AUTO-GENERATED" not in desc_line:
                desc = desc_line
        if not desc:
            desc = "AUTO-GENERATED: Short description of this prompt. Please refine."
        insert = f"## Description\n\n{desc}\n\n"
        # insert after frontmatter
        m = FRONTMATTER_RE.match(cur)
        if m:
            body_start = m.end()
            cur = cur[:body_start] + insert + cur[body_start:]
        else:
            cur = insert + cur
        changed = True

    # Ensure Prompt
    if not has_heading(cur, "Prompt"):
        snippet = extract_first_codeblock_or_para(orig)
        if snippet:
            prompt_block = "## Prompt\n\n"
            # If snippet is a fenced codeblock, keep as-is
            if snippet.startswith("```"):
                prompt_block += snippet + "\n\n"
            else:
                prompt_block += "```text\n" + snippet + "\n```\n\n"
        else:
            prompt_block = (
                "## Prompt\n\n```text\n[A user-facing prompt goes here]\n```\n\n"
            )
        # place Prompt after Description heading
        # find position after Description
        desc_m = re.search(r"^##\s+Description.*?$", cur, re.IGNORECASE | re.MULTILINE)
        if desc_m:
            # insert after that heading block (after the paragraph)
            # naive: insert after first blank line following Description
            parts = cur.splitlines()
            for i, line in enumerate(parts):
                if re.match(r"^##\s+Description", line, re.IGNORECASE):
                    # find next blank line index
                    j = i + 1
                    while j < len(parts) and parts[j].strip() != "":
                        j += 1
                    # reconstruct
                    before = "\n".join(parts[: j + 1]) + "\n"
                    after = "\n".join(parts[j + 1 :])
                    cur = before + prompt_block + after
                    break
        else:
            cur = prompt_block + cur
        changed = True

    # Ensure Variables
    if not has_heading(cur, "Variables"):
        var_section = build_variables_section(orig)
        # append after Prompt if present
        prompt_m = re.search(r"^##\s+Prompt.*?$", cur, re.IGNORECASE | re.MULTILINE)
        if prompt_m:
            # append after Prompt block: put at end of Prompt section by appending raw
            cur = cur + var_section
        else:
            cur = cur + var_section
        changed = True

    # Ensure Example
    if not has_heading(cur, "Example"):
        example = (
            "## Example\n\n"
            "### Input\n\n````text\n[Fill in a realistic input for the prompt]\n````\n\n"
            "### Expected Output\n\n````text\n[Representative AI response]\n````\n\n"
        )
        cur = cur + example
        changed = True

    if changed:
        write(path, cur, dry_run)
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--path", default=str(PROMPTS_DIR))
    args = ap.parse_args()
    root = Path(args.path)
    modified = []
    for p in sorted(root.rglob("*.md")):
        # skip README files in subfolders that are docs
        if p.parts[-1].lower() in ("readme.md", "index.md"):
            continue
        try:
            changed = process_file(p, args.dry_run)
            if changed:
                modified.append(str(p))
        except Exception as e:
            print(f"ERROR processing {p}: {e}")
    print(f"Processed {len(list(root.rglob('*.md')))} files; modified: {len(modified)}")
    if modified:
        for m in modified:
            print(f"  - {m}")


if __name__ == "__main__":
    main()
