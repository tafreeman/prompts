# 📋 Library Visual & Formatting Audit Report

<div align="center">

![Audit](https://img.shields.io/badge/Audit-Complete-green)
![Files](https://img.shields.io/badge/Files%20Analyzed-305-blue)
![Health](https://img.shields.io/badge/Health%20Score-72%2F100-yellow)
![Issues](https://img.shields.io/badge/Issues%20Found-226-orange)

**Comprehensive Visual and Formatting Assessment**

*Generated: December 3, 2025*

</div>

---

## 📈 Executive Summary

<table>
<tr>
<td width="25%" align="center">

### 📁 Files Audited
# 305
**148 prompts**

</td>
<td width="25%" align="center">

### 🎯 Health Score
# 72/100
**Grade C+**

</td>
<td width="25%" align="center">

### 🔴 Critical
# 8
**Fix immediately**

</td>
<td width="25%" align="center">

### 🟡 Total Issues
# 226
**Across all categories**

</td>
</tr>
</table>

---

### Top 3 Highest-Impact Improvements

| Priority | Issue | Files Affected | Effort | Impact |
|:--------:| :--- |---------------:|:------:|:------:|
| 🥇 | Fix 50 broken internal links | 50 | 2 hrs | 🔴 Critical |
| 🥈 | Add table alignment specifiers | 89 | 1 hr | 🟠 High |
| 🥉 | Add language tags to code blocks | 40+ | 1 hr | 🟠 High |

### Estimated Total Effort

| Category | Issues | Effort | Automatable |
| :--- |-------:|:------:|:-----------:|
| Critical (fix immediately) | 8 | 3 hrs | Partial |
| High priority | 50 | 4 hrs | 80% |
| Medium priority | 103 | 6 hrs | 60% |
| Low priority | 65 | 4 hrs | 40% |
| **Total** | **226** | **~17 hrs** | **65%** |

---

## 🔴 Critical Issues (8)

These must be fixed before enterprise deployment:

### 1. Broken Internal Links (50 files)

Related Prompts sections reference non-existent files:

| File | Broken Link | Fix |
| :--- |-------------| :--- |
| `prompts/advanced/chain-of-thought-concise.md` | `reflection-code-review-self-check.md` | Remove or create file |
| `prompts/advanced/chain-of-thought-detailed.md` | `tree-of-thoughts-decision-guide.md` | Update to `chain-of-thought-guide.md` |
| `prompts/business/agile-sprint-planner.md` | `project-charter-creator.md` | Remove or create file |
| `prompts/business/board-update-generator.md` | `executive-summary-writer.md` | Remove or create file |
| `prompts/business/budget-cost-controller.md` | `financial-report-generator.md` | Remove or create file |
| ... | ... | ... |

**Bulk Fix Script:**
```powershell
# Find all broken links in Related Prompts sections
Get-ChildItem -Path "prompts" -Filter "*.md" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $links = [regex]::Matches($content, '\[.*?\]\((\.\.?/.*?\.md)\)')
    foreach ($link in $links) {
        $target = Join-Path $_.DirectoryName $link.Groups[1].Value
        if (-not (Test-Path $target)) {
            Write-Output "$($_.FullName): Broken link to $($link.Groups[1].Value)"
        }
    }
}
```

### 2. Files Missing Standard Sections (19 files)

| File | Missing Sections |
| :--- |------------------|
| `prompts/advanced/library.md` | Prompt, Variables, Example |
| `prompts/advanced/chain-of-thought-guide.md` | Prompt |
| `prompts/advanced/prompt-library-refactor-react.md` | Prompt, Example |
| `prompts/advanced/example-research-output.md` | Prompt, Variables, Example |
| `prompts/analysis/library-capability-radar.md` | Variables |
| `prompts/analysis/library-network-graph.md` | Variables |
| `prompts/analysis/library-structure-treemap.md` | Variables |
| `prompts/system/example-research-output.md` | Frontmatter, Prompt, Variables |
| `testing/evals/*.md` (6 files) | Frontmatter |
| ... | ... |

### 3. Non-Standard Heading Hierarchy (19 files)

Files not following `# Title` → `## Description` → `## Prompt` pattern:

| File | Issue |
| :--- |-------|
| `prompts/m365/m365-customer-feedback-analyzer.md` | Starts with H2, no H1 |
| `prompts/m365/m365-data-insights.md` | H3 before H2 |
| `prompts/m365/m365-designer-image-prompt.md` | Mixed hierarchy |
| `prompts/developers/api-design-consultant.md` | Missing H1 |
| ... | ... |

---

## 🟠 High Priority (50 items)

### Category A: Structural Formatting (12 items)

#### Missing Horizontal Rules

19 files lack `---` separators between major sections:

```markdown
# Current (no separation)
## Description
Content here
## Prompt
Content here

# Recommended
## Description
Content here

---

## Prompt
Content here
```

**Files to update:**
- `prompts/developers/code-review-expert.md`
- `prompts/developers/code-review-expert-structured.md`
- `prompts/developers/api-design-consultant.md`
- `prompts/developers/security-code-auditor.md`
- `prompts/developers/sql-security-enforcer.md`
- `prompts/developers/test-automation-engineer.md`
- ... (13 more files)

#### Inconsistent Section Ordering

M365 prompts use different section order than other categories:

| Standard Order | M365 Order |
| :--- |------------|
| Description | Overview |
| Use Cases | When to Use |
| Prompt | Prompt |
| Variables | Inputs |
| Example | Example |
| Tips | Best Practices |

**Recommendation:** Standardize to library-wide order or add mapping comments.

---

### Category B: Tables & Data Presentation (15 items)

#### Tables Missing Alignment (89 files)

**Current (no alignment):**
```markdown
| Column | Data |
<<<<<<< HEAD
| :--- | :--- |
=======
| :--- | --- |
>>>>>>> main
| Value | Value |
```

**Recommended:**
```markdown
| Column | Data |
|:-------|-----:|
| Value  | 123  |
```

**Bulk Fix Regex:**
```
Find: \| --- \|
Replace: | :--- |
```

**Files with 5+ unaligned tables:**
- `docs/EVALUATION_REPORT.md` (12 tables)
- `docs/IMPROVEMENT_PLAN.md` (8 tables)
- `prompts/business/business-strategy-analysis.md` (6 tables)
- `reference/cheat-sheet.md` (9 tables)
- `reference/platform-comparison.md` (7 tables)

#### Large Tables Needing Collapsible Sections

Tables with 15+ rows should use `<details>`:

| File | Table Rows | Section |
| :--- |------------| :--- |
| `docs/EVALUATION_REPORT.md` | 36 (Business) | Category tables |
| `docs/EVALUATION_REPORT.md` | 24 (Developers) | Category tables |
| `docs/EVALUATION_REPORT.md` | 22 (System) | Category tables |
| `reference/cheat-sheet.md` | 25+ | Pattern tables |

**Template:**
```markdown
<details>
<summary><b>View all 36 Business prompts</b></summary>

| Prompt | Quality | Effectiveness |
|:-------|:-------:|:-------------:|
| ... | ... | ... |

</details>
```

---

### Category C: Code Blocks & Examples (15 items)

#### Code Blocks Missing Language Specifiers (40+ files)

| File | Block Count | Suggested Language |
| :--- |------------:|:------------------:|
| `prompts/developers/sql-*.md` | 8 | `sql` |
| `prompts/developers/csharp-*.md` | 6 | `csharp` |
| `prompts/creative/*.md` | 12 | `text` |
| `prompts/business/*.md` | 14 | `text` or `markdown` |

**Fix Pattern:**
```markdown
# Before
```
SELECT * FROM users
```

# After
```sql
SELECT * FROM users
```
```

#### Examples Without Input/Output Separation

32 files have examples without clear structure:

**Current:**
```markdown
## Example
Here is an example of using this prompt with real values...
```

**Recommended:**
```markdown
## Example Usage

### Input

```text
[Example input with variables replaced]
```

### Output

```text
[Example of expected output]
```
```

---

### Category D: Visual Enhancements (8 items)

#### Files Needing Badges (Top Candidates)

Only 2 files currently use shields.io badges. High-value additions:

| File | Recommended Badges |
| :--- |-------------------|
| `README.md` | Version, Prompts Count, License |
| `prompts/governance/*.md` | Compliance Status, Review Status |
| `prompts/advanced/*.md` | Difficulty, Platform Support |
| `agents/*.agent.md` | Agent Status, Compatibility |

**Badge Template:**
```markdown
<div align="center">

![Difficulty](https://img.shields.io/badge/Difficulty-Advanced-red)
![Platforms](https://img.shields.io/badge/Platforms-Claude%20%7C%20GPT%20%7C%20Copilot-blue)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green)

</div>
```

#### Files Benefiting from Mermaid Diagrams

| File | Diagram Type | Purpose |
| :--- |:------------:| :--- |
| `prompts/advanced/react-*.md` | flowchart | Thought→Action→Observation loop |
| `prompts/advanced/tree-of-thoughts-*.md` | graph | Branch structure |
| `docs/IMPROVEMENT_PLAN.md` | gantt | Timeline visualization |
| `get-started/choosing-the-right-pattern.md` | flowchart | Decision tree |

---

## 🟡 Medium Priority (103 items)

### Inconsistent Emoji Usage

Current usage is sporadic. Recommended standard:

| Context | Emoji | Example |
| :--- |:-----:| :--- |
| Section headers | 📋 📊 💡 🎯 ⚙️ | `## 📋 Description` |
| Status indicators | ✅ ⚠️ 🔧 ❌ | In tables |
| Priority levels | 🔴 🟠 🟡 🟢 | In reports |
| Categories | 🧠 💼 🎨 💻 📧 🏛️ | Category headers |

**Files needing emoji standardization:** 89 (all prompts)

### Missing Table of Contents

Long files (>300 lines) without TOC:

| File | Lines | Sections |
| :--- |------:|:--------:|
| `docs/EVALUATION_REPORT.md` | 521 | 15 |
| `docs/TOT_EVALUATION_REPORT.md` | 398 | 12 |
| `README.md` | 350+ | 10 |
| `reference/cheat-sheet.md` | 400+ | 8 |
| `docs/ultimate-prompting-guide.md` | 500+ | 12 |

**TOC Template:**
```markdown
## Table of Contents

- [Executive Summary](#executive-summary)
- [Scoring Methodology](#scoring-methodology)
- [Category Reports](#category-reports)
  - [Advanced](#advanced)
  - [Business](#business)
- [Appendix](#appendix)
```

### Centered Footer Missing

Only generated reports have footers. All prompts should have:

```markdown
---

<div align="center">

*Part of the Enterprise AI Prompt Library*

</div>
```

---

## 🟢 Low Priority (65 items)

### Nice-to-Have Improvements

| Improvement | Files | Effort |
| :--- |------:|:------:|
| Add "Last Updated" to prompts | 148 | Low |
| Add word count badges | 148 | Script |
| Standardize frontmatter field order | 148 | Script |
| Add reading time estimates | 148 | Script |
| Create category index cards | 8 | Medium |

### Visual Polish

- Add syntax highlighting themes to examples
- Create consistent screenshot/diagram style guide
- Add dark mode considerations to color choices
- Standardize quote block usage (`>`)

---

## 🛠️ Automation Opportunities

### 1. Python Script: `tools/fix_formatting.py`

```python
#!/usr/bin/env python3
"""Auto-fix common formatting issues across the library."""

import re
from pathlib import Path

def fix_table_alignment(content: str) -> str:
    """Add left alignment to table separators."""
    return re.sub(r'\| --- \|', '| :--- |', content)

def fix_code_blocks(content: str) -> str:
    """Add 'text' language to unmarked code blocks."""
    return re.sub(r'```\n(?!text|python|sql|csharp|json|yaml|markdown|powershell|bash)', 
                  '```text\n', content)

def add_horizontal_rules(content: str) -> str:
    """Add --- before ## headings if missing."""
    return re.sub(r'([^\n])\n(## )', r'\1\n\n---\n\n\2', content)

def process_file(path: Path):
    content = path.read_text(encoding='utf-8')
    original = content
    
    content = fix_table_alignment(content)
    content = fix_code_blocks(content)
    # content = add_horizontal_rules(content)  # Be careful with this one
    
    if content != original:
        path.write_text(content, encoding='utf-8')
        print(f"✅ Fixed: {path}")

if __name__ == "__main__":
    for md_file in Path("prompts").rglob("*.md"):
        process_file(md_file)
```

### 2. PowerShell: Find Broken Links

```powershell
# tools/find-broken-links.ps1
$brokenLinks = @()

Get-ChildItem -Path "prompts","docs" -Filter "*.md" -Recurse | ForEach-Object {
    $file = $_
    $content = Get-Content $file.FullName -Raw
    
    # Find markdown links
    $links = [regex]::Matches($content, '\[([^\]]+)\]\(([^)]+\.md)\)')
    
    foreach ($link in $links) {
        $linkPath = $link.Groups[2].Value
        if ($linkPath -notmatch '^https?://') {
            $resolvedPath = Join-Path $file.DirectoryName $linkPath
            if (-not (Test-Path $resolvedPath)) {
                $brokenLinks += [PSCustomObject]@{
                    File = $file.FullName
                    LinkText = $link.Groups[1].Value
                    BrokenPath = $linkPath
                }
            }
        }
    }
}

$brokenLinks | Format-Table -AutoSize
$brokenLinks | Export-Csv "docs/broken-links.csv" -NoTypeInformation
```

### 3. VS Code Find/Replace Patterns

```text
# Add alignment to tables
Find:    \| --- \|
Replace: | :--- |

# Add language to code blocks
Find:    ```\n([^`])
Replace: ```text\n$1

# Standardize horizontal rules
Find:    ^-{4,}$
Replace: ---

# Fix double blank lines
Find:    \n{3,}
Replace: \n\n
```

### 4. Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: check-markdown-formatting
        name: Check Markdown Formatting
        entry: python tools/check_formatting.py
        language: python
        files: \.md$
        
      - id: check-broken-links
        name: Check Internal Links
        entry: python tools/check_links.py
        language: python
        files: \.md$
```

### 5. GitHub Action Workflow

```yaml
# .github/workflows/docs-quality.yml
name: Documentation Quality

on:
  pull_request:
    paths:
      - 'prompts/**/*.md'
      - 'docs/**/*.md'

jobs:
  check-formatting:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check table alignment
        run: |
          if grep -rn "| :--- |" prompts/ docs/; then
            echo "::error::Found unaligned tables"
            exit 1
          fi
          
      - name: Check code block languages
        run: |
          python tools/check_code_blocks.py
          
      - name: Check broken links
        run: |
          python tools/check_links.py
```

---

## 📅 Recommended Action Plan

### Week 1: Critical Fixes

- [ ] Fix 50 broken internal links (2 hrs)
- [ ] Add missing sections to 8 Grade D prompts (3 hrs)
- [ ] Fix heading hierarchy in 19 files (1 hr)

### Week 2: High Priority

- [ ] Run table alignment bulk fix (30 min)
- [ ] Add language tags to 40+ code blocks (1 hr)
- [ ] Add `<details>` to large tables in reports (2 hrs)
- [ ] Standardize M365 prompt structure (2 hrs)

### Week 3: Medium Priority

- [ ] Add Input/Output structure to 32 examples (3 hrs)
- [ ] Add badges to governance and advanced prompts (1 hr)
- [ ] Add TOC to 5 long documents (1 hr)
- [ ] Create mermaid diagrams for advanced prompts (2 hrs)

### Week 4: Polish & Automation

- [ ] Deploy pre-commit hooks (1 hr)
- [ ] Create GitHub Action workflow (1 hr)
- [ ] Standardize emoji usage (2 hrs)
- [ ] Add footers to all prompts (script, 30 min)

---

## 📊 Success Metrics

| Metric | Current | Target | Timeline |
| :--- |:-------:|:------:|:--------:|
| Broken links | 50 | 0 | Week 1 |
| Unaligned tables | 89 | 0 | Week 2 |
| Missing code languages | 40+ | 0 | Week 2 |
| Files with all standard sections | 87% | 100% | Week 1 |
| Health Score | 72/100 | 90/100 | Week 4 |

---

<div align="center">

**Audit Completed**: December 3, 2025  
**Auditor**: Library Visual Audit Prompt  
**Next Audit**: After Week 4 fixes

*Enterprise AI Prompt Library — tafreeman/prompts*

</div>
