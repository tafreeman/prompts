# Changelog

All notable changes to this project are documented here.

---

## [Unreleased]

### New Features

- **Epic 1 — Platform Foundation (agentic-workflows-v2)**
  - **Typed core protocols** — `AgentProtocol.run` no longer accepts/returns `Any`; signature tightened to `object` so type checkers stop treating agent I/O as opaque. Companion `ToolProtocol` conformance test added.
  - **Consolidated `Settings`** — All environment variable reads routed through a single typed `pydantic-settings` class; scattered `os.environ` lookups removed so misconfigured deployments fail fast at startup instead of deep inside a run.
  - **Adapter registry test isolation** — Autouse fixture resets the `AdapterRegistry` singleton between tests, eliminating cross-test leakage and flakes when suites register alternate engine backends.
  - **Schema-drift CI gate** — New snapshot test on `contracts/` Pydantic models fails the build on any unreviewed wire-format change; `scripts/generate_schemas.py` refreshes the canonical snapshot.
  - **OTEL parent-child trace assertion** — Regression test verifies the engine → agent span chain is preserved end-to-end so distributed traces remain connected in Jaeger / Tempo.
  - **Golden-output regression test** — Deterministic fixture locks the `code_review` workflow's final output; any behavioral drift in the native engine trips the test.
  - **CI lint + coverage enforcement** — Ruff runs as a required job and the 80% coverage floor is now enforced in GitHub Actions rather than advisory.
  - **MCP results cleanup** — Ruff `UP006` / `S324` fixes across `mcp/results` remove legacy typing forms and insecure hash defaults.

- **Epic 2 — Observable Execution (agentic-workflows-v2)**
  - **Typed execution-event wire format** — New `contracts/events.py` Pydantic discriminated union covers `workflow_start`, `step_start`, `step_end`, `step_complete`, `step_error`, `workflow_end`, and `evaluation_*`. WebSocket and SSE broadcasts validate before emit; client union in `ui/src/api/types.ts` stays in lockstep.
  - **Live DAG animation** — `@xyflow/react` nodes and edges animate through queued → running → complete / error states as events arrive on `/ws/execution/{run_id}`, so users can watch a run progress without opening server logs.
  - **StepNode B2 redesign** — Each node now renders an ASCII status chip, LLM tier pill, token counter, and a streaming-progress bar driven by live events.
  - **Step drill-down panel** — Click a node to see a five-field detail pane (inputs, outputs, status, timing, errors) that handles partial state gracefully while a step is still running.
  - **Playwright streaming PR gate** — New E2E job runs the streaming flow 5× per PR using `data-testid` hooks added across the UI; any single failure blocks merge.
  - **WebSocket reconnect-replay test** — Fault-injection E2E kills the socket mid-run and asserts the server's 500-event replay buffer restores UI state on reconnect.
  - **Time-to-first-span SLO + p95 gate** — New measurement test records first-span latency and fails the build if the p95 regresses past the contract.
  - **Nightly 50× reliability job** — Streaming E2E runs 50× on a nightly cron with a rolling flake-rate gate; reconnect and p95 contracts hardened alongside.

- **Epic 3 — DevEx / Windows (agentic-workflows-v2)**
  - **Windows bring-up hardening** — `scripts/setup-dev.ps1` one-command bootstrap validated in CI so a fresh Windows clone installs deps, validates workflows, and runs a smoke test without manual intervention.
  - **`port-guard` devex tool** — Detects and reports processes holding dev ports (8010 / 5173 / 6006) before server startup so conflicts surface with an actionable message instead of a cryptic bind error.
  - **`workspace-test-runner` tool** — Single entry point to run the right test suite for whichever package you're in (backend pytest, eval pytest, UI vitest).
  - **`workflow-linter` tool** — Validates YAML workflow definitions against the required-fields contract (`name`, `agent`, `description`, `depends_on`, `inputs`, `outputs`) before they reach the runtime.
  - **Windows Unicode CLI fix** — `agentic` CLI no longer crashes on the Windows default codepage when rendering non-ASCII output; CLI verification added to CI to prevent regressions.

- **Epic 6 — Evaluation & Data Depth (agentic-workflows-v2)**
  - **Contracts** — Additive Pydantic v2 models (`EvaluationCriterionDetail`, `ScoreLayersModel`, `HardGatesModel`, `FloorViolationModel`, `RunEvaluationDetail`, `DatasetSampleSummary`, …) mirrored as TypeScript interfaces in `ui/src/api/types.ts`; `EvaluationCompleteEvent` expanded with `passed`, `pass_threshold`, `criteria`.
  - **Tokens-30d stat** — `RunsSummaryResponse` gains `tokens_30d`; `run_logger.summary()` aggregates tokens across all runs started in the last 30 days; Dashboard live stat wired to real data.
  - **`GET /runs/{filename}/evaluation`** — Returns full rubric breakdown for any stored run, including criteria scores, score layers, hard gates, and floor violations.
  - **Dataset sample endpoints** — `GET /eval/datasets/sample-list?dataset_id=…&limit=…` and `GET /eval/datasets/sample-detail?dataset_id=…&sample_index=…`; dataset IDs use query params to handle slash characters.
  - **Evaluations page** — `EvaluationRubricAccordion` with lazy `[+]`/`[-]` expansion: criterion table (normalized %, ASCII progress bar, `[FLOOR]` badge), score layers, hard gate `[OK]`/`[FAIL]` rows, floor violation list.
  - **Datasets page** — 3-pane browser: dataset catalog → `SampleIndexGrid` (paginated `[<]`/`[>]`) → `DatasetDetailPane` (collapsible `[meta +/-]`, field rendering, JSON viewer, workflow preview badge).

- **Epic 5 — Console UI Polish (agentic-workflows-v2/ui)**
  - `StatusBadge` migrated to ASCII bracket format: `[OK ]` `[RUN]` `[ERR]` `[WARN]` using `--b-*` CSS tokens; works across dark / paper / bolt themes.
  - `useHotkeys` hook — global keyboard shortcuts (n / f / / / j / k / Esc) with input-focus guard and unmount cleanup.
  - Dashboard filter — `/` and `f` focus the filter input; `Esc` clears and blurs; narrows runs by workflow name or run ID.
  - State pages — `EmptyState` (`$ no <entity> yet`), `ErrorBanner` (`[!] {msg}`), `NotFoundPage` (404 terminal-style), `AppErrorBoundary` (React error boundary).
  - Skip-to-main link — visually hidden, appears on first Tab; `<main id="main-content">` as target.
  - Focus ring audit — `focus:ring-1 focus:ring-b-clay/50` added to all interactive elements; audit notes at `docs/a11y-focus-ring-audit.md`.
  - Paper theme contrast QA — `--b-text-dim` on `--b-bg1` verified at 7.45:1 (passes AA); bolt 5.92:1; dark 3.80:1 (dim tier, intentional).
  - `BDagMini` — pure SVG static DAG thumbnail; reuses `layoutDAG` (Kahn topological sort); linear chains render as vertical, parallel branches center-aligned per rank; themed via CSS vars.

- **`skill-architect` agent** — New AI persona specialized in designing, extracting, and refactoring skills as reusable prompt programs. Added to the canonical agent roster with full documentation.
- **`verify-and-correct` skill** — Bounded self-correction loop: automatically runs tests, lint, and type checks after code changes, then retries fixes (up to a limit) before reporting back. Reduces back-and-forth on build failures.
- **`session-plan` skill** — Plan a focused session with 1–2 goals, explicit success criteria, and a TODO checklist. Prevents mega-sessions that hit rate limits by scoping work upfront.
- **Headless prompts** — New infrastructure for running agent prompts without an interactive session.
- **Adapter registry CLI wiring (ADR-001)** — Orchestrator, workflow runner, and CLI now route through the adapter registry, making engine backends (native DAG, LangGraph) fully swappable at runtime.
- **SmartModelRouter hardening (ADR-002)** — Added persistence across restarts, `Retry-After` header support, and degraded-mode fallback so the router stays operational when providers are rate-limited or unavailable.

### Improvements

- **CI pipeline upgrades** — Updated `actions/setup-python` from v4 → v5 across all workflows. Added cross-package E2E job, expanded security scanning with `pip-audit`, and tightened dependency review to fail on severity `moderate`.
- **Release pipeline** — New tag-triggered `deploy.yml` with build provenance for reproducible releases.
- **Performance regression detection** — Rewrote `performance-benchmark.yml` to compare against a stored baseline and fail on detected regressions.
- **Secret sanitization rule** — Always-on sanitization middleware now redacts API keys, tokens, and passwords before they reach LLM context. Covers all agent sessions by default.
- **Backlog tracking** — Added 11 new backlog tickets (rows 34–44) covering architectural debt, test gaps, and documentation tasks.

### Security

- **P0 tool-layer hardening** — `http_ops`, `search_ops`, and `shell_ops` received critical security fixes: SSRF URL validation, shell injection blocklist (20+ blocked patterns), `shlex.split` with `shell=False`, path traversal guards, and `__builtins__` restriction in the code execution sandbox.

### Bug Fixes & Documentation

- Fixed factual drift across monorepo documentation (CLAUDE.md, AGENTS.md, README files, ADRs).
- Corrected 40+ dangling references to deleted prompts and removed workflows.
- Removed 23 duplicate tests, fixed 2 broken tests as part of ADR-008 test coverage overhaul.
- Aligned stale agent config entries with the current agent roster.

### Test Coverage (ADR-008)

- Added tests for 12+ previously untested modules, including evaluation pipeline, workflow pipeline, server backends, LLM judge, and scoring.
- Hardened server test coverage for streaming backends and session handling.
- Overall test coverage for `agentic_v2` raised toward the 80% target.

### Cleanup & Refactoring

- **Presentation system extracted** — The presentation/deck builder has been moved to its own standalone repository (`present`). 245 files removed from this repo; raw-themes data and scripts are preserved in the new repo.
- Removed deprecated agent prompts, workflow definitions, Copilot config, and stale GitHub Actions workflows.
- Removed dead prompt constants, obsolete artifact files, and cleaned up `.gitignore`.

---

## Earlier History

For changes prior to March 2026, see the git log:

```
git log --oneline --before="2026-03-01"
```
