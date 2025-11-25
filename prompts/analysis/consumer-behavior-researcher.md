---

title: "Consumer Behavior Researcher"
category: "analysis"
tags: ["researcher", "consumer-research", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Consumer Behavior Researcher

## Description

Studies consumer behavior patterns

## Use Cases

- Consumer Research for Researcher persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Research consumer behavior for:

Product/Service: [product]
Target Demographics: [demographics]
Behavior Focus: [behavior]
Research Methods: [methods]

Provide:
1. Research methodology
2. Data collection approach
3. Behavioral analysis
4. Consumer insights
5. Implications for business
6. Recommendations
```

## Variables

- `[behavior]`: Behavior
- `[demographics]`: Demographics
- `[methods]`: Methods
- `[product]`: Product

## Example Usage

**Input:**

```text
[product]: Plant-based Meat Alternatives
[demographics]: Millennials and Gen Z, Urban, Income > $75k
[behavior]: "Flexitarian" diet adoption (reducing meat consumption without going full vegan)
[methods]: Social Listening (Reddit/TikTok), Online Surveys (N=1000)
```

**Output:**

```text
## Consumer Behavior Research Plan

### 1. Research Methodology
*   **Social Listening:** Analyze sentiment on r/PlantBasedDiet and TikTok #VeganRecipes to identify taste preferences.
*   **Survey:** Quantitative validation of "Price vs Taste" trade-offs.

### 2. Behavioral Analysis
*   **Driver:** Health consciousness is the #1 driver, followed by Climate Change.
*   **Barrier:** "Ultra-processed" perception is a growing concern among target demographic.

### 3. Consumer Insights
*   **Insight:** Consumers want "Clean Label" (pea protein) over "Hyper-realistic" (heme/soy) if it means fewer additives.

[... continues with implications and recommendations ...]
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
