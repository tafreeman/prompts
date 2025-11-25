---

title: "Stakeholder Communication Manager"
category: "business"
tags: ["project-manager", "communication", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Stakeholder Communication Manager

## Description

Manages stakeholder communications

## Use Cases

- Communication for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Develop communication strategy for:

Project: [project_name]
Stakeholders: [stakeholders]
Project Phase: [phase]
Communication Challenges: [challenges]

Include:
1. Stakeholder analysis
2. Communication matrix
3. Meeting schedules
4. Reporting templates
5. Escalation procedures
6. Feedback mechanisms
```

## Variables

- `[challenges]`: Challenges
- `[phase]`: Phase
- `[project_name]`: Project Name
- `[stakeholders]`: Stakeholders

## Example Usage

**Input:**

```text
[project_name]: SAP S/4HANA Implementation
[stakeholders]: CFO (Sponsor), VP Supply Chain (Key User), IT Director, Warehouse Staff (End Users)
[phase]: Blueprinting / Design
[challenges]: Resistance to change from warehouse staff (fear of automation), CFO demanding faster ROI visibility
```

**Output:**

```text
## Communication Strategy

### 1. Stakeholder Analysis
*   **CFO (High Power/High Interest):** Needs weekly executive summary focused on budget and milestones.
*   **Warehouse Staff (Low Power/High Interest):** Needs reassurance, training, and "What's in it for me?" (WIIFM).

### 2. Communication Matrix
*   **Steering Committee (CFO/VP):** Bi-weekly status meeting (Tuesday 10am).
*   **Project Team:** Daily Standup (9am).
*   **All Hands (Warehouse):** Monthly Town Hall with Q&A.

### 3. Key Messages
*   **To CFO:** "We are on track to deliver inventory visibility by Q3, enabling 15% stock reduction."
*   **To Staff:** "The new system eliminates manual paper counting, making your job safer and faster."

[... continues with reporting templates and feedback mechanisms ...]
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
