#!/usr/bin/env python3
"""
Frontmatter Fixer Script
Automatically fixes missing and invalid frontmatter fields based on the validation schema.
"""

import re
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import yaml


# Configuration
REPO_ROOT = Path(__file__).parent.parent
PROMPTS_DIR = REPO_ROOT / "prompts"


# Schema definitions (matching frontmatter_validator.py)
VALID_TYPES = ["conceptual", "quickstart", "how_to", "tutorial", "reference", "troubleshooting"]
VALID_DIFFICULTIES = ["beginner", "intermediate", "advanced"]
VALID_AUDIENCES = [
    "junior-engineer",
    "senior-engineer",
    "solution-architect",
    "qa-engineer",
    "business-analyst",
    "project-manager",
    "functional-team"
]
VALID_PLATFORMS = [
    "github-copilot",
    "claude",
    "chatgpt",
    "azure-openai",
    "m365-copilot"
]
VALID_GOVERNANCE_TAGS = [
    "PII-safe",
    "client-approved",
    "internal-only",
    "requires-human-review",
    "audit-required"
]
VALID_DATA_CLASSIFICATIONS = ["public", "internal", "confidential"]
VALID_REVIEW_STATUSES = ["draft", "reviewed", "approved"]

# Required fields for all content
REQUIRED_FIELDS_ALL = [
    "title",
    "shortTitle",
    "intro",
    "type",
    "difficulty",
    "author",
    "version",
    "date",
    "governance_tags",
    "dataClassification",
    "reviewStatus"
]

# Required fields for prompts (not index.md or README.md)
REQUIRED_FIELDS_PROMPTS = [
    "audience",
    "platforms"
]


def extract_frontmatter(content: str) -> Tuple[Optional[Dict], str, str]:
    """
    Extract YAML frontmatter from markdown content.
    Returns (frontmatter_dict, frontmatter_text, body_text)
    """
    if not content.strip().startswith('---'):
        return None, "", content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, "", content
    
    frontmatter_text = parts[1]
    body_text = parts[2]
    
    try:
        frontmatter = yaml.safe_load(frontmatter_text) or {}
        return frontmatter, frontmatter_text, body_text
    except yaml.YAMLError:
        return None, frontmatter_text, body_text


def infer_short_title(title: str) -> str:
    """Generate a shortTitle from title (max 27 chars)."""
    if len(title) <= 27:
        return title
    
    # Try to shorten intelligently
    # Remove common prefixes/suffixes
    short = title
    for word in ["Assistant", "Specialist", "Consultant", "Expert", "Designer", "Analyzer", "Generator", "Manager"]:
        if short.endswith(f" {word}"):
            short = short[:-len(word)-1]
            if len(short) <= 27:
                return short
    
    # Truncate if still too long
    if len(short) > 27:
        short = short[:24] + "..."
    
    return short


def infer_intro(title: str, description: str = None) -> str:
    """Generate an intro from title or description."""
    if description and len(description) < 200:
        # Clean up description - take first sentence
        first_sentence = description.split('.')[0].strip()
        if first_sentence:
            return first_sentence + "."
    
    return f"A prompt for {title.lower().replace('-', ' ')} tasks."


def infer_type_from_content(content: str, filename: str) -> str:
    """Infer the document type from content analysis."""
    content_lower = content.lower()
    
    if "step-by-step" in content_lower or "## steps" in content_lower:
        return "how_to"
    if "## guide" in content_lower or "tutorial" in filename.lower():
        return "tutorial"
    if "## reference" in content_lower or "api" in filename.lower():
        return "reference"
    if "troubleshoot" in content_lower or "debug" in filename.lower():
        return "troubleshooting"
    if "what is" in content_lower or "introduction" in content_lower:
        return "conceptual"
    if "quick start" in content_lower or "quickstart" in filename.lower():
        return "quickstart"
    
    return "how_to"  # Default


def infer_difficulty(fm: Dict) -> str:
    """Normalize and infer difficulty level."""
    if "difficulty" in fm:
        diff = str(fm["difficulty"]).lower()
        if diff in VALID_DIFFICULTIES:
            return diff
        if diff == "expert":
            return "advanced"
        if diff.startswith("inter"):
            return "intermediate"
        if diff.startswith("beg"):
            return "beginner"
    
    return "intermediate"  # Default


def normalize_audience(audience_value: str) -> Optional[str]:
    """Normalize an audience value to a valid one."""
    val = audience_value.lower().strip()
    
    # Direct mappings
    mappings = {
        "mid-engineer": "senior-engineer",
        "product-manager": "project-manager",
        "data-scientist": "senior-engineer",
        "developer": "junior-engineer",
        "engineer": "senior-engineer",
        "architect": "solution-architect",
        "analyst": "business-analyst",
        "manager": "project-manager",
        "qa": "qa-engineer",
        "tester": "qa-engineer",
        "functional": "functional-team",
    }
    
    if val in VALID_AUDIENCES:
        return val
    
    for key, mapped in mappings.items():
        if key in val:
            return mapped
    
    return None


def infer_audiences(fm: Dict, category: str = None) -> list:
    """Infer target audiences based on content and category."""
    # Check for existing tags that hint at audience
    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]
    
    tags_str = " ".join(str(t).lower() for t in tags)
    
    audiences = []
    
    # Map category/tags to audiences
    if category:
        category_lower = category.lower()
        if "developer" in category_lower or "developers" in category_lower:
            audiences = ["senior-engineer", "junior-engineer"]
        elif "business" in category_lower:
            audiences = ["business-analyst", "project-manager"]
        elif "analysis" in category_lower:
            audiences = ["business-analyst", "senior-engineer"]
        elif "governance" in category_lower:
            audiences = ["senior-engineer", "solution-architect"]
        elif "system" in category_lower:
            audiences = ["solution-architect", "senior-engineer"]
        elif "m365" in category_lower:
            audiences = ["functional-team", "business-analyst"]
        elif "creative" in category_lower:
            audiences = ["functional-team", "business-analyst"]
        elif "agents" in category_lower:
            audiences = ["senior-engineer", "solution-architect"]
        elif "concepts" in category_lower:
            audiences = ["junior-engineer", "senior-engineer"]
        elif "docs" in category_lower:
            audiences = ["junior-engineer", "senior-engineer"]
        elif "frameworks" in category_lower:
            audiences = ["senior-engineer", "solution-architect"]
        elif "techniques" in category_lower:
            audiences = ["senior-engineer", "junior-engineer"]
        elif "guides" in category_lower:
            audiences = ["junior-engineer", "senior-engineer"]
        elif "get-started" in category_lower:
            audiences = ["junior-engineer", "senior-engineer"]
    
    # Refine based on tags
    if "project-manager" in tags_str:
        if "project-manager" not in audiences:
            audiences.insert(0, "project-manager")
    if "architect" in tags_str or "enterprise" in tags_str:
        if "solution-architect" not in audiences:
            audiences.insert(0, "solution-architect")
    if "qa" in tags_str or "testing" in tags_str:
        if "qa-engineer" not in audiences:
            audiences.insert(0, "qa-engineer")
    
    if not audiences:
        audiences = ["senior-engineer", "junior-engineer"]
    
    return audiences[:3]  # Max 3 audiences


def infer_platforms(fm: Dict) -> list:
    """Infer platforms from existing platform field or default."""
    platform = fm.get("platform", "")
    
    if isinstance(platform, list):
        platforms = platform
    else:
        platform_str = str(platform).lower()
        platforms = []
        
        if "m365" in platform_str or "microsoft" in platform_str:
            platforms.append("m365-copilot")
        if "claude" in platform_str:
            platforms.append("claude")
        if "chatgpt" in platform_str or "openai" in platform_str:
            platforms.append("chatgpt")
        if "copilot" in platform_str and "m365" not in platform_str:
            platforms.append("github-copilot")
        if "azure" in platform_str:
            platforms.append("azure-openai")
    
    if not platforms:
        platforms = ["github-copilot", "claude", "chatgpt"]
    
    # Filter to valid platforms
    return [p for p in platforms if p in VALID_PLATFORMS][:5]


def infer_governance_tags(fm: Dict) -> list:
    """Infer governance tags from existing fields."""
    governance = fm.get("governance", {})
    tags = []
    
    if isinstance(governance, dict):
        risk = governance.get("risk_level", "").lower()
        if risk in ["critical", "high"]:
            tags.append("requires-human-review")
        if governance.get("approval_required"):
            tags.append("audit-required")
        data_class = governance.get("data_classification", "").lower()
        if data_class == "confidential":
            tags.append("internal-only")
    
    if not tags:
        tags = ["PII-safe"]
    
    return tags


def infer_data_classification(fm: Dict) -> str:
    """Infer data classification from existing fields."""
    governance = fm.get("governance", {})
    
    if isinstance(governance, dict):
        data_class = governance.get("data_classification", "").lower()
        if data_class in VALID_DATA_CLASSIFICATIONS:
            return data_class
    
    return "internal"  # Default


def get_category_from_path(filepath: Path) -> Optional[str]:
    """Extract category from file path."""
    parts = filepath.parts
    
    # Try to find category from various root directories
    root_dirs = ["prompts", "agents", "concepts", "docs", "examples", "frameworks", 
                 "guides", "get-started", "techniques", "templates", "workflows", "reference"]
    
    for root_dir in root_dirs:
        try:
            idx = parts.index(root_dir)
            # Return the root directory name as category
            # Or if there's a subdirectory, return that
            if idx + 1 < len(parts) - 1:
                return parts[idx + 1]
            else:
                return root_dir
        except ValueError:
            continue
    
    # Fallback: use parent directory name
    if len(parts) > 1:
        return parts[-2]
    
    return None


def fix_frontmatter(fm: Dict, content: str, filepath: Path) -> Dict:
    """Fix missing and invalid frontmatter fields."""
    filename = filepath.stem
    category = get_category_from_path(filepath)
    is_index = filepath.name == "index.md"
    is_readme = filepath.name.lower() == "readme.md"
    
    # Title
    if "title" not in fm:
        # Try to extract from first H1
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            fm["title"] = match.group(1).strip()
        else:
            fm["title"] = filename.replace("-", " ").title()
    
    # Ensure title is under 60 chars
    if len(fm.get("title", "")) > 60:
        fm["title"] = fm["title"][:57] + "..."
    
    # shortTitle
    if "shortTitle" not in fm:
        fm["shortTitle"] = infer_short_title(fm.get("title", filename))
    
    # Ensure shortTitle is under 27 chars
    if len(fm.get("shortTitle", "")) > 27:
        fm["shortTitle"] = fm["shortTitle"][:24] + "..."
    
    # intro
    if "intro" not in fm:
        description = fm.get("description", "")
        fm["intro"] = infer_intro(fm.get("title", filename), description)
    
    # type
    if "type" not in fm or fm["type"] not in VALID_TYPES:
        fm["type"] = infer_type_from_content(content, filename)
    
    # difficulty
    fm["difficulty"] = infer_difficulty(fm)
    
    # author
    if "author" not in fm:
        fm["author"] = "Prompts Library Team"
    
    # version
    if "version" not in fm:
        fm["version"] = "1.0"
    elif isinstance(fm["version"], (int, float)):
        fm["version"] = str(fm["version"])
    
    # date
    if "date" not in fm:
        fm["date"] = "2025-11-30"
    else:
        # Ensure proper format
        date_val = str(fm["date"])
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_val):
            fm["date"] = "2025-11-30"
    
    # governance_tags
    if "governance_tags" not in fm:
        fm["governance_tags"] = infer_governance_tags(fm)
    
    # dataClassification
    if "dataClassification" not in fm or fm["dataClassification"] not in VALID_DATA_CLASSIFICATIONS:
        fm["dataClassification"] = infer_data_classification(fm)
    
    # reviewStatus
    if "reviewStatus" not in fm or fm["reviewStatus"] not in VALID_REVIEW_STATUSES:
        fm["reviewStatus"] = "draft"
    
    # For non-index/README files, also need audience and platforms
    if not is_index and not is_readme:
        # audience
        if "audience" not in fm:
            fm["audience"] = infer_audiences(fm, category)
        elif not isinstance(fm["audience"], list):
            fm["audience"] = [fm["audience"]]
        
        # Normalize and validate audience values
        normalized_audiences = []
        for aud in fm["audience"]:
            if aud in VALID_AUDIENCES:
                normalized_audiences.append(aud)
            else:
                # Try to normalize
                normalized = normalize_audience(aud)
                if normalized and normalized not in normalized_audiences:
                    normalized_audiences.append(normalized)
        
        fm["audience"] = normalized_audiences
        if not fm["audience"]:
            fm["audience"] = infer_audiences(fm, category)
        
        # platforms
        if "platforms" not in fm:
            fm["platforms"] = infer_platforms(fm)
        elif not isinstance(fm["platforms"], list):
            fm["platforms"] = [fm["platforms"]]
        
        # Validate platform values
        valid_platforms = [p for p in fm["platforms"] if p in VALID_PLATFORMS]
        if not valid_platforms:
            fm["platforms"] = infer_platforms(fm)
        else:
            fm["platforms"] = valid_platforms
    
    return fm


def create_frontmatter_for_readme(filepath: Path) -> Dict:
    """Create minimal frontmatter for README files."""
    category = get_category_from_path(filepath) or "general"
    title = f"{category.title()} Prompts"
    
    return {
        "title": title,
        "shortTitle": category.title(),
        "intro": f"Overview of {category} prompts available in this library.",
        "type": "reference",
        "difficulty": "beginner",
        "author": "Prompts Library Team",
        "version": "1.0",
        "date": "2025-11-30",
        "governance_tags": ["PII-safe"],
        "dataClassification": "internal",
        "reviewStatus": "draft",
        "audience": ["senior-engineer", "junior-engineer"],
        "platforms": ["github-copilot", "claude", "chatgpt"]
    }


def serialize_frontmatter(fm: Dict) -> str:
    """Serialize frontmatter dict to YAML string with proper ordering."""
    # Define field order
    field_order = [
        "title",
        "shortTitle",
        "intro",
        "type",
        "difficulty",
        "audience",
        "platforms",
        "topics",
        "author",
        "version",
        "date",
        "governance_tags",
        "dataClassification",
        "reviewStatus",
        "effectivenessScore"
    ]
    
    # Build ordered dict
    ordered = {}
    
    # Add fields in order
    for field in field_order:
        if field in fm:
            ordered[field] = fm[field]
    
    # Add remaining fields
    for key, value in fm.items():
        if key not in ordered:
            ordered[key] = value
    
    return yaml.dump(ordered, default_flow_style=False, allow_unicode=True, sort_keys=False)


def process_file(filepath: Path, dry_run: bool = False) -> bool:
    """Process a single file. Returns True if changes were made."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ✗ Error reading {filepath}: {e}")
        return False
    
    fm, fm_text, body = extract_frontmatter(content)
    
    if fm is None:
        # No frontmatter - need to create it
        if filepath.name.lower() == "readme.md":
            fm = create_frontmatter_for_readme(filepath)
        else:
            # Extract what we can from content
            fm = {}
            fm = fix_frontmatter(fm, content, filepath)
        
        # Create new content with frontmatter
        new_fm_text = serialize_frontmatter(fm)
        new_content = f"---\n{new_fm_text}---\n{content}"
        
        if not dry_run:
            filepath.write_text(new_content, encoding='utf-8')
            print(f"  ✓ Added frontmatter: {filepath.name}")
        else:
            print(f"  [DRY-RUN] Would add frontmatter: {filepath.name}")
        
        return True
    
    # Fix existing frontmatter
    original_fm = fm.copy()
    fixed_fm = fix_frontmatter(fm, body, filepath)
    
    if fixed_fm != original_fm:
        new_fm_text = serialize_frontmatter(fixed_fm)
        new_content = f"---\n{new_fm_text}---{body}"
        
        if not dry_run:
            filepath.write_text(new_content, encoding='utf-8')
            print(f"  ✓ Fixed frontmatter: {filepath.name}")
        else:
            print(f"  [DRY-RUN] Would fix frontmatter: {filepath.name}")
        
        return True
    
    return False


def main():
    """Main entry point."""
    dry_run = '--dry-run' in sys.argv
    folder = None
    
    for arg in sys.argv[1:]:
        if not arg.startswith('--') and Path(arg).exists():
            folder = arg
            break
        elif not arg.startswith('--'):
            folder = arg
    
    print("=" * 60)
    print("Frontmatter Fixer")
    print("=" * 60)
    
    if dry_run:
        print("DRY RUN MODE - No files will be modified\n")
    
    # Find files to process
    if folder:
        search_path = REPO_ROOT / folder if not Path(folder).is_absolute() else Path(folder)
    else:
        search_path = PROMPTS_DIR
    
    if not search_path.exists():
        print(f"Error: Path not found: {search_path}")
        sys.exit(1)
    
    md_files = list(search_path.rglob("*.md"))
    
    # Filter out index.md files (they have different requirements)
    # But include README.md files that need frontmatter
    files_to_process = [f for f in md_files if f.name != "index.md"]
    
    print(f"Found {len(files_to_process)} markdown files to process.\n")
    
    changed_count = 0
    for filepath in sorted(files_to_process):
        if process_file(filepath, dry_run):
            changed_count += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {changed_count}/{len(files_to_process)} files {'would be ' if dry_run else ''}modified")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
