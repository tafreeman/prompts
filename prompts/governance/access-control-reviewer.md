---
title: Access Control Reviewer
shortTitle: Access Review
intro: A prompt to assist in conducting User Access Reviews (UAR) and analyzing role-based
  access control (RBAC) policies.
type: how_to
difficulty: intermediate
audience:

- security-analyst
- iam-engineer
- auditor

platforms:

- claude
- chatgpt
- github-copilot

topics:

- governance
- security
- iam
- access-control

author: Prompts Library Team
version: '1.0'
date: '2025-12-11'
governance_tags:

- requires-human-review
- security-critical

dataClassification: internal
reviewStatus: draft
regulatory_scope:

- SOX
- ISO-27001
- NIST-800-53

effectivenessScore: 0.0
---

# Access Control Reviewer

---

## Description

Assists in the periodic review of user access rights and the design of Role-Based Access Control (RBAC) models. It helps identify toxic combinations of permissions (SoD conflicts), over-privileged users, and dormant accounts.

---

## Use Cases

- Quarterly User Access Review (UAR) campaigns
- Designing new IAM roles for a system
- Auditing privileged access (admin accounts)
- Cleaning up access after a reorganization
- Identifying Segregation of Duties (SoD) conflicts

---

## Prompt

```text
You are an Identity and Access Management (IAM) Expert. Review the provided access list or role definition for security risks and best practices.

## Context
**System:** [SYSTEM_NAME]
**Review Type:** [REVIEW_TYPE] (e.g., Periodic Access Review, Role Design)

## Data / Policy
[DATA] (e.g., List of users and roles, or JSON policy definition)

## Instructions

1.  Analyze for Principle of Least Privilege violations.
2.  Identify potential Segregation of Duties (SoD) conflicts (e.g., can create and approve).
3.  Flag generic or shared accounts.
4.  Suggest improvements to the role structure.

## Output Format

- **Risk Analysis**
- **SoD Conflicts**
- **Cleanup Recommendations**

```

---

## Variables

- `[SYSTEM_NAME]`: The system being reviewed (e.g., "AWS Production Account").
- `[REVIEW_TYPE]`: The goal of the review.
- `[DATA]`: The raw data to analyze.

---

## Example

```text
## Access Review: AWS Production Account

### Risk Analysis

*   **Over-privileged Users:** User `jdoe` has `AdministratorAccess` policy attached directly. Best practice is to use groups/roles.
*   **Shared Account:** Found user `devops-shared`. Shared accounts destroy non-repudiation and should be removed.
*   **MFA Missing:** 3 users with write access do not have MFA enabled.

### SoD Conflicts

*   **Conflict:** Role `Deployer` has `iam:CreateUser` AND `ec2:RunInstances`. This allows a user to create a backdoor admin account and launch resources.
    *   *Recommendation:* Separate IAM administration from Infrastructure management.

### Cleanup Recommendations

1.  Delete `devops-shared` account immediately.
2.  Remove `AdministratorAccess` from `jdoe` and assign a specific role (e.g., `NetworkAdmin`).
3.  Enforce MFA for all IAM users via policy.

```

---

## Tips

- **Least Privilege:** Start with zero access and add only what is needed.
- **SoD:** Look for combinations that allow someone to complete a sensitive transaction alone (e.g., Create Vendor + Pay Vendor).
- **Just-in-Time (JIT):** Consider recommending temporary access for admins instead of permanent standing access.

---

## Related Prompts

- [SOC 2 Audit Preparation](/prompts/governance/soc2-audit-preparation) — Prepare for SOC 2 audits including access control requirements
- [SOX Audit Preparer](/prompts/governance/sox-audit-preparer) — Prepare for SOX ITGC audits with access control focus
- [Data Classification Helper](/prompts/governance/data-classification-helper) — Classify data to determine appropriate access levels
- [Security Incident Response](/prompts/governance/security-incident-response) — Handle access-related security incidents
