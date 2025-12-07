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
```

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
```

**Output:**

```markdown
# Sprint 12 Plan: Payment Friction Reduction

**Sprint Duration**: Nov 20 - Dec 1 (10 working days)  
**Sprint Goal**: *"Enable frictionless payments to reduce cart abandonment by 15% before Black Friday launch."*

---

## 1. User Story Breakdown

### Epic: Checkout Optimization

| Story ID | User Story | Story Points | Priority | Assignee | Status |
|----------|-----------|--------------|----------|----------|--------|
| **STORE-421** | As a returning user, I want my default payment method pre-selected so I can checkout in one tap | 8 | P0 | Sarah (Frontend) | Planned |
| **STORE-422** | As a user, I want address autofill (Google Places API) so I don't manually type shipping info | 5 | P1 | Mike (Frontend) | Planned |

#### Story STORE-421: One-Click Checkout

**Acceptance Criteria**:
1. ✅ User's saved credit card is pre-selected by default
2. ✅ "Buy Now" button visible without expanding payment section
3. ✅ Order confirmation shows in <3 seconds
4. ✅ Analytics event `checkout_onec click` fires

**Tasks** (Total: 8 points):
- [ ] API: Add `/user/default-payment GET` endpoint (2 points, 4 hours)
- [ ] Frontend: Build "Buy Now" button component (3 points, 6 hours)
- [ ] Testing: Appium test for one-click flow (2 points, 4 hours)
- [ ] Analytics: Integrate GA4 event (1 point, 2 hours)

**Dependencies**: 
- Requires Stripe API token refresh (currently rate-limited → contact DevOps)

---

### Epic: Payment Methods

| Story ID | User Story | Story Points | Priority | Assignee | Status |
|----------|-----------|--------------|----------|----------|--------|
| **STORE-423** | As a user, I want to pay with Apple Pay so I don't enter card details | 13 | P0 | Emily (Backend), Sarah (iOS) | Planned |
| **STORE-424** | As a user, I want to see "Secure Checkout" badge to trust the payment flow | 3 | P2 | Design Team | Backlog |

#### Story STORE-423: Apple Pay Integration

**Acceptance Criteria**:
1. ✅ Apple Pay button appears on iOS devices (not Android)
2. ✅ Payment auth completes via Touch ID/Face ID
3. ✅ Transaction confirmed in Stripe dashboard
4. ✅ Apple Pay certification passed (required for App Store approval)

**Tasks** (Total: 13 points):
- [ ] Backend: Stripe Apple Pay SDK integration (5 points, 10 hours)
- [ ] iOS: Apple Pay button + biometric auth flow (5 points, 10 hours)
- [ ] Certification: Submit test transaction to Apple (2 points, 4 hours)
- [ ] Testing: E2E test with real Apple Pay sandbox account (1 point, 2 hours)

**Risks**:
- 🔴 **Apple Pay certification** can take 2-5 business days (vs. 2-day sprint buffer)
- **Mitigation**: Start certification on Day 1 (Nov 20 morning) to allow 10-day window

---

### Epic: Social Commerce

| Story ID | User Story | Story Points | Priority | Assignee | Status |
|----------|-----------|--------------|----------|----------|--------|
| **STORE-425** | As a user, I want my wishlist synced across mobile & web so I can shop anywhere | 5 | P2 | Tom (Backend) | Deferred to Sprint 13 |

**Deferral Rationale**: Wishlist sync is P2 and doesn't impact Black Friday cart abandonment goal. Moving to Sprint 13 to protect sprint goal focus.

---

## 2. Capacity Planning

### Team Roster & Availability

| Team Member | Role | Normal Capacity | This Sprint Capacity | Notes |
|-------------|------|-----------------|----------------------|-------|
| Sarah | iOS Developer | 20 pts/sprint | 16 pts | Out Nov 27-29 (Thanksgiving) |
| Emily | Backend Engineer | 20 pts/sprint | 16 pts | Out Nov 27-29 (Thanksgiving) |
| Mike | Frontend Developer | 20 pts/sprint | 20 pts | Available full sprint |
| Tom | Backend Engineer | 20 pts/sprint | 20 pts | Available full sprint |
| Design Team | UI/UX | 10 pts/sprint | 8 pts | Reduced due to parallel holiday campaign work |
| **Total** | | **100 pts** | **80 pts** | |

### Story Point Allocation

| Epic | Stories | Total Points | % of Capacity |
|------|---------|--------------|---------------|
| Checkout Optimization | STORE-421, STORE-422 | 13 pts | 16% |
| Payment Methods | STORE-423 | 13 pts | 16% |
| **Sprint Committed** | | **26 pts** | **33%** |
| **Stretch Goals** | STORE-424 (Secure Badge) | 3 pts | 4% |
| **Buffer (Hotfixes, Tech Debt)** | | 5 pts | 6% |
| **Unallocated Reserve** | | 46 pts | 58% |

**Velocity Analysis**:
- **Historical Velocity**: 95 pts/sprint (avg last 3 sprints)
- **Holiday-Adjusted Target**: 80 pts (20% reduction due to PTO)
- **Conservative Commitment**: 26 pts (33% utilization to account for Apple Pay risk)

**Rationale for Low Commitment**:
- Apple Pay is high-risk (certification delays)
- Better to under-commit and over-deliver than miss sprint goal before Black Friday
- 46 pts reserve can absorb P0 production bugs

---

## 3. Risk Mitigation

### Risk Register

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| **Apple Pay certification delay** | High (60%) | Critical (blocks release) | Start cert on Day 1; parallel track with backup plan (Google Pay) |
| **Stripe API rate limit** | Medium (30%) | High (delays testing) | Contact DevOps to increase rate limit quota before sprint start |
| **Black Friday production load** | Low (20%) | Critical (site downtime) | Deploy payment changes to staging on Nov 25 for 1-week soak test |
| **Team member illness during holiday** | Medium (40%) | Medium (delays stories) | Cross-train Sarah & Emily on Apple Pay code (pair programming Day 1-2) |

---

## 4. Success Metrics

### Sprint Burndown Targets

| Day | Target Remaining Points | Actual Remaining | On Track? |
|-----|-------------------------|------------------|-----------|
| Day 0 (Nov 20) | 26 pts | 26 pts | ✅ Baseline |
| Day 2 (Nov 22) | 22 pts | TBD | |
| Day 5 (Nov 27) | 15 pts | TBD | (Thanksgiving week - expect slower burn) |
| Day 8 (Nov 30) | 5 pts | TBD | |
| Day 10 (Dec 1) | 0 pts | TBD | ✅ Goal |

**Key Performance Indicators (KPIs)**:
- **Commitment Met**: 100% of committed stories (STORE-421, STORE-422, STORE-423) delivered
- **Definition of Done**: All 5 DoD criteria met for each story
- **Cart Abandonment**: Reduce from 68% → 58% (10% improvement, measured via GA4)
- **Apple Pay Adoption**: 15% of iOS transactions use Apple Pay within 1 week of release

---

## 5. Sprint Ceremonies Schedule

### Daily Standup (Async in Slack #standup channel)

**Time**: 9:00 AM ET (daily)  
**Format**: 
- What I did yesterday
- What I'm doing today
- Blockers (tag @scrum-master if blocking)

**Sample**:
```

@Sarah: Yesterday: Completed Buy Now button UI. Today: Start Apple Pay iOS integration. Blockers: None.
@Emily: Yesterday: Designed /default-payment API. Today: Stripe Apple Pay SDK setup. Blockers: Need Stripe API token refresh (tagged @DevOps).

```

### Sprint Review (Demo)

**Date**: Dec 1 (Friday), 2:00 PM ET  
**Duration**: 60 minutes  
**Attendees**: Product Owner, Engineering Team, Marketing (for Black Friday alignment)  
**Agenda**:
1. Demo STORE-421: One-Click Checkout (5 min)
2. Demo STORE-423: Apple Pay (10 min)
3. Show cart abandonment metrics drop (5 min)
4. Q&A (10 min)

### Sprint Retrospective

**Date**: Dec 1 (Friday), 3:30 PM ET  
**Duration**: 45 minutes  
**Format**: Start/Stop/Continue  
**Focus Questions**:
- Did holiday PTO impact velocity as expected?
- Was Apple Pay risk mitigation effective?
- Should we adjust story point estimates for payment integration work?

---

## 6. Daily Burndown Tracking

**Tool**: Jira (auto-generates burndown chart)  
**Review Cadence**: Scrum Master reviews daily at 10 AM ET  
**Escalation Trigger**: If remaining points > target by 20% for 2 consecutive days → alert Product Owner

**Sample Burndown Chart** (ASCII representation):

```

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

```

---

## Contingency Plans

### If Apple Pay Certification Delayed Beyond Dec 1:
1. **Fallback**: Ship Sprint 12 without Apple Pay (deploy STORE-421 & STORE-422 only)
2. **Fast-Follow**: Release Apple Pay in hotfix Sprint 12.1 (Dec 2-3) if cert arrives
3. **Communication**: Notify Marketing that "Apple Pay by Black Friday" may slip
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
- **[project-charter-creator](./project-charter-creator.md)** - For initial sprint planning at project kickoff
