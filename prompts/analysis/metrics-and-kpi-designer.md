---

title: "Metrics and KPI Designer"
category: "analysis"
tags: ["business-analyst", "metrics", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Metrics and KPI Designer

## Description

Designs business metrics and KPIs

## Use Cases

- Metrics for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Design metrics for:

Business Objective: [objective]
Stakeholders: [stakeholders]
Data Availability: [data]
Reporting Frequency: [frequency]

Include:
1. KPI framework
2. Metric definitions
3. Data sources
4. Calculation methods
5. Reporting strategy
6. Action triggers
```

## Variables

- `[data]`: Data
- `[frequency]`: Frequency
- `[objective]`: Objective
- `[stakeholders]`: Stakeholders

## Example Usage

**Input:**

```text
[objective]: Improve Software Engineering Productivity & Developer Experience (DevEx)
[stakeholders]: CTO, VP Engineering, Team Leads
[data]: Jira (Task tracking), GitHub (Code activity), CI/CD Logs (Build times), Officevibe (Surveys)
[frequency]: Bi-weekly Sprint Reports + Quarterly Executive Review
```

**Output:**

```text
## Metrics and KPI Design

### 1. KPI Framework (DORA Metrics + SPACE)
*   **Velocity is NOT a KPI:** Explicitly avoiding "Lines of Code" or "Story Points" as performance targets to prevent gaming.
*   **Focus:** Flow efficiency and stability.

### 2. Metric Definitions
*   **Deployment Frequency:** How often code is deployed to production (Target: Daily).
*   **Lead Time for Changes:** Time from commit to production (Target: < 24 hours).
*   **Change Failure Rate:** % of deployments causing outages (Target: < 5%).

### 3. Action Triggers
*   **Red Flag:** If "Lead Time" > 3 days, trigger a "Pipeline Bottleneck" review.

[... continues with reporting strategy and calculation methods ...]
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
