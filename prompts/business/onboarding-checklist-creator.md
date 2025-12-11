---
title: "Onboarding Checklist Creator"
shortTitle: "Onboarding Checklist"
intro: "Generate comprehensive onboarding checklists that ensure new hires are set up for success from day one."
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
  - "management"
  - "hr"
  - "onboarding"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 0.0
---
# Onboarding Checklist Creator

---

## Description

Create structured onboarding plans that help new employees ramp up quickly and feel welcomed. Generates day-by-day checklists covering logistics, training, introductions, and early wins.

---

## Use Cases

- Preparing for a new hire's first week
- Standardizing onboarding across teams
- Creating role-specific onboarding tracks
- Remote employee onboarding planning
- Onboarding contractors or temporary staff

---

## Prompt

```text
You are an expert in employee onboarding who creates programs that accelerate time-to-productivity.

Create an onboarding checklist for:

**New Hire**: [hire_info]
**Role**: [role]
**Team**: [team]
**Start Date**: [start_date]
**Work Setup**: [setup]
**Manager**: [manager]

Generate:

1. **Pre-Start Checklist** (before Day 1)
   - IT setup and access
   - Welcome materials
   - Manager preparation

2. **Day 1 Checklist**
   - Morning: Logistics and welcome
   - Afternoon: Team introductions
   - End of day: Reflection and questions

3. **Week 1 Checklist** (Day 2-5)
   - Daily themes/focus areas
   - Key meetings to schedule
   - Learning objectives

4. **30-Day Milestones**
   - What they should understand
   - Relationships to build
   - First contribution goals

5. **60-Day Milestones**
   - Independence expectations
   - Project ownership
   - Feedback checkpoint

6. **90-Day Success Criteria**
   - Full productivity benchmarks
   - Cultural integration signs
   - Manager evaluation criteria

Include specific calendar invites to send and people to meet. Make it actionable, not generic.
```text

---

## Variables

- `[hire_info]`: New hire name and background (e.g., "Jane Doe, joining from Google")
- `[role]`: Job title (e.g., "Senior Product Manager")
- `[team]`: Team name (e.g., "Growth Product Team")
- `[start_date]`: Start date (e.g., "Monday, January 15")
- `[setup]`: Work setup (e.g., "Remote with quarterly offsites", "Hybrid 3 days/week")
- `[manager]`: Manager name (e.g., "John Smith, Director of Product")

---

## Example

### Context

You are onboarding a new Senior Data Scientist to your analytics team and want a detailed plan covering pre‑start tasks, Day 1, Week 1, and 30/60/90‑day milestones.

### Input

```text
You are an expert in employee onboarding who creates programs that accelerate time-to-productivity.

Create an onboarding checklist for:

**New Hire**: Priya Sharma – Senior Data Scientist with 6 years of experience in SaaS analytics
**Role**: Senior Data Scientist, Analytics Team
**Team**: Central Analytics team supporting Growth and Product
**Start Date**: Monday, December 9, 2024
**Work Setup**: Hybrid – 2 days/week in NYC office, rest remote
**Manager**: David Chen (Director of Analytics)

Generate the full onboarding plan as described in the prompt (pre‑start, Day 1, Week 1, 30/60/90‑day milestones and success criteria).
```text

### Expected Output

The AI produces a structured onboarding plan with checklists, schedules, milestones, and success criteria similar to the detailed example that follows.

**Output:**

```markdown
# Onboarding Plan: Priya Sharma
**Role**: Senior Data Scientist, Analytics Team  
**Start Date**: Monday, December 9, 2024  
**Manager**: David Chen  
**Buddy**: [Assign from team]

---

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

---

## Day 1: Monday, December 9

### Morning (9:00 AM - 12:00 PM)

| Time | Activity | Owner | Location |
|------|----------|-------|----------|
| 9:00 | Arrive, badge pickup, desk setup | David | NYC Office - Lobby |
| 9:30 | Welcome coffee with David | David | Coffee bar |
| 10:00 | HR orientation (benefits, policies, systems) | HR | Conf room A |
| 11:00 | IT setup walkthrough (laptop, accounts, tools) | IT | Priya's desk |
| 11:30 | Slack/email setup, calendar review | Priya (self) | Desk |

### Afternoon (12:00 PM - 5:00 PM)

| Time | Activity | Owner | Location |
|------|----------|-------|----------|
| 12:00 | Team lunch (Analytics team) | David | Local restaurant |
| 1:30 | Meet your buddy: Marcus | Marcus | Conf room B |
| 2:30 | Analytics team overview (mission, projects, rituals) | David | Conf room B |
| 3:30 | Codebase tour + dev environment setup | Marcus | Desk/Zoom |
| 4:30 | End-of-day check-in with David | David | David's office |

### Day 1 Goals
- [ ] Laptop fully configured and can access all systems
- [ ] Met the entire Analytics team
- [ ] Knows where to find help (buddy, Slack channels, wiki)
- [ ] Calendar populated with Week 1 meetings
- [ ] One small win: sent first Slack message to #analytics

### Evening Assignment (Optional)
- Read: Analytics team wiki (30 min)
- Skim: Churn model v1 documentation (15 min)

---

## Week 1: December 9-13

### Day 2 (Tuesday - Office Day)

**Theme**: Understand the data landscape

| Time | Activity | Purpose |
|------|----------|---------|
| 10:00 | Data infrastructure overview with Carlos (Data Eng) | Understand data pipelines, Snowflake structure |
| 11:30 | 1:1 with Lisa (current churn model owner) | Knowledge transfer kickoff |
| 2:00 | Product team intro: Meet Sarah (PM, Growth) | Understand customer context |
| 3:30 | Self-study: Explore Snowflake tables, run sample queries | Hands-on data familiarity |

**Day 2 Goals**:
- [ ] Can navigate Snowflake and find key tables
- [ ] Understands data flow from product → warehouse
- [ ] Has first conversation with stakeholder (Sarah)

---

### Day 3 (Wednesday - Remote)

**Theme**: Deep dive on current projects

| Time | Activity | Purpose |
|------|----------|---------|
| 10:00 | Churn model walkthrough with Lisa (Zoom) | Understand model architecture, features, limitations |
| 11:30 | Self-study: Run churn model notebook, review code | Hands-on with existing work |
| 2:00 | Meet Customer Success: Intro with Jordan (CS Lead) | Understand how predictions are used |
| 3:30 | Document questions for David | Prepare for Thursday sync |

**Day 3 Goals**:
- [ ] Can run existing churn model end-to-end
- [ ] Has list of questions about model/data
- [ ] Understands downstream users of the model

---

### Day 4 (Thursday - Office Day)

**Theme**: Cross-functional relationships

| Time | Activity | Purpose |
|------|----------|---------|
| 10:00 | Meet Engineering: Intro with Platform team lead | Understand tech stack, deployment process |
| 11:00 | Weekly Analytics team standup | Observe team rituals |
| 2:00 | 1:1 with David (weekly sync) | Discuss Week 1 learnings, answer questions |
| 3:00 | Skip-level: Coffee with VP of Data (optional if available) | Big picture context |

**Day 4 Goals**:
- [ ] Met key cross-functional partners
- [ ] Attended first team meeting
- [ ] Week 1 questions addressed with David

---

### Day 5 (Friday - Remote)

**Theme**: Consolidate and plan

| Time | Activity | Purpose |
|------|----------|---------|
| 10:00 | Self-study: Complete any pending documentation review | Fill knowledge gaps |
| 11:00 | Write Week 1 reflection doc (share with David) | Synthesize learnings |
| 2:00 | Buddy check-in with Marcus | Ask remaining questions |
| 3:00 | Plan Week 2 priorities with David (async or Zoom) | Set direction |

**Day 5 Goals**:
- [ ] Week 1 reflection doc completed and shared
- [ ] Comfortable with tools, systems, and team
- [ ] Knows Week 2 focus area

---

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

---

## 60-Day Milestones (by Feb 7)

### Independence
- [ ] Can run end-to-end analysis without significant guidance
- [ ] Owns churn model v2 improvements (Lisa has fully handed off)
- [ ] Responds to ad-hoc data requests from stakeholders independently
- [ ] Attends stakeholder meetings as Analytics representative (not shadow)

### Project Ownership
- [ ] Leading churn model v2 project (scope, timeline, execution)
- [ ] Has shipped at least one improvement to production model
- [ ] Documented work in team wiki for future reference

### Feedback
- [ ] Gave feedback to manager on onboarding experience
- [ ] Received first formal feedback from David (60-day check-in)
- [ ] Identified one area for personal development focus

### Check-in Meeting (60-day)
**Agenda**:
1. Review 60-day goals
2. Discuss project progress and blockers
3. Gather feedback on onboarding
4. Discuss development goals and interests

---

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

---

## Key Contacts Quick Reference

| Person | Role | When to Contact |
|--------|------|-----------------|
| David Chen | Manager | Weekly 1:1s, blockers, feedback |
| Marcus | Buddy | Day-to-day questions, cultural norms |
| Lisa | Churn model owner | Technical knowledge transfer |
| Carlos | Data Engineer | Data pipeline, Snowflake questions |
| Sarah | PM, Growth | Product context, stakeholder needs |
| Jordan | CS Lead | How predictions are used in field |
| IT Help Desk | Support | Access issues, tech problems |
| HR | People Ops | Benefits, policies, logistics |

---

## Onboarding Feedback (for Priya to complete at Day 30)

1. What was most helpful in your first month?
2. What was missing or confusing?
3. What would you change for the next new hire?
4. Rate your onboarding experience: 1-5
5. Additional comments?
```text

---


## Tips

- Front-load relationship building - people connections matter more than systems in Week 1
- Assign a buddy who isn't the manager - gives new hire a safe space to ask "dumb" questions
- Include quick wins - first commit, first Slack post, first meeting facilitation
- Don't over-schedule Week 1 - leave time for self-study and absorption
- Check in at 30/60/90 days - onboarding doesn't end after Week 1

---

## Related Prompts

- [job-description-writer](./job-description-writer.md) - For role clarity before hiring
- [interview-questions](./interview-questions.md) - For hiring the right person
- [performance-review](./performance-review.md) - For evaluating after onboarding
