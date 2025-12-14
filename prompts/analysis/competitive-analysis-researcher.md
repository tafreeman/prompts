---
title: Competitive Analysis Researcher
shortTitle: Competitive Analysis
intro: Conducts comprehensive competitive market analysis including landscape mapping,
  feature comparison, and strategic recommendations.
type: how_to
difficulty: intermediate
audience:
- business-analyst
- senior-engineer
platforms:
- claude
- chatgpt
- github-copilot
topics:
- analysis
- business
author: Prompts Library Team
version: '1.0'
date: '2025-11-16'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# Competitive Analysis Researcher

---

## Description

Conducts competitive market analysis

---

## Use Cases

- Market Analysis for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

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
```text

## Variables

| Variable | Description |
|----------|-------------|
| `[product]` | The product/service you’re analyzing competitors for |
| `[segment]` | The market segment (who/where/for what job) |
| `[competitors]` | Known competitors to include (names, URLs if available) |
| `[focus]` | What to emphasize (features, pricing, positioning, GTM, etc.) |

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

A product strategy lead at a project management SaaS company needs to understand the competitive landscape to inform the 2025 product roadmap.

### Input

```text
Product/Service: Project management software for creative agencies
Market Segment: SMB creative agencies (10-100 employees)
Key Competitors: Asana, Monday.com, ClickUp, Notion
Analysis Focus: Feature gaps, pricing strategy, positioning opportunities
```

### Expected Output

A comprehensive competitive analysis report including:

1. **Competitive Landscape** - Market positioning map, segment leaders, emerging challengers
2. **Feature Comparison** - Side-by-side matrix of key features with gap analysis
3. **Pricing Analysis** - Pricing tiers, per-seat costs, enterprise discounting patterns
4. **Market Positioning** - Messaging analysis, target audience, value propositions
5. **Opportunities and Threats** - White space opportunities, competitive moats, disruption risks
6. **Strategic Recommendations** - Feature prioritization, pricing strategy, differentiation plays

---

## Related Prompts

- [Competitive Analysis Framework](../business/competitive-analysis.md) - For comprehensive competitive intelligence
- [Business Strategy Analysis](../business/business-strategy-analysis.md) - For strategic planning based on competitive insights
- [Market Research Analyst](./market-research-analyst.md) - For broader market research
- [Industry Analysis Expert](./industry-analysis-expert.md) - For industry-level analysis
