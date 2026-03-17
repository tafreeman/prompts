# ADR Index — agentic-workflows-v2

> **Last updated:** 2026-03-17
> **Total ADRs:** 9 (4 Accepted, 4 Proposed, 1 Superseded)
> **Replaces:** `ADR_COMPILED.md` (deprecated — was missing ADRs 009-012)

---

## Quick-Access Deck

| ADR | Title | Status | File |
|-----|-------|--------|------|
| **001** | Dual Execution Engine (LangGraph vs. Kahn's DAG) | Accepted | [ADR-001-002-003](ADR-001-002-003-architecture-decisions.md) |
| **002** | SmartModelRouter Circuit-Breaker Hardening | Accepted | [ADR-001-002-003](ADR-001-002-003-architecture-decisions.md) |
| **003** | Deep Research Supervisor / CI Gating | Superseded → 007 | [ADR-001-002-003](ADR-001-002-003-architecture-decisions.md) |
| **007** | Multidimensional Classification Matrix & Stop Policy | Proposed | [ADR-007](ADR-007-classification-matrix-stop-policy.md) |
| **008** | Testing Approach Overhaul (Value Taxonomy) | Accepted | [ADR-008](ADR-008-testing-approach-overhaul.md) |
| **009** | Scoring Enhancements (Exponential Decay, Lexicographic) | Accepted | [ADR-009](ADR-009-scoring-enhancements.md) |
| **010** | Commit-Driven A/B Eval Harness Methodology | Proposed | [ADR-010](ADR-010-eval-harness-methodology.md) |
| **011** | Eval Harness API & Interface Design | Proposed | [ADR-011](ADR-011-eval-harness-api-interface.md) |
| **012** | UI Evaluation Hub & A/B Comparison | Proposed | [ADR-012](ADR-012-ui-evaluation-hub.md) |

**Note:** ADRs 004-006 were never created. The numbering gap is intentional.

---

## Lineage Chains

```
Engine Domain:
  ADR-001 (Dual Engine) ─── standalone

Models Domain:
  ADR-002 (Circuit Breaker) ─── standalone

Research Domain:
  ADR-003 (CI Gating) ──superseded-by──> ADR-007 (Classification Matrix)
                                              └──extended-by──> ADR-009 (Scoring Enhancements)

Testing Domain:
  ADR-008 (Test Value Taxonomy) ─── standalone

Evaluation Domain:
  ADR-010 (Harness Methodology) ──extended-by──> ADR-011 (API Interface)
                                                      └──extended-by──> ADR-012 (UI Hub)
```

---

## Implementation Status

| ADR | Decision | Implemented | Tests | Last Audit |
|-----|:---:|:---:|:---:|---|
| 001 | Yes | ~65% | Protocol + adapter tests | 2026-03-17 |
| 002 | Yes | ~80% | Extensive router/rate-limit tests | 2026-03-17 |
| 003 | Superseded | Legacy fragments only | Legacy scoring tests | 2026-03-17 |
| 007 | Yes | ~50% | Unit + wiring tests | 2026-03-17 |
| 008 | Yes | ~35% | Meta / partial cleanup only | 2026-03-17 |
| 009 | Yes | ~85% | CI + multidimensional scoring tests | 2026-03-17 |
| 010 | Proposed | ~10% (primitives only) | Reused primitives only | 2026-03-17 |
| 011 | Proposed | ~15% (partial eval infra) | Adjacent route/UI helpers only | 2026-03-17 |
| 012 | Proposed | ~10% (existing evaluations table only) | None specific | 2026-03-17 |

---

## Supporting Documents

| Document | Description |
|----------|-------------|
| [../audit/adr-implementation-review.md](../audit/adr-implementation-review.md) | 2026-03-17 deep review of canonical ADR accuracy, implementation status, gaps, and technical soundness |
| [ADR_COMPILED.md](ADR_COMPILED.md) | **Deprecated** — full-text compilation of ADRs 001-008 (stale, missing 009-012) |
| [ADR_IMPLEMENTATION_AUDIT.md](ADR_IMPLEMENTATION_AUDIT.md) | Implementation audit against codebase (2026-02-28) |
| [ADR_RESEARCH_JUSTIFICATIONS.md](ADR_RESEARCH_JUSTIFICATIONS.md) | Research citations and justifications |
| [RAG-pipeline-blueprint.md](RAG-pipeline-blueprint.md) | RAG architecture blueprint |
