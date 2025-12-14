---
title: Data Analysis Specialist
shortTitle: Data Analysis
intro: Performs comprehensive data analysis including exploration, statistical analysis,
  and visualization strategy.
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
- data-analysis
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

# Data Analysis Specialist

---

## Description

Performs comprehensive data analysis including data exploration, statistical analysis, trend identification, and visualization strategy. Helps business analysts and data practitioners transform raw data into actionable insights with structured recommendations and clear next steps.

---

## Use Cases

- Analyzing customer churn patterns to inform retention strategies
- Exploratory data analysis (EDA) on new datasets
- Identifying trends and anomalies in business metrics
- Generating data-driven recommendations for stakeholders
- Designing visualization strategies for executive dashboards

---

## Prompt

```text
Analyze data for:

Business Question: [question]
Data Sources: [sources]
Analysis Scope: [scope]
Decision Context: [context]

Provide:
1. Data exploration
2. Statistical analysis
3. Trend identification
4. Insights and findings
5. Recommendations
6. Visualization strategy
```

## Variables

| Variable | Description |
|----------|-------------|
| `[question]` | The business question to answer |
| `[sources]` | Data sources available (systems, tables, files) |
| `[scope]` | Timeframe, segments, constraints, and any exclusions |
| `[context]` | Decision context and stakeholders’ needs |

**Output:**

```text
## Data Analysis Report

### 1. Data Exploration
*   **Dataset:** 500 churned accounts in Q3 vs 430 in Q2.
*   **Segment:** 80% of churn came from "Legacy Plan" users who were forced to upgrade.

### 2. Statistical Analysis
*   **Correlation:** Strong correlation (r=0.85) between "Support Ticket Volume" and "Churn" in the month prior to cancellation.
*   **Price Sensitivity:** Churn rate doubled for customers with usage < 5 hours/week.

### 3. Insights and Findings
*   **Finding:** The price hike triggered a "value re-evaluation" for low-usage customers.
*   **Finding:** Support response time increased by 4 hours in Q3, compounding frustration.

[... continues with recommendations and visualization ...]
```

---

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Example Usage

### Context

A marketing director needs to understand why email campaign performance has declined over the past quarter and identify opportunities for improvement.

### Input

```text
Business Question: Why has email open rate dropped 25% in Q4 compared to Q3?
Data Sources: Email marketing platform (Mailchimp), CRM (Salesforce), Google Analytics
Analysis Scope: 150,000 subscribers across 3 segments (Enterprise, SMB, Individual)
Decision Context: Deciding whether to invest in new email personalization tools
```

### Expected Output

A comprehensive data analysis report including:

1. **Data Exploration** - Subscriber segment breakdown, send time analysis, device usage
2. **Statistical Analysis** - Correlation between subject line length and open rates, A/B test results
3. **Trend Identification** - Week-over-week performance patterns, seasonal factors
4. **Insights and Findings** - Root cause analysis (e.g., inbox filtering changes, content fatigue)
5. **Recommendations** - Prioritized action items with expected impact
6. **Visualization Strategy** - Suggested dashboards and charts for stakeholder presentation

---

## Related Prompts

- [Trend Analysis Specialist](./trend-analysis-specialist.md) - For identifying patterns over time
- [Metrics and KPI Designer](./metrics-and-kpi-designer.md) - For defining success metrics
- [Data Quality Assessment](./data-quality-assessment.md) - For validating data integrity
- [Data Analysis and Insights Generator](./data-analysis-insights.md) - For executive-ready insights
- [Data Quality Assessment](/prompts/analysis/data-quality-assessment) — Validate data quality before analysis
- [Business Case Developer](/prompts/analysis/business-case-developer) — Build ROI cases from your analysis findings
- [Trend Analysis Specialist](/prompts/analysis/trend-analysis-specialist) — Deep-dive into time series trends
