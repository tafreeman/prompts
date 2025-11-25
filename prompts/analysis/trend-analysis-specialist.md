---

title: "Trend Analysis Specialist"
category: "analysis"
tags: ["researcher", "trend-analysis", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Trend Analysis Specialist

## Description

Identifies and analyzes market trends

## Use Cases

- Trend Analysis for Researcher persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Analyze trends for:

Industry/Market: [market]
Trend Categories: [categories]
Time Horizon: [horizon]
Business Impact: [impact]

Include:
1. Trend identification
2. Trend analysis
3. Impact assessment
4. Future projections
5. Business implications
6. Strategic responses
```

## Variables

- `[categories]`: Categories
- `[horizon]`: Horizon
- `[impact]`: Impact
- `[market]`: Market

## Example Usage

**Input:**

```text
[market]: Digital Marketing
[categories]: AI Content Generation, Privacy/Cookie Deprecation
[horizon]: 12-24 Months
[impact]: High (Disruption of organic search traffic and ad targeting)
```

**Output:**

```text
## Trend Analysis Report

### 1. Trend Identification
*   **Trend:** "Zero-Click Search" (SGE). Users getting answers directly in search results without clicking links.
*   **Trend:** First-party data reliance due to 3rd party cookie death.

### 2. Impact Assessment
*   **SEO Traffic:** Predicted 20-30% drop in top-of-funnel blog traffic.
*   **Ad Efficiency:** CAC (Customer Acquisition Cost) likely to rise by 15% as targeting gets broader.

### 3. Strategic Responses
*   **Pivot:** Shift content strategy from "SEO Keywords" to "Thought Leadership" (Video/Podcasts) that AI can't easily replicate.
*   **Invest:** Build owned communities (Newsletters) to reduce platform dependency.

[... continues with future projections and business implications ...]
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
