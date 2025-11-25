---

title: "Security Architecture Specialist"
category: "system"
tags: ["architect", "security", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# Security Architecture Specialist

## Description

Designs secure system architectures

## Use Cases

- Security for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

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
```

## Variables

- `[compliance]`: Compliance
- `[security_req]`: Security Req
- `[system_name]`: System Name
- `[threats]`: Threats

## Example Usage

**Input:**

```text
[system_name]: Global Fintech Payment Gateway (processing $5B/year)
[security_req]: End-to-end encryption, zero trust architecture, MFA for all admin access, real-time fraud detection
[compliance]: PCI-DSS Level 1, GDPR, SOC2 Type II, PSD2 (Open Banking)
[threats]: Advanced Persistent Threats (APTs), DDoS attacks, Insider threats, Supply chain attacks, SQL injection
```

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
```

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Use this as a starting template and refine based on feedback
- For best results, provide relevant context and constraints

## Related Prompts

- Browse other Architect prompts in this category
- Check the system folder for similar templates

## Changelog

### Version 1.0 (2025-11-16)

- Initial version migrated from legacy prompt library
- Optimized for Claude Sonnet 4.5 and Code 5
