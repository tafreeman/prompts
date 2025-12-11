---
title: "API Architecture Designer"
shortTitle: "API Architecture Designer"
intro: "Designs comprehensive API architectures"
type: "how_to"
difficulty: "advanced"
audience:
  - "solution-architect"
  - "senior-engineer"
platforms:
  - "claude"
topics:
  - "api-design"
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
# API Architecture Designer

---

## Description

Designs comprehensive API architectures

---

## Use Cases

- API Design for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

---

## Prompt

```text
Design API architecture for:

Business Domain: [domain]
API Consumers: [consumers]
Integration Requirements: [integrations]
Security Needs: [security]
Scalability Goals: [scalability]

Include:
1. API design patterns
2. Authentication strategy
3. Rate limiting and throttling
4. Versioning strategy
5. Documentation framework
6. Monitoring and analytics
```text

**Output:**

```text
## API Architecture Design

### 1. API Design Patterns
*   **Style:** REST Level 3 (HATEOAS) for discoverability.
*   **Gateway:** API Gateway pattern for cross-cutting concerns (Auth, Rate Limiting).
*   **BFF:** Backend for Frontend pattern for the Internal Mobile App to aggregate calls.

### 2. Authentication Strategy
*   **Protocol:** OAuth 2.0 with OpenID Connect (OIDC).
*   **Security Profile:** FAPI Read/Write profile (requires mTLS for token endpoint, signed JWTs).
*   **Consent Management:** Granular scopes (`accounts:read`, `payments:write`) with explicit user consent UI.

### 3. Rate Limiting and Throttling
*   **Strategy:** Token Bucket algorithm.
*   **Tiers:**
    *   **Free:** 10 req/sec (Public data).
    *   **Partner:** 100 req/sec (Account access).
    *   **Internal:** Unlimited.

[... continues with versioning and documentation ...]
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
