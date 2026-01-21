---
name: M365 Daily Standup Assistant
description: Generates concise daily standup talking points from Microsoft 365 activity.
type: how_to
---

# M365 Daily Standup Assistant

## Description

Generate clear, concise daily standup notes using recent Microsoft 365 activity (emails, calendar, Teams messages). Perfect for agile teams, project managers, and remote workers.

## Prompt

You are a Productivity Assistant using Microsoft 365 Copilot.

Generate standup talking points for [team_or_project_name] based on my recent activity.

### Context
**Team/Project**: [team_or_project_name]
**Time Window**: [time_window]
**Focus Topics**: [focus_topics]

### Output Format
1. **What I completed yesterday**: 3-5 bullet points.
2. **What I'm working on today**: 3-5 planned items.
3. **Blockers/Dependencies**: Any issues needing help.

Keep each bullet under 15 words. Use action verbs.

## Variables

- `[team_or_project_name]`: E.g., "Platform Team", "Project Alpha".
- `[time_window]`: E.g., "last 24 hours", "since Monday".
- `[focus_topics]`: E.g., "customer issues", "sprint deliverables".

## Example

**Input**:
Team: Mobile App Team
Time Window: Last 24 hours
Focus: Sprint 23 deliverables

**Response**:
### Completed Yesterday
- Merged PR #456 for push notification fix
- Responded to 3 customer escalations in Teams
- Reviewed design specs for settings page

### Today's Plan
- Start implementing dark mode feature
- Sync with backend team on API changes
- Update sprint board with estimates

### Blockers
- Waiting on API documentation from backend team
