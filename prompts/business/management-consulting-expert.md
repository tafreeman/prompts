---

title: "Management Consulting Expert"
category: "business"
tags: ["consultant", "management", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Management Consulting Expert

## Description

Provides management consulting solutions

## Use Cases

- Management for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Provide consulting for:

Client: [client]
Business Challenge: [challenge]
Industry Context: [industry]
Stakeholders: [stakeholders]
Success Criteria: [criteria]

Deliver:
1. Problem diagnosis
2. Root cause analysis
3. Solution alternatives
4. Recommendation
5. Implementation plan
6. Change management
```

## Variables

- `[challenge]`: Challenge
- `[client]`: Client
- `[criteria]`: Criteria
- `[industry]`: Industry
- `[stakeholders]`: Stakeholders

## Example Usage

**Input:**

```text
[client]: Fortune 500 CPG Company ("SnackCo")
[challenge]: Declining market share in "Healthy Snacks" segment (-5% YoY) despite growing market
[industry]: Food & Beverage / FMCG
[stakeholders]: CMO, VP Innovation, Board of Directors
[criteria]: Identify $100M growth opportunity executable within 18 months
```

**Output:**

```text
## Management Consulting Report

### 1. Problem Diagnosis
*   **Issue:** SnackCo's "Healthy" line is perceived as "processed" by Gen Z consumers.
*   **Data:** Competitors with "Clean Label" (5 ingredients or less) grew 20%.

### 2. Root Cause Analysis
*   **R&D:** Innovation cycle (2 years) is too slow to catch micro-trends (e.g., Keto, Paleo).
*   **Marketing:** Brand messaging focuses on "Low Calorie" (outdated) vs "High Protein" (trending).

### 3. Recommendation
*   **Strategy:** "Acquire & Scale". Don't build internally.
*   **Target:** Acquire a high-growth indie brand ($20M-$50M revenue) with authentic "Clean Label" credentials.

[... continues with implementation plan and change management ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Consultant prompts in this category
- Check the business folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
