---
title: API Architecture Designer
shortTitle: API Architecture Designer
intro: Designs comprehensive API architectures
type: how_to
difficulty: advanced
audience:

- solution-architect
- senior-engineer

platforms:

- claude

topics:

- api-design
- architect
- system
- enterprise

author: Prompts Library Team
version: '1.0'
date: '2025-11-16'
governance_tags:

- general-use
- PII-safe

dataClassification: internal
reviewStatus: draft
effectivenessScore: 0.0
---

# API Architecture Designer

---

## Description

Designs comprehensive API architectures for enterprise systems, including RESTful, GraphQL, and gRPC patterns. This prompt helps architects define authentication strategies, rate limiting policies, versioning approaches, and API governance frameworks that scale with organizational needs.

---

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Clients
        Web[Web App]
        Mobile[Mobile App]
        Partner[Partner Systems]
    end

    subgraph API_Gateway[API Gateway Layer]
        Gateway[API Gateway]
        Auth[Auth Service]
        RateLimit[Rate Limiter]
    end

    subgraph API_Layer[API Services]
        REST[REST APIs]
        GraphQL[GraphQL API]
        gRPC[gRPC Services]
    end

    subgraph Backend[Backend Services]
        BFF[Backend for Frontend]
        Core[Core Services]
        Cache[(Cache Layer)]
    end

    Web --> Gateway
    Mobile --> Gateway
    Partner --> Gateway
    Gateway --> Auth
    Gateway --> RateLimit
    RateLimit --> REST
    RateLimit --> GraphQL
    RateLimit --> gRPC
    REST --> BFF
    GraphQL --> BFF
    gRPC --> Core
    BFF --> Core
    Core --> Cache
```

---

## Decision Framework

### When to Use This Pattern

| Criteria | Indicators |
| ---------- | ------------ |
| **Multiple Consumers** | 3+ different client types (web, mobile, partners) |
| **Security Requirements** | OAuth 2.0/OIDC, API key management, or mTLS needed |
| **Scale** | >1000 requests/second or expecting 10x growth |
| **Governance** | Regulatory compliance, audit requirements |
| **Team Structure** | Multiple teams building/consuming APIs |

### When NOT to Use

- Single internal application with one consumer
- Simple CRUD operations with <100 concurrent users
- Prototype or MVP with uncertain requirements
- Monolithic applications without external integrations

---

## Use Cases

- Designing API gateway architectures for microservices ecosystems
- Building multi-tenant SaaS API platforms with rate limiting
- Creating partner integration APIs with OAuth 2.0 authentication
- Establishing API versioning strategies for long-lived public APIs
- Implementing BFF (Backend for Frontend) patterns for mobile apps

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

## Variables

- `[domain]`: Business domain (e.g., "Open Banking / Financial Services")
- `[consumers]`: API consumers (e.g., "Internal mobile app, Partner fintechs, Third-party aggregators")
- `[integrations]`: Integration requirements (e.g., "Core banking system, Payment gateway, Identity provider")
- `[security]`: Security needs (e.g., "PSD2 compliance, Strong Customer Authentication (SCA), Audit logging")
- `[scalability]`: Scalability goals (e.g., "10K concurrent users, 50K API calls/minute at peak")

---

## Cloud Platform Notes

### Azure

- **API Management**: Azure API Management for gateway, policies, and developer portal
- **Authentication**: Azure AD B2C for consumer identity, Azure AD for enterprise
- **Rate Limiting**: Built-in APIM policies with Redis Cache backend
- **Monitoring**: Application Insights + Azure Monitor

### AWS

- **API Gateway**: Amazon API Gateway (REST/HTTP APIs) or AppSync (GraphQL)
- **Authentication**: Amazon Cognito User Pools + API Gateway authorizers
- **Rate Limiting**: API Gateway throttling + WAF rate-based rules
- **Monitoring**: CloudWatch + X-Ray for distributed tracing

### GCP

- **API Gateway**: Apigee API Management or Cloud Endpoints
- **Authentication**: Identity Platform + Firebase Auth
- **Rate Limiting**: Apigee Spike Arrest and Quota policies
- **Monitoring**: Cloud Monitoring + Cloud Trace

---

## Example

### Context
A multinational retail bank needs to expose Open Banking APIs to comply with PSD2 regulations while also supporting their mobile app and partner fintech integrations.

### Input

```text
Business Domain: Retail Banking (Open Banking / PSD2)
API Consumers: Mobile banking app, 50+ third-party fintechs, internal systems
Integration Requirements: Core banking (SOAP), Card processor (ISO 8583), Fraud detection (REST)
Security Needs: PSD2 SCA, OAuth 2.0 FAPI profile, certificate-bound tokens
Scalability Goals: 10,000 TPS peak, 99.99% availability, <200ms p99 latency
```

### Expected Output

```text
## API Architecture Design

### 1. API Design Patterns

- **Style:** REST Level 3 (HATEOAS) for discoverability and self-documentation
- **Gateway:** Kong Enterprise as API Gateway with custom plugins for PSD2 compliance
- **BFF Pattern:** Separate BFFs for Mobile (aggregated views) and Partner (granular resources)
- **Versioning:** URI-based versioning (/v1/, /v2/) with 12-month deprecation policy

### 2. Authentication Strategy

- **Protocol:** OAuth 2.0 with OpenID Connect (OIDC) using FAPI Read-Write profile
- **Strong Customer Authentication (SCA):** Dynamic linking with PKCE and signed request objects
- **Certificate Binding:** mTLS with eIDAS QWAC certificates for TPP identification
- **Token Lifetime:** Access tokens: 5 minutes, Refresh tokens: 90 days with rotation

### 3. Rate Limiting and Throttling
| Tier | Rate Limit | Burst | Use Case |
| ------ | ----------- | ------- | ---------- |
| Free | 100 req/min | 20 | Sandbox testing |
| Partner | 1,000 req/min | 200 | Production TPPs |
| Premium | 10,000 req/min | 2,000 | Strategic partners |
| Internal | Unlimited | N/A | Mobile app |

### 4. Versioning Strategy

- **Semantic Versioning:** MAJOR.MINOR for breaking vs additive changes
- **Sunset Headers:** X-API-Sunset header 6 months before deprecation
- **Changelog:** Machine-readable changelog at /api/changelog

### 5. Documentation Framework

- **OpenAPI 3.1:** Single source of truth for all API specifications
- **Developer Portal:** Self-service portal with sandbox environment
- **SDKs:** Auto-generated SDKs for Python, JavaScript, Java, .NET

### 6. Monitoring and Analytics

- **Metrics:** Request volume, latency percentiles (p50, p95, p99), error rates by endpoint
- **Alerting:** PagerDuty integration for >1% error rate or p99 >500ms
- **Business Analytics:** API usage by partner, revenue per API call

```

---

## Tips

- Be specific when filling in placeholder values for better results
- Review and adjust the output to match your organization's standards
- Consider API-first design approach with OpenAPI specification
- Plan for backward compatibility from day one
- Implement comprehensive API versioning strategy early

---

## Related Prompts

- [Microservices Architecture Expert](microservices-architecture-expert.md) - For service decomposition behind APIs
- [Security Architecture Specialist](security-architecture-specialist.md) - For API security controls
- [Performance Architecture Optimizer](performance-architecture-optimizer.md) - For API latency optimization
- [Cloud Architecture Consultant](cloud-architecture-consultant.md) - For cloud-native API deployments
- [Enterprise Integration Architect](enterprise-integration-architect.md) - For backend system integration

---

## Related Prompts

- Browse other Architect prompts in this category
- Check the system folder for similar templates
