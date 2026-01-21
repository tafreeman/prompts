#!/usr/bin/env python3
"""
Prompt Library Improvement Script
Uses evaluation rubrics and improvement prompts to systematically upgrade prompt quality.

This script:
1. Evaluates all prompts using both rubrics (Quality Standards + Effectiveness)
2. Identifies prompts needing improvement (Grade C/D/F or Quality <75)
3. Generates improvement recommendations using the prompt-quality-evaluator
4. Outputs actionable improvement tasks

Usage:
    python tools/improve_prompts.py --all
    python tools/improve_prompts.py --folder prompts/developers/
    python tools/improve_prompts.py --worst 10
    python tools/improve_prompts.py --generate-tasks
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
# FILE FILTERING
# =============================================================================

EXCLUDED_PATTERNS = [
    '*.agent.md', '*.instructions.md', 'index.md', 'README.md',
    '.github/**/*', 'docs/**/*', 'CONTRIBUTING.md', 'SECURITY.md',
    'LICENSE', 'agents/**/*', 'templates/**/*', '**/archive/**/*',
    'testing/**/*',
]

EXCLUDED_DIRS = {
    '.git', 'node_modules', '__pycache__', 'bin', 'obj',
    '.venv', 'venv', 'docs', 'agents', '.github', 'templates', 'archive', 'testing',
}


def should_exclude_file(file_path: Path, root_dir: Path) -> bool:
    """Determine if a file should be excluded from improvement."""
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
class IssueItem:
    """A specific issue found in a prompt."""
    priority: str  # P0, P1, P2, P3
    category: str
    description: str
    suggestion: str
    effort: str  # Low, Medium, High
    impact: int  # Expected score improvement


@dataclass
class PromptAssessment:
    """Complete assessment of a prompt with improvement recommendations."""
    file_path: str
    title: str
    category: str
    
    # Quality Standards Score (0-100)
    quality_total: float
    quality_tier: str
    completeness: float
    example_quality: float
    specificity: float
    format_adherence: float
    enterprise_quality: float
    
    # Effectiveness Score (1.0-5.0)
    effectiveness_total: float
    effectiveness_rating: str
    clarity: float
    effectiveness: float
    reusability: float
    simplicity: float
    examples: float
    
    # Combined
    combined_grade: str
    priority: int  # 1=critical, 2=high, 3=medium, 4=low
    
    # Issues and recommendations
    issues: List[IssueItem] = field(default_factory=list)
    
    # Content analysis
    word_count: int = 0
    has_frontmatter: bool = True
    has_description: bool = False
    has_prompt_section: bool = False
    has_variables: bool = False
    has_example: bool = False
    has_tips: bool = False
    line_count: int = 0


# Load registry.yaml for metadata
REGISTRY_PATH = Path('prompts/registry.yaml')
try:
    with REGISTRY_PATH.open('r', encoding='utf-8') as f:
        REGISTRY = yaml.safe_load(f)
except Exception:
    REGISTRY = None


def extract_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """Extract YAML frontmatter from markdown content (minimal: name, description)."""
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
    if score >= 4.5: return "⭐⭐⭐⭐⭐ Excellent"
    elif score >= 4.0: return "⭐⭐⭐⭐ Good"
    elif score >= 3.0: return "⭐⭐⭐ Acceptable"
    elif score >= 2.0: return "⭐⭐ Below Average"
    else: return "⭐ Poor"


def get_quality_tier(score: float) -> str:
    if score >= 90: return "Tier 1 (Excellent)"
    elif score >= 75: return "Tier 2 (Good)"
    elif score >= 60: return "Tier 3 (Acceptable)"
    else: return "Tier 4 (Poor)"


# =============================================================================
# ASSESSMENT ENGINE
# =============================================================================

def assess_prompt(file_path: Path) -> Optional[PromptAssessment]:
    """Assess a single prompt and identify improvement opportunities."""
    if file_path.suffix != '.md':
        return None
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return None
    
    frontmatter = extract_frontmatter(content) or {}
    body = extract_body(content)

    # Use registry.yaml for all metadata except minimal frontmatter
    rel_path = str(file_path).replace('\\', '/').split('prompts/', 1)[-1]
    registry_entry = None
    if REGISTRY:
        for entry in REGISTRY:
            if entry.get('path', '').replace('\\', '/') == rel_path:
                registry_entry = entry
                break

    # Use registry metadata if available
    title = registry_entry.get('title', file_path.stem.replace('-', ' ').title()) if registry_entry else frontmatter.get('name', file_path.stem.replace('-', ' ').title())
    category = registry_entry.get('categories', [file_path.parent.name])[0] if registry_entry and 'categories' in registry_entry else file_path.parent.name
    
    # Content analysis
    line_count = len([l for l in content.split('\n') if l.strip()])
    word_count = len(body.split())

    # Check for key sections
    body_lower = body.lower()
    has_description = '## description' in body_lower or '## purpose' in body_lower
    has_prompt_section = '## prompt' in body_lower
    has_variables = '## variable' in body_lower
    has_example = '## example' in body_lower
    has_tips = '## tips' in body_lower
    
    # Initialize assessment
    assessment = PromptAssessment(
        file_path=str(file_path),
        title=title,
        category=category,
        quality_total=0,
        quality_tier="",
        completeness=0,
        example_quality=0,
        specificity=0,
        format_adherence=0,
        enterprise_quality=0,
        effectiveness_total=0,
        effectiveness_rating="",
        clarity=3.0,
        effectiveness=3.0,
        reusability=3.0,
        simplicity=3.0,
        examples=2.5,
        combined_grade="",
        priority=3,
        word_count=word_count,
        has_frontmatter=bool(frontmatter),
        has_description=has_description,
        has_prompt_section=has_prompt_section,
        has_variables=has_variables,
        has_example=has_example,
        has_tips=has_tips,
        line_count=line_count,
    )
    
    # === QUALITY STANDARDS SCORING (0-100) ===

    # Completeness (25 points)
    completeness = 0
    # Only require minimal frontmatter (name, description)
    minimal_fm = ['name', 'description']
    fm_present = sum(1 for f in minimal_fm if f in frontmatter)
    completeness += (fm_present / len(minimal_fm)) * 8

    if has_description: completeness += 3
    else: assessment.issues.append(IssueItem("P1", "structure", "Missing Description section", "Add ## Description with 2-3 sentences explaining the prompt", "Low", 3))

    if has_prompt_section: completeness += 5
    else: assessment.issues.append(IssueItem("P0", "structure", "Missing Prompt section", "Add ## Prompt with the actual prompt template", "Low", 5))

    if has_variables: completeness += 3
    else: assessment.issues.append(IssueItem("P1", "structure", "Missing Variables section", "Add ## Variables documenting all placeholders", "Low", 3))

    if has_example: completeness += 4
    else: assessment.issues.append(IssueItem("P1", "structure", "Missing Example section", "Add ## Example Usage with realistic input/output", "Medium", 4))

    if has_tips: completeness += 2
    else: assessment.issues.append(IssueItem("P2", "structure", "Missing Tips section", "Add ## Tips with 3-5 actionable recommendations", "Low", 2))

    assessment.completeness = min(25, completeness)
    
    # Example Quality (30 points)
    example_quality = 0
    if has_example:
        example_match = re.search(r'## Example(?:\s+Usage)?\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
        if example_match:
            example_content = example_match.group(1)
            example_lines = len([l for l in example_content.split('\n') if l.strip()])
            
            if example_lines >= 100: example_quality += 10
            elif example_lines >= 50: example_quality += 7
            elif example_lines >= 20: example_quality += 4
            else:
                example_quality += 2
                assessment.issues.append(IssueItem("P1", "example", f"Example too short ({example_lines} lines)", "Expand example with detailed realistic scenario (aim for 50+ lines)", "Medium", 5))
            
            if '**Input**' in example_content or 'Input:' in example_content:
                example_quality += 5
            else:
                assessment.issues.append(IssueItem("P1", "example", "Example missing Input section", "Add **Input:** showing filled-in variables", "Low", 3))
            
            if '**Output**' in example_content or 'Output:' in example_content:
                example_quality += 5
            else:
                assessment.issues.append(IssueItem("P1", "example", "Example missing Output section", "Add **Output:** showing expected AI response", "Low", 3))
            
            if re.search(r'\$[\d,]+|\d+%|\d+\s*(hours?|days?|minutes?)', example_content):
                example_quality += 5
            
            if 'placeholder' in example_content.lower() or '[replace' in example_content.lower():
                example_quality -= 5
                assessment.issues.append(IssueItem("P0", "example", "Example contains placeholder text", "Replace all placeholders with realistic values", "Low", 5))
            else:
                example_quality += 5
    else:
        assessment.issues.append(IssueItem("P0", "example", "No example section", "Add complete example with realistic Input and Output", "Medium", 10))
    
    assessment.example_quality = max(0, min(30, example_quality))
    
    # Specificity (20 points)
    specificity = 0
    
    if has_tips:
        tips_match = re.search(r'## Tips\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
        if tips_match:
            tips_content = tips_match.group(1)
            tips_count = len(re.findall(r'^[-*]\s+', tips_content, re.MULTILINE))
            if tips_count >= 5: specificity += 6
            elif tips_count >= 3: specificity += 4
            elif tips_count >= 1: specificity += 2
            else:
                assessment.issues.append(IssueItem("P2", "tips", f"Only {tips_count} tips provided", "Add 3-5 actionable, specific tips", "Low", 2))
            
            generic_phrases = ['check your work', 'be careful', 'make sure', 'double check']
            if not any(p in tips_content.lower() for p in generic_phrases):
                specificity += 4
            else:
                assessment.issues.append(IssueItem("P2", "tips", "Tips contain generic phrases", "Replace generic tips with specific, actionable recommendations", "Low", 2))
    
    if has_variables:
        vars_match = re.search(r'## Variables?\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
        if vars_match:
            vars_content = vars_match.group(1)
            if 'example' in vars_content.lower() or 'e.g.' in vars_content.lower():
                specificity += 5
            else:
                assessment.issues.append(IssueItem("P1", "variables", "Variables lack example values", "Add realistic example values for each variable", "Low", 3))
    
    use_cases_match = re.search(r'## Use Cases?\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
    if use_cases_match:
        use_cases_content = use_cases_match.group(1)
        use_case_count = len(re.findall(r'^[-*\d.]\s+', use_cases_content, re.MULTILINE))
        if use_case_count >= 5: specificity += 5
        elif use_case_count >= 3: specificity += 3
        else:
            assessment.issues.append(IssueItem("P2", "use_cases", f"Only {use_case_count} use cases", "Add at least 5 specific use cases", "Low", 2))
    
    assessment.specificity = min(20, specificity)
    
    # Format Adherence (15 points)
    format_score = 0
    
    if frontmatter:
        format_score += 5
    else:
        assessment.issues.append(IssueItem("P0", "format", "Missing YAML frontmatter", "Add complete frontmatter with all required fields", "Low", 5))
    
    if re.search(r'^# ', body, re.MULTILINE):
        format_score += 3
    
    h2_count = len(re.findall(r'^## ', body, re.MULTILINE))
    if h2_count >= 4: format_score += 4
    elif h2_count >= 2: format_score += 2
    
    if re.search(r'\[[\w_-]+\]', body):
        format_score += 3
    
    assessment.format_adherence = min(15, format_score)
    
    # Enterprise Quality (10 points)
    enterprise = 0
    
    frameworks = ['iso', 'pmi', 'nist', 'owasp', 'itil', 'cobit', 'togaf', 'safe', 'agile']
    framework_count = sum(1 for f in frameworks if f in body.lower())
    if framework_count >= 2: enterprise += 4
    elif framework_count >= 1: enterprise += 2
    
    casual_phrases = ["let's", "gonna", "wanna", "kinda", "btw", "fyi"]
    if not any(p in body.lower() for p in casual_phrases):
        enterprise += 3
    
    if frontmatter.get('governance_tags'):
        enterprise += 3
    else:
        assessment.issues.append(IssueItem("P2", "governance", "Missing governance_tags", "Add governance_tags (e.g., PII-safe, requires-human-review)", "Low", 2))
    
    assessment.enterprise_quality = min(10, enterprise)
    
    # Calculate Quality Total
    assessment.quality_total = round(
        assessment.completeness + assessment.example_quality + assessment.specificity +
        assessment.format_adherence + assessment.enterprise_quality, 1
    )
    assessment.quality_tier = get_quality_tier(assessment.quality_total)
    
    # === EFFECTIVENESS SCORING (1.0-5.0) ===
    
    # Clarity
    clarity = 3.0
    if frontmatter.get('title') and len(str(frontmatter['title'])) > 5: clarity += 0.3
    if frontmatter.get('intro') and len(str(frontmatter['intro'])) > 20: clarity += 0.4
    if has_description: clarity += 0.3
    if has_prompt_section:
        if '```' in body: clarity += 0.4
        else: clarity += 0.2
    else:
        clarity -= 0.5
    if has_variables: clarity += 0.3
    assessment.clarity = round(max(1.0, min(5.0, clarity)), 1)
    
    # Effectiveness
    effectiveness = 3.0
    platforms = frontmatter.get('platforms', [])
    if isinstance(platforms, list):
        if len(platforms) >= 3: effectiveness += 0.5
        elif len(platforms) >= 2: effectiveness += 0.3
    
    prompt_match = re.search(r'## Prompt\s*\n+```[\w]*\s*(.*?)```', body, re.DOTALL | re.IGNORECASE)
    if prompt_match:
        prompt_text = prompt_match.group(1).lower()
        if any(f in prompt_text for f in ['format', 'structure', 'output as', 'respond with']):
            effectiveness += 0.4
        if any(r in prompt_text for r in ['you are', 'act as', 'role:']):
            effectiveness += 0.3
        if any(c in prompt_text for c in ['must', 'should', 'require', 'ensure', 'avoid']):
            effectiveness += 0.3
    
    if frontmatter.get('governance_tags'): effectiveness += 0.2
    assessment.effectiveness = round(max(1.0, min(5.0, effectiveness)), 1)
    
    # Reusability
    reusability = 3.0
    unique_vars = set(re.findall(r'\[[\w_-]+\]', body))
    if len(unique_vars) >= 5: reusability += 0.5
    elif len(unique_vars) >= 3: reusability += 0.3
    elif len(unique_vars) >= 1: reusability += 0.1
    else: reusability -= 0.3
    
    audience = frontmatter.get('audience', [])
    if isinstance(audience, list) and len(audience) >= 3: reusability += 0.3
    elif isinstance(audience, list) and len(audience) >= 2: reusability += 0.2
    
    if '## use case' in body_lower: reusability += 0.3
    if '## variation' in body_lower: reusability += 0.2
    assessment.reusability = round(max(1.0, min(5.0, reusability)), 1)
    
    # Simplicity
    simplicity = 3.0
    if line_count <= 80: simplicity += 0.6
    elif line_count <= 120: simplicity += 0.3
    elif line_count > 300: simplicity -= 0.6
    elif line_count > 200: simplicity -= 0.3
    
    if '## changelog' in body_lower:
        simplicity -= 0.5
        assessment.issues.append(IssueItem("P2", "simplicity", "Has Changelog section", "Remove Changelog (use git history instead)", "Low", 2))
    
    section_count = len(re.findall(r'^## ', body, re.MULTILINE))
    if section_count <= 6: simplicity += 0.3
    elif section_count > 10: simplicity -= 0.2
    assessment.simplicity = round(max(1.0, min(5.0, simplicity)), 1)
    
    # Examples
    examples_score = 2.5
    if has_example:
        examples_score += 0.5
        example_match = re.search(r'## Example(?:\s+Usage)?\s*\n+(.*?)(?=\n##|\Z)', body, re.DOTALL | re.IGNORECASE)
        if example_match:
            example_content = example_match.group(1)
            if '**Input**' in example_content or 'Input:' in example_content: examples_score += 0.4
            if '**Output**' in example_content or 'Output:' in example_content: examples_score += 0.4
            if '```' in example_content: examples_score += 0.3
            example_lines = len([l for l in example_content.split('\n') if l.strip()])
            if example_lines >= 15: examples_score += 0.3
    assessment.examples = round(max(1.0, min(5.0, examples_score)), 1)
    
    # Calculate Effectiveness Total
    assessment.effectiveness_total = round(
        assessment.clarity * 0.25 +
        assessment.effectiveness * 0.30 +
        assessment.reusability * 0.20 +
        assessment.simplicity * 0.15 +
        assessment.examples * 0.10,
        1
    )
    assessment.effectiveness_rating = get_effectiveness_rating(assessment.effectiveness_total)
    
    # === COMBINED GRADE ===
    if assessment.quality_total >= 90 and assessment.effectiveness_total >= 4.5:
        assessment.combined_grade = "A (Excellent)"
        assessment.priority = 4
    elif assessment.quality_total >= 75 and assessment.effectiveness_total >= 4.0:
        assessment.combined_grade = "B (Good)"
        assessment.priority = 4
    elif assessment.quality_total >= 60 and assessment.effectiveness_total >= 3.0:
        assessment.combined_grade = "C (Acceptable)"
        assessment.priority = 3
    elif assessment.quality_total >= 45 or assessment.effectiveness_total >= 2.5:
        assessment.combined_grade = "D (Below Average)"
        assessment.priority = 2
    else:
        assessment.combined_grade = "F (Poor)"
        assessment.priority = 1
    
    # Sort issues by priority
    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    assessment.issues.sort(key=lambda x: priority_order.get(x.priority, 99))
    
    return assessment


# =============================================================================
# IMPROVEMENT PROMPT GENERATOR
# =============================================================================

def generate_improvement_prompt(assessment: PromptAssessment) -> str:
    """Generate a prompt that can be used to improve this prompt."""
    
    issues_text = "\n".join([
        f"- [{i.priority}] {i.category}: {i.description}\n  Suggestion: {i.suggestion}\n  Effort: {i.effort}, Impact: +{i.impact} points"
        for i in assessment.issues[:7]
    ])
    
    prompt = f'''You are improving a prompt from the prompt library.

**File**: {assessment.file_path}
**Title**: {assessment.title}
**Current Quality Score**: {assessment.quality_total}/100 ({assessment.quality_tier})
**Current Effectiveness**: {assessment.effectiveness_total}/5.0 ({assessment.effectiveness_rating})
**Combined Grade**: {assessment.combined_grade}

## Current Issues (Priority Order)

{issues_text}

## Current Structure Analysis

- Has Description: {"✓" if assessment.has_description else "✗"}
- Has Prompt Section: {"✓" if assessment.has_prompt_section else "✗"}
- Has Variables: {"✓" if assessment.has_variables else "✗"}
- Has Example: {"✓" if assessment.has_example else "✗"}
- Has Tips: {"✓" if assessment.has_tips else "✗"}
- Word Count: {assessment.word_count}
- Line Count: {assessment.line_count}

## Your Task

1. Read the current prompt file
2. Fix all P0 (Critical) and P1 (High Priority) issues
3. Improve the prompt to achieve at least:
   - Quality Score: 75+ (Tier 2)
   - Effectiveness: 4.0+ (Good)
   - Combined Grade: B

## Improvement Template

Use this structure when improving:

```markdown
---
title: "[Clear, descriptive title ≤60 chars]"
shortTitle: "[Short version ≤27 chars]"
intro: "[2-3 sentence description of what this prompt does]"
type: "how_to"
difficulty: "[beginner|intermediate|advanced]"
audience:
  - "[primary-audience]"
  - "[secondary-audience]"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
topics:
  - "[topic1]"
  - "[topic2]"
author: "Prompts Library Team"
version: "[X.Y]"
date: "[YYYY-MM-DD]"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# [Title]

## Description

[2-3 sentences explaining the purpose and value of this prompt]

## Use Cases

- [Specific use case 1 with context]
- [Specific use case 2 with context]
- [Specific use case 3 with context]
- [Specific use case 4 with context]
- [Specific use case 5 with context]

## Prompt

```text
[The actual prompt template with [VARIABLE] placeholders]
```

## Variables

- `[VARIABLE1]`: Description and example value (e.g., "project name like 'Customer Portal Redesign'")
- `[VARIABLE2]`: Description and example value
- [Continue for all variables]

## Example Usage

**Input:**

```text
[Show the prompt with all variables filled in with realistic values]
```

**Output:**

```text
[Show the expected AI response - detailed and realistic, 30+ lines]
```

## Tips

- **Tip 1**: [Specific, actionable recommendation]
- **Tip 2**: [Specific, actionable recommendation]
- **Tip 3**: [Specific, actionable recommendation]
- **Tip 4**: [Specific, actionable recommendation]
- **Tip 5**: [Specific, actionable recommendation]

## Related Prompts

- [Related Prompt 1](path/to/prompt.md) - Brief description
- [Related Prompt 2](path/to/prompt.md) - Brief description
```

Now read the prompt file and generate the improved version.
'''
    return prompt


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_improvement_report(assessments: List[PromptAssessment], output_path: Optional[Path] = None) -> str:
    """Generate improvement report with prioritized tasks."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Filter to prompts needing improvement
    needs_improvement = [a for a in assessments if a.priority <= 3]  # C, D, F grades
    critical = [a for a in assessments if a.priority == 1]
    high = [a for a in assessments if a.priority == 2]
    medium = [a for a in assessments if a.priority == 3]
    
    # Sort by quality score (worst first)
    needs_improvement.sort(key=lambda x: x.quality_total)
    
    lines = [
        "# Prompt Improvement Plan",
        "",
        f"**Generated**: {now}",
        f"**Total Prompts Analyzed**: {len(assessments)}",
        f"**Prompts Needing Improvement**: {len(needs_improvement)}",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"| Priority | Count | Description |",
        f"|----------|-------|-------------|",
        f"| 🔴 Critical (F) | {len(critical)} | Major rewrite required |",
        f"| 🟠 High (D) | {len(high)} | Significant improvements needed |",
        f"| 🟡 Medium (C) | {len(medium)} | Minor improvements recommended |",
        f"| 🟢 Good (B/A) | {len(assessments) - len(needs_improvement)} | No action required |",
        "",
        "---",
        "",
    ]
    
    # Critical Issues
    if critical:
        lines.extend([
            "## 🔴 Critical Priority (Grade F)",
            "",
            "These prompts require major rewrites:",
            "",
        ])
        for a in critical:
            p0_issues = [i for i in a.issues if i.priority == "P0"]
            lines.append(f"### {a.title}")
            lines.append(f"**File**: `{a.file_path}`")
            lines.append(f"**Scores**: Quality {a.quality_total}/100, Effectiveness {a.effectiveness_total}/5.0")
            lines.append("")
            lines.append("**Critical Issues:**")
            for issue in p0_issues[:3]:
                lines.append(f"- {issue.description}")
                lines.append(f"  - Fix: {issue.suggestion}")
            lines.append("")
        lines.append("---")
        lines.append("")
    
    # High Priority
    if high:
        lines.extend([
            "## 🟠 High Priority (Grade D)",
            "",
            "| File | Quality | Effectiveness | Top Issue |",
            "|------|---------|---------------|-----------|",
        ])
        for a in high:
            top_issue = a.issues[0].description if a.issues else "General improvement"
            lines.append(f"| `{Path(a.file_path).name}` | {a.quality_total:.0f} | {a.effectiveness_total:.1f} | {top_issue[:40]}... |")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Medium Priority
    if medium:
        lines.extend([
            "## 🟡 Medium Priority (Grade C)",
            "",
            "| File | Quality | Effectiveness | Issues |",
            "|------|---------|---------------|--------|",
        ])
        for a in medium[:20]:  # Top 20
            issue_count = len(a.issues)
            lines.append(f"| `{Path(a.file_path).name}` | {a.quality_total:.0f} | {a.effectiveness_total:.1f} | {issue_count} issues |")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Common Issues Summary
    lines.extend([
        "## Common Issues Across Library",
        "",
    ])
    
    issue_counts = {}
    for a in needs_improvement:
        for issue in a.issues:
            key = f"{issue.priority}: {issue.description}"
            issue_counts[key] = issue_counts.get(key, 0) + 1
    
    sorted_issues = sorted(issue_counts.items(), key=lambda x: -x[1])[:10]
    
    lines.append("| Issue | Count | Priority |")
    lines.append("|-------|-------|----------|")
    for issue, count in sorted_issues:
        priority = issue.split(":")[0]
        desc = issue.split(": ", 1)[1] if ": " in issue else issue
        lines.append(f"| {desc[:50]}... | {count} | {priority} |")
    
    lines.extend([
        "",
        "---",
        "",
        "## Recommended Action Plan",
        "",
        "### Week 1: Critical Fixes",
        "",
    ])
    
    for a in critical[:5]:
        lines.append(f"- [ ] Fix `{Path(a.file_path).name}` (Quality: {a.quality_total:.0f})")
    
    lines.extend([
        "",
        "### Week 2: High Priority",
        "",
    ])
    
    for a in high[:10]:
        lines.append(f"- [ ] Improve `{Path(a.file_path).name}` (Quality: {a.quality_total:.0f})")
    
    lines.extend([
        "",
        "### Week 3-4: Medium Priority",
        "",
    ])
    
    for a in medium[:15]:
        lines.append(f"- [ ] Polish `{Path(a.file_path).name}` (Quality: {a.quality_total:.0f})")
    
    lines.extend([
        "",
        "---",
        "",
        f"*Generated: {now}*",
    ])
    
    content = "\n".join(lines)
    
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')
        print(f"✅ Improvement plan saved to {output_path}")
    
    return content


def print_worst_prompts(assessments: List[PromptAssessment], count: int = 10):
    """Print the worst prompts needing improvement."""
    sorted_assessments = sorted(assessments, key=lambda x: x.quality_total)
    
    print(f"\n{'='*80}")
    print(f"TOP {count} PROMPTS NEEDING IMPROVEMENT")
    print(f"{'='*80}\n")
    
    for i, a in enumerate(sorted_assessments[:count], 1):
        print(f"{i}. {a.title}")
        print(f"   File: {a.file_path}")
        print(f"   Grade: {a.combined_grade}")
        print(f"   Quality: {a.quality_total}/100 ({a.quality_tier})")
        print(f"   Effectiveness: {a.effectiveness_total}/5.0")
        print(f"   Issues: {len(a.issues)}")
        if a.issues:
            print(f"   Top Issue: [{a.issues[0].priority}] {a.issues[0].description}")
        print()


def generate_improvement_prompts_file(assessments: List[PromptAssessment], output_path: Path, count: int = 10):
    """Generate a file with improvement prompts for the worst prompts."""
    sorted_assessments = sorted(assessments, key=lambda x: x.quality_total)
    
    lines = [
        "# Improvement Prompts",
        "",
        "Copy these prompts to an AI assistant to improve each prompt.",
        "",
        "---",
        "",
    ]
    
    for i, a in enumerate(sorted_assessments[:count], 1):
        lines.append(f"## {i}. {a.title}")
        lines.append("")
        lines.append(f"**File**: `{a.file_path}`")
        lines.append(f"**Current Grade**: {a.combined_grade}")
        lines.append("")
        lines.append("### Improvement Prompt")
        lines.append("")
        lines.append("```text")
        lines.append(generate_improvement_prompt(a))
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")
    
    content = "\n".join(lines)
    output_path.write_text(content, encoding='utf-8')
    print(f"✅ Improvement prompts saved to {output_path}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Assess prompts and generate improvement recommendations",
        epilog="""
Examples:
  python tools/improve_prompts.py --all
  python tools/improve_prompts.py --folder prompts/governance/
  python tools/improve_prompts.py --worst 10
  python tools/improve_prompts.py --all --generate-tasks
        """
    )
    parser.add_argument("file", nargs="?", help="Single prompt file to assess")
    parser.add_argument("--all", action="store_true", help="Assess all prompts")
    parser.add_argument("--folder", type=str, help="Assess prompts in a specific folder")
    parser.add_argument("--worst", type=int, default=0, help="Show N worst prompts")
    parser.add_argument("--generate-tasks", action="store_true", help="Generate improvement task file")
    parser.add_argument("--generate-prompts", action="store_true", help="Generate improvement prompts file")
    parser.add_argument("--output", "-o", type=str, default="docs/IMPROVEMENT_PLAN.md",
                        help="Output path for improvement plan")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    
    args = parser.parse_args()
    
    assessments = []
    script_dir = Path(__file__).parent.parent
    
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}")
            return 1
        result = assess_prompt(file_path)
        if result:
            assessments = [result]
    
    elif args.folder:
        folder_path = Path(args.folder)
        if not folder_path.exists():
            print(f"Error: Folder not found: {args.folder}")
            return 1
        files = find_prompt_files(folder_path)
        print(f"Found {len(files)} prompt files in {folder_path}")
        for f in files:
            result = assess_prompt(f)
            if result:
                assessments.append(result)
    
    elif args.all:
        prompts_path = script_dir / "prompts"
        if not prompts_path.exists():
            print(f"Error: prompts folder not found at {prompts_path}")
            return 1
        files = find_prompt_files(prompts_path)
        print(f"Found {len(files)} prompt files")
        for i, f in enumerate(files):
            result = assess_prompt(f)
            if result:
                assessments.append(result)
            if (i + 1) % 20 == 0:
                print(f"  Assessed {i + 1}/{len(files)}...")
    
    else:
        parser.print_help()
        return 0
    
    if not assessments:
        print("No prompts found to assess.")
        return 1
    
    # Show worst prompts
    if args.worst > 0:
        print_worst_prompts(assessments, args.worst)
    
    # Generate improvement plan
    if args.all or args.generate_tasks:
        output_path = Path(args.output)
        generate_improvement_report(assessments, output_path)
    
    # Generate improvement prompts
    if args.generate_prompts:
        prompts_path = Path("docs/IMPROVEMENT_PROMPTS.md")
        generate_improvement_prompts_file(assessments, prompts_path, count=20)
    
    # Print summary
    needs_improvement = len([a for a in assessments if a.priority <= 3])
    print(f"\n{'='*60}")
    print(f"ASSESSMENT COMPLETE")
    print(f"{'='*60}")
    print(f"Total prompts:          {len(assessments)}")
    print(f"Needing improvement:    {needs_improvement}")
    print(f"Good (B or better):     {len(assessments) - needs_improvement}")
    print(f"{'='*60}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
