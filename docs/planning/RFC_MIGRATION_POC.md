# RFC: Modularization POC - Evaluations Package

> **Status: ✅ COMPLETE** (Verified 2026-02-03)

## Summary
 This PR introduces the `prompts/evaluations/` directory structure as a Proof of Concept (POC) for the proposed repository modularization. It establishes a dedicated home for evaluation configuration and runners, separating them from the broad `tools/` directory.

## Changes
- **New Package**: `prompts/evaluations/`
- **Runner**: `runner.py` - A lightweight, dependency-minimal runner for YAML-based evals.
- **Example**: `examples/sentiment_eval.yaml` - A sample config-driven evaluation.
- **CI**: `.github/workflows/eval-poc.yml` - Smoke test to ensure the runner works on PRs.
- **Entry Point**: `python -m prompts.evaluations` support.

## Motivation
Currently, evaluation logic is mixed with general tooling. This structure follows the "Config-Driven Evals" pattern observed in `openai/evals` and `EleutherAI/lm-evaluation-harness`, where evals are declarative (YAML) and the runner is a distinct application component.

## Verification
Run the POC eval locally:
```bash
python -m prompts.evaluations.runner prompts/evaluations/examples/sentiment_eval.yaml
```

## Next Steps
Upon merging, we will begin migrating existing evaluation tools (like `tools.prompteval`) into this structure or wrap them with this runner interface.

---

## Completion Checklist

- [x] **New Package**: `prompts/evaluations/` created with `__init__.py`, `__main__.py`
- [x] **Runner**: `runner.py` implemented (65 lines, YAML-driven)
- [x] **Example**: `examples/sentiment_eval.yaml` + results JSON
- [x] **CI**: `.github/workflows/eval-poc.yml` workflow active
- [x] **Entry Point**: `python -m prompts.evaluations.runner` works (Exit Code 0)
