# Code Quality Report

**Repository:** `tafreeman/prompts`
**Date:** 2026-03-03
**Auditor:** Code Quality Auditor (Automated Analysis)

---

## Executive Summary

The `agentic-workflows-v2` package demonstrates **strong code quality discipline**: zero bare `except:` clauses, consistent `from __future__ import annotations` usage across all 99 production modules, a well-structured error hierarchy, and proper use of `logging.getLogger(__name__)` across 40+ modules. Pre-commit hooks enforce formatting and linting on every commit.

Key gaps exist in the **tools/** package (legacy codebase with 365 print() calls, no future annotations, no ruff/mypy config), **CI coverage thresholds** (60% in CI vs 80% in pyproject.toml), and **several oversized files** exceeding the 800-line target. The ruff configuration is missing from the main `agentic-workflows-v2` pyproject.toml, relying solely on pre-commit hooks for enforcement.

**Overall Grade: B+** — The core package is well-maintained; the tools/ package needs modernization.

---

## 1. Linting Configuration & Results

### Pre-commit Hook Chain

| Hook | Version | Purpose | Status |
|------|---------|---------|--------|
| black | v26.1.0 | Code formatting (line-length 88) | Active |
| isort | v7.0.0 | Import sorting (profile=black) | Active |
| ruff | v0.15.0 | Linting with auto-fix | Active |
| docformatter | v1.7.7 | Docstring formatting (wrap 79) | Active |
| mypy | v1.19.1 | Type checking (--ignore-missing-imports) | Active |
| pydocstyle | v6.3.0 | Docstring convention (google) | Active |

### Ruff Configuration Analysis

**agentic-workflows-v2/pyproject.toml:** No `[tool.ruff]` section. Ruff runs via pre-commit with default rules + `--fix`. This means:
- Rule selection defaults to `E` (pycodestyle errors) and `F` (pyflakes) only
- CLAUDE.md prescribes: `E, F, W, I, N, UP, S, B, A, C4, SIM, TCH, RUF` — these are **not configured**
- Missing rules: `S` (bandit/security), `B` (bugbear), `UP` (pyupgrade), `SIM` (simplification), `N` (naming), `TCH` (type-checking), `RUF` (ruff-specific)

**agentic-v2-eval/pyproject.toml:** Has explicit config:
```toml
[tool.ruff]
line-length = 100    # Inconsistent with black's 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B", "C4"]  # Better but still missing S, N, SIM, TCH, RUF, W
```

**Root pyproject.toml (tools):** No ruff configuration at all.

### Bare Except Clauses

**Zero bare `except:` found** across the entire repository. This is excellent. All exception handlers catch specific types.

### Exception Handling Patterns

- **`except Exception` usage:** 144 occurrences in agentic_v2, 113 in tools/
- Most are appropriate catch-all handlers in infrastructure code (tool execution, LLM backends, CLI error display)
- The `tools/__init__.py` has a broad `except Exception` for optional import that could mask real errors
- `except ImportError` properly used for optional dependency guards (langchain, dotenv)

---

## 2. Type Checking Assessment

### mypy Configuration

**Pre-commit:** `--ignore-missing-imports` only (loose). No `--strict`, no `disallow_untyped_defs`.

**agentic-v2-eval/pyproject.toml:** Stricter:
```toml
[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

**agentic-workflows-v2 and tools:** No `[tool.mypy]` section at all.

### Type Annotation Quality

**agentic-workflows-v2 (GOOD):**
- 99/99 production files use `from __future__ import annotations`
- `core/protocols.py` uses `typing.Protocol` with `@runtime_checkable` — proper structural subtyping
- ~206 occurrences of `Any` annotations across 50 files — some are necessary for protocol interfaces (e.g., `ExecutionEngine.execute()` accepts `workflow: Any`), but others could be tightened
- Pydantic models in `contracts/` are fully typed
- RAG pipeline modules have strong typing throughout

**tools/ package (WEAK):**
- 28 out of 42 Python files lack `from __future__ import annotations`
- Uses legacy `Dict`, `List`, `Set`, `Tuple`, `Optional` from `typing` (should be `dict`, `list`, `set`, `tuple`, `X | None`)
- `tools/core/errors.py` uses `Set[ErrorCode]`, `Tuple[ErrorCode, bool]`, `Optional[int]` — legacy style
- Type annotations present on public functions but inconsistent on internal helpers

### Protocol Usage

The `core/protocols.py` file is well-designed:
- 6 protocols: `ExecutionEngine`, `SupportsStreaming`, `SupportsCheckpointing`, `AgentProtocol`, `ToolProtocol`, `MemoryStoreProtocol`
- All `@runtime_checkable` for duck-typing verification
- RAG has its own parallel protocol set: `LoaderProtocol`, `ChunkerProtocol`, `EmbeddingProtocol`, `VectorStoreProtocol`

**Concern:** Several protocol methods use `Any` for both input and return types (e.g., `execute(workflow: Any) -> Any`), which limits the value of static type checking.

---

## 3. Test Suite Analysis

### Test Counts

| Location | Files | Test Functions | Lines |
|----------|-------|----------------|-------|
| agentic-workflows-v2/tests/ | 68 | 1,387 (sync) + 334 (async) | 20,236 |
| agentic-v2-eval/tests/ | ~10 | ~100+ | ~2,400 |
| tests/e2e/ | 1 | few | minimal |

**Total reported: 1,305 passing, 3 pre-existing failures, 15 skipped** (from memory context).

### Test Configuration

**agentic-workflows-v2:**
```toml
asyncio_mode = "auto"         # Auto-detect async tests
markers = ["integration", "slow", "security"]
fail_under = 80               # In pyproject.toml
```

**CI override:** `--cov-fail-under=60` (significantly lower than the 80% pyproject.toml target)

**agentic-v2-eval:**
```toml
asyncio_mode = "auto"
markers = ["integration", "slow"]
fail_under = 80
```

### Test Patterns — Quality Assessment

**Strengths:**
- Tests follow **Arrange-Act-Assert** pattern consistently
- Good use of `pytest.fixture` for setup (conftest.py has 5 shared fixtures)
- Tests are **class-organized** by feature (e.g., `TestDAGExecutorBasic`, `TestBM25Index`)
- Each test has a **descriptive docstring** explaining expected behavior
- Proper use of `pytest.raises()` for error path testing
- Mock usage is appropriate — `AsyncMock`, `MagicMock(spec=...)` with spec enforcement
- Helper factories like `make_step()`, `_make_chunk()` keep tests DRY

**Weaknesses:**
- Only 1 `@pytest.mark.skipif` found — no `@pytest.mark.slow`, `@pytest.mark.integration`, or `@pytest.mark.security` markers used despite being declared
- Tests are all flat in one directory (no subdirectory organization like `tests/unit/`, `tests/integration/`)
- Some test files are large: `test_langchain_engine.py` (1,150 lines), `test_engine.py` (901 lines), `test_server_evaluation.py` (848 lines)
- autouse fixture `_reset_llm_client` in conftest.py — any test that needs a real client must explicitly override (documented but could be fragile)
- No visible parametrize usage in sampled tests (though may exist in files not sampled)

### Coverage

- **Configured target:** 80% (pyproject.toml)
- **CI gate:** 60% (ci.yml) — **inconsistency reduces the guardrail**
- **RAG module coverage:** ~92% (excellent, per memory context)
- **Branch coverage:** Enabled (`branch = true`)
- Coverage excludes: `TYPE_CHECKING` blocks, `__name__` guards, `NotImplementedError` raises — reasonable pragmatic exclusions

---

## 4. Dependency Health

### Pinning Strategy

**agentic-workflows-v2 (GOOD — compatible range pinning):**
```
pydantic>=2.0,<3
httpx>=0.25,<1
jinja2>=3.0,<4
pyyaml>=6.0,<7
```
Upper bounds prevent major-version breaks. This is the recommended strategy for libraries.

**agentic-v2-eval (LOOSE — floor-only):**
```
pyyaml>=6.0       # No upper bound
pytest>=7.0        # No upper bound
```

**Root tools package (LOOSE — floor-only):**
```
pyyaml>=6.0
aiohttp>=3.9
pydantic>=2.0
```

**Frontend (LOOSE — caret ranges):**
```json
"react": "^19.0.0"
"@xyflow/react": "^12.4.0"
```
Standard for npm/JS ecosystem. Acceptable.

### Dependency Concerns

| Concern | Package | Severity |
|---------|---------|----------|
| No lockfile for Python packages | All packages | MEDIUM — No `requirements.lock` or `uv.lock` for reproducible installs |
| `setuptools>=61.0` in root (no upper bound) | tools/ | LOW |
| LangChain ecosystem pinned to minor ranges | agentic-workflows-v2 | OK — LangChain has fast-moving breaking changes, tight pins are correct |
| `actions/setup-python@v4` in CI | .github/workflows/ci.yml | LOW — v5 available |
| No `npm ci` in CI for frontend | Missing | MEDIUM — `npm install` may not use lockfile |

### Optional Dependency Groups

agentic-workflows-v2 has 6 well-organized groups:
- `dev`: Testing + linting
- `server`: FastAPI + uvicorn
- `langchain`: Full LangGraph stack
- `tracing`: OpenTelemetry
- `claude`: Anthropic SDK
- `rag`: LanceDB + LiteLLM

This modular approach keeps the base install lightweight. Well-designed.

---

## 5. Error Handling Evaluation

### Exception Hierarchies

**agentic-workflows-v2 (`core/errors.py`):**
```
AgenticError (base)
├── WorkflowError
├── StepError
├── SchemaValidationError
├── AdapterError
│   └── AdapterNotFoundError
├── ToolError
├── MemoryStoreError
└── ConfigurationError
```

**RAG subsystem (`rag/errors.py`):**
```
RAGError (AgenticError)
├── IngestionError
├── ChunkingError
├── EmbeddingError
├── VectorStoreError
└── RetrievalError
```

**tools/ (`core/errors.py`):**
```
ErrorCode (str, Enum) — classification, not exceptions
LLMClientError (RuntimeError) — in llm_client.py, does NOT inherit from AgenticError
```

### Assessment

**Strengths:**
- Domain-specific exceptions with clear inheritance
- RAG errors properly chain to the core hierarchy
- `classify_error()` function provides heuristic error classification with retry recommendations
- No bare `except:` anywhere

**Weaknesses:**
- `tools/LLMClientError` inherits from `RuntimeError`, not `AgenticError` — cross-package error handling requires catching both hierarchies
- 144 `except Exception` occurrences in agentic_v2 — while mostly appropriate for infrastructure boundaries, some could be narrowed (e.g., catching `httpx.HTTPError` instead of `Exception` in backends)
- `tools/__init__.py` uses `except Exception` for optional import — should be `except ImportError`

### print() vs logging

**agentic-workflows-v2:**
- `cli/main.py`: 51 `print()` calls — all via `console.print()` (Rich library), appropriate for CLI output
- `tools/registry.py`: 1 print call
- `code_execution.py`: 2 print calls (in sandboxed execution output capture)
- `claude_sdk_agent.py`: 1 print call
- **40 modules use `logging.getLogger(__name__)`** — excellent logging discipline

**tools/ package:**
- **365 `print()` calls across 28 files** — significant deviation from the "no print()" standard
- Heaviest offenders: `runner.py` (63), `model_probe.py` (43), `runner_ui.py` (39), `tool_init.py` (32)
- These are CLI/interactive tools where `print()` is partially justified, but `rich.console` or `logging` would be more consistent

---

## 6. Code Metrics

### File Size Analysis

**Files exceeding 800-line target:**

| File | Lines | Package | Notes |
|------|-------|---------|-------|
| `server/routes/workflows.py` | 1,330 | agentic_v2 | Largest — route handlers + evaluation scoring |
| `server/evaluation_scoring.py` | 1,160 | agentic_v2 | Scoring logic |
| `engine/agent_resolver.py` | 994 | agentic_v2 | Agent resolution with many backends |
| `server/datasets.py` | 950 | agentic_v2 | Dataset management |
| `agents/base.py` | 860 | agentic_v2 | Base agent with capabilities |
| `models/backends.py` | 826 | agentic_v2 | 6+ LLM backend implementations |
| `langchain/models.py` | 818 | agentic_v2 | LangChain model wrappers |
| `llm/model_probe.py` | 2,360 | tools | Model probing + caching |
| `llm/local_model.py` | 846 | tools | ONNX runtime inference |

**9 files exceed 800 lines** (6 in agentic_v2, 3 in tools). The `model_probe.py` at 2,360 lines is nearly 3x the maximum.

### Function Length

Sampled modules show generally good function sizes:
- `DAGExecutor.execute()` — well-documented but spans ~100 lines (above 50-line target)
- Most RAG module functions are < 30 lines
- CLI command functions are 30-60 lines each (slightly over target due to Rich output formatting)

### Import Organization

- `from __future__ import annotations` used consistently in agentic_v2 (99/99 files)
- Missing in 28/42 tools/ files
- isort with black profile ensures consistent ordering
- `TYPE_CHECKING` guards used properly in RAG modules for circular import prevention

### `__init__.py` Barrel File

`agentic_v2/__init__.py` exports **80+ symbols** across 218 lines. While this provides a convenient public API surface, it:
- Creates tight coupling to internal module structure
- Makes it harder to identify which symbols are truly public
- Any internal rename requires updating the barrel

---

## 7. CI/CD Quality Gates

### Current Pipeline (ci.yml)

```
checkout → setup Python 3.11 → install deps → pip check → pre-commit → pytest (cov ≥ 60%) → check docs → build docs (optional)
```

### Gaps

| Gap | Impact |
|-----|--------|
| Coverage gate is 60% in CI vs 80% in pyproject.toml | Tests could regress to 60% without failing CI |
| No CI for `agentic-v2-eval` tests | Eval package regressions go undetected |
| No CI for `tools/` tests | Shared utility regressions go undetected |
| No frontend CI (no `npm test` step) | UI regressions go undetected |
| `sphinx-build` failure is swallowed (`|| true`) | Broken docs never fail the build |
| No dependency security scanning in main CI | `dependency-review.yml` exists but runs separately |
| `actions/setup-python@v4` — v5 available | Minor (v4 still maintained) |

---

## 8. Recommendations

| # | Recommendation | Impact (1-5) | Effort (S/M/L) | Priority |
|---|---------------|:---:|:---:|:---:|
| 1 | **Add `[tool.ruff.lint]` to agentic-workflows-v2 pyproject.toml** with the full rule set from CLAUDE.md (`E, F, W, I, N, UP, S, B, A, C4, SIM, TCH, RUF`). Currently relying on pre-commit defaults which only enforce E+F. | 5 | S | P0 |
| 2 | **Align CI coverage threshold** — change `--cov-fail-under=60` in ci.yml to match the 80% target in pyproject.toml, or set a realistic intermediate (e.g., 70%) and document the plan to reach 80%. | 4 | S | P0 |
| 3 | **Add `[tool.mypy]` to agentic-workflows-v2 pyproject.toml** with at minimum `disallow_untyped_defs = true` and `warn_return_any = true` to match eval package strictness. | 4 | M | P1 |
| 4 | **Modernize tools/ package** — add `from __future__ import annotations` to all 28 files, replace legacy `typing` imports (`Dict`/`List`/`Tuple`/`Set`/`Optional`) with built-in generics and `X | None`. | 3 | M | P1 |
| 5 | **Replace print() in tools/ with logging** — convert 365 print() calls across 28 files to use `logging` or `rich.console`. Start with the heaviest offenders: `runner.py`, `model_probe.py`, `runner_ui.py`. | 3 | M | P1 |
| 6 | **Split oversized files** — especially `server/routes/workflows.py` (1,330), `server/evaluation_scoring.py` (1,160), and `tools/llm/model_probe.py` (2,360). Extract related concerns into submodules. | 3 | L | P2 |
| 7 | **Add CI jobs for eval and tools tests** — `agentic-v2-eval/` and `tools/` both have test suites that are not run in CI. Add matrix jobs. | 4 | S | P1 |
| 8 | **Add frontend CI step** — add `npm ci && npm test` to ci.yml or create a separate frontend workflow. | 3 | S | P1 |
| 9 | **Narrow `except Exception` in backends** — audit `models/backends.py` and `langchain/*.py` to catch specific HTTP/provider exceptions where possible instead of blanket `Exception`. | 2 | M | P2 |
| 10 | **Unify error hierarchies** — make `tools/LLMClientError` inherit from `AgenticError` or create a shared base exception for cross-package error handling. | 2 | S | P2 |
| 11 | **Use test markers** — the `@pytest.mark.integration`, `@pytest.mark.slow`, `@pytest.mark.security` markers are declared but unused. Tag appropriate tests to enable selective test runs (e.g., fast CI vs full nightly). | 2 | M | P2 |
| 12 | **Create Python lockfiles** — add `uv.lock` or `pip-compile` output for reproducible CI and production installs. | 3 | M | P2 |
| 13 | **Reconcile ruff line-length** — agentic-v2-eval uses `line-length = 100` while black enforces 88. These should be aligned. | 2 | S | P2 |
| 14 | **Slim `__init__.py` barrel** — consider splitting agentic_v2's 80+ symbol re-exports into logical sub-namespaces or documenting which symbols are the stable public API. | 2 | M | P3 |

---

## Appendix: Raw Metrics

### Source Lines of Code

| Package | Files | Lines (approx) |
|---------|-------|----------------|
| agentic-workflows-v2/agentic_v2/ | 123 | ~33,500 |
| agentic-workflows-v2/tests/ | 68 | ~20,200 |
| agentic-v2-eval/ | ~20 | ~7,000 |
| tools/ | 42 | ~14,000 |
| **Total Python** | **~253** | **~74,700** |

### Test-to-Source Ratio

- agentic_v2: 20,200 test lines / 33,500 source lines = **0.60** (adequate)
- Eval and tools packages: test lines not counted precisely but visibly lower

### Logging vs Print Adoption

| Package | logging.getLogger usage | print() calls |
|---------|------------------------|---------------|
| agentic_v2 | 40 modules | 55 (mostly Rich console) |
| tools/ | Few | 365 |
| agentic-v2-eval | Few | Not measured |
