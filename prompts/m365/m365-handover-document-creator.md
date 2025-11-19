---
title: "M365 Handover Document Creator"
description: "Generates a comprehensive handover document for role transitions or project transfers, ensuring no critical knowledge is lost."
category: "business"
tags: ["m365", "documentation", "handover", "knowledge-management", "onboarding"]
author: "GitHub Copilot"
version: "1.0"
date: "2025-11-18"
difficulty: "Beginner"
platform: "Microsoft 365 Copilot"
---

## Description

This prompt is essential for employees leaving a role, going on extended leave, or transferring a project. It interviews the user (via the prompt inputs) to extract key responsibilities, contacts, and outstanding tasks, then formats them into a professional handover guide.

## Goal

To create a structured, easy-to-read handover document that allows a successor to pick up work immediately with minimal friction.

## Inputs

- **Role/Project Name**: [role_name]
- **Key Responsibilities**: [key_responsibilities]
- **Outstanding Tasks**: [outstanding_tasks]
- **Key Contacts**: [key_contacts]
- **File Locations**: [file_locations]

## Prompt

You are an expert in Knowledge Management and Business Continuity. I am preparing a handover document for my successor.

Here are the details:

- **Role/Project**: [role_name]
- **My Key Responsibilities**: [key_responsibilities]
- **Pending/Outstanding Tasks**: [outstanding_tasks]
- **Key Stakeholders/Contacts**: [key_contacts]
- **Where files are stored**: [file_locations]

Please generate a formal **Handover Document** that includes:

1. **Executive Summary**: A high-level overview of the role/project scope.
2. **Daily/Weekly Routine**: A checklist of recurring duties.
3. **Action Plan**: A prioritized list of the "Outstanding Tasks" with clear next steps.
4. **Stakeholder Map**: Who to contact for what (based on [key_contacts]).
5. **Resource Library**: Links to the [file_locations] and other critical tools.

## Variables

- `[role_name]`: The job title or project being handed over.
- `[key_responsibilities]`: Bullet points of main duties.
- `[outstanding_tasks]`: Things that are currently in flight or need immediate attention.
- `[key_contacts]`: Names and roles of people the successor needs to know.
- `[file_locations]`: Paths to SharePoint sites, Teams channels, or shared drives.

## Example Usage

**Input:**

- `[role_name]`: "Q3 Marketing Campaign Lead"
- `[key_responsibilities]`: "Manage agency relationship, approve social copy, track budget."
- `[outstanding_tasks]`: "Approve final video edits by Friday, Pay invoice #1234."
- `[key_contacts]`: "Sarah (Agency Lead), Mike (Finance)."
- `[file_locations]`: "Teams Channel 'Marketing Q3', SharePoint/Budget/Invoices."

**Output:**

### Handover Document: Q3 Marketing Campaign Lead

**1. Executive Summary**
Lead responsibility for the Q3 campaign, focusing on agency management, content approval, and budget tracking.

**2. Recurring Duties**

- **Weekly**: Review social copy with Sarah (Agency).
- **Monthly**: Reconcile budget with Mike (Finance).

**3. Action Plan (Immediate Priorities)**

- **High Priority**: Approve final video edits. *Deadline: This Friday.*
- **Medium Priority**: Process Invoice #1234. *Location: SharePoint/Budget/Invoices.*

**4. Stakeholder Map**

- **Sarah (Agency Lead)**: Contact for creative assets and timelines.
- **Mike (Finance)**: Contact for budget approvals and invoices.

**5. Resource Library**

- **Project Files**: Teams Channel 'Marketing Q3'
- **Financials**: SharePoint/Budget/Invoices

## Tips

- Use this output as the body of a OneNote page or a Word document.
- Add a "Passwords/Access" section manually if relevant (but never put actual passwords in the prompt!).

## Related Prompts

- `m365-project-status-reporter`
- `process-optimization-consultant`

## Changelog

- 2025-11-18: Initial version created.
