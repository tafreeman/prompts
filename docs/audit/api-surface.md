# API Surface Audit — 2026-04-14

**Git SHA (audit):** 0252c88ce93792d05d13613e0b1f431d3193d006
**Git SHA (after fixes):** 7f1ae0f
**Status:** ⚠️ Issues Found (H-2 partially resolved)

## Implementation Status (2026-04-14)

| Finding | Status | Commit |
|---------|--------|--------|
| H-1 — `ToolProtocol` not `@runtime_checkable` | ✅ Already present (audit snapshot stale) | — |
| H-2 — 7 endpoints missing `response_model` | ✅ Partial: 2/7 wired (`GET /runs` → `list[RunSummaryModel]`, `GET /runs/summary` → `RunsSummaryResponse`). 5 remaining need new model definitions — see Strategic S-10 | `f187420` |
| M-1 — Auth opt-in/open by default | Open — Strategic item S-3 | — |
| M-2 — `TaskInput.with_context()` mutates in-place | Open | — |
| M-3 — `WorkflowEvaluationRequest.rubric` deprecation doc-only | Open | — |
| M-4 — `agentic orchestrate` CLI stub unimplemented | Open | — |
| M-5 — No committed OpenAPI schema | Open — Strategic item S-10 | — |
| M-6 — `runs.py` router tagged as "workflows" | Open | — |

---

## FastAPI Endpoints

All routes are registered under the `/api/` prefix via `app.include_router(..., prefix="/api")`.
Auth is enforced by `APIKeyMiddleware` (opt-in via `AGENTIC_API_KEY` env var). When the var is set,
every `/api/` path **except** the public prefixes below requires a bearer token.

**Public (no auth required):** `/api/health`, `/docs`, `/openapi.json`, `/redoc`

| Method | Path | Auth | Response Model | Notes |
|--------|------|------|----------------|-------|
| GET | `/api/health` | None (public) | `HealthResponse` | Liveness probe |
| GET | `/api/agents` | Optional* | `ListAgentsResponse` | Reads `config/defaults/agents.yaml` on every call — no caching |
| GET | `/api/workflows` | Optional* | `ListWorkflowsResponse` | Lists YAML workflow definitions |
| GET | `/api/adapters` | Optional* | `{"adapters": list[str]}` | **No response_model declared** |
| GET | `/api/workflows/{name}/dag` | Optional* | None (raw dict) | **No response_model declared** |
| GET | `/api/workflows/{name}/capabilities` | Optional* | None (raw dict) | **No response_model declared** |
| GET | `/api/workflows/{name}/editor` | Optional* | `WorkflowEditorResponse` | Returns raw YAML for editor clients |
| PUT | `/api/workflows/{name}` | Optional* | `WorkflowEditorResponse` | Validate + persist workflow YAML |
| POST | `/api/workflows/validate` | Optional* | `WorkflowValidationResponse` | Validate without saving |
| POST | `/api/run` | Optional* | `WorkflowRunResponse` | Execute workflow async (background task); sanitization middleware applied |
| GET | `/api/runs` | Optional* | None (raw list) | **No response_model declared**; query params: `workflow`, `limit` |
| GET | `/api/runs/summary` | Optional* | None (raw dict) | **No response_model declared** |
| GET | `/api/runs/{filename}` | Optional* | None (raw dict) | **No response_model declared**; path traversal protection via `is_within_base()` |
| GET | `/api/eval/datasets` | Optional* | `ListEvaluationDatasetsResponse` | Query param: `workflow` |
| GET | `/api/workflows/{workflow_name}/preview-dataset-inputs` | Optional* | None (raw dict) | **No response_model declared**; query params: `dataset_source`, `dataset_id`, `sample_index` |

> *Optional* = enforced only when `AGENTIC_API_KEY` env var is set. When unset, all routes are open.
  A startup warning is logged when the key is absent.

**SPA fallback:** When `ui/dist/` exists, `GET /{path:path}` serves the React SPA. This catch-all
is registered at the app level (not the `/api/` router) so it does not interfere with API routes.

---

## WebSocket / SSE Endpoints

| Path | Auth | Notes |
|------|------|-------|
| `WS /ws/execution/{run_id}` | Optional* (header only) | Origin validated; query-string token explicitly rejected with 1008; replays buffered events on connect; max buffer 500 events |
| `GET /api/runs/{run_id}/stream` | Optional* | SSE via `StreamingResponse`; 30 s keepalive heartbeat; terminates on `workflow_end` or `evaluation_complete` |

> WebSocket auth reads `Authorization: Bearer` or `X-API-Key` header only. Query-string tokens are
actively rejected (returns 1008 with explicit reason). This is correctly documented and enforced.

---

## CLI Commands

Built with **Typer**. Entry point: `agentic_v2.cli.main:app`. All commands have docstrings that
Typer exposes via `--help`.

| Command | Sub-command | Options | Description |
|---------|-------------|---------|-------------|
| `agentic run` | — | `<workflow>`, `--input/-i`, `--output/-o`, `--dry-run`, `--verbose/-v`, `--adapter/-a` | Execute a workflow; adapter defaults to `langchain` |
| `agentic compare` | — | `<workflow>`, `--input/-i` (required), `--adapters` | Run workflow through multiple adapters and compare results |
| `agentic orchestrate` | — | `<task>`, `--max-parallel`, `--verbose/-v` | Dynamic orchestration — **not yet implemented**, exits 1 with message |
| `agentic list` | — | `<component_type>` (workflows/agents/tools/adapters) | List available components |
| `agentic validate` | — | `<workflow>`, `--verbose/-v` | Validate YAML + compile LangGraph; exits 1 on error |
| `agentic serve` | — | `--port/-p` (8000), `--dev`, `--no-open` | Start uvicorn dashboard server |
| `agentic version` | — | — | Print version |
| `agentic rag` | `ingest` | `--source/-s` (required), `--collection/-c` | Ingest documents into RAG index |
| `agentic rag` | `search` | `<query>`, `--top-k/-k` (5) | Hybrid search over RAG index |

---

## Protocol Interfaces

File: `agentic-workflows-v2/agentic_v2/core/protocols.py`

| Protocol | Methods | `@runtime_checkable` | All Args Typed | Notes |
|----------|---------|----------------------|----------------|-------|
| `ExecutionEngine` | `execute(workflow, ctx, on_update, **kwargs) -> WorkflowResult` | Yes | Yes | `workflow: Any` intentional — engines accept different representations |
| `SupportsStreaming` | `stream(workflow, ctx, **kwargs) -> AsyncIterator[dict]` | Yes | Yes | Optional capability protocol |
| `SupportsCheckpointing` | `get_checkpoint_state(workflow, *, thread_id, **kwargs) -> dict\|None`; `resume(workflow, *, thread_id, ctx, **kwargs) -> WorkflowResult` | Yes | Yes | Optional capability protocol |
| `AgentProtocol` | `name -> str` (property); `run(input_data, ctx) -> Any` | Yes | Partial | `input_data: Any` and return `Any` intentional for structural subtyping |
| `ToolProtocol` | `name -> str` (property); `description -> str` (property); `execute(**kwargs) -> Any` | No | Partial | `execute` returns `Any` — no `@runtime_checkable` |
| `MemoryStoreProtocol` | `store(key, value, *, metadata)`, `retrieve(key)`, `search(query, *, top_k)`, `delete(key)`, `list_keys(*, prefix)` | Yes | Yes | Alias re-exported as `MemoryStore` from `protocols.py` for backward compat |
| `DetectorProtocol` | `name -> str`, `version -> str`, `scan(text) -> Sequence[Finding]` | Yes | Yes | Sanitization pipeline |
| `MiddlewareProtocol` | `process(content, context) -> SanitizationResult` | Yes | Yes | Sanitization pipeline |
| `VerifierProtocol` | `verify(step_output, policy) -> VerificationStatus` | Yes | Yes | Verification gate (ADR-002) |

**Notable:** `ToolProtocol` is the only protocol without `@runtime_checkable`. This means
`isinstance(obj, ToolProtocol)` will raise `TypeError` at runtime.

---

## Contract Models

### `contracts/messages.py`

| Model | All Fields Described | Pydantic V2 | Notes |
|-------|---------------------|-------------|-------|
| `AgentMessage` | Yes | Yes (`model_dump()` compatible) | `extra="forbid"` — strict |
| `StepResult` | Yes | Yes | `extra="allow"` for extensibility |
| `WorkflowResult` | Yes | Yes | `extra="allow"`; computed fields: `total_duration_ms`, `success_rate`, `failed_steps`, `total_retries` |
| `ReviewReport` | Yes | Yes | `extra="allow"`; computed: `needs_fixes`, `critical_count` |
| `Finding` | Yes | Yes | `extra="allow"`, `frozen=True` |

### `contracts/schemas.py`

| Model | All Fields Described | Pydantic V2 | Notes |
|-------|---------------------|-------------|-------|
| `TaskInput` | Yes | Yes | Base class; `with_context()`/`with_constraint()` mutate `self` — **violates immutability rule** |
| `TaskOutput` | Yes | Yes | `extra="allow"` |
| `CodeGenerationInput` | Yes | Yes | Inherits `TaskInput` |
| `CodeGenerationOutput` | Yes | Yes | `get_diff()` imports `difflib` inline |
| `CodeIssue` | Yes | Yes | |
| `CodeReviewInput` | Yes | Yes | |
| `CodeReviewOutput` | Yes | Yes | Computed properties: `critical_count`, `high_count`, `issues_by_category` |
| `TestCase` | Yes | Yes | `__test__ = False` to prevent pytest collection |
| `TestGenerationInput` | Yes | Yes | |
| `TestGenerationOutput` | Yes | Yes | |

### `contracts/sanitization.py`

| Model | All Fields Described | Pydantic V2 | Notes |
|-------|---------------------|-------------|-------|
| `Finding` | Yes | Yes | `frozen=True`; `matched_pattern` stores pattern name, not matched text (security) |
| `SanitizationResult` | Yes | Yes | `frozen=True`; audit hash stored, not raw input |

### `contracts/verification.py`

| Model | All Fields Described | Pydantic V2 | Notes |
|-------|---------------------|-------------|-------|
| `VerificationPolicy` | Yes | Yes | `frozen=True` |
| `CorrectionAttempt` | Yes | Yes | `frozen=True` |
| `VerificationResult` | Yes | Yes | `frozen=True` |

### `server/models.py`

| Model | All Fields Described | Pydantic V2 | Notes |
|-------|---------------------|-------------|-------|
| `HealthResponse` | Partial | Yes | No `Field()` descriptions on fields |
| `WorkflowRunRequest` | Yes | Yes | `run_id` regex-validated: `^[a-zA-Z0-9_-]{1,128}$` |
| `WorkflowRunResponse` | Yes | Yes | |
| `StepResultModel` | Yes | Yes | Server-layer DTO (different from `contracts.StepResult`) |
| `WorkflowResultModel` | Yes | Yes | Server-layer DTO |
| `AgentInfo` | Yes | Yes | |
| `ListAgentsResponse` | No descriptions | Yes | No `Field()` on `agents` |
| `ListWorkflowsResponse` | No descriptions | Yes | No `Field()` on `workflows` |
| `DAGNodeModel` | Yes | Yes | |
| `DAGEdgeModel` | Yes | Yes | |
| `DAGResponse` | Yes | Yes | **Declared but not used as `response_model`** on `/api/workflows/{name}/dag` |
| `WorkflowEditorRequest` | Yes | Yes | Accepts both `document` dict and `yaml_text` string via `AliasChoices` |
| `WorkflowEditorResponse` | No descriptions | Yes | Fields lack `Field()` descriptions |
| `WorkflowValidationResponse` | No descriptions | Yes | |
| `RunSummaryModel` | Yes | Yes | **Declared but not used as `response_model`** on `/api/runs` |
| `RunsSummaryResponse` | Yes | Yes | **Declared but not used as `response_model`** on `/api/runs/summary` |
| `WorkflowEvaluationRequest` | Yes | Yes | `rubric` field marked deprecated in docstring but no `deprecated=True` in `Field()` |
| `EvaluationDatasetOption` | Yes | Yes | |
| `EvaluationSetOption` | Yes | Yes | |
| `ListEvaluationDatasetsResponse` | Yes | Yes | |

**No `.dict()` (Pydantic v1) usage found anywhere in the codebase.** All serialization uses `model_dump()` / Pydantic v2 patterns.

---

## OpenAPI / Schema

FastAPI auto-generates an OpenAPI 3.x schema at runtime, served at:
- `/openapi.json` — machine-readable schema
- `/docs` — Swagger UI
- `/redoc` — ReDoc UI

Both paths are public (no auth required, included in `_PUBLIC_PREFIXES`).

**No static OpenAPI schema file is committed to the repository.** The schema is generated dynamically
from route decorators and response models. This is the FastAPI default behavior; there is no separate
`openapi.yaml` or `openapi.json` artifact in `docs/`.

---

## Findings

### Critical

None.

### High

**H-1: Five endpoints missing `response_model`** — The following routes return raw dicts/lists
without a declared Pydantic `response_model`. This means FastAPI performs no output validation and
the OpenAPI schema shows `{}` for these responses, making client code generation unreliable:
- `GET /api/adapters` — returns `{"adapters": list[str]}`; `DAGResponse` model exists but is unused
- `GET /api/workflows/{name}/dag` — `DAGResponse` model exists and fully documents the shape but is not wired up
- `GET /api/workflows/{name}/capabilities` — no model exists; returns arbitrary dict
- `GET /api/runs` — `RunSummaryModel` model exists but is not wired up; endpoint returns a raw list
- `GET /api/runs/summary` — `RunsSummaryResponse` model exists but is not wired up
- `GET /api/runs/{filename}` — returns raw run log dict; no model
- `GET /api/workflows/{workflow_name}/preview-dataset-inputs` — returns raw dict; no model

**H-2: `ToolProtocol` is not `@runtime_checkable`** — Unlike all other protocols in the module,
`ToolProtocol` lacks `@runtime_checkable`. Any code calling `isinstance(obj, ToolProtocol)` will
raise `TypeError`. This is inconsistent with the rest of the protocol suite and breaks duck-type
checking for tools.

### Medium

**M-1: Authentication is opt-in via env var (not enforced by default)** — When `AGENTIC_API_KEY`
is not set, the server logs a warning but all `/api/` routes are completely open. For a deployed
environment this creates a risk of unprotected data exposure. The warning is appropriate for
development but there is no way to enforce mandatory auth via configuration (e.g., an
`AGENTIC_REQUIRE_AUTH=true` flag).

**M-2: `TaskInput.with_context()` and `with_constraint()` mutate `self`** — These fluent builder
methods call `self.context.update(kwargs)` and `self.constraints[key] = value`, directly mutating
the model in place. The codebase-wide immutability standard (CLAUDE.md) explicitly forbids this
pattern. The methods should return a new model instance using `model_copy(update={...})`.

**M-3: `WorkflowEvaluationRequest.rubric` deprecation not machine-readable** — The `rubric` field
is documented as deprecated in the class docstring but `Field(deprecated=True)` is not set.
Pydantic v2 and FastAPI support the `deprecated` flag on fields, which surfaces in the OpenAPI spec
and IDE tooling. Missing this means clients get no warning when using the old field.

**M-4: `orchestrate` CLI command is a stub** — `agentic orchestrate` exits immediately with code 1
and a message that the feature is not implemented. It should either be hidden from the CLI or removed
until the feature is ready, to avoid confusing users.

**M-5: No static OpenAPI schema artifact** — The schema is served live at `/openapi.json` but no
committed `docs/openapi.yaml` exists. This prevents offline client generation, PR-level schema diff
reviews, and external consumer contracts. A CI step to export and commit the schema would close
this gap.

**M-6: `runs.py` tag mismatch** — The runs router uses `tags=["workflows"]` instead of a
dedicated `tags=["runs"]`. In the OpenAPI Swagger UI, run endpoints appear under the "workflows"
group alongside workflow CRUD endpoints. This makes the API documentation harder to navigate.

### Low

**L-1: `AgentInfo.tier` is `str` not `Literal` or `int`** — The field accepts any string. The
docstring examples show `"1"`, `"2"`, `"3"` but there is no validation. Tightening to
`Literal["0", "1", "2", "3"]` or `int` would prevent silent misconfiguration.

**L-2: `HealthResponse` fields lack `Field()` descriptions** — `status` and `version` have default
values but no `Field(description=...)`. This leaves the OpenAPI schema's health endpoint response
undocumented beyond the type.

**L-3: `WorkflowEditorResponse` and `WorkflowValidationResponse` lack field descriptions** —
Multiple server model fields use plain type annotations without `Field(description=...)`, reducing
the quality of auto-generated API documentation.

**L-4: Agents config file path is hardcoded in route handler** — `routes/agents.py` constructs the
config path using `Path(__file__).resolve().parent...`. If the module is relocated or used from a
different working directory, the path will silently fail. This should be a configurable constant or
pulled from application settings.

**L-5: `InMemoryStore.search()` returns `score: 1.0` for all matches** — The search is substring
matching and returns a constant score regardless of match quality. Callers relying on score for
ranking will see misleading results in development/testing. This should be documented or replaced
with a relevance-aware scoring approach.

---

## Recommendations

1. **Wire existing response models to their endpoints** — `DAGResponse`, `RunSummaryModel`, and
   `RunsSummaryResponse` are already defined and fully typed. Attach them to their respective
   routes with `response_model=`. For `/api/runs/{filename}` and `/api/workflows/{name}/capabilities`,
   create minimal typed response models.

2. **Add `@runtime_checkable` to `ToolProtocol`** — One-line fix; aligns with all other protocols
   in the module and prevents `TypeError` at runtime checks.

3. **Set `Field(deprecated=True)` on `WorkflowEvaluationRequest.rubric`** — Allows Pydantic, FastAPI,
   and IDE tooling to surface the deprecation automatically without relying on docstring parsing.

4. **Fix `TaskInput` immutability violations** — Replace `self.context.update(kwargs)` with
   `return self.model_copy(update={"context": {**self.context, **kwargs}})`. Both `with_context`
   and `with_constraint` need this treatment. Note: `TaskInput` uses `frozen=False` so switching
   to `frozen=True` would be an additive-only breaking change — prefer a factory pattern instead.

5. **Remove or stub-out `orchestrate` CLI command** — Either implement it or remove it from the
   registered commands. A `typer.Option("--experimental")` gate is one approach if the intent is
   to soft-launch later.

6. **Export OpenAPI schema in CI** — Add a CI step: `python -c "from agentic_v2.server.app import app; import json; print(json.dumps(app.openapi()))" > docs/openapi.json`. Commit and diff on PRs.

7. **Rename runs router tag to `"runs"`** — Change `router = APIRouter(tags=["workflows"])` in
   `runs.py` to `tags=["runs"]` for clean Swagger UI grouping.

8. **Consider mandatory-auth mode** — Add an `AGENTIC_REQUIRE_AUTH` env flag that makes the server
   refuse to start if `AGENTIC_API_KEY` is also unset, preventing accidental open deployments.
