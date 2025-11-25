---

title: "Agile Sprint Planner"
category: "business"
tags: ["project-manager", "agile", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Agile Sprint Planner

## Description

Plans and manages agile sprints

## Use Cases

- Agile for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Plan sprint for:

Project: [project_name]
Sprint Duration: [duration]
Team Capacity: [capacity]
Priority Features: [features]
Definition of Done: [dod]

Provide:
1. Sprint goal
2. User story breakdown
3. Task estimation
4. Capacity planning
5. Risk mitigation
6. Success metrics
```

## Variables

- `[capacity]`: Capacity
- `[dod]`: Dod
- `[duration]`: Duration
- `[features]`: Features
- `[project_name]`: Project Name

## Example Usage

**Input:**

```text
[project_name]: E-commerce Mobile App
[duration]: 2 Weeks (Sprint 12)
[capacity]: 80 Story Points (Reduced from 100 due to Thanksgiving Holiday)
[features]: "One-click Checkout", "Apple Pay Integration", "Wishlist Sync"
[dod]: Unit tests passed, UI automated tests green, PO sign-off, Analytics events fired
```

**Output:**

```text
## Sprint Plan

### 1. Sprint Goal
"Enable frictionless payments to reduce cart abandonment by 15% before Black Friday."

### 2. User Story Breakdown
*   **Story 1 (13 pts):** As a user, I want to pay with Apple Pay so I don't have to enter card details.
*   **Story 2 (8 pts):** As a user, I want my "Default Card" pre-selected in Checkout.

### 3. Capacity Planning
*   **Total Load:** 75 Points (leaving 5 pts buffer for production hotfixes).
*   **Risk:** Apple Pay certification may take >2 days. *Mitigation:* Start certification process on Day 1.

[... continues with task estimation and success metrics ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Project Manager prompts in this category
- Check the business folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
