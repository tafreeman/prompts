# Phase 4: Best Practices & Standards

Local-only learning-platform calibration applied.

## Summary

- **Framework & Language (4A):** 0 Critical, 2 High, 8 Medium, 11 Low
- **CI/CD & DevEx (4B):** 1 Critical, 7 High, 11 Medium, 6 Low

---

## Framework & Language Findings (Phase 4A)

### High

- **H1** `.pre-commit-config.yaml:32-49` — mypy and pydocstyle hooks commented out with TODOs. CLAUDE.md claims they run. Re-enable scoped (`files: ^agentic_v2/core/` at minimum) or update the docs.
- **H2** `agentic_v2/integrations/langchain.py:68-69, 170-171` — Pydantic v1-style `class Config: arbitrary_types_allowed = True` in two LangChain wrappers. Replace with `model_config = ConfigDict(arbitrary_types_allowed=True)`. The only v1-style config in the repo; lives in the ADR-013-deprecated path.

### Medium

- **M1** `agentic_v2/models/router.py:296` — `asyncio.get_event_loop()` in async context. Use `asyncio.to_thread(self._health_checker, model)`.
- **M2** Zero `Depends(` usages across `server/routes/*.py` — services accessed via module-level globals. Add `dependencies.py` with `Annotated[..., Depends(...)]` — modern FastAPI pedagogy and trivially mockable.
- **M3** `tomllib` not used despite 3.11+ baseline — informational; YAML remains appropriate for workflow configs.
- **M4** `agentic_v2/integrations/base.py:133,149,166,179` — naive `datetime.now()` without `timezone.utc`.
- **M5** `RunConfigForm.tsx` 14× `useState` + zero `useReducer` in whole `ui/src`. Prime pedagogy target — one `useReducer` collapses 14 setters.
- **M6** Ruff ignore list defers ~500 UP006/UP007/UP017/UP035/UP037/UP045 violations ("Sprint C bulk migration"). One-shot `ruff check --fix` day.
- **M7** `contracts/events.py:103-114` uses `Union[...]` — intentional for `TypeAdapter` discriminator; add a comment explaining why PEP 604 `|` isn't used here.
- **M8** 13 `asyncio.gather` call sites across engine/orchestrator; no `asyncio.TaskGroup` usage. Migrate engine path first for structured concurrency.

### Low

- **L1** `ui/` has no ESLint or Prettier config — no exhaustive-deps/rules-of-hooks enforcement. Add `eslint` + `@typescript-eslint` + `eslint-plugin-react-hooks`.
- **L2** React 19 features unused: no `useOptimistic`, `useTransition`, `useDeferredValue`, `useActionState`, `use()`. `useTransition` for dataset preview fetches is low-effort, high-pedagogy.
- **L3** `forwardRef` unused (React 19 allows ref-as-prop) — informational, nothing to migrate.
- **L4** `ui/src/api/websocket.ts:34-36` — `catch { /* ignore parse errors */ }` violates the no-silent-swallow rule.
- **L5** No `React.lazy` / `manualChunks` code-splitting.
- **L6** Raw fetch in `useEffect` without `AbortController` in `RunConfigForm.tsx:76-79`. Convert to `useQuery`.
- **L7** Mixed `StrEnum` vs `class X(str, Enum)` (UP042 deferred, 20 hits).
- **L8** `typing.Self` never used (3.11+ feature). Builder patterns / `@classmethod` factories benefit.
- **L9** `node_modules/` committed at repo root (stale from misfired top-level `npm install`). UI deps live in `agentic-workflows-v2/ui/node_modules/`.
- **L10** Two ruff configs (`pyproject.toml` root vs `agentic-workflows-v2/pyproject.toml`) — different ignore lists; clarify which wins.
- **L11** `router.py:282-308` — `check_one` health-check fan-out unbounded; add `asyncio.Semaphore(4)` or `TaskGroup` with bounded concurrency.

### Framework Strengths

1. Pydantic v2 idioms are excellent: `ConfigDict(extra="forbid", frozen=True)`, `@computed_field`, `@field_validator(mode="before")`, `@model_validator(mode="after")`, discriminated-union `Annotated[Union[...], Field(discriminator="type")]` with `TypeAdapter`, `BaseAgent(ABC, Generic[TInput, TOutput])`.
2. FastAPI lifespan uses `@asynccontextmanager` (post-0.93 canonical); no `@app.on_event`.
3. `APIRouter(tags=[...])` + 51 `response_model=`/`status_code=` decorators.
4. 95%+ of `datetime.now(...)` calls include `timezone.utc`.
5. New `contracts/verification.py` and `contracts/sanitization.py` adopt 3.11+ `enum.StrEnum`.
6. TanStack Query v5 canonical object form everywhere; arrays as query keys; dependent queries gated via `enabled`.
7. `tsconfig.json` strict — `noUncheckedIndexedAccess`, `noUnusedLocals`, `noUnusedParameters`.
8. WebSocket reconnect with exponential backoff + `closed` flag in `ui/src/api/websocket.ts`.
9. RAG pipeline uses immutable frozen Pydantic models consistently.
10. LangGraph integration gated behind try/except + 501 when extras missing + deprecation filterwarnings entry.
11. Ruff rule set matches the documented standard exactly.

---

## CI/CD & DevEx Findings (Phase 4B)

### Critical

**C1 — Most CI gates silently disabled**
`.github/workflows/{eval-package-ci,tools-ci,docs-verify,dependency-review,performance-benchmark,eval-poc}.yml` all reduced to `workflow_dispatch:` only with `# TODO(tech-debt)` comments. Only 4 of 13 workflows actually trigger on PRs: `ci.yml`, `windows-workflows-ci.yml` (paths-filtered), `manifest-temperature-check.yml` (paths-filtered), `prompt-validation.yml`/`prompt-quality-gate.yml` (paths-filtered to `prompts/**`). `AGENTIC_NO_LLM=1` (landed in `c2aff71`/`ca106eb`) was the stated blocker for re-enabling — unblock now.

### High

- **H1** Phantom action tags: `actions/checkout@v6` (real latest: v5), `setup-python@v6` (real: v5), `upload-artifact@v7`/`download-artifact@v8` (real: v4), `setup-node@v6` (real: v4), `docker/build-push-action@v7` (real: v6), `softprops/action-gh-release@v3` (real: v2), `codecov-action@v6` (real: v5), `setup-buildx-action@v4` (real: v3). Resolving today by fallback; breaks when those future majors ship.
- **H2** `agentic-workflows-v2/pyproject.toml` ruff `ignore` list silences ~40 rules including `RUF006` (async-dangling-task — real bug class) and `S307` (eval-usage). Ratchet-forward 5 rules/sprint; prioritize correctness (`RUF006`, `B904`, `F841`, `S307`, `B017`) over style.
- **H3** `.pre-commit-config.yaml` missing mypy+pydocstyle — CLAUDE.md and CONTRIBUTING.md advertise them. Re-scope mypy to clean dirs (`core/`, `contracts/`) and ratchet outward, OR update docs.
- **H4** No `concurrency:` group on PR workflows — stale runs waste minutes. Add `concurrency: { group: ${{github.workflow}}-${{github.ref}}, cancel-in-progress: true }` to PR workflows.
- **H5** Pre-commit hook revs not tracked by Dependabot (ruff/black/isort); adding `package-ecosystem: "pre-commit"` closes the gap.
- **H6** Root `pyproject.toml` declares `[tool.uv.workspace]` but CI uses plain `pip install -e` per package — cold installs ~90s vs ~15s with uv. Adopt `astral-sh/setup-uv@v5 + uv sync --frozen`.
- **H7** `justfile` hard-coded to `powershell.exe` — Linux/macOS contributors blocked at `just setup`. Either portable `just` or `os() == "windows"` branching.

### Medium

- **M1** `ci.yml` test-coverage runs only Python 3.11 + ubuntu-latest. Windows-primary project; matrix should include `[ubuntu-latest, windows-latest] × ['3.11', '3.12']`.
- **M2** Playwright browser cache not restored — 20s reinstall per CI run. `actions/cache@v4` keyed on `package-lock.json` Playwright version.
- **M3** `ui/` has no ESLint config; `tsc --noEmit` is only frontend gate. Add `eslint` + `@typescript-eslint` + `eslint-plugin-react-hooks` + `jsx-a11y`.
- **M4** `agentic-workflows-v2/manifest.json` stale — lists 33 specific test files "Generated during test phase"; metadata says `"backend": "empty", "frontend": "not a directory"`. Delete or regenerate.
- **M5** `docker-compose.yml` wires Jaeger + OTEL collector — excellent for learners — but `CONTRIBUTING.md` never mentions `localhost:16686` as the "see your traces" URL. Add Observability section.
- **M6** Three Node versions across CI: `nightly.yml` 22.12, `ci.yml` 20, `docs-verify` 18. Add `.nvmrc` + `.python-version` as single source.
- **M7** `prompt-validation.yml` runs Python 3.13 — not a declared target. Standardize on 3.11+3.12.
- **M8** `.claude/settings.json` allows `npx:*` while project CLAUDE.md says "use npm instead of npx." Remove or warn.
- **M9** `ci.yml` `e2e-streaming` uses `GITHUB_TOKEN` for LLM; `AGENTIC_NO_LLM=1` now landed — switch and drop `models: read` permission.
- **M10** `docformatter` 1.7.7 and `detect-secrets` 1.5.0 predate current releases; unblocked by H5.
- **M11** No `CODEOWNERS` file — even solo, documents domain structure for the team.

### Low

- **L1** `justfile` lacks `lint`, `format`, `clean`, `pre-commit` recipes.
- **L2** `scripts/` at repo root is a grab-bag of one-off fixers (`fix-missing-init.py`, `fix-print-to-logging.py`, `fix-trailing-whitespace.py`, `fix-claudemd-counts.py`). Move to `scripts/migrations/` or delete.
- **L3** `.dockerignore` doesn't exclude `presentation/`, `_bmad*`, `_analysis`, `docs/`, `research/`, `planning-artifacts/` — build bloat.
- **L4** Verify `.gitignore` covers `output/`, `runs/`, `decks-generated/`.
- **L5** `.devcontainer/devcontainer.json` `postCreateCommand` doesn't run `pre-commit install` — first push from devcontainer bypasses local hooks.
- **L6** `Dockerfile.ui` uses `node:25-bookworm-slim`; CI uses 20; `setup-dev.ps1` gates 20+. Unify.

### DevOps / DX Strengths

1. **Observability stack is learner-gold.** `docker-compose up` brings backend + UI + OTEL + Jaeger on one command; single best teaching affordance.
2. **Wire-format drift gate** — regenerates both Py and TS in CI and diffs. Textbook pattern.
3. **`setup-dev.ps1`** — genuinely one-command: prereqs check, uv install, UI install, 6-workflow validation, dry-run smoke, health-endpoint probe. Windows-polished.
4. **Nightly 50× streaming flake gate** with SLO data persisted to a dedicated `slo-data` branch — rolling p95 + 0.5% flake enforcement.
5. **Dependabot** covers 6 ecosystems with staggered Monday schedules.
6. **`.claude/settings.json`** PreToolUse blocks `.env`; PostToolUse auto-runs ruff fix/format on Python edits; SessionStart surfaces venv/node state.
7. **Ruff per-file overrides for tests** (`S101/S105/S106/S108` in `tests/**`) — correct scoped approach.
8. **CONTRIBUTING.md** is actionable, dated (2026-04-22), 7-section flow matches contributor needs.
9. **PR template + 2 issue templates + CODE_OF_CONDUCT + SECURITY.md + SUPPORT.md** in `agentic-workflows-v2/`.
10. **`agentic devex port-guard`** invoked by `setup-dev.ps1` preempts "port 8010 in use."
