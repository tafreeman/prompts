---

title: "Business Case Developer"
category: "analysis"
tags: ["business-analyst", "business-case", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Business Case Developer

## Description

Develops compelling business cases

## Use Cases

- Business Case for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

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
```

## Variables

- `[benefits]`: Benefits
- `[initiative]`: Initiative
- `[investment]`: Investment
- `[risks]`: Risks
- `[timeline]`: Timeline

## Example Usage

**Input:**

```text
[initiative]: AI-Powered Customer Support Chatbot
[investment]: $250k (Software License + Implementation Services)
[benefits]: Reduce Tier 1 support ticket volume by 30%, Enable 24/7 support availability, Improve CSAT by 5 points
[risks]: Low user adoption, poor answer quality damaging brand reputation
[timeline]: 6 Months (Pilot in Month 3)
```

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
