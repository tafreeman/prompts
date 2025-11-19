---
title: "M365 Email Triage Helper"
category: "business"
tags: ["m365", "copilot", "email", "outlook", "productivity"]
author: "Your Name"
version: "1.0"
date: "2025-11-18"
difficulty: "beginner"
platform: "Microsoft 365 Copilot"
---

# M365 Email Triage Helper

## Description

This prompt helps an individual quickly triage their inbox in Outlook using Copilot. It groups important emails into action-oriented categories and drafts short replies where appropriate.

## Goal

Reduce inbox overwhelm by organizing recent emails into clear categories and providing ready-to-send response drafts for high-priority messages.

## Context

Assume the user primarily works in Outlook as part of Microsoft 365. They receive many emails of mixed importance and need help deciding what to respond to now, what can wait, and what is informational only.

The AI can:

- Look at emails received within a specified `[time_window]`.
- Prioritize emails based on flags, sender importance, subject, and content.
- Draft replies that match the user's desired tone.

## Inputs

The user provides:

- `[time_window]`: Period to consider (e.g., "today", "last 24 hours", "since Monday").
- `[max_urgent]`: Maximum number of "respond today" emails to highlight.
- `[tone]`: Desired tone for replies (e.g., "professional and concise", "friendly but direct").
- Optional: `[exclude_senders]`: List of senders or domains to ignore.

## Assumptions

- Flagged or replied-to emails may already have partial attention; the AI should treat them appropriately (e.g., deprioritize already-resolved threads).
- Not every email needs a drafted response; drafts are most useful for high-impact or time-sensitive messages.
- The user prefers short, to-the-point replies that can be easily edited before sending.

## Constraints

- For each email that needs a response, draft a reply no longer than 150 words.
- Group emails into three categories:
  - "Need response today"
  - "Need response this week"
  - "FYI / no response needed"
- Limit "Need response today" to `[max_urgent]` items.
- Do not include confidential details not already in the email content.

## Process / Reasoning Style

- Internally:
  - Evaluate importance based on sender, subject, and context.
  - Detect time-sensitive or action-requesting emails.
  - Group similar threads where helpful.
- Externally (visible to the user):
  - Present a simple inbox summary with categories.
  - Provide reply drafts only for "Need response today" items.
  - Avoid showing chain-of-thought; present final groupings and drafts.

## Output Requirements

Return the output in Markdown with:

- `## Inbox Summary`
  - Short paragraph summarizing volume and overall theme.
- `## Need Response Today`
  - For each email: subject, sender (role only if appropriate), and a short explanation.
  - A draft reply block.
- `## Need Response This Week`
  - Bulleted list with subject and what is needed.
- `## FYI / No Response Needed`
  - Bulleted list of informational emails.

## Use Cases

- Use case 1: Start of the day triage for a busy manager.
- Use case 2: After returning from time off with a large backlog of emails.
- Use case 3: Afternoon "clean-up" session to stay on top of communications.
- Use case 4: End-of-week sweep to ensure no important emails are left unattended.
- Use case 5: Triage a specific project-related inbox folder.

## Prompt

```text
You are my Email Triage Helper working in Microsoft 365 Outlook.

Goal:
Help me quickly triage my inbox for the last [time_window], grouping emails
by urgency and drafting short replies for the most critical ones.

Context:
- I receive a mix of high-priority and low-priority emails.
- I want to focus on what needs my attention today versus later this week.
- I prefer short, clear emails that get to the point.

Scope:
Look at emails in my inbox from [time_window].
- Prioritize messages that:
  - Come from key stakeholders or my direct manager.
  - Contain clear requests, deadlines, or escalations.
- Exclude senders or domains listed in [exclude_senders], if any.

Assumptions and constraints:
- Group emails into:
  - "Need response today"
  - "Need response this week"
  - "FYI / no response needed"
- Limit the "Need response today" group to at most [max_urgent] emails.
- Draft replies only for the "Need response today" emails.
- Use a [tone] tone for replies.
- Keep each drafted reply under 150 words.

Process:
1. Analyze emails from [time_window] and assess urgency and importance.
2. Group emails into the three categories.
3. For each "Need response today" email:
   - Summarize what is needed.
   - Draft a concise reply.
4. Summarize the overall state of my inbox.

Output format:
Return the result in Markdown:

## Inbox Summary
[short paragraph]

## Need Response Today
1. **Subject:** [subject]
   - Why it matters: [one-line explanation]
   - Draft reply:
   ```

   [reply text]

   ```text

## Need Response This Week
- **Subject:** [subject] — [what is needed]
- **Subject:** [subject] — [what is needed]

## FYI / No Response Needed
- **Subject:** [subject]
- **Subject:** [subject]

Now, using emails from [time_window], triage my inbox, group the emails, and
provide reply drafts as specified.
```

## Variables

- `[time_window]`: Time range of emails to analyze.
- `[max_urgent]`: Maximum number of "today" emails to highlight.
- `[tone]`: Reply tone (e.g., "professional and concise").
- `[exclude_senders]`: Optional list of senders or domains to ignore.

## Example Usage

**Input:**

```text
[time_window]: "last 24 hours"
[max_urgent]: "5"
[tone]: "professional and concise"
[exclude_senders]: "newsletters@company.com; noreply@system.com"

You are my Email Triage Helper working in Microsoft 365 Outlook...
```

**Output:**

```text
## Inbox Summary
You received 32 emails in the last 24 hours. Five require same-day attention,
seven can be handled later this week, and the rest are informational.

## Need Response Today
1. **Subject:** Customer escalation: onboarding delay
   - Why it matters: High-priority customer escalation with a requested update today.
   - Draft reply:
   ```

   Hi [Name],

   Thanks for raising this. I'm reviewing the onboarding delay with the
   engineering team and will share a concrete update by [time].

   In the meantime, please let the customer know we're actively investigating
   and treating this as a priority.

   Best regards,
   [Your Name]

   ```text

## Need Response This Week
- **Subject:** Q4 planning deck review — Provide feedback on slides by Thursday.
- **Subject:** Team offsite dates — Confirm your availability for the proposed dates.

## FYI / No Response Needed
- **Subject:** Weekly engineering newsletter
- **Subject:** System maintenance notification for Saturday night
```

## Tips

- Tip 1: Run this at the start and end of your day to keep your inbox manageable.
- Tip 2: Adjust `[max_urgent]` when your schedule is packed so you don't overcommit.
- Tip 3: Ask Copilot to "shorten the reply further" for busy recipients.
- Tip 4: Use folder or search filters in Outlook along with this prompt for project-specific triage.

## Related Prompts

- `m365-daily-standup-assistant.md`
- `m365-weekly-review-coach.md`

## Changelog

### Version 1.0 (2025-11-18)

- Initial version
