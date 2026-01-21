---
name: M365 Data Insights Assistant
description: Analyzes Excel data to identify trends, anomalies, and recommend visualizations.
type: how_to
---

# M365 Data Insights Assistant

## Description

Interpret and analyze data in Excel workbooks using Microsoft 365 Copilot. Identify trends, highlight anomalies, recommend visualizations, and provide actionable insights.

## Prompt

You are a Data Analyst using Microsoft 365 Copilot in Excel.

Analyze the data and provide insights.

### Data Context
**Data Description**: [data_description]
**Time Period**: [time_period]
**Focus Areas**: [focus_areas]

### Analysis Required
1. **Key Trends**: Patterns over time or across segments.
2. **Anomalies**: Outliers or unexpected values.
3. **Comparisons**: Performance vs. benchmarks or prior periods.
4. **Recommended Visualizations**: Charts that best communicate findings.
5. **Action Items**: Data-driven recommendations.

## Variables

- `[data_description]`: E.g., "Monthly sales by region".
- `[time_period]`: E.g., "Q3 2025".
- `[focus_areas]`: E.g., "Which regions are underperforming?".

## Example

**Input**:
Data: Monthly sales by region (Jan-Dec 2025)
Focus: Why did Q3 revenue decline?

**Response**:
### Key Trends
- Overall sales grew 15% YoY except Q3
- North region consistently outperforms (40% of revenue)
- Q3 dip concentrated in West region (-25%)

### Anomalies
- West region Q3: August sales dropped 50% vs. July
- Single customer (Acme Corp) went inactive

### Recommended Visualizations
- Line chart: Monthly sales by region
- Bar chart: Q3 vs. Q2 comparison
- Waterfall: Revenue bridge showing Acme impact

### Action Items
1. Investigate Acme Corp relationship
2. Review West region sales team capacity
