---
title: "Stakeholder Communication Manager"
shortTitle: "Stakeholder Comms"
intro: "Strategic communications specialist for complex stakeholder management with executive updates and crisis communication."
type: "how_to"
difficulty: "intermediate"
audience:

  - "project-manager"
  - "solution-architect"

platforms:

  - "claude"
  - "chatgpt"
  - "github-copilot"

topics:

  - "communication"
  - "stakeholder-management"

author: "Prompts Library Team"
version: "1.1"
date: "2025-11-26"
governance_tags:

  - "PII-safe"

dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 0.0
---
# Stakeholder Communication Manager

---

## Description

A strategic communications specialist for complex stakeholder management across enterprise projects. Focuses on executive updates, change management messaging, crisis communication, and multi-stakeholder alignment for distributed teams.

---

## Use Cases

- Quarterly executive board updates for technical transformation projects
- Change management communications for ERP/CRM migrations
- Crisis communication during service outages or project delays
- Multi-stakeholder alignment for cross-functional initiatives
- Vendor/partner relationship communication management

---

## Prompt

```text
You are a Senior Stakeholder Communication Manager responsible for enterprise project communications.

Develop a comprehensive communication strategy for:

**Project**: [project_name]
**Stakeholders**: [stakeholders]
**Project Phase**: [phase]
**Communication Challenges**: [challenges]

Provide:

1. **Stakeholder Analysis** (Power/Interest Matrix with RACI roles)
2. **Communication Matrix** (Who, What, When, How, Why)
3. **Meeting Schedules** (Cadence calendar with objectives)
4. **Reporting Templates** (Executive summaries, technical updates, all-hands formats)
5. **Escalation Procedures** (Issue triage flows)
6. **Feedback Mechanisms** (Surveys, pulse checks, retrospectives)
7. **Crisis Communication Playbook** (If project is at risk)

Format output in structured Markdown with tables for matrices and calendars.
```markdown

---

## Variables

- `[project_name]`: Project name and scope (e.g., "SAP S/4HANA Implementation - Finance & Supply Chain Modules")
- `[stakeholders]`: List of stakeholder groups with roles (e.g., "CFO (Sponsor), VP Supply Chain (Key User), IT Director, Warehouse Staff (End Users)")
- `[phase]`: Current project phase (e.g., "Blueprinting/Design", "UAT", "Go-Live", "Post-Production Support")
- `[challenges]`: Specific communication obstacles (e.g., "Resistance to change from warehouse staff, CFO demanding faster ROI visibility, offshore vendor language barriers")

---

## Example

### Context

You are leading communications for a large SAP S/4HANA implementation with multiple executive sponsors, business users, and offshore vendors. There is resistance to change and pressure to accelerate the timeline, so you need a robust stakeholder communication plan.

### Input

```text
You are a Senior Stakeholder Communication Manager responsible for enterprise project communications.

Develop a comprehensive communication strategy for:

**Project**: SAP S/4HANA Implementation (Finance & Supply Chain Modules)
**Stakeholders**:

- CFO (Executive Sponsor)
- VP Supply Chain (Key Business User)
- IT Director (Technical Owner)
- Finance Manager (Subject Matter Expert)
- Warehouse Staff (50 end users across 3 sites)
- SAP Consulting Partner (Offshore team in India)

**Project Phase**: Blueprinting / Design (Month 3 of 18-month project)
**Communication Challenges**:

- Resistance to change from warehouse staff (fear of job automation)
- CFO demanding weekly ROI metrics and faster go-live (pressure to cut timeline from 18 to 12 months)
- Language barriers with offshore SAP consultants causing design misalignments
- Finance Manager overwhelmed by day-to-day responsibilities + project duties

Provide:

1. **Stakeholder Analysis** (Power/Interest Matrix with RACI roles)
2. **Communication Matrix** (Who, What, When, How, Why)
3. **Meeting Schedules** (Cadence calendar with objectives)
4. **Reporting Templates** (Executive summaries, technical updates, all-hands formats)
5. **Escalation Procedures** (Issue triage flows)
6. **Feedback Mechanisms** (Surveys, pulse checks, retrospectives)
7. **Crisis Communication Playbook** (If project is at risk)

Format output in structured Markdown with tables for matrices and calendars.
```text

### Expected Output

The AI returns a communication strategy document containing: stakeholder analysis and RACI, a communication matrix, a meeting and reporting cadence, escalation paths, feedback mechanisms, and, if needed, a crisis communication playbook ready to share with the project team and sponsors.

---

## Tips

- **Tailor Messaging to Decision Authority**: Executives want ROI and risk; end users want "What's in it for me?" (WIIFM). Never use the same message for both audiences.
- **Use RACI to Clarify Ownership**: Ambiguous accountability kills stakeholder trust. Make it explicit who owns each communication stream.
- **Schedule Communication Cadence BEFORE Project Start**: Don't improvise. Lock in meeting rhythms (weekly, bi-weekly, monthly) and publish a 6-month calendar.
- **Over-Communicate During Crisis**: If the project is at risk, triple your communication frequency. Silence breeds speculation and panic.
- **Measure Effectiveness, Not Just Activity**: Don't just track "emails sent." Track stakeholder satisfaction, survey scores, and "surprised by issue" incidents.
- **Leverage Asynchronous Tools for Offshore Teams**: Record Loom videos, use Miro for design reviews, and post meeting summaries in Confluence to bridge time zones.
- **Celebrate Wins Publicly**: Monthly pizza parties, shoutouts in newsletters, and "Contributor of the Month" awards build momentum and morale.

---

## Related Prompts

- **[change-management-coordinator](./change-management-coordinator.md)** - For deeper change management playbooks
- **[risk-management-analyst](./risk-management-analyst.md)** - For quantifying communication risks
- **[agile-sprint-planner](./agile-sprint-planner.md)** - For structuring communication around sprints

