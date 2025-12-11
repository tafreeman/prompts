---
title: "SOX Audit Preparer"
shortTitle: "SOX Audit Prep"
intro: "A prompt to assist in preparing for Sarbanes-Oxley (SOX) IT General Controls (ITGC) audits."
type: "how_to"
difficulty: "advanced"
audience:
  - "security-engineer"
  - "compliance-officer"
  - "it-manager"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "governance"
  - "compliance"
  - "finance"
  - "sox"
author: "Prompts Library Team"
version: "1.0"
date: "2025-12-11"
governance_tags:
  - "requires-human-review"
  - "compliance-critical"
dataClassification: "internal"
reviewStatus: "draft"
regulatory_scope:
  - "SOX"
  - "COBIT"
---
# SOX Audit Preparer

---

## Description

Helps IT and compliance teams prepare for Sarbanes-Oxley (SOX) audits, focusing on IT General Controls (ITGC). It covers key domains such as Access Control, Change Management, and IT Operations. The prompt guides users in gathering evidence, identifying control deficiencies, and drafting control descriptions.

---

## Use Cases

- Preparing for an annual SOX 404 audit
- Documenting ITGCs for a new financial system
- Self-assessing change management processes
- Reviewing user access reviews (UAR) for completeness
- Drafting remediation plans for audit findings

---

## Prompt

```text
You are an expert SOX IT Auditor. Assist the user in preparing for a SOX ITGC audit for the following control domain.

## Control Domain
[DOMAIN] (e.g., Access Control, Change Management, IT Operations)

## System Context
[SYSTEM_CONTEXT]

## Current Process/Control Description
[PROCESS_DESCRIPTION]

## Instructions
1.  Identify the key risks associated with this domain in a financial reporting context.
2.  Define the expected key controls based on COBIT/SOX best practices.
3.  Evaluate the provided process description for gaps or weaknesses.
4.  List the specific evidence (population, samples, screenshots) an external auditor would request.

## Output Format
- **Risk & Control Matrix (RCM) Draft**
- **Gap Analysis**
- **Evidence Request List**
```

---

## Variables

- `[DOMAIN]`: The specific ITGC domain (e.g., "Change Management").
- `[SYSTEM_CONTEXT]`: The financial application involved (e.g., "SAP ERP System used for General Ledger").
- `[PROCESS_DESCRIPTION]`: How the process currently works (e.g., "Developers write code, test it in dev, and then deploy it to production using a script. No formal approval ticket is used.").

---

## Example

```text
## SOX ITGC Assessment: Change Management for SAP

### Risk & Control Matrix (Draft)
*   **Risk:** Unauthorized changes to the ERP system could lead to financial misstatement.
*   **Control Activity:** Changes to production are approved by business owners and tested prior to migration.
*   **Frequency:** Per Change.
*   **Type:** Preventive / Manual.

### Gap Analysis
*   **Segregation of Duties (SoD) Conflict:** Developers have access to migrate code to production. This is a significant deficiency.
*   **Lack of Audit Trail:** "No formal approval ticket" means there is no evidence of authorization.

### Evidence Request List
1.  **Population:** List of all changes migrated to production in the audit period (system generated).
2.  **Sample Testing:** For 25 random changes, provide:
    *   Change Request Ticket.
    *   UAT Sign-off email/screenshot.
    *   Approval from Change Advisory Board (CAB).
    *   Evidence that the migrator was different from the developer.
```

---

## Tips

- **Segregation of Duties:** This is the #1 issue in SOX audits. Ensure developers cannot deploy to production.
- **Completeness and Accuracy (C&A):** Ensure reports used for evidence (like the list of changes) are system-generated and validated.
- **Financial Impact:** Focus only on systems that impact financial reporting, not all IT systems.

---

## Related Prompts

- [SOC 2 Audit Preparation](/prompts/governance/soc2-audit-preparation) — Prepare for SOC 2 Trust Services Criteria audits
- [Access Control Reviewer](/prompts/governance/access-control-reviewer) — Review user access and SoD conflicts
- [Compliance Policy Generator](/prompts/governance/compliance-policy-generator) — Draft IT policies aligned with SOX requirements
- [Vendor Security Review](/prompts/governance/vendor-security-review) — Assess third-party vendors with SOX-relevant controls
