---
name: Unified Documentation Library Builder
description: Builds a cohesive, traceable engineering documentation set (SDD, ADRs, user guides, runbooks, backlog mapping) from tickets, requirements, repo context, and release history.
type: how_to
difficulty: advanced
---

# Unified Documentation Library Builder

## Description

This prompt turns scattered engineering inputs (tickets, requirements, repo structure, release notes, and architectural decisions) into a single, organized documentation library with a consistent taxonomy and clear traceability. It is designed for software engineering teams who need usable docs fast: onboarding-ready, audit-friendly, and maintainable.

## Prompt

### System Prompt

```text
You are a senior Staff+ software engineer and technical writer. You build engineering documentation that is:
- Correct, specific, and traceable to sources
- Structured and maintainable (consistent taxonomy + file naming)
- Optimized for real workflows (build, ship, support, operate, onboard)

Critical rules:
- Do not invent facts, APIs, metrics, timelines, or decisions. If information is missing, ask targeted questions or mark TODOs with a clear owner suggestion.
- Treat the provided sources as the only truth. When unsure, say "Unknown" and propose how to confirm.
- Never output secrets. If the input includes secrets or PII, redact it and add a "Security note".
- Prefer concrete artifacts over narrative. Produce doc skeletons that teams can commit to a repo.

Your job: produce a cohesive documentation library + traceability map that connects requirements → decisions → implementation artifacts → releases.
```

### User Prompt

```text
Build a single cohesive engineering documentation library for:

Project: [PROJECT_NAME]
Primary audience(s): [AUDIENCE]
Tech stack / platform context: [TECH_STACK]
Operating model: [OPERATING_MODEL]

Inputs (paste what you have; partial is OK):
1) Tickets / backlog export: [TICKETS]
2) Requirements / PRDs / epics: [REQUIREMENTS]
3) Repo structure (tree) + key files: [REPO_STRUCTURE]
4) Existing documentation (links or excerpts): [EXISTING_DOCS]
5) Releases + changelog notes + associated tickets: [RELEASE_HISTORY]
6) Architecture decisions (existing ADRs, notes, diagrams): [ARCHITECTURE_DECISIONS]
7) Constraints + NFRs (SLOs, compliance, data classification, budgets): [CONSTRAINTS_AND_NFRS]

Deliverables (required):
A) Documentation Library Plan
B) Documentation Library File Tree
C) Generated Doc Skeletons (ready to paste into files)
D) Traceability Matrix (requirements ↔ tickets ↔ ADRs ↔ releases ↔ docs)
E) Backlog / Docs Maintenance Plan (how to keep it current)

Output requirements:
- Output in Markdown.
- Use stable headings and consistent naming.
- Wherever you make a claim derived from input, add a Source tag like: (Source: Tickets) or (Source: Release History) or (Source: Repo Structure).
- For any missing critical inputs, ask at most 8 clarifying questions, prioritized by impact.

=== A) Documentation Library Plan ===
1. First, summarize what you believe the system is, in 5-8 bullets. Include uncertainty flags.
2. Propose a documentation taxonomy that includes, at minimum:
   - /docs/overview/ (system overview, domain model)
   - /docs/architecture/ (SDD + diagrams + ADR index)
   - /docs/decisions/ (ADRs)
   - /docs/guides/ (user guides, operator guides)
   - /docs/runbooks/ (incident/runbook playbooks)
   - /docs/api/ (API contracts and conventions)
   - /docs/backlog/ (epics, roadmap, release mapping)
   - /docs/security/ (threat model summary, data classification, access model)
3. Define document ownership model (DRI), review cadence, and Definition-of-Done for docs.

=== B) Documentation Library File Tree ===
Produce a proposed repo folder tree (only the docs area). Use filenames that are:
- lowercase-hyphenated
- short but descriptive
- grouped by purpose

=== C) Generated Doc Skeletons ===
Generate the full contents for each new file (skeletons with TODOs where needed). Each file must include:
- Purpose
- Audience
- Inputs / prerequisites
- How to keep it updated
- Links to related docs

Minimum required files to generate:
1) docs/overview/system-overview.md
2) docs/architecture/system-design-document.md
3) docs/architecture/architecture-diagrams.md (Mermaid is fine)
4) docs/decisions/adr-index.md
5) docs/decisions/adr-0001-template.md
6) docs/guides/user-guide.md
7) docs/guides/operator-guide.md
8) docs/runbooks/incident-response-runbook.md
9) docs/backlog/roadmap-and-release-map.md
10) docs/backlog/ticket-traceability.md
11) docs/security/security-and-data-classification.md

Guidance for content quality:
- ADRs: include Context, Decision, Options Considered, Consequences, Links.
- SDD: include goals/non-goals, architecture overview, data flows, failure modes, scaling model, observability, security.
- Runbooks: include triggers, diagnosis, mitigations, rollback, communications, verification.

=== D) Traceability Matrix ===
Create a table that maps:
- Requirement / Epic → Tickets → ADR(s) → Release(s) → Doc(s)
Rules:
- If you cannot map an item, mark it as "Unmapped" and propose the best next action.

=== E) Backlog / Docs Maintenance Plan ===
Provide a lightweight process to keep docs current:
- What gets updated on every PR?
- What gets updated on every release?
- What gets updated during incidents?
- Suggested automation hooks (e.g., CI checks for ADR links, release notes generation)

Finally: provide a short "Commit Plan" describing in what order a team should add these docs over 2-3 sprints.
```

## Variables

| Variable | Description |
|---|---|
| `[PROJECT_NAME]` | Product/system name and (optionally) repository name. |
| `[AUDIENCE]` | Who the docs are for (e.g., "new engineers", "SRE/on-call", "internal users", "external customers"). |
| `[TECH_STACK]` | Languages, frameworks, hosting, key dependencies (e.g., ".NET 8 + Azure + Postgres"). |
| `[OPERATING_MODEL]` | Team model and ops assumptions (e.g., "one on-call rotation", "SaaS multi-tenant"). |
| `[TICKETS]` | A list/export of work items (Jira/AzDO/GitHub issues), including IDs, titles, and short descriptions. |
| `[REQUIREMENTS]` | PRDs, epics, acceptance criteria, NFRs. |
| `[REPO_STRUCTURE]` | Folder tree + pointers to key modules, services, APIs. |
| `[EXISTING_DOCS]` | Links/excerpts of any current docs to reuse (README, wiki, runbooks). |
| `[RELEASE_HISTORY]` | Tags/versions + release notes + linked tickets/PRs. |
| `[ARCHITECTURE_DECISIONS]` | Existing ADRs or decision notes; diagrams if available. |
| `[CONSTRAINTS_AND_NFRS]` | Compliance, SLOs, data classification, budgets, latency, availability, security constraints. |

## Example

### Input

```text
Project: Northwind Subscriptions Platform
Primary audience(s): New engineers, on-call engineers, internal support
Tech stack / platform context: Node.js (TypeScript), Kubernetes, Postgres, Redis, Stripe integration
Operating model: SaaS multi-tenant, weekly deployments, one primary on-call rotation

Tickets / backlog export:
- SUB-101: Add subscription cancellation flow (customer self-serve)
- SUB-118: Implement webhook verification for Stripe events
- SUB-133: Reduce p95 API latency from 900ms to <400ms
- SUB-140: Add audit log entries for subscription state changes

Requirements / PRDs / epics:
- Epic: Subscription lifecycle v1
  - Must support create/upgrade/downgrade/cancel
  - NFR: 99.9% availability, p95 < 400ms for /api/subscriptions/*
  - Compliance: audit log retained 1 year

Repo structure (tree) + key files:
- services/api/src/routes/subscriptions.ts
- services/api/src/services/stripe.ts
- services/worker/src/jobs/webhooks.ts
- infra/k8s/

Existing documentation:
- README.md: basic local dev instructions
- No runbooks yet

Releases + changelog notes + associated tickets:
- v0.8.0: initial subscription create (SUB-001)
- v0.9.0: upgrades/downgrades (SUB-090)

Architecture decisions:
- "Use Stripe as source of truth for payment events" (note in PR description)

Constraints + NFRs:
- Data classification: customer PII (email) is Confidential
- Must verify Stripe webhook signatures
- Observability: logs + traces required for all subscription endpoints
```

### Expected Output

```text
(Excerpt)

A) Documentation Library Plan
- System summary:
  - Multi-tenant subscriptions API with async webhook worker (Source: Repo Structure)
  - Uses Stripe for payment + eventing (Source: Architecture Decisions)
  - Key risks: webhook authenticity, latency SLO, audit log retention (Source: Constraints + NFRs)

B) File Tree
docs/
  overview/
    system-overview.md
  architecture/
    system-design-document.md
    architecture-diagrams.md
  decisions/
    adr-index.md
    adr-0001-template.md
    adr-0002-stripe-webhook-verification.md
  guides/
    user-guide.md
    operator-guide.md
  runbooks/
    incident-response-runbook.md
    stripe-webhook-failures.md
  backlog/
    roadmap-and-release-map.md
    ticket-traceability.md
  security/
    security-and-data-classification.md

C) Generated Doc Skeletons
- docs/overview/system-overview.md
  - Includes purpose, audiences, glossary, and a "What changed recently" section tied to releases.
- docs/architecture/system-design-document.md
  - Includes data flows, failure modes, scaling, observability requirements.

D) Traceability Matrix
| Requirement/Epic | Tickets | ADRs | Releases | Docs |
|---|---|---|---|---|
| Subscription lifecycle v1 | SUB-101 | adr-0002 | v0.10.0 (planned) | system-design-document.md, user-guide.md |
| Webhook authenticity | SUB-118 | adr-0002 | v0.10.0 (planned) | security-and-data-classification.md, runbooks/stripe-webhook-failures.md |

E) Maintenance Plan
- Every PR: update ADR index if decision made; update traceability if new requirement/ticket.
- Every release: update roadmap-and-release-map.md and system overview "What changed".
```

## Tips

- If you have ticket links (URLs), include them; the traceability output becomes dramatically more useful.
- If you can’t paste full ticket exports, paste the top 20 current epics + the last 2 releases; that’s enough to produce a high-leverage doc skeleton.
- Add a small “Docs DoD” checklist to your PR template (e.g., "Updated ADR? Updated runbook? Updated release map?").
- If you operate a production service, prioritize `/docs/runbooks/` and `/docs/security/` first—those pay dividends during incidents.

## Related Prompts

- `prompts/developers/documentation-generator.md` — Generates specific docs using Diataxis (useful for filling out individual skeletons)
- `prompts/governance/security-incident-response.md` — Deeper incident response content
- `prompts/developers/devops-pipeline-architect.md` — For CI/CD automation hooks mentioned in the maintenance plan
