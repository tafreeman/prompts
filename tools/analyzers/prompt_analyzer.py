#!/usr/bin/env python3
"""
Prompt Analyzer for Prompt Library
Analyzes all prompts against the 5-dimension scoring rubric and generates a scorecard.

Scoring Dimensions (from tools/rubrics/prompt-scoring.yaml):
  - Clarity (25%): Is the prompt unambiguous and easy to understand?
  - Effectiveness (30%): Does it consistently produce quality output?
  - Reusability (20%): Works across different contexts/inputs?
  - Simplicity (15%): Minimal without losing value?
  - Examples (10%): Are examples helpful and realistic?

Usage:
    python tools/analyzers/prompt_analyzer.py --all
    python tools/analyzers/prompt_analyzer.py --folder prompts/developers/
    python tools/analyzers/prompt_analyzer.py --output docs/SCORECARD.md
"""

import argparse
import re
import sys
import yaml
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple

# =============================================================================
# CONSTANTS
# =============================================================================

SCORE_MIN = 1.0
SCORE_MAX = 5.0

# Weights from the rubric
WEIGHTS = {
    "clarity": 0.25,
    "effectiveness": 0.30,
    "reusability": 0.20,
    "simplicity": 0.15,
    "examples": 0.10,
}

RATING_LABELS = {
    (4.5, 5.0): ("⭐⭐⭐⭐⭐", "Excellent"),
    (4.0, 4.4): ("⭐⭐⭐⭐", "Good"),
    (3.0, 3.9): ("⭐⭐⭐", "Acceptable"),
    (2.0, 2.9): ("⭐⭐", "Below Average"),
    (1.0, 1.9): ("⭐", "Poor"),
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class DimensionScore:
    """Score for a single dimension."""
    name: str
    score: float
    weight: float
    weighted_score: float
    rationale: str
    flags: List[str] = field(default_factory=list)


@dataclass
class PromptAnalysis:
    """Complete analysis of a single prompt."""
    file_path: str
    title: str
    category: str
    clarity: DimensionScore
    effectiveness: DimensionScore
    reusability: DimensionScore
    simplicity: DimensionScore
    examples: DimensionScore
    total_score: float
    rating_stars: str
    rating_label: str
    existing_score: Optional[float] = None
    line_count: int = 0
    has_prompt_section: bool = False
    has_variables: bool = False
    has_example: bool = False
    has_tips: bool = False
    is_index: bool = False


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_rating(score: float) -> Tuple[str, str]:
    """Get star rating and label for a score."""
    for (min_score, max_score), (stars, label) in RATING_LABELS.items():
        if min_score <= score <= max_score:
            return stars, label
    return "?", "Unknown"


def extract_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """Extract YAML frontmatter from markdown content."""
    if not content.strip().startswith('---'):
        return None

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None

    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None


def extract_body(content: str) -> str:
    """Extract the body content after frontmatter."""
    if not content.strip().startswith('---'):
        return content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return content

    return parts[2]


def count_lines(content: str) -> int:
    """Count non-empty lines in content."""
    return len([line for line in content.split('\n') if line.strip()])


# =============================================================================
# DIMENSION ANALYZERS
# =============================================================================

def analyze_clarity(frontmatter: Dict, body: str, file_path: str) -> DimensionScore:
    """
    Analyze prompt clarity (25% weight).
    
    Criteria:
    - Purpose clear within 10 seconds?
    - Variables self-explanatory?
    - No ambiguous phrases?
    - Logical structure?
    - Would work for a newcomer?
    """
    score = 3.0  # Start with acceptable baseline
    flags = []
    rationale_parts = []

    # Check for title and intro
    title = frontmatter.get("title", "")
    intro = frontmatter.get("intro", "")
    short_title = frontmatter.get("shortTitle", "")

    if title and len(title) > 5:
        score += 0.3
        rationale_parts.append("Clear title")
    else:
        score -= 0.5
        flags.append("Missing or short title")

    if intro and len(intro) > 20:
        score += 0.4
        rationale_parts.append("Good intro")
    else:
        score -= 0.3
        flags.append("Missing or short intro")

    if short_title:
        score += 0.1
        rationale_parts.append("Has short title")

    # Check for description section
    if "## Description" in body:
        desc_match = re.search(r'## Description\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL)
        if desc_match:
            desc = desc_match.group(1).strip()
            if len(desc) > 50:
                score += 0.3
                rationale_parts.append("Has description")
            elif len(desc) > 0:
                score += 0.1

    # Check for prompt section with clear structure
    if "## Prompt" in body:
        prompt_match = re.search(r'## Prompt\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL)
        if prompt_match:
            prompt_content = prompt_match.group(1)
            if "```" in prompt_content:
                score += 0.3
                rationale_parts.append("Code-fenced prompt")
            else:
                score += 0.1
    else:
        score -= 0.5
        flags.append("No ## Prompt section")

    # Check for variables documentation
    if "## Variables" in body or "## Variable" in body:
        score += 0.3
        rationale_parts.append("Variables documented")
    elif re.search(r'\[[\w_]+\]', body):
        # Has variables but no documentation
        score -= 0.2
        flags.append("Variables used but not documented")

    # Check for logical structure (multiple sections)
    sections = re.findall(r'^## ', body, re.MULTILINE)
    if len(sections) >= 4:
        score += 0.2
        rationale_parts.append(f"{len(sections)} sections")
    elif len(sections) >= 2:
        score += 0.1

    # Clamp score
    score = max(1.0, min(5.0, score))

    return DimensionScore(
        name="Clarity",
        score=round(score, 1),
        weight=WEIGHTS["clarity"],
        weighted_score=round(score * WEIGHTS["clarity"], 2),
        rationale="; ".join(rationale_parts) if rationale_parts else "Basic structure",
        flags=flags
    )


def analyze_effectiveness(frontmatter: Dict, body: str, file_path: str) -> DimensionScore:
    """
    Analyze prompt effectiveness (30% weight).
    
    Criteria:
    - Does the prompt produce consistent outputs?
    - Does it handle edge cases gracefully?
    - Is the output quality meeting expectations?
    - Does it work across different AI platforms?
    """
    score = 3.0  # Start with acceptable baseline
    flags = []
    rationale_parts = []

    # Check for platforms specification (cross-platform compatibility)
    platforms = frontmatter.get("platforms", [])
    if isinstance(platforms, list) and len(platforms) >= 3:
        score += 0.5
        rationale_parts.append(f"Multi-platform ({len(platforms)})")
    elif isinstance(platforms, list) and len(platforms) >= 2:
        score += 0.3
        rationale_parts.append(f"{len(platforms)} platforms")
    elif platforms:
        score += 0.1
    else:
        flags.append("No platforms specified")

    # Check for specific instructions (produces consistent output)
    prompt_match = re.search(r'## Prompt\s*\n+```[\w]*\s*(.*?)```', body, re.DOTALL)
    if prompt_match:
        prompt_text = prompt_match.group(1)

        # Check for formatting instructions
        if any(fmt in prompt_text.lower() for fmt in
               ["format", "structure", "output as", "respond with", "provide:", "include:"]):
            score += 0.4
            rationale_parts.append("Has format instructions")

        # Check for role/persona
        if any(role in prompt_text.lower() for role in ["you are", "act as", "role:", "persona"]):
            score += 0.3
            rationale_parts.append("Has role definition")

        # Check for constraints
        if any(constraint in prompt_text.lower() for constraint in
               ["constraint", "must", "should", "require", "ensure", "avoid", "don't"]):
            score += 0.3
            rationale_parts.append("Has constraints")

        # Check prompt length (too short may be ineffective)
        prompt_lines = len([l for l in prompt_text.split('\n') if l.strip()])
        if prompt_lines >= 10:
            score += 0.2
            rationale_parts.append("Detailed prompt")
        elif prompt_lines < 3:
            score -= 0.3
            flags.append("Very short prompt")

    # Check for difficulty level (proxy for complexity handling)
    difficulty = frontmatter.get("difficulty", "")
    if difficulty:
        rationale_parts.append(f"Difficulty: {difficulty}")

    # Check governance tags (indicates production readiness)
    governance_tags = frontmatter.get("governance_tags", [])
    if governance_tags:
        score += 0.2
        rationale_parts.append("Has governance tags")

    # Clamp score
    score = max(1.0, min(5.0, score))

    return DimensionScore(
        name="Effectiveness",
        score=round(score, 1),
        weight=WEIGHTS["effectiveness"],
        weighted_score=round(score * WEIGHTS["effectiveness"], 2),
        rationale="; ".join(rationale_parts) if rationale_parts else "Standard prompt",
        flags=flags
    )


def analyze_reusability(frontmatter: Dict, body: str, file_path: str) -> DimensionScore:
    """
    Analyze prompt reusability (20% weight).
    
    Criteria:
    - Can this prompt be used for similar tasks?
    - Are variables generic enough for multiple use cases?
    - Does it require significant modification per use?
    - Would other teams find this useful?
    """
    score = 3.0  # Start with acceptable baseline
    flags = []
    rationale_parts = []

    # Check for variables (indicates customizability)
    variables_section = "## Variables" in body or "## Variable" in body
    variable_pattern = re.findall(r'\[[\w_-]+\]', body)
    unique_vars = list(set(variable_pattern))

    if len(unique_vars) >= 5:
        score += 0.5
        rationale_parts.append(f"{len(unique_vars)} variables")
    elif len(unique_vars) >= 3:
        score += 0.3
        rationale_parts.append(f"{len(unique_vars)} variables")
    elif len(unique_vars) >= 1:
        score += 0.1
    else:
        score -= 0.3
        flags.append("No variables - limited reusability")

    # Check for documented variables
    if variables_section and unique_vars:
        score += 0.3
        rationale_parts.append("Variables documented")

    # Check topics (indicates applicability breadth)
    topics = frontmatter.get("topics", [])
    if isinstance(topics, list) and len(topics) >= 3:
        score += 0.3
        rationale_parts.append(f"{len(topics)} topics")
    elif isinstance(topics, list) and len(topics) >= 1:
        score += 0.1

    # Check audience (broader audience = more reusable)
    audience = frontmatter.get("audience", [])
    if isinstance(audience, list) and len(audience) >= 3:
        score += 0.3
        rationale_parts.append("Broad audience")
    elif isinstance(audience, list) and len(audience) >= 2:
        score += 0.2

    # Check for use cases section
    if "## Use Cases" in body or "## When to Use" in body:
        score += 0.3
        rationale_parts.append("Has use cases")

    # Check for variations
    if "## Variation" in body or "### Variation" in body:
        score += 0.2
        rationale_parts.append("Has variations")

    # Clamp score
    score = max(1.0, min(5.0, score))

    return DimensionScore(
        name="Reusability",
        score=round(score, 1),
        weight=WEIGHTS["reusability"],
        weighted_score=round(score * WEIGHTS["reusability"], 2),
        rationale="; ".join(rationale_parts) if rationale_parts else "Standard reusability",
        flags=flags
    )


def analyze_simplicity(frontmatter: Dict, body: str, file_path: str, line_count: int) -> DimensionScore:
    """
    Analyze prompt simplicity (15% weight).
    
    Criteria:
    - Can any section be removed without losing value?
    - Is the prompt length appropriate for its purpose?
    - Are there redundant instructions?
    - Does it follow the minimal structure template?
    """
    score = 3.0  # Start with acceptable baseline
    flags = []
    rationale_parts = []

    # Check line count (target <100 lines for simple prompts)
    if line_count <= 80:
        score += 0.6
        rationale_parts.append(f"Concise ({line_count} lines)")
    elif line_count <= 120:
        score += 0.3
        rationale_parts.append(f"Moderate length ({line_count} lines)")
    elif line_count <= 200:
        # Acceptable
        rationale_parts.append(f"{line_count} lines")
    elif line_count <= 300:
        score -= 0.3
        flags.append(f"Long ({line_count} lines)")
    else:
        score -= 0.6
        flags.append(f"Very long ({line_count} lines)")

    # Check for changelog (should be removed per standards)
    if "## Changelog" in body or "### Changelog" in body:
        score -= 0.5
        flags.append("Has changelog (should be removed)")

    # Check for redundant sections
    sections = re.findall(r'^## (.+)$', body, re.MULTILINE)
    section_count = len(sections)

    if section_count <= 6:
        score += 0.3
        rationale_parts.append(f"{section_count} sections")
    elif section_count <= 10:
        rationale_parts.append(f"{section_count} sections")
    else:
        score -= 0.2
        flags.append(f"Many sections ({section_count})")

    # Check tips count (max 5 recommended)
    tips_match = re.search(r'## Tips\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL)
    if tips_match:
        tips_content = tips_match.group(1)
        tips_count = len(re.findall(r'^-\s+', tips_content, re.MULTILINE))
        if tips_count <= 5:
            score += 0.2
            rationale_parts.append(f"{tips_count} tips")
        else:
            score -= 0.1
            flags.append(f"Many tips ({tips_count}>5)")

    # Check related prompts count (max 3 recommended)
    related_match = re.search(r'## Related\s*(?:Prompts)?\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL)
    if related_match:
        related_content = related_match.group(1)
        related_count = len(re.findall(r'^-\s+', related_content, re.MULTILINE))
        if related_count <= 3:
            score += 0.1
        else:
            score -= 0.1
            flags.append(f"Many related prompts ({related_count}>3)")

    # Clamp score
    score = max(1.0, min(5.0, score))

    return DimensionScore(
        name="Simplicity",
        score=round(score, 1),
        weight=WEIGHTS["simplicity"],
        weighted_score=round(score * WEIGHTS["simplicity"], 2),
        rationale="; ".join(rationale_parts) if rationale_parts else "Standard complexity",
        flags=flags
    )


def analyze_examples(frontmatter: Dict, body: str, file_path: str) -> DimensionScore:
    """
    Analyze prompt examples quality (10% weight).
    
    Criteria:
    - Do examples show realistic use cases?
    - Is input/output clearly demonstrated?
    - Are examples comprehensive enough?
    - Do examples help understand edge cases?
    """
    score = 2.5  # Start below acceptable (many prompts lack good examples)
    flags = []
    rationale_parts = []

    # Check for example section
    has_example = ("## Example" in body or "## Example Usage" in body or
                   "### Example" in body)

    if has_example:
        score += 0.5
        rationale_parts.append("Has example section")

        # Check for input/output structure
        example_match = re.search(r'## Example(?:\s+Usage)?\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL)
        if example_match:
            example_content = example_match.group(1)

            # Check for input
            has_input = ("**Input**" in example_content or "**Input:**" in example_content or
                         "Input:" in example_content)
            if has_input:
                score += 0.4
                rationale_parts.append("Has input")

            # Check for output
            has_output = ("**Output**" in example_content or "**Output:**" in example_content or
                          "Output:" in example_content)
            if has_output:
                score += 0.4
                rationale_parts.append("Has output")

            # Check for code blocks in examples
            if "```" in example_content:
                score += 0.3
                rationale_parts.append("Code-fenced examples")

            # Check example length (substantive examples)
            example_lines = len([l for l in example_content.split('\n') if l.strip()])
            if example_lines >= 15:
                score += 0.3
                rationale_parts.append("Detailed example")
            elif example_lines >= 5:
                score += 0.1
    else:
        flags.append("No example section")

    # Check for use cases (also demonstrates usage)
    if "## Use Cases" in body:
        score += 0.2
        rationale_parts.append("Has use cases")

    # Check for variations (additional examples)
    if "## Variation" in body:
        score += 0.2
        rationale_parts.append("Has variations")

    # Clamp score
    score = max(1.0, min(5.0, score))

    return DimensionScore(
        name="Examples",
        score=round(score, 1),
        weight=WEIGHTS["examples"],
        weighted_score=round(score * WEIGHTS["examples"], 2),
        rationale="; ".join(rationale_parts) if rationale_parts else "Limited examples",
        flags=flags
    )


# =============================================================================
# MAIN ANALYZER
# =============================================================================

def analyze_prompt(file_path: Path) -> Optional[PromptAnalysis]:
    """Analyze a single prompt file and return complete analysis."""
    # Skip non-markdown files
    if file_path.suffix != '.md':
        return None

    # Check if it's an index/README file
    is_index = file_path.name.lower() in ['index.md', 'readme.md']

    # Read file
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return None

    # Extract frontmatter and body
    frontmatter = extract_frontmatter(content) or {}
    body = extract_body(content)
    line_count = count_lines(content)

    # Get basic info
    title = frontmatter.get("title", file_path.stem.replace("-", " ").title())
    category = file_path.parent.name

    # Get existing score if present
    existing_score = frontmatter.get("effectivenessScore")
    if existing_score:
        try:
            existing_score = float(existing_score)
        except (ValueError, TypeError):
            existing_score = None

    # For index/README files, provide minimal analysis
    if is_index:
        # Simplified scoring for index files
        return PromptAnalysis(
            file_path=str(file_path),
            title=title,
            category=category,
            clarity=DimensionScore("Clarity", 3.0, 0.25, 0.75, "Index file", []),
            effectiveness=DimensionScore("Effectiveness", 3.0, 0.30, 0.90, "Index file", []),
            reusability=DimensionScore("Reusability", 3.0, 0.20, 0.60, "Index file", []),
            simplicity=DimensionScore("Simplicity", 3.0, 0.15, 0.45, "Index file", []),
            examples=DimensionScore("Examples", 3.0, 0.10, 0.30, "Index file", []),
            total_score=3.0,
            rating_stars="⭐⭐⭐",
            rating_label="Acceptable",
            existing_score=existing_score,
            line_count=line_count,
            has_prompt_section=False,
            has_variables=False,
            has_example=False,
            has_tips=False,
            is_index=True
        )

    # Analyze each dimension
    clarity = analyze_clarity(frontmatter, body, str(file_path))
    effectiveness = analyze_effectiveness(frontmatter, body, str(file_path))
    reusability = analyze_reusability(frontmatter, body, str(file_path))
    simplicity = analyze_simplicity(frontmatter, body, str(file_path), line_count)
    examples = analyze_examples(frontmatter, body, str(file_path))

    # Calculate total weighted score
    total_score = (clarity.weighted_score + effectiveness.weighted_score +
                   reusability.weighted_score + simplicity.weighted_score +
                   examples.weighted_score)
    total_score = round(total_score, 1)

    # Get rating
    rating_stars, rating_label = get_rating(total_score)

    return PromptAnalysis(
        file_path=str(file_path),
        title=title,
        category=category,
        clarity=clarity,
        effectiveness=effectiveness,
        reusability=reusability,
        simplicity=simplicity,
        examples=examples,
        total_score=total_score,
        rating_stars=rating_stars,
        rating_label=rating_label,
        existing_score=existing_score,
        line_count=line_count,
        has_prompt_section="## Prompt" in body,
        has_variables="## Variables" in body,
        has_example="## Example" in body,
        has_tips="## Tips" in body,
        is_index=False
    )


def analyze_folder(folder_path: Path) -> List[PromptAnalysis]:
    """Analyze all markdown files in a folder recursively."""
    results = []
    for md_file in sorted(folder_path.rglob("*.md")):
        analysis = analyze_prompt(md_file)
        if analysis:
            results.append(analysis)
    return results


# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

def generate_scorecard(results: List[PromptAnalysis], output_path: Optional[Path] = None) -> str:
    """Generate a comprehensive scorecard in markdown format."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Filter out index files for main analysis
    prompts = [r for r in results if not r.is_index]
    indexes = [r for r in results if r.is_index]

    # Calculate summary statistics
    total = len(prompts)
    avg_score = sum(p.total_score for p in prompts) / total if total > 0 else 0
    avg_clarity = sum(p.clarity.score for p in prompts) / total if total > 0 else 0
    avg_effectiveness = sum(p.effectiveness.score for p in prompts) / total if total > 0 else 0
    avg_reusability = sum(p.reusability.score for p in prompts) / total if total > 0 else 0
    avg_simplicity = sum(p.simplicity.score for p in prompts) / total if total > 0 else 0
    avg_examples = sum(p.examples.score for p in prompts) / total if total > 0 else 0

    # Count by rating
    rating_counts = {}
    for p in prompts:
        label = p.rating_label
        rating_counts[label] = rating_counts.get(label, 0) + 1

    # Group by category
    by_category = {}
    for p in prompts:
        cat = p.category
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(p)

    # Build scorecard markdown
    lines = [
        "# Prompt Library Scorecard",
        "",
        f"**Generated**: {now}  ",
        f"**Scoring Rubric**: [`tools/rubrics/prompt-scoring.yaml`](../tools/rubrics/prompt-scoring.yaml)  ",
        f"**Total Prompts Analyzed**: {total}",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| **Total Prompts** | {total} |",
        f"| **Average Score** | {avg_score:.2f} |",
        f"| **Excellent (4.5-5.0)** | {rating_counts.get('Excellent', 0)} ({rating_counts.get('Excellent', 0)/total*100:.1f}%) |",
        f"| **Good (4.0-4.4)** | {rating_counts.get('Good', 0)} ({rating_counts.get('Good', 0)/total*100:.1f}%) |",
        f"| **Acceptable (3.0-3.9)** | {rating_counts.get('Acceptable', 0)} ({rating_counts.get('Acceptable', 0)/total*100:.1f}%) |",
        f"| **Below Average (2.0-2.9)** | {rating_counts.get('Below Average', 0)} ({rating_counts.get('Below Average', 0)/total*100:.1f}%) |",
        f"| **Poor (1.0-1.9)** | {rating_counts.get('Poor', 0)} ({rating_counts.get('Poor', 0)/total*100:.1f}%) |",
        "",
        "## Dimension Averages",
        "",
        "| Dimension | Weight | Average Score |",
        "|-----------|--------|---------------|",
        f"| **Clarity** | 25% | {avg_clarity:.2f} |",
        f"| **Effectiveness** | 30% | {avg_effectiveness:.2f} |",
        f"| **Reusability** | 20% | {avg_reusability:.2f} |",
        f"| **Simplicity** | 15% | {avg_simplicity:.2f} |",
        f"| **Examples** | 10% | {avg_examples:.2f} |",
        "",
        "---",
        "",
        "## Category Summary",
        "",
        "| Category | Count | Avg Score | Top Rating |",
        "|----------|-------|-----------|------------|",
    ]

    for cat in sorted(by_category.keys()):
        cat_prompts = by_category[cat]
        cat_count = len(cat_prompts)
        cat_avg = sum(p.total_score for p in cat_prompts) / cat_count
        cat_top = max(p.total_score for p in cat_prompts)
        _, cat_top_label = get_rating(cat_top)
        lines.append(f"| **{cat}** | {cat_count} | {cat_avg:.2f} | {cat_top_label} ({cat_top:.1f}) |")

    lines.extend([
        "",
        "---",
        "",
        "## Detailed Scores by Category",
        "",
    ])

    # Add detailed tables by category
    for cat in sorted(by_category.keys()):
        cat_prompts = sorted(by_category[cat], key=lambda x: x.total_score, reverse=True)

        lines.extend([
            f"### {cat.title()} ({len(cat_prompts)} prompts)",
            "",
            "| Prompt | Score | Rating | Clarity | Effect. | Reuse | Simple | Examples |",
            "|--------|-------|--------|---------|---------|-------|--------|----------|",
        ])

        for p in cat_prompts:
            # Create relative path link
            rel_path = Path(p.file_path).relative_to(Path(p.file_path).parents[2])
            link = f"[{p.title[:40]}](../{rel_path})"
            lines.append(
                f"| {link} | **{p.total_score}** | {p.rating_stars} | "
                f"{p.clarity.score} | {p.effectiveness.score} | {p.reusability.score} | "
                f"{p.simplicity.score} | {p.examples.score} |"
            )

        lines.append("")

    # Add prompts needing improvement
    needs_improvement = [p for p in prompts if p.total_score < 3.0]
    if needs_improvement:
        lines.extend([
            "---",
            "",
            "## ⚠️ Prompts Needing Improvement",
            "",
            "These prompts scored below 3.0 and should be reviewed:",
            "",
        ])
        for p in sorted(needs_improvement, key=lambda x: x.total_score):
            all_flags = (p.clarity.flags + p.effectiveness.flags +
                         p.reusability.flags + p.simplicity.flags + p.examples.flags)
            flags_str = ", ".join(all_flags[:3]) if all_flags else "General improvements needed"
            lines.append(f"- **{p.title}** ({p.total_score}): {flags_str}")
        lines.append("")

    # Add top performers
    top_performers = [p for p in prompts if p.total_score >= 4.5]
    if top_performers:
        lines.extend([
            "---",
            "",
            "## ⭐ Top Performers",
            "",
            "These prompts scored 4.5 or higher and can serve as examples:",
            "",
        ])
        for p in sorted(top_performers, key=lambda x: x.total_score, reverse=True):
            lines.append(f"- **{p.title}** ({p.total_score}): {p.clarity.rationale}")
        lines.append("")

    # Add scoring methodology note
    lines.extend([
        "---",
        "",
        "## Scoring Methodology",
        "",
        "Each prompt is analyzed against 5 dimensions with weighted scoring:",
        "",
        "1. **Clarity (25%)**: Clear title, intro, description, variables documented",
        "2. **Effectiveness (30%)**: Multi-platform, format instructions, role definition, constraints",
        "3. **Reusability (20%)**: Variable count, documentation, broad topics/audience",
        "4. **Simplicity (15%)**: Line count, section count, no redundant content",
        "5. **Examples (10%)**: Has examples with input/output, code-fenced, detailed",
        "",
        "**Rating Scale**:",
        "- ⭐⭐⭐⭐⭐ Excellent (4.5-5.0): Production-ready, high-quality",
        "- ⭐⭐⭐⭐ Good (4.0-4.4): High-quality, ready for use",
        "- ⭐⭐⭐ Acceptable (3.0-3.9): Functional, meets minimum standards",
        "- ⭐⭐ Below Average (2.0-2.9): Needs improvement",
        "- ⭐ Poor (1.0-1.9): Significant issues, requires major rewrite",
        "",
        "---",
        "",
        f"*Last updated: {now}*",
    ])

    content = "\n".join(lines)

    # Write to file if path provided
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')
        print(f"✅ Scorecard written to {output_path}")

    return content


def print_summary(results: List[PromptAnalysis]):
    """Print summary statistics to console."""
    prompts = [r for r in results if not r.is_index]
    total = len(prompts)

    if total == 0:
        print("No prompts found to analyze.")
        return

    avg_score = sum(p.total_score for p in prompts) / total
    rating_counts = {}
    for p in prompts:
        label = p.rating_label
        rating_counts[label] = rating_counts.get(label, 0) + 1

    print("\n" + "=" * 60)
    print("PROMPT ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Total prompts:     {total}")
    print(f"Average score:     {avg_score:.2f}")
    print()
    print("Distribution:")
    for label in ["Excellent", "Good", "Acceptable", "Below Average", "Poor"]:
        count = rating_counts.get(label, 0)
        pct = (count / total) * 100 if total else 0
        bar = "█" * int(pct / 5)
        print(f"  {label:<15} {count:>3} ({pct:>5.1f}%) {bar}")
    print("=" * 60)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Analyze prompts against the 5-dimension scoring rubric"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to a single markdown file to analyze"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Analyze all prompts in the repository"
    )
    parser.add_argument(
        "--folder",
        type=str,
        help="Analyze all files in a specific folder"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="docs/SCORECARD.md",
        help="Output path for the scorecard (default: docs/SCORECARD.md)"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary statistics to console"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output for each file"
    )

    args = parser.parse_args()

    results = []

    if args.file:
        # Single file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}")
            return 1
        analysis = analyze_prompt(file_path)
        if analysis:
            results = [analysis]

    elif args.folder:
        # Folder
        folder_path = Path(args.folder)
        if not folder_path.exists():
            print(f"Error: Folder not found: {args.folder}")
            return 1
        results = analyze_folder(folder_path)

    elif args.all:
        # All prompts
        prompts_path = Path(__file__).parent.parent.parent / "prompts"
        if prompts_path.exists():
            results = analyze_folder(prompts_path)
        else:
            print(f"Error: prompts folder not found at {prompts_path}")
            return 1

    else:
        parser.print_help()
        return 0

    if not results:
        print("No prompts found to analyze.")
        return 1

    # Generate scorecard
    output_path = Path(args.output)
    generate_scorecard(results, output_path)

    # Print verbose output if requested
    if args.verbose:
        print("\nDetailed Analysis:")
        for r in results:
            print(f"\n{r.file_path}")
            print(f"  Score: {r.total_score} {r.rating_stars} ({r.rating_label})")
            print(f"  Clarity: {r.clarity.score} - {r.clarity.rationale}")
            print(f"  Effectiveness: {r.effectiveness.score} - {r.effectiveness.rationale}")
            print(f"  Reusability: {r.reusability.score} - {r.reusability.rationale}")
            print(f"  Simplicity: {r.simplicity.score} - {r.simplicity.rationale}")
            print(f"  Examples: {r.examples.score} - {r.examples.rationale}")

    # Print summary
    if args.summary or args.all:
        print_summary(results)

    return 0


if __name__ == "__main__":
    sys.exit(main())
