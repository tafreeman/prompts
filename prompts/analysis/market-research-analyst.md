---
title: "Market Research Analyst"
shortTitle: "Market Research"
intro: "Conducts comprehensive market research with research design, data collection plans, and strategic implications."
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
---
# Market Research Analyst

---

## Description

Conducts comprehensive market research

---

## Use Cases

- Market Research for Researcher persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

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
```text

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

A startup founder is preparing to enter the meal kit delivery market and needs comprehensive market research to inform product positioning and go-to-market strategy.

### Input

```text
Research Topic: Premium organic meal kit subscription market
Target Market: Urban professionals aged 28-45 with household income >$100K
Research Objectives: Market size, customer segments, unmet needs, competitive gaps
Methodology Preference: Mixed methods (surveys + focus groups + secondary research)
Timeline: 6 weeks
```

### Expected Output

A comprehensive market research plan and findings:

1. **Research Design** - Phased approach with qualitative and quantitative methods
2. **Data Collection Plan** - Sampling strategy, recruitment channels, incentive structure
3. **Analysis Framework** - Segmentation criteria, conjoint analysis for feature prioritization
4. **Key Findings** - Market size ($2.5B), growth rate (18% CAGR), key segments
5. **Market Insights** - Unmet needs (flexibility, dietary restrictions, sustainability)
6. **Strategic Implications** - Positioning opportunities, pricing strategy, channel recommendations

---

## Related Prompts

- [Competitive Analysis Researcher](./competitive-analysis-researcher.md) - For competitor deep-dives
- [Consumer Behavior Researcher](./consumer-behavior-researcher.md) - For customer psychology insights
- [Industry Analysis Expert](./industry-analysis-expert.md) - For broader industry trends
- [Trend Analysis Specialist](./trend-analysis-specialist.md) - For emerging market trends
