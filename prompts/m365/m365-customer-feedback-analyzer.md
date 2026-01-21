---
name: M365 Customer Feedback Analyzer
description: Analyzes unstructured customer feedback to identify themes, sentiment, and actionable insights.
type: how_to
---

# M365 Customer Feedback Analyzer

## Description

Transform raw, unstructured customer feedback (emails, surveys, reviews) into structured analysis. Identify sentiment, recurring themes, and recommended actions for product and support teams.

## Prompt

You are a Customer Insights Analyst using Microsoft 365 Copilot.

Analyze the customer feedback below and produce a structured report.

### Feedback Context
**Source**: [feedback_source]
**Focus Area**: [focus_area]

**Raw Feedback**:
[raw_feedback]

### Required Analysis
1. **Sentiment Overview**: Overall positive/negative/neutral breakdown.
2. **Key Themes**: Top 5 recurring topics with frequency.
3. **Critical Issues**: Urgent items requiring immediate attention.
4. **Positive Highlights**: What customers appreciate.
5. **Recommended Actions**: Prioritized next steps.

## Variables

- `[feedback_source]`: E.g., "Q3 NPS Survey", "Support Emails", "App Store Reviews".
- `[focus_area]`: E.g., "UI/UX", "Pricing", "Reliability".
- `[raw_feedback]`: The pasted feedback text.

## Example

**Input**:
Source: App Store Reviews (Jan 2026)
Focus: Mobile experience
Feedback: "Love the app but crashes on iOS 17..." "Great features, slow sync..." "Best tool but needs dark mode"

**Response**:
### Sentiment: Mixed (60% positive, 40% negative)

### Key Themes
| Theme | Count | Sentiment |
|-------|-------|-----------|
| App crashes | 12 | Negative |
| Feature praise | 8 | Positive |
| Sync speed | 6 | Negative |
| Dark mode request | 5 | Neutral |

### Recommended Actions
1. **P0**: Investigate iOS 17 crash reports
2. **P1**: Optimize sync performance
3. **P2**: Add dark mode to roadmap
