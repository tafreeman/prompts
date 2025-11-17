# Developer Prompts Quality Uplift Plan
**Tree-of-Thoughts Analysis & Prioritization**

**Date**: November 17, 2025  
**Scope**: 17 prompts in `prompts/developers/`  
**Goal**: Elevate top 10 prompts to Tier 1 (9-10/10) quality  
**Methodology**: Multi-branch ToT evaluation → synthesis → actionable roadmap

---

## Executive Summary

**Current State**: All 17 developer prompts are Tier 3 (3/10 average), consisting of minimal templates with placeholder examples and no governance metadata.

**Target State**: Top 10 prompts upgraded to Tier 1 (9-10/10) with:
- Expert persona definitions with methodologies
- Structured output templates (JSON schemas, checklists)
- Realistic, comprehensive examples demonstrating full capabilities
- Governance metadata (risk levels, audit requirements, approval workflows)
- Research foundations and best practices

**Strategic Approach**: Prioritize based on usage frequency, quality improvement potential, and SDLC strategic impact.

**Expected Outcome**: 
- 59% of developer prompts at Tier 1 quality
- Repository becomes trusted reference for enterprise development teams
- Measurable improvement in developer productivity and decision quality

---

## Tree-of-Thoughts Analysis

### Branch A: Usage Frequency Priority

**Hypothesis**: Focus on most frequently used developer workflows to maximize impact.

**Analysis**:
Based on typical SDLC workflows, the most frequent activities are:

1. **Code Generation** - Daily activity for all developers
2. **Code Review** - Multiple times per day in active projects
3. **Debugging/Troubleshooting** - Constant need
4. **Testing** - Continuous activity in quality-focused teams
5. **API Design** - Frequent in microservices/integration work
6. **Security Audits** - Regular compliance requirement
7. **Performance Optimization** - Ongoing concern
8. **DevOps/CI-CD** - Daily pipeline work
9. **Database Design** - Regular but less frequent
10. **Documentation** - Ongoing but lower priority

**Top 10 by Usage**:
1. code-generation-assistant
2. code-review-expert
3. security-code-auditor
4. test-automation-engineer
5. api-design-consultant
6. devops-pipeline-architect
7. performance-optimization-specialist
8. database-schema-designer
9. documentation-generator
10. microservices-architect

**Strength**: Immediate impact on daily developer workflows  
**Weakness**: May miss strategically important but less frequent activities

---

### Branch B: Quality Gap Priority

**Hypothesis**: Focus on prompts with highest improvement potential (currently weakest with clearest path to excellence).

**Analysis**:
All 17 prompts currently at 3/10. Improvement potential depends on:
- Complexity of domain (more complex = more to add)
- Availability of standards/frameworks to reference
- Clarity of output format requirements
- Existing research/best practices

**Improvement Potential Scoring** (1-10, higher = more to gain):

| Prompt | Current | Potential | Gap | Standards Available |
|--------|---------|-----------|-----|-------------------|
| security-code-auditor | 3/10 | 10/10 | 7 | ✓ OWASP, NIST, CWE |
| microservices-architect | 3/10 | 10/10 | 7 | ✓ DDD, Event Storming, 12-Factor |
| devops-pipeline-architect | 3/10 | 10/10 | 7 | ✓ GitLab CI, Jenkins, GitHub Actions |
| api-design-consultant | 3/10 | 10/10 | 7 | ✓ OpenAPI, REST, GraphQL specs |
| test-automation-engineer | 3/10 | 10/10 | 7 | ✓ Test Pyramid, TDD, BDD |
| performance-optimization-specialist | 3/10 | 10/10 | 7 | ✓ Profiling tools, APM patterns |
| database-schema-designer | 3/10 | 10/10 | 7 | ✓ Normalization, ERD, indexing |
| code-review-expert | 3/10 | 9/10 | 6 | ✓ Style guides, SOLID |
| code-generation-assistant | 3/10 | 8/10 | 5 | ⚠ Broad, less structured |
| legacy-system-modernization | 3/10 | 9/10 | 6 | ✓ Strangler fig, DDD |

**Top 10 by Gap**:
1. security-code-auditor (7 points, OWASP framework)
2. microservices-architect (7 points, DDD/Event Storming)
3. devops-pipeline-architect (7 points, CI/CD frameworks)
4. api-design-consultant (7 points, OpenAPI spec)
5. test-automation-engineer (7 points, Test Pyramid)
6. performance-optimization-specialist (7 points, APM patterns)
7. database-schema-designer (7 points, ERD/normalization)
8. code-review-expert (6 points, SOLID principles)
9. legacy-system-modernization (6 points, migration patterns)
10. frontend-architecture-consultant (6 points, React/Vue patterns)

**Strength**: Maximizes quality improvement with clear frameworks to follow  
**Weakness**: May not align with actual usage patterns

---

### Branch C: Strategic SDLC Impact Priority

**Hypothesis**: Focus on prompts that support critical SDLC phases where poor decisions have cascading effects.

**SDLC Phase Analysis**:

```
Requirements → Design → Implementation → Testing → Deployment → Operations
                  ↓         ↓               ↓          ↓            ↓
            Architecture  Code Gen      Test Auto  DevOps Pipe  Performance
            API Design    Code Review                           Monitoring
            DB Schema     Security
            Microservices
```

**Strategic Impact Scoring**:

| Prompt | SDLC Phase | Impact if Poor | Reversibility | Strategic Score |
|--------|-----------|----------------|---------------|----------------|
| **microservices-architect** | Design | Very High | Low (expensive to reverse) | 10/10 |
| **api-design-consultant** | Design | High | Low (breaks contracts) | 9/10 |
| **database-schema-designer** | Design | High | Low (migration costly) | 9/10 |
| **security-code-auditor** | Design+Test | Very High | Medium (security debt) | 9/10 |
| **code-review-expert** | Implementation | High | Medium (technical debt) | 8/10 |
| **devops-pipeline-architect** | Deployment | High | Medium (pipeline refactor) | 8/10 |
| **test-automation-engineer** | Testing | High | High (can add tests later) | 7/10 |
| **performance-optimization-specialist** | Operations | Medium | High (can optimize later) | 7/10 |
| **code-generation-assistant** | Implementation | Medium | High (code is mutable) | 6/10 |
| **legacy-system-modernization** | Strategic | Very High | Low (costly migration) | 9/10 |

**Top 10 by Strategic Impact**:
1. microservices-architect (10/10 - architecture decisions are foundational)
2. api-design-consultant (9/10 - API contracts are hard to change)
3. database-schema-designer (9/10 - schema changes are expensive)
4. security-code-auditor (9/10 - security is non-negotiable)
5. legacy-system-modernization (9/10 - migration failures are costly)
6. code-review-expert (8/10 - prevents technical debt accumulation)
7. devops-pipeline-architect (8/10 - enables deployment velocity)
8. test-automation-engineer (7/10 - quality foundation)
9. performance-optimization-specialist (7/10 - scalability enabler)
10. frontend-architecture-consultant (7/10 - UX architecture)

**Strength**: Prevents costly mistakes in high-stakes decisions  
**Weakness**: May neglect frequently-used but lower-stakes prompts

---

## ToT Synthesis: Optimal Prioritization

**Evaluation Criteria**:
- ✅ Branch A captures daily usage impact
- ✅ Branch B ensures achievable quality with clear standards
- ✅ Branch C prevents costly architectural mistakes

**Weighted Scoring** (Usage × 0.3 + Gap × 0.3 + Strategic × 0.4):

| # | Prompt | Usage | Gap | Strategic | **Final Score** | Priority Tier |
|---|--------|-------|-----|-----------|----------------|---------------|
| 1 | **security-code-auditor** | 9 | 10 | 9 | **9.3** | **P0** |
| 2 | **code-review-expert** | 10 | 9 | 8 | **8.9** | **P0** |
| 3 | **microservices-architect** | 6 | 10 | 10 | **8.8** | **P0** |
| 4 | **api-design-consultant** | 8 | 10 | 9 | **9.0** | **P0** |
| 5 | **devops-pipeline-architect** | 8 | 10 | 8 | **8.8** | **P0** |
| 6 | **test-automation-engineer** | 9 | 10 | 7 | **8.6** | **P1** |
| 7 | **database-schema-designer** | 7 | 10 | 9 | **8.8** | **P1** |
| 8 | **code-generation-assistant** | 10 | 8 | 6 | **7.8** | **P1** |
| 9 | **performance-optimization-specialist** | 7 | 10 | 7 | **8.0** | **P1** |
| 10 | **legacy-system-modernization** | 5 | 9 | 9 | **8.0** | **P2** |

**Winner**: **Combined approach with strategic bias**
- P0 (Top 5): High usage + high strategic impact + clear improvement path
- P1 (6-9): Either high usage or high strategic impact
- P2 (10): Specialized but high impact when needed

---

## Detailed Uplift Plans: Top 10 Prompts

### Priority 0: Critical Path (Weeks 1-8)

---

#### 1. Security Code Auditor (Score: 9.3/10)

**Current State** (3/10):
```yaml
Description: "Conducts security code audits"
Prompt: Basic checklist (OWASP Top 10, SQL injection, XSS)
Variables: Placeholders only
Examples: None
Governance: None
```

**Gaps**:
- ❌ No expert persona (0/2 role clarity)
- ❌ No structured output format (0/2)
- ❌ No realistic vulnerability examples (0/2)
- ❌ No governance metadata despite security-critical nature (0/2)
- ❌ Minimal depth - no CWE mapping, severity scoring, remediation guidance (1/2)

**Target State** (9/10):
```yaml
Persona: "Expert security auditor following OWASP Secure Code Review Guide v2.0, 
          NIST SP 800-53, and SANS Top 25. Performs SAST analysis with CWE 
          classification and CVSS scoring."

Research Foundation: 
  - OWASP Code Review Guide v2.0
  - NIST SP 800-53 Rev 5
  - CWE/SANS Top 25 Most Dangerous Software Weaknesses

Structured Output:
  - JSON schema with findings array
  - Each finding: {line, severity, cwe, cvss_score, description, exploit, remediation}
  - Executive summary with risk heatmap

Realistic Examples:
  1. SQL Injection (CWE-89): Python Flask app with unsanitized queries
  2. XSS Vulnerability (CWE-79): React component with dangerouslySetInnerHTML
  3. Authentication Bypass (CWE-287): JWT implementation with weak secret
  4. Path Traversal (CWE-22): File upload with directory traversal

Governance:
  - risk_level: "Critical"
  - data_classification: "Confidential"
  - approval_required: "CISO"
  - retention_period: "7 years"
  - regulatory_scope: ["SOC2", "PCI-DSS", "ISO27001"]
  - audit_required: true
  - escalation_triggers: ["Critical/High findings → CISO within 24 hours"]

Tips:
  - Integrate with SAST tools (SonarQube, Snyk, Veracode)
  - Use severity scoring matrix (CVSS 3.1)
  - Provide exploit PoC for High/Critical findings
  - Include remediation code examples
  - Map to compliance frameworks (OWASP ASVS levels)
```

**Uplift Approach**:
1. Study `security-incident-response.md` (10/10 governance prompt) as template
2. Add OWASP Code Review Guide methodology to persona
3. Create 4 comprehensive examples covering OWASP Top 10 categories
4. Design JSON schema for automated scanning integration
5. Add governance metadata (CISO approval, audit logging)
6. Include remediation code snippets for each vulnerability type

**Effort Estimate**: 12-15 hours
- Research/planning: 2 hours
- Persona & methodology: 2 hours
- Examples (4 vulnerabilities): 5 hours
- JSON schema & governance: 2 hours
- Testing & refinement: 2 hours

**Success Criteria**:
- ✅ Score 9/10 on audit rubric
- ✅ Includes 4+ realistic vulnerability examples with CWE mapping
- ✅ JSON schema validated
- ✅ Governance fields complete
- ✅ Tested with actual vulnerable code samples

---

#### 2. Code Review Expert (Score: 8.9/10)

**Current State** (3/10):
```yaml
Description: "Provides comprehensive code reviews"
Prompt: Generic checklist (quality, security, performance, maintainability)
Variables: Placeholders only
Examples: None
Governance: None
```

**Gaps**:
- ❌ No methodology (0/2 role clarity)
- ❌ No structured review format (0/2)
- ❌ No code examples showing issues (0/2)
- ❌ No approval workflow despite critical nature (0/2)
- ❌ Minimal guidance (1/2)

**Target State** (9/10):
```yaml
Persona: "Senior code reviewer with 10+ years experience, following Google 
          Engineering Practices, SOLID principles, and language-specific 
          style guides. Focuses on correctness, maintainability, and team 
          knowledge transfer."

Research Foundation:
  - Google Engineering Practices: Code Review
  - SOLID Principles (Martin, 2000)
  - Clean Code (Martin, 2008)
  - Language-specific: PEP 8 (Python), Effective Java, ESLint (JS)

Review Framework:
  1. Correctness: Logic errors, edge cases, error handling
  2. Design: SOLID adherence, design patterns, abstractions
  3. Readability: Naming, comments, complexity (cyclomatic < 10)
  4. Security: OWASP checks, input validation, auth/authz
  5. Performance: Algorithmic complexity, database queries, caching
  6. Tests: Coverage (>80%), test quality, test organization
  7. Documentation: API docs, inline comments, README updates

Structured Output:
  - Three-tier feedback: Blocking, Suggested, Nitpicks
  - Each comment: {line, severity, category, issue, fix, learning_opportunity}
  - Overall assessment: LGTM / LGTM with comments / Needs work

Realistic Examples:
  1. Python API with SQL injection, missing error handling, no tests
  2. JavaScript React component with performance issues (unnecessary re-renders)
  3. Java service violating Single Responsibility, 200-line method
  4. Go code with race conditions and improper error wrapping

Governance:
  - governance_tags: ["audit-required", "requires-human-review"]
  - data_classification: "Confidential"
  - risk_level: "High"
  - approval_required: "Tech Lead"
  - retention_period: "3 years"

Tips:
  - Focus on teaching, not just finding issues
  - Use "why" explanations, not just "what"
  - Suggest specific fixes with code snippets
  - Prioritize: Blocking > Suggested > Nitpicks
  - Balance thoroughness with review velocity (< 400 LOC per review)
  - Link to style guides and best practices docs
```

**Uplift Approach**:
1. Study Google Engineering Practices guide
2. Define three-tier feedback system (Blocking/Suggested/Nitpicks)
3. Create 4 examples covering different languages and issue types
4. Add SOLID principles guidance
5. Include "teaching moment" pattern (explain why, not just what)
6. Design structured output format

**Effort Estimate**: 10-12 hours
- Research: 2 hours
- Framework design: 2 hours
- Examples (4 languages): 4 hours
- Output format & governance: 2 hours
- Testing: 2 hours

**Success Criteria**:
- ✅ Score 9/10 on audit
- ✅ Three-tier feedback system clearly defined
- ✅ 4+ language examples with comprehensive reviews
- ✅ Teaching-focused approach demonstrated
- ✅ Integrates with common code review tools (GitHub PR comments)

---

#### 3. API Design Consultant (Score: 9.0/10)

**Current State** (3/10):
```yaml
Description: "Creates RESTful API specifications"
Prompt: Basic requirements (endpoints, schemas, error handling, security)
Variables: Placeholders only
Examples: None
Governance: None
```

**Gaps**:
- ❌ No API design methodology (0/2)
- ❌ No OpenAPI spec output (0/2)
- ❌ No realistic API example (0/2)
- ❌ No versioning, deprecation strategy (0/2)
- ❌ Minimal guidance (1/2)

**Target State** (9/10):
```yaml
Persona: "API architect with expertise in RESTful design, OpenAPI 3.1, GraphQL, 
          and gRPC. Follows REST maturity model (Richardson), API-first design, 
          and web standards (RFC 7231, RFC 7807). Specializes in backward 
          compatibility and API evolution."

Research Foundation:
  - REST Architectural Style (Fielding, 2000)
  - Richardson Maturity Model
  - OpenAPI Specification 3.1
  - RFC 7231 (HTTP/1.1 Semantics)
  - RFC 7807 (Problem Details for HTTP APIs)
  - API Design Patterns (Daigneau, 2011)

Design Framework:
  1. Resource Modeling: Identify entities, relationships, operations
  2. Endpoint Design: RESTful conventions, URI design, HTTP methods
  3. Schema Design: Request/response models, validation rules
  4. Error Handling: RFC 7807 problem details, error codes
  5. Security: OAuth 2.0, API keys, rate limiting, CORS
  6. Versioning: URL vs header vs content negotiation
  7. Documentation: OpenAPI spec, examples, SDKs

Structured Output:
  - Complete OpenAPI 3.1 YAML specification
  - API design decision record (ADR) document
  - Security threat model (STRIDE analysis)
  - Rate limiting & throttling strategy
  - Versioning & deprecation policy

Realistic Examples:
  1. E-commerce Order Management API (CRUD, search, filtering)
     - Resources: /orders, /orders/{id}, /orders/{id}/items
     - OpenAPI spec with schemas, parameters, responses
     - OAuth 2.0 security scheme
     - Pagination (cursor-based)
     - Rate limiting (100 req/min per user)
  
  2. Real-time Notification API (webhooks, WebSocket alternative)
     - Webhook registration and management
     - Event payload schemas
     - Retry logic and idempotency
     - Signature verification

Governance:
  - governance_tags: ["requires-human-review", "architecture-decision"]
  - data_classification: "Confidential"
  - risk_level: "High"
  - approval_required: "Staff Engineer"
  - retention_period: "5 years"

Tips:
  - Design for clients first (developer experience)
  - Version from day 1 (don't wait for v2)
  - Use OpenAPI generators for SDKs and docs
  - Plan deprecation policy before launch
  - Test with real client implementations
  - Consider GraphQL for complex query needs
  - Use hypermedia (HATEOAS) for discoverability
```

**Uplift Approach**:
1. Study OpenAPI 3.1 specification
2. Define API design framework based on Richardson Maturity Model
3. Create complete e-commerce API example with OpenAPI YAML
4. Add versioning strategies comparison (URL vs header)
5. Include security threat model (STRIDE)
6. Design decision record template

**Effort Estimate**: 12-14 hours
- Research: 2 hours
- Framework design: 2 hours
- OpenAPI examples: 5 hours
- Security & versioning: 2 hours
- Testing & validation: 2 hours

**Success Criteria**:
- ✅ Score 9/10 on audit
- ✅ Complete OpenAPI 3.1 spec example
- ✅ Validates in Swagger Editor
- ✅ Includes security schemes and rate limiting
- ✅ Versioning strategy clearly defined

---

#### 4. Microservices Architect (Score: 8.8/10)

**Current State** (3/10):
```yaml
Description: "Designs microservices architectures"
Prompt: Basic components (service decomposition, communication, data, discovery)
Variables: Placeholders only
Examples: None
Governance: None
```

**Gaps**:
- ❌ No DDD methodology (0/2)
- ❌ No architecture diagram (0/2)
- ❌ No real decomposition example (0/2)
- ❌ No governance for architecture decisions (0/2)
- ❌ Minimal patterns (1/2)

**Target State** (9/10):
```yaml
Persona: "Staff-level microservices architect specializing in Domain-Driven Design, 
          Event Storming, and 12-Factor App principles. Expert in service boundaries, 
          distributed systems patterns, and organizational alignment (Conway's Law). 
          Experienced with service mesh (Istio, Linkerd) and observability."

Research Foundation:
  - Domain-Driven Design (Evans, 2003)
  - Building Microservices (Newman, 2021)
  - 12-Factor App methodology
  - Microservices Patterns (Richardson, 2018)
  - Conway's Law and Team Topologies (Skelton, 2019)
  - CAP Theorem, Saga Pattern, CQRS

Design Framework:
  1. Strategic Design (DDD)
     - Event Storming: Identify domain events, aggregates, bounded contexts
     - Context mapping: Relationships between contexts
     - Ubiquitous language per bounded context
  
  2. Service Decomposition
     - Business capability mapping
     - Subdomain analysis (Core, Supporting, Generic)
     - Service granularity assessment (not too fine, not too coarse)
  
  3. Inter-Service Communication
     - Synchronous: REST, gRPC (when to use each)
     - Asynchronous: Event-driven (Kafka, RabbitMQ)
     - Choreography vs Orchestration
  
  4. Data Management
     - Database per service pattern
     - Saga pattern for distributed transactions
     - CQRS and Event Sourcing (when appropriate)
     - Data consistency strategies (eventual vs strong)
  
  5. Cross-Cutting Concerns
     - Service mesh (traffic management, security, observability)
     - API Gateway pattern
     - Distributed tracing (OpenTelemetry)
     - Circuit breakers and resilience patterns
  
  6. Deployment & Operations
     - Containerization (Docker, Kubernetes)
     - Service discovery (Consul, Eureka)
     - Configuration management (ConfigMaps, external config)
     - Monitoring and alerting (Prometheus, Grafana)

Structured Output:
  - Event storming results (domain events, aggregates, commands)
  - Service boundary diagram with C4 model
  - Inter-service communication map
  - Data flow diagrams
  - Technology stack recommendations
  - Migration roadmap (if greenfield or brownfield)

Realistic Example:
  **E-commerce Platform Decomposition**
  
  **Current**: 300K LOC monolith
  **Goal**: Decompose into microservices
  
  **Event Storming Results**:
  - Domain Events: OrderPlaced, PaymentProcessed, InventoryReserved, 
    OrderShipped, OrderDelivered, RefundIssued
  - Aggregates: Order, Payment, Inventory, Shipment, Customer
  - Bounded Contexts: Order Management, Payment, Inventory, Fulfillment, 
    Customer Management
  
  **Service Decomposition** (7 services):
  1. **Order Service** (Core)
     - Responsibilities: Order CRUD, order lifecycle, order history
     - Data: Orders, OrderItems
     - API: REST (synchronous queries), Events (OrderPlaced, OrderCancelled)
  
  2. **Payment Service** (Core)
     - Responsibilities: Payment processing, refunds, transaction history
     - Data: Payments, Transactions
     - API: REST for queries, Events for completion
     - External: Stripe API integration
  
  3. **Inventory Service** (Core)
     - Responsibilities: Stock management, reservations, allocation
     - Data: Inventory, Reservations
     - API: gRPC (low latency for stock checks), Events
  
  4. **Fulfillment Service** (Supporting)
     - Responsibilities: Shipping, tracking, delivery confirmation
     - Data: Shipments, TrackingInfo
     - API: Events (OrderShipped), REST for tracking queries
  
  5. **Customer Service** (Supporting)
     - Responsibilities: Customer profiles, preferences, history
     - Data: Customers, Addresses
     - API: REST
  
  6. **Notification Service** (Generic)
     - Responsibilities: Email, SMS, push notifications
     - Data: NotificationTemplates, NotificationLogs
     - API: Events (consumes all domain events)
  
  7. **API Gateway**
     - BFF (Backend for Frontend) pattern
     - Aggregates data from multiple services
     - Authentication/authorization
     - Rate limiting
  
  **Communication Patterns**:
  - Sync: API Gateway → Services (gRPC for internal, REST for public)
  - Async: Services → Kafka topics → Services (domain events)
  - Saga: Order placement (Order → Payment → Inventory → Fulfillment)
  
  **Data Strategy**:
  - Each service has own database (PostgreSQL)
  - Event Sourcing for Payment Service (audit trail)
  - CQRS for Order Service (read-heavy queries)
  - Eventual consistency accepted (seconds, not milliseconds)
  
  **Service Mesh**: Istio for:
  - mTLS between services
  - Circuit breakers (3 failures → open for 30s)
  - Retries (exponential backoff)
  - Distributed tracing
  
  **Migration Strategy** (Strangler Fig):
  - Phase 1 (3 months): Extract Payment Service (standalone, high-value)
  - Phase 2 (3 months): Extract Inventory Service (scales independently)
  - Phase 3 (4 months): Extract Order Service (core, complex)
  - Phase 4 (2 months): Extract remaining services
  - Total: 12 months

Governance:
  - governance_tags: ["architecture-decision", "requires-human-review"]
  - data_classification: "Confidential"
  - risk_level: "Critical"
  - approval_required: "Principal Engineer + CTO"
  - retention_period: "10 years"
  - adr_required: true (Architecture Decision Records)

Tips:
  - Start with Event Storming (2-day workshop with domain experts)
  - Don't over-decompose (start with 5-7 services, not 50)
  - Design for failure (circuit breakers, timeouts, retries)
  - Observability is non-negotiable (logging, metrics, tracing)
  - Team structure follows service boundaries (Conway's Law)
  - Consider "modular monolith" first if team < 20 developers
  - Use Saga pattern, not distributed transactions (2PC is fragile)
  - Plan for eventual consistency from day 1
```

**Uplift Approach**:
1. Study DDD and Event Storming methodology
2. Create comprehensive e-commerce decomposition example
3. Design C4 model diagrams for service architecture
4. Add migration roadmap (Strangler Fig pattern)
5. Include Saga pattern example for distributed transactions
6. Add Conway's Law and team topology considerations

**Effort Estimate**: 16-18 hours (most complex prompt)
- Research: 3 hours
- Event Storming framework: 3 hours
- E-commerce example: 6 hours
- Diagrams (C4 model): 3 hours
- Migration roadmap: 2 hours
- Testing: 2 hours

**Success Criteria**:
- ✅ Score 9/10 on audit
- ✅ Complete Event Storming example
- ✅ C4 model diagrams (Context, Container, Component)
- ✅ Service decomposition with 5-7 services clearly defined
- ✅ Migration roadmap with phases

---

#### 5. DevOps Pipeline Architect (Score: 8.8/10)

**Current State** (3/10):
```yaml
Description: "Designs CI/CD pipelines"
Prompt: Basic stages (testing, deployment, monitoring, security, rollback)
Variables: Placeholders only
Examples: None
Governance: None
```

**Gaps**:
- ❌ No pipeline design methodology (0/2)
- ❌ No actual pipeline configuration (0/2)
- ❌ No realistic example (0/2)
- ❌ No approval workflow (0/2)
- ❌ Minimal patterns (1/2)

**Target State** (9/10):
```yaml
Persona: "DevOps architect specializing in CI/CD pipeline design, GitOps, 
          infrastructure as code, and deployment strategies. Expert in 
          GitHub Actions, GitLab CI, Jenkins, ArgoCD. Follows DORA metrics 
          framework and accelerates software delivery."

Research Foundation:
  - Accelerate (Forsgren, Humble, Kim, 2018) - DORA metrics
  - The DevOps Handbook (Kim, Humble, Debois, Willis, 2016)
  - GitOps principles (Weaveworks)
  - 12-Factor App methodology
  - NIST Secure Software Development Framework

Pipeline Design Framework:
  1. Source Control
     - Git branching strategy (trunk-based, GitFlow)
     - PR/MR workflow
     - Code ownership (CODEOWNERS)
  
  2. Build Stage
     - Dependency management and caching
     - Build optimization (parallel builds, incremental)
     - Artifact generation
  
  3. Test Pyramid
     - Unit tests (< 5 min, run on every commit)
     - Integration tests (< 15 min)
     - E2E tests (< 30 min, subset on PR, full on main)
     - Performance/load tests (nightly)
  
  4. Security Scanning
     - SAST (SonarQube, CodeQL)
     - Dependency scanning (Snyk, Dependabot)
     - Container scanning (Trivy, Anchore)
     - Secrets detection (GitGuardian, TruffleHog)
  
  5. Deployment Strategies
     - Blue-Green deployment
     - Canary deployment (10% → 50% → 100%)
     - Rolling updates
     - Feature flags for rollback
  
  6. Monitoring & Observability
     - Metrics: RED (Rate, Errors, Duration)
     - Logging: Structured logs with trace IDs
     - Distributed tracing: OpenTelemetry
     - SLOs and error budgets
  
  7. Rollback & Recovery
     - Automated rollback triggers (error rate > 5%)
     - Database migration rollback strategy
     - Backup and restore procedures

Structured Output:
  - Complete GitHub Actions / GitLab CI YAML
  - Architecture diagram (stages, dependencies, triggers)
  - DORA metrics targets (deployment freq, lead time, MTTR, change fail %)
  - Security gate policies
  - Rollback runbook

Realistic Example:
  **Node.js Microservice Pipeline (GitHub Actions)**
  
  ```yaml
  name: CI/CD Pipeline
  
  on:
    push:
      branches: [main, develop]
    pull_request:
      branches: [main]
  
  env:
    NODE_VERSION: '18'
    DOCKER_REGISTRY: ghcr.io
  
  jobs:
    # Stage 1: Build & Unit Tests (< 5 min)
    build:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        
        - name: Setup Node.js
          uses: actions/setup-node@v3
          with:
            node-version: ${{ env.NODE_VERSION }}
            cache: 'npm'
        
        - name: Install dependencies
          run: npm ci
        
        - name: Lint
          run: npm run lint
        
        - name: Unit tests
          run: npm test -- --coverage
        
        - name: Upload coverage
          uses: codecov/codecov-action@v3
    
    # Stage 2: Security Scanning (parallel with build)
    security:
      runs-on: ubuntu-latest
      permissions:
        security-events: write
      steps:
        - uses: actions/checkout@v3
        
        - name: Run SAST (CodeQL)
          uses: github/codeql-action/analyze@v2
        
        - name: Dependency scan (Snyk)
          uses: snyk/actions/node@master
          env:
            SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        
        - name: Secret scanning
          uses: trufflesecurity/trufflehog@main
    
    # Stage 3: Integration Tests
    integration:
      needs: build
      runs-on: ubuntu-latest
      services:
        postgres:
          image: postgres:15
          env:
            POSTGRES_PASSWORD: test
      steps:
        - uses: actions/checkout@v3
        - name: Run integration tests
          run: npm run test:integration
    
    # Stage 4: Build Docker Image
    docker:
      needs: [build, security, integration]
      runs-on: ubuntu-latest
      if: github.event_name == 'push'
      steps:
        - uses: actions/checkout@v3
        
        - name: Build image
          run: docker build -t ${{ env.DOCKER_REGISTRY }}/${{ github.repository }}:${{ github.sha }} .
        
        - name: Scan image (Trivy)
          uses: aquasecurity/trivy-action@master
          with:
            image-ref: ${{ env.DOCKER_REGISTRY }}/${{ github.repository }}:${{ github.sha }}
            severity: 'CRITICAL,HIGH'
            exit-code: 1
        
        - name: Push image
          run: docker push ${{ env.DOCKER_REGISTRY }}/${{ github.repository }}:${{ github.sha }}
    
    # Stage 5: Deploy to Staging
    deploy-staging:
      needs: docker
      runs-on: ubuntu-latest
      if: github.ref == 'refs/heads/develop'
      environment:
        name: staging
        url: https://staging.example.com
      steps:
        - name: Deploy to Kubernetes
          uses: azure/k8s-deploy@v4
          with:
            manifests: k8s/staging/
            images: ${{ env.DOCKER_REGISTRY }}/${{ github.repository }}:${{ github.sha }}
        
        - name: Run smoke tests
          run: |
            curl -f https://staging.example.com/health || exit 1
    
    # Stage 6: Deploy to Production (Canary)
    deploy-production:
      needs: docker
      runs-on: ubuntu-latest
      if: github.ref == 'refs/heads/main'
      environment:
        name: production
        url: https://example.com
      steps:
        - name: Canary deployment (10%)
          uses: azure/k8s-deploy@v4
          with:
            manifests: k8s/production/canary.yaml
            images: ${{ env.DOCKER_REGISTRY }}/${{ github.repository }}:${{ github.sha }}
        
        - name: Monitor canary (5 min)
          run: |
            sleep 300
            ERROR_RATE=$(curl -s https://metrics.example.com/error_rate)
            if (( $(echo "$ERROR_RATE > 0.05" | bc -l) )); then
              echo "Error rate too high: $ERROR_RATE"
              exit 1
            fi
        
        - name: Promote to full deployment
          uses: azure/k8s-deploy@v4
          with:
            manifests: k8s/production/deployment.yaml
            images: ${{ env.DOCKER_REGISTRY }}/${{ github.repository }}:${{ github.sha }}
    
    # Stage 7: Post-Deployment Tests
    e2e-tests:
      needs: deploy-production
      runs-on: ubuntu-latest
      if: github.ref == 'refs/heads/main'
      steps:
        - uses: actions/checkout@v3
        
        - name: Run E2E tests
          run: npm run test:e2e
          env:
            BASE_URL: https://example.com
  ```
  
  **DORA Metrics Targets**:
  - Deployment frequency: Multiple per day (main branch commits)
  - Lead time: < 1 hour (commit to production)
  - MTTR: < 15 minutes (automated rollback)
  - Change failure rate: < 15%

Governance:
  - governance_tags: ["architecture-decision", "security-critical"]
  - data_classification: "Confidential"
  - risk_level: "High"
  - approval_required: "DevOps Lead"
  - retention_period: "5 years"

Tips:
  - Optimize for DORA metrics (deploy freq, lead time, MTTR)
  - Test pyramid: Many unit tests, fewer integration, few E2E
  - Security gates must be fast (< 5 min) or run parallel
  - Canary deployments for production (10% → 50% → 100%)
  - Feature flags for quick rollback without redeploy
  - Monitor deployments with SLOs (error rate, latency)
  - Use GitOps (ArgoCD) for declarative deployments
  - Cache aggressively (dependencies, Docker layers)
```

**Uplift Approach**:
1. Study DORA metrics and Accelerate book
2. Create complete GitHub Actions pipeline example
3. Add deployment strategies comparison (Blue-Green, Canary, Rolling)
4. Include security scanning integration
5. Design monitoring and rollback triggers
6. Add DORA metrics targets

**Effort Estimate**: 12-14 hours
- Research: 2 hours
- Framework design: 2 hours
- GitHub Actions YAML: 5 hours
- Deployment strategies: 2 hours
- Monitoring & rollback: 2 hours
- Testing: 2 hours

**Success Criteria**:
- ✅ Score 9/10 on audit
- ✅ Complete working GitHub Actions pipeline
- ✅ Validates with `actionlint`
- ✅ Includes security scanning and canary deployment
- ✅ DORA metrics targets defined

---

### Priority 1: High Value (Weeks 9-16)

---

#### 6. Test Automation Engineer (Score: 8.6/10)

**Current State** (3/10):
- Basic test pyramid mention
- No concrete test framework examples
- No test data management strategy

**Target State** (9/10):
```yaml
Persona: "Test automation engineer specializing in Test Pyramid, TDD, BDD, 
          and test data management. Expert in Jest, Pytest, JUnit, Selenium, 
          Cypress. Designs testable architectures and CI integration."

Framework: Test Pyramid, Test-Driven Development, Behavior-Driven Development

Output:
  - Complete test suite (unit, integration, E2E)
  - Test configuration (Jest/Pytest config files)
  - Test data factories and fixtures
  - CI integration (GitHub Actions test stage)

Examples:
  1. React component testing (Jest + Testing Library)
  2. API integration tests (Supertest, Pytest fixtures)
  3. E2E tests (Cypress, Playwright)
  4. Performance tests (k6, JMeter)

Governance:
  - risk_level: "Medium"
  - approval_required: "Tech Lead"
```

**Uplift Approach**:
1. Define test pyramid with ratios (70% unit, 20% integration, 10% E2E)
2. Create examples for each test level
3. Add test data management patterns (factories, fixtures, mocks)
4. Include CI integration examples
5. Add TDD workflow demonstration

**Effort Estimate**: 10-12 hours

---

#### 7. Database Schema Designer (Score: 8.8/10)

**Current State** (3/10):
- Basic requirements (ERD, tables, indexes, normalization)
- No actual schema example
- No migration scripts

**Target State** (9/10):
```yaml
Persona: "Database architect specializing in relational design, normalization, 
          indexing strategies, and performance optimization. Expert in PostgreSQL, 
          MySQL. Follows data modeling best practices."

Framework:
  - Entity-Relationship Modeling
  - Normalization (1NF → 3NF → BCNF)
  - Index design (B-tree, Hash, GiST, GIN)
  - Query optimization
  - Migration strategies (zero-downtime)

Output:
  - ERD diagram (Mermaid syntax)
  - Complete SQL DDL (CREATE TABLE, INDEX, CONSTRAINT)
  - Migration scripts (up/down)
  - Query examples with EXPLAIN ANALYZE
  - Indexing strategy rationale

Examples:
  1. E-commerce schema (orders, products, customers, inventory)
     - Full DDL with constraints
     - Index strategy (composite indexes, partial indexes)
     - Migration script with zero-downtime approach
  2. Multi-tenant SaaS schema (row-level security)

Governance:
  - risk_level: "High"
  - approval_required: "Staff Engineer"
  - data_classification: "Confidential"
```

**Uplift Approach**:
1. Study normalization theory and indexing strategies
2. Create complete e-commerce schema with DDL
3. Add ERD diagram in Mermaid format
4. Include migration scripts (Flyway/Liquibase style)
5. Add query optimization examples with EXPLAIN

**Effort Estimate**: 12-14 hours

---

#### 8. Code Generation Assistant (Score: 7.8/10)

**Current State** (3/10):
- Generic "generate clean code" instruction
- No language-specific patterns
- No testing or documentation

**Target State** (9/10):
```yaml
Persona: "Senior software engineer expert in multiple languages (Python, 
          JavaScript, Java, Go, Rust). Generates production-ready, tested, 
          documented code following language idioms and best practices."

Framework:
  - Language-specific style guides (PEP 8, Google Java Style, etc.)
  - SOLID principles
  - Design patterns
  - Error handling patterns
  - Testing patterns (AAA, Given-When-Then)

Output:
  - Production code with error handling
  - Unit tests (>80% coverage)
  - Documentation (docstrings, JSDoc, Javadoc)
  - Usage examples
  - Type annotations (Python, TypeScript)

Examples:
  1. Python API client with async/await, retries, error handling, tests
  2. React custom hook with TypeScript, tests, Storybook
  3. Java service class with DI, logging, tests
  4. Go HTTP middleware with context, logging, tests

Governance:
  - risk_level: "Medium"
  - approval_required: "Code Review"
```

**Uplift Approach**:
1. Define code generation template (code + tests + docs)
2. Create 4 language examples (Python, TypeScript, Java, Go)
3. Add error handling patterns per language
4. Include testing examples (unit tests for generated code)
5. Add documentation standards (docstrings, comments)

**Effort Estimate**: 10-12 hours

---

#### 9. Performance Optimization Specialist (Score: 8.0/10)

**Current State** (3/10):
- Generic optimization areas
- No profiling methodology
- No concrete examples

**Target State** (9/10):
```yaml
Persona: "Performance engineer specializing in profiling, benchmarking, and 
          optimization. Expert in APM tools (New Relic, Datadog), profilers 
          (py-spy, Node.js profiler), and performance patterns."

Framework:
  - Performance profiling workflow
  - Bottleneck identification (CPU, I/O, memory, network)
  - Optimization strategies (caching, query optimization, concurrency)
  - Benchmarking methodology
  - Monitoring and SLOs

Output:
  - Profiling report with flamegraphs
  - Bottleneck analysis with root causes
  - Optimization recommendations (prioritized by impact)
  - Benchmark results (before/after)
  - Monitoring dashboards

Examples:
  1. Python API optimization (N+1 queries, async I/O, caching)
     - Profiling: py-spy flamegraph showing database calls
     - Fix: Batch queries, add Redis cache
     - Result: 200ms → 50ms response time
  2. React rendering performance (unnecessary re-renders)
     - Profiling: React DevTools showing render counts
     - Fix: useMemo, React.memo, virtualization
     - Result: 3s → 500ms load time

Governance:
  - risk_level: "Medium"
  - approval_required: "Tech Lead"
```

**Uplift Approach**:
1. Define performance profiling workflow
2. Create 2 detailed examples with before/after profiling
3. Add flamegraph interpretation guide
4. Include optimization pattern catalog (caching, batching, etc.)
5. Design monitoring dashboard templates

**Effort Estimate**: 10-12 hours

---

### Priority 2: Specialized High-Impact (Weeks 17-20)

---

#### 10. Legacy System Modernization (Score: 8.0/10)

**Current State** (3/10):
- Not currently in prompts directory (needs creation or uplift from system/)

**Target State** (9/10):
```yaml
Persona: "Modernization architect specializing in strangler fig pattern, 
          domain-driven design, and incremental migration. Expert in assessing 
          technical debt, risk mitigation, and team training."

Framework:
  - Assessment (code metrics, dependency analysis, technical debt)
  - Strategy selection (rewrite, refactor, replace, retire)
  - Strangler fig pattern for incremental migration
  - DDD for identifying bounded contexts
  - Change management and team training

Output:
  - Technical debt assessment report
  - Migration strategy comparison (rewrite vs refactor vs replace)
  - Phased migration roadmap
  - Risk mitigation plan
  - Team training plan

Examples:
  1. Monolith to microservices migration (300K LOC)
     - Assessment: Dependency graph, hotspot analysis
     - Strategy: Strangler fig, extract bounded contexts
     - Roadmap: 18-month phased approach
     - Risk: API versioning, data migration, team training

Governance:
  - risk_level: "Critical"
  - approval_required: "CTO"
  - data_classification: "Confidential"
```

**Uplift Approach**:
1. Study strangler fig pattern and Martin Fowler's refactoring
2. Create comprehensive migration assessment framework
3. Design phased migration roadmap template
4. Add risk mitigation strategies
5. Include real migration example with lessons learned

**Effort Estimate**: 12-14 hours

---

## Batch Grouping Strategy

**Batch 1: Security & Quality Foundation** (Weeks 1-4)
- ✅ security-code-auditor
- ✅ code-review-expert
- ✅ test-automation-engineer

**Why Together**: All focus on code quality and security. Can share governance patterns, testing examples, and security frameworks.

**Batch 2: Architecture & Design** (Weeks 5-8)
- ✅ microservices-architect
- ✅ api-design-consultant
- ✅ database-schema-designer

**Why Together**: All architecture decisions with high strategic impact. Can share DDD methodology, C4 diagrams, and decision records.

**Batch 3: DevOps & Performance** (Weeks 9-12)
- ✅ devops-pipeline-architect
- ✅ performance-optimization-specialist
- ✅ code-generation-assistant

**Why Together**: All focus on operational excellence and developer productivity. Can share CI/CD patterns and monitoring strategies.

**Batch 4: Specialized** (Weeks 13-16)
- ✅ legacy-system-modernization
- (Plus 3-4 additional prompts from Priority 1 if time permits)

---

## Success Metrics

**Quality Metrics**:
- ✅ All 10 prompts score 9-10/10 on audit rubric
- ✅ 100% have realistic, complete examples
- ✅ 100% have structured output formats (JSON schemas or templates)
- ✅ 100% have governance metadata
- ✅ 100% cite relevant frameworks/standards

**Impact Metrics** (6 months post-uplift):
- 📈 Web app usage increase: +40% for uplifted prompts
- 📈 User satisfaction: >85% "very satisfied" rating
- 📈 Repository stars/forks: +50% growth
- 📈 External citations: Repository referenced in 10+ blog posts/articles

**Adoption Metrics**:
- 📊 Top 3 most-used prompts include at least 2 from uplift list
- 📊 Average time spent per prompt: +30% (more comprehensive, more valuable)
- 📊 Copy-to-clipboard actions: +25%

---

## Risk Mitigation

**Risk 1: Effort Underestimation**
- **Likelihood**: Medium
- **Impact**: High (delayed completion)
- **Mitigation**: 
  - Add 20% buffer to all estimates
  - Start with easiest prompt (code-review-expert) to validate process
  - Checkpoint after Batch 1 (week 4) to assess velocity

**Risk 2: Quality Regression**
- **Likelihood**: Low
- **Impact**: High (reputation damage)
- **Mitigation**:
  - Mandatory peer review (2+ approvals)
  - Test all examples with actual AI models
  - User testing with 5-10 target users before merge

**Risk 3: Governance Inconsistency**
- **Likelihood**: Medium
- **Impact**: Medium (confusion, compliance gaps)
- **Mitigation**:
  - Create governance template from `security-incident-response.md`
  - Review all governance fields in Batch 1 before proceeding
  - Maintain governance field glossary

**Risk 4: Example Obsolescence**
- **Likelihood**: Medium (tech changes fast)
- **Impact**: Medium (examples become outdated)
- **Mitigation**:
  - Use stable technologies (PostgreSQL, REST, Docker) for examples
  - Include version numbers (Node.js 18, Python 3.11)
  - Schedule annual review cycle

---

## Next Steps

### Week 1: Setup & Planning
1. ✅ Review this uplift plan with maintainers
2. ✅ Assign contributors to Batch 1 prompts (3 prompts, 1-2 contributors each)
3. ✅ Create GitHub issues for each prompt uplift
4. ✅ Establish review workflow (PR template, review checklist)
5. ✅ Create governance template based on existing Tier 1 prompts

### Week 2-4: Batch 1 Execution
1. Uplift `security-code-auditor` (contributor A)
2. Uplift `code-review-expert` (contributor B)
3. Uplift `test-automation-engineer` (contributor C)
4. Peer review and test all 3 prompts
5. Merge to main and announce in README

### Week 5: Checkpoint & Iteration
1. Retrospective: What worked? What didn't?
2. Adjust estimates and approach for Batch 2
3. Measure early impact (web app analytics)
4. Refine governance template based on learnings

### Week 6-20: Continue with Batches 2-4
- Follow established workflow
- Maintain quality standards
- Celebrate milestones (5 prompts done, 10 prompts done)

---

## Appendix A: Audit Rubric Reference

**5 Dimensions (0-2 points each)**:

1. **Role Clarity** (0-2)
   - 2: Expert persona with specific methodology
   - 1: Generic role without depth
   - 0: Minimal/no role definition

2. **Structured Outputs** (0-2)
   - 2: Templates, schemas, formatted structures
   - 1: Basic structure (numbered lists)
   - 0: No formatting guidance

3. **Examples** (0-2)
   - 2: Realistic, comprehensive examples
   - 1: Basic placeholder examples
   - 0: No examples

4. **Governance Metadata** (0-2)
   - 2: Complete governance fields
   - 1: Partial governance tags
   - 0: No governance metadata

5. **Depth** (0-2)
   - 2: Comprehensive with tips, variations, research
   - 1: Basic coverage
   - 0: Minimal content

**Total Score**: 0-10 points
- **Tier 1**: 9-10 (Gold standard)
- **Tier 2**: 6-8 (Good quality)
- **Tier 3**: 0-5 (Needs uplift)

---

## Appendix B: Gold Standard Reference Prompts

Study these as templates:

1. **chain-of-thought-guide.md** (10/10)
   - Research citations (Wei et al. NeurIPS 2022)
   - Decision framework (when to use each mode)
   - Comprehensive examples (API debugging, architecture decisions)
   - Cost-benefit analysis
   - Integration patterns
   - Governance metadata

2. **reflection-self-critique.md** (9/10)
   - Two-phase pattern (initial + critique)
   - Comprehensive critique framework
   - Detailed microservices example showing bias detection
   - JSON schema for automation
   - Governance notes

3. **security-incident-response.md** (10/10)
   - NIST framework integration
   - GDPR compliance mapping
   - Real incident example
   - Audit requirements
   - Escalation workflows

---

**End of Uplift Plan**

*Total estimated effort*: **140-160 hours** for all 10 prompts  
*Timeline*: **16-20 weeks** (batched approach)  
*Expected outcome*: **59% of developer prompts at Tier 1 quality**
