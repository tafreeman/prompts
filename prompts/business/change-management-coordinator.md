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
effectivenessScore: 0.0
---
# Change Management Coordinator

---

## Description

Helps project and program leaders manage change requests in a structured, repeatable way. Guides you through impact analysis, approval workflows, stakeholder communication, and implementation planning so changes land smoothly instead of creating chaos.

---

## Use Cases

- Managing scope changes in large transformation or migration projects
- Coordinating change requests across multiple teams or vendors
- Preparing materials for Change Advisory Board (CAB) reviews
- Standardizing how change impact is documented across projects
- Turning ad-hoc change emails into formal, trackable change records

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

---

## Example

### Context

You are running a CRM migration from Salesforce to Microsoft Dynamics 365. A late-breaking change request would significantly impact Q4 sales operations and requires a clear impact analysis, approval path, and communication plan.

### Input

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

### Expected Output

The AI returns a structured change request package that includes: a concise executive summary of the proposed change, a quantified impact analysis (timeline, cost, risk, and resource implications), a step-by-step approval workflow, stakeholder-specific communication messages, a phased implementation plan with owners and dates, and measurable success criteria you can track after implementation.

---

## Tips

- **Avoid Q4 disruption**: Schedule major CRM changes during slower business periods (January is ideal for many organizations)
- **Train early, train often**: Give users 2+ weeks in sandbox before go-live to build muscle memory
- **Test integrations rigorously**: 80% of migration failures come from third-party connectors, not core data migration
- **Build rollback plans**: Always have a "return to old system" script ready for first 48 hours post-migration
- **Over-communicate**: Send 3x more updates than you think necessary—change anxiety is real
- **Budget 15% contingency**: Migrations always have unforeseen costs (API limits, additional licenses, custom development)
- **Celebrate wins**: Recognize early adopters and power users to build positive momentum

---

## Related Prompts

- **[agile-sprint-planner](./agile-sprint-planner.md)** - Plan migration work in 2-week sprints
- **[stakeholder-communication-manager](./stakeholder-communication-manager.md)** - Craft executive updates and user notifications
- **[risk-management-analyst](./risk-management-analyst.md)** - For change-related risk assessment
- **[Gap Analysis Expert](../analysis/gap-analysis-expert.md)** - For current/future state assessment
- **[Process Optimization Consultant](../analysis/process-optimization-consultant.md)** - For process improvements during change

