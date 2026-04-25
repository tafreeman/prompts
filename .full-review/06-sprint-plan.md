# Sprint Plan — Review Remediation

**Source:** Findings from `.full-review/05-final-report.md` (Phases 1-4).
**Context:** local-only team-learning platform; not production deployed.

---

## Estimation Scheme

Each ticket carries three independent measurements plus a derived ratio:

| Dimension | Scale | Meaning |
|---|---|---|
| **Points** | Fibonacci: 1, 2, 3, 5, 8, 13 | Relative effort — complexity × volume × uncertainty |
| **Value** | 1-10 | Business/learner impact. 10 = closes a Critical finding; 7-8 = closes High; 5-6 = quality-of-life; ≤4 = polish |
| **T-shirt** | XS, S, M, L, XL, XXL | Second effort lens for quick eyeballing (XS≈1pt, S≈2pt, M≈3pt, L≈5pt, XL≈8pt, XXL≈13pt) |
| **V/E** | Value ÷ Points | Derived. ≥2.0 = high-leverage, prioritize. 1.0-2.0 = normal. <1.0 = important-but-expensive, schedule carefully |

### Assumptions (CHANGE WHEN YOU HAVE REAL TEAM NUMBERS)

- **Sprint length:** 2 weeks.
- **Velocity:** ~25 pts/sprint assumed. Commit to ~20 pts (80% capacity, 5 pt buffer for interrupts).
- Adjust once you have a team velocity from sprint 1 retro.

### Definition of Done (all sprints)

- [ ] Code reviewed + merged to `main` · tests added/updated · `pre-commit` green · CI green · `CHANGELOG [Unreleased]` entry · relevant docs synced

---

## Sprint 1 — Tool Safety & Silent Failures

**Sprint Goal:** Close the agent-driven attack surface on the developer's own machine.

### Backlog (sorted by V/E — land top items first)

| # | Item | Points | Value | T-shirt | V/E | Phase ref |
|---|---|---|---|---|---|---|
| 1 | Sanitization middleware fail-closed + exploding-detector test | 2 | 9 | S | **4.50** | Sec C2, Test C1 |
| 2 | `file_ops` fail-closed when `AGENTIC_FILE_BASE_DIR` unset + regression test | 2 | 8 | S | **4.00** | Sec H3, Test H2 |
| 3 | `run_id` Pydantic regex `^[a-zA-Z0-9_-]{1,64}$` + traversal test | 2 | 6 | S | **3.00** | Sec M5, Test H5 |
| 4 | Audit `expressions.py:_validate_ast`; add `__class__`/`__mro__`/`__subclasses__` negative corpus | 3 | 8 | M | **2.67** | Sec H4, Test C3 |
| 5 | Replace `ShellTool` blocklist with env-driven argv-allowlist + bypass corpus test | 5 | 10 | L | **2.00** | Sec C1, Test C2 |
| 6 | Harden `code_execution.py`: remove `__import__`/`getattr`/`setattr`; sparse env; `resource.setrlimit` | 8 | 10 | XL | **1.25** | Sec H5, H6, Test H4 |
| **Stretch** | Subprocess env sparse-scope across *all* tools incl. MCP runtime | 3 | 6 | M | **2.00** | Sec L3 |

**Committed:** 22 pts (6 tickets) · **Stretch:** +3 pts · **Total planned:** 25 pts (100% of 25-pt velocity — tight but the P0s are non-negotiable).

**High-leverage quick wins to ship first:** #1, #2, #3 — all ≥3.0 V/E, all S-size.

### Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Shell allowlist too narrow breaks existing workflows | Blocks unrelated work | Land behind env flag; run full workflow YAMLs in CI before flipping default |
| `code_execution` sandbox tightening breaks legitimate agent demos | Teaching demos fail | Snapshot which demos use code-exec; adapt those first |

---

## Sprint 2 — Concurrency Correctness & Error Hygiene

**Sprint Goal:** Eliminate shared-state races, kill the thread-pool-in-event-loop, and stop swallowing exceptions.

### Backlog (sorted by V/E)

| # | Item | Points | Value | T-shirt | V/E | Phase ref |
|---|---|---|---|---|---|---|
| 1 | `StepExecutor`: compute `effective_timeout` locally; stop mutating `step_def` | 2 | 8 | S | **4.00** | Perf C2, Quality M13 |
| 2 | `asyncio.Lock` on `LangChainEngine.runner` lazy init | 2 | 7 | S | **3.50** | Perf H5, Arch M9 |
| 3 | Reparent bypass exceptions (dag.py, runtime.py, mcp/protocol/client.py) to `AgenticError`; regression test | 2 | 6 | S | **3.00** | Arch H3 |
| 4 | `WorkflowExecutor`: pass `engine_kwargs` through call stack; remove `self._engine_kwargs` singleton write | 3 | 8 | M | **2.67** | Perf H4, Quality M14 |
| 5 | Make `SupportsCheckpointing.get_checkpoint_state` async; delete `NativeEngine` thread-pool workaround | 3 | 8 | M | **2.67** | Perf C1, Arch H6 |
| 6 | Extract `classify_llm_error()` frozen dataclass; delete 3 duplicates | 3 | 7 | M | **2.33** | Quality C2 |
| 7 | Sweep 17+ `except: pass` → `logger.debug(..., exc_info=True)` + narrowed types | 5 | 7 | L | **1.40** | Quality C1 |
| 8 | Add `tests/slo/test_concurrent_runs.py` — 20 parallel runs, distinct timeouts, no crosstalk | 5 | 7 | L | **1.40** | Test C4 |
| **Stretch** | `LLMClientWrapper.complete()` → delegate to `router.call_with_fallback` (125 → ~30 lines) | 5 | 7 | L | **1.40** | Perf H1, Quality H3 |

**Committed:** 25 pts (8 tickets) · **Stretch:** +5 pts (likely drop if Sprint 1 slipped).

**High-leverage quick wins:** #1, #2, #3 — three S-size tickets clear critical races and the exception hierarchy gap in under 6 pts combined.

### Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Async checkpoint refactor touches `SupportsCheckpointing` protocol | Langchain engine path regression | ADR-013 sunsets langchain — verify still boots but don't extend |
| Concurrent-run test flakes | False failures | Pin seeds; scale 5 → 20 once stable |

---

## Sprint 3 — Architecture Cleanup

**Sprint Goal:** Fix inverted dep direction, `get_registry` collision, and the server's langchain coupling — unblocks ADR-013 deletion.

### Backlog (sorted by V/E)

| # | Item | Points | Value | T-shirt | V/E | Phase ref |
|---|---|---|---|---|---|---|
| 1 | Rename `get_registry()` → `get_adapter_registry()` / `get_tool_registry()`; remove top-level alias | 2 | 8 | S | **4.00** | Arch C2 |
| 2 | Collapse three `Severity` enums into `contracts/severity.py` superset | 2 | 5 | S | **2.50** | Arch H4 |
| 3 | Move `ExecutionContext`/`ServiceContainer`/`EventType`/`DAG` out of `engine/` into `core/` or `contracts/` | 3 | 8 | M | **2.67** | Arch C1 |
| 4 | Extract workflow-config loaders from `..langchain` into neutral `workflows/config.py` | 3 | 8 | M | **2.67** | Arch H1 |
| 5 | Split `graph_wiring.py` (806 → 3 files: nodes/edges/parsing) | 3 | 6 | M | **2.00** | Quality H1 |
| 6 | Unify engine dispatch in `server/execution.py` via `SupportsStreaming.stream()` | 5 | 7 | L | **1.40** | Arch H2 |
| 7 | Split `smart_router.py` (536 → router + cooldown + bulkhead + persistence) | 5 | 6 | L | **1.20** | Arch M3, Quality H6 |
| 8 | Split `server/evaluation_scoring.py` (762 → scorer classes) | 5 | 6 | L | **1.20** | Quality H8 |

**Committed:** 28 pts — over budget. Trim #8 to Sprint 4 (or stretch). Committed becomes 23 pts.

**High-leverage quick wins:** #1 and #2 — both S-size, both ≥2.5 V/E; land Monday of sprint.

### Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Core/engine move breaks imports repo-wide | CI red | Single atomic commit + full matrix run before merge |
| `get_registry` rename breaks external consumers | Unknown | `warnings.warn` shim for one release; grep all docs |

---

## Sprint 4 — Performance Hot Paths

**Sprint Goal:** Keep vector/BM25 search and UI responsive for a team of 5-10 devs running workflows concurrently.

### Backlog (sorted by V/E)

| # | Item | Points | Value | T-shirt | V/E | Phase ref |
|---|---|---|---|---|---|---|
| 1 | `useRuns`: `refetchIntervalInBackground: false`; invalidate on WS workflow_end | 1 | 5 | XS | **5.00** | Perf H9 |
| 2 | `_load_eval_config` + `list_local_datasets()` — `lru_cache` by path+mtime | 2 | 6 | S | **3.00** | Perf M3/M4 |
| 3 | SQLite checkpoint: WAL + `busy_timeout=5000` + `workflow_name` index | 2 | 6 | S | **3.00** | Perf M1/M2 |
| 4 | `event_buffers` reaper in `finally:`; `asyncio.gather` concurrent WS broadcast | 2 | 6 | S | **3.00** | Perf M7/M8 |
| 5 | UI `React.lazy` for `@xyflow/react` + `manualChunks` | 2 | 4 | S | **2.00** | Perf L5 |
| 6 | `InMemoryVectorStore` → numpy matrix + `argpartition` (50-200× speedup) | 3 | 8 | M | **2.67** | Perf H2 |
| 7 | BM25 → inverted posting lists (or adopt `rank_bm25`) | 3 | 7 | M | **2.33** | Perf H3 |
| 8 | Create `tests/slo/test_latency_budgets.py` with p95 gates for cosine/BM25/assembly | 3 | 6 | M | **2.00** | Test H6 |
| 9 | UI `RunConfigForm` split + `AbortController` + `useQuery` + `useReducer` | 5 | 7 | L | **1.40** | Perf H8, Quality M10, Framework M5 |

**Committed:** 23 pts (9 tickets).

**High-leverage quick wins:** #1 is the best V/E in the entire plan (5.00) — ship in an hour. Items 2-4 are all S-size ≥3.0 V/E; batch them into one PR day.

### Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Numpy RAG refactor changes search results | Golden tests drift | Allow tolerance on float comparisons; snapshot new scores |
| UI `useReducer` rewrite regresses UX | Form breaks | Keep 680-line version on branch until Vitest + manual QA pass |

---

## Sprint 5 — DevEx, CI, and Docs Drift

**Sprint Goal:** Restore CI gates, make pre-commit match the docs, kill doc drift so learners aren't misled.

### Backlog (sorted by V/E)

| # | Item | Points | Value | T-shirt | V/E | Phase ref |
|---|---|---|---|---|---|---|
| 1 | Pin GitHub Actions to real major tags (v4/v5) — kill phantom v6/v7/v8 | 1 | 6 | XS | **6.00** | DevEx H1, Sec M3 |
| 2 | Fix `AGENTIC_NO_LLM=1` doc contradiction; reconcile TS codegen doc vs CONTRIBUTING | 1 | 5 | XS | **5.00** | Docs D4, D8 |
| 3 | `.nvmrc` + `.python-version` single source; unify Node across CI | 1 | 4 | XS | **4.00** | DevEx M6, M7 |
| 4 | `CHANGELOG.md`: version-diff links + `[Unreleased]` dating discipline | 1 | 4 | XS | **4.00** | Docs D6 |
| 5 | Re-enable 9 disabled CI workflows; add `concurrency:` groups | 2 | 8 | S | **4.00** | DevEx C1, H4 |
| 6 | Pre-commit: re-enable mypy scoped to `core/` + `contracts/`; ratchet plan | 2 | 7 | S | **3.50** | DevEx H3, Framework H1 |
| 7 | Adopt `astral-sh/setup-uv@v5 + uv sync --frozen` in all Python CI steps | 2 | 6 | S | **3.00** | DevEx H6 |
| 8 | Generate `docs/CLI_REFERENCE.md` from `typer --help`; fix `create_app --factory` vs `:app` | 2 | 5 | S | **2.50** | Docs D7 |
| 9 | ADR hygiene: split combined 001-002-003; index count fix; reclassify Proposed-with-implementation | 2 | 5 | S | **2.50** | Docs D5 |
| 10 | Add `CODEOWNERS`; add UI ESLint + CI lint job | 2 | 4 | S | **2.00** | DevEx M11, M3, Framework L1 |
| 11 | Ratchet ruff: enable `RUF006`, `S307`, `B904`, `F841`, `B017`; fix violations | 3 | 6 | M | **2.00** | DevEx H2 |
| 12 | `justfile` portable (PowerShell + bash via `os()` or companion `dev.sh`) | 3 | 5 | M | **1.67** | DevEx H7 |
| 13 | Add `docs/LEARNING_PATH.md` ordering for educational audience | 2 | 4 | S | **2.00** | Docs D19 |

**Committed:** 24 pts (13 tickets — all small).

**High-leverage quick wins:** #1 wins the plan (6.00 V/E — 1pt, closes DevEx H1 + Sec M3); #2 and #3 close two High docs drift items in 1 pt each. Land items 1-4 on day 1 (4 pts, 4 Highs closed).

### Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Re-enabling CI surfaces accumulated red | Sprint stalls | Use `act` locally before flipping trigger |
| Mypy re-enable finds a mountain of findings | Scope creep | Scope to 2 directories only; rest to backlog |

---

## Cross-Sprint: Highest V/E Tickets

Across all 5 sprints the top 10 by value-per-point — if capacity drops, protect these first:

| Rank | Sprint | Item | Points | Value | V/E |
|---|---|---|---|---|---|
| 1 | S5 | Pin GH Actions to real tags | 1 | 6 | **6.00** |
| 2 | S4 | `useRuns` background polling off | 1 | 5 | **5.00** |
| 3 | S5 | Fix `AGENTIC_NO_LLM=1` doc contradiction | 1 | 5 | **5.00** |
| 4 | S1 | Sanitization fail-closed + test | 2 | 9 | **4.50** |
| 5 | S1 | `file_ops` fail-closed | 2 | 8 | **4.00** |
| 6 | S2 | Stop mutating `step_def.timeout_seconds` | 2 | 8 | **4.00** |
| 7 | S3 | Rename `get_registry()` duplicates | 2 | 8 | **4.00** |
| 8 | S5 | `.nvmrc` + `.python-version` unification | 1 | 4 | **4.00** |
| 9 | S5 | CHANGELOG version-diff links | 1 | 4 | **4.00** |
| 10 | S5 | Re-enable 9 disabled CI workflows | 2 | 8 | **4.00** |

**Quick-win PR day:** pick a slow afternoon, land all XS-size (1 pt) items in Sprints 4-5 — ~6 pts of work closes 5 findings across 3 sprints.

## Cross-Sprint: Highest-Value Work (regardless of effort)

Value=10 tickets are all Critical security fixes; Value=9 are high-impact correctness. Order by sprint:

- **S1:** ShellTool allowlist (10), code_execution harden (10), sanitization fail-closed (9)
- **S2:** none rated 9-10 (concurrency is V7-8)
- **S3:** none rated 9-10
- **S4:** InMemoryVectorStore numpy (8)
- **S5:** Re-enable CI workflows (8)

This confirms the sprint ordering: highest-value work lives in Sprints 1-2; Sprints 3-5 are architecture + perf + polish, with small high-V/E cleanup scattered throughout.

---

## Key Dates (tentative)

| Date | Event |
|---|---|
| 2026-04-27 | Sprint 1 start |
| 2026-05-08 | Sprint 1 demo / retro (establish actual velocity) |
| 2026-05-11 | Sprint 2 start |
| 2026-05-22 | Sprint 2 end |
| ... | 2-week cadence |
| 2026-07-03 | Sprint 5 demo — target: all Critical + most High findings closed |

## Re-planning Notes

1. **After Sprint 1, recompute velocity.** If the team completed 18 pts, drop the 25-pt assumption to 20 and rebalance Sprints 2-5.
2. **Treat V/E as a tiebreaker, not an oracle.** A 1-pt item with V=4 beats a 5-pt item with V=5 on ratio, but if the 5-pt item unblocks three downstream tickets, land it first.
3. **P0 safety work (Sprint 1) is non-negotiable** — do not trade safety tickets for higher-V/E cleanup.
