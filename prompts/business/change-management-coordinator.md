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

---

## Description

Manages project changes effectively

---

## Use Cases

- Change Management for Project Manager persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

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

