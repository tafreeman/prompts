---

title: "Strategic Planning Consultant"
category: "business"
tags: ["consultant", "strategy", "enterprise"]
author: "Prompts Library Team"
version: "1.1"
date: "2025-11-18"
difficulty: "advanced"
governance_tags: ["strategic-decision", "requires-executive-review"]
data_classification: "confidential"
risk_level: "high"
regulatory_scope: ["internal-governance"]
approval_required: true
retention_period: "5-years"
platform: "Claude Sonnet 4.5"
---

# Strategic Planning Consultant

## Description

Develops strategic plans and roadmaps

## Use Cases

- Strategy for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Develop strategic plan for:

Organization: [organization]
Industry: [industry]
Current Challenges: [challenges]
Growth Objectives: [objectives]
Timeframe: [timeframe]

Provide:
1. Situation analysis
2. Strategic options
3. Recommended strategy
4. Implementation roadmap
5. Success metrics
6. Risk mitigation
```

## Variables

- `[challenges]`: Challenges
- `[industry]`: Industry
- `[objectives]`: Objectives
- `[organization]`: Organization
- `[timeframe]`: Timeframe

## Example Usage

**Input:**

```text
[organization]: "ShopMart" (Mid-sized Retail Chain, 50 stores)
[industry]: Retail / E-commerce
[challenges]: Declining foot traffic (-10% YoY), fierce competition from Amazon, aging loyalty program
[objectives]: Double online revenue share (to 30%), launch mobile loyalty app, close 5 underperforming stores
[timeframe]: 3 Years (2025-2028)
```

**Output:**

```text
## Strategic Plan (2025-2028)

### 1. Situation Analysis (SWOT)
*   **Strengths:** Strong local brand presence, experienced store staff.
*   **Weaknesses:** Legacy IT systems, no mobile app.
*   **Opportunities:** "Buy Online, Pick Up In-Store" (BOPIS), hyper-local marketing.
*   **Threats:** Big-box price wars, supply chain inflation.

### 2. Strategic Options
*   **Option A (Defensive):** Cut costs, close 10 stores, focus on profitability.
*   **Option B (Pivot):** Aggressive digital transformation, omnichannel focus. (Recommended)

### 3. Recommended Strategy: "Omnichannel Neighborhood Hub"
*   Transform stores into fulfillment centers for online orders.
*   Launch "ShopMart Rewards" app to drive foot traffic via personalized offers.

[... continues with implementation roadmap and success metrics ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Consultant prompts in this category
- Check the business folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
