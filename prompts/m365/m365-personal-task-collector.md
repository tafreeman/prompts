---
name: M365 Personal Task Collector
description: This prompt helps an individual extract and organize personal tasks from unstructured sources across Microsoft 365. It scans recent emails, Teams chats, meeting notes, and calendar events to identi...
type: how_to
---

# M365 Personal Task Collector

## Use Cases

- Use case 1: A busy professional consolidating scattered tasks at the start of the week.
- Use case 2: An individual returning from time off and needing to quickly triage accumulated commitments.
- Use case 3: A project manager reviewing their personal follow-ups across multiple projects.
- Use case 4: A team lead preparing their daily to-do list from recent meetings and emails.
- Use case 5: A consultant organizing client-related action items from multiple communication channels.

## Example

**Inputs**

- `[time_window]`: `last 7 days`
- `[priority_definition]`: `High = urgent and important; Medium = important; Low = nice-to-have`
- `[exclude_completed]`: `true`

**Expected output (excerpt)**

```text
## Tasks Summary
I found 10 tasks you're responsible for over the last 7 days, mostly follow-ups from meetings and email requests.

## Task List
| Task | Description | Suggested Due Date | Priority |
| ------ | ------------- | ------------------- | ---------- |
| Respond to customer escalation email | Provide an update to the CS team | Nov 19 | High |
| Schedule go/no-go meeting | Book time with key stakeholders | Nov 20 | Medium |

## Uncertain or Ambiguous Tasks

- "Review onboarding improvements" mentioned in chat — what scope and timeframe?

```


## Tips

- Tip 1: Run this prompt at the start of each week to build your weekly to-do list.
- Tip 2: Adjust `[time_window]` if you've been away or want to catch up on older commitments.
- Tip 3: Copy the "Task List" table directly into Microsoft To Do, Planner, Jira, or your preferred task tracker.
- Tip 4: Review the "Uncertain or Ambiguous Tasks" section and clarify with relevant stakeholders before committing.

---

## Related Prompts

- `m365-daily-standup-assistant.md`
- `m365-weekly-review-coach.md`
- `m365-email-triage-helper.md`
