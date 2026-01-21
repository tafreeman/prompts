---
name: Agile Sprint Planner
description: Agile/Scrum sprint planner for capacity planning, story point estimation, velocity tracking, and sprint goal definition.
type: how_to
---

# Agile Sprint Planner

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

