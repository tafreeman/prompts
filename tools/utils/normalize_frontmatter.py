#!/usr/bin/env python3
"""Frontmatter Normalization Script.

Adds missing required fields to prompt markdown files based on the
unified schema.
"""

import argparse
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import yaml

# Default values for new fields
DEFAULTS = {
    "shortTitle": lambda title: title[:27] if len(title) > 27 else title,
    "intro": lambda title, desc: (
        desc if desc else f"A prompt for {title.lower().replace('prompt', '').strip()}."
    ),
    "type": "how_to",
    "audience": ["senior-engineer"],
    "platforms": ["github-copilot"],
    "governance_tags": ["general-use", "PII-safe"],
    "dataClassification": "internal",
    "reviewStatus": "draft",
}

# Platform mapping from old values to new standardized values
PLATFORM_MAP = {
    "gpt-4": "chatgpt",
    "gpt-4o": "chatgpt",
    "gpt-5": "chatgpt",
    "openai": "chatgpt",
    "claude": "claude",
    "claude-3": "claude",
    "claude-4": "claude",
    "anthropic": "claude",
    "copilot": "github-copilot",
    "github copilot": "github-copilot",
    "m365": "m365-copilot",
    "m365 copilot": "m365-copilot",
    "microsoft 365": "m365-copilot",
    "gemini": "gemini",
    "google": "gemini",
}

# Type inference from title/content
TYPE_KEYWORDS = {
    "quickstart": "quickstart",
    "quick start": "quickstart",
    "getting started": "quickstart",
    "tutorial": "tutorial",
    "guide": "tutorial",
    "walkthrough": "tutorial",
    "reference": "reference",
    "cheat sheet": "reference",
    "glossary": "reference",
    "troubleshoot": "troubleshooting",
    "debug": "troubleshooting",
    "fix": "troubleshooting",
    "about": "conceptual",
    "overview": "conceptual",
    "introduction": "conceptual",
}

# Audience inference from folder/content
AUDIENCE_MAP = {
    "developers": ["senior-engineer"],
    "advanced": ["senior-engineer", "solution-architect"],
    "business": ["business-analyst", "product-manager"],
    "analysis": ["business-analyst", "senior-engineer"],
    "m365": ["junior-engineer", "business-analyst"],
    "system": ["solution-architect", "senior-engineer"],
    "governance": ["solution-architect", "senior-engineer"],
    "creative": ["junior-engineer", "senior-engineer"],
}


def parse_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], str, str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return None, "", content

    # Find the closing ---
    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        return None, "", content

    end_pos = end_match.end() + 3
    fm_text = content[4 : end_match.start() + 3]
    body = content[end_pos:]

    try:
        fm = yaml.safe_load(fm_text)
        return fm, fm_text, body
    except yaml.YAMLError:
        return None, fm_text, body


def infer_type(title: str, body: str) -> str:
    """Infer content type from title and body."""
    title_lower = title.lower()
    body_lower = body[:500].lower()

    for keyword, content_type in TYPE_KEYWORDS.items():
        if keyword in title_lower or keyword in body_lower:
            return content_type

    return "how_to"


def infer_platforms(fm: Dict[str, Any]) -> list:
    """Infer platforms from existing platform field or default."""
    platforms = []

    # Check existing platform field (singular)
    if "platform" in fm:
        platform_str = str(fm["platform"]).lower()
        for old, new in PLATFORM_MAP.items():
            if old in platform_str:
                if new not in platforms:
                    platforms.append(new)

    # Check existing platforms field (plural)
    if "platforms" in fm:
        existing = fm["platforms"]
        if isinstance(existing, list):
            for p in existing:
                p_lower = str(p).lower()
                mapped = PLATFORM_MAP.get(p_lower, p_lower)
                if mapped not in platforms:
                    platforms.append(mapped)
        elif isinstance(existing, str):
            p_lower = existing.lower()
            mapped = PLATFORM_MAP.get(p_lower, p_lower)
            if mapped not in platforms:
                platforms.append(mapped)

    return platforms if platforms else ["github-copilot"]


def infer_audience(folder: str) -> list:
    """Infer audience from folder name."""
    folder_name = Path(folder).name
    return AUDIENCE_MAP.get(folder_name, ["senior-engineer"])


def extract_intro(body: str, title: str) -> str:
    """Extract intro from body description section or generate one."""
    # Look for Description section
    desc_match = re.search(r"##?\s*Description\s*\n+([^\n#]+)", body, re.IGNORECASE)
    if desc_match:
        intro = desc_match.group(1).strip()
        # Truncate if too long
        if len(intro) > 200:
            intro = intro[:197] + "..."
        return intro

    # Look for first paragraph after title
    para_match = re.search(r"^[A-Z][^#\n]{20,200}", body, re.MULTILINE)
    if para_match:
        return para_match.group(0).strip()

    # Generate from title
    return f"A prompt for {title.lower().replace('prompt', '').strip()}."


def normalize_frontmatter(fm: Dict[str, Any], body: str, folder: str) -> Dict[str, Any]:
    """Add missing required fields to frontmatter."""
    title = fm.get("title", "Untitled Prompt")

    # Add shortTitle if missing
    if "shortTitle" not in fm:
        short = title
        # Remove common suffixes
        for suffix in [" Prompt", " Template", " Guide", " Assistant"]:
            if short.endswith(suffix):
                short = short[: -len(suffix)]
        # Truncate to 27 chars
        if len(short) > 27:
            short = short[:24] + "..."
        fm["shortTitle"] = short

    # Add intro if missing
    if "intro" not in fm:
        fm["intro"] = extract_intro(body, title)

    # Add type if missing
    if "type" not in fm:
        fm["type"] = infer_type(title, body)

    # Normalize difficulty to lowercase
    if "difficulty" in fm:
        fm["difficulty"] = str(fm["difficulty"]).lower()
    else:
        fm["difficulty"] = "intermediate"

    # Add/normalize platforms
    fm["platforms"] = infer_platforms(fm)

    # Remove old platform field (singular)
    if "platform" in fm:
        del fm["platform"]

    # Add audience if missing
    if "audience" not in fm:
        fm["audience"] = infer_audience(folder)

    # Convert category/tags to topics
    topics = []
    if "category" in fm:
        topics.append(str(fm["category"]).lower())
        del fm["category"]
    if "tags" in fm:
        tags = fm["tags"]
        if isinstance(tags, list):
            topics.extend([str(t).lower() for t in tags[:3]])
        del fm["tags"]
    if topics and "topics" not in fm:
        fm["topics"] = list(set(topics))[:5]

    # Add governance fields if missing
    if "governance_tags" not in fm:
        fm["governance_tags"] = ["general-use", "PII-safe"]
    elif isinstance(fm["governance_tags"], str):
        # Fix string that should be list
        fm["governance_tags"] = ["general-use", "PII-safe"]

    if "dataClassification" not in fm:
        fm["dataClassification"] = "internal"

    if "reviewStatus" not in fm:
        fm["reviewStatus"] = "draft"

    # Add metadata defaults
    if "author" not in fm:
        fm["author"] = "Prompt Library Team"
    if "version" not in fm:
        fm["version"] = "1.0"
    if "date" not in fm:
        fm["date"] = "2025-11-30"

    return fm


def format_frontmatter(fm: Dict[str, Any]) -> str:
    """Format frontmatter dict as YAML string with proper ordering."""
    # Define field order
    order = [
        "title",
        "shortTitle",
        "intro",
        "type",
        "difficulty",
        "audience",
        "platforms",
        "topics",
        "technique",
        "author",
        "version",
        "date",
        "governance_tags",
        "dataClassification",
        "reviewStatus",
    ]

    lines = ["---"]

    # Add fields in order
    for key in order:
        if key in fm:
            value = fm[key]
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f'  - "{item}"')
            elif isinstance(value, str):
                # Escape quotes in strings
                if '"' in value or ":" in value or "\n" in value:
                    lines.append(f'{key}: "{value}"')
                else:
                    lines.append(f'{key}: "{value}"')
            else:
                lines.append(f"{key}: {value}")

    # Add any remaining fields not in order
    for key, value in fm.items():
        if key not in order:
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f'  - "{item}"')
            elif isinstance(value, str):
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f"{key}: {value}")

    lines.append("---")
    return "\n".join(lines)


def process_file(filepath: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """Process a single markdown file."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Read error: {e}"

    fm, fm_text, body = parse_frontmatter(content)

    if fm is None:
        return False, "No valid frontmatter found"

    # Normalize
    folder = str(filepath.parent)
    normalized = normalize_frontmatter(fm.copy(), body, folder)

    # Format new frontmatter
    new_fm_text = format_frontmatter(normalized)
    new_content = new_fm_text + "\n" + body.lstrip()

    if dry_run:
        return True, "Would update"

    try:
        filepath.write_text(new_content, encoding="utf-8")
        return True, "Updated"
    except Exception as e:
        return False, f"Write error: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Normalize frontmatter in prompt files"
    )
    parser.add_argument("--all", action="store_true", help="Process all prompt files")
    parser.add_argument("--folder", type=str, help="Process files in specific folder")
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be changed"
    )
    parser.add_argument("file", nargs="?", help="Single file to process")

    args = parser.parse_args()

    base_dir = Path("d:/source/prompts")
    files_to_process = []

    if args.file:
        files_to_process = [Path(args.file)]
    elif args.folder:
        folder_path = base_dir / args.folder
        files_to_process = list(folder_path.rglob("*.md"))
    elif args.all:
        files_to_process = list((base_dir / "prompts").rglob("*.md"))
    else:
        print("Specify --all, --folder, or a file path")
        return

    # Filter out index.md and README.md
    files_to_process = [
        f for f in files_to_process if f.name not in ("index.md", "README.md")
    ]

    success = 0
    failed = 0

    for filepath in files_to_process:
        ok, msg = process_file(filepath, args.dry_run)
        status = "✓" if ok else "✗"
        print(f"{status} {filepath.name}: {msg}")
        if ok:
            success += 1
        else:
            failed += 1

    print(f"\nProcessed: {success + failed} files")
    print(f"Success: {success}, Failed: {failed}")


if __name__ == "__main__":
    main()
