---

title: "Meeting Facilitator"
category: "business"
tags: ["project-manager", "meeting-management", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Meeting Facilitator

## Description

Facilitates effective project meetings

## Use Cases

- Meeting Management for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

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
```

## Variables

- `[attendees]`: Attendees
- `[decisions]`: Decisions
- `[duration]`: Duration
- `[purpose]`: Purpose

## Example Usage

**Input:**

```text
[purpose]: Q3 Quarterly Business Review (QBR)
[attendees]: Regional Sales Directors (x4), VP Sales, Marketing Lead, Finance Partner
[duration]: 4 Hours (Half-day offsite)
[decisions]: Finalize Q4 Quotas, Approve Q4 Marketing Budget Allocation, Go/No-Go on "Winter Promo"
```

**Output:**

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
