---
name: Onboarding Checklist Creator
description: Generate comprehensive onboarding checklists that ensure new hires are set up for success from day one.
type: how_to
---
## Description

## Prompt

```text
You are an HR and onboarding specialist who creates comprehensive onboarding plans that set new hires up for success. You understand that great onboarding combines logistics, relationship-building, and clear milestone expectations.
```

Generate comprehensive onboarding checklists that ensure new hires are set up for success from day one.

## Description

## Prompt

```text
You are an HR and onboarding specialist who creates comprehensive onboarding plans that set new hires up for success. You understand that great onboarding combines logistics, relationship-building, and clear milestone expectations.
```

Generate comprehensive onboarding checklists that ensure new hires are set up for success from day one.


# Onboarding Checklist Creator

## Description

This prompt generates comprehensive onboarding checklists that ensure new hires are set up for success from day one. It creates structured plans covering pre-start preparation, first week activities, and 30/60/90 day milestones.

## Use Cases

- Preparing for a new hire's first week
- Standardizing onboarding across teams
- Creating role-specific onboarding tracks
- Remote employee onboarding planning
- Onboarding contractors or temporary staff

## Variables

- `[hire_info]`: New hire name and background (e.g., "Jane Doe, joining from Google")
- `[role]`: Job title (e.g., "Senior Product Manager")
- `[team]`: Team name (e.g., "Growth Product Team")
- `[start_date]`: Start date (e.g., "Monday, January 15")
- `[setup]`: Work setup (e.g., "Remote with quarterly offsites", "Hybrid 3 days/week")
- `[manager]`: Manager name (e.g., "John Smith, Director of Product")

## Prompt

### System Prompt

```text
You are an HR and onboarding specialist who creates comprehensive onboarding plans that set new hires up for success. You understand that great onboarding combines logistics, relationship-building, and clear milestone expectations.
```

### User Prompt

```text
Create an onboarding checklist for the following new hire:

New Hire Details:
- Name/Background: [hire_info]
- Role: [role]
- Team: [team]
- Start Date: [start_date]
- Work Setup: [setup]
- Manager: [manager]

Please provide:
1. Pre-start checklist (IT, access, welcome materials)
2. Day 1 agenda
3. Week 1 schedule with key meetings
4. 30-day milestones and check-in agenda
5. 60-day expectations
6. 90-day success criteria
```

## Example

### Input

```text
Create an onboarding checklist for the following new hire:

New Hire Details:
- Name/Background: Jane Doe, joining from Google
- Role: Senior Product Manager
- Team: Growth Product Team
- Start Date: Monday, January 15
- Work Setup: Remote with quarterly offsites
- Manager: John Smith, Director of Product
```

### Expected Output

```text
## Onboarding Plan: Jane Doe, Senior PM

### Pre-Start Checklist (Complete by Jan 12)

**IT & Access** (Owner: IT)
- [ ] Laptop ordered and shipped
- [ ] Email account: jane.doe@company.com
- [ ] Slack added to #growth-team, #product, #all-hands
- [ ] Figma, Jira, Amplitude access provisioned
- [ ] 1Password vault access

**Manager Prep** (Owner: John Smith)
- [ ] 30/60/90 day goals drafted
- [ ] Onboarding buddy assigned (recommend: Senior PM who's been here 1+ year)
- [ ] First project identified
- [ ] Week 1 calendar blocked for key intros

### Day 1: Monday, Jan 15
| Time | Activity | Purpose |
|------|----------|----------|
| 9:00 | Welcome call with John | Expectations, logistics |
| 10:00 | IT setup support | Get systems working |
| 11:00 | Meet onboarding buddy | Informal culture intro |
| 1:00 | Product overview with John | Strategy, roadmap context |
| 3:00 | Self-study: Internal wiki, docs | Absorb context |

### Week 1 Key Meetings
- **Day 2**: Meet Engineering counterpart
- **Day 3**: Growth team standup (observe)
- **Day 4**: 1:1s with 3 cross-functional partners
- **Day 5**: End-of-week check-in with John

### 30-Day Milestones (by Feb 14)
- [ ] Completed all team 1:1s
- [ ] Understands Growth team OKRs and how role contributes
- [ ] Shadowed 3 customer calls
- [ ] Presented initial observations at team meeting
- [ ] First small project shipped or in progress

### 60-Day Expectations (by Mar 15)
- [ ] Owns one significant workstream independently
- [ ] Has built relationships with key stakeholders
- [ ] Contributing to roadmap discussions

### 90-Day Success Criteria (by Apr 15)
- [ ] Performing at expected Senior PM level
- [ ] One major initiative shipped or clearly on track
- [ ] Manager confident in independent execution
```

## Pre-Start Checklist (Complete by Dec 6)

### IT & Access (Owner: IT/Manager)

- [ ] Laptop ordered and configured (MacBook Pro 16")
- [ ] Email account created: priya.sharma@company.com
- [ ] Slack account provisioned + added to channels: #analytics, #data-science, #nyc-office
- [ ] GitHub access granted to analytics repos
- [ ] Snowflake/data warehouse credentials created
- [ ] Jupyter/Databricks workspace provisioned
- [ ] VPN access configured
- [ ] Building access badge prepared (for Tues/Thurs office days)

### Manager Prep (Owner: David Chen)

- [ ] 30/60/90 day goals drafted
- [ ] Onboarding buddy assigned (recommend: Marcus - senior DS, been here 2 years)
- [ ] First project identified (churn model v2 handoff from Lisa)
- [ ] Week 1 calendar blocked for key meetings
- [ ] Welcome message drafted for team Slack channel

### Welcome Materials (Owner: HR/Manager)

- [ ] Welcome email sent with:
  - [ ] First day logistics (arrive by 9am, ask for David at reception)
  - [ ] What to bring (ID for badge, personal items for desk)
  - [ ] Dress code (casual)
  - [ ] Parking/transit info
- [ ] Company swag kit shipped to home address
- [ ] Benefits enrollment packet ready
- [ ] Org chart and team directory shared

## Week 1: December 9-13

### Day 2 (Tuesday - Office Day)

**Theme**: Understand the data landscape

| Time | Activity | Purpose |
| ------ | ---------- | --------- |
| 10:00 | Data infrastructure overview with Carlos (Data Eng) | Understand data pipelines, Snowflake structure |
| 11:30 | 1:1 with Lisa (current churn model owner) | Knowledge transfer kickoff |
| 2:00 | Product team intro: Meet Sarah (PM, Growth) | Understand customer context |
| 3:30 | Self-study: Explore Snowflake tables, run sample queries | Hands-on data familiarity |

**Day 2 Goals**:

- [ ] Can navigate Snowflake and find key tables
- [ ] Understands data flow from product → warehouse
- [ ] Has first conversation with stakeholder (Sarah)

### Day 4 (Thursday - Office Day)

**Theme**: Cross-functional relationships

| Time | Activity | Purpose |
| ------ | ---------- | --------- |
| 10:00 | Meet Engineering: Intro with Platform team lead | Understand tech stack, deployment process |
| 11:00 | Weekly Analytics team standup | Observe team rituals |
| 2:00 | 1:1 with David (weekly sync) | Discuss Week 1 learnings, answer questions |
| 3:00 | Skip-level: Coffee with VP of Data (optional if available) | Big picture context |

**Day 4 Goals**:

- [ ] Met key cross-functional partners
- [ ] Attended first team meeting
- [ ] Week 1 questions addressed with David

## 30-Day Milestones (by Jan 8)

### Understanding

- [ ] Can explain company's business model and key metrics to a new hire
- [ ] Understands Analytics team's OKRs and how churn model fits
- [ ] Knows the top 5 data tables used by the team and their purpose
- [ ] Can articulate why churn prediction matters to the business

### Relationships

- [ ] Had 1:1s with all Analytics team members
- [ ] Built relationship with key stakeholder (Sarah in Product)
- [ ] Knows who to go to for: data questions (Carlos), product context (Sarah), model review (Lisa)
- [ ] Comfortable asking questions in team Slack channel

### Contribution

- [ ] Completed churn model v2 knowledge transfer from Lisa
- [ ] Identified 2-3 potential improvements to existing model
- [ ] Made first commit to analytics codebase (even if small)
- [ ] Presented initial findings/ideas at team standup

### Check-in Meeting (30-day)
**Agenda**:

1. What's going well?
2. What's confusing or frustrating?
3. Review 30-day goals (what's on track, what needs adjustment)
4. Preview 60-day expectations

## 90-Day Success Criteria (by Mar 8)

### Full Productivity

- [ ] Performing at expected level for Senior Data Scientist
- [ ] Independently scoping and delivering projects
- [ ] Proactively identifying opportunities, not just executing requests
- [ ] Velocity comparable to tenured team members

### Cultural Integration

- [ ] Contributing to team discussions and decisions
- [ ] Building reputation as go-to person for churn/retention analysis
- [ ] Comfortable pushing back respectfully on stakeholder requests
- [ ] Has helped onboard or mentor someone else (if opportunity arises)

### Deliverables

- [ ] Churn model v2 shipped and in production
- [ ] Model performance improved by [target metric]
- [ ] Stakeholders (Product, CS) actively using new predictions
- [ ] Presented results to broader team or company

### Manager Evaluation Questions

1. Would I hire Priya again? (Yes/No + why)
2. Is Priya performing at the Senior level? (expectations met?)
3. What would make Priya exceptional in the next 6 months?
4. Any concerns about culture fit or collaboration?

## Onboarding Feedback (for Priya to complete at Day 30)

1. What was most helpful in your first month?
2. What was missing or confusing?
3. What would you change for the next new hire?
4. Rate your onboarding experience: 1-5
5. Additional comments?

```text

## Related Prompts

- [job-description-writer](./job-description-writer.md) - For role clarity before hiring
- [interview-questions](./interview-questions.md) - For hiring the right person
- [performance-review](./performance-review.md) - For evaluating after onboarding## Variables

| Variable | Description |
|---|---|
| `[ ]` | AUTO-GENERATED: describe ` ` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````
## Variables

| Variable | Description |
|---|---|
| `[ ]` | AUTO-GENERATED: describe ` ` |
| `[Fill in a realistic input for the prompt]` | AUTO-GENERATED: describe `Fill in a realistic input for the prompt` |
| `[Representative AI response]` | AUTO-GENERATED: describe `Representative AI response` |
| `[hire_info]` | AUTO-GENERATED: describe `hire_info` |
| `[interview-questions]` | AUTO-GENERATED: describe `interview-questions` |
| `[job-description-writer]` | AUTO-GENERATED: describe `job-description-writer` |
| `[manager]` | AUTO-GENERATED: describe `manager` |
| `[performance-review]` | AUTO-GENERATED: describe `performance-review` |
| `[role]` | AUTO-GENERATED: describe `role` |
| `[setup]` | AUTO-GENERATED: describe `setup` |
| `[start_date]` | AUTO-GENERATED: describe `start_date` |
| `[target metric]` | AUTO-GENERATED: describe `target metric` |
| `[team]` | AUTO-GENERATED: describe `team` |

## Example

### Input

````text
[Fill in a realistic input for the prompt]
````

### Expected Output

````text
[Representative AI response]
````

