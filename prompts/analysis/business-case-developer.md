---
title: Business Case Developer
shortTitle: Business Case
intro: Develops compelling business cases with executive summaries, cost-benefit analysis,
  ROI calculations, and implementation plans.
type: how_to
difficulty: intermediate
audience:
- business-analyst
- project-manager
platforms:
- claude
- chatgpt
- github-copilot
topics:
- business
- planning
author: Prompts Library Team
version: '1.0'
date: '2025-11-16'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# Business Case Developer

---

## Description

Develops compelling business cases

---

## Use Cases

- Business Case for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Develop business case for:

Initiative: [initiative]
Investment Required: [investment]
Expected Benefits: [benefits]
Risks: [risks]
Timeline: [timeline]

Provide:
1. Executive summary
2. Cost-benefit analysis
3. ROI calculations
4. Risk assessment
5. Implementation plan
6. Success metrics
```text

## Variables

| Variable | Description |
|----------|-------------|
| `[initiative]` | Name/summary of the initiative being proposed |
| `[investment]` | Budget, resources, and/or cost required |
| `[benefits]` | Expected outcomes (revenue, savings, risk reduction, etc.) |
| `[risks]` | Key risks and uncertainties to address |
| `[timeline]` | Target schedule (phases, milestones, or timeframe) |

**Output:**

```text
## Business Case

### 1. Executive Summary
Implementing an AI Chatbot will automate 30% of routine queries, saving $400k/year in support costs and providing 24/7 service. Payback period is 9 months.

### 2. Cost-Benefit Analysis
*   **Costs:** $250k Year 1 (One-time setup + License).
*   **Savings:** $400k/year (Equivalent to 6 FTEs).
*   **Net Benefit (Year 1):** $150k.

### 3. Risk Assessment
*   **Risk:** "Hallucinations" providing wrong answers.
*   **Mitigation:** Implement "Human in the Loop" handoff for low-confidence answers (<80%).

[... continues with implementation plan and success metrics ...]
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

A product manager at a SaaS company needs to build a business case for investing in a new mobile app feature to improve user engagement and reduce churn.

### Input

```text
Initiative: In-app push notifications for personalized content recommendations
Investment Required: $150,000 (development) + $30,000/year (infrastructure)
Expected Benefits: 15% reduction in churn, 20% increase in daily active users
Risks: User notification fatigue, privacy concerns, technical integration complexity
Timeline: 6 months development, 3 months pilot
```

### Expected Output

A complete business case document with:

1. **Executive Summary** - Concise overview of the investment opportunity with key financial metrics
2. **Cost-Benefit Analysis** - Detailed breakdown of costs vs. projected savings/revenue
3. **ROI Calculations** - NPV, payback period, and IRR analysis
4. **Risk Assessment** - Risk matrix with mitigation strategies for each identified risk
5. **Implementation Plan** - Phased rollout with milestones and resource requirements
6. **Success Metrics** - KPIs for measuring feature success (DAU, retention rate, NPS)

---

## Related Prompts

- [Gap Analysis Expert](./gap-analysis-expert.md) - For current/desired state comparison
- [Requirements Analysis Expert](./requirements-analysis-expert.md) - For gathering detailed requirements
- [Business Strategy Analysis](../business/business-strategy-analysis.md) - For strategic alignment
- [Risk Management Analyst](../business/risk-management-analyst.md) - For deeper risk assessment
