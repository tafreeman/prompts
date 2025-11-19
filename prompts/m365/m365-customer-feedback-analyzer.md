---
title: "M365 Customer Feedback Analyzer"
description: "Analyzes unstructured customer feedback (emails, notes, surveys) to identify key themes, sentiment, and actionable insights."
category: "analysis"
tags: ["m365", "customer-success", "feedback", "sentiment-analysis", "summarization"]
author: "GitHub Copilot"
version: "1.0"
date: "2025-11-18"
difficulty: "Intermediate"
platform: "Microsoft 365 Copilot"
---

## Description

This prompt is designed for Product Managers, Support Leads, and Sales teams who receive scattered feedback from customers. It uses the LLM's summarization capabilities to aggregate multiple feedback points into a coherent report with identified trends and recommended actions.

## Goal

To turn raw, unstructured customer feedback into a structured analysis of sentiment, recurring themes, and necessary actions.

## Inputs

- **Feedback Source**: [feedback_source]
- **Raw Feedback Text**: [raw_feedback]
- **Focus Area**: [focus_area]

## Prompt

You are an expert Customer Experience Analyst. I have collected feedback from [feedback_source] and I need you to analyze it.

**Raw Feedback:**
"""
[raw_feedback]
"""

**Analysis Focus**: Please focus specifically on [focus_area].

Based on the text above, please generate a **Feedback Analysis Report**:

1. **Overall Sentiment**: (Positive/Neutral/Negative) with a brief summary.
2. **Top 3 Themes**: The most frequent topics or issues mentioned.
3. **Specific Pain Points**: Direct quotes or details about what is frustrating customers.
4. **Feature Requests**: Any specific suggestions for improvement.
5. **Recommended Actions**: 3 bullet points on what we should do next.

## Variables

- `[feedback_source]`: Where the data came from (e.g., "Q3 Survey", "Support Emails", "App Store Reviews").
- `[raw_feedback]`: The pasted text of the feedback (can be long).
- `[focus_area]`: What you care about most (e.g., "UI/UX", "Pricing", "Bugs", "General Satisfaction").

## Example Usage

**Input:**

- `[feedback_source]`: "Beta User Emails"
- `[raw_feedback]`: "User A: I love the new design but the login is slow. User B: The app crashed twice when I tried to upload a photo. User C: Great features, but I can't find the settings menu. User D: Uploading is broken for me too."
- `[focus_area]`: "Bugs and Usability"

**Output:**

### Feedback Analysis Report: Beta User Emails

**1. Overall Sentiment**
**Mixed**. Users appreciate the new design/features but are frustrated by technical stability.

**2. Top 3 Themes**

- Photo Upload Failures
- Slow Login Performance
- Navigation/UI Confusion

**3. Specific Pain Points**

- "App crashed twice when I tried to upload a photo."
- "Can't find the settings menu."

**4. Feature Requests**

- Clearer navigation to Settings.

**5. Recommended Actions**

- **Urgent**: Investigate and fix the photo upload crash.
- **High**: Optimize login API response time.
- **Medium**: A/B test a more visible Settings icon.

## Tips

- You can paste up to ~2000 words of feedback at once. For larger datasets, analyze in batches and then ask Copilot to summarize the batch results.
- Be careful not to include PII (Personally Identifiable Information) like customer phone numbers or addresses in the `[raw_feedback]`.

## Related Prompts

- `m365-data-insights-assistant`
- `consumer-behavior-researcher`

## Changelog

- 2025-11-18: Initial version created.
