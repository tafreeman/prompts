---
title: "M365 Project Status Reporter"
category: "business"
tags: ["m365", "copilot", "project-management", "status-update", "reporting"]
author: "Your Name"
version: "1.0"
date: "2025-11-18"
difficulty: "beginner"
platform: "Microsoft 365 Copilot"
---

# M365 Project Status Reporter

## Description

This prompt helps an individual quickly generate a structured project status update using Microsoft 365 context. It synthesizes recent emails, Teams chats, documents, and calendar events into a summary suitable for stakeholders, highlighting progress, risks, and upcoming milestones.

## Goal

Enable a user to produce a clear, accurate project status update without manually compiling information from multiple sources, saving time and ensuring nothing important is missed.

## Context

Assume the user manages or contributes to a project within Microsoft 365, using Outlook, Teams, OneDrive/SharePoint, and a calendar. Status updates typically cover progress since the last update, current risks or issues, upcoming milestones, and requests for help or decisions.

The AI can reference:

- Recent emails and Teams chats related to the project
- Documents and files updated in project-related folders
- Calendar events (meetings, milestones, deadlines)
- Previous status updates if available

## Inputs

The user provides:

- `[project_name]`: Name of the project (e.g., "Customer Onboarding Platform V2").
- `[time_window]`: Period to review (e.g., "last 7 days", "since last status update").
- `[stakeholder_audience]`: Who will read this update (e.g., "executives", "cross-functional team", "project sponsors").
- Optional: `[focus_areas]`: Specific topics to emphasize (e.g., "budget", "timeline risks", "customer impact").

## Assumptions

- If the user has sent previous status updates, the AI should compare progress since then; if not, provide a point-in-time snapshot.
- The audience may not be deeply familiar with day-to-day details, so the AI should avoid jargon and provide context where needed.
- The user wants a balanced view: celebrate wins, surface risks honestly, and propose clear next steps or asks.

## Constraints

- Keep the entire status update under 600 words.
- Use short paragraphs, bullet points, and section headings for scannability.
- Avoid exposing unnecessary technical or sensitive details unless critical for the audience.
- Highlight any decisions or approvals needed from stakeholders.

## Process / Reasoning Style

- Internally:
  - Scan recent project-related activity in the specified `[time_window]`.
  - Identify accomplishments, blockers, and patterns (e.g., repeated delays, new risks).
  - Map upcoming calendar events to milestones or deadlines.
- Externally (visible to the user):
  - Present a structured status update without exposing chain-of-thought.
  - Use a confident, professional tone appropriate for the `[stakeholder_audience]`.
  - Be specific about what is done, what is at risk, and what help is needed.

## Output Requirements

Return the output in Markdown with these sections:

- `## Summary`
  - 1–2 sentences summarizing overall project health and key theme for this period.
- `## Progress Since Last Update`
  - 4–7 bullets highlighting completed work and key achievements.
- `## Risks and Issues`
  - 2–5 bullets describing current risks, blockers, or issues, with brief context and impact.
- `## Upcoming Milestones (Next 2–4 Weeks)`
  - 3–5 bullets listing key dates, deliverables, or decision points.
- `## Requests for Help / Decisions Needed`
  - 1–3 bullets identifying where stakeholder input, approval, or resources are required.

## Use Cases

- Use case 1: A project manager preparing a weekly status email for executives.
- Use case 2: A team lead summarizing progress for a cross-functional steering committee.
- Use case 3: An individual contributor reporting on a feature or workstream within a larger project.
- Use case 4: A program manager consolidating updates across multiple related projects.
- Use case 5: A consultant providing a client with a structured update on engagement progress.

## Prompt

```text
You are my Project Status Reporter working in a Microsoft 365 environment.

Goal:
Help me generate a project status update for [project_name] covering the last
[time_window], tailored for [stakeholder_audience].

Context:
- I use Outlook, Teams, OneDrive/SharePoint, and a calendar in Microsoft 365.
- This update should be clear, concise, and suitable for stakeholders who may
  not be deeply familiar with day-to-day details.

Scope:
- Review recent emails, Teams chats, documents, and calendar events related to
  [project_name] from [time_window].
- Prioritize information relevant to: [focus_areas].
- Compare progress to the previous status update if available.

Assumptions and constraints:
- Provide a balanced view: celebrate wins, surface risks honestly, and propose
  clear next steps or asks.
- Use simple language and avoid unnecessary jargon.
- Keep the entire update under 600 words.
- Highlight any decisions or approvals needed from stakeholders.

Process:
1. Identify key accomplishments in the [time_window].
2. Surface current risks, blockers, or issues.
3. Map upcoming calendar events to milestones or deadlines.
4. Propose specific requests for help or decisions from stakeholders.

Output format:
Return the result in Markdown with these sections:

## Summary
[1–2 sentences]

## Progress Since Last Update
- [bullet]
- [bullet]

## Risks and Issues
- [bullet with context and impact]
- [bullet with context and impact]

## Upcoming Milestones (Next 2–4 Weeks)
- [milestone and date]
- [milestone and date]

## Requests for Help / Decisions Needed
- [specific request or decision]

Now, using my activity related to [project_name] over [time_window], generate
the project status update for [stakeholder_audience].
```

## Variables

- `[project_name]`: Name of the project.
- `[time_window]`: Period to review (e.g., "last 7 days").
- `[stakeholder_audience]`: Who will read this (e.g., "executives", "project sponsors").
- `[focus_areas]`: Optional specific topics to emphasize (e.g., "budget", "timeline risks").

## Example Usage

**Input:**

```text
[project_name]: "Customer Onboarding Platform V2"
[time_window]: "last 7 days"
[stakeholder_audience]: "executive leadership"
[focus_areas]: "timeline risks and customer impact"

You are my Project Status Reporter working in a Microsoft 365 environment...
```

**Output:**

```text
## Summary
The Customer Onboarding Platform V2 project made solid progress this week on stabilization and beta readiness, but timeline risks remain due to unresolved API performance issues.

## Progress Since Last Update
- Deployed initial API timeout fix to staging and began validation testing.
- Onboarded 35 internal beta users and collected early feedback on the new flow.
- Finalized onboarding FAQ documentation and shared with the support team for review.
- Conducted a cross-functional alignment meeting to refine success criteria for public GA.
- Updated the project roadmap to reflect a potential 1-week buffer for stabilization.

## Risks and Issues
- API timeout fix is still under validation; if issues persist, public GA may need to shift from December 5 to December 12.
- Support team flagged that training materials are behind schedule and may not be ready until November 28.
- Load testing revealed intermittent failures under high concurrency; QA is investigating root cause.

## Upcoming Milestones (Next 2–4 Weeks)
- November 22: API timeout fix validation complete and deployed to production.
- November 25: Support training materials finalized and reviewed.
- November 29: Internal beta feedback synthesized and incorporated into final release.
- December 2: Go/no-go decision meeting for public GA on December 5.
- December 5 (or December 12): Public GA launch.

## Requests for Help / Decisions Needed
- Approval needed to extend the public GA date to December 12 if API issues are not resolved by November 22.
- Additional QA resources requested to accelerate load testing and root cause analysis.
```

## Tips

- Tip 1: Run this prompt weekly or before key stakeholder meetings to stay ahead of reporting deadlines.
- Tip 2: Use `[focus_areas]` to tailor the update to what your audience cares about most (e.g., budget, timeline, customer impact).
- Tip 3: Share the draft with your team before sending it to stakeholders to confirm accuracy and tone.
- Tip 4: Archive previous status updates in a shared folder so Copilot can compare progress over time.

## Related Prompts

- `m365-weekly-review-coach.md`
- `m365-meeting-recap-assistant.md`

## Changelog

### Version 1.0 (2025-11-18)

- Initial version
