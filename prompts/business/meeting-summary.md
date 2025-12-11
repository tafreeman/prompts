---
title: "Meeting Summary Generator"
shortTitle: "Meeting Summary"
intro: "Generate clear, actionable meeting summaries with key decisions, action items, and follow-up tasks."
type: "how_to"
difficulty: "beginner"
audience:
  - "project-manager"
  - "business-analyst"
platforms:
  - "github-copilot"
  - "claude"
  - "chatgpt"
topics:
  - "productivity"
  - "communication"
  - "meetings"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Meeting Summary Generator

---

## Description

Transform meeting notes or transcripts into clear, actionable summaries. Captures key decisions, assigns action items with owners and due dates, and highlights important discussion points.

---

## Use Cases

- Summarizing team meetings and standups
- Documenting 1:1 conversations with direct reports
- Creating executive briefings from long meetings
- Sharing meeting outcomes with absent stakeholders
- Tracking action items across recurring meetings

---

## Prompt

```text
You are an expert at synthesizing meeting discussions into clear, actionable summaries.

Create a meeting summary from:

**Meeting Type**: [meeting_type]
**Date/Time**: [datetime]
**Attendees**: [attendees]
**Meeting Purpose**: [purpose]
**Notes/Transcript**: [notes]

Generate:

1. **Executive Summary** (2-3 sentences)
   - What was decided
   - Why it matters

2. **Key Decisions Made**
   - Decision + rationale
   - Who made/approved it

3. **Discussion Highlights**
   - Main topics covered
   - Different viewpoints expressed
   - Open questions raised

4. **Action Items** (table format)
   - Task description
   - Owner
   - Due date
   - Priority

5. **Parking Lot**
   - Topics deferred for later
   - Items needing more research

6. **Next Steps**
   - Follow-up meeting (if any)
   - Pre-work for next meeting

Keep it concise. Focus on decisions and actions, not who said what.
```text

---

## Variables

- `[meeting_type]`: Type of meeting (e.g., "Weekly team sync", "Project kickoff", "1:1")
- `[datetime]`: When the meeting occurred
- `[attendees]`: Who was present (names and roles)
- `[purpose]`: Meeting objective or agenda
- `[notes]`: Raw notes, transcript, or key points from the meeting

---

## Example Usage

**Input:**

```text
Meeting Type: Product Roadmap Review
Date/Time: November 29, 2024, 2:00 PM - 3:30 PM
Attendees: Sarah (VP Product), Marcus (Eng Lead), Priya (Design Lead), Jordan (PM), David (CEO - partial)
Meeting Purpose: Finalize Q1 2025 product priorities and resource allocation

Notes:
- David kicked off with company context: Q4 revenue 15% below target, need to focus on features that drive expansion revenue
- Sarah presented 3 options for Q1 focus: (A) New analytics dashboard, (B) API v2 for enterprise, (C) Mobile app redesign
- Marcus raised concern that API v2 is understaffed - would need 2 more engineers or slip timeline
- Long discussion about mobile app - Priya showed user research, 60% of users access on mobile but current experience is poor. Jordan pushed back that mobile users don't convert as well.
- David said he wants API v2 because 3 enterprise deals are contingent on it. Willing to delay mobile.
- Debate about whether to hire contractors for API work vs. delay mobile
- Decision: Go with API v2 as top priority. Mobile pushed to Q2. Sarah to explore contractor options with HR by Dec 6.
- Jordan asked about the analytics dashboard - agreed it's important but not urgent. Will revisit in Q2 planning.
- Marcus mentioned tech debt backlog is growing - team morale concern. Sarah agreed to allocate 20% of sprint capacity to tech debt.
- Next meeting: Dec 13 to review contractor candidates and finalize sprint plans
- Priya needs to update mobile designs based on delayed timeline - will share revised mockups by Dec 20
```text

---

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
