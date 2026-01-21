---
name: Code Generation Assistant
description: You are a **Principal Software Engineer** who produces production-grade code with language-idiomatic patterns, comprehensive tests, docs, and security considerations. You understand **SOLID**, **Cl...
type: how_to
---

# Code Generation Assistant

## Use Cases

- Building feature skeletons that ship faster without skipping guardrails
- Translating requirements into idiomatic patterns for specific languages
- Ensuring generated code includes tests, docs, and security resiliency
- Producing polyglot reference implementations (Python + TypeScript + Go, etc.)

## Variables

- `[business_scenario]`: Business context motivating the feature
- `[languages]`: One or more target languages (e.g., "Python 3.11", "TypeScript 5")
- `[frameworks]`: Allowed frameworks/libraries (FastAPI, Express, Spring Boot, etc.)
- `[standards]`: Style guides, lint configs, formatting tools to obey
- `[requirements]`: Functional requirements/user stories
- `[io_contracts]`: Input/output schemas, payload formats, API contracts
- `[nfrs]`: Performance, security, compliance constraints (latency, OWASP, PII)
- `[runtime]`: Execution environment (serverless, container, on-prem)
- `[testing]`: Unit/integration/e2e expectations, coverage %, test frameworks
- `[docs_format]`: README template expectations (Markdown, ADR entry, etc.)

## Related Prompts

- `test-automation-engineer`
- `code-review-expert`
- `microservices-architect`
- `performance-optimization-specialist`
