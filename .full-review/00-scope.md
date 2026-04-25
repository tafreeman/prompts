# Review Scope

## Target

Comprehensive review of the `tafreeman/prompts` monorepo at `C:\Users\tandf\source\prompts` on branch `main`. This is a multi-agent workflow runtime + evaluation framework + shared LLM utilities, plus a React 19 dashboard.

## Deployment Context (IMPORTANT)

**Local-only, developer-workstation use. Educational/learning platform for a team — not deployed to production, not exposed beyond localhost, not multi-tenant.**

Implications for findings:

- **In scope:** correctness, agent/tool safety (because LLM-driven agents execute shell, code, and file tools on the developer's own machine — prompt injection can still cause local damage/data exposure), test coverage, code quality, docs for contributors and learners, concurrency correctness.
- **Out of scope / de-prioritized:** default-open auth hardening, CORS/HSTS/CSP for production, SSE auth for enterprise, multi-worker horizontal scaling, operations runbooks, incident response, federal-compliance docs, data-retention compliance. These may be noted but are not priority blockers.

## Files

Primary source directories under review:

- `agentic-workflows-v2/agentic_v2/` — main runtime (~192 Python files; agents, adapters, core, engine, langchain, models, rag, contracts, prompts, server, tools/builtin, workflows)
- `agentic-workflows-v2/tests/` — 100+ test files (pytest-asyncio auto mode)
- `agentic-workflows-v2/ui/` — React 19 + Vite 6 + @xyflow/react + TanStack Query + Tailwind dashboard
- `agentic-v2-eval/` — evaluation framework (~41 Python files; rubrics, evaluators, runners, reporters)
- `tools/` (prompts-tools) — shared LLM client, benchmarks, caching, utilities (~64 Python files)
- `docs/` — ARCHITECTURE.md, CODING_STANDARDS.md, ADRs (docs/adr/)
- Root configuration: `pyproject.toml`, `Dockerfile`, `Dockerfile.ui`, `docker-compose.yml`, `.pre-commit-config.yaml`, `package.json`, `uv.lock`

Excluded from review:

- `.venv/`, `node_modules/`, `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/` — dependency/cache artifacts
- `_analysis/`, `_bmad/`, `_bmad-output/`, `planning-artifacts/`, `decks-generated/`, `reports/`, `runs/`, `output/` — generated outputs and scratch
- `presentation/` — extracted to separate repo (per CLAUDE.md note)
- `.env` — blocked by env-protect.sh; never read

## Flags

- Security Focus: no (not explicitly set; standard OWASP coverage)
- Performance Critical: no (not explicitly set; standard perf review)
- Strict Mode: no
- Framework: auto-detect (Python 3.11 backend with FastAPI/Pydantic v2/LangGraph; React 19 + Vite 6 frontend)

## Review Phases

1. Code Quality & Architecture
2. Security & Performance
3. Testing & Documentation
4. Best Practices & Standards
5. Consolidated Report

## Repo Facts

- Python 3.11+, hatchling builds, pre-commit runs black/isort/ruff/docformatter/mypy/pydocstyle/detect-secrets
- Test markers: `integration`, `slow`, `security`; `asyncio_mode=auto`
- 8+ LLM providers via `smart_router` (OpenAI, Anthropic, Gemini, Azure OpenAI, Azure Foundry, GitHub Models, Ollama, local ONNX)
- Adapter registry with two execution engines: `native` (DAG Kahn's algorithm) and `langchain` (LangGraph state machines)
- Pydantic v2 contracts (additive-only)
- Recent work: Sprint B stabilization, `AGENTIC_NO_LLM=1` placeholder mode, Pydantic↔TS wire-format drift gate
