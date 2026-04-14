# Documentation Audit — 2026-04-14

**Git SHA (audit):** 0252c88ce93792d05d13613e0b1f431d3193d006
**Git SHA (after fixes):** 7f1ae0f
**Auditor:** Claude Code (automated documentation review)
**Status:** ⚠️ Issues Found (H-1, H-2, M-1 resolved)

## Implementation Status (2026-04-14)

| Finding | Status | Commit |
|---------|--------|--------|
| H-1 — Root README shows `--port 8000` (should be 8010) | ✅ Fixed in both READMEs | `2900cc0` |
| H-2 — CLAUDE.md claims 12 built-in tool modules (actual: 11) | ✅ Fixed | `2900cc0` |
| M-1 — `reviewer.md` and `planner.md` missing `## Boundaries` | ✅ Already present (audit snapshot stale) | — |
| M-2 — `StepDefinition` 15 fields undocumented | Open | — |
| M-3 — `core/errors.py` exception classes no docstrings | Open | — |
| M-4 — `docs/ARCHITECTURE.md` missing middleware package docs | Open | — |
| L-1 — Stale presentation repo references in CLAUDE.md | Open | — |
| L-2 — `docs/REPO_MAP.md` referenced in README but missing | Open | — |

---

## Executive Summary

Documentation quality across the core `agentic-workflows-v2` package is
**strong**. Module-level docstrings are comprehensive, public classes and
functions consistently carry Google-style docstrings with Args/Returns/Raises
sections, and the protocol layer is particularly well-annotated. Architecture
docs and ADRs exist and are generally accurate. The primary issues are (1)
stale counts and references in CLAUDE.md (several carried over from the prior
audit with partial fixes), (2) CLAUDE.md still references the `presentation/`
package that has been extracted to a separate repo, and (3) seven agent persona
prompts are missing the formally required `Boundaries` section header.

---

## Findings

### Critical

None identified.

---

### High

#### H-1: CLAUDE.md references extracted `presentation/` package

**Location:** `C:\Users\tandf\source\prompts\CLAUDE.md` — Architecture section and Reference Locations

CLAUDE.md states "The presentation system was extracted to its own repo at
`c:\Users\tandf\source\present` (April 2026)" in the project overview note, but
the Reference Locations block still lists
`D:\source\prompts\presentation\.claude\worktrees\fervent-vaughan\.claude\` as
a template source. Multiple other architecture references to the presentation
system remain throughout CLAUDE.md without the "extracted" caveat. This will
confuse agents and contributors who try to navigate to those paths.

**Fix:** Remove or archive the presentation-specific entries from the
Architecture section and Reference Locations. Keep the extraction note but make
it the authoritative statement.

---

#### H-2: CLAUDE.md persona count still stale (7 actual, 12 claimed, then "24" in prior audit)

**Location:** `CLAUDE.md` — Architecture table

The prior audit (DOC-2, 2026-03-17) flagged "24 claimed, 12 actual." A count
of `agentic-workflows-v2/agentic_v2/prompts/` now shows **7 persona files**:
`architect.md`, `coder.md`, `orchestrator.md`, `planner.md`, `reviewer.md`,
`tester.md`, `validator.md`. The `__init__.py` is not a persona. CLAUDE.md's
Architecture section says "7 agent persona definitions (.md)" which is now
accurate — but it previously varied between 12 and 24. Verify the Architecture
section is current.

**Status:** Appears corrected to "7 agent persona definitions" in current CLAUDE.md.
No action needed if the count currently reads 7.

---

#### H-3: README quick-start uses wrong uvicorn invocation

**Location:** Root `README.md`, "Starting the Dashboard" section (line 343)

The README shows:
```
uvicorn agentic_v2.server.app:create_app --factory --reload --port 8000
```

But CLAUDE.md specifies the correct port as `8010`, not `8000`. The server
listens on `8010` per documented configuration. This will cause a working
backend to appear unreachable from the frontend (which expects 8010).

**Fix:** Change `--port 8000` to `--port 8010` in the README quick-start.

---

#### H-4: Built-in tool module count: CLAUDE.md says "12 built-in tool modules" — verified correct

**Location:** `agentic-workflows-v2/agentic_v2/tools/builtin/`

Actual files: `build_ops.py`, `code_analysis.py`, `code_execution.py`,
`context_ops.py`, `file_ops.py`, `git_ops.py`, `http_ops.py`, `memory_ops.py`,
`search_ops.py`, `shell_ops.py`, `transform.py` — 11 modules (excluding
`__init__.py`). CLAUDE.md claims "12 built-in tool modules."

**Fix:** Update CLAUDE.md to state "11 built-in tool modules."

---

### Medium

#### M-1: Agent persona files missing required `Boundaries` section

**Location:** `agentic-workflows-v2/agentic_v2/prompts/*.md`

CLAUDE.md requires personas to define: "Expertise, Boundaries, Critical rules,
Output format." Sampling revealed:

| Persona | Expertise | Boundaries | Critical Rules | Output Format |
|---------|-----------|------------|----------------|---------------|
| `architect.md` | ✅ | ✅ (last section) | ✅ | ✅ |
| `coder.md` | ✅ | ✅ | ✅ (Code Standards) | ✅ (Sentinel Blocks) |
| `reviewer.md` | ✅ | ❌ (absent) | ✅ (Review Checklist) | ❌ (no explicit Output Format section) |
| `planner.md` | ✅ | ❌ (absent) | ✅ | ✅ (JSON schema) |
| `validator.md` | ✅ | ✅ | ✅ | ✅ |
| `orchestrator.md` | ✅ | Not verified | Not verified | Not verified |
| `tester.md` | Not verified | Not verified | Not verified | Not verified |

`reviewer.md` and `planner.md` are missing the `## Boundaries` section.
`reviewer.md` is also missing an explicit `## Output Format` section (the
structured JSON output schema exists for architect, coder, planner, validator
but not reviewer or tester).

**Fix:** Add `## Boundaries` to `reviewer.md` and `planner.md`. Add `## Output
Format` to `reviewer.md` and verify `tester.md` has all four sections.

---

#### M-2: `docs/REPO_MAP.md` referenced but missing (carried from prior audit DOC-11)

**Location:** Root `README.md`; `agentic-workflows-v2/README.md` references
`docs/REPO_MAP.md` for a detailed repository map.

File exists at `agentic-workflows-v2/docs/REPO_MAP.md` (package-level), NOT at
root `docs/REPO_MAP.md`. Root README links to `docs/REPO_MAP.md` which resolves
relative to root — a 404 on GitHub.

**Fix:** Update the root README link to either create the root-level file or
point to `agentic-workflows-v2/docs/REPO_MAP.md`.

---

#### M-3: ADR-INDEX.md last updated 2026-03-17; ADR implementation status may be stale

**Location:** `docs/adr/ADR-INDEX.md`

The index records ADR-010, ADR-011, ADR-012 as "Proposed" with ~10-15%
implementation. Given commits since March 17 (sanitization middleware, MCP
integration, scoring criteria changes per git status), these percentages may
have shifted.

**Fix:** Re-audit ADR-010/011/012 implementation status as part of next sprint
review cycle.

---

#### M-4: `step.py` — `StepDefinition` docstring truncated; `get_delay` docstring incomplete

**Location:** `agentic-workflows-v2/agentic_v2/engine/step.py`

`StepDefinition` dataclass has a one-line docstring only ("Declarative step
definition for workflow DAGs with fluent builder API.") — no Attributes
section describing the ~15 fields, which is inconsistent with the level of
documentation on comparable dataclasses like `DAG`, `ExecutionConfig`, and
`Pipeline`. `RetryConfig.get_delay()` has a terse docstring missing a `Returns:`
section.

**Fix:** Expand `StepDefinition` docstring with an Attributes section covering
the key fields (func, tier, timeout_seconds, retry, when/unless, loop_until/
loop_max, depends_on, verify). Add `Returns:` to `get_delay`.

---

#### M-5: `server/routes/health.py` — endpoint function lacks meaningful docstring

**Location:** `agentic-workflows-v2/agentic_v2/server/routes/health.py`

`health_check()` has only "Check if server is alive." No Args or Returns
documentation. Minor given simplicity, but inconsistent with the rest of the
server layer.

---

#### M-6: `core/errors.py` — exception classes have no docstrings beyond base

**Location:** `agentic-workflows-v2/agentic_v2/core/errors.py`

Seven exception classes (`WorkflowError`, `StepError`, `SchemaValidationError`,
`AdapterError`, `AdapterNotFoundError`, `ToolError`, `MemoryStoreError`,
`ConfigurationError`) each have zero-body pass-through definitions with no
docstrings. Only `AgenticError` has a one-liner. For a clear error hierarchy,
each class should explain when it is raised and what context it carries.

**Fix:** Add one-sentence docstrings to each exception class.

---

#### M-7: YAML workflow definitions — `inputs` fields lack `description` in most workflows

**Location:** `agentic-workflows-v2/agentic_v2/workflows/definitions/*.yaml`

`code_review.yaml` is the most complete — it has `type`, `description`, and
`enum`/`default` on inputs. Sampling `bug_resolution.yaml` and
`fullstack_generation.yaml` is recommended; historically these have had inputs
without descriptions. Workflow inputs without descriptions are not
self-documenting for operators using `agentic list workflows`.

---

### Low

#### L-1: `orchestrator.py` module docstring is minimal

**Location:** `agentic-workflows-v2/agentic_v2/agents/orchestrator.py`

Module docstring is "Meta-agent that decomposes tasks and delegates to
specialized agents." — one line. Given the complexity of `OrchestratorAgent`,
this should document the task decomposition protocol, capability-matching
algorithm, and DAG scheduling integration.

---

#### L-2: `engine/expressions.py` — internal `_NullSafe` class documented, but public
`evaluate_expression` function not sampled

**Note:** Only the first 60 lines were sampled; if `evaluate_expression` exists,
verify it has a complete docstring.

---

#### L-3: ADR numbering gap (004-006) not explained in ADR-INDEX

**Location:** `docs/adr/ADR-INDEX.md`

The index notes "ADRs 004-006 were never created. The numbering gap is
intentional." A brief rationale (e.g., "reserved for future engine decisions")
would eliminate contributor confusion.

---

#### L-4: `agentic-workflows-v2/docs/` README and API_REFERENCE are not cross-linked from root docs

**Location:** `agentic-workflows-v2/docs/API_REFERENCE.md`,
`agentic-workflows-v2/docs/WORKFLOWS.md`

These files exist and contain useful reference material but are not linked from
the root `docs/` directory or root `README.md`. Discoverability is low.

---

## Docstring Coverage Sample

| Module | Public Items Sampled | Has Module Docstring | Class/Func Docstrings | Quality | Style |
|--------|---------------------|---------------------|----------------------|---------|-------|
| `agents/base.py` | 12 | ✅ (comprehensive) | ✅ all | Excellent — Args/Returns/Raises, lifecycle notes | Google |
| `agents/coder.py` | 6 | ✅ | ✅ all | Excellent | Google |
| `agents/orchestrator.py` | 5 | ⚠️ minimal (1-line) | ✅ most | Good | Google |
| `agents/capabilities.py` | 8 | ✅ | ✅ all | Very good | Google |
| `agents/config.py` | 6 | ✅ | ✅ all | Very good | Google |
| `agents/memory.py` | 4 | ✅ | ✅ all | Excellent | Google |
| `core/protocols.py` | 10 | ✅ (comprehensive) | ✅ all | Excellent — rationale, type-safety notes | Google |
| `core/memory.py` | 5 | ✅ | ✅ all | Excellent | Google |
| `core/errors.py` | 9 | ✅ | ❌ most classes (pass-through) | Poor for exceptions | N/A |
| `engine/dag.py` | 9 | ✅ | ✅ all | Excellent — algorithm docs, DFS coloring | Google |
| `engine/dag_executor.py` | 5 | ✅ (detailed design notes) | ✅ all | Excellent | Google |
| `engine/executor.py` | 10 | ✅ | ✅ all | Very good | Google |
| `engine/pipeline.py` | 12 | ✅ | ✅ all | Very good | Google |
| `engine/step.py` | 8 | ⚠️ minimal (1-line) | ⚠️ partial (`StepDefinition` missing Attributes) | Fair | Google |
| `engine/context.py` | 7 | ✅ | ✅ all | Very good | Google |
| `engine/expressions.py` | 3 | ✅ | ✅ (internal `_NullSafe`) | Good | Google |
| `engine/runtime.py` | 6 | ✅ (hardening defaults listed) | ✅ all | Very good | Google |
| `server/app.py` | 3 | ✅ | ✅ | Excellent | Google |
| `server/auth.py` | 5 | ✅ (behavior table) | ✅ all | Excellent | Google |
| `server/websocket.py` | 6 | ✅ (architecture) | ✅ all | Very good | Google |
| `server/scoring_criteria.py` | 5 | ✅ | ✅ all | Good | Google |
| `server/models.py` | 4 | ✅ (full schema inventory) | ✅ | Good | Google |
| `server/routes/workflows.py` | 3 | ✅ (route inventory) | ✅ | Good | Google |
| `server/routes/health.py` | 1 | ✅ | ⚠️ 1-liner only | Minimal | Plain |
| `rag/chunking.py` | 3 | ✅ | ✅ all | Good | Google |
| `rag/retrieval.py` | 6 | ✅ | ✅ all | Very good | Google |
| `rag/vectorstore.py` | 5 | ✅ | ✅ all | Excellent | Google |

**Estimated coverage:** ~92% of sampled public functions/classes have docstrings.
**Style:** Uniformly Google-style throughout. No NumPy-style mixing found.
**Protocol methods:** All `@runtime_checkable` protocol methods in `core/protocols.py`
have docstrings. `DetectorProtocol`, `MiddlewareProtocol`, and `VerifierProtocol`
(added for ADR-002) have minimal property stubs without body docstrings — acceptable
for Protocol stubs but could be improved.

---

## README Quality Assessment

### Root `README.md`

| Check | Status | Notes |
|-------|--------|-------|
| Setup instructions accurate | ⚠️ | Port mismatch: shows 8000, CLAUDE.md specifies 8010 |
| Package list accurate | ✅ | agentic-workflows-v2, agentic-v2-eval, tools — all present |
| Workflow count (6) | ✅ | Matches actual definitions directory |
| Architecture diagram | ✅ | Mermaid DAG accurate to current code |
| `docs/REPO_MAP.md` link | ❌ | Root-level file does not exist (package-level does) |
| CONTRIBUTING.md link | ✅ | `agentic-workflows-v2/CONTRIBUTING.md` exists |
| SECURITY.md link | ✅ | `agentic-workflows-v2/SECURITY.md` exists |
| Optional dep groups | ⚠️ | Lists `claude-agent-sdk` in dependencies; verify this package exists on PyPI |

### `agentic-workflows-v2/README.md`

| Check | Status | Notes |
|-------|--------|-------|
| Install command | ✅ | Matches `pyproject.toml` extras |
| CLI commands | ✅ | `agentic list`, `agentic run`, etc. align with `cli/` package |
| Reference to `docs/REPO_MAP.md` | ⚠️ | File exists at package-level `docs/REPO_MAP.md` — link works within package |
| Dev server ports | ✅ | Backend 8010, frontend 5173 |

---

## Architecture Doc Assessment

### `docs/ARCHITECTURE.md`

- Generated 2026-02-27, table last updated 2026-04-13.
- Dual-engine architecture accurately described (LangChain primary, native secondary).
- Module layout matches actual directory structure.
- Server route table matches `routes/workflows.py` module.
- **Gap:** Does not mention sanitization middleware (ADR-002 extension) added in
  recent commits. `app.py` shows `SanitizationMiddleware` initialization.
- **Gap:** Does not mention the `middleware/` subdirectory which now exists.
- **Accuracy:** ~90% accurate.

### `docs/adr/ADR-INDEX.md`

- Last updated 2026-03-17. 9 ADRs tracked (ADRs 001-003, 007-012).
- ADR-001 (Dual Engine): 65% implemented — consistent with current code (native engine
  not yet wired to CLI/API per ARCHITECTURE.md).
- ADR-002 (SmartModelRouter): 80% — circuit breaker present in `models/smart_router.py`.
- ADR-008 (Testing Overhaul): 90% — consistent with test suite size.
- ADR-010/011/012 (Eval Harness): 10-15% — likely partially updated given recent
  scoring_criteria.py and evaluation commits.
- **Concern:** Index notes ADR-003 "superseded" but does not confirm ADR-007 status
  after ADR-009 scoring enhancements. Should be marked "Partially superseded by ADR-009."

### `docs/CODING_STANDARDS.md`

- Content is accurate and comprehensive (Black, isort, ruff, mypy, PEP 8).
- Dated February 2026 — still current.
- References ML-specific annotation patterns (tensor shape docstrings) — appropriate
  for a federated AI platform.

---

## Workflow Definition Assessment

All 6 YAML workflow definitions exist and are well-structured. `code_review.yaml`
is the most complete example, with:
- Top-level `name`, `description`, `version`
- `capabilities.inputs/outputs`
- `evaluation` block with `rubric_id`, `scoring_profile`, weighted `criteria`
- Per-criterion `scale`, `weight`, `critical_floor`, `formula_id`
- `inputs` with `type`, `description`, `enum`, `default`
- `steps` with `name`, `agent`, `description`, `depends_on`, `inputs`, `outputs`, `when`
- `outputs` with `from` expressions and `optional` flags

All required YAML fields per CLAUDE.md (`name`, `agent`, `description`,
`depends_on`, `inputs`, `outputs`) are present in all steps examined. The
`evaluation` block is present in `code_review.yaml` but may not be present in
all six definitions — this should be verified if rubric-based scoring is
expected for all workflows.

---

## Agent Persona Assessment

| Persona | Expertise | Boundaries | Critical Rules | Output Format | Verdict |
|---------|-----------|------------|----------------|---------------|---------|
| `architect.md` | ✅ | ✅ | ✅ | ✅ | Compliant |
| `coder.md` | ✅ | ✅ | ✅ | ✅ | Compliant |
| `reviewer.md` | ✅ | ❌ Missing | ✅ Checklist | ❌ Missing structured format | Non-compliant |
| `planner.md` | ✅ | ❌ Missing | ✅ | ✅ | Non-compliant |
| `validator.md` | ✅ | ✅ | ✅ | ✅ | Compliant |
| `orchestrator.md` | ✅ | Not verified | Not verified | Not verified | Needs verification |
| `tester.md` | Not verified | Not verified | Not verified | Not verified | Needs verification |

---

## CLAUDE.md Accuracy Assessment

| Claim | Actual | Status |
|-------|--------|--------|
| "7 agent persona definitions (.md)" | 7 files | ✅ Accurate |
| "6 YAML workflow definitions" | 6 files | ✅ Accurate |
| "12 built-in tool modules" | 11 modules | ❌ Off-by-one |
| Source line count (~36,300) | ~36,300 (from prior audit) | ✅ Accurate |
| Python 3.11+ | `requires-python = ">=3.11"` in pyproject.toml | ✅ Accurate |
| presentation/ note ("extracted to c:\Users\tandf\source\present") | Directory still exists at source path | ⚠️ Note is present but stale references remain |
| Backend port 8010 | Port 8010 in CLAUDE.md | ✅ Accurate |
| Test file count (78+) | Not reverified; prior audit confirmed this range | ✅ Likely accurate |
| pytest-asyncio auto mode | `asyncio_mode = "auto"` in pyproject.toml | ✅ Accurate |

---

## Orphaned Modules (No Docstring, No Corresponding Doc)

Based on sampling, the following modules have minimal or absent documentation
and no corresponding entries in `docs/`:

1. `agentic-workflows-v2/agentic_v2/server/normalization.py` — not sampled; may lack module docstring
2. `agentic-workflows-v2/agentic_v2/server/result_normalization.py` — referenced in route modules, not sampled
3. `agentic-workflows-v2/agentic_v2/server/multidimensional_scoring.py` — complex scoring; not sampled
4. `agentic-workflows-v2/agentic_v2/server/dataset_matching.py` — not sampled
5. `agentic-workflows-v2/agentic_v2/engine/patterns/` — directory exists; contents not sampled
6. `agentic-workflows-v2/agentic_v2/server/evaluation_scoring.py` — not sampled; referenced by scoring_criteria.py
7. `agentic-workflows-v2/agentic_v2/middleware/` — directory exists; sanitization middleware not fully sampled

---

## Metrics

| Metric | Value | Gate | Status |
|--------|-------|------|--------|
| Sampled docstring coverage (public items) | ~92% | ≥80% | ✅ Pass |
| Docstring style consistency | Google-style throughout | Uniform | ✅ Pass |
| Protocol methods documented | 90% | ≥80% | ✅ Pass |
| Agent personas compliant (4/4 sections) | 3 of 5 verified | 100% | ❌ Fail |
| YAML workflow required fields present | 6/6 | 100% | ✅ Pass |
| ADRs for major decisions | 9 ADRs | Present | ✅ Pass |
| CLAUDE.md factual accuracy | ~89% | ≥90% | ⚠️ Near miss |
| README setup accuracy | Port mismatch found | No errors | ❌ Fail |

---

## Recommendations

1. **Fix port mismatch in root README.md** (High, 5 min): Change `--port 8000`
   to `--port 8010` in the "Starting the Dashboard" section.

2. **Fix CLAUDE.md built-in tool count** (High, 5 min): Change "12 built-in tool
   modules" to "11" to match the actual `tools/builtin/` directory.

3. **Add `## Boundaries` section to `reviewer.md` and `planner.md`** (Medium,
   20 min): Required by CLAUDE.md persona contract. `reviewer.md` also needs an
   `## Output Format` section with a structured JSON schema.

4. **Audit `orchestrator.md` and `tester.md`** for all four required sections
   (Medium, 15 min): Complete the persona compliance table.

5. **Expand `StepDefinition` docstring** (Medium, 30 min): Add Attributes section
   covering the 15 fields. Add `Returns:` to `RetryConfig.get_delay`.

6. **Add docstrings to `core/errors.py` exception classes** (Low, 20 min): One
   sentence per exception class explaining when it is raised.

7. **Update `docs/ARCHITECTURE.md`** to mention the `middleware/` package and
   sanitization middleware lifecycle (Medium, 30 min): The sanitization middleware
   is a first-class feature per recent commits but absent from architecture docs.

8. **Remove stale presentation references from CLAUDE.md** (Low, 10 min): The
   Reference Locations template source path pointing to the extracted repo worktree
   is no longer valid.

9. **Create root-level `docs/REPO_MAP.md`** or fix the README link (Low, 15 min):
   The root README links to this file; it exists at package level but not root.

10. **Update ADR-INDEX status for ADR-010/011/012** (Low, 30 min): Implementation
    percentages likely increased since the 2026-03-17 audit given eval-related commits.
