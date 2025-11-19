---
title: "M365 Manager Sync Planner"
description: "Generates a structured agenda for 1:1 meetings with your manager, highlighting achievements, blockers, and career development topics."
category: "business"
tags: ["m365", "management", "career", "productivity", "meeting-prep"]
author: "GitHub Copilot"
version: "1.0"
date: "2025-11-18"
difficulty: "Beginner"
platform: "Microsoft 365 Copilot"
---

## Description

This prompt helps employees prepare for effective one-on-one meetings with their managers. It takes raw notes about the week's work, challenges, and future goals, and organizes them into a professional, time-boxed agenda that ensures all critical topics are covered.

## Goal

To create a concise, prioritized agenda for a manager 1:1 that demonstrates progress, clearly articulates help needed, and advances career discussions.

## Inputs

- **Recent Wins**: [recent_wins]
- **Current Blockers**: [current_blockers]
- **Decisions Needed**: [decisions_needed]
- **Career/Growth Topic**: [career_topic]
- **Meeting Duration**: [meeting_duration]

## Prompt

You are an expert career coach and executive assistant. I need you to prepare a structured agenda for my upcoming 1:1 meeting with my manager.

Here is the context for the meeting:

- **Recent Wins/Completed Work**: [recent_wins]
- **Current Blockers/Challenges**: [current_blockers]
- **Decisions/Approvals Needed**: [decisions_needed]
- **Career Development Topic**: [career_topic]
- **Meeting Duration**: [meeting_duration]

Please generate a meeting agenda that:

1. Allocates time efficiently based on the [meeting_duration].
2. Starts with a "Wins" section to set a positive tone.
3. Clearly frames the "Blockers" and "Decisions" as actionable items for the manager.
4. Reserves time for the "Career Development" topic.
5. Includes a section for "Manager's Topics" to ensure two-way communication.

Output the agenda in a clean Markdown format suitable for pasting into a Teams chat, Outlook invite, or OneNote page.

## Variables

- `[recent_wins]`: List of tasks completed or milestones achieved since the last meeting.
- `[current_blockers]`: Issues preventing progress where manager intervention is needed.
- `[decisions_needed]`: Specific items requiring approval or guidance.
- `[career_topic]`: A specific area of professional growth or feedback to discuss.
- `[meeting_duration]`: Length of the meeting (e.g., 30 minutes, 1 hour).

## Example Usage

**Input:**

- `[recent_wins]`: "Shipped the Q4 report, fixed the login bug, onboarded the new intern."
- `[current_blockers]`: "Waiting for legal review on the vendor contract."
- `[decisions_needed]`: "Need budget approval for the team lunch."
- `[career_topic]`: "Discuss potential for leading the next sprint."
- `[meeting_duration]`: "30 minutes"

**Output:**

### 1:1 Agenda (30 Mins)

**1. Wins & Progress (5 mins)**

- Shipped Q4 Report.
- Resolved critical login bug.
- Completed onboarding for new intern.

**2. Blockers & Support (10 mins)**

- **Legal Review**: Blocked on vendor contract. *Action: Can you escalate to Legal?*
- **Budget**: Need approval for team lunch.

**3. Career Development (10 mins)**

- Topic: Leading the upcoming sprint.
  - *Discussion: Readiness and expectations.*

**4. Manager's Topics (5 mins)**

- [Open for your items]

## Tips

- Use this prompt in **OneNote** or **Loop** to maintain a running document of your 1:1s.
- Be specific about what you need from your manager in the "Blockers" section (e.g., "I need you to email X" vs "X is slow").

## Related Prompts

- `m365-meeting-prep-brief`
- `m365-weekly-review-coach`

## Changelog

- 2025-11-18: Initial version created.
