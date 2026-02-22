# Repository Master Manifest

This file is a human-maintained inventory of major repository areas and their purpose.

## Top-Level Inventory

| Path | Type | Purpose |
| --- | --- | --- |
| `README.md` | doc | Main project entrypoint |
| `CONTRIBUTING.md` | doc | Contribution workflow and required checks |
| `CODE_OF_CONDUCT.md` | doc | Community behavior expectations |
| `SECURITY.md` | doc | Vulnerability reporting policy |
| `SUPPORT.md` | doc | Support and issue routing |
| `LICENSE` | doc | License terms |
| `pyproject.toml` | config | Python package metadata and dependency groups |
| `dev.sh` | script | Local backend+frontend dev launcher |
| `agentic_v2/` | package | Core runtime, agents, engine, server, workflows |
| `docs/` | docs | Architecture, API, workflow, and operations docs |
| `examples/` | examples | Minimal runnable examples |
| `fixtures/` | fixtures | Sample artifacts for docs/tests |
| `feature_package/` | artifacts | Generated package and handoff outputs |
| `scripts/` | scripts | Utility scripts and docs validators |
| `tests/` | tests | Backend test suite |
| `ui/` | frontend | React application and UI tests |
| `backend/` | prototype | Minimal backend scaffold |
| `shared/` | shared | Shared package source |
| `.github/` | templates | Issue templates and PR template |

## `agentic_v2/` Module Inventory

| Path | Responsibility |
| --- | --- |
| `agentic_v2/agents/` | Agent implementations and capabilities |
| `agentic_v2/cli/` | `agentic` CLI commands |
| `agentic_v2/config/` | Default model, agent, and evaluation config |
| `agentic_v2/contracts/` | Typed message and schema contracts |
| `agentic_v2/engine/` | Workflow graph and step execution engine |
| `agentic_v2/evaluation/` | Scoring normalization helpers |
| `agentic_v2/integrations/` | Tracing and integration adapters |
| `agentic_v2/langchain/` | LangChain/LangGraph-specific integration layer |
| `agentic_v2/models/` | Tier routing and provider client wrappers |
| `agentic_v2/prompts/` | Prompt templates for role-specific agents |
| `agentic_v2/server/` | FastAPI app and API routes |
| `agentic_v2/tools/` | Tool registry and built-in tool implementations |
| `agentic_v2/workflows/` | Workflow loader, runner, definitions, run logger |

## Workflow Definitions

Located in `agentic_v2/workflows/definitions/`:
- `bug_resolution.yaml`
- `code_review.yaml`
- `deep_research.yaml`
- `fullstack_generation.yaml`
- `fullstack_generation_bounded_rereview.yaml`
- `multi_agent_codegen_e2e.yaml`
- `multi_agent_codegen_e2e_single_loop.yaml`
- `plan_implementation.yaml`
- `tdd_codegen_e2e.yaml`
- `test_deterministic.yaml`

## Reference Links

- Docs index: `docs/README.md`
- Architecture: `docs/ARCHITECTURE.md`
- Workflow guide: `docs/WORKFLOWS.md`
- API reference: `docs/API_REFERENCE.md`
- Repo map: `docs/REPO_MAP.md`
- Active vs legacy map: `docs/reports/ACTIVE_VS_LEGACY_TOOLING_MAP.md`
