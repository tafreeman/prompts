# Contributing Guide

Welcome to the `prompts` monorepo. This guide explains how to contribute code, documentation, and tests. The project serves dual purpose as a working agentic AI platform and an educational portfolio for enterprise teams, so quality standards are high and consistently enforced.

---

## Table of Contents

1. [Welcome](#welcome)
2. [Development Setup](#development-setup)
3. [Git Workflow](#git-workflow)
   - [Conventional Commits](#conventional-commits)
   - [Branch Naming](#branch-naming)
4. [Pull Request Process](#pull-request-process)
5. [Python Code Style](#python-code-style)
   - [Formatting and Linting](#formatting-and-linting)
   - [Type Checking](#type-checking)
   - [Naming Conventions](#naming-conventions)
   - [Immutability](#immutability)
   - [File and Function Size](#file-and-function-size)
   - [Error Handling](#error-handling)
   - [Pydantic v2 Usage](#pydantic-v2-usage)
   - [Import Style](#import-style)
6. [TypeScript Code Style](#typescript-code-style)
7. [Testing Requirements](#testing-requirements)
   - [Coverage Thresholds](#coverage-thresholds)
   - [TDD Workflow](#tdd-workflow)
   - [Test Markers](#test-markers)
   - [Test Value Taxonomy](#test-value-taxonomy)
8. [Security Checklist](#security-checklist)
9. [Contract Schema Policy](#contract-schema-policy)
10. [Workflow and Agent Authoring](#workflow-and-agent-authoring)
11. [Documentation Standards](#documentation-standards)

---

## Welcome

All contributions — bug fixes, new features, documentation improvements, and test coverage — are welcome. Before opening a pull request, please read this guide in full. Standards exist not to slow contributors down but to keep a large, multi-package codebase maintainable and auditable over time.

---

## Development Setup

See [development-guide.md](development-guide.md) for the complete setup walkthrough, including:

- Prerequisites (Python 3.11+, Node 24, uv, Git)
- Installing all sub-packages
- Configuring `.env`
- Running the dev servers
- Running the test suites

All contributors are expected to have the full stack running locally before submitting a pull request.

---

## Git Workflow

### Conventional Commits

All commit messages must follow the Conventional Commits format:

```
<type>(<scope>): <short description>

<optional body — explain WHY, not WHAT>
```

#### Commit Types

| Type | When to Use |
|------|-------------|
| `feat` | A new feature visible to users or downstream consumers |
| `fix` | A bug fix |
| `refactor` | Code restructuring with no behavior change |
| `docs` | Documentation changes only |
| `test` | Adding or updating tests only |
| `chore` | Maintenance (dependency bumps, config, CI tweaks) |
| `perf` | Performance improvement |
| `ci` | Changes to CI/CD pipeline configuration |

#### Scope (optional but encouraged)

Use the sub-package or module name as scope:

```
feat(rag): add BM25 fallback for zero-embedding queries
fix(server): handle WebSocket disconnect on workflow timeout
test(eval): add coverage for PatternEvaluator hard gates
chore(deps): bump anthropic to 0.26.0
docs(api): document streaming endpoint response format
```

#### Rules

- Description is lowercase, imperative mood, no trailing period.
- Body is optional. Use it to explain the reasoning for non-obvious changes.
- Keep commits atomic: one logical change per commit.
- Do not reference ticket numbers in the short description; put them in the body.

### Branch Naming

| Branch type | Convention | Example |
|-------------|-----------|---------|
| New feature | `feature/<short-description>` | `feature/rag-bm25-fallback` |
| Bug fix | `fix/<short-description>` | `fix/websocket-disconnect-timeout` |
| Maintenance | `chore/<short-description>` | `chore/bump-anthropic-dep` |
| Documentation | `docs/<short-description>` | `docs/update-deployment-guide` |

Branch names are lowercase with hyphens. No uppercase letters or underscores.

---

## Pull Request Process

### Before Opening a PR

Run the full quality suite locally and confirm it passes before pushing:

```bash
# Lint, format, type-check (from repo root)
pre-commit run --all-files

# Backend unit tests with coverage
cd agentic-workflows-v2
python -m pytest tests/ -q --cov=agentic_v2 --cov-report=term-missing

# Frontend TypeScript check + production build
cd agentic-workflows-v2/ui
npm run build

# Eval package tests
cd agentic-v2-eval
python -m pytest tests/ -q --cov=agentic_v2_eval --cov-report=term-missing

# Tools package tests
cd tools
python -m pytest tests/ -q --cov=tools --cov-report=term-missing
```

Do not open a PR if any of these steps fail. Fix the issues first.

### PR Size

Keep pull requests under **400 lines changed** (excluding generated files, lock files, and test fixtures). Large changes are harder to review and more likely to introduce regressions. Break large features into a sequence of smaller PRs with a clear ordering.

### PR Description

A complete PR description includes:

- What the change does and why.
- Which issue(s) it closes, if applicable: `Closes #123`.
- A test plan covering what was tested manually (if integration paths are not fully automated).
- Any known limitations or follow-up items.
- Confirmation that the security checklist has been reviewed (see [Security Checklist](#security-checklist)).

### Review Requirements

- **1 approval** from a maintainer is required before merging.
- Address all `CRITICAL` and `HIGH` review comments before requesting re-review.
- `MEDIUM` comments must be addressed or acknowledged with a written rationale.
- `LOW` / `NIT` comments are optional but should be considered.

### Merging

The maintainer merges approved PRs using squash merge to keep the main branch history clean. The squash commit message must follow the Conventional Commits format and summarize the entire PR.

### CI Requirements

The following CI checks must be green before merging:

| Check | Tool | Blocks merge |
|-------|------|-------------|
| Formatting | Black + isort | Yes |
| Linting | Ruff | Yes |
| Type checking | mypy --strict | Yes |
| Unit tests | pytest | Yes |
| Coverage threshold | pytest-cov | Yes |
| Secret scan | detect-secrets | Yes |

---

## Python Code Style

### Formatting and Linting

All Python code is formatted with **Black** (line length 88) and **isort** (profile=black). These are enforced as pre-commit hooks and in CI. Do not manually reformat code to override them — configure your editor to run Black on save.

**Ruff** is the single linter, replacing Flake8, pylint, and pycodestyle. The following rule sets are enabled and must pass with zero errors:

| Prefix | Rule set |
|--------|---------|
| `E` | pycodestyle errors |
| `F` | Pyflakes |
| `W` | pycodestyle warnings |
| `I` | isort |
| `N` | pep8-naming |
| `UP` | pyupgrade |
| `S` | flake8-bandit (security) |
| `B` | flake8-bugbear |
| `A` | flake8-builtins |
| `C4` | flake8-comprehensions |
| `SIM` | flake8-simplify |
| `TCH` | flake8-type-checking |
| `RUF` | Ruff-native rules |

Run Ruff locally before pushing:

```bash
ruff check .
ruff check . --fix   # auto-fix safe violations
```

### Type Checking

All code must pass **mypy --strict** with zero errors. Key settings enforced:

- `disallow_untyped_defs = true` — every function must have type annotations on all parameters and return values.
- `warn_return_any = true` — `Any` return types trigger a warning.
- `strict_optional = true` — `None` is not a valid value unless the type is `Optional[T]` or `T | None`.
- `disallow_any_generics = true` — bare container types like `List`, `Dict` are not allowed; use `list[str]`, `dict[str, int]`.

Annotate all class attributes, not just `__init__` parameters:

```python
class WorkflowStep:
    name: str
    agent: str
    depends_on: list[str]
    inputs: dict[str, str]
    outputs: dict[str, str]

    def __init__(self, name: str, agent: str) -> None:
        self.name = name
        self.agent = agent
        self.depends_on = []
        self.inputs = {}
        self.outputs = {}
```

### Naming Conventions

Follow PEP 8 strictly:

| Identifier type | Convention | Example |
|----------------|-----------|---------|
| Functions | `snake_case` | `run_workflow_step` |
| Variables | `snake_case` | `retry_count` |
| Modules | `snake_case` | `smart_router.py` |
| Classes | `PascalCase` | `WorkflowOrchestrator` |
| Constants | `UPPER_SNAKE` | `MAX_RETRY_ATTEMPTS` |
| Internal APIs | `_snake_case` | `_build_prompt` |

**Booleans must be phrased as questions:** `is_ready`, `has_errors`, `can_retry`, `should_stream`.

**Name by intent, not by type.** Avoid vague names like `data`, `model`, `result`, `obj`. Use descriptive names that communicate the domain concept: `embedding_vector`, `workflow_definition`, `evaluation_rubric`.

The exception: short-lived loop variables in small scopes (e.g., `i`, `k`, `v`) are acceptable.

### Immutability

Always create new objects. Never mutate existing ones in-place.

```python
# WRONG — mutates the caller's dict
def add_metadata(config: dict[str, str], key: str, value: str) -> None:
    config[key] = value

# CORRECT — returns a new dict
def add_metadata(config: dict[str, str], key: str, value: str) -> dict[str, str]:
    return {**config, key: value}
```

Rationale: Immutable patterns prevent hidden side effects, make debugging tractable, and enable safe concurrent access.

For Pydantic models, use `model_copy(update={...})` to produce modified instances:

```python
updated_step = original_step.model_copy(update={"status": "completed"})
```

### File and Function Size

| Metric | Target | Hard limit |
|--------|--------|-----------|
| Lines per file | 200–400 | 800 |
| Lines per function | — | 50 |
| Nesting depth | — | 4 levels |

When a file approaches 800 lines, extract utilities into a separate module. Organize by feature or domain, not by technical layer (not `utils.py` containing everything).

### Error Handling

Handle errors explicitly at every level of the call stack.

```python
# WRONG — swallows the exception silently
try:
    result = call_llm(prompt)
except Exception:
    pass

# WRONG — bare except catches SystemExit and KeyboardInterrupt
try:
    result = call_llm(prompt)
except:
    log.warning("something failed")

# CORRECT — catch specific exceptions, log context, re-raise or recover
try:
    result = call_llm(prompt)
except LLMProviderError as exc:
    log.error("llm_call_failed", provider=exc.provider, status=exc.status_code)
    raise WorkflowExecutionError("LLM call failed") from exc
```

Use **structlog** or **loguru** for all log output. Never use `print`.

Map exceptions to HTTP status codes at API boundaries. Do not leak internal stack traces or error messages to API responses.

The project defines a custom exception hierarchy under `agentic_v2/core/errors.py`. Use these types instead of generic exceptions:

- `WorkflowExecutionError` — runtime workflow failures
- `AgentConfigurationError` — invalid agent or step definitions
- `ToolPermissionError` — tool called outside its allowlist
- `ContractValidationError` — Pydantic validation failures at boundaries
- `ProviderError` — upstream LLM provider errors

### Pydantic v2 Usage

The codebase uses **Pydantic v2**. Do not use v1 compatibility aliases.

| v1 (forbidden) | v2 (required) |
|----------------|---------------|
| `.dict()` | `.model_dump()` |
| `.parse_obj(data)` | `Model.model_validate(data)` |
| `.parse_raw(json_str)` | `Model.model_validate_json(json_str)` |
| `.schema()` | `Model.model_json_schema()` |
| `validator` decorator | `field_validator` decorator |
| `root_validator` | `model_validator` |

### Import Style

Never use `sys.path` manipulation to resolve imports. Use proper package-relative imports.

```python
# WRONG
import sys
sys.path.insert(0, "/path/to/package")
from module import thing

# CORRECT
from agentic_v2.core.protocols import ExecutionEngine
from tools.llm import LLMClient
```

For optional dependencies (e.g., the LangChain adapter), guard imports with `try/except ImportError` so that the feature degrades gracefully rather than blocking startup:

```python
try:
    from agentic_v2.langchain.engine import LangGraphEngine
    _LANGCHAIN_AVAILABLE = True
except ImportError:
    _LANGCHAIN_AVAILABLE = False
```

---

## TypeScript Code Style

### Strict Mode

All TypeScript must compile with `strict: true`. The following compiler options are active:

- `noImplicitAny` — every value must have a known type.
- `strictNullChecks` — `undefined` and `null` are distinct types.
- `noUncheckedIndexedAccess` — array and object index access returns `T | undefined`.

Using `any` is permitted only when genuinely unavoidable (e.g., bridging an untyped third-party library). Every `any` must be justified with an inline comment explaining why a more specific type is not feasible.

### Exports

Prefer **named exports** over default exports. Named exports are easier to refactor, grep, and auto-import correctly across the codebase.

```typescript
// WRONG
export default function WorkflowGraph() { ... }

// CORRECT
export function WorkflowGraph() { ... }
```

### Styling

Use **Tailwind CSS** for all styling. Do not add inline `style` props or separate CSS files unless Tailwind utilities cannot express the required style.

### State Management

Use **TanStack Query** (`@tanstack/react-query`) for all server state (data fetched from the backend). Do not introduce Redux, Zustand, or React Context for global server-side state.

Component-local UI state (open/closed, selected tab, etc.) belongs in `useState` or `useReducer`.

### Component Guidelines

- Components over 150 lines should be decomposed.
- Extract data-fetching hooks into `hooks/` rather than embedding them in components.
- Each component file exports exactly one primary component, plus any tightly related subcomponents.

---

## Testing Requirements

### Coverage Thresholds

| Package | Minimum coverage |
|---------|-----------------|
| `agentic-workflows-v2` | 80% |
| `agentic-v2-eval` | 80% |
| `tools` | 70% |
| `agentic-workflows-v2/ui` | 60% (not CI-enforced, monitored) |

PRs that reduce coverage below the threshold for a package will not be merged.

### TDD Workflow

Follow test-driven development for all new features and non-trivial bug fixes:

1. **RED** — Write a failing test that precisely describes the expected behavior.
2. **GREEN** — Write the minimum implementation to make the test pass.
3. **IMPROVE** — Refactor while keeping the test suite green.
4. **VERIFY** — Confirm coverage meets threshold: `python -m pytest --cov=<package> --cov-report=term-missing`.

Tests should assert behavior, not implementation. Use the Arrange-Act-Assert pattern:

```python
async def test_workflow_step_returns_agent_output() -> None:
    # Arrange
    mock_agent = MockAgent(output={"summary": "done"})
    step = WorkflowStep(name="summarize", agent=mock_agent)

    # Act
    result = await step.execute(inputs={"text": "some content"})

    # Assert
    assert result.outputs["summary"] == "done"
```

### Test Markers

Mark tests that require external services or are unusually slow:

```python
@pytest.mark.integration    # requires network, real LLM, or real DB
@pytest.mark.slow           # takes > 5 seconds
@pytest.mark.security       # security-sensitive assertion
```

The fast local test run skips integration and slow tests:

```bash
pytest -m 'not integration and not slow'
```

CI runs the full suite including integration tests.

### pytest-asyncio Configuration

The project uses **pytest-asyncio** in `auto` mode (`asyncio_mode = "auto"` in `pyproject.toml`). Do not add `@pytest.mark.asyncio` to individual test functions — it is unnecessary and will produce a deprecation warning.

### No Real API Calls in Unit Tests

All unit tests must mock `LLMClientProtocol` and any network I/O using `unittest.mock` or `pytest-mock`. Tests that make real API calls must be marked `@pytest.mark.integration`. Unmarked tests with real API calls will be rejected in review.

### Test Value Taxonomy

Prioritize tests that deliver real protection against regressions:

| Tier | Description | Action |
|------|-------------|--------|
| **Tier 1** | Edge cases, error paths, integration boundaries — catches real bugs | Write first, always keep |
| **Tier 2** | Happy-path coverage of core business logic | Include |
| **Tier 3** | Constructor tests, enum round-trips, trivial getters — low value | Consolidate or remove |
| **Tier 4** | Tests that never fail, duplicate other tests, or only assert mocks | Delete immediately |

When reviewing a PR, question the value of any new test that cannot fail under any plausible code change.

---

## Security Checklist

Review every item before opening a pull request. The `detect-secrets` pre-commit hook catches many of these automatically, but static analysis cannot catch all problems.

### Secrets and Credentials

- [ ] No hardcoded API keys, tokens, passwords, or any secret values.
- [ ] `.env` and `.env.*` patterns are in `.gitignore` (with `!.env.example` exception).
- [ ] New required secrets are documented in `.env.example` with a placeholder value, never a real value.
- [ ] Secrets are read from environment variables using `os.getenv()` or `pydantic-settings` at runtime.

If a secret is accidentally committed:

1. Remove it from the codebase immediately.
2. Rotate the credential at the provider before doing anything else.
3. Audit the git history for propagation.
4. Notify the maintainer.

### Input Validation

- [ ] All external inputs (API requests, file content, CLI arguments) are validated with Pydantic models at the system boundary before entering business logic.
- [ ] SQL queries use parameterized statements — no string interpolation into queries.
- [ ] No user-controlled values passed to `subprocess`, `eval`, or `exec` without explicit sanitization.

### Output Safety

- [ ] HTML output is escaped before rendering. React JSX is safe by default; `dangerouslySetInnerHTML` is forbidden unless reviewed.
- [ ] API error responses do not include internal stack traces, file paths, or system configuration.
- [ ] Log entries do not contain API keys, user PII, or raw model outputs that may encode sensitive data.

### Authentication and Authorization

- [ ] New API endpoints pass through the authentication middleware.
- [ ] Changes to `AGENTIC_API_KEY` validation or provider credential handling are reviewed by the security reviewer before merging.
- [ ] Changes to `AGENTIC_FILE_BASE_DIR` path-traversal protection require security review.

### Rate Limiting

- [ ] New public-facing endpoints include rate limiting configuration.

Use the `security-reviewer` agent (available in `.claude/agents/`) for any PR touching authentication, API key handling, or secrets management.

---

## Contract Schema Policy

Pydantic models in `agentic-workflows-v2/agentic_v2/contracts/` define the public I/O interface between workflow steps and between the backend and frontend. They are treated as versioned contracts.

### Additive-Only Rule

**Contracts are additive-only.** You may:

- Add new optional fields with defaults.
- Add new model classes.
- Add new enum members.

You may **not**:

- Remove existing fields.
- Rename existing fields.
- Change the type of an existing field in a way that breaks existing serialized data.
- Change an optional field to required.

### Adding New Fields

New fields must have a default value so that existing callers that do not populate the field continue to work:

```python
class WorkflowStepResult(BaseModel):
    step_name: str
    outputs: dict[str, str]
    duration_ms: int
    # Added in v1.3 — defaults to None for backwards compatibility
    trace_id: str | None = None
```

### Deprecating Fields

To deprecate a field:

1. Add a comment: `# deprecated: use <replacement_field> instead, remove in v2.0`.
2. Keep the field functional for at least one minor version.
3. File an issue tracking the removal.
4. Remove the field only in the next major version, coordinated with all callers.

### Breaking Changes

Breaking contract changes require:

1. An ADR filed in `docs/adr/` documenting the rationale and migration path.
2. A coordinated migration of all callers within the same PR or a tracked follow-up.
3. A major version bump if the package is externally published.

If you are unsure whether a change is breaking, open a discussion issue before proceeding.

---

## Workflow and Agent Authoring

### YAML Step Definition

Every step in a workflow YAML definition must include all of the following fields:

```yaml
steps:
  - name: summarize_research         # unique identifier within the workflow
    agent: researcher                # agent persona name (maps to prompts/*.md)
    description: >
      Summarize the collected research into a structured report.
    depends_on:                      # list of step names this step waits for
      - collect_sources
    inputs:                          # named inputs consumed by this step
      raw_sources: "{{ collect_sources.outputs.sources }}"
    outputs:                         # named outputs produced by this step
      - summary_report
```

Steps with missing required fields will fail YAML validation at startup.

### Tool Allowlisting

Built-in tools default to **DENY** for high-risk operations. Each step must explicitly allowlist the tools it requires:

```yaml
tools:
  allowed:
    - web_search
    - file_read
  # file_delete, shell_exec, git_commit default to DENY
  # and must be explicitly permitted with justification
```

Avoid granting `shell_exec` or `file_delete` to any agent step unless there is no alternative. Document the rationale in a comment.

### Agent Persona Definitions

Persona files live in `agentic_v2/prompts/*.md`. Every persona must define all four sections:

| Section | Purpose |
|---------|---------|
| **Expertise** | The domain knowledge and capabilities the agent is expected to have |
| **Boundaries** | What the agent will not do or decide (scope limits) |
| **Critical rules** | Non-negotiable behaviors — output format, safety, hallucination prevention |
| **Output format** | Exact structure of the agent's response (JSON schema, Markdown template, etc.) |

A persona file missing any of these sections will be rejected in review. Concise, specific personas produce better agent behavior than vague, verbose ones.

---

## Documentation Standards

### When to Update Docs

Update documentation in the same PR as the code change when:

- Adding or changing a public API (function signatures, CLI commands, contract schemas).
- Changing architectural components (update the relevant `docs/architecture-*.md` file).
- Changing deployment or environment configuration (update `docs/deployment-guide.md`).
- Adding new built-in tools, agents, or workflows (update `docs/development-guide.md`).

### Writing Style

- Use clear, direct technical prose. Avoid marketing language, hedging, and filler phrases.
- Use present tense for descriptions of how the system behaves.
- Use imperative mood for instructions.
- Use tables for structured comparisons and lists for enumerable items.
- Include code examples for anything non-trivial.
- Do not include emojis in documentation files.

### Architecture Decision Records

For any significant architectural change — new execution engine, new protocol, schema changes, substantial new external dependency — create an ADR in `docs/adr/` using the existing template. ADRs are immutable after acceptance. To change a past decision, file a new ADR that supersedes the old one; do not edit the original.
