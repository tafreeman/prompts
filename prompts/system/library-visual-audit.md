---
title: "Library Visual & Formatting Audit"
shortTitle: "Visual Audit"
intro: "Systematically audit a prompt library for visual consistency, readability improvements, and formatting standardization opportunities."
type: "how_to"
difficulty: "intermediate"
audience:
  - "senior-engineer"
  - "technical-writer"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
topics:
  - "documentation"
  - "quality"
  - "refactoring"
author: "Prompts Library Team"
version: "1.0"
date: "2025-12-03"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "approved"
---

# Library Visual & Formatting Audit

## Description

This prompt performs a comprehensive visual and formatting audit of a prompt library, identifying opportunities for improved readability in Markdown viewers, GitHub rendering, and generated reports. It produces a prioritized list of specific improvements with file locations and suggested changes.

## Use Cases

- Standardizing visual formatting across a large prompt library
- Preparing documentation for public release or enterprise adoption
- Identifying inconsistencies in report generation scripts
- Improving GitHub Pages or documentation site rendering
- Creating a batch update plan for library-wide formatting improvements
- Ensuring accessibility and readability standards compliance

## Prompt

```text
You are a documentation quality auditor specializing in Markdown formatting, GitHub rendering, and technical documentation best practices.

## Your Task

Perform a comprehensive visual and formatting audit of the prompt library in this workspace. Analyze ALL files for opportunities to improve:

1. **Markdown Readability** - How files render in VS Code, GitHub, and documentation sites
2. **Report Generation** - Consistency in generated reports and automated outputs
3. **Visual Consistency** - Standardized formatting patterns across the library

## Audit Categories

### Category A: Structural Formatting

Scan for and report on:
- [ ] Inconsistent heading hierarchy (H1 → H2 → H3 flow)
- [ ] Missing or inconsistent horizontal rules (`---`) between sections
- [ ] Inconsistent blank line spacing (before/after headings, lists, code blocks)
- [ ] Files missing standard sections (Description, Prompt, Variables, Example, Tips)
- [ ] Inconsistent section ordering across similar files

### Category B: Tables & Data Presentation

Scan for and report on:
- [ ] Tables without alignment specifiers (`:---`, `:---:`, `---:`)
- [ ] Tables that could benefit from column alignment
- [ ] Data that should be in tables but is in plain lists
- [ ] Tables missing header rows or with inconsistent column counts
- [ ] Large tables that should use `<details>` collapsible sections
- [ ] Opportunities for adding emoji/icon columns for visual scanning

### Category C: Code Blocks & Examples

Scan for and report on:
- [ ] Code blocks missing language specifiers (```text, ```python, etc.)
- [ ] Inconsistent code fence styles (``` vs ~~~)
- [ ] Examples without clear Input/Output separation
- [ ] Code blocks that should be syntax highlighted but aren't
- [ ] Very long code blocks that could be collapsed
- [ ] Missing or inconsistent indentation in nested code

### Category D: Visual Enhancements

Scan for and report on:
- [ ] Opportunities for status badges (shields.io style)
- [ ] Files that could benefit from mermaid diagrams
- [ ] Places where emoji icons would improve scannability
- [ ] Opportunities for `<table>` HTML for complex layouts
- [ ] Missing visual hierarchy indicators (bold, icons, colors)
- [ ] Opportunities for `<details>` expandable sections
- [ ] Files that could benefit from centered `<div>` sections

### Category E: Links & Navigation

Scan for and report on:
- [ ] Broken or missing internal links
- [ ] Inconsistent relative vs absolute paths
- [ ] Missing "Related Prompts" sections
- [ ] Missing breadcrumb or navigation aids
- [ ] Opportunities for table of contents
- [ ] Anchor links that could improve navigation

### Category F: Metadata & Frontmatter

Scan for and report on:
- [ ] Missing or incomplete YAML frontmatter
- [ ] Inconsistent frontmatter field ordering
- [ ] Fields with inconsistent value formats (dates, arrays, strings)
- [ ] Missing governance or classification tags
- [ ] Opportunities for additional metadata fields

### Category G: Generated Reports

Scan for and report on:
- [ ] Reports using plain text where visual formatting would help
- [ ] Inconsistent report structures across different tools
- [ ] Missing executive summaries or dashboards
- [ ] Reports without visual progress indicators
- [ ] Opportunities for charts/graphs in reports
- [ ] Reports missing timestamps or version info

## Output Format

Return your findings as a structured Markdown document with:

### 1. Executive Summary
- Total files audited
- Overall formatting health score (A/B/C/D/F)
- Top 3 highest-impact improvements
- Estimated effort for full standardization

### 2. Critical Issues (Fix Immediately)
| File | Issue | Category | Impact | Fix |
|------|-------|----------|--------|-----|
| path/file.md | Description | A-G | High/Med/Low | Specific fix |

### 3. High Priority Improvements
Group by category with specific file lists and suggested changes.

### 4. Medium Priority Improvements
Bulk improvements that can be scripted or batch-applied.

### 5. Low Priority / Nice-to-Have
Visual polish items for future consideration.

### 6. Standardization Templates
Provide template snippets for:
- Standard section headers
- Table formatting
- Badge placement
- Collapsible section structure
- Report header/footer templates

### 7. Automation Opportunities
List improvements that could be automated via:
- Python scripts
- VS Code find/replace patterns
- Pre-commit hooks
- CI/CD checks

## Analysis Instructions

1. **Start with index files** - `index.md`, `README.md` files set the tone
2. **Sample each category** - Check 3-5 files from each prompts/ subfolder
3. **Compare generated reports** - Look at `docs/*.md` for report consistency
4. **Check templates** - Ensure `templates/` files follow best practices
5. **Review tools output** - Run evaluation scripts and assess their output format

## Quality Thresholds

| Metric | Target | Current Baseline |
|--------|--------|------------------|
| Files with proper heading hierarchy | 100% | Check |
| Tables with alignment | 100% | Check |
| Code blocks with language tags | 100% | Check |
| Files with all standard sections | 95%+ | Check |
| Internal links working | 100% | Check |
| Consistent frontmatter | 100% | Check |

Be thorough, specific, and actionable. Every issue should include:
1. Exact file path
2. Line number or section if applicable
3. Current state
4. Recommended change
5. Priority level
```text
## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `[WORKSPACE_PATH]` | Root path of the prompt library | `D:\source\prompts`, `./prompts` |
| `[FOCUS_AREA]` | Optional: limit audit to specific folder | `prompts/developers/`, `docs/` |
| `[OUTPUT_FORMAT]` | Report format preference | `markdown`, `json`, `csv` |
| `[SEVERITY_THRESHOLD]` | Minimum severity to report | `all`, `high`, `critical` |

## Example Usage

### Input

```text
You are a documentation quality auditor specializing in Markdown formatting, GitHub rendering, and technical documentation best practices.

Perform a comprehensive visual and formatting audit of the prompt library in the current workspace. Focus on the prompts/ and docs/ folders.

[Full prompt as above]
```text
### Output

```markdown
# Library Visual & Formatting Audit Report

**Audit Date**: 2025-12-03
**Files Analyzed**: 186
**Overall Health Score**: B (76/100)

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total files audited | 186 |
| Critical issues | 4 |
| High priority items | 23 |
| Medium priority items | 67 |
| Low priority items | 31 |

### Top 3 Highest-Impact Improvements

1. **Add table alignment to 89 tables** - Improves readability across all GitHub views
2. **Standardize code block languages** - 34 code blocks missing language specifiers
3. **Add collapsible sections to large reports** - 8 reports exceed 500 lines

### Estimated Effort

| Task | Effort | Automatable |
|------|--------|-------------|
| Table alignment | 2 hours | Yes (regex) |
| Code block languages | 1 hour | Yes (script) |
| Collapsible sections | 3 hours | Partial |
| Total | ~8 hours | 60% |

---

## Critical Issues (4)

| File | Issue | Category | Impact | Fix |
|------|-------|----------|--------|-----|
| `prompts/advanced/library.md` | Missing ## Prompt section entirely | A | High | Add prompt section with template |
| `docs/EVALUATION_REPORT.md` | 521 lines without navigation | D | High | Add TOC and collapsible categories |
| `prompts/system/example-research-output.md` | No frontmatter | F | High | Add complete YAML frontmatter |
| `reference/cheat-sheet.md` | 12 broken internal links | E | High | Update relative paths |

---

## High Priority Improvements (23)

### Category A: Structural Formatting (8 items)

| File | Issue | Fix |
|------|-------|-----|
| `prompts/developers/code-review-expert.md` | H3 before H2 | Reorder headings |
| `prompts/business/budget-tracker.md` | No horizontal rules | Add `---` between sections |
| `prompts/analysis/*.md` (6 files) | Missing Tips section | Add ## Tips with 3-5 items |

### Category B: Tables (9 items)

| File | Issue | Fix |
|------|-------|-----|
| `prompts/business/*.md` (9 files) | Tables without alignment | Add `:---:` for centered columns |

**Bulk Fix Pattern:**
```regex
Find: \| --- \|
Replace: | :--- |
```sql
### Category C: Code Blocks (6 items)

| File | Issue | Fix |
|------|-------|-----|
| `prompts/developers/sql-*.md` (3 files) | Code blocks missing `sql` tag | Add language specifier |
| `prompts/creative/*.md` (3 files) | Code blocks missing `text` tag | Add language specifier |

---

## Medium Priority Improvements (67)

### Add Visual Badges (12 files)

Files that would benefit from shields.io-style badges:

```markdown
<!-- Recommended badge set for prompt files -->
![Difficulty](https://img.shields.io/badge/Difficulty-Intermediate-yellow)
![Platform](https://img.shields.io/badge/Platform-Claude%20%7C%20GPT-blue)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green)
```sql
**Files to update:**
- `prompts/governance/legal-contract-review.md`
- `prompts/governance/security-incident-response.md`
- [10 more files...]

### Add Mermaid Diagrams (8 files)

Files describing workflows or processes that would benefit from diagrams:

| File | Diagram Type | Purpose |
|------|--------------|---------|
| `prompts/advanced/react-*.md` | flowchart | Show Thought→Action→Observation loop |
| `prompts/business/project-*.md` | gantt | Show timeline/milestone structure |
| `docs/IMPROVEMENT_PLAN.md` | timeline | Show week-by-week improvement plan |

### Collapsible Sections Needed (15 files)

Files with large content blocks that should use `<details>`:

```markdown
<details>
<summary><b>View all 36 Business prompts</b></summary>

| Prompt | Quality | Effectiveness |
|--------|---------|---------------|
| ... | ... | ... |

</details>
```text
---

## Low Priority / Nice-to-Have (31)

### Emoji Standardization

Current emoji usage is inconsistent. Recommended standard:

| Context | Emoji | Usage |
|---------|-------|-------|
| Sections | 📋 📊 💡 🎯 | Category headers |
| Status | ✅ ⚠️ 🔧 ❌ | Quality indicators |
| Priority | 🔴 🟠 🟡 🟢 | Urgency levels |
| Types | 💻 💼 🎨 📧 | Category icons |

### Footer Standardization

Add consistent footer to all generated reports:

```markdown
---

<div align="center">

*Generated by [Tool Name] | [Repository Name]*

</div>
```text
---

## Standardization Templates

### Standard Prompt Header

```markdown
---
title: "[Title]"
shortTitle: "[Short Title]"
intro: "[2-3 sentence description]"
...
---

# [Title]

<div align="center">

![Difficulty](https://img.shields.io/badge/Difficulty-[Level]-[color])
![Platforms](https://img.shields.io/badge/Platforms-[list]-blue)

</div>

## Description

[2-3 paragraphs]

---
```text
### Standard Table Format

```markdown
| Column 1 | Column 2 | Column 3 |
|:---------|:--------:|---------:|
| Left     | Center   | Right    |
```text
### Standard Collapsible Section

```markdown
<details>
<summary><b>Section Title (X items)</b></summary>

[Content here]

</details>
```text
---

## Automation Opportunities

### Python Script: `tools/format_tables.py`

```python
# Auto-add alignment to markdown tables
# Run: python tools/format_tables.py --all
```text
### VS Code Find/Replace Patterns

```yaml
# Add language to unmarked code blocks
Find: ```\n(?!text|python|sql|markdown|json|yaml)
Replace: ```text\n

# Standardize horizontal rules
Find: ^-{3,}$
Replace: ---
```sql
### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    - id: check-markdown-tables
      name: Check table alignment
      entry: python tools/check_tables.py
      language: python
      files: \.md$
```text
---

## Next Steps

1. [ ] Fix 4 critical issues (1 hour)
2. [ ] Run bulk table alignment script (30 min)
3. [ ] Add language tags to code blocks (30 min)
4. [ ] Add collapsible sections to reports (2 hours)
5. [ ] Standardize emoji usage (1 hour)
6. [ ] Create pre-commit hooks (1 hour)

**Total estimated effort: 6-8 hours**

---

*Audit completed: 2025-12-03*
```text
## Tips

- **Start with high-traffic files**: README.md, index.md, and main documentation get the most views
- **Use VS Code's Markdown preview**: Toggle preview (`Ctrl+Shift+V`) to see rendering issues
- **Check GitHub rendering**: Some features (mermaid, HTML tables) render differently on GitHub
- **Batch similar fixes**: Group files with the same issue for efficient bulk updates
- **Create automation first**: A 30-minute script saves hours of manual work
- **Test on multiple viewers**: VS Code, GitHub, and documentation sites render differently

## Platform Adaptations

### GitHub Copilot

Use `@workspace` to ensure full context:

```text
@workspace Perform a visual formatting audit of all markdown files. Focus on tables, code blocks, and section consistency. Return a prioritized list of improvements.
```text
### Claude

Claude excels at comprehensive analysis. Add:

```text
Be exhaustive in your analysis. Check every file, not just samples. I want a complete inventory of formatting inconsistencies.
```text
### ChatGPT

For large libraries, process in chunks:

```text
Audit the prompts/developers/ folder first. Then I'll ask you to audit other folders. Track issues in a running list.
```text
## Related Prompts

- [Prompt Quality Evaluator](prompt-quality-evaluator.md) - Evaluate prompt content quality
- [Library Analysis ReAct](../advanced/library-analysis-react.md) - Deep library analysis
- [Tree-of-Thoughts Evaluator](../advanced/tree-of-thoughts-evaluator-reflection.md) - Comprehensive assessment
