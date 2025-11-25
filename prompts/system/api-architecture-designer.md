---

title: "API Architecture Designer"
category: "system"
tags: ["architect", "api-design", "enterprise"]
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-16"
difficulty: "advanced"
platform: "Claude Sonnet 4.5"
---

# API Architecture Designer

## Description

Designs comprehensive API architectures

## Use Cases

- API Design for Architect persona
- Enterprise-grade prompt optimized for production use
- Suitable for teams requiring structured, repeatable workflows

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
```

## Variables

- `[consumers]`: Consumers
- `[domain]`: Domain
- `[integrations]`: Integrations
- `[scalability]`: Scalability
- `[security]`: Security

## Example Usage

**Input:**

```text
[domain]: Open Banking Platform (PSD2 Compliant)
[consumers]: Third-Party Providers (TPPs), Fintech Apps, Internal Mobile App
[integrations]: Legacy Core Banking (SOAP), KYC Provider (REST), Fraud Detection System
[security]: FAPI (Financial-grade API) Profile, OAuth 2.0 / OIDC, mTLS
[scalability]: 1000 TPS, <100ms latency
```

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
