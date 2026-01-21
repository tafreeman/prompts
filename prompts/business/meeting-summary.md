---
name: Meeting Summary Generator
description: Generate clear, actionable meeting summaries with key decisions, action items, and follow-up tasks.
type: how_to
---

# Meeting Summary Generator

## Description

This prompt generates clear, actionable meeting summaries with key decisions, action items, and follow-up tasks. It helps professionals quickly document meeting outcomes and ensure nothing falls through the cracks.

## Use Cases

- Summarizing team meetings and standups
- Documenting 1:1 conversations with direct reports
- Creating executive briefings from long meetings
- Sharing meeting outcomes with absent stakeholders
- Tracking action items across recurring meetings

## Variables

- `[meeting_type]`: Type of meeting (e.g., "Weekly team sync", "Project kickoff", "1:1")
- `[datetime]`: When the meeting occurred
- `[attendees]`: Who was present (names and roles)
- `[purpose]`: Meeting objective or agenda
- `[notes]`: Raw notes, transcript, or key points from the meeting

## Prompt

### System Prompt

```text
You are an expert at synthesizing meeting discussions into clear, actionable summaries. You distinguish between decisions made, items discussed, and topics parked. You ensure action items have owners and deadlines.
```

### User Prompt

```text
Create a meeting summary from the following:

Meeting Details:
- Type: [meeting_type]
- Date/Time: [datetime]
- Attendees: [attendees]
- Purpose: [purpose]

Raw Notes:
[notes]

Please provide:
1. Executive summary (3 sentences max)
2. Key decisions made
3. Action items with owners and deadlines
4. Topics discussed (not decided)
5. Parking lot items for future meetings
6. Next meeting date/topics (if applicable)
```

## Example

### Input

```text
Create a meeting summary from the following:

Meeting Details:
- Type: Weekly team sync
- Date/Time: Tuesday, Jan 14, 2025, 10:00 AM
- Attendees: Sarah (PM), John (Eng Lead), Lisa (Design), Mike (QA)
- Purpose: Sprint review and planning

Raw Notes:
Discussed sprint 12 results. Completed checkout feature, apple pay delayed due to certification. John said apple pay will slip to next sprint. Sarah concerned about Q1 deadline. Decided to add 1 contractor for 2 sprints. Lisa showed new dashboard designs, team liked option B. Need to finalize by Friday. Mike raised testing environment issues - keeps crashing. John will look into it. Sarah mentioned customer feedback on mobile - parking for now. Next sprint planning Monday.
```

### Expected Output

```text
## Meeting Summary: Weekly Team Sync
**Date**: Tuesday, Jan 14, 2025 | **Attendees**: Sarah, John, Lisa, Mike

### Executive Summary
Sprint 12 completed checkout feature but Apple Pay slipped due to certification delays. Team approved hiring a contractor to address Q1 deadline risk. Dashboard design Option B selected pending final review.

### Decisions Made
| Decision | Made By | Rationale |
|----------|---------|----------|
| Add 1 contractor for 2 sprints | Sarah | Address Q1 deadline risk from Apple Pay delay |
| Dashboard design: Option B | Team | Unanimous preference in design review |

### Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| Finalize dashboard design Option B | Lisa | Friday, Jan 17 |
| Investigate testing environment crashes | John | Thursday, Jan 16 |
| Post contractor job req | Sarah | Wednesday, Jan 15 |
| Apple Pay certification follow-up | John | Ongoing |

### Discussed (Not Decided)
- Q1 deadline risk if Apple Pay slips further
- Testing environment stability issues

### Parking Lot
- Mobile customer feedback review (Sarah to schedule separately)

### Next Meeting
**Sprint Planning**: Monday, Jan 20, 10:00 AM
```

## Tips

- Capture decisions explicitly - who decided, what was decided, why
- Action items need owners and dates - "we should do X" isn't actionable
- Distinguish between decisions made vs. topics discussed vs. items parked
- Send summary within 24 hours while context is fresh
- Keep it scannable - busy stakeholders will read headers and action items first

---

## Related Prompts

- [board-update](./board-update.md) - For executive-level meeting summaries
- [stakeholder-communication-manager](./stakeholder-communication-manager.md) - For distributing meeting outcomes
- [follow-up-email](./follow-up-email.md) - For action item follow-ups
