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
```text

---

## Variables

- `[project_name]`: Project name and scope (e.g., "SAP S/4HANA Implementation - Finance & Supply Chain Modules")
- `[stakeholders]`: List of stakeholder groups with roles (e.g., "CFO (Sponsor), VP Supply Chain (Key User), IT Director, Warehouse Staff (End Users)")
- `[phase]`: Current project phase (e.g., "Blueprinting/Design", "UAT", "Go-Live", "Post-Production Support")
- `[challenges]`: Specific communication obstacles (e.g., "Resistance to change from warehouse staff, CFO demanding faster ROI visibility, offshore vendor language barriers")


---

## Example Usage

**Input:**

```text
Project: SAP S/4HANA Implementation (Finance & Supply Chain Modules)
Stakeholders:
- CFO (Executive Sponsor)
- VP Supply Chain (Key Business User)
- IT Director (Technical Owner)
- Finance Manager (Subject Matter Expert)
- Warehouse Staff (50 end users across 3 sites)
- SAP Consulting Partner (Offshore team in India)

Phase: Blueprinting / Design (Month 3 of 18-month project)

Challenges:
- Resistance to change from warehouse staff (fear of job automation)
- CFO demanding weekly ROI metrics and faster go-live (pressure to cut timeline from 18 to 12 months)
- Language barriers with offshore SAP consultants causing design misalignments
- Finance Manager overwhelmed by day-to-day responsibilities + project duties
```text
**Output:**

```markdown
# Stakeholder Communication Strategy: SAP S/4HANA Implementation

## 1. Stakeholder Analysis

### Power/Interest Matrix

| Stakeholder | Power | Interest | Strategy |
| :--- |-------| :--- |----------|
| CFO | High | High | **Manage Closely** - Weekly exec summary, focus on ROI/milestones |
| VP Supply Chain | High | High | **Manage Closely** - Bi-weekly design reviews, process walkthroughs  |
| IT Director | Medium | High | **Keep Informed** - Technical steering committee, architecture decisions |
| Finance Manager | Low | High | **Keep Informed** - Weekly SME sessions, workload balancing |
| Warehouse Staff | Low | High | **Keep Satisfied** - Monthly town halls, WIIFM messaging, training roadmap |
| SAP Partner | Medium | Medium | **Monitor** - Daily standups via Zoom, design walkthrough recordings |

### RACI Matrix (Communication Ownership)

| Activity | CFO | VP SC | IT Dir | Fin Mgr | Staff | Partner |
| :--- |-----| :--- |--------| :--- |-------| :--- |
| Exec Status Report | **A** | I | I | I | :--- | - |
| Blueprint Approval | **A** | **R** | **C** | **C** | I | **C** |
| Change Management | **A** | **R** | **C** | I | **C** | :--- |
| Technical Design | I | **C** | **A/R** | I | :--- | **C** |
| Go-Live Decision | **A** | **R** | **C** | I | I | I |

*R=Responsible, A=Accountable, C=Consulted, I=Informed*

---

## 2. Communication Matrix

| Stakeholder | Message Type | Frequency | Channel | Objective | Owner |
| :--- |-------------| :--- |---------| :--- |-------|
| **CFO** | Executive Summary | Weekly (Fri 4pm) | Email + 15min call | ROI tracking, risk flagging, decision requests | PM |
| **CFO** | Steering Committee | Monthly (1st Tue) | In-person meeting | Strategic alignment, budget approval | PM |
| **VP Supply Chain** | Design Review | Bi-weekly (Wed 2pm) | Teams + Miro | Blueprint validation, process signoff | Business Analyst |
| **IT Director** | Technical Steering | Bi-weekly (Thu 10am) | Teams | Architecture decisions, integration updates | Solution Architect |
| **Finance Manager** | SME Session | Weekly (Mon 9am) | Teams | Gather requirements, review test scenarios | Business Analyst |
| **Warehouse Staff** | Town Hall | Monthly (Last Fri) | On-site + Webex | Answer questions, demo system, training updates | Change Manager |
| **SAP Partner** | Daily Standup | Daily (8am IST) | Zoom | Sprint progress, blockers, clarifications | Scrum Master |
| **All** | Project Newsletter | Bi-weekly (Thu) | Email | Milestone updates, wins, upcoming events | Communications Lead |

---

## 3. Meeting Schedules (Cadence Calendar)

### Executive Layer (CFO)

**Weekly Executive Brief (Fridays, 4:00 PM ET, 15 min)**
- **Format**: Email dashboard + optional phone call
- **Content**: 
  - Traffic light status (scope, schedule, budget)
  - Top 3 wins this week
  - Top 3 risks/blockers
  - Decision requests (if any)
- **Sample Email Subject**: "SAP Exec Brief W12: Blueprint 75% Complete, Budget Green, CFO Approval Needed for Seat Licenses"

**Monthly Steering Committee (1st Tuesday, 10:00 AM ET, 90 min)**
- **Attendees**: CFO, VP Supply Chain, IT Director, PM, Sponsor
- **Agenda**:
  1. Previous month recap (10 min)
  2. Financial deep dive (20 min) — Burn rate, variance analysis
  3. Risk register review (20 min) — Top 5 risks, mitigation status
  4. Go/No-Go decisions (30 min) — Phase gate approvals
  5. Strategic pivots (10 min) — Scope changes, timeline adjustments
- **Deliverable**: Approved decision log, updated project charter

---

### Operational Layer (VP, IT, SMEs)

**Bi-Weekly Design Review (Wednesdays, 2:00 PM ET, 60 min)**
- **Attendees**: VP Supply Chain, Finance Manager, Business Analyst, SAP Partner Lead
- **Agenda**:
  1. Blueprint walkthrough (30 min) — Procure-to-Pay, Order-to-Cash flows
  2. Gap analysis (15 min) — Custom vs. standard functionality
  3. Action items review (15 min) — Open questions, dependencies
- **Deliverable**: Signed blueprint sections, change request log

**Weekly SME Sessions (Mondays, 9:00 AM ET, 60 min)**
- **Attendees**: Finance Manager, Business Analyst
- **Purpose**: Deep dive into finance module requirements (GL, AP, AR, Asset Accounting)
- **Note**: Limit to 3 hours/week max to prevent SME burnout. Use asynchronous Loom videos for non-critical items.

---

### Change Management & Training (Warehouse Staff)

**Monthly Town Hall (Last Friday, 3:00 PM ET, 45 min)**
- **Location**: Warehouse breakroom + Webex for remote shifts
- **Agenda**:
  1. "What's New" (10 min) — Progress update in plain English
  2. System Demo (15 min) — Show new barcode scanning workflow
  3. Q\u0026A (15 min) — Address fears (\"Will I lose my job?\")
  4. Training Preview (5 min) — Upcoming hands-on sessions
- **Key Message Theme**: "This system makes YOUR job easier, NOT obsolete."

**Quarterly Survey (Anonymous)**
- **Tool**: Microsoft Forms
- **Questions**:
  1. How well do you understand the project? (1-5 scale)
  2. What's your #1 concern?
  3. What communication method works best for you? (Email/Town Hall/Manager 1-on-1)
- **Action**: Address top 3 concerns in next town hall

---

## 4. Reporting Templates

### Executive Summary (Weekly to CFO)

**SAP S/4HANA Executive Brief - Week 12**

**Overall Status**: 🟢 Green

| Dimension | Status | Detail |
| :--- |--------| :--- |
| Scope | 🟢 | Blueprint 75% complete (Finance done, Supply Chain in review) |
| Schedule | 🟡 | 2 days behind due to offshore holiday. Plan to recover via weekend catch-up session. |
| Budget | 🟢 | $1.2M spent of $8M (15% utilization, on track for Phase 1) |
| Risks | 🟡 | Risk #3 elevated: Warehouse staff morale declining (see mitigation below) |

**This Week's Wins**:
1. ✅ Finance blueprint approved by CFO (blueprint-v2.pdf attached)
2. ✅ Secured 20 additional SAP licenses for contractors
3. ✅ Warehouse staff training roadmap finalized

**Top 3 Risks**:
1. **🔴 Critical**: CFO pushing for 12-month timeline (vs. 18-month plan). **Mitigation**: Schedule impact analysis meeting for Tuesday.
2. **🟡 Medium**: Language barriers with offshore team causing re-work. **Mitigation**: Added daily Zoom call + Loom video summaries.
3. **🟡 Medium**: Warehouse staff resistance increasing (survey shows 40% fear automation). **Mitigation**: Change manager conducting 1-on-1s, emphasizing job security.

**Decision Needed**:
- Approve $150K for additional training budget (3-day onsite sessions vs. 1-day webinars). ROI: Reduces post-go-live support costs by est. $300K.

---

### Technical Update (Bi-Weekly to IT Director)

**SAP Technical Steering - Sprint 6**

**Infrastructure**:
- ✅ Azure environment provisioned (2x App Servers, 1x DB Server, 1x Gateway)
- ⏳ SSO integration with Azure AD (80% complete, pending SAML cert from Security team)

**Integrations**:
- ⏳ **Salesforce ↔ SAP**: Order sync API design in review (ComplexityScore: 8/10, needs architect approval)
- ✅ **PowerBI ↔ SAP**: OData connectors configured, real-time dashboards operational

**Technical Debt**:
- 🔴 Legacy inventory system (AS/400) doesn't support REST APIs. **Options**: 1) Build custom middleware (4 weeks, $80K), 2) Manual CSV exports (no cost, high risk).

---

### All-Hands Newsletter (Bi-Weekly)

**SAP Update: November Edition 🚀**

**What's Happening?**
We're 3 months into our SAP journey! The Finance module blueprint is DONE, and we're now designing how you'll use the system in the warehouse.

**Cool Demo**: Check out this 2-minute video showing how the new barcode scanner eliminates paper clipboards: [Loom Link]

**Upcoming**:
- **Dec 5-9**: Hands-on training for Warehouse Team A (sign up by Nov 28)
- **Dec 15**: Holiday pizza party + Q\u0026A with the SAP Partner team

**Your Voice Matters**: We read every survey response. This month, you asked for more "show, don't tell" — that's why we're adding monthly demos!

---

## 5. Escalation Procedures

### Issue Triage Flow

| Issue Severity | Response Time | Escalation Path | Example |
| :--- |--------------| :--- |---------|
| **P0 - Critical** | Immediate (< 1 hour) | PM → IT Director → CFO | Production outage, data loss, security breach |
| **P1 - High** | Same day (< 4 hours) | PM → Steering Committee | Major design conflict, vendor delay \u003e 5 days |
| **P2 - Medium** | Next business day | PM handles | Minor scope change, offshore communication issue |
| **P3 - Low** | Within 1 week | Team handles | Documentation typo, training schedule tweak |

### Crisis Communication Playbook (If Project at Risk)

**Trigger**: If **2 or more** of these occur in same week:
- Schedule slips \u003e 2 weeks
- Budget overrun \u003e 10%
- Key stakeholder threatens to pull support
- Vendor misses critical deliverable

**Immediate Actions (Within 24 hours)**:
1. **Emergency Steering Committee** (CFO, PM, Sponsor)
   - Root cause analysis
   - Go/No-Go decision framework
   - Communication lockdown (no external updates until alignment)
2. **Stakeholder Notification Matrix**:
   - **CFO**: Phone call (PM) + written brief within 2 hours
   - **VP/IT**: In-person meeting (PM) + recovery plan draft
   - **Staff/Partner**: Hold all updates until recovery plan approved
3. **Media Strategy** (If public company):
   - Route all inquiries to Corporate Comms
   - Standard holding statement: "We are addressing a technical challenge and will update stakeholders on [date]."

**Recovery Communication Cadence**:
- **Week 1**: Daily exec updates (15 min standup)
- **Week 2-4**: Return to weekly cadence once green light confirmed

---

## 6. Feedback Mechanisms

### Quarterly Stakeholder Pulse Check

**Survey Tool**: Microsoft Forms (anonymous)
**Distribution**: Email to all stakeholders (100% response target)
**Questions**:
1. How satisfied are you with project communication? (1-5)
2. What communication channel is MOST valuable? (Email/Meetings/Newsletter/Town Hall)
3. What's ONE thing we should START/STOP/CONTINUE doing?
4. Open feedback box

**Action Plan**:
- Review results in next Steering Committee
- Address top 2 concerns within 2 weeks
- Publish "You Said, We Did" summary in newsletter

---

### Retrospectives (After Each Phase Gate)

**Attendees**: Core project team (PM, BA, Architect, Change Manager)
**Format**: Start/Stop/Continue + Action Items
**Sample Output (Post-Blueprint Phase)**:
- **START**: Recording design sessions for offshore team to review async
- **STOP**: 2-hour meetings (fatigue is real — break into 60-min chunks)
- **CONTINUE**: Executive summaries (CFO loves the traffic light format)

**Transparency**: Share sanitized retrospective notes in next newsletter to show team is listening.

---

## Success Metrics

**Communication Effectiveness KPIs (Track Monthly)**:

| Metric | Target | Actual (Month 3) | Trend |
| :--- |--------| :--- |-------|
| Stakeholder Survey Score | \u003e 4.0/5.0 | 3.8/5.0 | 🔴 (Needs improvement) |
| Meeting On-Time Start Rate | \u003e 90% | 85% | 🟡 (Offshore time zone issues) |
| Email Open Rate (Newsletters) | \u003e 70% | 82% | 🟢 (High engagement) |
| Town Hall Attendance | \u003e 80% of staff | 65% | 🔴 (Friday fatigue — move to Thursdays?) |
| CFO "Surprised by Issue" Count | 0 | 1 (warehouse resistance) | 🟡 (Improve early warning) |

**Improvement Actions**:
- Survey score: Add more "show, don't tell" demos per warehouse feedback
- Meeting punctuality: Send Outlook invites with time zone converters for offshore team
```text

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
- **project-charter-creator** - For initial stakeholder identification
