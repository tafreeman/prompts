---
name: Library Capability Radar Chart Generator
description: Guides generation of a Radar Chart to assess the maturity and balance of the prompt library across key domains.
type: how_to
---

<!-- markdownlint-disable MD025 -->
# Library Capability Radar Chart Generator

## Description

Generates radar chart visualizations to assess prompt library maturity and balance across key domains. Identifies coverage gaps and strengths by plotting category counts on a spider plot for strategic library expansion planning.

## Output Requirements

- A detailed description or code (e.g., Python/Matplotlib, Excel instructions) to generate the chart.

## Prompt

```text
Design a Radar Chart (Spider Plot) to score the maturity of my prompt library across its 7 key domains: Advanced, Analysis, Business, Creative, Developers, Governance, and System.

Use the provided [CATEGORY_COUNTS] for the axes.
The axis for each domain should represent the number of prompts available (e.g., Business might score 25, while Creative scores 2).

This visualization should highlight gaps in the library—for example, showing a strong spike in "Business" analysis but a potential deficiency in "Creative" or "Governance" tools.
```text

```

## Variables

| Variable | Description | Example |
|:---------|:------------|:--------|
| `[CATEGORY_COUNTS]` | Number of prompts in each of the 7 key domains | Advanced: 8, Analysis: 18, Business: 25, Creative: 3, Developers: 15, Governance: 4, System: 6 |

## Example

**Input:**

```text

CATEGORY_COUNTS:

- Advanced: 12
- Analysis: 24
- Business: 30
- Creative: 6
- Developers: 18
- Governance: 5
- System: 9

```

**Output:**

```text

Provide Python/Matplotlib code that:
1) Creates 7 radar axes labeled: Advanced, Analysis, Business, Creative, Developers, Governance, System
2) Plots the provided values as a closed polygon
3) Sets the radial limit to at least max(value) (e.g., 0..30)
4) Adds a title "Prompt Library Coverage Radar" and a light grid

```

## Tips

- **Use appropriate scale**: Ensure the radar chart scale accommodates the highest category count
- **Visualize gaps**: Look for categories with significantly lower counts to prioritize expansion
- **Track over time**: Generate periodic radar charts to monitor library growth and balance
