---
title: "ReAct: Prompt Library Analysis"
shortTitle: "Repo Analysis ReAct"
intro: "ReAct-based prompt for analyzing and improving prompt library repository structure, content gaps, and quality."
type: "how_to"
difficulty: "advanced"
audience:
  - "senior-engineer"
  - "solution-architect"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
topics:
  - "analysis"
  - "architecture"
  - "quality-assurance"
author: "Prompt Library Team"
version: "3.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "approved"
---
# ReAct: Prompt Library Analysis

## Description

This is an executable ReAct (Reasoning + Acting) prompt for analyzing prompt library repositories. Use this prompt to systematically audit content, identify gaps, validate standards compliance, and generate improvement recommendations.

## Goal

Perform comprehensive analysis of a prompt library repository to:

1. **Map repository structure** - Document folder hierarchy and content distribution
2. **Audit frontmatter compliance** - Validate all files against schema requirements
3. **Identify content gaps** - Find missing prompt categories and coverage holes
4. **Assess quality** - Evaluate prompt effectiveness and documentation completeness
5. **Generate expansion roadmap** - Prioritize new content creation

---

## Current Repository Context

> **Note**: This context reflects the `tafreeman/prompts` repository state as of November 2025.

### Completed State

| Component | Status | Details |
|-----------|--------|---------|
| Frontmatter schema | ✅ Complete | 19 standardized fields |
| Content types | ✅ Complete | conceptual, quickstart, how_to, tutorial, reference, troubleshooting |
| Total prompts | 145+ | Across 8 categories |
| Validation tooling | ✅ Complete | `tools/validators/frontmatter_validator.py` |

### Known Gaps (Expansion Targets)

| Category | Current Count | Target | Priority |
|----------|---------------|--------|----------|
| Creative | 2 prompts | 15-20 | **HIGH** |
| Business | 26 prompts | 35-40 | MEDIUM |

---

## Available Tools

When executing this analysis, you have access to:

### 1. `file_search`
Search for files matching glob patterns.
```
file_search("**/*.md") → Find all markdown files
file_search("prompts/**/*.md") → Find all prompts
```

### 2. `read_file`
Read file contents to inspect frontmatter and content.
```
read_file("/path/to/file.md") → Get file content
```

### 3. `grep_search`
Search for patterns across files.
```
grep_search("type: how_to") → Find all how_to prompts
grep_search("difficulty: beginner") → Find beginner content
```

### 4. `list_dir`
List directory contents to map structure.
```
list_dir("/prompts/") → Get folder structure
```

### 5. `run_in_terminal`
Execute validation scripts.
```
python tools/validators/frontmatter_validator.py <file>
python tools/validate_all.py
```

---

## ReAct Analysis Loop

Execute analysis using iterative Thought → Action → Observation cycles:

### Phase 1: Structure Mapping

**Thought**: I need to understand the repository structure before analyzing content.

**Action**: Map the folder hierarchy
```
list_dir("/") → Get top-level structure
list_dir("/prompts/") → Get prompt categories
```

**Observation**: Document the folder tree and note category organization.

---

### Phase 2: Content Inventory

**Thought**: I need to count and categorize all prompts to identify distribution.

**Action**: Search and count files by category
```
file_search("prompts/creative/*.md") → Count creative prompts
file_search("prompts/business/*.md") → Count business prompts
file_search("prompts/developers/*.md") → Count developer prompts
```

**Observation**: Create inventory table showing prompts per category.

---

### Phase 3: Frontmatter Audit

**Thought**: I need to verify all files comply with the frontmatter schema.

**Action**: Run validation and check specific fields
```
run_in_terminal("python tools/validate_all.py")
grep_search("governance_tags:") → Check governance compliance
grep_search("dataClassification:") → Check classification coverage
```

**Observation**: Document validation results, noting any failures or warnings.

---

### Phase 4: Gap Analysis

**Thought**: I need to compare current content against target coverage.

**Action**: Analyze content distribution
```
grep_search("type: quickstart") → Count quickstarts per platform
grep_search("difficulty: beginner") → Count beginner-friendly content
grep_search("audience:.*junior") → Count junior engineer content
```

**Observation**: Identify gaps in:
- Platform coverage (github-copilot, claude, chatgpt, azure-openai, m365-copilot)
- Difficulty balance (beginner vs intermediate vs advanced)
- Audience coverage (junior, senior, architect, business)

---

### Phase 5: Quality Assessment

**Thought**: I need to evaluate prompt quality and documentation completeness.

**Action**: Sample and review prompts
```
read_file("/prompts/creative/[sample].md") → Check content quality
read_file("/prompts/business/[sample].md") → Check documentation
```

**Observation**: Score prompts on:
- Clear description (1-5)
- Complete frontmatter (1-5)
- Example quality (1-5)
- Practical usability (1-5)

---

### Phase 6: Expansion Recommendations

**Thought**: Based on gaps identified, I need to prioritize new content.

**Action**: Cross-reference gaps with research
```
# Reference the Knowledge Base Research prompt for external best practices
# Compare against industry prompt libraries
```

**Observation**: Generate prioritized expansion roadmap.

---

## Required Deliverables

After completing the ReAct loop, produce:

### 1. Repository Health Report

```markdown
## Repository Analysis Summary

**Analysis Date**: YYYY-MM-DD
**Total Files Analyzed**: X
**Validation Pass Rate**: X%

### Structure Overview
[Folder tree with file counts]

### Content Distribution
| Category | Count | % of Total | Health |
|----------|-------|------------|--------|
| ...      | ...   | ...        | ✅/⚠️/❌ |
```

### 2. Gap Analysis Matrix

```markdown
## Content Gap Analysis

### By Platform
| Platform | Quickstart | How-To | Tutorial | Reference |
|----------|------------|--------|----------|-----------|
| github-copilot | ✅ | ⚠️ | ❌ | ✅ |
| ...      | ...        | ...    | ...      | ...       |

### By Audience
| Audience | Beginner | Intermediate | Advanced |
|----------|----------|--------------|----------|
| junior-engineer | X prompts | X prompts | X prompts |
| ...      | ...      | ...          | ...      |
```

### 3. Expansion Roadmap

```markdown
## Priority Expansion Roadmap

### P0 - Critical (Creative Category)
| Prompt | Type | Difficulty | Effort |
|--------|------|------------|--------|
| professional-email-writer.md | how_to | beginner | S |
| blog-post-generator.md | how_to | intermediate | M |
| ...    | ...  | ...        | ...    |

### P1 - High (Business Expansion)
| Prompt | Type | Difficulty | Effort |
|--------|------|------------|--------|
| pitch-deck-generator.md | how_to | intermediate | M |
| ...    | ...  | ...        | ...    |
```

### 4. Quality Scorecard

```markdown
## Quality Assessment

**Overall Score**: X/5

### By Dimension
| Dimension | Score | Notes |
|-----------|-------|-------|
| Frontmatter Compliance | X/5 | ... |
| Documentation Completeness | X/5 | ... |
| Example Quality | X/5 | ... |
| Practical Usability | X/5 | ... |
```

---

## Expansion Priorities

Based on current repository state, prioritize analysis on these areas:

### Creative Category (CRITICAL - 2 prompts → 15-20 target)

**Research Focus Areas**:
- Professional writing prompts (emails, reports, proposals)
- Marketing content generation (blogs, social, ads)
- Editing and refinement tools (tone, simplification)
- Storytelling and narrative (case studies, presentations)

**Recommended Additions**:
1. `professional-email-writer.md` - Formal business emails
2. `blog-post-generator.md` - Long-form content
3. `social-media-creator.md` - Platform-specific posts
4. `tone-adjuster.md` - Formal ↔ casual conversion
5. `report-summarizer.md` - Executive summaries
6. `proposal-generator.md` - Project proposals
7. `case-study-builder.md` - Customer success stories
8. `content-simplifier.md` - Plain language conversion

### Business Category (MEDIUM - 26 prompts → 35-40 target)

**Research Focus Areas**:
- Sales enablement (pitch, objection handling, follow-up)
- HR and recruiting (job descriptions, interviews)
- Executive communications (board updates, all-hands)

**Recommended Additions**:
1. `pitch-deck-generator.md` - Sales presentations
2. `objection-handler.md` - Sales objection responses
3. `job-description-writer.md` - Role descriptions
4. `interview-question-generator.md` - Role-specific questions
5. `board-update-generator.md` - Executive summaries

---

## Execution Instructions

To run this analysis:

1. **Initialize**: Load this prompt into your AI assistant
2. **Scope**: Specify the repository path to analyze
3. **Execute**: Follow the ReAct loop phases sequentially
4. **Iterate**: Use observations to refine subsequent actions
5. **Synthesize**: Compile deliverables from all observations
6. **Validate**: Run validation tools to confirm findings

---

## Related Resources

- [Knowledge Base Research](/prompts/advanced/react-knowledge-base-research) - External research prompt
- [Frontmatter Validator](/tools/validators/frontmatter_validator.py) - Validation tooling
- [Prompt Template](/templates/prompt-template.md) - Template for new prompts

---
