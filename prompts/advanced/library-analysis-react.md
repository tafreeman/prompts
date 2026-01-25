---
name: Library Analysis React
description: ---
type: how_to
---
## Description

## Prompt

```text

**Output:**

```

---

## Description

## Prompt

```text

**Output:**

```

---


# ReAct: Library Structure & Content Analysis

## Use Cases

- **Library Auditing**: Identifying stub files, missing metadata, or incomplete prompts.
- **Structure Verification**: Ensuring files are in the correct directories (e.g., `analysis` vs `creative`).
- **Content Quality Checks**: Verifying that prompts follow the standard template (Description, Goal, Variables, etc.).
- **Gap Analysis**: Finding missing topics or categories based on existing content.
- **Maintenance**: Generating reports on "to-do" items for library improvement.

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

```text

**Output:**

```text
**Thought 1**: I need to start by listing the contents of the `prompts/analysis` directory to see what files exist. This will give me the list of candidates to check.

**Action 1**:
Tool: list_directory
Parameters: {
  "path": "[repository_root]/prompts/analysis"
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
```text

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
```text

---


## Related Prompts

- [ReAct: Document Search and Synthesis](react-doc-search-synthesis.md) - General document research.
- [Data Quality Assessment](../analysis/data-quality-assessment.md) - For analyzing data quality (conceptually similar).## Variables

_No bracketed variables detected._

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `["..."]` | AUTO-GENERATED: describe `"..."` |
| `["Generic example", "Brief description"]` | AUTO-GENERATED: describe `"Generic example", "Brief description"` |
| `[Comprehensive analysis of the target area]` | AUTO-GENERATED: describe `Comprehensive analysis of the target area` |
| `[Data Quality Assessment]` | AUTO-GENERATED: describe `Data Quality Assessment` |
| `[Description of any misplaced files]` | AUTO-GENERATED: describe `Description of any misplaced files` |
| `[Files missing frontmatter]` | AUTO-GENERATED: describe `Files missing frontmatter` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Number]` | AUTO-GENERATED: describe `Number` |
| `[ReAct: Document Search and Synthesis]` | AUTO-GENERATED: describe `ReAct: Document Search and Synthesis` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[System returns:]` | AUTO-GENERATED: describe `System returns:` |
| `[repository_root]` | AUTO-GENERATED: describe `repository_root` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

