---
name: Library Structure Treemap Generator
description: Guides generation of a hierarchical Treemap chart to visualize the structure and distribution of prompts across categories.
type: how_to
---

<!-- markdownlint-disable MD025 -->
# Library Structure Treemap Generator

## Description

Produces hierarchical treemap charts visualizing prompt library structure and distribution across categories. Enables quick identification of largest sections and category coverage imbalances through proportional tile sizing.

## Output Requirements

- A detailed description or code (e.g., Python/Matplotlib, Mermaid, or Vega-Lite) to generate the chart.

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
