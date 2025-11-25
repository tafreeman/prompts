---

title: "Project Charter Creator"
category: "business"
tags: ["project-manager", "planning", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Project Charter Creator

## Description

Develops comprehensive project charters

## Use Cases

- Planning for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Create a project charter for:

Project Name: [project_name]
Business Objective: [objective]
Key Stakeholders: [stakeholders]
Budget Range: [budget]
Timeline: [timeline]

Include:
1. Executive summary
2. Scope and deliverables
3. Success criteria
4. Resource requirements
5. Risk assessment
6. Communication plan
```

## Variables

- `[budget]`: Budget
- `[objective]`: Objective
- `[project_name]`: Project Name
- `[stakeholders]`: Stakeholders
- `[timeline]`: Timeline

## Example Usage

**Input:**

```text
[project_name]: "Project Phoenix" (CRM Replacement)
[objective]: Replace 15-year-old legacy CRM with Salesforce to improve sales efficiency by 25% and enable mobile access
[stakeholders]: VP Sales (Sponsor), CIO, Regional Sales Managers, IT Director
[budget]: $1.5M (CapEx) + $200k/yr (OpEx)
[timeline]: 12 Months (Jan 2026 - Dec 2026)
```

**Output:**

```text
## Project Charter

### 1. Executive Summary
Legacy CRM is end-of-life and lacks mobile capabilities, causing sales reps to update data only once a week. "Project Phoenix" will implement Salesforce Sales Cloud to enable real-time data entry and boost sales productivity.

### 2. Scope and Deliverables
*   **In Scope:** Migration of 5 years of customer data, Integration with Outlook, Mobile App rollout, Training for 200 reps.
*   **Out of Scope:** Marketing Automation (Phase 2), Customer Support module.

### 3. Success Criteria
*   **Adoption:** 90% of sales reps logging in daily by Month 3 post-launch.
*   **Efficiency:** Reduce "Admin Time" per rep from 5hrs/week to 2hrs/week.
*   **Revenue:** 10% increase in pipeline visibility.

[... continues with resource requirements and risks ...]
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
