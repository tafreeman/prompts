#!/usr/bin/env python3
"""
Unified Prompt Library Evaluator
Combines both rubrics to provide comprehensive scoring:
  1. Quality Standards (quality_standards.json) - Tier scoring (0-100)
  2. Effectiveness Rubric (prompt-scoring.yaml) - 5-dimension scoring (1.0-5.0)

This tool evaluates actual prompt files only, excluding agent files, instruction files,
and other non-prompt markdown content.

Usage:
    python evaluate_library.py --all
    python evaluate_library.py --folder prompts/developers/
    python evaluate_library.py prompts/path/to/prompt.md
    python evaluate_library.py --all --output evaluation_report.md
"""

import argparse
import json
import re
import sys
import yaml
import fnmatch
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple

# =============================================================================
# FILE FILTERING - Only process actual prompt files
# =============================================================================

EXCLUDED_PATTERNS = [
    '*.agent.md', '*.instructions.md', 'index.md', 'README.md',
    '.github/**/*', 'docs/**/*', 'CONTRIBUTING.md', 'SECURITY.md',
    'LICENSE', 'agents/**/*', 'templates/**/*', '**/archive/**/*',
]

EXCLUDED_DIRS = {
    '.git', 'node_modules', '__pycache__', 'bin', 'obj',
    '.venv', 'venv', 'docs', 'agents', '.github', 'templates', 'archive',
}


def should_exclude_file(file_path: Path, root_dir: Path) -> bool:
    """Determine if a file should be excluded from evaluation."""
    try:
        rel_path = str(file_path.relative_to(root_dir)).replace('\\', '/')
    except ValueError:
        rel_path = file_path.name
    
    filename = file_path.name
    
    for pattern in EXCLUDED_PATTERNS:
        if fnmatch.fnmatch(filename, pattern) or fnmatch.fnmatch(rel_path, pattern):
            return True
    
    if any(part in EXCLUDED_DIRS for part in file_path.parts):
        return True
    
    return False


def find_prompt_files(root_dir: Path) -> List[Path]:
    """Find all prompt files, excluding non-prompt content."""
    files = []
    for md_file in sorted(root_dir.rglob("*.md")):
        if not should_exclude_file(md_file, root_dir):
            files.append(md_file)
    return files


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class QualityScore:
    """Score from quality_standards.json rubric (0-100 scale)"""
    completeness: float = 0.0
    example_quality: float = 0.0
    specificity: float = 0.0
    format_adherence: float = 0.0
    enterprise_quality: float = 0.0
    total: float = 0.0
    tier: str = "Tier 4"
    issues: List[str] = field(default_factory=list)


@dataclass
class EffectivenessScore:
    """Score from prompt-scoring.yaml rubric (1.0-5.0 scale)"""
    clarity: float = 3.0
    effectiveness: float = 3.0
    reusability: float = 3.0
    simplicity: float = 3.0
    examples: float = 3.0
    total: float = 3.0
    rating: str = "⭐⭐⭐ Acceptable"
    flags: List[str] = field(default_factory=list)


@dataclass
class UnifiedEvaluation:
    """Combined evaluation result from both rubrics"""
    file_path: str
    title: str
    category: str
    quality_score: QualityScore
    effectiveness_score: EffectivenessScore
    combined_grade: str = ""
    recommendation: str = ""
    priority: int = 0  # 1=critical, 2=high, 3=medium, 4=low


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

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
    return parts[2] if len(parts) >= 3 else content


def get_effectiveness_rating(score: float) -> str:
    """Get star rating for effectiveness score."""
    if score >= 4.5:
        return "⭐⭐⭐⭐⭐ Excellent"
    elif score >= 4.0:
        return "⭐⭐⭐⭐ Good"
    elif score >= 3.0:
        return "⭐⭐⭐ Acceptable"
    elif score >= 2.0:
        return "⭐⭐ Below Average"
    else:
        return "⭐ Poor"


def get_quality_tier(score: float) -> str:
    """Get tier label for quality score."""
    if score >= 90:
        return "Tier 1 (Excellent)"
    elif score >= 75:
        return "Tier 2 (Good)"
    elif score >= 60:
        return "Tier 3 (Acceptable)"
    else:
        return "Tier 4 (Poor)"


# =============================================================================
# RUBRIC 1: QUALITY STANDARDS (0-100)
# =============================================================================

def evaluate_quality_standards(frontmatter: Dict, body: str, file_path: str) -> QualityScore:
    """
    Evaluate against quality_standards.json rubric.
    
    Criteria:
      - Completeness (25%): All required sections present
      - Example Quality (30%): Realistic, detailed examples
      - Specificity (20%): Domain-specific, actionable content
      - Format Adherence (15%): Valid YAML, correct markdown
      - Enterprise Quality (10%): Professional, references frameworks
    """
    score = QualityScore()
    
    # === COMPLETENESS (25 points) ===
    completeness = 0
    completeness_max = 25
    
    # Check frontmatter fields
    required_fm = ['title', 'difficulty', 'version', 'date']
    fm_present = sum(1 for f in required_fm if f in frontmatter)
    completeness += (fm_present / len(required_fm)) * 5
    
    # Check sections
    sections_to_check = [
        ('## Description', 3),
        ('## Prompt', 5),
        ('## Variables', 3),
        ('## Example', 4),
        ('## Tips', 2),
        ('## Related', 2),
        ('## Use Cases', 1),
    ]
    for section, points in sections_to_check:
        if section.lower() in body.lower():
            completeness += points
    
    score.completeness = min(completeness_max, completeness)
    if score.completeness < 15:
        score.issues.append("Missing required sections (Description, Prompt, Variables, Example)")
    
    # === EXAMPLE QUALITY (30 points) ===
    example_quality = 0
    example_max = 30
    
    # Check for example section
    example_match = re.search(r'## Example(?:\s+Usage)?\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
    if example_match:
        example_content = example_match.group(1)
        example_lines = len([l for l in example_content.split('\n') if l.strip()])
        
        # Length check (>150 lines = full points, scale down)
        if example_lines >= 150:
            example_quality += 10
        elif example_lines >= 50:
            example_quality += 7
        elif example_lines >= 20:
            example_quality += 4
        else:
            example_quality += 2
            score.issues.append("Example section too short (<20 lines)")
        
        # Has input/output
        if '**Input**' in example_content or 'Input:' in example_content:
            example_quality += 5
        if '**Output**' in example_content or 'Output:' in example_content:
            example_quality += 5
        
        # Has metrics/data
        if re.search(r'\$[\d,]+|\d+%|\d+\s*(hours?|days?|minutes?)', example_content):
            example_quality += 5
            
        # No placeholder text
        if 'placeholder' not in example_content.lower() and '[replace' not in example_content.lower():
            example_quality += 5
        else:
            score.issues.append("Example contains placeholder text")
    else:
        score.issues.append("Missing Example section")
    
    score.example_quality = min(example_max, example_quality)
    
    # === SPECIFICITY (20 points) ===
    specificity = 0
    specificity_max = 20
    
    # Check tips section for actionable content
    tips_match = re.search(r'## Tips\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
    if tips_match:
        tips_content = tips_match.group(1)
        tips_count = len(re.findall(r'^[-*]\s+', tips_content, re.MULTILINE))
        if tips_count >= 5:
            specificity += 6
        elif tips_count >= 3:
            specificity += 4
        elif tips_count >= 1:
            specificity += 2
        
        # Check for generic phrases (penalize)
        generic_phrases = ['check your work', 'be careful', 'make sure', 'double check']
        generic_count = sum(1 for p in generic_phrases if p in tips_content.lower())
        if generic_count == 0:
            specificity += 4
    
    # Check variables for realistic values
    vars_match = re.search(r'## Variables?\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
    if vars_match:
        vars_content = vars_match.group(1)
        # Has example values
        if 'example' in vars_content.lower() or ':' in vars_content:
            specificity += 5
    
    # Use cases are concrete
    use_cases_match = re.search(r'## Use Cases?\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
    if use_cases_match:
        use_cases_content = use_cases_match.group(1)
        use_case_count = len(re.findall(r'^[-*\d.]\s+', use_cases_content, re.MULTILINE))
        if use_case_count >= 5:
            specificity += 5
        elif use_case_count >= 3:
            specificity += 3
    
    score.specificity = min(specificity_max, specificity)
    if score.specificity < 10:
        score.issues.append("Content lacks specificity (generic tips, missing use cases)")
    
    # === FORMAT ADHERENCE (15 points) ===
    format_score = 0
    format_max = 15
    
    # Valid frontmatter
    if frontmatter:
        format_score += 5
    else:
        score.issues.append("Invalid or missing YAML frontmatter")
    
    # Has H1 heading
    if re.search(r'^# ', body, re.MULTILINE):
        format_score += 3
    
    # Has H2 sections
    h2_count = len(re.findall(r'^## ', body, re.MULTILINE))
    if h2_count >= 4:
        format_score += 4
    elif h2_count >= 2:
        format_score += 2
    
    # Uses square-bracket variables consistently
    if re.search(r'\[[\w_-]+\]', body):
        format_score += 3
    
    score.format_adherence = min(format_max, format_score)
    
    # === ENTERPRISE QUALITY (10 points) ===
    enterprise = 0
    enterprise_max = 10
    
    # References frameworks
    frameworks = ['iso', 'pmi', 'nist', 'owasp', 'itil', 'cobit', 'togaf', 'safe', 'agile']
    framework_count = sum(1 for f in frameworks if f in body.lower())
    if framework_count >= 2:
        enterprise += 4
    elif framework_count >= 1:
        enterprise += 2
    
    # Professional tone (no casual language)
    casual_phrases = ["let's", "gonna", "wanna", "kinda", "btw", "fyi"]
    casual_count = sum(1 for p in casual_phrases if p in body.lower())
    if casual_count == 0:
        enterprise += 3
    
    # Has governance tags
    if frontmatter.get('governance_tags'):
        enterprise += 3
    
    score.enterprise_quality = min(enterprise_max, enterprise)
    
    # === TOTAL ===
    score.total = round(
        score.completeness + score.example_quality + score.specificity +
        score.format_adherence + score.enterprise_quality, 1
    )
    score.tier = get_quality_tier(score.total)
    
    return score


# =============================================================================
# RUBRIC 2: EFFECTIVENESS SCORE (1.0-5.0)
# =============================================================================

def evaluate_effectiveness(frontmatter: Dict, body: str, file_path: str) -> EffectivenessScore:
    """
    Evaluate against prompt-scoring.yaml rubric.
    
    Dimensions:
      - Clarity (25%): Unambiguous, easy to understand
      - Effectiveness (30%): Produces quality output consistently
      - Reusability (20%): Works across contexts
      - Simplicity (15%): Minimal without losing value
      - Examples (10%): Helpful and realistic
    """
    score = EffectivenessScore()
    
    # === CLARITY (weight: 0.25) ===
    clarity = 3.0  # baseline
    
    # Title and intro
    if frontmatter.get('title') and len(str(frontmatter['title'])) > 5:
        clarity += 0.3
    if frontmatter.get('intro') and len(str(frontmatter['intro'])) > 20:
        clarity += 0.4
    if frontmatter.get('shortTitle'):
        clarity += 0.1
    
    # Has description
    if '## description' in body.lower():
        clarity += 0.3
    
    # Prompt section with code fence
    if '## prompt' in body.lower():
        if '```' in body:
            clarity += 0.4
        else:
            clarity += 0.2
    else:
        clarity -= 0.5
        score.flags.append("No ## Prompt section")
    
    # Variables documented
    if '## variable' in body.lower():
        clarity += 0.3
    elif re.search(r'\[[\w_]+\]', body):
        clarity -= 0.2
        score.flags.append("Variables used but not documented")
    
    score.clarity = round(max(1.0, min(5.0, clarity)), 1)
    
    # === EFFECTIVENESS (weight: 0.30) ===
    effectiveness = 3.0  # baseline
    
    # Multi-platform support
    platforms = frontmatter.get('platforms', [])
    if isinstance(platforms, list):
        if len(platforms) >= 3:
            effectiveness += 0.5
        elif len(platforms) >= 2:
            effectiveness += 0.3
        elif len(platforms) >= 1:
            effectiveness += 0.1
    
    # Format instructions in prompt
    prompt_match = re.search(r'## Prompt\s*\n+```[\w]*\s*(.*?)```', body, re.DOTALL | re.IGNORECASE)
    if prompt_match:
        prompt_text = prompt_match.group(1).lower()
        if any(f in prompt_text for f in ['format', 'structure', 'output as', 'respond with']):
            effectiveness += 0.4
        if any(r in prompt_text for r in ['you are', 'act as', 'role:']):
            effectiveness += 0.3
        if any(c in prompt_text for c in ['must', 'should', 'require', 'ensure', 'avoid']):
            effectiveness += 0.3
    
    # Governance tags (production readiness)
    if frontmatter.get('governance_tags'):
        effectiveness += 0.2
    
    score.effectiveness = round(max(1.0, min(5.0, effectiveness)), 1)
    
    # === REUSABILITY (weight: 0.20) ===
    reusability = 3.0  # baseline
    
    # Variable count
    unique_vars = set(re.findall(r'\[[\w_-]+\]', body))
    if len(unique_vars) >= 5:
        reusability += 0.5
    elif len(unique_vars) >= 3:
        reusability += 0.3
    elif len(unique_vars) >= 1:
        reusability += 0.1
    else:
        reusability -= 0.3
        score.flags.append("No variables - limited reusability")
    
    # Broad audience
    audience = frontmatter.get('audience', [])
    if isinstance(audience, list) and len(audience) >= 3:
        reusability += 0.3
    elif isinstance(audience, list) and len(audience) >= 2:
        reusability += 0.2
    
    # Has use cases
    if '## use case' in body.lower():
        reusability += 0.3
    
    # Has variations
    if '## variation' in body.lower():
        reusability += 0.2
    
    score.reusability = round(max(1.0, min(5.0, reusability)), 1)
    
    # === SIMPLICITY (weight: 0.15) ===
    simplicity = 3.0  # baseline
    
    # Line count
    line_count = len([l for l in body.split('\n') if l.strip()])
    if line_count <= 80:
        simplicity += 0.6
    elif line_count <= 120:
        simplicity += 0.3
    elif line_count > 300:
        simplicity -= 0.6
        score.flags.append(f"Very long ({line_count} lines)")
    elif line_count > 200:
        simplicity -= 0.3
    
    # No changelog (should be removed)
    if '## changelog' in body.lower():
        simplicity -= 0.5
        score.flags.append("Has changelog (should be removed)")
    
    # Section count
    section_count = len(re.findall(r'^## ', body, re.MULTILINE))
    if section_count <= 6:
        simplicity += 0.3
    elif section_count > 10:
        simplicity -= 0.2
    
    score.simplicity = round(max(1.0, min(5.0, simplicity)), 1)
    
    # === EXAMPLES (weight: 0.10) ===
    examples = 2.5  # lower baseline (many prompts lack good examples)
    
    if '## example' in body.lower():
        examples += 0.5
        
        example_match = re.search(r'## Example(?:\s+Usage)?\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
        if example_match:
            example_content = example_match.group(1)
            
            if '**Input**' in example_content or 'Input:' in example_content:
                examples += 0.4
            if '**Output**' in example_content or 'Output:' in example_content:
                examples += 0.4
            if '```' in example_content:
                examples += 0.3
            
            example_lines = len([l for l in example_content.split('\n') if l.strip()])
            if example_lines >= 15:
                examples += 0.3
    else:
        score.flags.append("No example section")
    
    score.examples = round(max(1.0, min(5.0, examples)), 1)
    
    # === TOTAL (weighted) ===
    score.total = round(
        score.clarity * 0.25 +
        score.effectiveness * 0.30 +
        score.reusability * 0.20 +
        score.simplicity * 0.15 +
        score.examples * 0.10,
        1
    )
    score.rating = get_effectiveness_rating(score.total)
    
    return score


# =============================================================================
# UNIFIED EVALUATION
# =============================================================================

def evaluate_prompt(file_path: Path) -> Optional[UnifiedEvaluation]:
    """Evaluate a single prompt file against both rubrics."""
    if file_path.suffix != '.md':
        return None
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return None
    
    frontmatter = extract_frontmatter(content) or {}
    body = extract_body(content)
    
    title = frontmatter.get('title', file_path.stem.replace('-', ' ').title())
    category = file_path.parent.name
    
    # Evaluate against both rubrics
    quality = evaluate_quality_standards(frontmatter, body, str(file_path))
    effectiveness = evaluate_effectiveness(frontmatter, body, str(file_path))
    
    # Determine combined grade and recommendation
    if quality.total >= 90 and effectiveness.total >= 4.5:
        combined_grade = "A (Excellent)"
        recommendation = "Feature as recommended prompt"
        priority = 4
    elif quality.total >= 75 and effectiveness.total >= 4.0:
        combined_grade = "B (Good)"
        recommendation = "Production ready"
        priority = 4
    elif quality.total >= 60 and effectiveness.total >= 3.0:
        combined_grade = "C (Acceptable)"
        recommendation = "Usable with optional improvements"
        priority = 3
    elif quality.total >= 45 or effectiveness.total >= 2.5:
        combined_grade = "D (Below Average)"
        recommendation = "Needs improvement before use"
        priority = 2
    else:
        combined_grade = "F (Poor)"
        recommendation = "Major rewrite or deprecate"
        priority = 1
    
    return UnifiedEvaluation(
        file_path=str(file_path),
        title=title,
        category=category,
        quality_score=quality,
        effectiveness_score=effectiveness,
        combined_grade=combined_grade,
        recommendation=recommendation,
        priority=priority
    )


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_report(results: List[UnifiedEvaluation], output_path: Optional[Path] = None) -> str:
    """Generate comprehensive evaluation report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total = len(results)
    
    if total == 0:
        return "No prompts found to evaluate."
    
    # Calculate averages
    avg_quality = sum(r.quality_score.total for r in results) / total
    avg_effectiveness = sum(r.effectiveness_score.total for r in results) / total
    
    # Count by grade
    grade_counts = {}
    for r in results:
        grade = r.combined_grade.split()[0]
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
    
    # Count by tier
    tier_counts = {}
    for r in results:
        tier = r.quality_score.tier.split()[0]
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
    
    # Group by category
    by_category = {}
    for r in results:
        if r.category not in by_category:
            by_category[r.category] = []
        by_category[r.category].append(r)
    
    lines = [
        "# Unified Prompt Library Evaluation Report",
        "",
        f"**Generated**: {now}  ",
        f"**Total Prompts Evaluated**: {total}",
        "",
        "---",
        "",
        "## Scoring Rubrics Used",
        "",
        "This report combines two complementary scoring systems:",
        "",
        "### 1. Quality Standards (0-100 scale)",
        "| Criterion | Weight | Focus |",
        "|-----------|--------|-------|",
        "| Completeness | 25% | All required sections present |",
        "| Example Quality | 30% | Realistic, detailed examples |",
        "| Specificity | 20% | Domain-specific, actionable |",
        "| Format Adherence | 15% | Valid YAML, correct markdown |",
        "| Enterprise Quality | 10% | Professional, frameworks |",
        "",
        "### 2. Effectiveness Score (1.0-5.0 scale)",
        "| Dimension | Weight | Focus |",
        "|-----------|--------|-------|",
        "| Clarity | 25% | Unambiguous, easy to understand |",
        "| Effectiveness | 30% | Produces quality output |",
        "| Reusability | 20% | Works across contexts |",
        "| Simplicity | 15% | Minimal without losing value |",
        "| Examples | 10% | Helpful and realistic |",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| **Total Prompts** | {total} |",
        f"| **Avg Quality Score** | {avg_quality:.1f}/100 |",
        f"| **Avg Effectiveness** | {avg_effectiveness:.2f}/5.0 |",
        "",
        "### Grade Distribution",
        "",
        "| Grade | Count | % |",
        "|-------|-------|---|",
    ]
    
    for grade in ['A', 'B', 'C', 'D', 'F']:
        count = grade_counts.get(grade, 0)
        pct = (count / total) * 100 if total else 0
        lines.append(f"| {grade} | {count} | {pct:.1f}% |")
    
    lines.extend([
        "",
        "### Quality Tier Distribution",
        "",
        "| Tier | Count | % |",
        "|------|-------|---|",
    ])
    
    for tier in ['Tier', 'Tier', 'Tier', 'Tier']:
        for i in range(1, 5):
            tier_key = f"Tier"
            count = tier_counts.get(tier_key, 0)
            # This is a simplification - actual counting would need adjustment
    
    for tier_label in ['Tier 1', 'Tier 2', 'Tier 3', 'Tier 4']:
        tier_key = tier_label.split()[0] + " " + tier_label.split()[1]
        count = sum(1 for r in results if tier_label in r.quality_score.tier)
        pct = (count / total) * 100 if total else 0
        lines.append(f"| {tier_label} | {count} | {pct:.1f}% |")
    
    lines.extend([
        "",
        "---",
        "",
        "## Priority Actions",
        "",
    ])
    
    # Critical priority (F grade)
    critical = [r for r in results if r.priority == 1]
    if critical:
        lines.append("### 🔴 Critical (Rewrite or Deprecate)")
        lines.append("")
        for r in sorted(critical, key=lambda x: x.quality_score.total):
            issues = r.quality_score.issues[:2] if r.quality_score.issues else ["General improvements needed"]
            lines.append(f"- **{r.title}** (Q:{r.quality_score.total:.0f}, E:{r.effectiveness_score.total:.1f})")
            lines.append(f"  - Issues: {'; '.join(issues)}")
        lines.append("")
    
    # High priority (D grade)
    high = [r for r in results if r.priority == 2]
    if high:
        lines.append("### 🟠 High Priority (Needs Improvement)")
        lines.append("")
        for r in sorted(high, key=lambda x: x.quality_score.total)[:10]:
            lines.append(f"- **{r.title}** (Q:{r.quality_score.total:.0f}, E:{r.effectiveness_score.total:.1f})")
        lines.append("")
    
    lines.extend([
        "---",
        "",
        "## Detailed Scores by Category",
        "",
    ])
    
    for cat in sorted(by_category.keys()):
        cat_results = sorted(by_category[cat], key=lambda x: x.quality_score.total, reverse=True)
        cat_avg_q = sum(r.quality_score.total for r in cat_results) / len(cat_results)
        cat_avg_e = sum(r.effectiveness_score.total for r in cat_results) / len(cat_results)
        
        lines.extend([
            f"### {cat.title()} ({len(cat_results)} prompts, Avg Q:{cat_avg_q:.0f}, E:{cat_avg_e:.1f})",
            "",
            "| Prompt | Grade | Quality | Effectiveness | Recommendation |",
            "|--------|-------|---------|---------------|----------------|",
        ])
        
        for r in cat_results:
            title_short = r.title[:35] + "..." if len(r.title) > 35 else r.title
            lines.append(
                f"| {title_short} | {r.combined_grade.split()[0]} | "
                f"{r.quality_score.total:.0f} ({r.quality_score.tier.split('(')[0].strip()}) | "
                f"{r.effectiveness_score.total:.1f} {r.effectiveness_score.rating.split()[0]} | "
                f"{r.recommendation} |"
            )
        
        lines.append("")
    
    lines.extend([
        "---",
        "",
        f"*Report generated: {now}*",
    ])
    
    content = "\n".join(lines)
    
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')
        print(f"✅ Report saved to {output_path}")
    
    return content


def print_summary(results: List[UnifiedEvaluation]):
    """Print summary to console."""
    total = len(results)
    if total == 0:
        print("No prompts found.")
        return
    
    avg_quality = sum(r.quality_score.total for r in results) / total
    avg_effectiveness = sum(r.effectiveness_score.total for r in results) / total
    
    print("\n" + "=" * 70)
    print("UNIFIED EVALUATION SUMMARY")
    print("=" * 70)
    print(f"Total prompts:        {total}")
    print(f"Avg Quality Score:    {avg_quality:.1f}/100")
    print(f"Avg Effectiveness:    {avg_effectiveness:.2f}/5.0")
    print()
    
    # Grade distribution
    grade_counts = {}
    for r in results:
        grade = r.combined_grade.split()[0]
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
    
    print("Grade Distribution:")
    for grade in ['A', 'B', 'C', 'D', 'F']:
        count = grade_counts.get(grade, 0)
        pct = (count / total) * 100
        bar = "█" * int(pct / 5)
        print(f"  {grade}: {count:>3} ({pct:>5.1f}%) {bar}")
    
    print("=" * 70)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Unified prompt evaluation using both Quality Standards and Effectiveness rubrics",
        epilog="""
Examples:
  python evaluate_library.py --all
  python evaluate_library.py --folder prompts/developers/
  python evaluate_library.py prompts/business/budget-tracker.md
  python evaluate_library.py --all --output docs/EVALUATION_REPORT.md
        """
    )
    parser.add_argument("file", nargs="?", help="Single prompt file to evaluate")
    parser.add_argument("--all", action="store_true", help="Evaluate all prompts")
    parser.add_argument("--folder", type=str, help="Evaluate prompts in a specific folder")
    parser.add_argument("--output", "-o", type=str, default="docs/EVALUATION_REPORT.md",
                        help="Output path for report (default: docs/EVALUATION_REPORT.md)")
    parser.add_argument("--summary", action="store_true", help="Print summary to console")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    
    args = parser.parse_args()
    
    results = []
    script_dir = Path(__file__).parent.parent
    
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}")
            return 1
        result = evaluate_prompt(file_path)
        if result:
            results = [result]
    
    elif args.folder:
        folder_path = Path(args.folder)
        if not folder_path.exists():
            print(f"Error: Folder not found: {args.folder}")
            return 1
        files = find_prompt_files(folder_path)
        print(f"Found {len(files)} prompt files in {folder_path}")
        for f in files:
            result = evaluate_prompt(f)
            if result:
                results.append(result)
    
    elif args.all:
        prompts_path = script_dir / "prompts"
        if not prompts_path.exists():
            print(f"Error: prompts folder not found at {prompts_path}")
            return 1
        files = find_prompt_files(prompts_path)
        print(f"Found {len(files)} prompt files")
        for i, f in enumerate(files):
            result = evaluate_prompt(f)
            if result:
                results.append(result)
            if (i + 1) % 20 == 0:
                print(f"  Processed {i + 1}/{len(files)}...")
    
    else:
        parser.print_help()
        return 0
    
    if not results:
        print("No prompts found to evaluate.")
        return 1
    
    # Generate report
    output_path = Path(args.output)
    generate_report(results, output_path)
    
    # Print verbose output
    if args.verbose:
        print("\nDetailed Results:")
        for r in results:
            print(f"\n{r.file_path}")
            print(f"  Grade: {r.combined_grade}")
            print(f"  Quality: {r.quality_score.total:.0f}/100 ({r.quality_score.tier})")
            print(f"    - Completeness: {r.quality_score.completeness:.0f}")
            print(f"    - Example Quality: {r.quality_score.example_quality:.0f}")
            print(f"    - Specificity: {r.quality_score.specificity:.0f}")
            print(f"    - Format: {r.quality_score.format_adherence:.0f}")
            print(f"    - Enterprise: {r.quality_score.enterprise_quality:.0f}")
            print(f"  Effectiveness: {r.effectiveness_score.total:.1f}/5.0 ({r.effectiveness_score.rating})")
            print(f"    - Clarity: {r.effectiveness_score.clarity:.1f}")
            print(f"    - Effectiveness: {r.effectiveness_score.effectiveness:.1f}")
            print(f"    - Reusability: {r.effectiveness_score.reusability:.1f}")
            print(f"    - Simplicity: {r.effectiveness_score.simplicity:.1f}")
            print(f"    - Examples: {r.effectiveness_score.examples:.1f}")
            if r.quality_score.issues:
                print(f"  Issues: {'; '.join(r.quality_score.issues[:3])}")
    
    # Print summary
    if args.summary or args.all:
        print_summary(results)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
