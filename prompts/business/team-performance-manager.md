---

title: "Team Performance Manager"
category: "business"
tags: ["project-manager", "team-management", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "intermediate"
platform: "Claude Sonnet 4.5"
---

# Team Performance Manager

## Description

Optimizes team performance

## Use Cases

- Team Management for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

## Prompt

```text
Improve team performance for:

Team: [team_name]
Current Challenges: [challenges]
Performance Goals: [goals]
Team Dynamics: [dynamics]

Include:
1. Performance assessment
2. Skill development plan
3. Motivation strategies
4. Communication improvement
5. Conflict resolution
6. Recognition programs
```

## Variables

- `[challenges]`: Challenges
- `[dynamics]`: Dynamics
- `[goals]`: Goals
- `[team_name]`: Team Name

## Example Usage

**Input:**

```text
[team_name]: "Alpha Squad" (Backend Engineering - 6 members)
[challenges]: High burnout risk, low velocity (missed last 2 sprints), knowledge silos in senior devs
[goals]: Increase velocity by 20%, reduce bug reopen rate to <5%, improve team morale score
[dynamics]: 2 senior devs dominate architectural decisions, 3 junior devs hesitant to speak up
```

**Output:**

```text
## Team Performance Improvement Plan

### 1. Performance Assessment
*   **Root Cause:** "Hero Culture" leading to bottlenecks at senior devs; juniors blocked waiting for reviews.
*   **Metric Analysis:** Cycle time is high due to long code review wait times (avg 2 days).

### 2. Skill Development Plan
*   **Pair Programming:** Mandate 2 hours/day pairing (Senior + Junior) to transfer knowledge.
*   **Tech Talks:** Weekly rotation where juniors present a technical topic to build confidence.

### 3. Motivation Strategies
*   **Autonomy:** Assign end-to-end ownership of smaller features to juniors.
*   **Purpose:** Connect sprint tasks directly to customer impact metrics in planning meetings.

[... continues with communication and conflict resolution ...]
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Project Manager prompts in this category
- Check the business folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
