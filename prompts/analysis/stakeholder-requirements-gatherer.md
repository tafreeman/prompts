---
title: Stakeholder Requirements Gatherer
shortTitle: Stakeholder Requirements
intro: Gathers and manages stakeholder requirements with interview planning, conflict
  resolution, and communication strategies.
type: how_to
difficulty: intermediate
audience:

- business-analyst
- project-manager

platforms:

- claude
- chatgpt
- github-copilot

topics:

- requirements
- stakeholder-management

author: Prompts Library Team
version: '1.0'
date: '2025-11-16'
governance_tags:

- PII-safe

dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# Stakeholder Requirements Gatherer

---

## Description

Gathers and manages stakeholder requirements

---

## Use Cases

- Stakeholder Management for Business Analyst persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

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

```text

## Variables

| Variable | Description |
| ---------- | ------------- |
| `[project_name]` | Project name and scope |
| `[groups]` | Stakeholder groups/roles to interview |
| `[domain]` | Business domain/context (industry, processes, regulations) |
| `[complexity]` | Complexity level and notable constraints (integrations, legacy, scale) |

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
```text

---


## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Example Usage

### Context

A Business Analyst is leading requirements gathering for a CRM migration project with conflicting stakeholder priorities between Sales, Marketing, and Operations teams.

### Input

```text
Project: Salesforce to HubSpot CRM Migration
Stakeholder Groups: Sales Reps, Sales Leadership, Marketing, Revenue Operations, IT
Business Domain: B2B SaaS with complex sales cycles
Complexity Level: High (10 years of customizations, 50+ integrations)
```

### Expected Output

A comprehensive stakeholder requirements plan including:

1. **Stakeholder Analysis** - Power/interest matrix, key influencers, potential blockers
2. **Interview Planning** - Interview guides per stakeholder type, "day in the life" session design
3. **Requirements Elicitation** - Categorized requirements by stakeholder with priority and feasibility
4. **Conflict Resolution** - Identified conflicts (Sales wants simplicity, Ops wants data capture) with resolution approach
5. **Prioritization Framework** - MoSCoW or weighted scoring with stakeholder buy-in
6. **Communication Strategy** - Cadence for updates, feedback loops, sign-off process

---

## Related Prompts

- [Requirements Analysis Expert](./requirements-analysis-expert.md) - For detailed requirements documentation
- [Gap Analysis Expert](./gap-analysis-expert.md) - For current/desired state comparison
- [Process Optimization Consultant](./process-optimization-consultant.md) - For process requirements
- [User Experience Analyst](./user-experience-analyst.md) - For user-centric requirements
