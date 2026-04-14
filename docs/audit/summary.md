# Codebase Audit Summary — 2026-04-14
**Git SHA (audit):** 0252c88ce93792d05d13613e0b1f431d3193d006  
**Git SHA (after quick wins):** 7f1ae0f  
**Branch:** main  
**Audited by:** 7 parallel specialist agents  
**Quick wins implemented:** 2026-04-14  
**Reports:** [dependencies](dependencies.md) · [code-quality](code-quality.md) · [test-coverage](test-coverage.md) · [api-surface](api-surface.md) · [performance](performance.md) · [security](security.md) · [documentation](documentation.md)

---

## Overall Health: ⚠️ Issues Found (Quick Wins Complete)

12 quick wins identified at audit time. All 12 resolved: 9 implemented via commits, 3 were already resolved in the codebase (audit ran against a slightly stale snapshot: QW-1, QW-8, QW-12).

Remaining open work is in the Strategic Items backlog — no more quick wins outstanding.

---

## Metrics Snapshot (post quick-wins)

| Metric | Audit Value | Current Value | Gate | Status |
|--------|-------------|---------------|------|--------|
| Python packages | 3 | 3 | — | — |
| Source files (Python) | ~285 | ~285 | — | — |
| Test files | 78+ | 78+ | — | — |
| Files > 800 lines | 1 | 1 | 0 | ⚠️ |
| Silent exception swallows | 11 | 11 | 0 | ⚠️ |
| `tools/` modules with tests | ~3 of 35+ | ~3 of 35+ | 80% | 🔴 |
| Undeclared runtime deps | 3 | **0** ✅ | 0 | ✅ |
| Sync I/O in async handlers | 2 routes | 2 routes | 0 | ⚠️ |
| Endpoints missing `response_model` | 7 | **5** (2 wired) | 0 | ⚠️ |
| Sanitization enforcement | dry_run=True | **dry_run=False** ✅ | enforced | ✅ |
| `load_workflow_config()` caching | none | **@lru_cache** ✅ | — | ✅ |
| Auth default | opt-in/open | opt-in/open | enforced | ⚠️ |
| `.env.*` in `.gitignore` | missing | **present** ✅ | present | ✅ |
| `AGENTIC_FILE_BASE_DIR` documented | missing | **documented** ✅ | present | ✅ |
| Slow tests marked | 0 of 2 | **2 of 2** ✅ | all | ✅ |
| Docstring coverage (sampled) | ~92% | ~92% | 80% | ✅ |
| Hardcoded production secrets | 0 | 0 | 0 | ✅ |
| Star imports | 0 | 0 | 0 | ✅ |
| Bare `except:` | 0 | 0 | 0 | ✅ |

---

## Top 10 Prioritized Action Items (updated)

Items marked ✅ were resolved during quick-win implementation.

### ✅ ~~1. [CORRECTNESS] `ToolProtocol` not `@runtime_checkable`~~
Already present in codebase — audit snapshot was stale.

### ✅ 2. [RELIABILITY] Sanitization middleware in `dry_run=True` — never enforces
**Fixed:** `server/app.py:88` flipped to `dry_run=False`. Commit `9cc4003`.  
The sanitization chain now blocks/redacts unsafe content end-to-end.

### 3. 🔴 [PERFORMANCE] Sync I/O blocking the async event loop
**Files:** `server/routes/agents.py:46`, `server/datasets.py:114`  
Both `_discover_agents()` and `_load_eval_config()` perform synchronous file I/O inside async FastAPI route handlers, blocking the uvicorn event loop on every request. Neither result is cached.  
**Fix:** `asyncio.to_thread()` + `@lru_cache` (same pattern applied to `load_workflow_config` in QW-5). → Strategic item S-1.

### 4. 🔴 [SECURITY] `ShellTool` uses `create_subprocess_shell` with bypassable blocklist
**File:** `tools/builtin/shell_ops.py:113`  
The substring blocklist for dangerous commands is bypassable via casing/whitespace variants. `ShellExecTool` in the same codebase already uses the safe pattern (`create_subprocess_exec` + `shlex.split`). → Strategic item S-4.

### 5. 🔴 [RELIABILITY] 11 silent exception swallows
**Files:** `agent_resolver.py`, `capabilities.py`, `graph_wiring.py`, `langchain/tools.py`  
`except Exception: pass` with no logging or re-raise means failures disappear silently. → Strategic item S-5.

### 6. 🔴 [COVERAGE] `tools/` package — <10% test coverage, 35+ untested modules
**Worst offenders:** `model_probe.py` (2,313 lines, 0 tests), `llm_evaluator.py` (777 lines, 0 tests)  
Coverage gate (`fail_under=80`) cannot pass while these are untested. → Strategic item S-2.

### ✅ 7. [DEPS] `openai`, `anthropic`, `numpy` undeclared in `prompts-tools`
**Fixed:** Added to `pyproject.toml` as `openai>=1.0,<2`, `anthropic>=0.40,<1`, `numpy>=1.24.0,<3`. Commits `61a7168` + `271939f`.

### 8. ⚠️ [SECURITY] Auth open by default — all `/api/` routes publicly accessible
**File:** `agentic_v2/server/auth.py`  
With no `AGENTIC_API_KEY` set, workflow execution and shell tool invocation are unauthenticated. A startup guard should reject non-localhost bindings when no key is configured. → Strategic item S-3.

### 9. ⚠️ [PERFORMANCE] `subprocess.run()` + `time.sleep()` in async call paths
**Files:** `tools/llm/probe_config.py`, `tools/llm/provider_adapters.py`, `tools/core/tool_init.py`, `langchain/tools.py:225`  
These block the event loop for the duration of the call. Wrap with `asyncio.to_thread()` or migrate to async equivalents. → Strategic item S-1 (broader async I/O fix).

### 10. ⚠️ [QUALITY] `langchain/graph_wiring.py` at 807 lines — over the 800-line gate
**File:** `agentic_v2/langchain/graph_wiring.py`  
Only file exceeding the project's 800-line limit. → Strategic item S-6.

---

## Quick Wins — Final Status

| # | Fix | Status | Commit | Notes |
|---|-----|--------|--------|-------|
| QW-1 | `@runtime_checkable` on `ToolProtocol` | ✅ Already present | — | Audit snapshot was stale |
| QW-2 | Wire `response_model`s to endpoints | ✅ Partial (2/7) | `f187420` | 5 remaining need new models; see S-10 |
| QW-3 | Flip sanitization `dry_run=False` | ✅ Done | `9cc4003` | |
| QW-4 | `.env.*` wildcard in `.gitignore` | ✅ Done | `2900cc0` | |
| QW-5 | `@lru_cache` on `load_workflow_config()` | ✅ Done | `9cc4003` + `34294c5` | Added cache invalidation on save + test isolation fixture |
| QW-6 | README port `8000` → `8010` | ✅ Done | `2900cc0` | Fixed in both READMEs |
| QW-7 | CLAUDE.md tool count `12` → `11` | ✅ Done | `2900cc0` | |
| QW-8 | Delete 2 duplicate test files | ✅ Already deleted | — | Audit snapshot was stale |
| QW-9 | Mark slow tests `@pytest.mark.slow` | ✅ Done | `e07a991` | `test_timeout_handling` + `test_shell_tool_timeout` |
| QW-10 | Declare `openai`, `anthropic`, `numpy` | ✅ Done | `61a7168` + `271939f` | Includes upper bounds |
| QW-11 | `AGENTIC_FILE_BASE_DIR` in `.env.example` | ✅ Done | `c9b3247` + `7f1ae0f` | Uncommented for dotenv tool compatibility |
| QW-12 | `## Boundaries` in persona files | ✅ Already present | — | Audit snapshot was stale |

### Implementation discoveries (beyond the original spec)

During the two-stage review process, reviewers surfaced additional issues that were fixed inline:

- **QW-5 expanded:** `@lru_cache` on `load_workflow_config()` required a `cache_clear()` call in the workflow save route (`routes/workflows.py`) to prevent stale YAML being served after an editor save. A pytest autouse fixture was also added to `tests/conftest.py` for test isolation under parallel execution.
- **QW-10 refined:** Initial `numpy>=1.24.0` spec lacked an upper bound; corrected to `numpy>=1.24.0,<3` for semver safety (consistent with `openai<2` and `anthropic<1` pins).
- **QW-11 format:** Initial `.env.example` entry used a commented-out key (`# AGENTIC_FILE_BASE_DIR=`), inconsistent with all other entries; corrected to uncommented form for dotenv tool compatibility.

---

## Strategic Items (require planning / design)

| Priority | Item | Effort | Status |
|----------|------|--------|--------|
| S-1 | Migrate `server/routes/agents.py` + `server/datasets.py` to async I/O with caching | M | Open |
| S-2 | Write tests for `tools/` package (35+ untested modules, start with `llm_evaluator.py`) | L | Open |
| S-3 | Implement mandatory auth mode for non-localhost bindings | M | Open |
| S-4 | Replace `ShellTool`'s `create_subprocess_shell` with `create_subprocess_exec` + `shlex.split` | S | Open |
| S-5 | Fix 11 silent exception swallows — add logging + re-raise pattern | M | Open |
| S-6 | Split `graph_wiring.py` into 3 focused modules | M | Open |
| S-7 | Replace ~30 magic number floats in `scoring_criteria.py` with named constants | S | Open |
| S-8 | Enable `ruff BLE001` in CI to enforce no-blind-except at the tool level | S | Open |
| S-9 | Add rate limiting to `/api/run` (unbounded workflow spawning) | M | Open |
| S-10 | Define missing `response_model` types for 5 endpoints + export `openapi.json` | S | Open |
| S-11 | Refactor `InMemoryVectorStore.search()` to cache L2 norms and add result limits | M | Open |
| S-12 | Replace 81 eager f-string log calls in MCP subsystem with lazy `%s` format | S | Open |

---

## Cross-Reference: Compounding Issues (updated)

| Module | Quality | Coverage | Performance | Security | Fixed? |
|--------|---------|----------|-------------|---------|--------|
| `server/datasets.py` | deep nesting | no dedicated tests | sync I/O in async | path safety opt-in (now documented) | Partial |
| `langchain/graph_wiring.py` | 807 lines, silent excepts | partial coverage | — | — | No |
| `langchain/tools.py` | silent excepts | partial | subprocess in async | — | No |
| `tools/llm/provider_adapters.py` | — | 0 tests | `time.sleep` in async | **deps now declared** ✅ | Partial |
| `server/app.py` | — | — | — | **dry_run=False** ✅, open auth remains | Partial |

---

## What's Working Well

- **Docstring coverage: ~92%** — exceptionally strong, Google-style, consistent
- **No hardcoded production secrets** — clean across 285 files
- **No bare `except:` or star imports** — zero occurrences
- **RAG embedding cache** — content-hash dedup is correct and present
- **`CodeExecutionTool`** — AST safety check + sandboxing is well-implemented
- **Constant-time token comparison** — `secrets.compare_digest` used correctly
- **`LanceDBVectorStore`** — properly caches, deduplicates, and uses `Path.resolve()`
- **Optional dep guarding** — all LangChain adapter imports are `try/except`-guarded
- **Protocol coverage** — all 9 protocols are `@runtime_checkable` and fully typed ✅
- **Workflow config caching** — `load_workflow_config()` now `@lru_cache` with save-route invalidation ✅
- **Sanitization enforcement** — middleware now in blocking mode ✅
