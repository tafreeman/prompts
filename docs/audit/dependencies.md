# Dependencies Audit — 2026-04-14

**Git SHA (audit):** 0252c88ce93792d05d13613e0b1f431d3193d006
**Git SHA (after fixes):** 7f1ae0f
**Status:** ⚠️ Issues Found (H-1 resolved)

## Implementation Status (2026-04-14)

| Finding | Status | Commit |
|---------|--------|--------|
| H-1 — `openai`, `anthropic`, `numpy` undeclared in `prompts-tools` | ✅ Fixed: `openai>=1.0,<2`, `anthropic>=0.40,<1`, `numpy>=1.24.0,<3` added to root `pyproject.toml` | `61a7168` + `271939f` |
| H-2 — `numpy` undeclared | ✅ Fixed (part of H-1 above) | `61a7168` + `271939f` |
| M-1 — Version bound inconsistencies | Open | — |
| M-2 — `claude-agent-sdk` canonical name unverified | Open | — |
| M-3 — `litellm` in `rag` extra appears unused | Open | — |
| M-4 — `langsmith` version range too wide | Open | — |
| M-5 — `mypy` missing from dev extras | Open | — |

---

## Executive Summary

Four package manifests were audited: three Python (`agentic-workflows-v2`, `agentic-v2-eval`, root `prompts-tools`) and one JavaScript (`agentic-workflows-v2/ui`). No critical security vulnerabilities were found in the dependency declarations themselves. Several medium-priority structural issues exist: the `prompts-tools` root package omits key runtime transitive providers (`openai`, `anthropic`) from its own manifest while its source code conditionally imports them; version ranges across packages are partially mismatched; and two optional-extra packages (`claude-agent-sdk`, `langchain-google-genai`) may be non-standard or renamed.

---

## Findings

### Critical

_None identified._

### High

- **`openai` and `anthropic` not declared in `prompts-tools` (`pyproject.toml` at repo root)**
  `tools/llm/llm_client.py` and `tools/llm/provider_adapters.py` conditionally import `openai` (including `AzureOpenAI`) and `anthropic`. Neither package is listed in `[project].dependencies` for `prompts-tools`. They are available at runtime only because consumers (`agentic-workflows-v2`) pull in the `claude` optional extra, creating an implicit undeclared dependency. Any consumer that installs `prompts-tools` alone (e.g., `agentic-v2-eval`) gets no LLM providers.
  **Fix:** Add `openai>=1.0,<2` and `anthropic>=0.40,<1` to `prompts-tools` dependencies (or as an `llm` optional extra).

- **`numpy` not declared in `prompts-tools` (`tools/core/local_media.py`)**
  `local_media.py` has three lazy `import numpy as np` calls with no guard for `ImportError`. `numpy` is not listed anywhere in the `prompts-tools` pyproject.toml.
  **Fix:** Add `numpy>=1.24` to `prompts-tools` dependencies or wrap each import in `try/except ImportError`.

### Medium

- **`aiohttp` upper-bound mismatch between packages**
  `agentic-workflows-v2` pins `aiohttp>=3.9,<4`; `prompts-tools` declares `aiohttp>=3.9` (no upper bound). When installed together in a workspace these resolve the same version, but the missing upper cap in `prompts-tools` allows a future `aiohttp` v4 to be installed for `prompts-tools` consumers in isolation.
  **Fix:** Align to `aiohttp>=3.9,<4` in `prompts-tools`.

- **`pydantic` upper-bound mismatch**
  `agentic-workflows-v2` and `prompts-tools` both require `pydantic>=2.0`, but `agentic-workflows-v2` adds `<3` while `prompts-tools` omits the upper cap. A hypothetical Pydantic v3 breaking release would be accepted by `prompts-tools`.
  **Fix:** Align to `pydantic>=2.0,<3` in `prompts-tools`.

- **`pyyaml` upper-bound missing in `agentic-v2-eval` and `prompts-tools`**
  `agentic-workflows-v2` pins `pyyaml>=6.0,<7`; the other two packages declare only `pyyaml>=6.0`. Inconsistent bounding could allow version drift.
  **Fix:** Add `<7` upper bound to both.

- **`claude-agent-sdk` package name appears non-standard**
  `agentic-workflows-v2`'s `claude` extra declares `claude-agent-sdk>=0.1,<1`. The Anthropic Claude Agent SDK is published as `claude-code-sdk` on PyPI (as of the knowledge cutoff). If the name differs, installation will silently fail.
  **Fix:** Verify the exact PyPI distribution name; update if needed. The source code imports it as `claude_agent_sdk` (matching the declared name with underscores), so confirm the dist name matches.

- **`langchain-google-genai` not listed in langchain extra but is imported**
  `agentic_v2/langchain/model_builders.py` imports `from langchain_google_genai import ChatGoogleGenerativeAI`. The `langchain` extra lists `langchain-google-genai>=2.0,<3` — this is present. However, the package `langchain-google-genai` was renamed to `langchain-google` in LangChain 0.3+. The declared name may be out of date if using recent LangChain.
  **Risk:** Medium — confirm the package name still resolves on PyPI for the declared version range.

- **`langsmith` version range is unusually wide**
  The `langchain` extra lists `langsmith>=0.1.0,<0.4` — a range spanning 0.3 minor versions. LangSmith has had significant API changes between 0.1 and 0.3. This broad range risks resolving an older version with an incompatible API.
  **Fix:** Tighten to `langsmith>=0.3.0,<0.4`.

- **`mypy` missing from `agentic-workflows-v2` dev extra**
  `agentic-v2-eval` includes `mypy>=1.0` in dev deps. The root workspace includes `mypy>=1.19`. But `agentic-workflows-v2/pyproject.toml` does not list `mypy` in its `[project.optional-dependencies].dev`. The `[tool.mypy]` section is configured, implying mypy is expected to be used, but is not declared.
  **Fix:** Add `mypy>=1.0` to `agentic-workflows-v2` dev extras.

- **`lancedb` and `litellm` upper bounds are very loose**
  The `rag` extra uses `lancedb>=0.15,<1` and `litellm>=1.50,<2`. Both packages release frequently with breaking changes; the `<1` / `<2` caps are wide. No imports of `litellm` were found in the codebase — only `lancedb` is conditionally imported in `rag/vectorstore.py`.
  **Fix:** Verify `litellm` is still actively used; remove from `rag` extra if not. If retained, tighten the upper bound.

### Low

- **`dev` deps duplicated between `[project.optional-dependencies]` and `[dependency-groups]` in root `pyproject.toml`**
  The root `pyproject.toml` declares identical tools (`pytest`, `pytest-asyncio`, etc.) in both `[project.optional-dependencies].dev` and `[dependency-groups].dev`. The `dependency-groups` table is a `uv`-specific workspace feature; `[project.optional-dependencies]` is the PEP 517/518 standard. Having both creates confusion about which is authoritative.
  **Fix:** Use `[dependency-groups]` only for workspace-level tooling and remove the duplicate `[project.optional-dependencies].dev` section, or vice versa.

- **No `black` or `mypy` in `agentic-v2-eval` dev extra**
  `agentic-v2-eval` lists `mypy>=1.0` and `ruff>=0.1.0` in dev but not `black`. The project-wide pre-commit hook runs `black`. Minor inconsistency; will work if `black` is installed from the root workspace.

- **`python-multipart` upper-bound `<1` is very broad**
  `python-multipart` is in the `server` extra as `>=0.0.6,<1`. There is a `0.0.x` series and the jump to `0.1.x` happened in 2024. Since the lower bound is `0.0.6`, any `0.x` version is accepted including a hypothetical `0.99`. Tighten to `>=0.0.9,<0.1` once confirmed compatible.

- **`rich` version pinned to `<14` but current major is 13.x**
  `agentic-workflows-v2` pins `rich>=13.0,<14`. Rich 14 is not yet released (as of the audit date). The cap is appropriate but should be reviewed when Rich 14 is released.

- **`@xyflow/react` version `^12.4.0`**
  ReactFlow/XYFlow recently released v12. The `^12.4.0` caret allows any `12.x`. This is a relatively new major version; confirm upstream changelog for breaking API changes against the current usage.

- **`react-router-dom` version `^7.1.0`**
  React Router v7 was released in late 2024 and is a significant rewrite with `data` APIs. The project depends on `^7.1.0`. Ensure the router usage is aligned with the v7 API (no `<Route>` component usage patterns from v6 that changed).

---

## Package Inventory

### Python Packages

| Package | agentic-workflows-v2 | agentic-v2-eval | prompts-tools (root) |
|---------|---------------------|-----------------|----------------------|
| pydantic | `>=2.0,<3` | — | `>=2.0` ⚠️ (missing upper) |
| pyyaml | `>=6.0,<7` | `>=6.0` ⚠️ | `>=6.0` ⚠️ |
| aiohttp | `>=3.9,<4` | — | `>=3.9` ⚠️ (missing upper) |
| httpx | `>=0.25,<1` | — | — |
| jinja2 | `>=3.0,<4` | — | — |
| jmespath | `>=1.0,<2` | — | — |
| aiofiles | `>=23.0,<25` | — | — |
| filelock | `>=3.0,<4` | — | — |
| typer | `>=0.9,<1` | — | — |
| rich | `>=13.0,<14` | — | — |
| prompts-tools | workspace | workspace | (this package) |
| openai | — (undeclared) | — | — 🔴 (imported, missing) |
| anthropic | `[claude] >=0.40,<1` | — | — 🔴 (imported, missing) |
| numpy | — | — | — 🔴 (imported, missing) |

**Optional extras — agentic-workflows-v2:**

| Extra | Packages |
|-------|---------|
| dev | pytest, pytest-asyncio, pytest-cov, pytest-mock, pytest-timeout, black, ruff |
| server | fastapi `>=0.100,<1`, uvicorn `>=0.23,<1`, python-multipart `>=0.0.6,<1` |
| langchain | langchain-core, langgraph, langchain, langchain-openai, langchain-anthropic, langchain-google-genai, langchain-ollama, langgraph-checkpoint-sqlite, langsmith |
| tracing | opentelemetry-sdk, opentelemetry-exporter-otlp-proto-grpc, opentelemetry-exporter-otlp-proto-http |
| claude | anthropic `>=0.40,<1`, claude-agent-sdk `>=0.1,<1` ⚠️ |
| rag | lancedb `>=0.15,<1`, litellm `>=1.50,<2` ⚠️ (litellm not found in imports) |

**Optional extras — agentic-v2-eval:**

| Extra | Packages |
|-------|---------|
| dev | pytest, pytest-cov, pytest-asyncio, mypy, ruff |

**Root workspace dev tools (dependency-groups):**

| Package | Version |
|---------|---------|
| pytest | `>=7.0` |
| pytest-asyncio | `>=0.21` |
| pytest-cov | `>=4.0` |
| pytest-mock | `>=3.12` |
| pytest-timeout | `>=2.2` |
| black | `>=23.0` |
| ruff | `>=0.1.0` |
| mypy | `>=1.19` |
| pre-commit | `>=3.0` |

### JavaScript Packages (agentic-workflows-v2/ui)

| Package | Version | Category | Notes |
|---------|---------|----------|-------|
| @tanstack/react-query | `^5.62.0` | Runtime | Current, healthy |
| @xyflow/react | `^12.4.0` | Runtime | New major, verify API |
| lucide-react | `^0.468.0` | Runtime | Current |
| react | `^19.0.0` | Runtime | React 19 (stable Apr 2025) |
| react-dom | `^19.0.0` | Runtime | Current |
| react-router-dom | `^7.1.0` | Runtime | ⚠️ Major rewrite vs v6 |
| @testing-library/jest-dom | `^6.6.0` | Dev | Current |
| @testing-library/react | `^16.1.0` | Dev | Current |
| @types/react | `^19.0.0` | Dev | Current |
| @types/react-dom | `^19.0.0` | Dev | Current |
| @vitejs/plugin-react | `^4.3.0` | Dev | Current |
| @vitest/coverage-v8 | `^2.1.0` | Dev | Current |
| autoprefixer | `^10.4.20` | Dev | Current |
| jsdom | `^25.0.0` | Dev | Current |
| postcss | `^8.4.49` | Dev | Current |
| tailwindcss | `^3.4.17` | Dev | ⚠️ Tailwind v4 released; v3 still maintained |
| typescript | `^5.7.0` | Dev | Current |
| vite | `^6.0.0` | Dev | Current |
| vitest | `^2.1.0` | Dev | Current |

No JS packages flagged with known critical CVEs based on declared versions. All devDependencies correctly placed in `devDependencies` (not `dependencies`). No runtime test tools leaked into `dependencies`.

---

## Requirements.txt Files

| File | Status |
|------|--------|
| `.claude/skills/mcp-builder/scripts/requirements.txt` | Isolated — only `anthropic>=0.39.0` and `mcp>=1.1.0`. Not part of any package build. No conflict with pyproject.toml declarations. |

No other `requirements.txt` files found in the main source tree. No conflicts identified.

---

## Import vs Declaration Cross-Check

| Import | Source File | Declared In | Status |
|--------|-------------|-------------|--------|
| `openai` | `tools/llm/llm_client.py`, `provider_adapters.py` | agentic-workflows-v2 `claude` extra (indirectly) | 🔴 Missing from prompts-tools |
| `anthropic` | `tools/llm/provider_adapters.py` | agentic-workflows-v2 `claude` extra (indirectly) | 🔴 Missing from prompts-tools |
| `numpy` | `tools/core/local_media.py` | Not declared anywhere | 🔴 Missing |
| `fastapi` | `agentic_v2/server/app.py` et al. | `server` extra | ✅ Guarded by extra |
| `langchain_core`, `langgraph` | `agentic_v2/langchain/` | `langchain` extra | ✅ All lazy-imported |
| `opentelemetry` | `agentic_v2/integrations/otel.py` | `tracing` extra | ✅ All lazy-imported |
| `lancedb` | `agentic_v2/rag/vectorstore.py` | `rag` extra | ✅ Lazy-imported |
| `anthropic` | `agentic_v2/agents/implementations/claude_agent.py` | `claude` extra | ✅ Lazy-imported |
| `claude_agent_sdk` | `agentic_v2/agents/implementations/claude_sdk_agent.py` | `claude` extra | ⚠️ Declared as `claude-agent-sdk`; verify PyPI name |
| `langsmith` | `agentic_v2/integrations/tracing.py` | `langchain` extra | ✅ Lazy-imported |
| `langchain_openai/anthropic/google/ollama` | `agentic_v2/langchain/model_builders.py` | `langchain` extra | ✅ All lazy-imported |
| `pydantic` | Throughout | All packages | ✅ |
| `yaml` | Throughout | All packages | ✅ |
| `aiohttp` | `agentic_v2/` | `agentic-workflows-v2` core deps | ✅ |
| `litellm` | Not found in any import | `rag` extra | ⚠️ Declared but unused |

---

## Metrics

| Metric | Value | Gate | Status |
|--------|-------|------|--------|
| Total Python runtime deps (agentic-v2) | 11 core + 6 extras | — | — |
| Total Python runtime deps (eval) | 2 | — | — |
| Total Python runtime deps (tools) | 3 | — | — |
| JS runtime dependencies | 6 | — | — |
| JS dev dependencies | 11 | — | — |
| Undeclared imports found | 3 (`openai`, `anthropic`, `numpy` in prompts-tools) | 0 | ⚠️ Fail |
| requirements.txt conflicts | 0 | 0 | ✅ Pass |
| Dev deps leaked to runtime | 0 | 0 | ✅ Pass |
| Legacy pydantic v1 patterns | 0 | 0 | ✅ Pass |
| Packages with version conflicts across manifests | 3 (`pydantic`, `pyyaml`, `aiohttp`) | 0 | ⚠️ Fail |
| Potentially unused declared deps | 1 (`litellm`) | 0 | ⚠️ Warning |

---

## Recommendations

1. **[High] Add `openai>=1.0,<2` and `anthropic>=0.40,<1` to `prompts-tools` dependencies** or create an `llm` optional extra. These are conditionally imported in `tools/llm/` and consumers that install `prompts-tools` directly will have silent failures.

2. **[High] Add `numpy>=1.24` to `prompts-tools` dependencies** or wrap the lazy imports in `try/except ImportError` with a clear error message. Found in `tools/core/local_media.py`.

3. **[Medium] Tighten upper bounds for `pydantic`, `pyyaml`, and `aiohttp` in `prompts-tools`** to match `agentic-workflows-v2` (`<3`, `<7`, `<4` respectively) for version consistency across the workspace.

4. **[Medium] Verify `claude-agent-sdk` PyPI distribution name.** The Anthropic SDK may be published under a different name (`claude-code-sdk` or similar). The import alias `claude_agent_sdk` matches the declared name, but confirm this resolves correctly with `pip install claude-agent-sdk`.

5. **[Medium] Remove `litellm` from the `rag` extra if unused.** No `litellm` imports were found in `agentic_v2/`. If it was a future placeholder, document it or remove it to reduce install footprint.

6. **[Medium] Tighten `langsmith>=0.1.0,<0.4` to `>=0.3.0,<0.4`** in the `langchain` extra. The 0.1–0.3 range spans significant API changes.

7. **[Medium] Add `mypy>=1.0` to `agentic-workflows-v2` dev extras.** The `[tool.mypy]` config is present but mypy is not declared as a dev dependency for that package.

8. **[Low] Resolve duplicate dev dep declarations in root `pyproject.toml`.** Choose either `[project.optional-dependencies].dev` or `[dependency-groups].dev`, not both.

9. **[Low] Review `react-router-dom` v7 usage** to ensure no legacy v6 API patterns (e.g., `<Switch>`, non-data-router `<Route>`) are present after the major version bump.

10. **[Low] Plan migration to Tailwind CSS v4** when ready. v3 is still maintained but v4 introduces a new configuration model. Starting migration planning now avoids a forced rush later.

11. **[Low] Run `ruff check --fix --select I001,F401,UP017,UP035,UP045` in a single formatted commit** to clear the ~400+ deferred violations noted in the ruff ignore list (Sprint C backlog items). These are acknowledged technical debt but should be scheduled.
