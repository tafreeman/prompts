---
title: "Trend Analysis Specialist"
shortTitle: "Trend Analysis"
intro: "Identifies and analyzes market trends including impact assessment, future projections, and strategic responses."
type: "how_to"
difficulty: "intermediate"
audience:
  - "business-analyst"
  - "solution-architect"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "research"
  - "analysis"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 3.2
---
# Trend Analysis Specialist

---

## Description

Identifies and analyzes market trends

---

## Use Cases

- Trend Analysis for Researcher persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

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
```text

## Variables

| Variable | Description |
|----------|-------------|
| `[market]` | Industry/market to analyze |
| `[categories]` | Trend categories to consider (tech, consumer behavior, regulation, etc.) |
| `[horizon]` | Time horizon for projections |
| `[impact]` | How to frame business impact (roadmap, investment, risk, GTM, etc.) |

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
```text

---


## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Example Usage

### Context

A CPO at an e-commerce company needs to understand emerging trends in consumer shopping behavior to inform the product roadmap for the next 18 months.

### Input

```text
Industry/Market: E-commerce / Direct-to-Consumer retail
Trend Categories: Technology, Consumer Behavior, Payment Methods, Sustainability
Time Horizon: 18-24 months
Business Impact: Product roadmap prioritization and competitive positioning
```

### Expected Output

A comprehensive trend analysis report including:

1. **Trend Identification** - 5-7 major trends with supporting data (social commerce growth, AI personalization, BNPL adoption)
2. **Trend Analysis** - Maturity assessment (emerging, growing, mature) for each trend
3. **Impact Assessment** - Quantified impact on revenue, operations, and customer experience
4. **Future Projections** - 18-month forecast with adoption curves and market penetration estimates
5. **Business Implications** - How each trend affects current business model and operations
6. **Strategic Responses** - Prioritized initiatives with resource requirements and timeline

---

## Related Prompts

- [Market Research Analyst](./market-research-analyst.md) - For comprehensive market research
- [Industry Analysis Expert](./industry-analysis-expert.md) - For industry-specific analysis
- [Consumer Behavior Researcher](./consumer-behavior-researcher.md) - For customer behavior insights
- [Competitive Analysis Researcher](./competitive-analysis-researcher.md) - For competitive landscape
