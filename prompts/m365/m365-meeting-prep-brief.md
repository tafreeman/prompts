---
title: "M365 Meeting Prep Brief"
category: "business"
tags: ["m365", "copilot", "meetings", "preparation", "teams"]
author: "Your Name"
version: "1.0"
date: "2025-11-18"
difficulty: "beginner"
---

# M365 Meeting Prep Brief

## Description
This prompt helps an individual quickly prepare for an upcoming meeting using Microsoft 365 context. It generates a brief that includes meeting purpose, key talking points, questions to ask, and potential risks or sensitive topics based on the meeting invite, related emails, chats, and documents.

## Goal
Enable a user to walk into any meeting confident and well-prepared, with clear talking points and an understanding of context, even when preparation time is limited.

## Context
Assume the user works in Microsoft 365 with access to Outlook, Teams, OneDrive/SharePoint, and calendar. Meetings often reference prior discussions, documents, and email threads that the AI can surface to help the user prepare efficiently.

The AI can reference:
- The meeting invite (subject, attendees, agenda if available)
- Recent emails and Teams chats involving the attendees or meeting topic
- Documents shared or mentioned in relation to the meeting
- Calendar context (previous meetings with the same participants)

## Inputs
The user provides:
- `[meeting_title]`: Title or subject of the meeting.
- `[meeting_date]`: Date and time of the meeting.
- `[focus]`: Optional emphasis area (e.g., "budget review", "risk assessment", "customer feedback").
- `[time_window]`: How far back to look for relevant context (e.g., "last 2 weeks", "since last meeting").

## Assumptions
- If the meeting has a formal agenda, the AI should reference it; if not, infer purpose from title, attendees, and recent context.
- The AI should prioritize high-impact or decision-oriented topics.
- The user wants to be briefed on both opportunities (positive outcomes) and risks (sensitive topics or potential conflicts).

## Constraints
- Keep the entire brief under 600 words.
- Use bullet points and short paragraphs for scannability.
- Avoid exposing unnecessary sensitive details; summarize instead of quoting verbatim.
- Highlight any gaps in context where the user may need to gather more information before the meeting.

## Process / Reasoning Style
- Internally:
  - Review the meeting invite and identify attendees, agenda items, and stated purpose.
  - Scan recent emails, chats, and documents for relevant background.
  - Identify patterns: recurring themes, unresolved questions, recent decisions.
- Externally (visible to the user):
  - Present a structured brief without exposing chain-of-thought.
  - Use a supportive, coaching tone.
  - Flag topics that may require diplomatic handling or deeper preparation.

## Output Requirements
Return the output in Markdown with these sections:

- `## Meeting Overview`
  - 1–2 sentences summarizing meeting purpose and expected outcome.
- `## Key Context`
  - 3–5 bullets summarizing relevant background from emails, chats, documents, or prior meetings.
- `## Your Talking Points`
  - 3–5 bullets of topics you should cover or contribute.
- `## Questions to Ask`
  - 3–5 questions you should ask other participants to clarify, align, or uncover issues.
- `## Risks or Sensitive Topics`
  - 1–3 bullets flagging any areas requiring careful handling, or "None identified" if the context is straightforward.

## Use Cases
- Use case 1: A project manager preparing for a stakeholder sync with limited time.
- Use case 2: An engineer reviewing context before a design review or technical discussion.
- Use case 3: A consultant preparing for a client check-in using recent emails and shared documents.
- Use case 4: A team lead getting ready for a 1:1 with a direct report.
- Use case 5: A cross-functional team member preparing for a planning or retrospective meeting.

## Prompt

```
You are my Meeting Prep Assistant working in a Microsoft 365 environment.

Goal:
Help me prepare for my upcoming meeting: [meeting_title] on [meeting_date].

Context:
- I use Outlook, Teams, OneDrive/SharePoint, and a calendar in Microsoft 365.
- I want to walk into this meeting confident, with clear talking points and an
  understanding of any risks or sensitive topics.

Scope:
- Review the meeting invite (subject, attendees, agenda if available).
- Look at relevant emails, Teams chats, and documents from [time_window] involving
  the meeting attendees or related to the meeting topic.
- Prioritize information related to: [focus].

Assumptions and constraints:
- If the agenda is not explicit, infer the meeting purpose from the title, attendees,
  and recent context.
- Highlight both opportunities (positive outcomes) and risks (sensitive or contentious topics).
- Keep the entire brief under 600 words.
- Use bullets and short paragraphs for easy scanning.
- If context is incomplete, flag gaps so I can gather more information before the meeting.

Process:
1. Identify the meeting purpose and key attendees.
2. Surface relevant background from recent communications and documents.
3. Propose clear talking points I should cover.
4. Suggest questions I should ask to clarify, align, or uncover issues.
5. Flag any risks or sensitive topics requiring diplomatic handling.

Output format:
Return the result in Markdown with these sections:

## Meeting Overview
[1–2 sentences]

## Key Context
- [bullet]
- [bullet]

## Your Talking Points
- [bullet]
- [bullet]

## Questions to Ask
- [question]
- [question]

## Risks or Sensitive Topics
- [bullet, or "None identified"]

Now, using the context around [meeting_title] on [meeting_date], prepare my meeting brief.
```

## Variables
- `[meeting_title]`: Title or subject of the meeting.
- `[meeting_date]`: Date and time of the meeting (e.g., "November 20, 2025 at 2 PM").
- `[focus]`: Optional emphasis area (e.g., "budget review", "customer feedback").
- `[time_window]`: How far back to consider relevant context (e.g., "last 2 weeks").

## Example Usage

**Input:**
```
[meeting_title]: "Q4 Onboarding Roadmap Review"
[meeting_date]: "November 20, 2025 at 2 PM"
[focus]: "risk assessment and timeline feasibility"
[time_window]: "last 2 weeks"

You are my Meeting Prep Assistant working in a Microsoft 365 environment...
```

**Output:**
```
## Meeting Overview
This meeting is a review of the Q4 onboarding roadmap with product, engineering, and support stakeholders. The goal is to align on priorities, assess timeline feasibility, and identify risks before committing to a phased rollout.

## Key Context
- Product recently proposed a phased rollout approach with two waves: internal beta (mid-November) and public GA (early December).
- Engineering flagged potential delays due to unresolved API timeout issues that surfaced in recent incidents.
- Support raised concerns about readiness of documentation and training materials for the public launch.
- Last week's email thread highlighted tension between aggressive timelines and quality/stability goals.

## Your Talking Points
- Summarize current status of the API timeout fix and realistic deployment timeline.
- Advocate for a realistic buffer in the public GA date to allow for stabilization and support readiness.
- Propose clear success criteria for the internal beta phase before advancing to public GA.

## Questions to Ask
- What are the minimum requirements for declaring the internal beta phase successful?
- Does support have a firm date by which documentation and training must be finalized?
- Are we aligned on the acceptable level of risk for the public GA, or should we plan a more conservative rollout?

## Risks or Sensitive Topics
- Tension between product's aggressive timeline and engineering/support's concerns about readiness may surface; approach diplomatically.
- If the API fix timeline slips, the phased rollout plan may need significant revision; be prepared to propose alternatives.
```

## Tips
- Tip 1: Run this prompt 15–30 minutes before the meeting for a quick refresh even if you're generally familiar with the topic.
- Tip 2: Use `[focus]` to zoom in on a specific aspect (e.g., "budget", "risks", "decisions needed") when the meeting has multiple themes.
- Tip 3: After the meeting, pair this with `m365-meeting-recap-assistant.md` to capture decisions and actions.
- Tip 4: Share the "Your Talking Points" section with your manager or a peer if you want feedback before the meeting.

## Related Prompts
- `m365-meeting-recap-assistant.md`
- `m365-daily-standup-assistant.md`

## Changelog

### Version 1.0 (2025-11-18)
- Initial version
