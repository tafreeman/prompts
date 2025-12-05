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
```sql
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
**Output:**

```markdown
# Meeting Summary: Q1 2025 Product Roadmap Review

**Date**: November 29, 2024 | 2:00 PM - 3:30 PM  
**Attendees**: Sarah Chen (VP Product), Marcus Thompson (Eng Lead), Priya Sharma (Design Lead), Jordan Lee (PM), David Miller (CEO - partial)

---

## Executive Summary

The team finalized Q1 2025 priorities, selecting **API v2 for Enterprise** as the top focus due to pending enterprise deals. Mobile app redesign was deprioritized to Q2 despite strong user research supporting its importance. Engineering capacity concerns were addressed with a commitment to explore contractor options and allocate 20% of sprint capacity to tech debt.

---

## Key Decisions Made

| # | Decision | Rationale | Approved By |
| :--- |----------|-----------|-------------|
| 1 | **API v2 is Q1 priority** | 3 enterprise deals ($[X]M ARR) contingent on delivery | David (CEO) |
| 2 | **Mobile redesign delayed to Q2** | Insufficient resources for parallel work; enterprise revenue takes precedence | Sarah/David |
| 3 | **20% sprint capacity for tech debt** | Address growing backlog and team morale concerns | Sarah |
| 4 | **Explore contractors for API v2** | Engineering understaffed by 2 headcount for current timeline | Sarah |

---

## Discussion Highlights

### API v2 vs. Mobile Debate
- **For Mobile (Priya)**: User research shows 60% of users access via mobile; current experience is poor
- **For Mobile (Jordan's counter)**: Mobile users have lower conversion rates than desktop
- **For API v2 (David)**: Enterprise deals worth $[X]M are contingent on API v2; immediate revenue impact
- **Resolution**: Short-term revenue needs outweighed mobile improvements; mobile remains high priority for Q2

### Engineering Capacity
- Marcus flagged API v2 requires 2 additional engineers to hit timeline
- Options discussed: (1) Hire contractors, (2) Delay mobile further, (3) Extend API timeline
- Consensus: Explore contractor path first; revisit if candidates aren't available by Dec 13

### Tech Debt Concerns
- Marcus raised team morale issues due to growing tech debt backlog
- Sarah committed to 20% sprint allocation (roughly 2 days/sprint/engineer)
- Will track tech debt completion as an OKR metric

### Parking Lot: Analytics Dashboard
- Jordan advocated for analytics dashboard; acknowledged as important but not urgent
- Will revisit in Q2 planning cycle

---

## Action Items

| Task | Owner | Due Date | Priority |
|------|-------|----------|----------|
| Explore contractor options with HR and present candidates | Sarah | Dec 6 | 🔴 High |
| Update mobile designs for Q2 timeline, share revised mockups | Priya | Dec 20 | 🟡 Medium |
| Draft API v2 sprint plan assuming current + 2 contractor headcount | Marcus | Dec 10 | 🔴 High |
| Define tech debt allocation process and tracking | Marcus | Dec 13 | 🟡 Medium |
| Share enterprise deal pipeline details for API v2 scoping | Jordan | Dec 4 | 🔴 High |
| Schedule Q2 planning kickoff meeting | Sarah | Dec 13 | 🟢 Low |

---

## Parking Lot (Deferred Topics)

- **Analytics Dashboard**: Important but not urgent. Revisit in Q2 planning.
- **Long-term mobile strategy**: Needs dedicated session once Q1 plan is solid.
- **Engineering hiring plan**: Beyond contractors, should we open full-time reqs?

---

## Next Steps

**Next Meeting**: December 13, 2024 @ 2:00 PM  
**Purpose**: Review contractor candidates + finalize Q1 sprint plans

**Pre-work for Dec 13**:
- Sarah: Contractor candidate shortlist
- Marcus: API v2 sprint breakdown with resource scenarios
- Jordan: Enterprise deal requirements document

---

## Distribution

**Sent to**: All attendees + Emily (Engineering Manager, FYI)  
**Confidentiality**: Internal only - contains revenue targets

---

*Summary prepared by [Your Name] | Questions? Reach out in #product-roadmap Slack channel*
```text
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
