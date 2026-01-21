---
name: Library Visual & Formatting Audit
description: Systematically audit a prompt library for visual consistency, readability improvements, and formatting standardization opportunities.
type: how_to
---

# Library Visual & Formatting Audit

## Description

This prompt systematically audits a prompt library for visual consistency, readability improvements, and formatting standardization opportunities. It generates actionable reports identifying structural issues, table formatting problems, code block inconsistencies, and provides automation scripts for batch fixes.

## Prompt

```text
You are a Documentation Quality Auditor specializing in Markdown formatting and visual consistency.

### Audit Task
Conduct a comprehensive visual and formatting audit of this prompt library.

### Audit Dimensions

1. **Structural Formatting**
   - Heading hierarchy (H1 → H2 → H3 in order)
   - Horizontal rules between major sections
   - Consistent section ordering across files

2. **Table Formatting**
   - Column alignment (left, center, right)
   - Header row consistency
   - Cell content formatting

3. **Code Blocks**
   - Language specifiers present (```python, ```text, etc.)
   - Proper indentation within blocks
   - Consistent use of fenced vs. indented blocks

4. **Visual Elements**
   - Emoji usage consistency
   - Badge/shield formatting
   - Collapsible sections for long content

### Output Format
Generate a report with:
- Executive summary with metrics
- Issues categorized by priority (Critical, High, Medium, Low)
- Bulk fix patterns (regex) where applicable
- Estimated effort for each fix category
```

## Use Cases

- Standardizing visual formatting across a large prompt library
- Preparing documentation for public release or enterprise adoption
- Identifying inconsistencies in report generation scripts
- Improving GitHub Pages or documentation site rendering
- Creating a batch update plan for library-wide formatting improvements
- Ensuring accessibility and readability standards compliance

## Variables

This prompt is designed to work on the current workspace without explicit variables. The AI agent will automatically scan the workspace structure to identify:

- **Workspace path**: Current repository or documentation folder
- **File patterns**: `*.md` files across all directories
- **Report locations**: `docs/`, `docs/reports/` folders for generated content
- **Template locations**: `templates/` folder for standard templates

## Executive Summary

| Metric | Value |
| -------- | ------- |
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
| ------ | -------- | ------------- |
| Table alignment | 2 hours | Yes (regex) |
| Code block languages | 1 hour | Yes (script) |
| Collapsible sections | 3 hours | Partial |
| Total | ~8 hours | 60% |

## High Priority Improvements (23)

### Category A: Structural Formatting (8 items)

| File | Issue | Fix |
| ------ | ------- | ----- |
| `prompts/developers/code-review-expert.md` | H3 before H2 | Reorder headings |
| `prompts/business/budget-tracker.md` | No horizontal rules | Add `---` between sections |
| `prompts/analysis/*.md` (6 files) | Missing Tips section | Add ## Tips with 3-5 items |

### Category B: Tables (9 items)

| File | Issue | Fix |
| ------ | ------- | ----- |
| `prompts/business/*.md` (9 files) | Tables without alignment | Add `:---:` for centered columns |

**Bulk Fix Pattern:**

```regex

Find: \| --- \|
Replace: | :--- |

```text

### Category C: Code Blocks (6 items)

| File | Issue | Fix |
| ------ | ------- | ----- |
| `prompts/developers/sql-*.md` (3 files) | Code blocks missing `sql` tag | Add language specifier |
| `prompts/creative/*.md` (3 files) | Code blocks missing `text` tag | Add language specifier |

## Low Priority / Nice-to-Have (31)

### Emoji Standardization

Current emoji usage is inconsistent. Recommended standard:

| Context | Emoji | Usage |
| --------- | ------- | ------- |
| Sections | 📋 📊 💡 🎯 | Category headers |
| Status | ✅ ⚠️ 🔧 ❌ | Quality indicators |
| Priority | 🔴 🟠 🟡 🟢 | Urgency levels |
| Types | 💻 💼 🎨 📧 | Category icons |

### Footer Standardization

Add consistent footer to all generated reports:

```markdown

## Standardization Templates

### Standard Prompt Header

```markdown

# [Title]

<div align="center">

![Difficulty](https://img.shields.io/badge/Difficulty-[Level]-[color])
![Platforms](https://img.shields.io/badge/Platforms-[list]-blue)

</div>

```text

### Standard Collapsible Section

```markdown

<details>
<summary><b>Section Title (X items)</b></summary>

[Content here]

</details>

```xml

```text

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

```python

*Audit completed: 2025-12-03*
```text

```markdown

### Claude

Claude excels at comprehensive analysis. Add:

```text

Be exhaustive in your analysis. Check every file, not just samples. I want a complete inventory of formatting inconsistencies.

```text

---

## Example

**Input:**

```text
Audit the prompts/ directory for visual and formatting consistency.
```

**Output (Summary):**

```markdown
## Executive Summary

| Metric | Value |
| -------- | ------- |
| Total files audited | 186 |
| Critical issues | 4 |
| High priority items | 23 |

### Top 3 Most Impactful Fixes

1. **89 tables need alignment specifiers** (`:---` for left, `:---:` for center)
   - Regex: `\| --- \|` → `| :--- |`
   - Effort: 2 hours (automated)

2. **34 code blocks missing language tags**
   - Affects syntax highlighting in GitHub
   - Effort: 1 hour (script-assisted)

3. **8 reports over 500 lines need collapsible sections**
   - Use `<details>` tags for large reference sections
   - Effort: 3 hours (manual review needed)
```

## Related Prompts

- [Prompt Quality Evaluator](prompt-quality-evaluator.md) - Evaluate prompt content quality
- [Library Analysis ReAct](../advanced/library-analysis-react.md) - Deep library analysis
- [Tree-of-Thoughts Evaluator](../advanced/tree-of-thoughts-evaluator-reflection.md) - Comprehensive assessment
