---
name: run-ci-local
description: Run the full CI pipeline locally (lint, type-check, test all packages)
disable-model-invocation: true
---

# Run CI Locally

Mirror the GitHub Actions CI pipeline on your local machine before pushing.

## Steps

1. **Lint & Format** (fail-fast):
   - `pre-commit run --all-files`
2. **Type Check**:
   - `uv run mypy agentic-workflows-v2/agentic_v2/ --ignore-missing-imports`
3. **Test Suites** (run all, report failures at end):
   - `uv run pytest tools/tests/ -q --tb=line` (shared tools, coverage gate: 70%)
   - `uv run pytest agentic-v2-eval/tests/ -q --tb=line` (eval framework)
   - `uv run pytest agentic-workflows-v2/tests/ -q --tb=line` (main runtime, coverage gate: 80%)
4. **Frontend Tests**:
   - `cd agentic-workflows-v2/ui && npm test` (Vitest)
5. **Summary**: Report pass/fail table for all steps

## Notes

- Pre-commit failure blocks remaining steps (lint must pass first)
- Test suites run independently — all are attempted even if one fails
- Expected runtime: ~3-5 minutes for full suite
