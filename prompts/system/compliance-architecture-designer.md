---
title: "Compliance Architecture Designer"
shortTitle: "Compliance Architecture ..."
intro: "Designs compliance-focused architectures"
type: "how_to"
difficulty: "advanced"
audience:
  - "solution-architect"
  - "senior-engineer"
platforms:
  - "claude"
topics:
  - "architect"
  - "system"
  - "compliance"
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
# Compliance Architecture Designer

---

## Description

Designs compliance-focused architectures

---

## Use Cases

- Compliance for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Design compliant architecture for:

Regulatory Requirements: [regulations]
Business Domain: [domain]
Data Sensitivity: [sensitivity]
Audit Requirements: [audit]

Provide:
1. Compliance framework
2. Control implementation
3. Data governance
4. Audit trail design
5. Monitoring strategy
6. Reporting mechanisms
```text

**Output:**

```text
## Compliance Architecture

### 1. Compliance Framework
*   **Strategy:** "Privacy by Design" and "Zero Trust".
*   **Mapping:** Unified Control Framework (UCF) mapping ISO 27001 controls to GDPR articles.

### 2. Control Implementation
*   **Data Sovereignty:** Tenant pinning to specific AWS regions (e.g., EU-West-1 for German customers) to satisfy GDPR residency.
*   **Encryption:** Field-level encryption for SPII (SSN, Salary) using distinct KMS keys per tenant.

### 3. Data Governance
*   **Classification:** Auto-tagging data at ingestion (Public, Internal, Confidential, Restricted).
*   **Retention:** Automated S3 Lifecycle policies to delete candidate data after 6 months (GDPR minimization).
*   **Deletion:** "Tombstoning" records for Right to be Forgotten, ensuring backups are also scrubbed (crypto-shredding).

[... continues with audit trail and monitoring ...]
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
