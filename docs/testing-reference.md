## [testing] Reference

- Generated: 2025-12-19
- Files analyzed: ~37
- Recommendation summary: 26 KEEP, 7 CONSOLIDATE, 4 ARCHIVE

## Summary

The `testing/` directory houses the project's test suites, validation tools, and the evaluation framework used to run unit, integration, and multi-model prompt evaluations. It contains the evaluation engine (`evals/`), validation helpers (`validators/`), an internal test framework (`framework/core`), and a set of test harnesses for tools and integrations.

---

### `conftest.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `testing/conftest.py` |
| **Type** | Library (pytest fixtures) |
| **Lines** | ~220 |

#### Function
Provides shared pytest fixtures: repository path helpers, prompt discovery fixtures, temporary file fixtures, frontmatter schema fixtures, mock evaluation data, and helpers to parse/load prompt frontmatter.

#### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| N/A | N/A | N/A | Fixtures exposed to tests (see file for names) |

#### Environment Variables (if any)
| Variable | Required | Description |
|----------|----------|-------------|
| None | No | - |

#### Workflow Usage
- **Used by**: pytest test suite across `testing/` and other tests that import fixtures
- **Calls**: yaml parsing via PyYAML
- **Example**: PyTest automatically uses these fixtures

#### Value Assessment
- **Unique Value**: Centralizes fixtures and helpers for testing consistency
- **Overlap**: Minimal; unique utility for tests
- **Recommendation**: KEEP

---

### `run_tests.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `testing/run_tests.py` |
| **Type** | CLI / Orchestrator Script |
| **Lines** | ~380 |

#### Function
Orchestrates execution of test suites using `framework.core.test_runner.PromptTestRunner`. Supports parallel execution, filtering, summary printing, and saving aggregated results.

#### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `suites` | List[str] | `test_suites/example_test_suite.yaml` | Paths to suite files |
| `--parallel` | bool | True | Run suites in parallel |
| `--max-workers` | int | 5 | Max parallel workers |
| `--output` | str | timestamped file | Output results file |

#### Environment Variables (if any)
| Variable | Required | Description |
|----------|----------|-------------|
| None | No | - |

#### Workflow Usage
- **Used by**: CI scripts / developers to run entire testing framework
- **Calls**: `framework.core.test_runner.PromptTestRunner`
- **Example**: `python testing/run_tests.py testing/evals/example.yaml`

#### Value Assessment
- **Unique Value**: Central CLI for running suites and collecting results
- **Overlap**: Overlaps with direct `pytest` runs; orchestration is distinct
- **Recommendation**: KEEP

---

### `validate_consolidation.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `testing/validate_consolidation.py` |
| **Type** | Script (validation smoke tests) |
| **Lines** | ~220 |

#### Function
Smoke validation for the consolidated test runner: imports, provider detection, prompt loading, and a basic execution sanity check. Useful for CI sanity checks when LLM credentials are not present.

#### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| N/A | N/A | N/A | Test functions called directly when executed |

#### Environment Variables (if any)
| Variable | Required | Description |
|----------|----------|-------------|
| (LLM creds) | Optional | Some tests note LLM creds required for full execution |

#### Workflow Usage
- **Used by**: Maintainers for quick validation of runner integration
- **Calls**: `testing.framework.core.test_runner` classes
- **Example**: `python testing/validate_consolidation.py`

#### Value Assessment
- **Unique Value**: Quick smoke checks and documentation of runner expectations
- **Overlap**: Partially overlaps with unit/integration tests but provides a runnable script
- **Recommendation**: KEEP

---

### `README.md` (testing)

| Attribute | Value |
|-----------|-------|
| **Location** | `testing/README.md` |
| **Type** | Reference |
| **Frontmatter** | Complete |

#### Function
Documentation for the testing framework: directory structure, quick start commands, rubric, and CI integration notes.

#### Variables
| Variable | Required | Description |
|----------|----------|-------------|
| N/A | N/A | N/A |

#### Use Cases
1. Onboarding developers to the test framework
2. Quick commands for running evaluation/validation tests

#### Value Assessment
- **Recommendation**: KEEP

---

### `validators/frontmatter_auditor.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `testing/validators/frontmatter_auditor.py` |
| **Type** | Library / CLI |
| **Lines** | ~400 |

#### Function
Parses, validates, and optionally autofixes frontmatter for prompt markdown files. Provides normalization rules, schema enforcement, and a CLI interface for batch auditing.

#### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| CLI `paths` | List[str] | required | Files or directories to audit |
| `--fix` | bool | False | Apply autofixes |
| `--format` | str | text | Output format (text/json) |

#### Environment Variables (if any)
| Variable | Required | Description |
|----------|----------|-------------|
| None | No | - |

#### Workflow Usage
- **Used by**: validation tests and CI frontmatter checks
- **Calls**: PyYAML; used by `testing/validators/test_frontmatter_auditor.py`
- **Example**: `python testing/validators/frontmatter_auditor.py prompts/ --fix`

#### Value Assessment
- **Unique Value**: Centralizes frontmatter hygiene and autofix behavior
- **Overlap**: Similar checks exist in `testing/validators/*` tests but auditor provides apply/fix capability
- **Recommendation**: KEEP

---

### `validators/test_frontmatter.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `testing/validators/test_frontmatter.py` |
| **Type** | Unit tests |
| **Lines** | ~260 |

#### Function
PyTest suite that validates frontmatter presence, required fields, and sample prompt compliance. Uses fixtures from `conftest.py`.

#### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| N/A | N/A | N/A | Test functions driven by fixtures |

#### Environment Variables (if any)
| Variable | Required | Description |
|----------|----------|-------------|
| None | No | - |

#### Workflow Usage
- **Used by**: CI to validate prompt metadata
- **Calls**: `conftest.parse_frontmatter`, `conftest.load_prompt_file`
- **Example**: `pytest testing/validators/test_frontmatter.py -q`

#### Value Assessment
- **Recommendation**: KEEP

---

### `validators/test_frontmatter_auditor.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `testing/validators/test_frontmatter_auditor.py` |
| **Type** | Unit tests |
| **Lines** | ~140 |

#### Function
Tests for the frontmatter auditor: validation detection, autofix behavior, normalization of scalar/list values, and date normalization.

#### Value Assessment
- **Recommendation**: KEEP

---

### `validators/test_schema.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `testing/validators/test_schema.py` |
| **Type** | Unit tests |
| **Lines** | ~360 |

#### Function
Schema compliance tests: enforces types, string lengths, enums, list constraints, and content structure expectations for prompts.

#### Value Assessment
- **Recommendation**: KEEP

---

### `tool_tests/` (tests for CLI & tools)

Files documented below (all are unit/integration tests for tools in `tools/`):

- `tool_tests/test_generator.py` — Integration test for `tools.code_generator.UniversalCodeGenerator`. Requires external API keys; marked SKIP when not present. Recommendation: KEEP (or CONSOLIDATE into a single tools test file if desired).

- `tool_tests/test_evaluation_agent.py` — Extensive unittest suite for the evaluation agent, checkpointing, CLI parsing, and dataclasses. Recommendation: KEEP.

- `tool_tests/test_cli.py` — CLI tests using Click's CliRunner for `tools.cli`. Recommendation: KEEP.

- `tool_tests/test_llm_connection.py` — LLM connectivity smoke tests; skips when credentials missing. Recommendation: KEEP (or run as optional integration suite).

- `tool_tests/__init__.py` — Package marker. Recommendation: KEEP

---

### `integration/` tests

Files:

- `integration/test_prompt_integration.py` — Integration tests for running `prompt.py` commands with local models; uses subprocess and may be skipped if local models not present. Recommendation: KEEP (integration).

- `integration/test_prompt_toolkit.py` — Unit tests for provider routing and parameter handling in `tools.llm_client`. Recommendation: KEEP.

- `integration/test_evaluation_agent_integration.py` — Integration-level dry-run tests for the evaluation agent. Recommendation: KEEP.

- `integration/test_evaluation_agent_e2e.py` — End-to-end evaluation agent tests (mocked IO). Recommendation: KEEP.

- `integration/__init__.py` — Package marker. Recommendation: KEEP

---

### `evals/dual_eval.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `testing/evals/dual_eval.py` |
| **Type** | CLI / Evaluation tool (primary) |
| **Lines** | ~1525 |

#### Function
Primary multi-model evaluation tool. Discovers prompt files, runs evaluations across configured GH models (and optionally other providers), aggregates run-level EvalResult objects into model summaries and cross-validation reports, and emits JSON/markdown results. Handles git changed-only mode, logging, batching, and output formatting.

#### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| CLI args | see `--runs`, `--output`, `--format`, `--changed-only` | various | Controls evaluation behavior and output |

#### Environment Variables (if any)
| Variable | Required | Description |
|----------|----------|-------------|
| GITHUB / gh auth | When using `gh` models | Authentication for `gh` CLI |

#### Workflow Usage
- **Used by**: CI evaluation runs, developers running prompt evaluations
- **Calls**: `gh` CLI, subprocess, JSON/YAML parsing
- **Example**: `python testing/evals/dual_eval.py prompts/developers/ --format json`

#### Value Assessment
- **Unique Value**: Core evaluation engine for multi-model cross-validation — central to quality gating and CI
- **Overlap**: None of equivalent depth elsewhere
- **Recommendation**: KEEP

---

### `testing/evals/README.md`

| Attribute | Value |
|-----------|-------|
| **Location** | `testing/evals/README.md` |
| **Type** | How-To / Reference |
| **Frontmatter** | Present |

#### Function
Provides usage and design details for the evaluation tooling (dual_eval, test harnesses, results storage). Recommendation: KEEP

---

### `testing/evals/test_dual_eval.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `testing/evals/test_dual_eval.py` |
| **Type** | Unit tests (evaluation tool) |
| **Lines** | small |

#### Function
Unit tests that exercise `dual_eval.py` logic (scoring, parsing, aggregation). Recommendation: KEEP

---

### `framework/core/test_runner.py`

| Attribute | Value |
|-----------|-------|
| **Location** | `testing/framework/core/test_runner.py` |
| **Type** | Library / Framework Core |
| **Lines** | ~840 |

#### Function
Universal runner implementing TestCase/TestResult dataclasses, provider detection, and execution methods for local/gh/ollama/azure providers. This is the core engine used by `run_tests.py` and validation scripts.

#### Environment Variables
| Variable | Required | Description |
|----------|----------|-------------|
| AZURE_FOUNDRY_API_KEY | No (only for Azure flow) | API key for Azure provider paths |
| AZURE_FOUNDRY_ENDPOINT_* | No | Endpoint URLs for azure provider |

#### Value Assessment
- **Recommendation**: KEEP

---

### `framework/validators/` (base, code, content, format, semantic)

These modules implement validators used by the test runner (JSON, code, semantic, safety, format). They are referenced by `test_runner._initialize_components()` and are important for automated checks. Recommendation: KEEP

---

### Results, fixtures and archive

- `testing/evals/results/` — Contains JSON/markdown outputs of evaluation runs. These are artifacts and can be archived. Recommendation: ARCHIVE or move to `reports/` with timestamped folders.

- `testing/archive/` — Legacy/archived tests. Recommendation: ARCHIVE (keep for history, consider pruning older snapshots).

---

## Workflow Map

- `run_tests.py` / `framework/core/test_runner.py` orchestrate suites defined in YAML/JSON test_suites.
- `testing/validators/*` provide programmatic validators used during test execution.
- `testing/evals/dual_eval.py` discovers prompt files and runs model evaluations; results can be consumed by CI and `CONSOLIDATION_REPORT.md`.
- `tool_tests/` and `integration/` contain targeted tests for `tools/*` and integration points (LLM clients, CLI, evaluation agent).

## Consolidation Recommendations

| Source | Suggested Action | Rationale |
|--------|------------------|-----------|
| `tool_tests/*` | CONSOLIDATE into `testing/tools_tests.py` or a test package | Reduce duplication and simplify CI invocation; keep integration tests gated by env var
| `testing/evals/results/` | ARCHIVE (move to `reports/evals/YYYYMMDD/`) | Large artifacts belong in reports, not source tree
| `testing/archive/` | ARCHIVE | History kept but not needed for daily development
| `testing/validators/*` | KEEP (but consider moving heavy CLI-only scripts under `tools/`) | Validators are central to metadata quality

---

Completion notes

- Generated by an automated audit reading top-level and submodule files in `testing/` (core scripts, validators, eval tool, integration and tool tests).
- I focused on the active code paths used in CI and the evaluation pipeline; archived artifacts and result files were marked for archival.

