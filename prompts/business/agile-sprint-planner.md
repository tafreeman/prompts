---
name: Agile Sprint Planner
description: Agile/Scrum sprint planner for capacity planning, story point estimation, velocity tracking, and sprint goal definition.
type: how_to
---

# Agile Sprint Planner

## Description

This prompt helps Agile/Scrum teams plan effective sprints by providing structured guidance for capacity planning, story point estimation, velocity tracking, and sprint goal definition. Use it to create comprehensive sprint plans that account for team capacity, holidays, and risk factors.

## Use Cases

- Two-week sprint planning for product development teams
- Capacity planning during holidays or team transitions
- User story decomposition and estimation
- Sprint retrospective preparation
- Release planning and roadmap alignment

## Variables

- `[project_name]`: Product or feature name (e.g., "E-commerce Mobile App - Payment Module")
- `[sprint_number]`: Sprint number in sequence (e.g., "Sprint 12 of24")
- `[duration]`: Sprint length (e.g., "2 Weeks", "10 Working Days")
- `[capacity]`: Available story points (e.g., "80 points (reduced from 100 due to Thanksgiving holiday, 2 devs on PTO)")
- `[features]`: Priority features from product backlog (e.g., "One-click Checkout, Apple Pay Integration, Wishlist Sync")
- `[dod]`: Definition of Done criteria (e.g., "Unit tests passed, UI automated tests green, PO sign-off, Analytics events fired")

## Prompt

### System Prompt

```text
You are an experienced Agile Coach and Scrum Master with expertise in sprint planning, capacity management, and agile best practices. Help teams create effective sprint plans that balance ambition with realistic delivery.
```

### User Prompt

```text
Help me plan a sprint for [project_name].

Sprint Details:
- Sprint Number: [sprint_number]
- Duration: [duration]
- Team Capacity: [capacity]
- Priority Features: [features]
- Definition of Done: [dod]

Please provide:
1. Sprint goal statement
2. Capacity analysis with any risks or adjustments needed
3. Recommended story breakdown and point allocation
4. Key milestones and checkpoints
5. Risk factors and mitigation strategies
6. Success criteria for the sprint
```

## Example

### Input

```text
Help me plan a sprint for E-commerce Mobile App - Payment Module.

Sprint Details:
- Sprint Number: Sprint 12 of 24
- Duration: 2 Weeks (10 Working Days)
- Team Capacity: 80 points (reduced from 100 due to Thanksgiving holiday, 2 devs on PTO)
- Priority Features: One-click Checkout, Apple Pay Integration, Wishlist Sync
- Definition of Done: Unit tests passed, UI automated tests green, PO sign-off, Analytics events fired
```

### Expected Output

```text
## Sprint 12 Plan: Payment Module

### Sprint Goal
Enable seamless checkout experiences by delivering one-click checkout and Apple Pay integration, increasing conversion rates for returning customers.

### Capacity Analysis
- Base Capacity: 100 points
- Holiday Adjustment: -10 points (Thanksgiving)
- PTO Adjustment: -10 points (2 developers)
- Available Capacity: 80 points
- Recommended Commitment: 72 points (90% of capacity for buffer)

### Story Breakdown
| Story | Points | Priority | Risk |
|-------|--------|----------|------|
| One-click Checkout | 21 | P1 | Low |
| Apple Pay Integration | 34 | P1 | High |
| Wishlist Sync | 13 | P2 | Low |
| Tech Debt: Payment Logging | 8 | P3 | Low |
| Total | 76 | | |

### Key Milestones
- Day 2: Apple Pay sandbox setup complete
- Day 5: One-click checkout feature complete
- Day 7: Apple Pay integration code complete
- Day 8: QA begins full regression
- Day 10: Sprint review and demo

### Risk Mitigation
- Apple Pay certification may cause delays - start Day 1
- Schedule daily syncs for payment features
```

## Tips

- **Protect the Sprint Goal**: If mid-sprint scope creep occurs (e.g., CEO requests "Buy Now, Pay Later"), defer to backlog unless P0 production bug
- **Adjust Velocity for Holidays**: Reduce capacity by 20-30% during holiday weeks (Thanksgiving, Christmas, New Year's)
- **Front-Load Risky Stories**: Start Apple Pay (STORE-423) on Day 1 to maximize time for certification blockers
- **Cross-Train Team Members**: Pair programming on Day 1-2 prevents single points of failure (especially before holiday PTO)
- **Monitor Burndown Daily**: If burndown flatlines for 2 days, escalate immediately (don't wait for retrospective)
- **Celebrate Small Wins**: If one-click checkout deploys early, demo it in mid-sprint to build momentum

---

## Related Prompts

- **[stakeholder-communication-manager](./stakeholder-communication-manager.md)** - For sprint review stakeholder updates
- **[risk-management-analyst](./risk-management-analyst.md)** - For sprint risk assessment

