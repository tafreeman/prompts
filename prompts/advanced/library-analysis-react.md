---
title: "ReAct: Library Structure & Content Analysis"
category: "advanced-techniques"
tags: ["react", "library-analysis", "audit", "structure", "content-quality", "maintenance"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-25"
difficulty: "advanced"
governance_tags: ["internal-use-only", "safe-for-automated-analysis"]
platform: "Claude Sonnet 4.5, GPT-5.1, Code 5"
---

# ReAct: Library Structure & Content Analysis

## Description

A specialized ReAct (Reasoning + Acting) pattern designed for analyzing the structure, quality, and completeness of a prompt library or code repository. This prompt guides the AI to act as a "Library Analyst," systematically exploring directories, reading files, checking metadata, and identifying gaps or inconsistencies. It combines file system exploration with content evaluation logic.

## Use Cases

- **Library Auditing**: Identifying stub files, missing metadata, or incomplete prompts.
- **Structure Verification**: Ensuring files are in the correct directories (e.g., `analysis` vs `creative`).
- **Content Quality Checks**: Verifying that prompts follow the standard template (Description, Goal, Variables, etc.).
- **Gap Analysis**: Finding missing topics or categories based on existing content.
- **Maintenance**: Generating reports on "to-do" items for library improvement.

## Prompt

```text
You are an expert Library Analyst AI using the ReAct (Reasoning + Acting) pattern to audit and analyze a prompt library.

**Task**: [ANALYSIS_TASK]

**Context**: 
- You have access to the file system of the prompt library.
- The library root is typically `d:\source\osi\prompts` (or similar).
- Prompts are Markdown (`.md`) files.
- Standard prompts should have YAML frontmatter and specific sections (Description, Prompt, Variables, etc.).

**Available Tools**:
1.  **list_directory**: List files and subdirectories in a given path.
    -   Parameters: {path: string}
    -   Returns: List of names, types (file/dir), and sizes.

2.  **read_file**: Read the contents of a specific file.
    -   Parameters: {path: string}
    -   Returns: Full file content.

3.  **search_files**: Search for files containing specific text or matching a pattern.
    -   Parameters: {pattern: string, path: string}
    -   Returns: List of matching files.

4.  **check_metadata**: (Virtual Tool) Analyze the YAML frontmatter of a file content.
    -   Parameters: {content: string}
    -   Returns: Extracted metadata (title, version, tags, etc.) or "MISSING".

**Instructions**:
Use the Thought → Action → Observation → Synthesis cycle to perform the analysis.

For each cycle:

**Thought [N]**:
-   What part of the library do I need to inspect next?
-   Do I need to list a directory to see what's there?
-   Do I need to read a file to check its content?
-   What criteria am I evaluating against (e.g., "is it a stub?")?

**Action [N]**:
Tool: [TOOL_NAME]
Parameters: {
  "param": "value"
}

[SYSTEM PROVIDES RESULTS]

**Observation [N]**:
-   What did the tool return?
-   Are there empty files?
-   Do files have the correct structure?
-   Are there unexpected files?

**Synthesis [N]**:
-   What does this tell me about the library's state?
-   Have I found the answer to the user's question?
-   Do I need to dig deeper into a specific folder?

---

Continue until you can provide:

**Final Report**:
[Comprehensive analysis of the target area]

**Summary of Findings**:
-   **Total Files Scanned**: [Number]
-   **Complete Prompts**: [Number]
-   **Stubs/Incomplete**: [Number] (List them)
-   **Structure Issues**: [Description of any misplaced files]
-   **Metadata Gaps**: [Files missing frontmatter]

**Recommendations**:
-   Specific actions to improve the library (e.g., "Fill out `xyz.md`", "Move `abc.md` to `analysis` folder").

**Confidence Assessment**:
-   **High/Medium/Low**: Based on how much of the requested scope was covered.

```

## Variables

- `[ANALYSIS_TASK]`: The specific auditing or analysis goal (e.g., "Audit the 'analysis' folder for incomplete prompts").

## Example Usage

**Input:**

```text
You are an expert Library Analyst AI using the ReAct (Reasoning + Acting) pattern to audit and analyze a prompt library.

**Task**: Analyze the `prompts/analysis` directory. Identify all prompt files, determine which are "stubs" (under 2KB or missing sections), and list any missing metadata.

**Context**: 
- Root path: `d:\source\osi\prompts`
- Stubs often have just a header or empty sections.

**Available Tools**:
[As described above]

**Instructions**:
[As specified above]
```

**Output:**

```text
**Thought 1**: I need to start by listing the contents of the `prompts/analysis` directory to see what files exist. This will give me the list of candidates to check.

**Action 1**:
Tool: list_directory
Parameters: {
  "path": "d:\\source\\osi\\prompts\\prompts\\analysis"
}

**Observation 1**:
[System returns:]
- competitive-analysis-researcher.md (1.8 KB)
- consumer-behavior-researcher.md (1.8 KB)
- data-analysis-insights.md (24.6 KB)
- data-quality-assessment.md (12.1 KB)
- gap-analysis-expert.md (1.8 KB)
- market-research-analyst.md (1.8 KB)
- user-experience-analyst.md (1.8 KB)
... (total 15 files)

**Synthesis 1**: I see a mix of file sizes. `data-analysis-insights.md` is large (24.6 KB) and likely complete. `data-quality-assessment.md` is also substantial (12.1 KB). However, there are several files around 1.8 KB (e.g., `competitive-analysis-researcher.md`, `gap-analysis-expert.md`). These are likely stubs or templates. I need to read one of the small files and one of the large files to confirm my hypothesis and check for metadata.

---

**Thought 2**: I'll read `competitive-analysis-researcher.md` (small) and `data-analysis-insights.md` (large) to compare their structure and verify if the small ones are indeed stubs.

**Action 2**:
Tool: read_file
Parameters: {
  "path": "d:\\source\\osi\\prompts\\prompts\\analysis\\competitive-analysis-researcher.md"
}

**Observation 2**:
[System returns content of competitive-analysis-researcher.md]
- Frontmatter: Present (title, category, tags...)
- Description: "Conducts competitive market analysis" (Very brief)
- Prompt: Brief placeholder text.
- Variables: Listed but minimal.
- Example Usage: Generic placeholder.

**Action 3**:
Tool: read_file
Parameters: {
  "path": "d:\\source\\osi\\prompts\\prompts\\analysis\\data-analysis-insights.md"
}

**Observation 3**:
[System returns content of data-analysis-insights.md]
- Frontmatter: Present and detailed.
- Description: Detailed paragraph.
- Prompt: Comprehensive, multi-section prompt.
- Variables: Fully documented.
- Example Usage: Real-world example with data.

**Synthesis 2**: My hypothesis is confirmed. The ~1.8KB files are "stubs" - they have the structure but lack deep content (generic descriptions, placeholder examples). The larger files are fully developed. I can now categorize the rest based on size without reading every single one, but to be thorough, I should check if any *missing* metadata exists in the stubs. The read of `competitive-analysis-researcher.md` showed it *had* metadata, just weak content.

---

**Thought 3**: I have enough information to form a conclusion about the state of this folder. Most files appear to be stubs based on the file size pattern observed.

**Final Report**:

### Analysis of `prompts/analysis` Directory

**State Overview**:
The directory contains a mix of fully developed prompts and initial "stub" templates. Approximately 80% of the files are stubs that need significant expansion.

**Detailed Findings**:

1.  **Fully Developed Prompts**:
    -   `data-analysis-insights.md` (Excellent quality, full examples)
    -   `data-quality-assessment.md` (Good quality)

2.  **Identified Stubs (High Priority for Expansion)**:
    -   `competitive-analysis-researcher.md`
    -   `consumer-behavior-researcher.md`
    -   `gap-analysis-expert.md`
    -   `market-research-analyst.md`
    -   `user-experience-analyst.md`
    -   *(and others approx 1.8KB)*

    *Criteria*: These files are < 2KB and contain generic placeholders in "Example Usage" and brief descriptions.

3.  **Metadata Status**:
    -   All checked files *do* contain YAML frontmatter.
    -   Tags are present but generic in stubs.

**Summary of Findings**:
-   **Total Files Scanned**: 15
-   **Complete Prompts**: 2
-   **Stubs/Incomplete**: 13
-   **Structure Issues**: None (all in correct folder)
-   **Metadata Gaps**: None (frontmatter exists)

**Recommendations**:
1.  **Prioritize Expansion**: The `analysis` category is thin. Focus on expanding `competitive-analysis-researcher.md` and `gap-analysis-expert.md` first as these are high-value use cases.
2.  **Use Template**: Use `data-analysis-insights.md` as the "Gold Standard" reference when expanding the stubs.

**Confidence Assessment**: **High** - File size correlation with content quality was verified by sampling.
```

## Tips

- **Size Heuristics**: File size is often a good initial proxy for completeness (e.g., < 2KB is usually a stub).
- **Sampling**: You don't need to read every file if a pattern emerges. Read a representative sample.
- **Structure Checks**: Always verify that "Example Usage" contains *actual* examples, not just "Insert example here" text.
- **Metadata**: Check for `title`, `category`, `tags`, and `version` in the frontmatter.

## Output Schema (JSON)

```json
{
  "target_path": "...",
  "analysis_summary": {
    "total_files": 15,
    "complete": 2,
    "stubs": 13
  },
  "files_analyzed": [
    {
      "filename": "data-analysis-insights.md",
      "status": "complete",
      "size_kb": 24.6,
      "issues": []
    },
    {
      "filename": "gap-analysis-expert.md",
      "status": "stub",
      "size_kb": 1.8,
      "issues": ["Generic example", "Brief description"]
    }
  ],
  "recommendations": ["..."]
}
```

## Related Prompts

- [ReAct: Document Search and Synthesis](react-doc-search-synthesis.md) - General document research.
- [Data Quality Assessment](../analysis/data-quality-assessment.md) - For analyzing data quality (conceptually similar).

## Changelog

### Version 1.0 (2025-11-25)

- Initial release.
- Specialized for library auditing and maintenance.

```
