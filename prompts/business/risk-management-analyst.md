---

title: "Risk Management Analyst"
category: "business"
tags: ["project-manager", "risk-management", "enterprise"]
author: "Prompts Library Team"
version: "1.1"
date: "2025-11-18"
difficulty: "intermediate"
governance_tags: ["risk-assessment", "audit-trail"]
data_classification: "internal"
risk_level: "medium"
regulatory_scope: ["compliance"]
approval_required: false
retention_period: "3-years"
platform: "Claude Sonnet 4.5"
---

# Risk Management Analyst

## Description

Identifies and manages project risks

## Use Cases

- Risk Management for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Analyze risks for:

Project: [project_name]
Project Phase: [phase]
Key Concerns: [concerns]
Stakeholder Impact: [impact]

Provide:
1. Risk identification matrix
2. Probability and impact assessment
3. Risk mitigation strategies
4. Contingency plans
5. Monitoring procedures
6. Escalation protocols
```

## Variables

- `[concerns]`: Concerns
- `[impact]`: Impact
- `[phase]`: Phase
- `[project_name]`: Project Name

## Example Usage

**Input:**

```text
[project_name]: New Data Center Build (DC-04)
[phase]: Construction / Fit-out
[concerns]: Supply chain delays for cooling units, potential labor strikes in region, power grid connection permit delays
[impact]: Critical path delay costs $500k/month in penalties; potential loss of anchor tenant
```

**Output:**

```text
## Risk Management Plan

### 1. Risk Identification Matrix
*   **Risk ID R-01:** Cooling Unit Delivery Delay.
*   **Risk ID R-02:** Local Union Labor Strike.
*   **Risk ID R-03:** Utility Grid Connection Permit Rejection.

### 2. Probability and Impact Assessment
*   **R-01:** High Probability (80%), High Impact (3-month delay). **Score: Critical.**
*   **R-02:** Medium Probability (40%), Medium Impact (2-week delay). **Score: Major.**

### 3. Risk Mitigation Strategies
*   **R-01 (Avoid):** Pre-order units from secondary supplier (paying 10% premium) to secure stock.
*   **R-03 (Mitigate):** Hire specialized local expeditor to manage permit application process.

[... continues with contingency plans and monitoring ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Project Manager prompts in this category
- Check the business folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
