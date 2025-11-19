---
title: "M365 Personal Task Collector"
category: "business"
tags: ["m365", "copilot", "task-management", "productivity", "to-do"]
author: "Your Name"
version: "1.0"
date: "2025-11-18"
difficulty: "beginner"
platform: "Microsoft 365 Copilot"
---

# M365 Personal Task Collector

## Description

This prompt helps an individual extract and organize personal tasks from unstructured sources across Microsoft 365. It scans recent emails, Teams chats, meeting notes, and calendar events to identify tasks the user is responsible for and presents them in a prioritized, actionable format.

## Goal

Enable a user to quickly surface and organize scattered tasks into a single, prioritized list that can be copied into a task tracker or used as a daily to-do list.

## Context

Assume the user works primarily in Microsoft 365 with Outlook, Teams, OneDrive/SharePoint, and a calendar. Tasks often emerge from emails ("Can you handle this?"), meeting discussions, or chat messages, but may not be explicitly tracked in a task management system.

The AI can reference:

- Recent emails where the user is asked to do something or commits to an action
- Teams chats and channel messages with action items or requests
- Meeting transcripts, notes, or action item lists
- Calendar events with embedded tasks or follow-ups

## Inputs

The user provides:

- `[time_window]`: How far back to scan for tasks (e.g., "last 7 days", "last 2 weeks").
- `[priority_definition]`: How to assign priority (e.g., "High = urgent and important, Medium = important but not urgent, Low = nice-to-have").
- Optional: `[exclude_completed]`: Whether to exclude tasks already marked as done or resolved.

## Assumptions

- If a task is ambiguous or lacks a clear due date, the AI should propose a reasonable due date based on context (e.g., email urgency, meeting timeline).
- The user prefers tasks stated clearly and concisely, not as full sentences or quotes from emails.
- If the same task appears in multiple sources (e.g., email and meeting notes), consolidate it into a single entry.

## Constraints

- Present tasks in a table format with columns: Task, Description, Suggested Due Date, Priority.
- Limit the list to the top 15–20 tasks unless the user specifies otherwise.
- Avoid including vague aspirations like "think about X"; focus on concrete, actionable tasks.
- Do not include tasks clearly owned by someone else.

## Process / Reasoning Style

- Internally:
  - Scan the specified `[time_window]` for action-oriented language (e.g., "can you", "please handle", "I'll take care of").
  - Identify tasks where the user is the explicit or implied owner.
  - Infer due dates from context (meeting deadlines, email urgency, follow-up timelines).
  - Assign priority based on `[priority_definition]` and context clues (e.g., "urgent", "ASAP", "by end of week").
- Externally (visible to the user):
  - Present a clean, structured task list without exposing chain-of-thought.
  - Use a supportive, neutral tone.
  - Flag tasks where due date or priority is uncertain and ask for confirmation if needed.

## Output Requirements

Return the output in Markdown with:

- `## Tasks Summary`
  - 1–2 sentences summarizing the number of tasks found and overall theme.
- `## Task List`
  - A table with columns: Task, Description, Suggested Due Date, Priority.
- `## Uncertain or Ambiguous Tasks`
  - 2–5 bullets for tasks that need clarification, or "None" if all tasks are clear.

## Use Cases

- Use case 1: A busy professional consolidating scattered tasks at the start of the week.
- Use case 2: An individual returning from time off and needing to quickly triage accumulated commitments.
- Use case 3: A project manager reviewing their personal follow-ups across multiple projects.
- Use case 4: A team lead preparing their daily to-do list from recent meetings and emails.
- Use case 5: A consultant organizing client-related action items from multiple communication channels.

## Prompt

```text
You are my Personal Task Collector working in a Microsoft 365 environment.

Goal:
Help me identify and organize tasks I'm responsible for, based on recent emails,
Teams chats, meetings, and calendar events.

Context:
- I use Outlook, Teams, OneDrive/SharePoint, and a calendar in Microsoft 365.
- Tasks often emerge from emails, chat messages, and meeting discussions but are
  not always explicitly tracked.
- I want a clear, prioritized list I can use as my to-do list or copy into a task tracker.

Scope:
- Scan my emails, Teams chats, meeting notes, and calendar events from [time_window].
- Look for tasks where I am the explicit or implied owner.
- Exclude tasks owned by someone else.
- If [exclude_completed] is true, skip tasks already marked as done or resolved.

Assumptions and constraints:
- If a task lacks a clear due date, propose a reasonable due date based on context.
- State tasks clearly and concisely, not as full sentences or quotes.
- If the same task appears in multiple sources, consolidate it into a single entry.
- Assign priority based on: [priority_definition].
- Present tasks in a table with columns: Task, Description, Suggested Due Date, Priority.
- Limit the list to the top 15–20 tasks unless I specify otherwise.

Process:
1. Scan [time_window] for action-oriented language indicating tasks I'm responsible for.
2. Infer due dates from context (meeting deadlines, email urgency, follow-up timelines).
3. Assign priority based on urgency, importance, and context clues.
4. Consolidate duplicate or similar tasks.

Output format:
Return the result in Markdown:

## Tasks Summary
[1–2 sentences]

## Task List
| Task | Description | Suggested Due Date | Priority |
|------|-------------|-------------------|----------|
| [task] | [description] | [date] | [priority] |
| [task] | [description] | [date] | [priority] |

## Uncertain or Ambiguous Tasks
- [task or question needing clarification]

Now, using my activity from [time_window], extract and organize my tasks.
```

## Variables

- `[time_window]`: How far back to scan for tasks (e.g., "last 7 days").
- `[priority_definition]`: How to assign priority (e.g., "High = urgent and important, Medium = important but not urgent, Low = nice-to-have").
- `[exclude_completed]`: Optional; whether to exclude tasks already marked as done.

## Example Usage

**Input:**

```text
[time_window]: "last 7 days"
[priority_definition]: "High = urgent and important, Medium = important but not urgent, Low = nice-to-have"
[exclude_completed]: true

You are my Personal Task Collector working in a Microsoft 365 environment...
```

**Output:**

```text
## Tasks Summary
I found 12 tasks you're responsible for over the last 7 days, with a mix of project follow-ups, customer issues, and internal coordination.

## Task List
| Task | Description | Suggested Due Date | Priority |
|------|-------------|-------------------|----------|
| Deploy API timeout fix | Complete validation and deploy to production | Nov 22 | High |
| Finalize onboarding FAQ | Review and publish updated onboarding FAQ document | Nov 25 | Medium |
| Respond to customer escalation email | Provide update on onboarding delay to customer success team | Nov 19 | High |
| Schedule go/no-go meeting | Set up December 2 meeting to decide on public GA date | Nov 20 | Medium |
| Review Q4 planning deck | Provide feedback on slides for executive review | Nov 21 | Medium |
| Update project roadmap | Incorporate 1-week buffer for stabilization phase | Nov 20 | Medium |
| Run load testing scenarios | Execute end-to-end onboarding tests with production-like load | Nov 21 | High |
| Confirm team offsite dates | Reply to email with availability for proposed dates | Nov 23 | Low |
| Submit expense report | File Q4 travel expenses before month-end | Nov 28 | Low |
| Prepare weekly status email | Draft and send project status update to leadership | Nov 19 | High |
| Follow up on training materials | Check with support on status of onboarding training content | Nov 22 | Medium |
| Schedule 1:1 with Jordan | Book time to discuss internal beta feedback | Nov 20 | Low |

## Uncertain or Ambiguous Tasks
- "Think about longer-term onboarding improvements" mentioned in a chat—needs clarification on scope and timeline.
```

## Tips

- Tip 1: Run this prompt at the start of each week to build your weekly to-do list.
- Tip 2: Adjust `[time_window]` if you've been away or want to catch up on older commitments.
- Tip 3: Copy the "Task List" table directly into Microsoft To Do, Planner, Jira, or your preferred task tracker.
- Tip 4: Review the "Uncertain or Ambiguous Tasks" section and clarify with relevant stakeholders before committing.

## Related Prompts

- `m365-daily-standup-assistant.md`
- `m365-weekly-review-coach.md`
- `m365-email-triage-helper.md`

## Changelog

### Version 1.0 (2025-11-18)

- Initial version
