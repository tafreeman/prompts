---
title: "M365 Meeting Recap Assistant"
category: "business"
tags: ["m365", "copilot", "meetings", "recap", "teams", "action-items"]
author: "Your Name"
version: "1.0"
date: "2025-11-18"
difficulty: "beginner"
---

# M365 Meeting Recap Assistant

## Description
This prompt helps an individual quickly turn a meeting transcript or notes into a structured summary with decisions, action items, and follow-ups. It leverages Microsoft 365 context (Teams meeting transcripts, chat, and shared documents) to produce actionable outputs.

## Goal
Enable a user to capture and communicate meeting outcomes clearly and efficiently, ensuring nothing important is missed and follow-ups are tracked.

## Context
Assume the user works in Microsoft 365 with access to Teams, Outlook, and OneDrive/SharePoint. Meetings often generate transcripts, chat messages, and references to documents that the AI can synthesize into a cohesive summary.

The AI can reference:
- Meeting transcript (if available)
- Meeting chat messages
- Documents or links shared during the meeting
- Calendar invite and attendee list

## Inputs
The user provides:
- `[priority_scheme]`: How to categorize action items (e.g., "High/Medium/Low" or "Urgent/Important/Nice-to-have").
- `[due_date_horizon]`: Suggested timeframe for action items (e.g., "within 2 weeks", "by end of quarter").
- Optional: `[focus_topics]`: Specific topics to emphasize in the recap (e.g., "risks", "budget", "customer impact").

## Assumptions
- If a transcript is available, the AI should use it as the primary source; if not, it should work from chat messages and any notes the user provides.
- Not every discussion point needs to be captured—focus on decisions, action items, and unresolved questions.
- The user prefers action items with clear owners and realistic due dates, even if those are suggestions that need confirmation.

## Constraints
- Keep the entire recap under 800 words.
- Use bullet points, tables, and short paragraphs for scannability.
- Avoid quoting verbatim from the transcript unless it's a critical decision statement; summarize instead.
- Action items should be specific and actionable, not vague aspirations.

## Process / Reasoning Style
- Internally:
  - Parse the transcript and chat for key themes, decisions, and commitments.
  - Identify who committed to what, even if not stated explicitly (infer from context).
  - Group related action items to avoid redundancy.
- Externally (visible to the user):
  - Present a clean, structured summary without exposing chain-of-thought.
  - Use a neutral, professional tone.
  - Provide a table for action items for easy copy/paste into task trackers.

## Output Requirements
Return the output in Markdown with these sections:

- `## Meeting Summary`
  - 1–2 short paragraphs summarizing the overall purpose and outcome of the meeting.
- `## Key Decisions`
  - 3–7 bullets listing decisions made, each with a brief explanation if needed.
- `## Action Items`
  - A table with columns: Owner, Action, Suggested Due Date, Priority.
- `## Open Questions / Follow-ups`
  - 2–5 bullets for unresolved issues or topics that need follow-up discussions.

## Use Cases
- Use case 1: A project manager capturing outcomes from a sprint planning or retrospective meeting.
- Use case 2: A team lead summarizing a stakeholder sync for distribution to attendees and non-attendees.
- Use case 3: An engineer documenting decisions from a design review or architecture discussion.
- Use case 4: A consultant recapping a client meeting and preparing follow-up tasks.
- Use case 5: An operations lead capturing action items from an incident review or post-mortem.

## Prompt

```
You are my Meeting Recap Assistant working in a Microsoft 365 environment.

Goal:
Help me turn this meeting into a structured summary with decisions, action items,
and follow-ups, based on the transcript, chat, and shared documents.

Context:
- I use Teams, Outlook, and OneDrive/SharePoint in Microsoft 365.
- I need a clear, actionable recap that I can share with attendees and use to
  track follow-ups.

Scope:
- Use the meeting transcript (if available), meeting chat, and any documents or
  links shared during the meeting.
- Focus on:
  - Decisions made
  - Action items and who owns them
  - Unresolved questions or topics requiring follow-up
- Emphasize these topics if relevant: [focus_topics].

Assumptions and constraints:
- If no transcript is available, work from chat messages and any notes I provide.
- Focus on decisions and actions, not every discussion point.
- For action items:
  - Propose an owner (even if inferred from context).
  - Suggest a due date within [due_date_horizon].
  - Assign a priority using [priority_scheme].
- Keep the recap under 800 words.
- Use tables and bullets for easy scanning.

Process:
1. Parse the transcript and chat for key themes, decisions, and commitments.
2. Identify action items and their owners (infer if not explicitly stated).
3. Group related actions to avoid redundancy.
4. List unresolved questions or follow-up topics.

Output format:
Return the result in Markdown with these sections:

## Meeting Summary
[1–2 short paragraphs]

## Key Decisions
- [decision with brief explanation]
- [decision with brief explanation]

## Action Items
| Owner | Action | Suggested Due Date | Priority |
|-------|--------|-------------------|----------|
| [name] | [action] | [date] | [priority] |
| [name] | [action] | [date] | [priority] |

## Open Questions / Follow-ups
- [unresolved question or topic]
- [unresolved question or topic]

Now, using the meeting transcript, chat, and context, generate the meeting recap.
```

## Variables
- `[priority_scheme]`: How to categorize action items (e.g., "High/Medium/Low").
- `[due_date_horizon]`: Suggested timeframe for action items (e.g., "within 2 weeks").
- `[focus_topics]`: Optional specific topics to emphasize (e.g., "risks", "budget").

## Example Usage

**Input:**
```
[priority_scheme]: "High/Medium/Low"
[due_date_horizon]: "within 2 weeks"
[focus_topics]: "timeline risks and customer impact"

You are my Meeting Recap Assistant working in a Microsoft 365 environment...
```

**Output:**
```
## Meeting Summary
This meeting reviewed the Q4 onboarding roadmap and assessed timeline feasibility for the phased rollout. The team aligned on success criteria for the internal beta, discussed risks related to API stability, and identified several action items to de-risk the public GA launch.

## Key Decisions
- Proceed with the phased rollout: internal beta starting November 18, public GA targeting December 5.
- Internal beta success criteria: zero critical incidents, support team confirms documentation readiness, and at least 50 internal users onboarded without major issues.
- If API timeout fix is not deployed by November 22, push public GA to December 12 to allow additional stabilization time.

## Action Items
| Owner | Action | Suggested Due Date | Priority |
|-------|--------|-------------------|----------|
| Alex (Engineering) | Deploy API timeout fix and confirm stability in staging | Nov 22 | High |
| Jordan (Product) | Finalize internal beta communication plan and recruit 50 beta users | Nov 18 | High |
| Taylor (Support) | Complete onboarding FAQ and training materials review | Nov 25 | Medium |
| Morgan (QA) | Run end-to-end onboarding test scenarios with production-like load | Nov 21 | High |
| Casey (PM) | Schedule a go/no-go decision meeting for public GA on December 2 | Nov 29 | Medium |

## Open Questions / Follow-ups
- What is the fallback plan if the internal beta reveals a critical issue after November 22?
- Should we prepare a public communication in case the GA date shifts to December 12?
- Do we need additional QA resources to accelerate load testing?
```

## Tips
- Tip 1: Run this prompt immediately after the meeting while the context is fresh.
- Tip 2: Share the recap with attendees and ask them to confirm action item ownership and due dates.
- Tip 3: Use the "Action Items" table directly in your task tracker (Planner, Jira, etc.) by copying and pasting.
- Tip 4: Pair this with `m365-meeting-prep-brief.md` for full meeting lifecycle coverage (prep → meeting → recap).

## Related Prompts
- `m365-meeting-prep-brief.md`
- `m365-project-status-reporter.md`

## Changelog

### Version 1.0 (2025-11-18)
- Initial version
