# Code Quality Audit — 2026-04-14

**Git SHA:** 0252c88ce93792d05d13613e0b1f431d3193d006
**Auditor:** Claude Code (automated — Code Quality Expert role)
**Scope:** `agentic-workflows-v2/agentic_v2/`, `agentic-v2-eval/`, `tools/`
**Status:** Issues Found

> This supersedes the 2026-03-17 audit. Prior findings CQ-1 through CQ-4 (stale prompt exports,
> broken agent YAML references, and presentation import paths) are not in scope for this audit
> as they target the presentation package now extracted to a separate repo.

---

## Findings

### Critical

None identified in this pass.

### High

#### H-1: Silent Exception Swallowing — 11 confirmed `except Exception: pass` blocks

Eleven locations use `except Exception: pass` with no logging, re-raise, or fallback assignment.
This is a rule violation (`except: pass` is **forbidden** per coding standards) and actively hides
bugs in production.

| File | Line(s) | Context |
|------|---------|---------|
| `engine/agent_resolver.py` | 113, 121 | Context lookup for `file_path`/`code_file` keys |
| `agents/capabilities.py` | 380–381 | Capability introspection probe |
| `langchain/graph_wiring.py` | 244, 265 | JSON parsing / output extraction |
| `langchain/tools.py` | 430–431 | Tool schema introspection |
| `integrations/tracing.py` | 83–84 | Tracer cleanup (comment says intentional) |
| `engine/step.py` | 446–447 | Error hook invocation (comment says intentional) |

The tracing and error-hook cases have inline comments explaining intent. The remaining 5 locations
(agent_resolver, capabilities, graph_wiring×2, tools) are unprotected and should log at `DEBUG`
or `WARNING` level so errors surface during development.

#### H-2: Oversized Files — 1 file exceeds 800-line gate

| File | Lines | Over by |
|------|-------|---------|
| `langchain/graph_wiring.py` | 807 | 7 |

The following files are approaching the 800-line ceiling and should be watched:

| File | Lines |
|------|-------|
| `server/evaluation_scoring.py` | 750 |
| `langchain/runner.py` | 654 |
| `tools/llm/local_model.py` | 641 |
| `tools/llm/probe_discovery_providers.py` | 590 |
| `server/judge.py` | 579 |
| `workflows/loader.py` | 575 |
| `server/dataset_matching.py` | 564 |
| `contracts/messages.py` | 566 |
| `server/multidimensional_scoring.py` | 549 |
| `agents/test_agent.py` | 544 |
| `agents/orchestrator.py` | 541 |
| `agents/base.py` | 541 |
| `tools/llm/model_probe.py` | 538 |
| `models/smart_router.py` | 536 |
| `tools/llm/model_inventory.py` | 534 |
| `models/client.py` | 526 |
| `server/execution.py` | 520 |
| `langchain/tools.py` | 520 |
| `engine/step.py` | 517 |
| `tools/core/tool_init.py` | 509 |
| `cli/main.py` | 509 |

### Medium

#### M-1: Broad `except Exception` — 171 occurrences across 71 files (agentic_v2 alone)

The codebase relies heavily on `except Exception as e` with logging or return-value fallbacks.
While most log the error or re-raise, the sheer volume (171 in agentic_v2, 17 in agentic-v2-eval,
108 in tools) makes it difficult to distinguish intentional broad catches from accidental masking.

High-density files (>5 occurrences each):

| File | Count |
|------|-------|
| `langchain/tools.py` | 10 |
| `tools/builtin/memory_ops.py` | 6 |
| `tools/builtin/file_ops.py` | 6 |
| `server/routes/workflows.py` | 5 |
| `langchain/runner.py` | 5 |
| `langchain/graph_wiring.py` | 5 |
| `tools/builtin/transform.py` | 5 |
| `server/routes/evaluation_routes.py` | 4 |
| `integrations/mcp/adapters/resource_adapter.py` | 4 |
| `agents/base.py` | 4 |
| `agents/orchestrator.py` | 4 |
| `integrations/mcp/transports/websocket.py` | 5 |

**Recommendation:** Audit each `except Exception` site to narrow to the specific exception class
expected. Use `except (ValueError, KeyError)` patterns where the callee raises predictable errors.

#### M-2: Magic Numbers in Scoring Logic

`server/scoring_criteria.py` and `server/evaluation_scoring.py` contain inline numeric literals
that represent domain thresholds without named constants. Examples:

- `0.7` / `0.3` blend weights for correctness
- `0.75` penalty multiplier for failed correctness
- `45.0`, `4.0`, `20.0`, `78.0`, `8.0`, `12.0` in code-quality scoring
- `1.5`, `55.0`, `5.0` in efficiency scoring
- `120.0` richness divisor and `6.0` key bonus in documentation scoring
- `30.0` base, `15.0` failure penalty in documentation scoring
- `50.0` baseline for unknown criteria, `20.0` failure adjustment
- Score thresholds 90/80/70/60 for grade mapping (A/B/C/D/F) — these are acceptable but
  benefit from a named `GRADE_THRESHOLDS` mapping for discoverability

These literals are scattered across approximately 30 lines in scoring_criteria.py. They should be
extracted to named constants at the top of the module (e.g. `CORRECTNESS_SUCCESS_WEIGHT = 0.7`).

#### M-3: Deep Nesting — 9 files with 5+ indent levels (32+ spaces)

Files confirmed to have code at 5+ levels of indentation (each level = 4 spaces):

| File | Deep-nest occurrences |
|------|----------------------|
| `server/execution.py` | 9 |
| `integrations/mcp/adapters/resource_adapter.py` | 5 |
| `server/routes/runs.py` | 4 |
| `langchain/tools.py` | 3 |
| `workflows/loader.py` | 4 |
| `agents/architect.py` | 4 |
| `agents/implementations/claude_agent.py` | 3 |
| `engine/llm_output_parsing.py` | 1 |
| `middleware/detectors/secrets.py` | 1 |

`server/execution.py` is the worst offender (9 occurrences at 32+ spaces).

#### M-4: `print()` in Production Source — `agentic-v2-eval` evaluators

The `agentic_v2` package itself avoids bare `print()` (CLI code uses Rich's `console.print`,
and the single `print(json.dumps(output))` in `code_execution.py` is inside a generated
subprocess wrapper — intentional). However, `agentic-v2-eval` source has 11 files with
bare `print()` in non-test production code:

| File | Pattern |
|------|---------|
| `evaluators/standard.py` | `print(f"Warning: ...")` in module-level loader |
| `evaluators/pattern.py` | `print(f"Warning: ...")` in module-level loader |
| `evaluators/standard.py` | `print(f"Standard eval run {i+1} failed: {e}")` |
| `evaluators/pattern.py` | `print(f"Pattern eval run {i+1} failed: {e}")` |
| `runners/streaming.py` | `print(result)` in docstring example (acceptable) |
| `__main__.py` | Multiple `print()` for CLI output |

The evaluator warning prints bypass structured logging and will not appear in log aggregators.
The `__main__.py` prints are CLI output (lower priority).

**Fix:** Replace evaluator `print()` calls with `logger.warning()`.

#### M-5: `sys.path` Hacks in Source Code (Not Just Tests)

`sys.path.insert(0, ...)` appears in 3 non-test source files:

| File | Location |
|------|----------|
| `tools/agents/benchmarks/runner.py` | Line 33 |
| `tools/llm/list_gemini.py` | Line 9 |
| `agentic-workflows-v2/scripts/run_deep_research.py` | Lines 59–62 |

Tests using `sys.path` in `conftest.py` are acceptable (standard pytest pattern). The source
files above should be refactored to use proper package imports, enabled by `pip install -e .`.

### Low

#### L-1: TODO/FIXME Count — 2 tracked items

| File | Line | Content |
|------|------|---------|
| `cli/main.py` | 197 | `# TODO(ADR-001): The LangChain path uses a separate...` |
| `workflows/runner.py` | 313 | `# TODO(ADR-001): When a custom step_executor is provided...` |

Both reference ADR-001 and appear intentional/tracked. No untracked `HACK` or `XXX` markers found.

#### L-2: No Star Imports Detected

`from x import *` — 0 instances found. Clean.

#### L-3: No Bare `except:` (Without `Exception`) Detected

Bare `except:` (without a type) — 0 instances found. Clean.

---

## Metrics

| Metric | Value | Gate | Status |
|--------|-------|------|--------|
| Files > 800 lines | 1 (`graph_wiring.py` at 807) | 0 | Issues Found |
| `except Exception: pass` (silent) | 11 | 0 | Issues Found |
| Total `except Exception` occurrences | 296 (all packages) | — | Monitor |
| Bare `except:` (no type) | 0 | 0 | OK |
| Star imports | 0 | 0 | OK |
| `sys.path` hacks in non-test source | 3 | 0 | Issues Found |
| `print()` in production source (non-CLI, non-test) | ~6 (eval package) | 0 | Issues Found |
| TODO/FIXME count | 2 | — | — |
| Deep nesting (5+ levels) files | 9 | 0 | Monitor |
| Magic number density | High (scoring_criteria.py) | 0 | Issues Found |

---

## Oversized Files

| File | Lines | Over by |
|------|-------|---------|
| `agentic-workflows-v2/agentic_v2/langchain/graph_wiring.py` | 807 | 7 |

Files 700–799 lines (approaching gate — monitor):

| File | Lines |
|------|-------|
| `agentic-workflows-v2/agentic_v2/server/evaluation_scoring.py` | 750 |
| `agentic-workflows-v2/agentic_v2/langchain/runner.py` | 654 |
| `tools/llm/local_model.py` | 641 |
| `tools/llm/probe_discovery_providers.py` | 590 |
| `agentic-workflows-v2/agentic_v2/server/judge.py` | 579 |

---

## Recommendations

1. **Fix silent exception swallows (H-1, 5 sites):** Add `logger.debug("...", exc_info=True)`
   inside the `except Exception: pass` blocks in `agent_resolver.py`, `capabilities.py`,
   `graph_wiring.py` (×2), and `tools.py`. Do NOT change the tracing/error-hook cases —
   those are intentional and commented.

2. **Extract scoring magic numbers to named constants (M-2):** Introduce a `_SCORING_WEIGHTS`
   or `_THRESHOLDS` dict/dataclass at the top of `scoring_criteria.py`. This is a 30-minute
   refactor with high readability payoff.

3. **Split `langchain/graph_wiring.py` (H-2):** At 807 lines with 25+ functions, this file
   should be split into `node_factories.py` (step node builders), `edge_wiring.py` (add_*/wire_*
   helpers), and `graph_builder.py` (`build_graph`, `compile_graph`). The existing function
   boundaries make this straightforward.

4. **Watch `evaluation_scoring.py` (750 lines):** One more significant addition will push it
   past the gate. Consider extracting the `compute_hard_gates` and `_step_scores` groups into
   a `gates.py` submodule.

5. **Remove `sys.path` hacks from source (M-5):** `runner.py` and `list_gemini.py` should use
   proper package imports. Ensure `pip install -e .` is documented in the contributor setup.

6. **Replace `print()` with logging in evaluators (M-4):** Two evaluator files use `print()`
   for warnings that belong in the logging pipeline.

7. **Narrow `except Exception` over time (M-1):** Prioritize the 10 densest files. Use
   `ruff` rule `BLE001` (blind exception) to enforce this in CI once the count is reduced.

---

## Prior Findings Status

From the 2026-03-17 audit:

| Finding | Status |
|---------|--------|
| CQ-1: Stale prompt exports in `__init__.py` | Out of scope (presentation repo extracted) |
| CQ-2: Broken agent YAML references | Out of scope (presentation repo extracted) |
| CQ-3: Wrong relative import paths in presentation | Out of scope (presentation repo extracted) |
| CQ-4: `.js` extension imports in TypeScript | Out of scope (presentation repo extracted) |
| CQ-5: 40+ bare `except Exception:` handlers | Still present — narrowed to 11 silent, 296 total |
| CQ-6: `print()` in production code | Partially resolved — CLI uses Rich console (correct), eval package still has raw prints |
