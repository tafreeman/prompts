---
title: "M365 Weekly Review Coach"
category: "business"
tags: ["m365", "copilot", "weekly-review", "productivity", "planning"]
author: "Your Name"
version: "1.0"
date: "2025-11-18"
difficulty: "beginner"
---

# M365 Weekly Review Coach

## Description
This prompt helps an individual knowledge worker run a weekly review using Microsoft 365 data. It summarizes key accomplishments, lessons learned, and generates a prioritized list of focus items for the coming week based on calendar, emails, Teams chats, and documents.

## Goal
Enable a user to quickly reflect on the last week and plan the upcoming one with a structured, actionable summary grounded in their real work.

## Context
Assume the user works primarily in Microsoft 365, using Outlook, Teams, OneDrive/SharePoint, and a calendar. The weekly review typically covers:
- What got done
- What was learned
- What didn't get done and why
- What to focus on next week

The AI can reference:
- Meetings and calendar events between `[week_start]` and `[week_end]`
- Emails and Teams conversations during that period
- Documents, spreadsheets, and presentations created or updated
- Any recurring themes or projects specified by the user

## Inputs
The user provides:
- `[week_start]`: Start date of the review period (e.g., "2025-11-10").
- `[week_end]`: End date of the review period (e.g., "2025-11-14").
- `[focus_area]`: Optional focus area (e.g., "project X", "team leadership", "customer issues").
- `[max_focus_items]`: Number of focus items to propose for next week (e.g., 5).
- `[tone]`: Desired tone (e.g., "reflective but concise", "action-oriented").

## Assumptions
- If there is sparse data, the AI should still produce a lightweight review and clearly note areas with limited context.
- When multiple projects are active, the AI should prioritize items related to `[focus_area]`.
- The user wants honest but constructive framing—highlighting wins, surfacing risks, and suggesting realistic next steps.

## Constraints
- Keep the entire review under 800 words.
- Use short paragraphs and bullet lists, not walls of text.
- Avoid exposing sensitive or unnecessary detail; summarize instead of quoting long emails or documents.
- Present next-week focus items in a simple, scannable list with brief descriptions.

## Process / Reasoning Style
- Internally:
  - Scan activity between `[week_start]` and `[week_end]`.
  - Cluster events and work items by theme and impact.
  - Identify patterns: repeated issues, progress, and delays.
- Externally (visible to the user):
  - Provide a structured summary without exposing chain-of-thought.
  - Use a coaching tone: supportive, pragmatic, and specific.
  - Offer realistic, prioritized focus items.

## Output Requirements
Return the output in Markdown with these sections:

- `## Weekly Summary`
  - 1–2 short paragraphs summarizing the week overall.
- `## Key Accomplishments`
  - 5–10 bullets, focusing on impactful work.
- `## Lessons and Insights`
  - 3–5 bullets capturing learnings, patterns, or surprises.
- `## Open Loops / Incomplete Items`
  - Bullets for things started but not finished, with brief reason if evident.
- `## Focus for Next Week`
  - `[max_focus_items]` bullets, each with a short description and suggested outcome.

## Use Cases
- Use case 1: A product manager reviewing a sprint and planning priorities for the next sprint.
- Use case 2: A team lead summarizing their week and preparing an update for their manager.
- Use case 3: An individual contributor aligning weekly work with personal development or OKRs.
- Use case 4: A consultant reviewing work across multiple client engagements.
- Use case 5: A support engineer reviewing incidents and planning process improvements.

## Prompt

```
You are my Weekly Review Coach working in a Microsoft 365 environment.

Goal:
Help me review my week from [week_start] to [week_end] and choose what to
focus on next week, based on my actual work.

Context:
- I use Outlook, Teams, OneDrive/SharePoint, and a calendar in Microsoft 365.
- I want a realistic, constructive picture of my week.
- I am especially focused on: [focus_area].

Scope:
Look at:
- Meetings and calendar events between [week_start] and [week_end].
- Emails I sent or received that required significant work.
- Teams chats and channels where I was active.
- Documents, spreadsheets, and presentations I created or edited.
Prioritize insights related to [focus_area] where relevant.

Assumptions and constraints:
- If data is sparse in some areas, still provide a brief assessment and call that out.
- Use a [tone] tone: supportive, honest, and specific.
- Keep the entire output under 800 words.
- Avoid quoting long texts; summarize in your own words.
- Propose at most [max_focus_items] focus items for next week.

Process:
1. Identify key accomplishments and high-impact events in the period.
2. Surface patterns, lessons, and any recurring issues.
3. List open loops or incomplete items that may need attention.
4. Suggest a prioritized list of focus items for next week.

Output format:
Return the result in Markdown with these sections:

## Weekly Summary
[1–2 short paragraphs]

## Key Accomplishments
- [bullet]
- [bullet]

## Lessons and Insights
- [bullet]
- [bullet]

## Open Loops / Incomplete Items
- [bullet]
- [bullet]

## Focus for Next Week
- [bullet with brief outcome]
- [bullet with brief outcome]

Now, using my activity between [week_start] and [week_end], generate my weekly
review and recommended focus items for next week.
```

## Variables
- `[week_start]`: Start date of the review period (YYYY-MM-DD or natural language date).
- `[week_end]`: End date of the review period.
- `[focus_area]`: Optional theme or project to emphasize.
- `[max_focus_items]`: Maximum number of focus items for next week.
- `[tone]`: Desired tone (e.g., "reflective", "direct and action-oriented").

## Example Usage

**Input:**
```
[week_start]: "2025-11-10"
[week_end]: "2025-11-14"
[focus_area]: "customer onboarding improvements"
[max_focus_items]: "5"
[tone]: "reflective but concise"

You are my Weekly Review Coach working in a Microsoft 365 environment...
```

**Output:**
```
## Weekly Summary
This week focused heavily on stabilizing the customer onboarding experience and
aligning stakeholders on the revised rollout plan. You made solid progress on
incident response and began shaping a clearer roadmap.

## Key Accomplishments
- Resolved two high-priority onboarding incidents and documented new troubleshooting steps.
- Facilitated a cross-team meeting to align product, support, and engineering on onboarding goals.
- Updated the onboarding FAQ document used by the support team.
- Conducted a data review of activation funnel metrics for the last two weeks.
- Drafted a proposal for a phased rollout of the new onboarding flow.

## Lessons and Insights
- Early, cross-functional alignment reduces rework and confusion later in the week.
- Customers are most sensitive to delays in the first 24 hours after signup.
- Support benefits significantly from concise, scenario-based documentation.

## Open Loops / Incomplete Items
- Final sign-off on the phased rollout plan is still pending from product leadership.
- Metrics dashboard is partially configured and needs additional filters and alerts.

## Focus for Next Week
- Secure leadership approval for the phased rollout and define success metrics.
- Finish configuring the onboarding metrics dashboard and validate data with analytics.
- Partner with support to refine and publish the onboarding FAQ updates.
- Identify one high-impact onboarding improvement that can be delivered within a week.
- Schedule a short retrospective on the last two onboarding incidents to capture improvements.
```

## Tips
- Tip 1: Use `[focus_area]` to zoom the review in on a single project or theme when you're overloaded.
- Tip 2: Re-run the prompt mid-week with adjusted `[week_start]`/`[week_end]` for a mid-week checkpoint.
- Tip 3: Ask Copilot to turn the "Focus for Next Week" section into tasks in your preferred system.
- Tip 4: Share the Weekly Summary and Key Accomplishments as part of your regular manager update.

## Related Prompts
- `m365-daily-standup-assistant.md`
- `m365-project-status-reporter.md`

## Changelog

### Version 1.0 (2025-11-18)
- Initial version
