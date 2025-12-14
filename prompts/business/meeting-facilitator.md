---
title: Meeting Facilitator
shortTitle: Meeting Facilitator
intro: Facilitates effective project meetings with agendas, facilitation techniques,
  decision-making process, and follow-up procedures.
type: how_to
difficulty: intermediate
audience:
- project-manager
- business-analyst
platforms:
- claude
- chatgpt
- github-copilot
topics:
- communication
- project-management
author: Prompts Library Team
version: '1.0'
date: '2025-11-16'
governance_tags:
- PII-safe
dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# Meeting Facilitator

---

## Description

Facilitates effective project meetings

---

## Use Cases

- Meeting Management for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Plan meeting for:

Meeting Purpose: [purpose]
Attendees: [attendees]
Duration: [duration]
Key Decisions Needed: [decisions]

Include:
1. Meeting agenda
2. Pre-meeting preparation
3. Facilitation techniques
4. Decision-making process
5. Action item tracking
6. Follow-up procedures
```text

---

## Variables

- `[purpose]`: Meeting purpose (e.g., "Quarterly Business Review – Q3 results and Q4 planning")
- `[attendees]`: Attendee list (e.g., "VP Sales, Regional Directors, Finance Lead, Marketing Lead")
- `[duration]`: Meeting duration (e.g., "4 hours including lunch break")
- `[decisions]`: Key decisions needed (e.g., "Q4 quota allocation, Winter Promo campaign approval")

---

## Example

```text
## Meeting Plan

### 1. Agenda
*   **09:00 - 10:00:** Q3 Performance Review (Data Deep Dive).
*   **10:00 - 11:00:** Marketing Retrospective & Q4 Plan.
*   **11:15 - 12:30:** Q4 Quota Setting & "Winter Promo" Decision.
*   **12:30 - 13:00:** Action Items & Lunch.

### 2. Pre-meeting Preparation
*   **Requirement:** All Regional Directors must update Salesforce pipeline by Friday 5pm.
*   **Read-ahead:** Finance to circulate "Q3 Variance Report" 48hrs prior.

### 3. Facilitation Techniques
*   **"Parking Lot":** Use for tactical issues (e.g., specific deal blockers) to keep QBR strategic.
*   **ELMO Rule:** "Enough, Let's Move On" if quota debates circle for >10 mins.

[... continues with decision process and follow-up ...]
```text

---


## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- Browse other Project Manager prompts in this category
- Check the business folder for similar templates
