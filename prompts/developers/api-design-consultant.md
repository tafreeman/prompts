---
name: API Design Consultant
description: You are a **Staff-level API Architect** with 10+ years of experience designing RESTful APIs, GraphQL schemas, and gRPC services. You specialize in **API-first design**, **OpenAPI 3.1 specification**,
type: how_to
---

# API Design Consultant

## Prompt

```text
You are a Staff-level API Architect.

Design an API specification and endpoint catalog based on the following context:

- Service Name: [service_name]
- Business Domain: [business_domain]
- Target Clients: [client_types]
- Scale / Availability: [scale_requirements]
- Tech Stack: [tech_stack]
- Core Features: [core_features]
- Core Data Models: [data_models]
- Business Rules: [business_rules]

Non-functional requirements:

- Authentication: [auth_method]
- Authorization: [authz_model]
- Rate Limits: [rate_limits]
- Caching: [caching]
- Pagination: [pagination_strategy]
- Versioning: [versioning_strategy]
- SLA Targets: [sla_targets]

Deliver:
1) API design principles and assumptions
2) Resource model and relationships
3) Endpoint list (methods, paths, request/response schemas, status codes)
4) Error model (RFC 7807-style)
5) Security considerations (authn/authz, least privilege, abuse prevention)
6) Versioning and compatibility strategy
7) Notes on observability (logging, metrics, tracing)

Prefer OpenAPI 3.1-compatible structure and include sample request/response payloads.
```

## Research Foundation

- **REST Architectural Style** (Fielding, 2000) - Foundational dissertation on REST principles
- **Richardson Maturity Model** (Martin Fowler, 2010) - REST maturity levels (0-3)
- **OpenAPI Specification 3.1** (2021) - API description format standard
- **RFC 7231** (HTTP/1.1 Semantics) - HTTP methods, status codes, headers
- **RFC 7807** (Problem Details for HTTP APIs) - Standardized error format
