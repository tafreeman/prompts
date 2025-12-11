---
title: "Security Architecture Specialist"
shortTitle: "Security Architecture Sp..."
intro: "Designs secure system architectures"
type: "how_to"
difficulty: "advanced"
audience:
  - "solution-architect"
  - "senior-engineer"
platforms:
  - "claude"
topics:
  - "security"
  - "architect"
  - "system"
  - "enterprise"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
governance_tags:
  - "general-use"
  - "PII-safe"
dataClassification: "internal"
reviewStatus: "draft"
---
# Security Architecture Specialist

---

## Description

Designs secure system architectures

---

## Use Cases

- Security for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Design security architecture for:

System: [system_name]
Security Requirements: [security_req]
Compliance Standards: [compliance]
Threat Landscape: [threats]

Include:
1. Security controls framework
2. Identity and access management
3. Data protection strategy
4. Network security design
5. Monitoring and incident response
6. Compliance mapping
```text

**Output:**

```text
## Security Architecture Framework

### 1. Security Controls Framework (NIST CSF Aligned)

**Identify:**
*   Asset Management: AWS Config + Tagging policies
*   Risk Assessment: Quarterly penetration testing (external)

**Protect:**
*   **Data Protection:**
    *   At Rest: AES-256 (AWS KMS with customer-managed keys)
    *   In Transit: TLS 1.3 with mTLS for service-to-service
    *   Tokenization: VGS (Very Good Security) for PAN data isolation
*   **Identity (IAM):**
    *   Workforce: Okta + AWS SSO (Just-in-Time access)
    *   Service: IAM Roles with least privilege (IRSA for Kubernetes)

**Detect:**
*   GuardDuty (Threat detection)
*   WAF (Web Application Firewall) with managed rules for OWASP Top 10
*   Macie (Sensitive data discovery)

[... continues with network security and incident response ...]
```text

---


## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

---

## Related Prompts

- Browse other Architect prompts in this category
- Check the system folder for similar templates
