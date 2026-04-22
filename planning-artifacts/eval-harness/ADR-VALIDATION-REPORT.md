# ADR Validation Report: Truth-Grounding Review

**Date:** 2026-03-09
**Method:** Three parallel code-explorer agents, each reading every referenced source file
**Scope:** ADR-010, ADR-011, ADR-012 (Commit-Driven A/B Evaluation Harness)

---

## Executive Summary

| ADR | Accuracy | Verified | Partial | Inaccurate | Unverifiable |
|-----|----------|----------|---------|------------|--------------|
| ADR-010 (Methodology) | ~70% | 18 claims | 6 claims | 8 claims | 5 claims |
| ADR-011 (API & Interface) | ~58% | 13 claims | 6 claims | 5 claims | 7 claims |
| ADR-012 (UI Overhaul) | ~78% | 16 claims | 5 claims | 2 claims | 5 claims |

### Convergent Findings (highest confidence — found by 2+ agents)

1. **`tools/pyproject.toml` does not exist** — ADR-010 and ADR-011 both reference it. The correct file is the root `d:\source\prompts\pyproject.toml` (package: `prompts-tools`).
2. **WebSocket backoff is linear, not exponential** — ADR-011 and ADR-012 both label `retryDelayMs * retryCount` as "exponential backoff." The formula is linear (`1s, 2s, 3s, 4s, 5s`); exponential would be `retryDelayMs * 2^retryCount`.
3. **"Zero new client code" is overstated** — ADR-011 and ADR-012 claim reusing `connectExecutionStream()` verbatim. The function hardcodes URL prefix `/ws/execution/`. A new `/ws/eval/` path requires either modifying the function or writing a new call-site. A new backend WebSocket route handler is also required.
4. **`useWorkflowStream` uses `useState`, not `useReducer`** — ADR-011 and ADR-012 describe the hook using `useReducer`. The actual hook uses five `useState` calls.
5. **`typer` already exists as a dependency** — `agentic-workflows-v2/pyproject.toml` declares `typer>=0.9,<1`. The ADRs present it as a new addition.

### Critical Issues Requiring ADR Amendments

1. **Three fabricated author attributions in ADR-010** (see Section 1, item 4.4–4.6)
2. **`Scorer` output range is 0.0–1.0, not 0–100** (ADR-010 Section 1, item 3.3)
3. **Existing SSE infrastructure not acknowledged** (ADR-011 Section 2, item 6.1)
4. **`WorkflowDetailPage` already has eval entry point** (ADR-012 Section 3, item 7.4)
5. **`bg-surface-hover` phantom token** in `EvaluationsPage.tsx` (ADR-012 Section 3, item 7.1)

---

## Section 1: ADR-010 — Methodology & Design

### Verified Claims (18)

| # | Claim | Evidence |
|---|-------|----------|
| 1 | `evaluate_with_llm()` exists at `tools/agents/benchmarks/llm_evaluator.py:372` | Function confirmed with full signature |
| 2 | Five dimensions: completeness (25%), correctness (25%), quality (20%), specificity (15%), alignment (15%) | `EVALUATION_DIMENSIONS` dict at lines 40-61 matches exactly |
| 3 | Score scale 0-10 per dimension | `SCORE_RUBRIC` spans 0.0-10.0; `EvaluationResult.overall_score` typed as float |
| 4 | `EvaluationResult` is the return type | Line 381 confirms return annotation |
| 5 | `LLMClient.generate_text()` exists at `tools/llm/llm_client.py:186` | `@staticmethod` with `model_name` as first arg, then `prompt` |
| 6 | `Scorer` class exists at `agentic-v2-eval/src/agentic_v2_eval/scorer.py:65` | Class confirmed; rubric-driven via `_parse_criteria()` |
| 7 | `coding_standards.yaml` exists | File present in `rubrics/` directory |
| 8 | 8 rubric YAML files total | agent, code, default, pattern, prompt_pattern, prompt_standard, quality, coding_standards |
| 9 | `WorkflowRunner` at `workflows/runner.py:46` | Class confirmed at stated line |
| 10 | `WorkflowRunner.run()` exists | `async def run(...)` at line 102 |
| 11 | `ClaudeAgent` at `agents/implementations/claude_agent.py:65` | Class confirmed at stated line |
| 12 | SWE-bench: ICLR 2024, arXiv:2310.06770 | Venue and arXiv ID confirmed via web search |
| 13 | SWE-bench: Jimenez, Yang, Wettig, Yao, Pei, Press, Narasimhan | All 7 authors confirmed |
| 14 | SWE-bench: 2,294 instances, 12 repos, 1.96% RAG, 4.80% oracle, 1.7 files / 3.0 functions / 32.8 lines | All statistics confirmed |
| 15 | SWE-rebench: arXiv:2505.20411, NeurIPS 2025, 450K+ PRs, 30K+ repos, 21K+ tasks | ArXiv ID, venue, and statistics confirmed |
| 16 | Aider: 26.3% on SWE-bench Lite (May 22, 2024) | Confirmed via aider.chat |
| 17 | promptfoo is a Node.js dependency | Confirmed; rejection reason accurate |
| 18 | `git worktree add`, `git checkout -f HEAD`, `git worktree remove --force` are valid commands | Standard documented git syntax |

### Partially Accurate Claims (6)

**3.1 `Scorer` output range: ADR says "0-100", actual is 0.0-1.0**

The `ScoringResult.weighted_score` is computed as `weighted_sum / total_weight` where normalized values are in `[0,1]`. No percentage multiplication exists anywhere in `scorer.py`. The ADR should say "0.0-1.0 weighted rubric score."

**3.2 `coding_standards.yaml` criteria described incompletely**

ADR says: "type hints, error handling, naming, no magic numbers, test presence." Actual criteria: Style & Formatting, Type Safety, Naming & Structure, Error Handling, Testing, Security & Privacy, ML Reproducibility, Deployment Readiness. The ADR omits 4 of 8 criteria.

**3.3 "Two-layer scoring" modules are not currently wired together**

`evaluate_with_llm()` and `Scorer` both exist independently but have never been composed into a pipeline anywhere in the codebase. The ADR presents them as an existing integrated system. The integration is new work, not reuse.

**3.4 `evaluate_with_llm()` is synchronous, not async**

The ADR's sandbox code uses `await runner.run(contestant_a, ...)`, implying async context. But `evaluate_with_llm()` is a regular `def`, not `async def`. Integration requires `asyncio.to_thread()` or similar wrapping.

**3.5 `coding_standards.yaml` uses 0-5 levels, not binary pass/fail**

Each criterion has a `levels` dict from 0 to 5. The `Scorer` normalizes via `(value - min_value) / range_size`. Callers must normalize inputs to 0-1 before calling `Scorer.score()`, or override `max_value`. The ADR does not address this impedance mismatch.

**3.6 Git worktree performance claims lack citations**

"~100ms (index checkout)" and "~30 seconds (worktree-based)" CI context switching are stated as empirical facts with no supporting benchmark citation. Plausible but unverifiable.

### Inaccurate Claims (8)

**4.1 `tools/commit_eval/` module does not exist**

All 10 files listed in the Files Changed table are absent. Expected for a Proposed ADR, but the language should clarify these are entirely new, not partially implemented.

**4.2 `tools/pyproject.toml` does not exist**

The tools package is configured by the root `d:\source\prompts\pyproject.toml` (package: `prompts-tools`). The ADR targets a non-existent file.

**4.3 `tools/__init__.py` has no `commit_eval` export**

Current file contains only `__version__` and a backwards-compatible `evaluation_agent` alias. Consistent with module not existing.

**4.4 SWE-rebench author: "Aleithan et al." is WRONG**

First author is Ibragim Badertdinov. Co-authors: Golubev, Nekrashevich, Shevtsov, Karasik, Andriushchenko, Trofimova, Litvintseva, Yangel. "Aleithan" is the first author of a *different* paper: SWE-bench+ (arXiv:2410.06992). The ADR confuses two papers with similar names.

**4.5 SWE-bench Live author: "Gauthier Guinet et al." is WRONG**

First author is Linghao Zhang (Microsoft Research). Full author list: Zhang, He, Zhang, Kang, Li, Xie, Wang, Wang, Huang, Fu, Nallipogu, Lin, Dang, Rajmohan, Zhang. "Gauthier Guinet" does not appear in the author list.

**4.6 SWE-Bench++ author: "Chen et al." is WRONG, year is wrong**

Actual authors: Wang, Ramalho, Celestino, Pham, Liu, Sinha, Portillo, Osunwa, Maduekwe. No "Chen" found. ArXiv prefix `2512` = December 2025, not "2024" as stated.

**4.7 `typer` presented as new dependency**

Already declared in `agentic-workflows-v2/pyproject.toml` as `typer>=0.9,<1`.

**4.8 Cross-package dependency omitted**

`agentic-v2-eval` is a separate installable package. `tools/commit_eval/` would need to declare it as a dependency to import `agentic_v2_eval.scorer`. The ADR's dependency table omits this.

### Unverifiable Claims (5)

| # | Claim | Status |
|---|-------|--------|
| 1 | Docker startup time "5+ seconds per published benchmarks" | No citation; plausible but unverifiable |
| 2 | Git worktree reset "microseconds" | No citation; depends on repo size |
| 3 | CI context switch "~30s (worktree) vs 10+ min (Docker)" | No benchmark citation |
| 4 | LLM judge "documented blind spot" for fluency over structure | Widely held view; no citation given |
| 5 | SWE-rebench GPT-4.1 contamination finding with specific date range | Paper confirms contamination effects; specific model/dates unverified |

---

## Section 2: ADR-011 — API & Interface Design

### Verified Claims (13)

| # | Claim | Evidence |
|---|-------|----------|
| 1 | `connectExecutionStream()` exists at `api/websocket.ts:9` | Function signature confirmed |
| 2 | 5 retries default | `maxRetries = 5` at line 14 |
| 3 | Backoff formula `retryDelayMs * retryCount` | Line 42: `setTimeout(connect, retryDelayMs * retries)` |
| 4 | `useWorkflowStream.ts` exists | Hook confirmed at stated path |
| 5 | `LivePage.tsx` uses WebSocket via `useWorkflowStream` | Import at line 4, usage at line 37 |
| 6 | `server/routes/workflows.py` exists as structural reference | Uses `APIRouter` pattern |
| 7 | Router registration via `app.include_router()` | Lines 132-135 of `app.py` confirm pattern |
| 8 | `contracts/` exists with additive-only policy | Docstring at `__init__.py:6`: "never remove or rename existing fields" |
| 9 | Pydantic v2 used in contracts | `pydantic>=2.0,<3` in pyproject.toml |
| 10 | `WorkflowRunner` has `run()` method | Class at line 46, `run()` at line 102 |
| 11 | `ClaudeAgent` exists | File and class confirmed |
| 12 | `typer` already in agentic-workflows-v2 deps | Line 20: `typer>=0.9,<1` |
| 13 | Both LangChain and native WorkflowRunners exist | Two `runner.py` files confirmed |

### Partially Accurate Claims (6)

**3.1 WebSocket backoff labeled "exponential" — actually linear**

Formula `retryDelayMs * retryCount` produces `1s, 2s, 3s, 4s, 5s` (linear). Exponential would be `retryDelayMs * 2^retryCount` producing `1s, 2s, 4s, 8s, 16s`. The formula itself is correctly stated, but the label is wrong.

**3.2 `useWorkflowStream.ts` event handling vocabulary is incomplete**

ADR says: `workflow_start`, `step_start/end`, `evaluation_*`, `error`. Actual switch handles: `workflow_start`, `step_start`, `step_end`, `step_complete`, `step_error`, `workflow_end`, `evaluation_start`, `evaluation_complete`, `error`, plus `keepalive` and `connection_established` in the type union. The ADR omits `step_complete`, `step_error`, `workflow_end`.

**3.3 New eval event taxonomy is novel, not reused**

Proposed events (`eval_start`, `phase_start`, `phase_end`, `eval_complete`, `error`) differ from the existing vocabulary. The ADR doesn't acknowledge this as a new taxonomy — it implies reuse.

**3.4 "30-60 minute workflow runs" is an ungrounded operational claim**

No codebase evidence supports or contradicts a specific duration. The infrastructure is functional, but the time figure cannot be verified from code.

**3.5 "Zero new client code" is overstated**

`connectExecutionStream()` hardcodes URL to `/ws/execution/${runId}`. A new `/ws/eval/` path requires either modifying the function signature or writing a new call-site. New TypeScript event types (`eval_start`, `phase_start`, etc.) also need definition.

**3.6 Hexagonal architecture is aspirational, not current state**

`server/routes/workflows.py` directly imports `LangChainRunner` (lines 46-52, 1182) with no port/adapter abstraction. The ADR proposes hexagonal for the new module but implies the codebase already follows the pattern.

### Inaccurate Claims (5)

**4.1 `tools/pyproject.toml` does not exist**

Same as ADR-010 finding. The root `pyproject.toml` is the correct file for `prompts-tools` dependencies.

**4.2 `typer>=0.12` version conflicts with existing `typer>=0.9,<1`**

ADR proposes adding `typer>=0.12` but the existing constraint is `>=0.9,<1`. The version discrepancy is not discussed.

**4.3 Typer "native Pydantic v2 integration" claim is version-dependent**

The comparison table says "Native" for Pydantic integration, but the risk section says it requires version 0.12+. These are internally inconsistent — the table implies current native support, the risk section says it's future.

**4.4 "38.7% of Python CLI projects use click" — uncited statistic**

This specific figure appears in two ADR sections with no source citation and no entry in the references table. Cannot be verified.

**4.5 The existing server already has SSE infrastructure**

`server/routes/workflows.py` implements SSE at `GET /api/runs/{run_id}/stream` (lines 660-682, `StreamingResponse` with `media_type="text/event-stream"`). The ADR argues SSE would require "a new FastAPI streaming response handler" — but one already exists. The argument for WebSocket over SSE should focus on client-side reuse, not server-side novelty.

### Missing Context the ADR Should Mention (6)

1. **SSE endpoint already exists** — weakens the "new infrastructure" argument for rejecting SSE
2. **Two `WorkflowRunner` implementations** — `Comparator` must choose between native and LangChain runners or abstract over both
3. **`ConnectionManager` has 500-event replay buffer** — relevant for late-joining eval clients
4. **`connectExecutionStream()` URL template is fixed** — requires extension to support `/ws/eval/` prefix
5. **`pytest-json-report` is net-new dependency** — not in any existing pyproject.toml
6. **`agentic-v2-eval` cross-package dependency** — not mentioned but required for `Scorer` imports

### Unverifiable External References (7)

| Reference | Status |
|-----------|--------|
| Cockburn, Hexagonal Architecture (2005) | Plausible; standard attribution |
| typer documentation (tiangolo.com) | Broadly accurate for typer 0.12+ |
| FastAPI WebSocket docs | Consistent with observed codebase usage |
| Promptfoo config reference | YAML-based LLM eval description accurate |
| Ably Engineering, WebSocket vs SSE (2024) | Conclusion reasonable; article unverified |
| Timeplus, WebSocket vs SSE (2024) | Same status as above |
| GitHub Actions "WebSocket log stream" | Simplification — GitHub uses HTTP chunked transfer, not pure WebSocket |

---

## Section 3: ADR-012 — UI Evaluation Hub

### Verified Claims (16)

| # | Claim | Evidence |
|---|-------|----------|
| 1 | `EvaluationsPage.tsx` exists and is a passive filtered table | Filters `r.evaluation_score != null`, renders static `<table>`, no CTA |
| 2 | Column headers match: Workflow, Score, Grade, Steps, Date, Details | `<thead>` at lines 35-44 matches exactly |
| 3 | 7-page route audit is accurate | `App.tsx`: `/`, `/workflows`, `/workflows/:name`, `/datasets`, `/evaluations`, `/runs/:filename`, `/live/:runId` |
| 4 | `connectExecutionStream()` exists at `api/websocket.ts:9` | Confirmed with 5-retry default |
| 5 | `useWorkflowStream.ts` exports `useWorkflowStream(runId: string \| null)` | Hook structure confirmed |
| 6 | `LivePage.tsx` uses WebSocket via `useWorkflowStream` | Import at line 4 |
| 7 | `WorkflowDAG.tsx` uses React Flow | Imports from `@xyflow/react`, renders `<ReactFlow>`, `<Background>`, `<Controls>`, `<MiniMap>` |
| 8 | React Flow is installed as `@xyflow/react` v12.4.0 | `package.json` dependency confirmed |
| 9 | Sidebar has "Evaluations" link | `Sidebar.tsx:15`: `{ to: "/evaluations", icon: Trophy, label: "Evaluations" }` |
| 10 | `CriterionRow` exists in `LivePage.tsx:223-250` | Bar colors: `bg-green-500` (>=80), `bg-amber-500` (>=50), `bg-red-500` (default) |
| 11 | Sidebar is 5-item nav | Dashboard, Workflows, Datasets, Evaluations, Live |
| 12 | No `useEvalStream.ts`, `pages/eval/`, or `components/eval/` exist | All proposed files confirmed absent |
| 13 | React 19 | `package.json`: `"react": "^19.0.0"` |
| 14 | "Six of seven pages untouched" | Only `EvaluationsPage.tsx` and `App.tsx` modified |
| 15 | Design tokens `bg-surface-1`, `bg-surface-2`, `bg-accent-blue/10`, `text-accent-blue`, `border-white/5`, `btn-ghost`, `card-hover`, `tabular-nums` are used | All found across multiple source files |
| 16 | `api/client.ts` has no `/eval/compare` or `/eval/validate-commit` endpoints | Confirmed absent; only `/api/eval/datasets` exists |

### Partially Accurate Claims (5)

**3.1 WebSocket backoff labeled "exponential" — actually linear**

Same convergent finding as ADR-011. Formula `retryDelayMs * retryCount` is linear, not exponential. The formula is correctly quoted but mislabeled.

**3.2 `useEvalStream` described as mirroring `useWorkflowStream` "line-for-line" with `useReducer`**

`useWorkflowStream` uses five `useState` calls (lines 27-35), not `useReducer`. An implementer building `useEvalStream` with `useReducer` would produce a structurally different hook, contradicting the "line-for-line mirror" intent.

**3.3 "No new Tailwind classes" — mixes custom tokens with standard utilities**

The token table implies all listed classes are custom. Several (`text-gray-400`, `text-gray-500`, `text-gray-600`) are standard Tailwind color utilities, not custom extensions. The constraint should say "no new custom tokens."

**3.4 `EvaluationsPage` description slightly understates current functionality**

The page also shows `evaluation_grade`, links to run detail pages, and has a non-trivial empty state with search icon and guidance copy. "Only filters runs by score" is directionally correct but incomplete.

**3.5 `bg-surface-2` token exists but `bg-surface-3` is omitted**

Both are defined in `tailwind.config.js`. `bg-surface-3` is defined but unused in any `.tsx` file. The omission is acceptable but should be noted.

### Inaccurate Claims (2)

**4.1 "No new WebSocket infrastructure" — backend route IS required**

The server WebSocket endpoint at `server/websocket.py:189` only handles `/ws/execution/{run_id}`. No `/ws/eval/*` handler exists. The client function (`connectExecutionStream`) is reusable, but a new server-side route handler must be written. This is a significant scope item not acknowledged.

**4.2 NNGroup citation mismatch**

The quote in section 5.1 about "dynamically display relevant fields based on users' prior input" comes from the NNGroup article "Wizards: Definition and Design Recommendations" (`nngroup.com/articles/wizards/`). But the references table (section 8) only cites the different article "4 Principles to Reduce Cognitive Load in Forms." The citation table is incomplete — it should include both NNGroup articles.

### Missing Context (7)

**7.1 `bg-surface-hover` is a phantom token in `EvaluationsPage.tsx`**

Line 60 uses `bg-surface-hover` as a Tailwind class, but this token is not defined in `tailwind.config.js` or `globals.css`. Tailwind JIT will silently drop it, producing no styles. Any implementer studying the existing page for token precedents may replicate this error.

**7.2 `useWorkflowStream` uses `useState`, not `useReducer`**

The ADR's pseudocode for `useEvalStream` specifies `useReducer`, claiming it mirrors `useWorkflowStream` "line-for-line." Using `useReducer` is a legitimate design choice but diverges from the pattern it claims to mirror.

**7.3 Eval WebSocket path `/ws/eval/{run_id}` requires new backend route**

Same as convergent finding. The server only registers `/ws/execution/{run_id}`. A new handler must be written.

**7.4 `WorkflowDetailPage` already has eval entry point**

The page includes `RunConfigForm` with evaluation dataset selection, rubric selection, multi-sample batch runs, and evaluation-enabled run triggering. The ADR's claim that the UI has "no entry point to run a new evaluation" is true for `EvaluationsPage`, but false at the application level. This is directly relevant context.

**7.5 Sidebar "Live" link points to `/live/latest`**

`Sidebar.tsx:16`: `{ to: "/live/latest", icon: Radio, label: "Live" }`. If navigated, the WebSocket tries to connect to `/ws/execution/latest`. This may or may not be handled gracefully — relevant for WebSocket infrastructure assessment.

**7.6 Partial eval API already exists**

`api/client.ts:64` defines `listEvaluationDatasets()` calling `GET /api/eval/datasets`. An eval API namespace already exists server-side. The proposed endpoints are additive but this existing namespace context is unstated.

**7.7 React Flow package name is `@xyflow/react`, not `reactflow`**

React Flow v12 publishes under the `@xyflow` organization. The ADR's reference to "reactflow.dev" is colloquially correct but the actual import uses `@xyflow/react`. Implementers should know the correct package name.

### External References Validation

| Reference | Verified | Notes |
|-----------|----------|-------|
| NNGroup "4 Principles to Reduce Cognitive Load" | Yes | Real article at nngroup.com/articles/4-principles-reduce-cognitive-load/ |
| NNGroup "Wizards" article | Yes (but missing from citation table) | Real article at nngroup.com/articles/wizards/ — quoted in section 5.1 but not cited in section 8 |
| GOV.UK "One thing per page" | Yes | Pattern at design-system.service.gov.uk/patterns/question-pages/; lab-tested through Register to Vote and GOV.UK Verify |
| Smashing Magazine (2017) | Yes | Real article, correct year, correct URL |
| GitHub Actions single-URL pattern | Unverified (common knowledge) | Behaviorally accurate |
| Vercel deployment status page | Unverified (common knowledge) | Behaviorally accurate |
| DORA State of DevOps 2024 | Partially | Report is real; "DORA Dashboard" as a canonical UI pattern is editorial |
| SWE-bench results viewer | Partially | Site exists at swebench.com; "dimension-per-row score bar" pattern unconfirmed |
| React Flow documentation | Yes | Library installed as `@xyflow/react` v12.4.0; reactflow.dev redirects correctly |

---

## Section 4: Cross-ADR Consistency Issues

### 4.1 Circular References Between ADR-010 and ADR-011

ADR-011 section 3.1 implies `Comparator.run()` already exists ("The `Comparator.run()` core (ADR-010) must be reachable..."). ADR-010 lists `comparator.py` as a new file. Neither file exists. Both ADRs reference each other as if the core exists, but it is itself proposed. This is acceptable for a set of coordinated proposals but should be stated explicitly.

### 4.2 Inconsistent Dependency Targets

- ADR-010: "Add typer, pytest-json-report to `tools/pyproject.toml`"
- ADR-011: "Add typer>=0.12, pytest-json-report>=1.5 to `tools/pyproject.toml`"
- Reality: `tools/pyproject.toml` does not exist. Root `pyproject.toml` manages `prompts-tools`. `typer>=0.9,<1` already in `agentic-workflows-v2/pyproject.toml`.

### 4.3 Scorer Range Inconsistency

- ADR-010: "0-100 weighted rubric score"
- Actual `Scorer.score()`: returns `float` in `[0.0, 1.0]`
- ADR-011 and ADR-012 do not reference the scorer directly but inherit this assumption

### 4.4 WebSocket "Zero New Infrastructure" vs Reality

All three ADRs frame the WebSocket infrastructure as fully reusable. In reality:
- **Client function**: reusable with URL parameterization (minor change)
- **Server endpoint**: `/ws/eval/{run_id}` does not exist (new code required)
- **Event types**: novel taxonomy (`eval_start`, `phase_start`, etc.) requires new TypeScript union types
- **React hook**: `useEvalStream` described as `useReducer`-based, but the template (`useWorkflowStream`) uses `useState`

---

## Section 5: Recommended Amendments

### Priority 1 — Factual Corrections (must fix before implementation)

| Item | ADR | Fix |
|------|-----|-----|
| SWE-rebench author | 010 | Change "Aleithan et al." to "Badertdinov et al." |
| SWE-bench Live author | 010 | Change "Gauthier Guinet et al." to "Zhang et al." |
| SWE-Bench++ author & year | 010 | Change "Chen et al., 2024" to "Wang et al., 2025" |
| Scorer output range | 010 | Change "0-100" to "0.0-1.0" |
| `tools/pyproject.toml` path | 010, 011 | Change to root `pyproject.toml` |
| "Exponential" backoff label | 011, 012 | Change to "linear backoff" or fix formula |

### Priority 2 — Accuracy Improvements (should fix for implementer clarity)

| Item | ADR | Fix |
|------|-----|-----|
| Acknowledge new backend WebSocket route | 011, 012 | Add `/ws/eval/{run_id}` to server scope |
| Note `connectExecutionStream` URL parameterization needed | 011, 012 | Describe function extension or new call-site |
| `useReducer` vs `useState` | 011, 012 | Either match `useWorkflowStream` or acknowledge divergence |
| Existing SSE endpoint | 011 | Acknowledge `GET /api/runs/{run_id}/stream` exists |
| Two `WorkflowRunner` implementations | 011 | Note native vs LangChain runner choice |
| `WorkflowDetailPage` eval entry point | 012 | Note existing `RunConfigForm` with eval dataset selection |
| Missing NNGroup "Wizards" citation | 012 | Add to references table |
| `coding_standards.yaml` full criteria list | 010 | List all 8 criteria, not 5 |
| `evaluate_with_llm()` is sync, not async | 010 | Note wrapping requirement |
| `agentic-v2-eval` cross-package dependency | 010, 011 | Add to dependency table |

### Priority 3 — Nice to Have

| Item | ADR | Fix |
|------|-----|-----|
| `bg-surface-hover` phantom token | 012 | Flag existing defect in `EvaluationsPage.tsx:60` |
| `ConnectionManager` replay buffer | 011 | Mention 500-event circular buffer for late joins |
| Partial eval API already exists | 012 | Note `GET /api/eval/datasets` in `client.ts` |
| React Flow package name | 012 | Use `@xyflow/react`, not `reactflow` |
| Remove uncited "38.7%" statistic | 011 | Either cite source or remove claim |

---

## Appendix: Source Files Verified

### ADR-010 Sources
- `tools/agents/benchmarks/llm_evaluator.py` — LLM judge (Layer 1)
- `agentic-v2-eval/src/agentic_v2_eval/scorer.py` — Rubric scorer (Layer 2)
- `agentic-v2-eval/src/agentic_v2_eval/rubrics/coding_standards.yaml` — Rubric criteria
- `agentic-workflows-v2/agentic_v2/workflows/runner.py` — WorkflowRunner
- `agentic-workflows-v2/agentic_v2/agents/implementations/claude_agent.py` — ClaudeAgent
- `tools/llm/llm_client.py` — LLMClient
- `tools/__init__.py` — Package exports
- `pyproject.toml` (root) — prompts-tools package config

### ADR-011 Sources
- `agentic-workflows-v2/ui/src/api/websocket.ts` — connectExecutionStream
- `agentic-workflows-v2/ui/src/hooks/useWorkflowStream.ts` — React hook
- `agentic-workflows-v2/ui/src/pages/LivePage.tsx` — WebSocket consumer
- `agentic-workflows-v2/ui/src/api/types.ts` — ExecutionEvent union
- `agentic-workflows-v2/agentic_v2/server/app.py` — Router registration
- `agentic-workflows-v2/agentic_v2/server/websocket.py` — ConnectionManager
- `agentic-workflows-v2/agentic_v2/server/routes/workflows.py` — Structural reference + SSE endpoint
- `agentic-workflows-v2/agentic_v2/contracts/__init__.py` — Additive-only policy

### ADR-012 Sources
- `agentic-workflows-v2/ui/src/App.tsx` — Route definitions
- `agentic-workflows-v2/ui/src/pages/EvaluationsPage.tsx` — Current eval page
- `agentic-workflows-v2/ui/src/pages/WorkflowDetailPage.tsx` — Existing eval entry point
- `agentic-workflows-v2/ui/src/components/layout/Sidebar.tsx` — Navigation
- `agentic-workflows-v2/ui/src/components/dag/WorkflowDAG.tsx` — React Flow usage
- `agentic-workflows-v2/ui/src/api/client.ts` — API client
- `agentic-workflows-v2/ui/src/styles/globals.css` — Custom CSS classes
- `agentic-workflows-v2/ui/tailwind.config.js` — Design tokens
- `agentic-workflows-v2/ui/package.json` — Dependencies
