---
title: Library Structure Treemap Generator
shortTitle: Treemap Generator
intro: Guides generation of a hierarchical Treemap chart to visualize the structure
  and distribution of prompts across categories.
type: how_to
difficulty: intermediate
audience:

- senior-engineer
- solution-architect

platforms:

- claude
- chatgpt
- github-copilot

topics:

- visualization
- analysis

author: GitHub Copilot
version: '1.0'
date: '2025-11-18'
governance_tags:

- PII-safe

dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

<!-- markdownlint-disable MD025 -->
# Library Structure Treemap Generator

---

## Description

This prompt guides the generation of a hierarchical Treemap chart to visualize the structure of the prompt library. It helps in understanding the distribution of prompts across different categories.

## Goal

To create a visual representation that allows users to instantly see the relative sizes of different prompt categories.

## Context

The user has a library of prompts organized into folders (Business, Analysis, Developers, etc.) and wants to visualize this structure.

## Inputs

- `[PROMPT_LIBRARY_STRUCTURE]`: The file structure or list of files in the prompt library.

## Assumptions

- The library is organized hierarchically.
- File counts are a good proxy for "size" or "importance" in this context.

## Constraints

- The output should be a description or code to generate a Treemap.
- Tiles should be sized by count.
- Color-coding should be used for categories.

## Process / Reasoning Style

Direct instruction for visualization generation.

---

## Output Requirements

- A detailed description or code (e.g., Python/Matplotlib, Mermaid, or Vega-Lite) to generate the chart.

---

## Use Cases

- Visualizing the current state of the prompt library.
- Identifying which categories are well-populated and which are sparse.
- Presenting the library structure to stakeholders.

---

## Prompt

```text
Create a hierarchical Treemap chart to visualize my prompt library structure based on the provided [PROMPT_LIBRARY_STRUCTURE].

The top-level hierarchy should be the main folders (Business, Analysis, Developers, Advanced, Creative, Governance, System).
Inside each category, show the individual prompt files as tiles.
Size the tiles equally to represent count, or color-code them by "Category" to show which domains have the most coverage.

I want to instantly see that "Business" and "Analysis" are my largest sections compared to "Creative" or "System".
```text

```

## Variables

| Variable | Description | Example |
|:---------|:------------|:--------|
| `[PROMPT_LIBRARY_STRUCTURE]` | The file structure or list of files in the prompt library | Directory tree or JSON structure of prompts organized by category |

## Example

**Input:**

```text

PROMPT_LIBRARY_STRUCTURE (JSON):
{
  "Business": ["business-case-developer.md", "risk-management-analyst.md"],
  "Analysis": ["trend-analysis-specialist.md", "market-research-analyst.md"],
  "Developers": ["code-review-assistant.md"]
}

```

**Output:**

```text

Provide a working example (e.g., Python with plotly.express.treemap) that:
1) Converts the JSON into a hierarchy of categories -> files
2) Sizes rectangles by count (each file weight=1)
3) Colors by top-level category
4) Includes a title and readable labels

```

## Tips

- **Use consistent sizing**: Ensure tiles are sized proportionally to accurately represent relative category sizes
- **Color code by category**: Use distinct colors for each main category for quick visual identification
- **Interactive elements**: Consider making the treemap interactive so users can drill down into individual prompts
