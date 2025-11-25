---

title: "Market Research Analyst"
category: "analysis"
tags: ["researcher", "market-research", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Market Research Analyst

## Description

Conducts comprehensive market research

## Use Cases

- Market Research for Researcher persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Conduct market research for:

Research Topic: [topic]
Target Market: [market]
Research Objectives: [objectives]
Methodology Preference: [methodology]
Timeline: [timeline]

Provide:
1. Research design
2. Data collection plan
3. Analysis framework
4. Key findings
5. Market insights
6. Strategic implications
```

## Variables

- `[market]`: Market
- `[methodology]`: Methodology
- `[objectives]`: Objectives
- `[timeline]`: Timeline
- `[topic]`: Topic

## Example Usage

**Input:**

```text
[topic]: Smart Home Security Adoption
[market]: US Homeowners aged 30-50, Household Income > $100k
[objectives]: Understand barriers to entry (Privacy concerns vs Cost) and feature preferences
[methodology]: Mixed Methods (Online Survey N=1500 + 20 In-home Ethnographic Interviews)
[timeline]: 8 Weeks
```

**Output:**

```text
## Market Research Plan

### 1. Research Design
*   **Phase 1 (Qual):** In-home interviews to observe current security setups and frustrations.
*   **Phase 2 (Quant):** MaxDiff survey to rank feature importance (e.g., "Face Recognition" vs "Local Storage").

### 2. Data Collection Plan
*   **Recruitment:** Use panel provider (e.g., UserInterviews.com) targeting suburban homeowners.
*   **Incentive:** $100 Amazon Gift Card for 60-min interview.

### 3. Analysis Framework
*   **Segmentation:** Cluster analysis to identify "Privacy Purists" vs "Tech Enthusiasts."

[... continues with key findings and strategic implications ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Researcher prompts in this category
- Check the analysis folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
