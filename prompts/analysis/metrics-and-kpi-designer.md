---
title: Metrics and KPI Designer
shortTitle: Metrics & KPI Design
intro: Designs business metrics and KPIs with calculation methods, data sources, and
  reporting strategies.
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

- metrics
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

# Metrics and KPI Designer

---

## Description

Designs business metrics and KPIs

---

## Use Cases

- Metrics for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

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

```text

## Variables

| Variable | Description |
| ---------- | ------------- |
| `[objective]` | The business objective the metrics should support |
| `[stakeholders]` | Who will consume the metrics and make decisions |
| `[data]` | Available data sources/fields and data quality constraints |
| `[frequency]` | Reporting cadence (daily/weekly/monthly/quarterly) |

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

A VP of Customer Success needs to design a comprehensive metrics framework to measure and improve customer health, reduce churn, and identify expansion opportunities.

### Input

```text
Business Objective: Reduce customer churn from 15% to 8% annually, increase NRR to 110%
Stakeholders: Customer Success Managers, Account Executives, Product Team, Executive Leadership
Data Availability: CRM (Salesforce), Product Analytics (Mixpanel), Support (Zendesk), NPS surveys
Reporting Frequency: Weekly team dashboards, monthly executive reviews, quarterly board updates
```

### Expected Output

A comprehensive metrics and KPI design including:

1. **KPI Framework** - Health Score model with weighted components (adoption, engagement, support, growth)
2. **Metric Definitions** - DAU/MAU ratio, feature adoption rate, support ticket velocity, expansion revenue
3. **Data Sources** - Integration points, data freshness requirements, ownership
4. **Calculation Methods** - Formulas with examples, handling edge cases (new customers, seasonal businesses)
5. **Reporting Strategy** - Dashboard wireframes, drill-down hierarchy, audience-specific views
6. **Action Triggers** - Health score thresholds for intervention (red <60, yellow 60-80, green >80)

---

## Related Prompts

- [Data Analysis Specialist](./data-analysis-specialist.md) - For analyzing metrics data
- [Trend Analysis Specialist](./trend-analysis-specialist.md) - For identifying metric trends
- [Business Case Developer](./business-case-developer.md) - For ROI of metrics initiatives
- [Gap Analysis Expert](./gap-analysis-expert.md) - For metrics capability gaps
