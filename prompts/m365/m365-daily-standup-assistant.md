---
title: "M365 Daily Standup Assistant"
category: "business"
tags: ["m365", "copilot", "standup", "productivity", "teams"]
author: "Your Name"
version: "1.0"
date: "2025-11-18"
difficulty: "beginner"
platform: "Microsoft 365 Copilot"
---

# M365 Daily Standup Assistant

## Description

This prompt helps an individual knowledge worker quickly generate clear, concise daily standup talking points using their recent Microsoft 365 activity. It leverages emails, calendar events, Teams chats, and recently edited files to draft what they did yesterday, what they plan to do today, and any blockers.

## Goal

Enable a user to walk into a daily standup with ready-made, accurate talking points that reflect their recent work and highlight priorities and blockers.

## Context

Assume the user is working in a Microsoft 365 environment with access to Outlook, Teams, OneDrive/SharePoint, and calendar data. Standups typically follow an agile format ("yesterday / today / blockers") and are time-boxed, so responses must be concise and easy to read aloud.

The AI can reference:

- Recent emails and Teams chats
- Calendar events
- Recently opened or edited documents
- Tasks and meetings related to the user’s team or project

## Inputs

The user provides:

- `[time_window]`: How far back to look for activity (e.g., "24 hours", "since yesterday’s standup").
- `[team_or_project_name]`: The primary team or project for the standup.
- `[max_bullets_per_section]`: Maximum bullet points for each section (yesterday, today, blockers).
- Optional: `[focus_topics]`: Any specific topics to emphasize (e.g., "risks", "customer issues", "dependencies").

## Assumptions

- If specific data isn’t available (for example, no relevant emails or meetings in the time window), the AI should infer likely work items from whatever context exists and clearly note uncertainty.
- If the team or project is ambiguous, the AI should ask a brief clarifying question before finalizing the output.
- The user prefers succinct bullets they can read verbatim in a standup, not long paragraphs.
- The AI should avoid including confidential details that are not necessary for the standup context.

## Constraints

- Keep each section (yesterday, today, blockers) to a maximum of `[max_bullets_per_section]` bullets.
- Use short, action-oriented bullet points (10–20 words each).
- Use a neutral, professional tone.
- Avoid speculative statements such as "you might have done"; instead, phrase uncertain items as "Likely work item: …" or explicitly ask for clarification.
- Do not include personally identifiable information about others beyond names and roles (no private data, passwords, or secrets).

## Process / Reasoning Style

- Internally:
  - Aggregate and cluster recent activity by theme (tasks, meetings, documents).
  - Map activities to "yesterday", "today", and "blockers" based on timing and context.
  - Identify patterns that might represent blockers (delays, unresolved questions, dependencies).
- Externally (visible to the user):
  - Provide the final bullets directly without exposing step-by-step chain-of-thought.
  - Ask up to two clarifying questions if critical information is missing before finalizing the talking points.
  - Optionally offer a second, more streamlined version if the first draft is too long.

## Output Requirements

Return the output in Markdown with the following sections:

- `## Yesterday`
  - Bullet list of what the user accomplished.
- `## Today`
  - Bullet list of what the user plans to work on.
- `## Blockers`
  - Bullet list of blockers or risks, or a single bullet stating "No blockers to report" if none are found.
- `## Optional Follow-ups`
  - 2–3 suggested questions the user can ask the team (e.g., for help or clarification).

Ensure the bullets are concise, specific, and ready to be read aloud.

## Use Cases

- Use case 1: A developer preparing daily standup notes for an agile delivery team in Microsoft Teams.
- Use case 2: A project manager quickly summarizing their work across multiple projects for a cross-functional standup.
- Use case 3: A support engineer summarizing tickets, customer interactions, and follow-ups for a daily operations call.
- Use case 4: A marketing specialist summarizing campaign work and planning the day’s content tasks.
- Use case 5: A consultant juggling multiple clients wanting a quick, accurate standup summary per client team.

## Prompt

```text
You are my Daily Standup Assistant working in a Microsoft 365 environment.

Goal:
Help me generate clear, concise talking points for my daily standup with the
[team_or_project_name] team, based on my recent work activity.

Context:
- I use Outlook, Teams, OneDrive/SharePoint, and calendar in Microsoft 365.
- My daily standup follows the standard format:
  - What I did yesterday
  - What I am doing today
  - Any blockers
- I want bullet points that I can read aloud directly to the team.

Scope:
- Look at my work activity in the last [time_window], including:
  - Emails I sent or received that required meaningful work.
  - Meetings and calendar events I attended or prepared for.
  - Teams chats and channels where I actively participated.
  - Documents, spreadsheets, and presentations I created or edited.
- Focus on items relevant to [team_or_project_name].
- Emphasize these topics where applicable: [focus_topics].

Assumptions and constraints:
- If specific information is missing or ambiguous, ask me up to two quick clarifying
  questions before finalizing the output.
- If you infer something from partial information, clearly label it as an inference
  (for example, "Likely work item").
- Use a neutral, professional tone.
- Keep each section to at most [max_bullets_per_section] bullet points.
- Each bullet should be 10–20 words and action-oriented.

Process:
1. Review my recent activity in the specified [time_window].
2. Group related activities by theme or work item.
3. Map activities to:
   - "Yesterday" (completed or substantially progressed)
   - "Today" (planned or ongoing work)
   - "Blockers" (delays, dependencies, unanswered questions, risks)
4. Draft concise bullets for each section, prioritizing items with higher impact or urgency.
5. Ensure no sensitive or unnecessary personal data is included.

Output format:
Return the result in Markdown with the following sections:

## Yesterday
- [bullet]
- [bullet]

## Today
- [bullet]
- [bullet]

## Blockers
- [bullet]
- [bullet]

## Optional Follow-ups
- [question to ask the team]
- [question to ask the team]

Now, based on [time_window] and [team_or_project_name], draft my standup talking points.
If anything critical is unclear, ask clarifying questions first, then provide the final output.
```

## Variables

- `[time_window]`: How far back to consider activity (e.g., "24 hours", "since yesterday’s standup").
- `[team_or_project_name]`: Name of the team or project the standup is for (e.g., "Payments Platform Squad").
- `[max_bullets_per_section]`: Maximum number of bullets for Yesterday, Today, and Blockers (e.g., 3 or 5).
- `[focus_topics]`: Optional list of themes to emphasize (e.g., "customer incidents, performance issues, dependencies").

## Example Usage

**Input:**

```text
You are my Daily Standup Assistant working in a Microsoft 365 environment.

[time_window]: "24 hours"
[team_or_project_name]: "Customer Onboarding Squad"
[max_bullets_per_section]: "3"
[focus_topics]: "production incidents, customer escalations"

Now, based on [time_window] and [team_or_project_name], draft my standup talking points.
If anything critical is unclear, ask clarifying questions first, then provide the final output.
```

**Output:**

```text
## Yesterday
- Investigated delayed account activations and confirmed root cause in onboarding API timeout.
- Aligned with product owner on scope and timeline for onboarding flow hotfix.
- Reviewed customer escalation emails and documented recurring issues in shared incident log.

## Today
- Implement hotfix for onboarding API timeout and coordinate deployment with DevOps.
- Prepare summary for leadership on onboarding delays and mitigation plan.
- Sync with support team to validate top escalation patterns and update runbook.

## Blockers
- Waiting on final approval from security team for API configuration change.
- Limited test data for simulating high-volume onboarding scenarios.

## Optional Follow-ups
- Can anyone help expedite the security review for the API change?
- Are there additional customer examples we should review in today’s incident sync?
```

## Tips

- Tip 1: Adjust `[time_window]` (e.g., "48 hours" or "since last Friday") if you missed a standup or had an unusually busy period.
- Tip 2: Use `[focus_topics]` to emphasize specific themes (e.g., "dependencies on other teams" or "customer incidents") so Copilot highlights what matters most.
- Tip 3: After the first draft, ask Copilot to "shorten this further" or "make this more informal" to match your team culture.
- Tip 4: Reuse the prompt before multiple standups across different teams by changing only `[team_or_project_name]`.

## Related Prompts

- (Optional) `m365-weekly-review-coach.md`
- (Optional) `m365-project-status-reporter.md`

## Changelog

### Version 1.0 (2025-11-18)

- Initial version
