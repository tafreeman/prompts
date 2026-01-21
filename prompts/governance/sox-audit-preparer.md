---
name: SOX Audit Preparer
description: A prompt to assist in preparing for Sarbanes-Oxley (SOX) IT General Controls (ITGC) audits.
type: how_to
---

# SOX Audit Preparer

## Use Cases

- Preparing for an annual SOX 404 audit
- Documenting ITGCs for a new financial system
- Self-assessing change management processes
- Reviewing user access reviews (UAR) for completeness
- Drafting remediation plans for audit findings

## Variables

- `[DOMAIN]`: The specific ITGC domain (e.g., "Change Management").
- `[SYSTEM_CONTEXT]`: The financial application involved (e.g., "SAP ERP System used for General Ledger").
- `[PROCESS_DESCRIPTION]`: How the process currently works (e.g., "Developers write code, test it in dev, and then deploy it to production using a script. No formal approval ticket is used.").

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
