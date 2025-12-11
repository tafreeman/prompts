---
title: "Compliance Policy Generator"
shortTitle: "Policy Generator"
intro: "A prompt to draft formal corporate policies (Security, Privacy, HR) based on industry standards and organizational needs."
type: "how_to"
difficulty: "intermediate"
audience:
  - "compliance-officer"
  - "security-manager"
  - "hr-manager"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "governance"
  - "policy"
  - "documentation"
author: "Prompts Library Team"
version: "1.0"
date: "2025-12-11"
governance_tags:
  - "requires-human-review"
  - "policy-drafting"
dataClassification: "internal"
reviewStatus: "draft"
regulatory_scope:
  - "ISO-27001"
  - "SOC-2"
  - "NIST"
---
# Compliance Policy Generator

---

## Description

Generates comprehensive, professional drafts of corporate policies. It ensures policies include standard sections (Purpose, Scope, Roles, Policy Statements, Enforcement) and align with frameworks like ISO 27001, SOC 2, or NIST.

---

## Use Cases

- Drafting a new "Acceptable Use Policy"
- Creating a "Remote Work Security Policy"
- Updating the "Incident Response Policy" for SOC 2
- Writing a "Clean Desk Policy"
- Formalizing "Password Management" guidelines

---

## Prompt

```text
You are a Policy Writer specializing in corporate governance. Draft a formal policy document based on the following parameters.

## Policy Topic
[TOPIC] (e.g., Acceptable Use, Password Security)

## Framework Alignment
[FRAMEWORK] (e.g., ISO 27001, SOC 2, NIST 800-53)

## Key Requirements / Custom Rules
[REQUIREMENTS] (e.g., "Must require MFA," "Passwords expire every 90 days," "No personal devices")

## Instructions
1.  Structure the document with standard headers: Purpose, Scope, Definitions, Policy Statements, Roles & Responsibilities, Enforcement, Version History.
2.  Use clear, mandatory language ("Employees must..." rather than "should").
3.  Ensure alignment with the specified framework.

## Output Format
Markdown formatted policy document.
```

---

## Variables

- `[TOPIC]`: The subject of the policy.
- `[FRAMEWORK]`: The standard to align with.
- `[REQUIREMENTS]`: Specific rules the user wants included.

---

## Example

```text
# Password Security Policy

## 1. Purpose
To establish standards for creating, protecting, and changing strong passwords to protect corporate assets.

## 2. Scope
This policy applies to all employees, contractors, and third parties accessing [Company Name] systems.

## 3. Policy Statements
### 3.1 Password Complexity
*   Passwords must be at least 12 characters long.
*   Must contain a mix of uppercase, lowercase, numbers, and symbols.
*   Common phrases or dictionary words alone are prohibited.

### 3.2 Multi-Factor Authentication (MFA)
*   MFA is mandatory for all remote access and cloud applications (Email, CRM, AWS).
*   SMS-based MFA is discouraged; Authenticator apps or hardware tokens are preferred.

### 3.3 Password Management
*   Passwords must not be shared or written down.
*   Use of the corporate Password Manager (e.g., 1Password) is mandatory.

## 4. Enforcement
Violation of this policy may result in disciplinary action, up to and including termination of employment.

## 5. Version History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-12-11 | SecTeam | Initial Draft |
```

---

## Tips

- **Tone:** Policies should be authoritative but readable. Avoid legalese where possible.
- **Enforcement:** Always include an enforcement clause; a policy without consequences is just a suggestion.
- **Review:** Policies should be reviewed annually. Include a "Next Review Date" in the metadata.

---

## Related Prompts

- [SOC 2 Audit Preparation](/prompts/governance/soc2-audit-preparation) — Align policies with SOC 2 Trust Services Criteria
- [Access Control Reviewer](/prompts/governance/access-control-reviewer) — Develop access policies based on review findings
- [Data Retention Policy](/prompts/governance/data-retention-policy) — Generate data lifecycle policies
- [Regulatory Change Analyzer](/prompts/governance/regulatory-change-analyzer) — Update policies based on new regulations
