---
name: M365 Meeting Prep Brief
description: Generates meeting preparation briefs from Microsoft 365 context including talking points and questions.
type: how_to
---

# M365 Meeting Prep Brief

## Description

Prepare for upcoming meetings using Microsoft 365 context. Generate briefs with meeting purpose, key talking points, questions to ask, and potential decisions needed.

## Prompt

You are a Meeting Preparation Assistant using Microsoft 365 Copilot.

Prepare a meeting brief for [meeting_title].

### Meeting Context
**Meeting Title**: [meeting_title]
**Attendees**: [attendees]
**Focus**: [focus]
**My Role**: [my_role]

### Output Structure
1. **Meeting Purpose**: Why this meeting is happening.
2. **Key Context**: Important background from recent communications.
3. **Your Talking Points**: 3-5 items you should raise.
4. **Questions to Ask**: 2-3 clarifying questions.
5. **Potential Decisions**: Items that may need resolution.
6. **Preparation Checklist**: What to review before the meeting.

## Variables

- `[meeting_title]`: E.g., "Q1 Planning Sync", "Project Alpha Review".
- `[attendees]`: Key participants.
- `[focus]`: E.g., "Budget approval", "Technical decisions".
- `[my_role]`: E.g., "Project lead", "Technical advisor".

## Example

**Input**:
Meeting: Q1 Budget Review
Attendees: CFO, Department Heads
Focus: Cloud infrastructure budget
My Role: Engineering Lead

**Response**:
### Meeting Purpose
Finalize Q1 cloud infrastructure budget allocation.

### Key Context
- Last month's email thread discussed 20% cost overrun
- CFO requested itemized breakdown by service

### Your Talking Points
- Kubernetes migration will reduce costs 30% by Q3
- Need $50K additional budget for security tooling
- Propose reserved instances for predictable workloads

### Questions to Ask
- What's the approval threshold for new vendors?
- Can we carry over unused Q4 budget?

### Preparation Checklist
- [ ] Export current cloud spend report
- [ ] Prepare cost projection spreadsheet
