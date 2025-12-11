---
title: "HIPAA Compliance Checker"
shortTitle: "HIPAA Checker"
intro: "A comprehensive prompt for assessing healthcare applications and systems against HIPAA Privacy and Security Rules."
type: "how_to"
difficulty: "advanced"
audience:
  - "solution-architect"
  - "security-engineer"
  - "healthcare-it"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "governance"
  - "compliance"
  - "healthcare"
  - "hipaa"
author: "Prompts Library Team"
version: "1.0"
date: "2025-12-11"
governance_tags:
  - "requires-human-review"
  - "compliance-critical"
  - "phi-handling"
dataClassification: "internal"
reviewStatus: "draft"
regulatory_scope:
  - "HIPAA"
  - "HITECH"
---
# HIPAA Compliance Checker

---

## Description

A specialized prompt for evaluating software systems, architectures, and operational processes against the Health Insurance Portability and Accountability Act (HIPAA). It covers the Privacy Rule, Security Rule (Administrative, Physical, Technical safeguards), and Breach Notification Rule. Uses a systematic checklist approach to identify gaps in PHI (Protected Health Information) handling.

---

## Use Cases

- Evaluating new healthcare software architectures
- Preparing for a HIPAA audit
- Assessing third-party vendors handling PHI
- Reviewing cloud infrastructure configurations (AWS/Azure/GCP)
- Developing HIPAA-compliant operational procedures

---

## Prompt

```text
You are an expert HIPAA Compliance Officer and Security Architect. Your task is to evaluate the following system or process for compliance with HIPAA regulations, specifically the Security Rule and Privacy Rule.

## System/Process Description
[DESCRIPTION]

## Assessment Scope
- [ ] Administrative Safeguards
- [ ] Physical Safeguards
- [ ] Technical Safeguards
- [ ] Privacy Rule Requirements

## Instructions
1.  Analyze the provided description against specific HIPAA citations (e.g., 45 CFR § 164.312).
2.  Identify potential compliance gaps or risks.
3.  Recommend specific technical or procedural controls to address each gap.
4.  Classify findings by risk level (High/Medium/Low).

## Output Format
Provide a structured report with:
- **Executive Summary**
- **Compliance Matrix** (Rule | Requirement | Status | Observation)
- **Gap Analysis**
- **Remediation Roadmap**
```

---

## Variables

- `[DESCRIPTION]`: Detailed description of the system, architecture, or process involving PHI (e.g., "A mobile app for patient telehealth visits using AWS WebRTC and storing recordings in S3").

---

## Example

```text
## HIPAA Compliance Assessment: Telehealth Mobile App

### Executive Summary
The proposed architecture leverages AWS services which are HIPAA-eligible, but specific configurations regarding logging and access control need remediation to meet Technical Safeguards.

### Compliance Matrix (Partial)

| Rule Ref | Requirement | Status | Observation |
|----------|-------------|--------|-------------|
| § 164.312(a)(1) | Access Control | ⚠️ Partial | Unique user IDs present, but automatic logoff not described. |
| § 164.312(a)(2)(iv) | Encryption and Decryption | ✅ Compliant | Data at rest encrypted via AWS KMS; in transit via TLS 1.3. |
| § 164.312(b) | Audit Controls | ❌ Gap | No centralized logging of PHI access events mentioned. |

### Gap Analysis
1.  **Audit Trails (High Risk):** Lack of detailed logs for "read" access to patient records violates § 164.312(b).
2.  **BAA (Medium Risk):** Need to confirm Business Associate Agreement is signed with AWS and Twilio (if used).

### Remediation Roadmap
1.  **Immediate:** Enable CloudTrail and S3 server access logging; configure application-level logging for patient record access.
2.  **Short-term:** Implement 15-minute idle session timeout in the mobile app.
```

---

## Tips

- **BAA is Key:** Always check if a Business Associate Agreement is in place for cloud providers.
- **Encryption is Mandatory:** In practice, encryption at rest and in transit is expected, even if the rule says "addressable".
- **Minimum Necessary:** Verify that the system only accesses the minimum PHI required for the task.

---

## Related Prompts

- [Privacy Impact Assessment](/prompts/governance/privacy-impact-assessment) — Conduct data protection impact assessments for healthcare systems
- [Security Incident Response](/prompts/governance/security-incident-response) — Handle PHI breach incidents per HIPAA Breach Notification Rule
- [Vendor Security Review](/prompts/governance/vendor-security-review) — Evaluate cloud providers handling PHI
- [Data Classification Helper](/prompts/governance/data-classification-helper) — Classify healthcare data sensitivity levels
