---
title: Data Classification Helper
shortTitle: Data Classifier
intro: A prompt to help categorize data assets based on sensitivity and regulatory
  requirements.
type: how_to
difficulty: beginner
audience:
- data-steward
- compliance-officer
- developer
platforms:
- claude
- chatgpt
- github-copilot
topics:
- governance
- data-management
- security
author: Prompts Library Team
version: '1.0'
date: '2025-12-11'
governance_tags:
- requires-human-review
- data-privacy
dataClassification: internal
reviewStatus: draft
regulatory_scope:
- GDPR
- CCPA
- Internal-Policy
effectivenessScore: 0.0
---

# Data Classification Helper

---

## Description

Assists in classifying data fields or datasets into standard sensitivity levels (e.g., Public, Internal, Confidential, Restricted). It analyzes the nature of the data and maps it to common regulatory and security handling requirements.

---

## Use Cases

- Creating a data dictionary for a new application
- Tagging data in a catalog (e.g., Collibra, Alation)
- Determining encryption requirements for a database schema
- Assessing the impact of a potential data breach
- Configuring DLP (Data Loss Prevention) rules

---

## Prompt

```text
You are a Data Governance Specialist. Classify the following data elements based on a standard 4-tier classification scheme (Public, Internal, Confidential, Restricted).

## Classification Scheme Definition
- **Public:** Freely shareable (e.g., marketing info).
- **Internal:** Business data, low risk if leaked (e.g., org charts).
- **Confidential:** Sensitive business data or PII (e.g., salaries, customer emails).
- **Restricted:** Highly sensitive, regulatory impact (e.g., SSNs, Credit Cards, Health Data).

## Data Elements to Classify
[DATA_LIST]

## Instructions
1.  Assign a classification level to each element.
2.  Cite the reasoning (e.g., "Contains PII", "PCI-DSS requirement").
3.  Recommend handling controls (e.g., "Encrypt at rest").

## Output Format
| Data Element | Classification | Reasoning | Handling Controls |
|--------------|----------------|-----------|-------------------|
```

---

## Variables

- `[DATA_LIST]`: List of fields or data types (e.g., "User ID, Email, Password Hash, Date of Birth, Last 4 of SSN, Public Profile URL").

---

## Example

```text
## Data Classification Report

| Data Element | Classification | Reasoning | Handling Controls |
|--------------|----------------|-----------|-------------------|
| Public Profile URL | **Public** | Intended for public consumption. | None specific. |
| User ID | **Internal** | System identifier, low risk alone. | Access control. |
| Email Address | **Confidential** | PII (GDPR/CCPA). | Encrypt in transit, access logging. |
| Password Hash | **Restricted** | Critical security credential. | Strong hashing (Argon2/bcrypt), salt. |
| Last 4 of SSN | **Confidential** | Partial PII, used for verification. | Encrypt at rest, mask on display. |
| Date of Birth | **Confidential** | PII, identity theft risk. | Encrypt at rest. |
```

---

## Tips

- **Context Matters:** "Name" might be Public for a CEO but Confidential for a covert operative.
- **Aggregation:** A collection of "Internal" data might become "Confidential" when aggregated (mosaic effect).
- **Regulations:** Always check if specific laws (HIPAA, PCI) mandate a higher classification.

---

## Related Prompts

- [Data Retention Policy](/prompts/governance/data-retention-policy) — Define lifecycle and retention schedules for classified data
- [Privacy Impact Assessment](/prompts/governance/privacy-impact-assessment) — Assess privacy risks for data processing activities
- [GDPR Compliance Assessment](/prompts/governance/gdpr-compliance-assessment) — Evaluate compliance for personal data handling
- [Access Control Reviewer](/prompts/governance/access-control-reviewer) — Review who has access to classified data
