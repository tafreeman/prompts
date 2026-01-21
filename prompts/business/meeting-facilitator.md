---
name: Meeting Facilitator
description: Facilitates effective project meetings with agendas, facilitation techniques, decision-making process, and follow-up procedures.
type: how_to
---

# Meeting Facilitator

## Description

This prompt facilitates effective project meetings by creating structured agendas, facilitation guides, decision-making frameworks, and follow-up procedures. It helps meeting organizers run productive sessions that achieve their objectives.

## Use Cases

- Meeting Management for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Variables

- `[purpose]`: Meeting purpose (e.g., "Quarterly Business Review – Q3 results and Q4 planning")
- `[attendees]`: Attendee list (e.g., "VP Sales, Regional Directors, Finance Lead, Marketing Lead")
- `[duration]`: Meeting duration (e.g., "4 hours including lunch break")
- `[decisions]`: Key decisions needed (e.g., "Q4 quota allocation, Winter Promo campaign approval")

## Prompt

### System Prompt

```text
You are an expert meeting facilitator with experience running executive meetings, workshops, and strategic planning sessions. You help organizations design and execute meetings that achieve clear outcomes while respecting participants' time.
```

### User Prompt

```text
Design a facilitation plan for the following meeting:

Meeting Details:
- Purpose: [purpose]
- Attendees: [attendees]
- Duration: [duration]
- Key Decisions: [decisions]

Please provide:
1. Meeting agenda with time allocations
2. Preparation materials needed from attendees
3. Facilitation techniques for each section
4. Decision-making framework
5. Potential challenges and mitigation
6. Follow-up and action item template
```

## Example

### Input

```text
Design a facilitation plan for the following meeting:

Meeting Details:
- Purpose: Quarterly Business Review – Q3 results and Q4 planning
- Attendees: VP Sales, Regional Directors, Finance Lead, Marketing Lead
- Duration: 4 hours including lunch break
- Key Decisions: Q4 quota allocation, Winter Promo campaign approval
```

### Expected Output

```text
## Meeting Facilitation Plan: Q3 QBR

### Agenda
| Time | Section | Owner | Objective |
|------|---------|-------|----------|
| 9:00-9:15 | Opening & Objectives | VP Sales | Align on meeting goals |
| 9:15-10:15 | Q3 Results Review | Regional Directors | Each region: 15 min |
| 10:15-10:30 | Break | - | - |
| 10:30-11:15 | Q4 Quota Discussion | Finance Lead | Present options, discuss |
| 11:15-12:00 | **DECISION**: Q4 Quotas | VP Sales | Facilitate decision |
| 12:00-12:45 | Lunch | - | Informal networking |
| 12:45-1:30 | Winter Promo Review | Marketing Lead | Campaign proposal |
| 1:30-2:00 | **DECISION**: Promo Approval | VP Sales | Go/no-go decision |
| 2:00-2:30 | Action Items & Close | Facilitator | Summarize, assign owners |

### Pre-Work Required
| Attendee | Pre-Work | Due |
|----------|----------|-----|
| Regional Directors | Q3 results deck (5 slides max) | 48 hours before |
| Finance Lead | Q4 quota options with rationale | 48 hours before |
| Marketing Lead | Promo proposal with budget | 48 hours before |

### Facilitation Techniques

**For Q3 Review (divergent)**: Round-robin presentations, no interruptions, questions at end of each.

**For Quota Discussion (exploratory)**: Structured debate - Finance presents 3 options, each Director states preference with rationale.

**For Decisions (convergent)**: Modified Delphi - silent individual voting, then discussion of outliers, then final vote.

### Decision Framework
1. Present options with data
2. Round-robin: Each person states preference + rationale (2 min each)
3. Identify areas of agreement/disagreement
4. Discuss outliers, seek to understand
5. VP Sales makes final call if no consensus

### Follow-Up Template
```
Subject: QBR Action Items - [Date]

DECISIONS MADE:
- Q4 Quotas: [decision]
- Winter Promo: [decision]

ACTION ITEMS:
| Action | Owner | Due Date |
|--------|-------|----------|

NEXT MEETING: [Date]
```
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- Browse other Project Manager prompts in this category
- Check the business folder for similar templates
