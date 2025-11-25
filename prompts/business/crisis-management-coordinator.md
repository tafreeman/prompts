---

title: "Crisis Management Coordinator"
category: "business"
tags: ["project-manager", "crisis-management", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Crisis Management Coordinator

## Description

Manages project crises

## Use Cases

- Crisis Management for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Handle crisis for:

Project: [project_name]
Crisis Description: [crisis]
Impact Assessment: [impact]
Urgency Level: [urgency]

Provide:
1. Crisis response plan
2. Stakeholder communication
3. Resource mobilization
4. Risk mitigation
5. Recovery strategy
6. Lessons learned
```

## Variables

- `[crisis]`: Crisis
- `[impact]`: Impact
- `[project_name]`: Project Name
- `[urgency]`: Urgency

## Example Usage

**Input:**

```text
[project_name]: Global ERP Rollout
[crisis]: Ransomware attack detected on Staging Environment servers
[impact]: All test data encrypted, rollout to APAC region (scheduled for Monday) blocked, potential PII leak
[urgency]: Critical (Level 1) - Immediate Action Required
```

**Output:**

```text
## Crisis Response Plan

### 1. Immediate Response (Containment)
*   **Action:** Isolate Staging VPC from Production and Corporate networks immediately.
*   **Owner:** CISO & Network Ops Lead.
*   **Status:** Execute "Kill Switch" protocol.

### 2. Stakeholder Communication
*   **Internal:** Notify Steering Committee via out-of-band channel (Signal/WhatsApp) - Do not use email.
*   **External:** Prepare statement for APAC partners regarding "Technical Maintenance Delay" (holding statement).

### 3. Risk Mitigation
*   **Forensics:** Engage 3rd party incident response team to determine entry point.
*   **Recovery:** Do not pay ransom. Restore Staging from immutable backups (WORM storage) once environment is clean.

[... continues with resource mobilization and lessons learned ...]
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
