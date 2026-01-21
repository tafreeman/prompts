---
name: Access Control Reviewer
description: A prompt to assist in conducting User Access Reviews (UAR) and analyzing role-based access control (RBAC) policies.
type: how_to
---

# Access Control Reviewer

## Use Cases

- Quarterly User Access Review (UAR) campaigns
- Designing new IAM roles for a system
- Auditing privileged access (admin accounts)
- Cleaning up access after a reorganization
- Identifying Segregation of Duties (SoD) conflicts

## Variables

- `[SYSTEM_NAME]`: The system being reviewed (e.g., "AWS Production Account").
- `[REVIEW_TYPE]`: The goal of the review.
- `[DATA]`: The raw data to analyze.

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
