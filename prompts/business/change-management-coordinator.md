---
title: "Change Management Coordinator"
shortTitle: "Change Management"
intro: "Manages project changes with impact analysis, approval workflow, communication strategy, and implementation planning."
type: "how_to"
difficulty: "intermediate"
audience:
  - "project-manager"
  - "business-analyst"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "change-management"
  - "project-management"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
governance_tags:
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Change Management Coordinator

<<<<<<< HEAD

=======
>>>>>>> main
---

## Description

Manages project changes effectively

<<<<<<< HEAD

=======
>>>>>>> main
---

## Use Cases

- Change Management for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

<<<<<<< HEAD

=======
>>>>>>> main
---

## Prompt

```text
Manage change for:

Project: [project_name]
Proposed Changes: [changes]
Impact Assessment: [impact]
Stakeholder Concerns: [concerns]

Provide:
1. Change impact analysis
2. Approval workflow
3. Communication strategy
4. Implementation plan
5. Risk mitigation
6. Success measurement
```text

---

## Variables

- `[project_name]`: Project name (e.g., "CRM System Migration", "Cloud Infrastructure Upgrade", "ERP Implementation Phase 2")
- `[changes]`: Proposed changes (e.g., "Migration from Salesforce to Microsoft Dynamics 365, affecting 500 users across 3 departments")
- `[impact]`: Impact assessment (e.g., "2-week data migration window, 40 hours training required, $200K budget impact")
- `[concerns]`: Stakeholder concerns (e.g., "Sales team worried about data loss during Q4, IT concerned about integration with legacy inventory system")

<<<<<<< HEAD

=======
>>>>>>> main
---

## Example Usage

**Input:**

```text
Manage change for:

Project: CRM System Migration (Salesforce → Microsoft Dynamics 365)
Proposed Changes: Migrate 500 users (Sales, Marketing, Customer Success) from Salesforce to Dynamics 365. Includes data migration (10 years of customer records, 2.5M contacts), custom workflow recreation, and third-party integrations (Mailchimp, DocuSign, PowerBI).
Impact Assessment: 2-week migration window (Dec 10-23), 40 hours training per department, $200K implementation cost, temporary loss of mobile access during cutover.
Stakeholder Concerns: 
- Sales VP: "We can't lose pipeline visibility during Q4 close"
- Marketing Director: "Our email campaigns are tightly integrated with Salesforce"
- IT Director: "Dynamics 365 doesn't natively support our legacy inventory system API"
- CFO: "$200K budget not approved; need cost justification"

Provide:
1. Change impact analysis
2. Approval workflow
3. Communication strategy
4. Implementation plan
5. Risk mitigation
6. Success measurement
```text
<<<<<<< HEAD
=======

>>>>>>> main
**Output:**

```markdown
# Change Management Plan: CRM System Migration

## 1. Change Impact Analysis

### Business Impact
- **High Risk**: Q4 sales cycle disruption (Nov-Dec revenue: $4.2M at risk)
- **Medium Risk**: Marketing campaign delays (20 active campaigns, 50K contacts/week)
- **Medium Risk**: Customer success team productivity loss (15% estimated during training)

### Technical Impact
- **Data Migration**: 10 years customer history (2.5M contacts, 500K opportunities, 1.8M activities)
- **Integration Changes**: 8 third-party tools require reconfiguration
- **Custom Logic**: 42 Salesforce workflows need Dynamics 365 equivalents
- **API Compatibility**: Legacy inventory system (built 2015) lacks Dynamics connector

### Financial Impact
| Item | Cost | Timeline |
| :--- |------| :--- |
| Dynamics 365 licenses (500 users) | $60K/year | Ongoing |
| Implementation services | $120K | One-time |
| Training (120 hours @ $150/hr) | $18K | Dec-Jan |
| Integration development | $35K | Nov-Dec |
| Contingency (15%) | $30K | :--- |
| **Total** | **$263K** | :--- |

**ROI Justification**: Salesforce renewal ($85K/year) + PowerBI premium ($24K/year) eliminated. Break-even in 24 months.

---

## 2. Approval Workflow

### Phase 1: Executive Steering (Nov 1-7)
- [x] Present business case to CFO (cost justification, ROI)
- [ ]  VP Sales approval (with Q4 mitigation plan)
- [ ] CTO sign-off (technical architecture review)
- Decision:  Proceed with Jan 2026 migration (avoid Q4 conflict)

### Phase 2: Stakeholder Alignment (Nov 8-15)
- [ ] Sales team workshop: Demo Dynamics mobile CRM, pipeline view
- [ ] Marketing alignment: Test Mailchimp + Dynamics integration in sandbox
- [ ] IT technical review: Evaluate legacy inventory API workarounds (middleware vs custom connector)

### Phase 3: Budget Approval (Nov 16-22)
- [ ] Finance Committee presentation (3-year TCO analysis)
- [ ] Contingency approval ($30K reserve for unforeseen issues)

---

## 3. Communication Strategy

### Internal Communications

**Week 1 (Nov 1-7)**: Executive Announcement
- **Audience**: All 500 users
- **Channel**: CEO email + town hall
- **Message**: "Why we're moving to Dynamics 365" (vision, timeline, benefits)

**Week 2-4 (Nov 8-30)**: Department-Specific Briefings
- **Sales (250 users)**: VP-led roadshow, address Q4 concerns, demo mobile CRM
- **Marketing (150 users)**: Integration testing results, campaign migration plan
- **Customer Success (100 users)**: Training schedule, support ticket process

**Week 5-8 (Dec 1-31)**: Training \u0026 Preparation
- **Format**: 4-hour hands-on workshops per department
- **Schedule**: 
  - Sales: Dec 5-9 (5 sessions, 50 users each)
  - Marketing: Dec 12-16
  - Customer Success: Dec 19-23
- **Materials**: Video tutorials, quick reference guides, sandbox access

**Migration Week (Jan 6-10, 2026)**: Daily Standup Updates
- **Format**: 15-min Slack updates (08:00, 12:00, 17:00)
- **Content**: Migration progress, known issues, support hotline

**Post-Launch (Jan 13+)**: Ongoing Support
- **Week 1-2**: Dedicated support team (8am-8pm)
- **Week 3-4**: Office hours (M/W/F 10-2pm)
- **Month 2+**: Standard IT helpdesk

### External Communications (if needed)
- **Customers**: No impact (external-facing systems unchanged)
- **Vendors**: Notify Mailchimp, DocuSign of integration changes (Oct 15 notice)

---

## 4. Implementation Plan

### Pre-Migration (Nov 1 - Dec 31, 2025)

**Technical Setup**
- [x] Dynamics 365 tenant provisioned
- [ ] Sandbox environment configured (Nov 15)
- [ ] Security roles mapped (Salesforce → Dynamics)
- [ ] Data migration scripts tested (3 sandbox runs)

**Integration Development**
- [ ] Mailchimp connector: Nov 1-15 (vendor-supported)
- [ ] DocuSign connector: Nov 15-30 (custom OAuth flow)
- [ ] PowerBI reports: Dec 1-15 (rebuild dashboards)
- [ ] Legacy inventory API: Dec 16-30 (middleware via Azure Logic Apps)

**Training Prep**
- [ ] Dynamics 365 training materials: Nov 20
- [ ] Sandbox access for all users: Dec 1
- [ ] Pre-training knowledge test (baseline): Dec 1

### Migration (Jan 6-10, 2026)

| Day | Activity | Owner | Rollback Point |
| :--- |----------| :--- |----------------|
| Mon | Data export (contacts, accounts, opportunities) | IT | Salesforce remains live |
| Tue | Data import + validation (2.5M records) | Vendor | Revert to Salesforce |
| Wed | Integration testing (all 8 connectors) | IT | Still reversible |
| Thu | User Acceptance Testing (50 power users) | Business | Final rollback window |
| Fri | Go-live (500 users) | All | Full cutover, no rollback |

### Post-Migration (Jan 13+, 2026)

**Week 1-2: Hypercare**
- Dedicated war room (Slack, Teams, hotline)
- Daily triage meetings (8am standup)
- Bug fix prioritization (P0/P1 within 4 hours)

**Week 3-4: Stabilization**
- Resolve top 20 reported issues
- Publish FAQ based on tickets
- Optimize slow queries/reports

**Month 2: Optimization**
- Benchmark adoption (login frequency, feature usage)
- Sunset Salesforce (export archive, cancel licenses)
- Conduct lessons learned retrospective

---

## 5. Risk Mitigation

### Critical Risks

| Risk | Probability | Impact | Mitigation | Contingency Plan |
| :--- |-------------| :--- |------------| :--- |
| **Q4 sales disruption** | High | Critical ($4.2M) | Move to Jan 2026 (avoid Q4) | If Jan slips, use hybrid mode (Dynamics + Salesforce read-only) |
| **Data loss during migration** | Low | Critical | 3 sandbox tests, full backup | Rollback script ready (restore from backup in 4 hours) |
| **Legacy inventory API incompatible** | Medium | High | Build Azure Logic Apps middleware | Manual CSV export/import (temp workaround for 2 weeks) |
| **User adoption resistance** | Medium | Medium | 40 hours training, sandbox practice | Extend support period to 8 weeks, add champions program |
| **Integration failures (Mailchimp, DocuSign)** | Low | Medium | Pre-test in sandbox 4 weeks early | Manual workarounds documented, escalate to vendors |
| **Budget overrun ($263K)** | Medium | Low | 15% contingency included | Phase 2 integrations (defer non-critical to Feb) |

### Monitoring Triggers
- **Red Alert**: >10% data mismatch after import → Halt go-live, investigate
- **Yellow Alert**: >50% of users not logged in Day 1 → Extend training, send reminders
- **Green Light**: <5% helpdesk tickets on Day 3 → Reduce war room hours

---

## 6. Success Measurement

### KPIs (30/60/90 Days)

| Metric | Baseline (Salesforce) | Target (30d) | Target (90d) | Measurement |
| :--- |----------------------| :--- |--------------| :--- |
| **User Adoption** | 100% | 95% active logins | 98% | Dynamics analytics |
| **Sales Productivity** | 42 opps/rep/month | 38 (training ramp) | 45 (+7%) | Pipeline reports |
| **Support Tickets** | 5/week (Salesforce) | <20/week | <8/week | IT helpdesk |
| **System Uptime** | 99.7% | 99.5% | 99.8% | Azure monitor |
| **Data Accuracy** | 95% | 97% (cleanup) | 98% | Quality audits |
| **Cost Savings** | $109K/year | :--- | -$13K (net first year) | Finance tracking |

### Qualitative Success Indicators
- Sales VP: "Mobile CRM improves field productivity" (survey at 60 days)
- Marketing: "Mailchimp sync reduces manual work by 8 hours/week"
- Customer Success: "Better case tracking via Dynamics service module"

### Lessons Learned Session (Day 90)
- Retrospective with all stakeholders
- Document wins, challenges, process improvements
- Update change management playbook for future migrations
```text

---

## Tips

- **Avoid Q4 disruption**: Schedule major CRM changes during slower business periods (January is ideal for many organizations)
- **Train early, train often**: Give users 2+ weeks in sandbox before go-live to build muscle memory
- **Test integrations rigorously**: 80% of migration failures come from third-party connectors, not core data migration
- **Build rollback plans**: Always have a "return to old system" script ready for first 48 hours post-migration
- **Over-communicate**: Send 3x more updates than you think necessary—change anxiety is real
- **Budget 15% contingency**: Migrations always have unforeseen costs (API limits, additional licenses, custom development)
- **Celebrate wins**: Recognize early adopters and power users to build positive momentum

<<<<<<< HEAD

=======
>>>>>>> main
---

## Related Prompts

- **[agile-sprint-planner](./agile-sprint-planner.md)** - Plan migration work in 2-week sprints
- **[stakeholder-communication-manager](./stakeholder-communication-manager.md)** - Craft executive updates and user notifications
<<<<<<< HEAD
- **risk-assessment-analyst** - Quantify migration risks with probability models
- **data-migration-architect** - Technical ETL strategy for CRM data migration
=======
>>>>>>> main
