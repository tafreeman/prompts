# Product Backlog — tafreeman/prompts

**Repository:** `tafreeman/prompts`
**Last Updated:** 2026-03-05
**Health Score:** 7.9 / 10 *(post-remediation, 2026-03-03)*
**Analysis Team:** Architecture Analyst · ML/AI Patterns Reviewer · Code Quality Auditor · Documentation & DX Reviewer

**Source documents:**
| File | Summary |
|------|---------|
| [`analysis/architecture-review.md`](architecture-review.md) | A- — Protocol-first adapter registry, dual engine, DAG superiority over Microsoft candidates; ctx forwarding bug in LangChainEngine, no checkpointing implementation |
| [`analysis/ml-ai-patterns-review.md`](ml-ai-patterns-review.md) | A- — 24 personas fully structured post-remediation; CoT, Boundaries, Output Format, domain-specific Reasoning Protocols; gap is zero-shot only (no few-shot, no reflection loops) |
| [`analysis/code-quality-report.md`](code-quality-report.md) | B+ — Strong agentic_v2 quality; ruff.lint not configured (E+F only), CI coverage gate 60% vs 80% target, tools/ package needs modernization |
| [`analysis/documentation-review.md`](documentation-review.md) | B+ — Excellent CLAUDE.md and README; 11 broken cross-references, no onboarding tutorial, minimal examples |
| [`analysis/ANALYSIS-SUMMARY.md`](ANALYSIS-SUMMARY.md) | Synthesized findings — 25 prioritized recommendations, 4-sprint roadmap, 7.9/10 health score |

---

## Health Score Dashboard

| Dimension | Score | Rationale |
|-----------|:-----:|-----------|
| **Modularity & separation** | 9/10 | Zero cross-package imports; clean adapter pattern; excellent RAG module boundaries |
| **Protocol design** | 8/10 | PEP 544 protocols with `@runtime_checkable`; deducted for `Any` in core signatures |
| **Config-driven design** | 9/10 | 81% config for workflows; all 24 personas fully structured (Expertise, Reasoning Protocol, Output Format, Boundaries, Critical Rules); comprehensive YAML DSL |
| **ML/AI pattern sophistication** | 9/10 | ToT, ReAct, CoVe, RRF hybrid retrieval, circuit breakers, CoT scaffolding in all personas, RAG prompt injection framing; deducted for no few-shot/reflection |
| **Code quality discipline** | 7/10 | Strong in agentic_v2 (no bare except, good typing, logging); tools/ package drags the score |
| **Test coverage & strategy** | 7/10 | 1305+ tests, ~92% RAG coverage; CI threshold mismatch and missing markers hurt |
| **Documentation completeness** | 7/10 | Excellent CLAUDE.md and README; broken cross-refs, no onboarding tutorial, minimal examples |
| **Production readiness** | 7/10 | Good observability, auth, security; in-memory stores limit production scalability |
| **Extensibility** | 9/10 | New workflow/persona/loader/adapter via protocol implementation only; entry_points gap |
| **Educational clarity** | 7/10 | Self-documenting architecture; lacks explicit learning path and pattern catalog |

**Overall: 79/100 → 7.9/10**

---

## Key Strengths

| # | Strength | Evidence |
|---|----------|----------|
| 1 | **Protocol-first architecture** | 9 `@runtime_checkable` Protocol classes in `core/protocols.py` + `rag/protocols.py` enable structural subtyping and clean engine swapping |
| 2 | **Production-grade LLM routing** | `SmartModelRouter` implements circuit breakers, adaptive cooldowns, per-provider bulkheads, rate-limit header parsing, and cross-tier degradation |
| 3 | **Comprehensive RAG pipeline** | 13 protocol-backed modules: load → chunk → embed → index → hybrid retrieve (BM25 + dense + RRF) → token-budget assemble → trace |
| 4 | **Advanced deep-research workflow** | `deep_research.yaml` demonstrates ToT, ReAct, CoVe, and confidence-gated iteration in declarative YAML — rare in the field |
| 5 | **Antagonist review personas** | Two orthogonal antagonist personas (FMEA murder-board + systemic pre-mortem) embody adversarial review methodology at the prompt level |

---

## Full Backlog (All 25 Items + 1 New)

| # | ID | Status | Sprint | Recommendation | Impact | Effort | Owner | Source |
|---|----|--------|--------|----------------|:------:|:------:|-------|--------|
| 1 | CQ-1 | **DONE** ✅ | — | ~~Add `[tool.ruff.lint]` with full rule set~~ — `pyproject.toml:98` has all 13 rules (2026-03-05) | 5 | S | Code Quality | CQ-1 |
| 2 | CQ-2 | **DONE** ✅ | — | ~~Align CI coverage threshold~~ — `ci.yml:31` at 70% with 80% target comment (2026-03-05) | 4 | S | Code Quality | CQ-2 |
| 3 | ML-1 | **DONE** ✅ | — | ~~Add few-shot examples~~ — 8 personas have `## Few-Shot Examples` sections (2026-03-05) | 5 | M | ML/AI | ML-1 |
| 4 | DX-1 | BACKLOG | Sprint B | Create `docs/ONBOARDING.md` — progressive tutorial: minimum setup → first workflow → first agent → first evaluation | 5 | M | Docs | DX-1 |
| 5 | DX-3 | BACKLOG | Sprint B | Create a Pattern Catalog mapping agentic AI patterns (ReAct, CoVe, ToT, RRF, confidence gating) to their codebase implementations | 5 | M | Docs | DX-3 |
| 6 | ML-2 | BACKLOG | Sprint D | Implement reflection/self-correction loop in `BaseAgent` — add `_self_critique()` + `_revise()` phase after initial response | 5 | L | ML/AI | ML-2 |
| 7 | ARCH-4 | BACKLOG | Sprint C | Add cross-package integration tests — E2E tests exercising tools/ LLM client → agentic_v2 engine → agentic-v2-eval scoring | 4 | M | Architecture | ARCH-4 |
| 8 | ARCH-1 | BACKLOG | Sprint C | Tighten protocol type signatures — replace `Any` in `ExecutionEngine.execute()` and `AgentProtocol.run()` with Union type aliases | 4 | M | Architecture | ARCH-1 |
| 9 | ARCH-2 | **DONE** ✅ | — | ~~Bridge ExecutionContext to LangChainEngine~~ — async paths (run, astream) forward ctx (2026-03-05) | 4 | M | Architecture | ARCH-2 |
| 10 | DX-2 | **DONE** ✅ | — | ~~Verify cross-references~~ — `check_docs_refs.py` passes locally and in CI (2026-03-05) | 4 | S | Docs | DX-2 |
| 11 | DX-4 | BACKLOG | Sprint B | Add 5-8 examples — cover RAG pipeline, custom agent with tools, new YAML workflow creation, model router, adapter switching | 5 | M | Docs | DX-4 |
| 12 | CQ-3 | **DONE** ✅ | — | ~~Add `[tool.mypy]`~~ — `pyproject.toml:213` with `disallow_untyped_defs = true` (2026-03-05) | 4 | M | Code Quality | CQ-3 |
| 13 | CQ-7 | **DONE** ✅ | — | ~~Add CI job for tools/ test suite~~ — `.github/workflows/tools-ci.yml` created (2026-03-05) | 4 | S | Code Quality | CQ-7 |
| 14 | ARCH-6 | **DONE** ✅ | — | ~~LanceDB VectorStore~~ — `rag/vectorstore.py:LanceDBVectorStore`, protocol-compliant, tested (2026-03-05) | 4 | M | Architecture | ARCH-6 |
| 15 | ML-5 | BACKLOG | Sprint D | Integrate online evaluation feedback — evaluation scores feed back into agent execution loop for self-correction | 4 | L | ML/AI | ML-5 |
| 16 | CQ-4/5 | BACKLOG | Sprint C | Modernize `tools/` package — `from __future__ import annotations`, replace legacy typing, convert 365 `print()` to logging | 3 | M | Code Quality | CQ-4/5 |
| 17 | ML-3 | **DONE** ✅ | — | ~~Add chain-of-thought scaffolding to agent prompts~~ — `## Reasoning Protocol` added to all 24 personas (2026-03-03) | 4 | S | ML/AI | ML-3 |
| 18 | DX-5 | BACKLOG | Sprint B | Add YAML workflow authoring guide — document expression syntax, `when` conditions, loops, agent naming, evaluation blocks | 4 | M | Docs | DX-5 |
| 19 | ML-4 | BACKLOG | Sprint C | Add re-ranking stage to RAG pipeline — cross-encoder or LLM re-ranker after RRF fusion | 4 | M | ML/AI | ML-4 |
| 20 | ARCH-3 | BACKLOG | Sprint D | Add workflow `iterate:` construct — YAML looping directive to eliminate `deep_research.yaml` 4x duplication | 3 | M | Architecture | ARCH-3 |
| 21 | ML-6 | **DONE** ✅ | — | ~~Enrich lower-tier personas (B-rated)~~ — all 24 now have Boundaries, Output Format, and Reasoning Protocol (2026-03-03) | 4 | M | ML/AI | ML-6 |
| 22 | DX-6 | **DONE** ✅ | — | ~~Create GitHub templates~~ — PR template + bug/feature issue templates created (2026-03-05) | 3 | S | Docs | DX-6 |
| 23 | DX-9 | **DONE** ✅ | — | ~~Add concept glossary~~ — `docs/GLOSSARY.md` with ~28 terms (2026-03-05) | 4 | S | Docs | DX-9 |
| 24 | CQ-6 | BACKLOG | Sprint D | Split oversized files — `model_probe.py` (2,360 lines), `server/routes/workflows.py` (1,330), `evaluation_scoring.py` (1,160) | 3 | L | Code Quality | CQ-6 |
| 25 | DX-13 | BACKLOG | Sprint D | Add annotated code walkthroughs — guided walkthroughs of workflow execution, model routing, RAG retrieval | 4 | L | Docs | DX-13 |
| 26 | ARCH-5 | **DONE** ✅ | — | ~~SupportsCheckpointing in NativeEngine~~ — SQLite CheckpointStore, full test suite (2026-03-05) | 4 | M | Architecture | ARCH-5 |

---

## Microsoft Agent Framework Decision (ADR-012 Summary)

**Decision: DEFERRED** — Not high value relative to existing capabilities as of 2026-03-04.

### Candidates Evaluated

| Candidate | Status | DAG Alignment | Decision |
|-----------|--------|:-------------:|----------|
| Microsoft AutoGen v0.4 | Maintenance mode (Oct 2025) | 60% | **REJECTED** — maintenance mode |
| Semantic Kernel | Maintenance mode (Oct 2025) | 40% | **REJECTED** — maintenance mode + poor alignment |
| Azure AI Agent Service | Active (cloud-only) | N/A | **REJECTED** — not an adapter candidate; cloud service, not a library |
| Microsoft Agent Framework (MAF) | Public preview | 70% | **DEFERRED** — viable when GA, but inferior parallelism vs local DAG |

### Why the Local DAG Wins

The repo's native DAG executor uses Kahn's algorithm with `asyncio.wait(FIRST_COMPLETED)` — steps unblock immediately when their dependencies resolve. MAF uses superstep barriers (all dependencies must finish before any successor starts), which is fundamentally inferior parallelism. Implementing a MAF adapter would add a vendor dependency while delivering worse execution characteristics.

### Trigger Conditions for Revisit

Revisit ADR-012 when **all three** conditions are met:

1. **MAF reaches GA** (currently public preview — API stability not guaranteed)
2. **Engagement-specific Purview requirement** — client requires Microsoft Purview audit trail for agentic workflow provenance
3. **`SupportsCheckpointing` implemented** in `NativeEngine` (ARCH-5, Item #26) — MAF's only genuine capability advantage is eliminated once SQLite checkpointing is in place

**Full research document:** To be created as `analysis/microsoft-agent-framework-research.md`

---

## Completed Items

| ID | Item | Completion Date | Notes |
|----|------|-----------------|-------|
| ML-3 | Chain-of-thought scaffolding added to all 24 agent personas (`## Reasoning Protocol`) | 2026-03-03 | Domain-specific 5-step reasoning workflows replacing generic boilerplate |
| ML-6 | Lower-tier personas enriched — all 24 now have Boundaries, Output Format, Reasoning Protocol | 2026-03-03 | Post-remediation: all personas rated A- or higher (3 A+, 3 A, 17 A-, 1 B+) |
| CQ-1 | Ruff lint config — full 13-rule set in `pyproject.toml:98` | 2026-03-05 | Rules: E, F, W, I, N, UP, S, B, A, C4, SIM, TCH, RUF |
| CQ-2 | CI coverage threshold aligned to 70% (`ci.yml:31`) | 2026-03-05 | `--cov-fail-under=70` with 80% target documented |
| CQ-3 | Mypy config in `pyproject.toml:213` | 2026-03-05 | `disallow_untyped_defs = true`, `warn_return_any = true` |
| ML-1 | Few-shot examples added to 8 personas | 2026-03-05 | coder, reviewer, orchestrator, researcher, architect, tester, both antagonists |
| ARCH-2 | LangChainEngine ctx forwarding (async paths) | 2026-03-05 | `run()` and `astream()` merge ctx vars into LangGraph state |
| ARCH-5 | SupportsCheckpointing — SQLite CheckpointStore + NativeEngine | 2026-03-05 | Write/read/resume/clear, async I/O via to_thread, full test suite |
| ARCH-6 | LanceDB VectorStore adapter in `rag/vectorstore.py` | 2026-03-05 | Protocol-compliant, content-hash dedup, cosine distance, tested |
| DX-2 | Cross-references verified — `check_docs_refs.py` passes | 2026-03-05 | CI script already in place; confirmed locally |
| CQ-7 | tools/ CI workflow — `.github/workflows/tools-ci.yml` | 2026-03-05 | Python 3.10/3.11/3.12 matrix, path-filtered, lint + test jobs |
| DX-6 | GitHub PR/issue templates | 2026-03-05 | PR template, bug report, feature request, template chooser |
| DX-9 | Concept glossary — `docs/GLOSSARY.md` | 2026-03-05 | ~28 terms across architecture, AI/ML patterns, development |

---

## Sprint Roadmap

### Sprint A — Quick Wins ✅ COMPLETE

All 11 items completed (7 discovered done + 4 implemented 2026-03-05).

| # | ID | Item | Status |
|---|----|------|--------|
| 1-7 | CQ-1/2/3, ML-1, ARCH-2/5/6 | Previously implemented | **DONE** ✅ |
| 8 | DX-2 | Cross-references verified | **DONE** ✅ |
| 9 | CQ-7 | tools/ CI workflow created | **DONE** ✅ |
| 10 | DX-6 | GitHub PR/issue templates created | **DONE** ✅ |
| 11 | DX-9 | Concept glossary created | **DONE** ✅ |

### Sprint B — Educational Materials (~1-2 weeks)

| # | ID | Item |
|---|----|------|
| 12 | DX-1 | Create `docs/ONBOARDING.md` progressive tutorial |
| 13 | DX-3 | Create Pattern Catalog |
| 14 | DX-4 | Add 5-8 code examples |
| 15 | DX-5 | Add YAML workflow authoring guide |

### Sprint C — Architecture Hardening (~2-3 weeks)

| # | ID | Item |
|---|----|------|
| 16 | ARCH-1 | Tighten protocol type signatures (bounded TypeVars) |
| 17 | ARCH-4 | Add cross-package integration tests |
| 18 | ML-4 | Add re-ranking stage to RAG pipeline |
| 19 | CQ-4/5 | Modernize tools/ package |

### Sprint D — Advanced Patterns (~4+ weeks)

| # | ID | Item |
|---|----|------|
| 20 | ML-2 | Implement BaseAgent reflection/self-correction loop |
| 21 | ML-5 | Integrate online evaluation feedback loop |
| 22 | ARCH-3 | Add workflow `iterate:` construct |
| 23 | CQ-6 | Split oversized files |
| 24 | DX-13 | Add annotated code walkthroughs |

---

## Current Implementation Plan

**Plan file:** `C:\Users\tandf\.claude\plans\adaptive-crafting-fountain.md`

**Phase 0:** Update BACKLOG.md with 7 completed items ✅
**Sprint A (parallel):** DX-2 verify refs + CQ-7 tools CI + DX-6 templates + DX-9 glossary
**Sprint B (parallel):** DX-1 onboarding + DX-3 pattern catalog + DX-4 examples + DX-5 YAML guide
**Sprint C:** ARCH-1 type tightening ∥ ML-4 re-ranking ∥ CQ-4/5 tools modernization → ARCH-4 integration tests
