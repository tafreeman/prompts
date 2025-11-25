---

title: "Organizational Change Manager"
category: "business"
tags: ["consultant", "change-management", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Organizational Change Manager

## Description

Manages organizational change initiatives

## Use Cases

- Change Management for Consultant persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Manage change for:

Organization: [organization]
Change Initiative: [initiative]
Impacted Groups: [groups]
Resistance Factors: [resistance]

Provide:
1. Change impact assessment
2. Stakeholder analysis
3. Communication strategy
4. Training plan
5. Resistance management
6. Success measurement
```

## Variables

- `[groups]`: Groups
- `[initiative]`: Initiative
- `[organization]`: Organization
- `[resistance]`: Resistance

## Example Usage

**Input:**

```text
[organization]: Global Manufacturing Co. (Engineering Division)
[initiative]: Agile Transformation (Waterfall to Scrum)
[groups]: Engineering (500 staff), Product Mgmt (50 staff), QA (100 staff)
[resistance]: Middle management fears loss of control; Senior engineers skeptical of "meetings overhead"
```

**Output:**

```text
## Change Management Strategy (ADKAR Model)

### 1. Change Impact Assessment
*   **High Impact:** Project Managers (Role changes to Scrum Master/Product Owner).
*   **Medium Impact:** Developers (New cadence, daily standups).

### 2. Stakeholder Analysis
*   **Resistors:** Engineering Directors. *Strategy:* Involve them in defining "Definition of Done" to maintain quality control authority.
*   **Champions:** Junior Developers (Eager for modern practices).

### 3. Communication Strategy
*   **The "Why":** "We are moving to Agile to reduce our 18-month release cycle to 3 months, keeping us competitive."
*   **Channels:** Town Halls for vision, "Lunch & Learns" for tactics.

[... continues with training plan and resistance management ...]
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
