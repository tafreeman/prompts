---
title: "Visual and Formatting Audit Report"
shortTitle: "Formatting Audit"
intro: "Comprehensive audit of visual formatting, markdown structure, and readability across the prompt library."
type: reference
difficulty: intermediate
audience:
  - senior-engineer
  - solution-architect
platforms:
  - github-copilot
topics:
  - documentation
  - quality
author: Prompt Library Team
version: "1.0"
date: "2025-12-03"
governance_tags:
  - PII-safe
dataClassification: internal
reviewStatus: draft
---

# 📊 Visual and Formatting Audit Report

<div align="center">

![Version](https://img.shields.io/badge/Version-1.0-blue)
![Files Audited](https://img.shields.io/badge/Files%20Audited-305-green)
![Health Score](https://img.shields.io/badge/Health%20Score-72%2F100-yellow)
![Status](https://img.shields.io/badge/Status-Needs%20Improvement-orange)

**Prompt Library Formatting & Readability Assessment**

*Generated: December 3, 2025*

</div>

---

## 📈 Executive Summary

| Metric | Value | Assessment |
|:-------|------:|:----------:|
| **Total Markdown Files** | 305 | — |
| **Prompt Files Analyzed** | 148 | — |
| **Overall Health Score** | 72/100 | 🟡 Fair |
| **Critical Issues** | 8 | 🔴 |
| **High Priority Issues** | 50 | 🟠 |
| **Medium Priority Issues** | 103 | 🟡 |
| **Low Priority Polish Items** | 65+ | 🟢 |

### 🎯 Top 3 Issues

| Rank | Issue | Impact | Files Affected |
|:----:| :--- |:------:|---------------:|
| 🥇 | **Broken internal links** | Navigation fails, poor UX | 50 links |
| 🥈 | **Missing standard sections** | Inconsistent structure | 19 files |
| 🥉 | **Code blocks without language specifiers** | Poor syntax highlighting | 40+ blocks |

---

## 🔴 Critical Issues (Must Fix)

### Issue 1: Broken Internal Links

**Impact**: Users clicking "Related Prompts" links get 404 errors. Breaks navigation and trust.

| Source File | Broken Link | Status |
|:------------|:------------|:------:|
| `chain-of-thought-debugging.md` | `../developers/reflection-code-review-self-check.md` | ❌ |
| `chain-of-thought-debugging.md` | `react-codebase-navigator.md` | ❌ |
| `chain-of-thought-detailed.md` | `reflection-evaluator.md` | ❌ |
| `chain-of-thought-guide.md` | `tree-of-thoughts-decision-guide.md` | ❌ |
| `chain-of-thought-performance-analysis.md` | `../developers/sql-query-optimizer-advanced.md` | ❌ |
| `rag-document-retrieval.md` | `rag-code-ingestion.md` | ❌ |
| `rag-document-retrieval.md` | `rag-citation-framework.md` | ❌ |
| `react-tool-augmented.md` | `react-api-integration.md` | ❌ |
| `react-tool-augmented.md` | `rag-citation-framework.md` | ❌ |
| `reflection-self-critique.md` | `reflection-iterative-improvement.md` | ❌ |
| `tree-of-thoughts-architecture-evaluator.md` | `tree-of-thoughts-database-migration.md` | ❌ |
| `tree-of-thoughts-template.md` | `tree-of-thoughts-decision-guide.md` | ❌ |
| `competitive-intelligence-researcher.md` | `../business/swot-analysis.md` | ❌ |
| `data-quality-assessment.md` | `experiment-design-analyst.md` | ❌ |
| `agile-sprint-planner.md` | `./project-charter-creator.md` | ❌ |
| `budget-and-cost-controller.md` | `./project-charter-creator.md` | ❌ |
| `business-strategy-analysis.md` | `market-research-analysis.md` | ❌ |

**Total**: 50 broken links across the library

**Fix Options**:
1. Create the missing referenced files
2. Update links to existing equivalent files
3. Remove links to non-existent files

---

### Issue 2: Missing Standard Sections

Files missing required prompt template sections (Description, Prompt, Variables, Example, Tips):

| File | Missing Sections | Quality Score |
|:-----|:-----------------|:-------------:|
| `prompts/advanced/library.md` | Description, Variables, Example, Tips | 21/100 🔴 |
| `prompts/advanced/prompt-library-refactor-react.md` | Variables, Example | 33/100 🔴 |
| `prompts/advanced/chain-of-thought-guide.md` | Variables, Tips | 40/100 🔴 |
| `prompts/analysis/library-capability-radar.md` | Variables, Tips | 39/100 🔴 |
| `prompts/analysis/library-network-graph.md` | Variables, Tips | 44/100 🔴 |
| `prompts/analysis/library-structure-treemap.md` | Variables, Tips | 41/100 🔴 |
| `prompts/system/example-research-output.md` | Description, Prompt, Variables, Tips | 22/100 🔴 |
| `prompts/system/frontier-agent-deep-research.md` | Tips | — |
| `prompts/system/m365-copilot-research-agent.md` | Tips | — |
| `prompts/system/office-agent-technical-specs.md` | Tips | — |

**Fix**: Add missing sections following `templates/prompt-template.md`

---

### Issue 3: Files with Non-Standard H1→H2 Structure

These files don't follow the H1 → blank line → ## Description pattern:

| File | Issue |
|:-----|:------|
| `m365-excel-formula-expert.md` | H1 followed directly by ## Description (missing Description header) |
| `m365-customer-feedback-analyzer.md` | Non-standard section order |
| `m365-designer-*.md` (6 files) | Inconsistent structure |
| `m365-handover-document-creator.md` | Non-standard structure |
| `m365-manager-sync-planner.md` | Non-standard structure |
| `m365-slide-content-refiner.md` | Non-standard structure |
| `m365-sway-*.md` (2 files) | Non-standard structure |
| `api-design-consultant.md` | Uses "Purpose" instead of "Description" |
| `code-review-expert.md` | Uses "Purpose" instead of "Description" |
| `code-review-expert-structured.md` | Uses "Purpose" instead of "Description" |
| `security-code-auditor.md` | Non-standard structure |
| `sql-security-standards-enforcer.md` | Non-standard structure |

**Fix**: Standardize to use `## Description` as the first section after H1

---

## 🟠 High Priority Issues

### Category 1: Code Blocks Missing Language Specifiers

**Impact**: No syntax highlighting in GitHub, VS Code, or documentation viewers

<details>
<summary><b>Files with unlabeled code blocks (40+ instances)</b></summary>

| File | Approximate Count |
|:-----|------------------:|
| `docs/COMPREHENSIVE_PROMPT_DEVELOPMENT_GUIDE.md` | 20+ blocks |
| `prompts/system/tree-of-thoughts-repository-evaluator.md` | 4 blocks |
| `prompts/system/solution-architecture-designer.md` | 3 blocks |
| `prompts/system/security-architecture-specialist.md` | 3 blocks |
| `prompts/system/prompt-quality-evaluator.md` | 8 blocks |
| `prompts/system/performance-architecture-optimizer.md` | 2 blocks |
| Multiple other system prompts | Various |

</details>

**Fix Pattern**:
```diff
- ```
+ ```text
[content]
- ```
+ ```
```

Common language specifiers to use:
- `text` - Plain text prompts
- `python` - Python code
- `json` - JSON structures
- `markdown` - Markdown examples
- `bash` / `powershell` - Shell commands

---

### Category 2: Tables Without Alignment Specifiers

**Impact**: Inconsistent column alignment across different Markdown viewers

**Current Pattern** (many files):
```markdown
| Column1 | Column2 |
| :--- |---------|
```

**Recommended Pattern**:
```markdown
| Column1 | Column2 | Column3 |
|:--------|:-------:|--------:|  <!-- left, center, right -->
```

**Files needing table alignment updates**: ~80% of prompt files

---

### Category 3: Long Tables Needing Collapsible Sections

These files have large tables (10+ rows) that should use `<details>` tags:

| File | Table Size | Recommendation |
|:-----|:----------:|:---------------|
| `docs/EVALUATION_REPORT.md` | ✅ Already uses `<details>` | Good example |
| `prompts/system/ai-assistant-system-prompt.md` | 15+ rows | Add collapsible |
| `prompts/developers/code-review-expert.md` | 10+ rows | Add collapsible |
| Various analysis prompts | 10+ rows | Add collapsible |

**Pattern**:
```html
<details>
<summary><b>View full table (N items)</b></summary>

| Column | Data |
|:-------|:-----|
| ... | ... |

</details>
```

---

### Category 4: Missing "Related Prompts" Sections

**Impact**: Poor discoverability, users don't find related content

Files **WITH** Related Prompts: 140 files ✅
Files **WITHOUT** Related Prompts: ~8 prompt files

| File Missing Related Prompts |
|:-----------------------------|
| `prompts/advanced/library.md` |
| `prompts/advanced/prompt-library-refactor-react.md` |
| `prompts/system/example-research-output.md` |
| Various index.md files (expected) |

---

## 🟡 Medium Priority Issues

### Category 1: Inconsistent Section Ordering

**Standard order per template**:
1. Description
2. Use Cases (optional)
3. Prompt
4. Variables
5. Example Usage
6. Tips
7. Related Prompts

**Files with non-standard order**:

| File | Current Order Issue |
|:-----|:--------------------|
| `m365-excel-formula-expert.md` | Goal/Inputs before Description |
| `library-capability-radar.md` | Uses Goal/Context/Inputs/Assumptions/Constraints instead |
| Multiple m365 files | Inconsistent section names |

---

### Category 2: Missing Horizontal Rules Between Major Sections

**Impact**: Sections blend together, harder to scan

**Files needing `---` separators**:
- Most prompt files (add between major sections for long documents)
- `docs/IMPROVEMENT_PLAN.md` - Sections run together
- `docs/TOT_EVALUATION_REPORT.md` - Could use more visual breaks

**Good Example**: `docs/EVALUATION_REPORT.md` - Excellent use of `---` separators

---

### Category 3: Examples Without Clear Input/Output Separation

**Impact**: Users can't easily distinguish what to provide vs. what to expect

**Current (some files)**:
```markdown
## Example

Here's how to use this prompt...
[mixed content]
```

**Recommended**:
```markdown
## Example Usage

**Input:**

```text
[User provides this]
```

**Output:**

```text
[AI generates this]
```
```

**Files needing Input/Output separation**: ~30 prompts

---

### Category 4: Very Long Code Blocks Needing Collapse

Files with code blocks > 50 lines that should be collapsible:

| File | Block Type | Lines |
|:-----|:-----------|------:|
| `react-tool-augmented.md` | Example output | 150+ |
| `data-analysis-insights.md` | Example output | 200+ |
| `agile-sprint-planner.md` | Example output | 180+ |
| `governance/security-incident-response.md` | Multiple examples | 300+ total |
| `governance/legal-contract-review.md` | Multiple examples | 200+ total |

---

## 🟢 Low Priority (Polish Items)

### Visual Enhancements

#### 1. Files That Could Benefit from Shields.io Badges

Currently only 2 files use badges: `EVALUATION_REPORT.md`, `library-visual-audit.md`

**Recommendation**: Add badges to key entry points:
- `README.md` (root) - Already has some
- `prompts/index.md` - Add prompt count, categories
- `docs/README.md` - Add documentation status
- Category `index.md` files - Add category-specific stats

**Example badge set**:
```markdown
![Prompts](https://img.shields.io/badge/Prompts-148-blue)
![Categories](https://img.shields.io/badge/Categories-8-green)
![Grade](https://img.shields.io/badge/Grade-B-yellow)
```

---

#### 2. Files That Could Benefit from Mermaid Diagrams

Currently 11 files use mermaid. Additional candidates:

| File | Diagram Type | Purpose |
|:-----|:-------------|:--------|
| `docs/getting-started.md` | flowchart | Decision tree for platform selection |
| `get-started/choosing-the-right-pattern.md` | flowchart | Pattern selection guide |
| `tutorials/building-effective-prompts.md` | flowchart | Component decision tree |
| `prompts/advanced/index.md` | graph | Pattern relationships |
| `workflows/sdlc.md` | sequence | Workflow visualization |

---

#### 3. Emoji Usage for Scannability

**Good examples** (already implemented):
- `EVALUATION_REPORT.md` - Uses 📊🎯🏆⚠️✅🔴🟡🟢

**Files that could benefit from emoji headers**:
- `docs/IMPROVEMENT_PLAN.md` - Priority sections
- `reference/cheat-sheet.md` - Quick pattern sections
- Category README files - Section markers

**Recommended emoji vocabulary**:
| Emoji | Use For |
|:-----:|:--------|
| 📊 | Data/Statistics |
| 🎯 | Goals/Targets |
| ⚠️ | Warnings |
| ✅ | Success/Done |
| ❌ | Errors/Avoid |
| 🔴🟠🟡🟢 | Priority levels |
| 💡 | Tips |
| 📝 | Notes |
| 🔗 | Links/References |

---

#### 4. Missing Table of Contents

Long documents (>500 lines) without TOC:

| File | Lines | Needs TOC |
|:-----|------:|:---------:|
| `prompts/governance/security-incident-response.md` | 750+ | ✅ |
| `prompts/governance/legal-contract-review.md` | 460+ | ✅ |
| `prompts/advanced/react-tool-augmented.md` | 450+ | Consider |
| `prompts/creative/brand-voice-developer.md` | 500+ | Consider |

---

## 📊 Report Structure Inconsistencies

### Generated Reports Comparison

| Report | Badges | Mermaid | Details | Centered | HR Rules | Grade |
|:-------|:------:|:-------:|:-------:|:--------:|:--------:|:-----:|
| `EVALUATION_REPORT.md` | ✅ | ✅ | ✅ | ✅ | ✅ | A |
| `TOT_EVALUATION_REPORT.md` | ❌ | ❌ | ❌ | ❌ | ✅ | C |
| `IMPROVEMENT_PLAN.md` | ❌ | ❌ | ❌ | ❌ | ✅ | C |

**Recommendation**: Update `TOT_EVALUATION_REPORT.md` and `IMPROVEMENT_PLAN.md` to match `EVALUATION_REPORT.md` styling

---

## 🤖 Automation Opportunities

### 1. Pre-commit Hook: Link Validator

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Find broken internal links
find prompts -name "*.md" -exec grep -l '\]\([^http][^)]*\.md\)' {} \; | while read file; do
  grep -oP '\]\(\K[^http][^)]*\.md' "$file" | while read link; do
    target="$(dirname "$file")/$link"
    if [ ! -f "$target" ]; then
      echo "BROKEN LINK in $file: $link"
      exit 1
    fi
  done
done
```

### 2. PowerShell Script: Add Language to Code Blocks

```powershell
# fix-code-blocks.ps1
Get-ChildItem -Path "prompts" -Recurse -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    # Replace empty code fences with ```text
    $content = $content -replace '(?m)^```\s*$(?!\s*```)', '```text'
    Set-Content $_.FullName $content
}
```

### 3. Python Validator: Section Order Check

```python
# validate_sections.py
import re
import sys
from pathlib import Path

EXPECTED_ORDER = ['Description', 'Use Cases', 'Prompt', 'Variables', 'Example', 'Tips', 'Related Prompts']

def check_file(path):
    content = path.read_text()
    sections = re.findall(r'^## (.+)$', content, re.MULTILINE)
    
    # Check required sections exist
    required = ['Description', 'Prompt', 'Variables', 'Example']
    missing = [s for s in required if s not in sections]
    
    if missing:
        print(f"{path}: Missing sections: {missing}")
        return False
    return True

if __name__ == "__main__":
    prompts = Path("prompts").rglob("*.md")
    errors = sum(1 for p in prompts if not check_file(p))
    sys.exit(1 if errors else 0)
```

### 4. Regex Patterns for Bulk Fixes

| Issue | Find Pattern | Replace Pattern |
|:------|:-------------|:----------------|
| Empty code fence | `` ^```\s*$ `` | `` ```text `` |
| Table without alignment | `\|---\|` | `\|:---\|` |
| Missing blank after H1 | `^# (.+)\n##` | `# $1\n\n##` |
| Inconsistent "Purpose" | `^## Purpose$` | `## Description` |

### 5. GitHub Action: Formatting Check

```yaml
# .github/workflows/format-check.yml
name: Format Check
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check broken links
        run: python scripts/check_links.py
      - name: Check code block languages
        run: |
          if grep -r "^\`\`\`$" prompts/; then
            echo "Found code blocks without language specifier"
            exit 1
          fi
      - name: Check required sections
        run: python scripts/validate_sections.py
```

---

## 📋 Prioritized Action Plan

### Week 1: Critical Fixes

- [ ] Fix 50 broken internal links
  - Option A: Create 15 missing referenced files
  - Option B: Update links to existing alternatives
  - Option C: Remove links to non-existent files
- [ ] Add missing sections to 8 Grade D prompts
- [ ] Standardize 19 files to use `## Description`

### Week 2: High Priority

- [ ] Add language specifiers to 40+ code blocks
- [ ] Add table alignment to all tables
- [ ] Wrap large tables in `<details>` tags
- [ ] Add Related Prompts to 8 missing files

### Week 3-4: Medium Priority

- [ ] Standardize section ordering across M365 prompts
- [ ] Add horizontal rules between major sections
- [ ] Add Input/Output separation to 30 examples
- [ ] Collapse long code blocks

### Month 2: Polish

- [ ] Add badges to key entry points
- [ ] Add mermaid diagrams to decision guides
- [ ] Standardize emoji usage
- [ ] Add TOC to long documents
- [ ] Update generated reports for consistency

### Ongoing: Automation

- [ ] Implement pre-commit link checker
- [ ] Create formatting validation script
- [ ] Add GitHub Action for PR checks
- [ ] Document formatting standards

---

## 📈 Success Metrics

| Metric | Current | Target | Timeline |
|:-------|--------:|-------:|:---------|
| Broken Links | 50 | 0 | 1 week |
| Files Missing Sections | 19 | 0 | 2 weeks |
| Code Blocks w/o Language | 40+ | 0 | 2 weeks |
| Tables w/o Alignment | ~80% | 0% | 3 weeks |
| Formatting Health Score | 72/100 | 90/100 | 4 weeks |

---

<div align="center">

**Report Generated**: 2025-12-03  
**Auditor**: Visual Formatting Analysis Tool  
**Methodology**: Automated grep/PowerShell analysis + manual sampling

*Prompt Library Formatting Audit — tafreeman/prompts*

</div>
