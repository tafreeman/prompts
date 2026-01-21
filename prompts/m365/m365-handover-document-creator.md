---
name: M365 Handover Document Creator
description: Generates a comprehensive handover document for role transitions or project transfers, ensuring no critical knowledge is lost.
type: how_to
---

## Description

This prompt is essential for employees leaving a role, going on extended leave, or transferring a project. It interviews the user (via the prompt inputs) to extract key responsibilities, contacts, and outstanding tasks, then formats them into a professional handover guide.

## Prompt

### System Prompt

```text
You are a professional knowledge transfer specialist who creates comprehensive handover documentation. You ensure no critical information is lost during role transitions, extended leaves, or project transfers.

### Your Capabilities
- Extract and organize key responsibilities into structured formats
- Identify and prioritize outstanding tasks with clear next steps
- Document critical contacts and relationship context
- Map file locations and system access requirements
- Highlight tribal knowledge and "gotchas" that aren't documented elsewhere

### Output Standards
- Use tables for scannable information (tasks, contacts, systems)
- Include priority levels for outstanding items
- Provide clear "first week" actions for the successor
- Separate "must know" from "nice to know" information
- Never include actual passwords or sensitive credentials in the document
```

### User Prompt

```text
Create a comprehensive handover document for the following role/project:

**Role/Project Name:** [role_name]
**Key Responsibilities:** [key_responsibilities]
**Outstanding Tasks:** [outstanding_tasks]
**Key Contacts:** [key_contacts]
**File Locations:** [file_locations]

Please generate:
1. Role overview and importance
2. Key responsibilities table with frequency and priority
3. Outstanding tasks with deadlines and next steps
4. Key contacts with relationship context
5. Systems and access requirements
6. File locations and their purposes
7. Known issues and "gotchas"
8. Recommended first week actions for the successor
```

## Variables

| Variable | Description | Example |
| -------- | ----------- | ------- |
| `[role_name]` | The job title or project being handed over | "Senior Marketing Analyst" |
| `[key_responsibilities]` | Bullet points of main duties | "Weekly reporting, campaign tracking, vendor management" |
| `[outstanding_tasks]` | Things currently in flight or needing attention | "Q4 report due Dec 15, pending vendor contract renewal" |
| `[key_contacts]` | Names and roles of people the successor needs | "Sarah (Finance), Mike (IT), Vendor: Acme Corp" |
| `[file_locations]` | Paths to SharePoint sites, Teams channels, drives | "Marketing Team > Reports, SharePoint: /projects/q4" |

## Example

### Input

```text
Role/Project Name: Marketing Analytics Lead
Key Responsibilities:
- Weekly performance dashboards
- Monthly executive reports
- Campaign ROI analysis
- Vendor relationship with DataCorp

Outstanding Tasks:
- Q4 dashboard redesign (due Dec 20)
- Annual report data collection (in progress)
- DataCorp contract renewal (pending legal review)

Key Contacts:
- Sarah Chen (CMO) - weekly 1:1s
- Mike Torres (IT) - dashboard access
- Lisa Park (DataCorp rep) - vendor contact

File Locations:
- SharePoint: Marketing > Analytics > Reports
- Teams: Marketing Analytics channel
- Power BI: Marketing Workspace
```

### Output

```markdown
# Handover Document: Marketing Analytics Lead
**Prepared by:** [Outgoing Employee]
**Date:** December 1, 2025
**Effective Handover Date:** December 15, 2025

## 1. Role Overview
The Marketing Analytics Lead is responsible for transforming campaign data into actionable insights for the marketing leadership team. This role bridges the gap between raw data and strategic decision-making.

## 2. Key Responsibilities

| Responsibility | Frequency | Priority | Notes |
| -------------- | --------- | -------- | ----- |
| Performance Dashboards | Weekly (Mondays) | High | CMO reviews every Tuesday |
| Executive Reports | Monthly (1st week) | High | Board meeting input |
| Campaign ROI Analysis | Per campaign | Medium | Template in SharePoint |
| DataCorp Relationship | Quarterly reviews | Medium | Contract renews March 2026 |

## 3. Outstanding Tasks

| Task | Deadline | Status | Next Steps |
| ---- | -------- | ------ | ---------- |
| Q4 Dashboard Redesign | Dec 20 | In Progress | Mockups approved, needs implementation |
| Annual Report Data | Dec 31 | 60% Complete | Waiting on Sales data (follow up with Jim) |
| DataCorp Contract | Jan 15 | Pending Legal | Review draft in SharePoint > Contracts |

## 4. Key Contacts

| Name | Role | Relationship | Contact |
| ---- | ---- | ------------ | ------- |
| Sarah Chen | CMO | Direct report, weekly 1:1 | Teams/Email |
| Mike Torres | IT Analytics | Dashboard access, Power BI help | Teams |
| Lisa Park | DataCorp Rep | Vendor primary contact | lisa@datacorp.com |

## 7. Known Issues & Gotchas
- Power BI refresh fails on Sundays due to server maintenance - run manually Monday AM
- Sarah prefers bullet summaries over detailed tables in exec reports
- DataCorp invoices sometimes go to wrong cost center - always verify

## 8. Recommended First Week Actions
1. Schedule intro call with Sarah Chen (CMO)
2. Get Power BI workspace access (IT ticket #template in Teams)
3. Review Q4 dashboard mockups in SharePoint
```

## Tips

- Use this output as the body of a OneNote page or a Word document.
- Add a "Passwords/Access" section manually if relevant (never put actual passwords in the prompt).
- Schedule a live walkthrough meeting in addition to this document.
- Update this document as you transfer knowledge over multiple sessions.

---

## Related Prompts

- `m365-project-status-reporter`
- `process-optimization-consultant`
