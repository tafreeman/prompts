---
title: "Crisis Management Coordinator"
shortTitle: "Crisis Management"
intro: "Manages project crises with response plans, stakeholder communication, resource mobilization, and recovery strategy."
type: "how_to"
difficulty: "intermediate"
audience:

  - "project-manager"
  - "solution-architect"

platforms:

  - "claude"
  - "chatgpt"
  - "github-copilot"

topics:

  - "risk-management"
  - "project-management"

author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
governance_tags:

  - "PII-safe"

dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 0.0
---
# Crisis Management Coordinator

---

## Description

Helps project leaders and incident commanders coordinate structured responses when projects or services are in crisis. Guides you through containment steps, stakeholder communication, resource mobilisation, recovery planning, and lessons learned.

---

## Use Cases

- Coordinating response to major production incidents or outages
- Managing high-impact project delays or deployment failures
- Preparing structured war-room plans for executive stakeholders
- Standardising crisis playbooks across programmes or portfolios
- Capturing post-incident lessons learned and improvements

---

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

```text

---

## Variables

- `[project_name]`: Name of the project or system in crisis (e.g., "Global Payments Platform Migration")
- `[crisis]`: Description of the crisis situation (e.g., "New release caused 18% payment failure rate in EU region")
- `[impact]`: Business impact assessment (e.g., "$250K lost revenue per hour, reputational damage, contract breach risk")
- `[urgency]`: Severity level (e.g., "Critical (SEV-1) – immediate executive visibility required")

---

## Example

### Context

During a critical production deployment, a payment platform experiences a severe outage affecting thousands of customers. Leadership needs a clear crisis response plan, communication strategy, and recovery roadmap within minutes.

### Input

```text
Handle crisis for:

Project: Global Payments Platform Migration
Crisis Description: New release caused intermittent payment failures across EU region; error rate spiked to 18% and major merchant complained publicly on social media.
Impact Assessment: Estimated $250K in lost revenue per hour, reputational damage in key markets, and contract breach risk with 3 strategic merchants.
Urgency Level: Critical (SEV-1) – immediate executive visibility required.

Provide:

1. Crisis response plan
2. Stakeholder communication
3. Resource mobilization
4. Risk mitigation
5. Recovery strategy
6. Lessons learned

```text

### Expected Output

The AI returns a crisis playbook-style document with: immediate containment actions, clear ownership and war-room structure, internal and external communication templates, a risk and impact summary, a phased recovery and verification plan, and a short "lessons learned" section to capture improvements after the incident.

---


## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- [Risk Management Analyst](./risk-management-analyst.md) - For proactive risk identification before crises
- [Stakeholder Communication Manager](./stakeholder-communication-manager.md) - For crisis communications
- [Change Management Coordinator](./change-management-coordinator.md) - For managing organizational change after crisis
- [Business Strategy Analysis](./business-strategy-analysis.md) - For strategic recovery planning
