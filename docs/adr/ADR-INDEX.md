# ADR Index — agentic-workflows-v2

> **Last updated:** 2026-03-15
> **Total ADRs:** 9 (3 Accepted, 5 Proposed, 1 Superseded)
> **Replaces:** `ADR_COMPILED.md` (deprecated — was missing ADRs 009-012)

---

## Quick-Access Deck

| ADR | Title | Status | File |
|-----|-------|--------|------|
| **001** | Dual Execution Engine (LangGraph vs. Kahn's DAG) | Accepted | [ADR-001-002-003](ADR-001-002-003-architecture-decisions.md) |
| **002** | SmartModelRouter Circuit-Breaker Hardening | Accepted | [ADR-001-002-003](ADR-001-002-003-architecture-decisions.md) |
| **003** | Deep Research Supervisor / CI Gating | Superseded → 007 | [ADR-001-002-003](ADR-001-002-003-architecture-decisions.md) |
| **007** | Multidimensional Classification Matrix & Stop Policy | Proposed | [ADR-007](ADR-007-classification-matrix-stop-policy.md) |
| **008** | Testing Approach Overhaul (Value Taxonomy) | Proposed | [ADR-008](ADR-008-testing-approach-overhaul.md) |
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
| 001 | Yes | ~40% | Protocol tests | 2026-02-28 |
| 002 | Yes | ~100% | 67 tests | 2026-02-28 |
| 003 | Superseded | N/A | N/A | — |
| 007 | Yes | ~50% | Partial | 2026-02-28 |
| 008 | Yes | Phase 0 done | N/A (meta) | 2026-03-09 |
| 009 | Yes | 100% | 28 tests | 2026-03-03 |
| 010 | Proposed | 0% | — | — |
| 011 | Proposed | 0% | — | — |
| 012 | Proposed | 0% | — | — |

---

## Supporting Documents

| Document | Description |
|----------|-------------|
| [ADR_COMPILED.md](ADR_COMPILED.md) | **Deprecated** — full-text compilation of ADRs 001-008 (stale, missing 009-012) |
| [ADR_IMPLEMENTATION_AUDIT.md](ADR_IMPLEMENTATION_AUDIT.md) | Implementation audit against codebase (2026-02-28) |
| [ADR_RESEARCH_JUSTIFICATIONS.md](ADR_RESEARCH_JUSTIFICATIONS.md) | Research citations and justifications |
| [RAG-pipeline-blueprint.md](RAG-pipeline-blueprint.md) | RAG architecture blueprint |
