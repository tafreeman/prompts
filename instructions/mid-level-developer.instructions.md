---
applyTo: "**/*.cs,**/*.cshtml"
name: "mid-level-developer-guidance"
description: "Guidance for mid-level developers focusing on architecture and optimization"
---

# Mid-Level Developer Guidance

> Prompt reference: `dotnet-prompts/developers/mid-level-developer-architecture-coach.md` is the Tier 1 AI prompt that mirrors this guidance. Keep both files synchronized; edit this instructions file first, then mirror wording in the prompt.

Mid-level engineers are expected to deliver production-ready C#/Razor solutions that are architecturally sound, secure, observable, and performant. Treat the standards below as mandatory unless the product owner explicitly approves a deviation.

## Core Responsibilities

- Provide end-to-end reasoning for every solution (pattern selection, trade-offs, scalability impact).
- Keep controllers/pages thin, async, and focused on orchestration; delegate business logic to injected services or domain layers.
- Favor dependency injection, interface-driven contracts, and SOLID adherence; document when exceptions are unavoidable.
- Surface risks early (performance, security, maintainability) with mitigation steps and escalation paths.

## Architecture & Patterns

- Apply layered/clean architecture boundaries (Presentation → Application → Domain → Infrastructure) and explain interaction points.
- Select patterns intentionally (CQRS, mediator, decorator, factory, etc.) and justify how they improve extensibility or isolation.
- Highlight cross-cutting concerns (logging, caching, authorization, tracing) and specify where they plug in (middleware, filters, pipelines).
- For Razor UI, separate view models from domain models and ensure partials/components remain logic-light.

## Integration & API Development

- Document request/response contracts, validation rules, and error envelopes for each endpoint.
- Specify middleware/filters for exception handling, correlation IDs, localization, throttling, or retries.
- Use parameterized queries or EF Core with explicit transaction scopes and connection lifecycle guidance.
- Provide rollout considerations (feature flags, backward compatibility, migrations/data seeding) for integrations.

## Security & Compliance

- Enforce least privilege, secure configuration loading, and prohibition of hardcoded secrets.
- Validate and sanitize all inputs; combine server-side guards with DataAnnotations/FluentValidation.
- Apply `[Authorize]` attributes/policies on protected endpoints and explain how roles map to actions.
- Log authentication/authorization failures, unusual payloads, and sensitive operations with structured logging; reference STIG/enterprise controls when relevant.

## Performance, Resilience & Operations

- Recommend caching strategies (in-memory, distributed) with eviction, expiration, and invalidation details.
- Define pagination/streaming strategies for large datasets; choose EF loading patterns (`Include`, projection, `AsNoTracking`) explicitly.
- Include retry/backoff policies, circuit breakers, and timeout rationale for outbound calls.
- Outline observability hooks: structured logs, metrics, tracing identifiers, and dashboards needed for root-cause analysis.

## Code Quality & Testing

- Supply refactoring plans that reduce complexity while preserving behavior; pair them with unit/integration test recommendations.
- Provide testing matrices (unit, integration, contract, performance) noting the most critical paths to automate.
- Produce concise technical documentation or inline summaries explaining non-obvious decisions (algorithms, third-party dependencies).
- Track technical debt explicitly and propose remediation timelines when trade-offs are accepted.

## Constraints and Fallbacks

- Do NOT introduce architectural patterns (e.g., CQRS, event sourcing) without justifying the complexity against project scale and team capability.
- When performance or security conflicts arise, prioritize security first, then document the performance trade-off and propose optimization paths.
- If context is incomplete (e.g., missing deployment targets, unclear NFRs), state assumptions explicitly and propose validation steps.

## Response Format Expectations

When applying these standards in an AI-generated response (or code review), use this structure:

1. **Summary (≤3 sentences)** – What you delivered and which goals/constraints it satisfies.
2. **Standards-Aligned Actions** – Bullet list referencing the sections above (e.g., "Security & Compliance – added policy-based authorization").
3. **Solution Details / Code** – Complete code, architecture narrative, or pseudo-steps showing DI wiring, async patterns, error handling, and cross-cutting concerns.
4. **Testing & Validation Plan** – Tests, metrics, and verification steps required before release.
5. **Deviations & Assumptions** – Explicit list of standards not met with rationale. Prefix each assumption with `Assumption:` and describe its impact.

Always reference the prompt noted above when AI assistance is required so the enforced structure and these standards stay in sync.
