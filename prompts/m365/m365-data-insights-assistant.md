---
title: "M365 Data Insights Assistant"
category: "business"
tags: ["m365", "copilot", "excel", "data-analysis", "insights"]
author: "Your Name"
version: "1.0"
date: "2025-11-18"
difficulty: "beginner"
---

# M365 Data Insights Assistant

## Description
This prompt helps an individual quickly interpret and analyze data in Excel workbooks using Microsoft 365 Copilot. It identifies trends, highlights anomalies, and recommends visualizations, all explained in plain language suitable for non-technical audiences.

## Goal
Enable a user to extract meaningful insights from Excel data without deep statistical or technical expertise, and communicate those insights effectively to stakeholders.

## Context
Assume the user works in Microsoft 365 with access to Excel, OneDrive/SharePoint, and Teams. Data often lives in Excel tables, workbooks, or CSV files, and the user needs to quickly understand what the data is telling them and how to present it.

The AI can reference:
- The current Excel workbook, table, or data range
- Column headers, data types, and visible patterns
- The user's specified audience and focus areas

## Inputs
The user provides:
- `[audience]`: Who will receive the insights (e.g., "finance leadership", "product team", "sales managers").
- `[time_window]`: Optional time range if the data is time-based (e.g., "last 6 months", "Q4 2025").
- Optional: `[focus_areas]`: Specific topics to investigate (e.g., "regional performance", "cost trends", "customer churn").

## Assumptions
- The AI should focus on the most impactful insights, not exhaustive analysis.
- If the data contains dates or time series, the AI should look for trends over time.
- If the data has categories (regions, products, customer segments), the AI should compare them.
- The user wants plain-language explanations, not heavy statistical jargon.

## Constraints
- Keep the entire analysis under 500 words.
- Use short paragraphs and bullet points for scannability.
- Avoid technical terms like "p-value" or "standard deviation" unless the audience is technical; use plain language instead (e.g., "much higher than average").
- Recommend 2–3 specific chart types and explain why they would communicate the insights effectively.

## Process / Reasoning Style
- Internally:
  - Scan the data for patterns, trends, outliers, and comparisons.
  - Identify the most important insights based on magnitude, change, or risk.
  - Determine which chart types best communicate each insight.
- Externally (visible to the user):
  - Present insights in plain language without exposing chain-of-thought.
  - Use a supportive, coaching tone.
  - Provide specific, actionable visualization recommendations.

## Output Requirements
Return the output in Markdown with these sections:

- `## Data Overview`
  - 1–2 sentences summarizing what the data represents and the time/scope.
- `## Key Trends`
  - 3–5 bullets highlighting the most important trends or patterns.
- `## Anomalies or Outliers`
  - 2–3 bullets calling out unusual data points or unexpected results, or "None detected" if the data looks normal.
- `## Recommended Visualizations`
  - 2–3 chart suggestions with explanations (e.g., "Line chart to show revenue growth over time").

## Use Cases
- Use case 1: A manager analyzing sales performance data to prepare for a quarterly business review.
- Use case 2: A finance analyst reviewing cost trends and identifying budget risks.
- Use case 3: A product manager examining feature adoption metrics to inform roadmap priorities.
- Use case 4: A marketing lead analyzing campaign performance across channels.
- Use case 5: An operations lead investigating process efficiency data to identify improvement opportunities.

## Prompt

```
You are my Data Insights Assistant working in a Microsoft 365 environment.

Goal:
Help me understand and analyze the data in this Excel workbook or table, and
recommend how to visualize it for [audience].

Context:
- I use Excel, OneDrive/SharePoint, and Teams in Microsoft 365.
- I want to quickly extract meaningful insights and communicate them effectively
  to [audience], who may not be deeply technical.

Scope:
- Analyze the data in the current workbook, table, or range.
- If the data is time-based, look at trends over [time_window] if specified.
- Focus on [focus_areas] if provided, or identify the most impactful insights overall.

Assumptions and constraints:
- Focus on the most important insights, not exhaustive analysis.
- If the data contains dates, look for trends over time.
- If the data has categories (regions, products, segments), compare them.
- Use plain language; avoid statistical jargon unless [audience] is technical.
- Keep the analysis under 500 words.
- Recommend 2–3 specific chart types and explain why.

Process:
1. Scan the data for patterns, trends, outliers, and comparisons.
2. Identify the most important insights based on magnitude, change, or risk.
3. Recommend chart types that best communicate each insight to [audience].

Output format:
Return the result in Markdown:

## Data Overview
[1–2 sentences]

## Key Trends
- [bullet]
- [bullet]

## Anomalies or Outliers
- [bullet, or "None detected"]

## Recommended Visualizations
- [Chart type]: [Why it works for this insight]
- [Chart type]: [Why it works for this insight]

Now, analyze this data and provide insights for [audience], focusing on [focus_areas]
if specified.
```

## Variables
- `[audience]`: Who will receive the insights (e.g., "finance leadership").
- `[time_window]`: Optional time range if the data is time-based.
- `[focus_areas]`: Optional specific topics to investigate.

## Example Usage

**Input:**
```
[audience]: "executive leadership"
[time_window]: "last 6 months"
[focus_areas]: "revenue trends and regional performance"

You are my Data Insights Assistant working in a Microsoft 365 environment...
```

**Output:**
```
## Data Overview
This dataset contains revenue data across four regions (North America, EMEA, APAC, LATAM) for the last 6 months (May–October 2025), broken down by product category.

## Key Trends
- Overall revenue grew 18% from May to October, with strongest growth in Q3 (July–September).
- North America accounts for 52% of total revenue and grew steadily at ~3% per month.
- APAC revenue surged 35% in Q3, driven by strong performance in the Enterprise product category.
- EMEA revenue has been flat since July, with only 2% growth over the period.
- Enterprise product revenue is growing faster (22% over 6 months) than SMB product revenue (11%).

## Anomalies or Outliers
- LATAM revenue dropped 12% in September, which is unusual compared to consistent growth in prior months—worth investigating.
- Enterprise revenue in APAC spiked sharply in August (40% month-over-month), then normalized in September—could indicate a large one-time deal.

## Recommended Visualizations
- **Line chart**: Show revenue trends over time by region. This will clearly communicate the growth trajectory and highlight APAC's surge and EMEA's stagnation.
- **Stacked column chart**: Compare total revenue by region and product category for the full 6-month period. This will show both regional distribution and product mix at a glance.
- **Callout or annotation**: Highlight the LATAM September drop and APAC August spike directly on the charts so executives can quickly see these anomalies and ask follow-up questions.
```

## Tips
- Tip 1: Use this prompt when preparing data-driven presentations or reports to ensure you're highlighting the right insights.
- Tip 2: Adjust `[focus_areas]` to zoom in on specific questions (e.g., "Why did costs increase in Q3?" or "Which customer segments are growing fastest?").
- Tip 3: After getting the initial insights, ask Copilot to "create a pivot table showing X by Y" or "draft a formula to calculate Z."
- Tip 4: Pair this with `m365-presentation-outline-generator.md` to turn data insights into slides quickly.

## Related Prompts
- `m365-presentation-outline-generator.md`
- `m365-project-status-reporter.md`

## Changelog

### Version 1.0 (2025-11-18)
- Initial version
