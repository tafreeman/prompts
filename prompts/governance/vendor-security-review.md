---
title: Vendor Security Reviewer
shortTitle: Vendor Review
intro: A prompt to analyze vendor security questionnaires and documentation to assess
  third-party risk.
type: how_to
difficulty: intermediate
audience:

- security-analyst
- procurement-manager

platforms:

- claude
- chatgpt
- github-copilot

topics:

- governance
- security
- third-party-risk

author: Prompts Library Team
version: '1.0'
date: '2025-12-11'
governance_tags:

- requires-human-review
- security-critical

dataClassification: internal
reviewStatus: draft
regulatory_scope:

- ISO-27001
- SOC-2
- GDPR

effectivenessScore: 0.0
---

# Vendor Security Reviewer

---

## Description

Streamlines the vendor risk assessment process by analyzing security documentation (SOC 2 reports, SIG questionnaires, Pen Test summaries). It helps identify red flags, missing controls, and compliance gaps in third-party service providers.

---

## Use Cases

- Evaluating a new SaaS vendor before purchase
- Annual review of critical vendors
- Assessing a vendor's incident response capabilities
- Comparing security postures of two competing vendors
- Drafting follow-up questions for a vendor security team

---

## Prompt

```text
You are a Third-Party Risk Analyst. Review the provided summary of a vendor's security posture and identify risks.

## Vendor Information
**Vendor Name:** [VENDOR_NAME]
**Service Provided:** [SERVICE_TYPE]
**Data Shared:** [DATA_TYPES]

## Security Documentation Summary
[DOC_SUMMARY] (e.g., "SOC 2 Type II report available with qualified opinion. ISO 27001 certified. No recent pen test provided.")

## Instructions

1.  Assess the inherent risk based on the data shared.
2.  Evaluate the residual risk based on the controls/certifications provided.
3.  Identify specific "Red Flags" or missing information.
4.  Generate a list of clarifying questions to ask the vendor.

## Output Format

- **Risk Scorecard** (High/Medium/Low)
- **Key Findings**
- **Clarifying Questions**
- **Recommendation** (Approve / Conditional Approval / Reject)

```

---

## Variables

- `[VENDOR_NAME]`: Name of the vendor.
- `[SERVICE_TYPE]`: What they do (e.g., "Marketing Automation Platform").
- `[DATA_TYPES]`: Data they will access (e.g., "Customer Email Addresses, Purchase History").
- `[DOC_SUMMARY]`: Key points from their security docs.

---

## Example

```text
## Vendor Security Review: MailBlast Inc
### Risk Scorecard

*   **Inherent Risk:** Medium (PII involved: Emails).
*   **Control Effectiveness:** Medium.
*   **Residual Risk:** Medium-Low.

### Key Findings

*   **Positive:** ISO 27001 certification is current.
*   **Concern:** SOC 2 report had a "Qualified Opinion" (exceptions noted).
*   **Gap:** No mention of data residency (GDPR concern if data leaves EU).

### Clarifying Questions

1.  "Please provide the management response and remediation status for the exceptions noted in the SOC 2 report."
2.  "Can you confirm where customer data is hosted? Do you offer EU-only data residency?"
3.  "When was your last external penetration test, and were critical findings remediated?"

### Recommendation
**Conditional Approval.** Proceed with contract negotiation, but require satisfactory answers to the questions above and include a Data Processing Addendum (DPA).
```

---

## Tips

- **Data Context:** The risk depends heavily on *what* data you share. A cafeteria vendor needs less scrutiny than a payroll processor.
- **"Qualified Opinion":** In a SOC 2 report, this means the auditor found significant issues. Always investigate.
- **Fourth Parties:** Ask about *their* vendors (sub-processors).

---

## Related Prompts

- [SOC 2 Audit Preparation](/prompts/governance/soc2-audit-preparation) — Understand SOC 2 criteria when reviewing vendor reports
- [Data Classification Helper](/prompts/governance/data-classification-helper) — Classify data shared with vendors
- [Privacy Impact Assessment](/prompts/governance/privacy-impact-assessment) — Assess privacy risks of vendor data processing
- [HIPAA Compliance Checker](/prompts/governance/hipaa-compliance-checker) — Evaluate vendors handling healthcare data
