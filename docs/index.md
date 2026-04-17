# Project Documentation Index

> **Generated:** 2026-04-16 | **Scan Mode:** initial_scan (exhaustive) | **Workflow Version:** 1.2.0

---

## Project Overview

- **Repository:** tafreeman/prompts
- **Type:** Monorepo (uv workspace) with 4 parts
- **Primary Language:** Python 3.11+ / TypeScript 5.7
- **Architecture:** Dual execution engine (native DAG + LangGraph), protocol-based, FastAPI + React 19

### Quick Reference by Part

#### Runtime — `agentic-workflows-v2/` (backend)

- **Tech Stack:** Python 3.11, FastAPI, Pydantic v2, Typer CLI, httpx/aiohttp
- **Engines:** Native DAG (Kahn's algorithm) + LangGraph state machines
- **Providers:** 8+ LLM providers (OpenAI, Anthropic, Gemini, Azure, GitHub Models, Ollama, local ONNX, Windows AI)
- **Root:** `agentic-workflows-v2/`

#### UI — `agentic-workflows-v2/ui/` (web)

- **Tech Stack:** React 19, Vite 6, TypeScript 5.7, TanStack Query 5, @xyflow/react 12, Tailwind CSS 3.4
- **Root:** `agentic-workflows-v2/ui/`

#### Eval — `agentic-v2-eval/` (library)

- **Tech Stack:** Python 3.11, PyYAML, 8 rubrics, 4 evaluator types, batch/streaming runners
- **Root:** `agentic-v2-eval/`

#### Tools — `tools/` (library, package: prompts-tools)

- **Tech Stack:** Python 3.11, OpenAI/Anthropic SDKs, Pydantic, NumPy, aiohttp
- **Role:** Shared LLM client (10 providers), benchmarks, caching, error taxonomy
- **Root:** `tools/` (workspace root)

---

## Generated Documentation

### Project-Wide

- [Project Overview](./project-overview.md) — Purpose, tech stack summary, architecture type, links to all docs
- [Source Tree Analysis](./source-tree-analysis.md) — Full annotated directory tree with entry points and integration points
- [Integration Architecture](./integration-architecture.md) — How the 4 parts communicate (REST, WebSocket, SSE, imports)
- [Development Guide](./development-guide.md) — Prerequisites, installation, dev servers, testing, CLI, common issues
- [Deployment Guide](./deployment-guide.md) — CI/CD pipeline (8 jobs), security scanning, environment variables, production checklist
- [Contribution Guide](./contribution-guide.md) — Code style, git workflow, testing requirements, security checklist, PR process

### Runtime (Backend)

- [Architecture — Runtime](./architecture-runtime.md) — Dual-engine architecture, server layers, agents, models, RAG, security
- [API Contracts — Runtime](./api-contracts-runtime.md) — 16 REST endpoints + WebSocket + SSE, auth model, request/response schemas
- [Data Models — Runtime](./data-models-runtime.md) — 38+ Pydantic v2 models across server, contracts, core (messages, schemas, sanitization, verification, memory, errors)

### UI (Frontend)

- [Architecture — UI](./architecture-ui.md) — React 19 SPA, TanStack Query, routing, design system, WebSocket streaming
- [Component Inventory — UI](./component-inventory-ui.md) — 17 components across 6 categories (layout, common, DAG, runs, live, pages)

### Evaluation Framework

- [Architecture — Eval](./architecture-eval.md) — Rubric-driven evaluation, 4 evaluator types, scoring engine, runners, reporters, sandbox

### Shared Tools

- [Architecture — Tools](./architecture-tools.md) — Multi-provider LLM client, response caching, model probing, benchmarks, error taxonomy

---

## Existing Documentation

### Architecture Decision Records

- [ADR-001/002/003 — Architecture Decisions](./adr/ADR-001-002-003-architecture-decisions.md) — Foundational architecture choices
- [ADR-007 — Classification Matrix Stop Policy](./adr/ADR-007-classification-matrix-stop-policy.md)
- [ADR-008 — Testing Approach Overhaul](./adr/ADR-008-testing-approach-overhaul.md)
- [ADR-009 — Scoring Enhancements](./adr/ADR-009-scoring-enhancements.md)
- [ADR-010 — Eval Harness Methodology](./adr/ADR-010-eval-harness-methodology.md)
- [ADR-011 — Eval Harness API Interface](./adr/ADR-011-eval-harness-api-interface.md)
- [ADR-012 — UI Evaluation Hub](./adr/ADR-012-ui-evaluation-hub.md)
- [ADR Index](./adr/ADR-INDEX.md) — Master index of all ADRs
- [ADR Compiled](./adr/ADR_COMPILED.md) — All ADRs in single document
- [ADR Implementation Audit](./adr/ADR_IMPLEMENTATION_AUDIT.md)
- [ADR Research Justifications](./adr/ADR_RESEARCH_JUSTIFICATIONS.md)
- [RAG Pipeline Blueprint](./adr/RAG-pipeline-blueprint.md)

### Reference Documents

- [Architecture (Legacy)](./ARCHITECTURE.md) — Original architecture document
- [Coding Standards](./CODING_STANDARDS.md) — Detailed coding standards reference
- [Workflow Authoring](./WORKFLOW_AUTHORING.md) — YAML workflow definition guide
- [Pattern Catalog](./PATTERN_CATALOG.md) — Agentic pattern reference
- [Glossary](./GLOSSARY.md) — Term definitions
- [Onboarding](./ONBOARDING.md) — Team onboarding guide
- [Test Coverage Analysis](./TEST_COVERAGE_ANALYSIS.md) — Coverage audit
- [Context Engineering Audit](./CONTEXT_ENGINEERING_AUDIT.md)
- [GitHub Repo Technical Audit](./GitHub_Repo_Technical_Audit.md)
- [Implementation Roadmap](./IMPLEMENTATION_ROADMAP.md)
- [Improvement Tracker](./IMPROVEMENT_TRACKER.md)

---

## Getting Started

### For New Developers

1. Read the [Project Overview](./project-overview.md) to understand the system
2. Follow the [Development Guide](./development-guide.md) to set up your environment
3. Review the [Contribution Guide](./contribution-guide.md) for code standards and workflow
4. Explore the [Source Tree Analysis](./source-tree-analysis.md) to understand the codebase layout

### For Feature Work

- **Backend features:** Start with [Architecture — Runtime](./architecture-runtime.md) + [API Contracts](./api-contracts-runtime.md)
- **UI features:** Start with [Architecture — UI](./architecture-ui.md) + [Component Inventory](./component-inventory-ui.md)
- **Full-stack features:** Add [Integration Architecture](./integration-architecture.md)
- **Evaluation work:** Start with [Architecture — Eval](./architecture-eval.md)
- **Shared utilities:** Start with [Architecture — Tools](./architecture-tools.md)

### For Brownfield PRD

When ready to plan new features, run the BMad PRD workflow (`bmad-create-prd`) and provide this index as input context.
