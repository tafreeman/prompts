---

title: "User Experience Analyst"
category: "analysis"
tags: ["business-analyst", "user-experience", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# User Experience Analyst

## Description

Analyzes and improves user experiences

## Use Cases

- User Experience for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Analyze user experience for:

System/Process: [system]
User Groups: [users]
Current Pain Points: [pain_points]
Business Goals: [goals]

Provide:
1. User journey mapping
2. Pain point analysis
3. Improvement opportunities
4. Solution recommendations
5. Success metrics
6. Implementation approach
```

## Variables

- `[goals]`: Goals
- `[pain_points]`: Pain Points
- `[system]`: System
- `[users]`: Users

## Example Usage

**Input:**

```text
[system]: Employee Expense Portal (Legacy Web App)
[users]: Frequent Travelers (Sales Reps), Finance Approvers
[pain_points]: "Receipt upload fails on mobile", "Too many clicks to submit a meal", "Status is unclear"
[goals]: Reduce submission time by 50%, Reduce "Returned for Correction" rate by 20%
```

**Output:**

```text
## UX Analysis Report

### 1. User Journey Mapping (Current)
*   **Step 4 (Friction):** User must scan receipt, email to self, save to desktop, then upload. (Time: 5 mins).
*   **Step 7 (Friction):** "Category" dropdown has 50 options not sorted alphabetically.

### 2. Pain Point Analysis
*   **Severity: Critical.** Mobile incompatibility forces users to do expenses on weekends (unpaid time), leading to resentment.

### 3. Improvement Opportunities
*   **Quick Win:** Enable "Drag and Drop" for receipt images.
*   **Feature:** Implement OCR (Optical Character Recognition) to auto-fill Date and Amount.

[... continues with solution recommendations and metrics ...]
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
