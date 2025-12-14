---
title: Industry Analysis Expert
shortTitle: Industry Analysis
intro: Performs detailed industry analysis including market dynamics, competitive
  landscape, and strategic recommendations.
type: how_to
difficulty: intermediate
audience:
- business-analyst
- solution-architect
platforms:
- claude
- chatgpt
- github-copilot
topics:
- research
- analysis
author: Prompts Library Team
version: '1.0'
date: '2025-11-16'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# Industry Analysis Expert

---

## Description

Performs detailed industry analysis

---

## Use Cases

- Industry Analysis for Researcher persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Analyze industry:

Industry: [industry]
Analysis Scope: [scope]
Key Questions: [questions]
Stakeholder Interest: [stakeholders]

Include:
1. Industry overview
2. Market dynamics
3. Competitive landscape
4. Trends and drivers
5. Future outlook
6. Strategic recommendations
```text

## Variables

| Variable | Description |
|----------|-------------|
| `[industry]` | The industry/sector to analyze |
| `[scope]` | Geographic, segment, and time horizon scope |
| `[questions]` | Key questions to answer (bullets are fine) |
| `[stakeholders]` | Who the analysis is for and what decisions they’ll make |

**Output:**

```text
## Industry Analysis Report

### 1. Industry Overview
*   **Size:** $3B market in 2024, projected to reach $15B by 2030 (CAGR 25%).
*   **Structure:** Fragmented market consolidating around 3-4 major networks (Tesla, Electrify America, ChargePoint).

### 2. Market Dynamics
*   **Driver:** Federal NEVI funding ($5B) accelerating highway corridor buildout.
*   **Constraint:** Grid capacity bottlenecks delaying site energization by 12-18 months.

### 3. Future Outlook
*   **Standardization:** NACS (Tesla) adoption by Ford/GM signals the end of the "Connector War."
*   **Prediction:** 40% of smaller CPOs (Charge Point Operators) will be acquired by 2026.

[... continues with strategic recommendations ...]
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

A venture capital analyst needs to evaluate the electric vehicle charging infrastructure industry to inform investment decisions in the space.

### Input

```text
Industry: Electric Vehicle Charging Infrastructure
Analysis Scope: North America, focus on DC fast charging networks
Key Questions: Market size, growth drivers, competitive moats, consolidation trends
Stakeholder Interest: Investment committee evaluating Series B opportunities
```

### Expected Output

A comprehensive industry analysis report including:

1. **Industry Overview** - Market size ($3B in 2024), growth trajectory (25% CAGR), key segments
2. **Market Dynamics** - Demand drivers (EV adoption, policy mandates), supply constraints (grid capacity, permitting)
3. **Competitive Landscape** - Major players (Tesla, ChargePoint, EVgo), market share, differentiation strategies
4. **Trends and Drivers** - Technology evolution (charging speeds), standardization (NACS), business model shifts
5. **Future Outlook** - 5-year market projections, consolidation predictions, regulatory trajectory
6. **Strategic Recommendations** - Investment criteria, attractive niches, risk factors to monitor

---

## Related Prompts

- [Trend Analysis Specialist](./trend-analysis-specialist.md) - For emerging industry trends
- [Competitive Analysis Researcher](./competitive-analysis-researcher.md) - For competitor deep-dives
- [Market Research Analyst](./market-research-analyst.md) - For market research methodology
- [Business Case Developer](./business-case-developer.md) - For investment analysis
