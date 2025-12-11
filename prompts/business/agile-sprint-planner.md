---
title: "Agile Sprint Planner"
shortTitle: "Sprint Planner"
intro: "Agile/Scrum sprint planner for capacity planning, story point estimation, velocity tracking, and sprint goal definition."
type: "how_to"
difficulty: "intermediate"
audience:
  - "project-manager"
  - "senior-engineer"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "agile"
  - "project-management"
author: "Prompts Library Team"
version: "1.1"
date: "2025-11-26"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 4.5
---
# Agile Sprint Planner

---

## Description

Agile/Scrum sprint planner for software development teams. Focuses on capacity planning, story point estimation, velocity tracking, and sprint goal definition using Scrum framework best practices.

---

## Use Cases

- Two-week sprint planning for product development teams
- Capacity planning during holidays or team transitions
- User story decomposition and estimation
- Sprint retrospective preparation
- Release planning and roadmap alignment

---

## Prompt

```text
You are a certified Scrum Master planning Sprint [sprint_number].

Plan sprint for:

**Project**: [project_name]
**Sprint Duration**: [duration]
**Team Capacity**: [capacity]
**Priority Features**: [features]
**Definition of Done**: [dod]

Provide:
1. **Sprint Goal** (One-sentence SMART goal)
2. **User Story Breakdown** (Epics → Stories → Tasks with acceptance criteria)
3. **Task Estimation** (Story points + hourly breakdown)
4. **Capacity Planning** (Velocity analysis + buffer allocation)
5. **Risk Mitigation** (Dependencies, blockers, technical unknowns)
6. **Success Metrics** (Burndown targets, completion criteria)
7. **Sprint Ceremonies** (Daily standup, review, retro schedules)

Format output with Markdown tables for story breakdown and capacity allocation.
```markdown

---

## Variables

- `[project_name]`: Product or feature name (e.g., "E-commerce Mobile App - Payment Module")
- `[sprint_number]`: Sprint number in sequence (e.g., "Sprint 12 of24")
- `[duration]`: Sprint length (e.g., "2 Weeks", "10 Working Days")
- `[capacity]`: Available story points (e.g., "80 points (reduced from 100 due to Thanksgiving holiday, 2 devs on PTO)")
- `[features]`: Priority features from product backlog (e.g., "One-click Checkout, Apple Pay Integration, Wishlist Sync")
- `[dod]`: Definition of Done criteria (e.g., "Unit tests passed, UI automated tests green, PO sign-off, Analytics events fired")

---

## Example Usage

**Input:**

```text
Project: E-commerce Mobile App - Payment Module
Sprint Number: Sprint 12 (of 24-sprint roadmap)
Duration: 2 Weeks (Nov 20 - Dec 1)
Capacity: 80 Story Points (Reduced from 100 due to Thanksgiving Holiday - 2 devs on PTO for 3 days)
Features: 
- "One-click Checkout" (Epic: Checkout Optimization)
- "Apple Pay Integration" (Epic: Payment Methods)
- "Wishlist Sync Across Devices" (Epic: Social Commerce)

Definition of Done:
- Unit tests passed (>90% coverage)
- UI automated tests green (Appium suite)
- Product Owner sign-off on acceptance criteria
- Analytics events fired correctly (Google Analytics 4)
- API documentation updated in Swagger

Context: Black Friday launch deadline is Dec 15. This sprint must deliver payment improvements to reduce cart abandonment (currently 68%).
```text

@Sarah: Yesterday: Completed Buy Now button UI. Today: Start Apple Pay iOS integration. Blockers: None.
@Emily: Yesterday: Designed /default-payment API. Today: Stripe Apple Pay SDK setup. Blockers: Need Stripe API token refresh (tagged @DevOps).

```text

Points ↑
26 |●
   |  ●●
20 |      ●●
   |          ●●
10 |              ●
   |                  ●
 0 |____________________●____→ Days
   0  2  4  6  8  10

   Ideal Burndown: ● (diagonal line)
   Actual: Monitor daily

```text

---

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

