---
title: PromptEval Consolidation — Areas to Review & Incorporate
generated: 2025-12-22
related: CONDENSED_EVAL_FILE_INDEX.md
---

# PromptEval Consolidation — Areas to Review

This document uses `CONSOLIDATED_EVAL_FILE_INDEX.md` (the repo index of evaluation artifacts) as the source of truth. The sections below call out specific files/areas and the design/implementation items to incorporate into a standalone PromptEval tool that can run against any repository.

## 1) Scoring & Metrics (what to port)
- Source files: `docs/prompt-effectiveness-scoring-methodology.md`, `docs/prompt-evaluation-research.md`, `docs/SCORECARD.md`
- Actions:
  - Implement the five primary scoring dimensions (Clarity, Structure, Usefulness, Technical, Ease-of-Use) as modular metric classes.
  - Support multiple scoring backends: G-Eval-style LLM judge, rubric averaging (RubricEval), MT-Bench turn-based scoring, and semantic similarity (BERTScore-like).
  - Allow configurable thresholds and normalization (0–1 normalization, percentiles).

## 2) Eval Case Schema & Discovery
- Source files: `tools/generate_eval_files.py`, `testing/evals/*.prompt.yml`
- Actions:
  - Standardize `.prompt.yml` schema and document it in the tool (fields: id, prompt_path, test_cases, expected_format, validators, metadata).
  - Implement repo discovery heuristics: find prompts (frontmatter), candidate folders (`prompts/`, `toolkit/`, `testing/evals/`), and optional include/exclude globs.

## 3) Multi-Provider Model Layer
- Source files: `tools/run_gh_eval.py`, `tools/run_eval_geval.py`, `tools/run_eval_direct.py`, `tools/local_model.py`
- Actions:
  - Create provider adapters (GitHub Models, OpenAI, Anthropic, Azure, local ONNX). Keep a common interface for evaluate(prompt_case) → result JSON.
  - Add retry, rate-limit handling, concurrency controls.

## 4) Orchestration & Parallel Execution
- Source files: `tools/evaluation_agent.py`, `_archive/tools/evaluation_agent.py`, `tools/tiered_eval.py`
- Actions:
  - Implement a task queue with configurable parallelism, checkpoints, and resume capability (.eval_checkpoint.json pattern).
  - Support batching strategies: per-prompt, per-category, and sample-based runs.

## 5) Reproducibility & Cross-Validation
- Source files: `docs/prompt-evaluation-research.md`, `tools/evaluation_agent.py` (cross-validation thresholds)
- Actions:
  - Multi-run reproducibility: run N times, compute variance, and flag unstable prompts.
  - Cross-validate across multiple providers/models; compute agreement statistics and highlight divergent cases.

## 6) Reporters & CI Integration
- Source files: `tools/evaluate_library.py`, `docs/reports/*`, `tools/README.md`
- Actions:
  - Provide reporters: console, markdown (docs/), JSON (machine consumption), and HTML dashboards.
  - CI mode: return non-zero exit codes when overall pass thresholds are not met and publish artifact (report JSON/MD) for pipelines.

## 7) Validators, Thresholds & Governance
- Source files: `tools/validators/score_validator.py`, docs/gov files
- Actions:
  - Include validators for output schemas, PII checks, governance tags, and security scans.
  - Integrate with policy rules (e.g., do not publish prompts with PII, or mark as review-required).

## 8) Tool Extensibility & Plugins
- Source files: `docs/PROMPTEVAL_IMPLEMENTATION_PLAN.md`, `frameworks/*`
- Actions:
  - Plugin hooks: custom metric loader, custom reporters, pre/post processors for prompts, and provider plugins.
  - YAML-based test definitions compatible with Promptfoo-like syntax.

## 9) Tests & CI Examples
- Source files: `testing/tool_tests/test_evaluation_agent.py`, `testing/integration/*`
- Actions:
  - Provide a small test-suite that runs locally (unit + integration) and example CI config snippets (GitHub Actions) to demonstrate running PromptEval on a repo.

## 10) UX & Documentation
- Source files: `docs/tools-reference.md`, `docs/UNIFIED_TOOLING_GUIDE.md`, `docs/ARCHITECTURE_PLAN.md`
- Actions:
  - CLI with discover, init (generate prompteval.yml), run, report, and compare commands.
  - A short quickstart and examples to run PromptEval against `prompts/` and arbitrary repositories.

## Minimal Implementation Plan (v1)
1. Create `prompteval` Python package with CLI entrypoint.
2. Implement core interfaces: Metric, ProviderAdapter, Reporter.
3. Implement `tiered_eval` compatible runner that consumes `.prompt.yml` test cases.
4. Add `generate_eval_files` port and a `prompteval init` to create a sample config + schema.
5. Provide example reports and unit tests mirroring `testing/tool_tests`.

## Next steps / Proposed repo edits
- Add `docs/CONSOLIDATED_EVAL_FILE_INDEX.md` (done) and `docs/PROMPTEVAL_CONSOLIDATION_NOTES.md` (this file).
- Create a new top-level package `prompteval/` (later) and migrate `tools/tiered_eval.py` into it as a CLI shim.

---
Short completion note: this document references `CONSOLIDATED_EVAL_FILE_INDEX.md` and enumerates the concrete items to incorporate into a standalone PromptEval tool that can run against any repository. If you want, I can scaffold the `prompteval` package (skeleton CLI, config schema, and one metric) next.
