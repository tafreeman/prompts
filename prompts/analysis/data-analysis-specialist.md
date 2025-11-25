---

title: "Data Analysis Specialist"
category: "analysis"
tags: ["business-analyst", "data-analysis", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Data Analysis Specialist

## Description

Performs comprehensive data analysis

## Use Cases

- Data Analysis for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

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

- `[context]`: Context
- `[question]`: Question
- `[scope]`: Scope
- `[sources]`: Sources

## Example Usage

**Input:**

```text
[question]: Why did customer churn increase by 15% in Q3?
[sources]: CRM (Salesforce), Support Tickets (Zendesk), Usage Logs (Mixpanel)
[scope]: US Market, Enterprise Segment
[context]: We implemented a 10% price increase on July 1st
```

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
