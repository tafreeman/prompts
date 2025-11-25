---

title: "Stakeholder Requirements Gatherer"
category: "analysis"
tags: ["business-analyst", "stakeholder-management", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Stakeholder Requirements Gatherer

## Description

Gathers and manages stakeholder requirements

## Use Cases

- Stakeholder Management for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Gather requirements from:

Project: [project_name]
Stakeholder Groups: [groups]
Business Domain: [domain]
Complexity Level: [complexity]

Include:
1. Stakeholder analysis
2. Interview planning
3. Requirements elicitation
4. Conflict resolution
5. Prioritization framework
6. Communication strategy
```

## Variables

- `[complexity]`: Complexity
- `[domain]`: Domain
- `[groups]`: Groups
- `[project_name]`: Project Name

## Example Usage

**Input:**

```text
[project_name]: CRM Migration (Salesforce to HubSpot)
[groups]: Sales Reps (End Users), Sales Ops (Admins), Marketing (Lead Gen)
[domain]: B2B SaaS Sales
[complexity]: High (Data migration + Process re-engineering required)
```

**Output:**

```text
## Stakeholder Requirements Plan

### 1. Stakeholder Analysis
*   **Sales Reps:** High Influence / High Interest. Concern: "Will this slow me down?"
*   **Marketing:** Medium Influence / High Interest. Concern: "Will lead attribution break?"

### 2. Interview Planning
*   **Format:** "Day in the Life" shadowing sessions with top 3 sales reps.
*   **Key Question:** "Show me the most frustrating part of logging a deal today."

### 3. Requirements Elicitation
*   **Requirement (Sales):** "Must be able to log calls from mobile app in < 2 clicks."
*   **Requirement (Ops):** "Must enforce 'Deal Stage' validation rules."

[... continues with conflict resolution and communication ...]
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
