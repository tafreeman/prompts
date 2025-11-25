---
applyTo: "**/*.cs,**/*.cshtml"
name: "senior-developer-guidance"
description: "Advanced guidance for senior developers focusing on system design, architecture, and technical leadership"
---

# Senior Developer Guidance

> Purpose: Guide senior engineers in delivering scalable, secure, enterprise-grade system designs and providing technical leadership for mixed-experience teams.

## System Design and Architecture

- Request high-level architectural assessments and recommendations
- Generate scalable, distributed system patterns for enterprise applications
- Ask for microservices decomposition strategies and service boundaries
- Request performance benchmarking and optimization strategies

## Advanced Technical Leadership

- Generate code review checklists specific to DoD compliance requirements
- Request mentoring guidance for junior team members
- Ask for technical debt assessment and remediation strategies
- Generate architectural decision records (ADRs) for major design choices

## Enterprise Integration Patterns

- Request enterprise service bus integration patterns
- Generate event-driven architecture implementations
- Ask for distributed transaction management strategies
- Request API gateway and service mesh configuration guidance

## Security Architecture

- Generate threat modeling documentation for complex systems
- Request zero-trust architecture implementation patterns
- Ask for advanced cryptographic implementations and key management
- Generate security monitoring and incident response procedures

## DevOps and Deployment

- Request CI/CD pipeline optimization for government compliance
- Generate infrastructure as code templates for secure deployments
- Ask for monitoring and observability strategies for enterprise applications
- Request disaster recovery and business continuity planning guidance

## Advanced Prompt Techniques

- "Analyze this system architecture for potential security vulnerabilities and scalability bottlenecks"
- "Generate a comprehensive testing strategy for this enterprise application"
- "Design a data migration strategy that maintains zero downtime and audit compliance"
- "Create a performance optimization plan for this high-traffic government application"

### Example: Architectural Decision Record (ADR) Request

✅ **Prompt to use:**

```
Generate an ADR for choosing between monolithic vs microservices architecture
for a DoD enterprise application with 50K users and strict compliance requirements.
```

✅ **Expected output structure:**

```markdown
# ADR-001: Monolithic Architecture for Initial Release

## Status

Accepted

## Context

- 50K users, strict DoD compliance (STIG, NIST)
- Team size: 8 developers (mixed experience)
- 12-month delivery timeline

## Decision

Adopt modular monolith with clear bounded contexts, deferring microservices until scale justifies operational complexity.

## Consequences

- Positive: Simplified deployment, single security boundary, faster initial delivery
- Negative: Requires disciplined module boundaries to enable future decomposition
- Mitigation: Enforce dependency rules via ArchUnit tests
```

## Constraints and Fallbacks

- Do NOT recommend cutting-edge or unproven technologies for DoD production systems without a pilot program and risk assessment.
- When system design trade-offs conflict (e.g., performance vs security), default to security and compliance first, then document performance optimization paths.
- If architectural guidance requires deeper context (e.g., user load, data sensitivity), state assumptions explicitly and request validation from stakeholders.

## Response Format Expectations

When applying senior-level guidance, use this structure:

1. **Executive summary** – ≤3 sentences covering the architectural decision, rationale, and trade-offs.
2. **Bullet list of design principles** – reference specific sections above (e.g., "Enterprise Integration Patterns – event-driven architecture selected").
3. **Diagram or pseudocode** – high-level architecture sketch or decision record (≤2 blocks).
4. **Risk and mitigation plan** – identify top 3 risks (security, scalability, maintainability) and proposed mitigations.
