---

title: "Competitive Analysis Researcher"
category: "analysis"
tags: ["business-analyst", "market-analysis", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Competitive Analysis Researcher

## Description

Conducts competitive market analysis

## Use Cases

- Market Analysis for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Analyze competition for:

Product/Service: [product]
Market Segment: [segment]
Key Competitors: [competitors]
Analysis Focus: [focus]

Include:
1. Competitive landscape
2. Feature comparison
3. Pricing analysis
4. Market positioning
5. Opportunities and threats
6. Strategic recommendations
```

## Variables

- `[competitors]`: Competitors
- `[focus]`: Focus
- `[product]`: Product
- `[segment]`: Segment

## Example Usage

**Input:**

```text
[product]: Enterprise Project Management Tool ("TaskMaster")
[segment]: Mid-market Creative Agencies (50-200 employees)
[competitors]: Asana, Monday.com, ClickUp
[focus]: Pricing Strategy and Feature Gaps in "Creative Proofing"
```

**Output:**

```text
## Competitive Analysis Report

### 1. Competitive Landscape
*   **Asana:** Market Leader. Strong on usability, weak on reporting. Expensive ($30/user).
*   **Monday.com:** Strong marketing. Highly customizable but complex setup.
*   **ClickUp:** "All-in-one" value play. Feature rich but buggy.

### 2. Feature Comparison (Creative Proofing)
*   **TaskMaster (Us):** Basic file attachment only. 🔴 Gap.
*   **Competitors:** All three offer visual annotation on images/videos. Asana's is best-in-class.

### 3. Strategic Recommendations
*   **Product:** Prioritize "Visual Proofing" integration (e.g., with Figma) to close the gap.
*   **Pricing:** Undercut Asana by 20% to capture price-sensitive agencies.

[... continues with market positioning and opportunities ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Business Analyst prompts in this category
- Check the analysis folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
