---
name: M365 Meeting Recap Assistant
description: Transforms meeting transcripts into structured summaries with decisions and action items.
type: how_to
---

# M365 Meeting Recap Assistant

## Description

Turn meeting transcripts or notes into structured recaps with decisions, action items, and follow-ups. Perfect for distribution to attendees and stakeholders who couldn't attend.

## Prompt

You are a Meeting Documentation Assistant using Microsoft 365 Copilot.

Create a meeting recap from the transcript/notes below.

### Meeting Context
**Meeting Title**: [meeting_title]
**Date**: [date]
**Attendees**: [attendees]

**Transcript/Notes**:
[transcript]

### Output Format
1. **Meeting Summary**: 2-3 sentence overview.
2. **Key Decisions**: What was decided.
3. **Action Items Table**:
   | Action | Owner | Due Date |
   |--------|-------|----------|
4. **Open Questions**: Items needing follow-up.
5. **Next Meeting**: If scheduled.

## Variables

- `[meeting_title]`: E.g., "Sprint Planning", "Stakeholder Sync".
- `[date]`: Meeting date.
- `[attendees]`: Key participants.
- `[transcript]`: Meeting transcript or notes.

## Example

**Input**:
Meeting: Project Alpha Kickoff
Date: 2026-01-20
Attendees: Sarah (PM), Mike (Dev Lead), Lisa (Design)
Notes: Discussed timeline... agreed to 3-month MVP... Mike to set up repo... Lisa needs brand guidelines...

**Response**:
### Meeting Summary
Project Alpha kickoff established a 3-month MVP timeline with development starting February 1st. Key dependencies identified around brand guidelines and cloud infrastructure setup.

### Key Decisions
- MVP scope: Core features only, no integrations
- Launch target: April 30, 2026
- Tech stack: React + Node.js

### Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| Set up GitHub repo | Mike | Jan 22 |
| Share brand guidelines | Lisa | Jan 24 |
| Draft project plan | Sarah | Jan 25 |

### Next Meeting
Weekly sync: Mondays 10am starting Jan 27
