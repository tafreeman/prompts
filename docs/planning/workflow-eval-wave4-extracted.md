# Wave 4 Extracted Plan

Last updated: 2026-02-10
Primary source: `docs/planning/workflow-eval-consolidated-plan.md`
Related backlog: `docs/planning/workflow-eval-backlog.md`

## Scope

Wave 4 is the finalization wave:

- `W4-CI-001` CI benchmark gating
- `W4-PR-001` Promotion policy automation
- `W4-DOC-001` Rollout runbooks + tooling map

Current status: all three tickets are still `pending`.

## Preconditions

Wave 4 depends on:

- `W3-FL-001` feature flags (completed)
- `W2-AG-001` per-agent scoring (completed, required for promotion policy)
- Wave 1-3 regression gates staying green

## Ticket Details

### W4-CI-001 — CI benchmark gating

Field values (from consolidated plan):

- Track: CI
- Est: 1 day
- Depends on: `W3-FL-001`
- Files: CI config, `scripts/`
- Status: `pending`

Description:

- Add CI step that runs tier-0 benchmark smoke against all non-experimental workflows.
- Merge gate: all must pass hard gates.
- Failure blocks merge.

Tests:

1. `test_ci_smoke_script_exits_zero`:
- Script runs against fixtures and exits `0`.

2. `test_ci_smoke_script_exits_nonzero_on_failure`:
- Bad fixture produces exit `1`.

### W4-PR-001 — Promotion policy automation

Field values (from consolidated plan):

- Track: CI
- Est: 1.5 days
- Depends on: `W3-FL-001`, `W2-AG-001`
- Files: `server/evaluation.py`, `scripts/promotion_check.py` (new)
- Status: `pending`

Description:

Implement promotion policy checks:

1. Non-inferiority per criterion:
- New version score must be `>= baseline - delta` (`delta=0.02` default).

2. Floor regression detection:
- If a criterion that previously passed its floor now fails, block promotion.

3. Minimum sample requirement:
- Promotion requires at least `N` scored runs (`N=10` default).

4. Reporting:
- Produce promotion report with per-criterion comparison, trend direction, and pass/block verdict.

5. Integration:
- Expose as optional post-evaluation step callable from CLI and CI.

Tests (`test_promotion.py`):

1. `test_promotion_passes_when_better`
2. `test_promotion_blocks_on_regression`
3. `test_promotion_blocks_floor_regression`
4. `test_promotion_requires_min_samples`
5. `test_promotion_report_structure`

### W4-DOC-001 — Rollout runbooks + tooling map

Field values (from consolidated plan):

- Track: Docs
- Est: 1.5 days
- Depends on: all waves substantially complete
- Files: `docs/operations/` (new), `docs/reports/ACTIVE_VS_LEGACY_TOOLING_MAP.md`, `README.md`
- Status: `pending`

Description:

1. Create operational runbooks for:
- Enabling features
- Rolling back flag changes
- Incident response for scoring failures

2. Create/update tooling map:
- `docs/reports/ACTIVE_VS_LEGACY_TOOLING_MAP.md`
- Active modules vs deprecated/stale paths

3. Clean top-level docs:
- Remove stale references from `README.md`.

Tests:

- Docs-only (no dedicated test file in ticket spec).

## Wave 4 Final Regression Gate

Wave 4 is complete only when all are true:

1. Full backend suite green: `pytest tests/`
2. Full UI build/test green: `npm run build && npm run test`
3. Server starts with all feature flags on and off
4. Full UI smoke with all features enabled
5. CI smoke script passes
6. Rollback check passes:
- Disable all feature flags and system behaves like Foundation baseline

## Extracted Backlog (Wave 4 only)

Priority order:

1. `W4-CI-001` CI benchmark gating
2. `W4-PR-001` Promotion policy automation
3. `W4-DOC-001` Rollout runbooks + tooling map

## GitHub Backlog Mapping

If tracked in GitHub Issues, create one issue per ticket:

1. `[W4-CI-001] CI benchmark gating`
2. `[W4-PR-001] Promotion policy automation`
3. `[W4-DOC-001] Rollout runbooks + tooling map`

Recommended labels:

- `wave-4`
- `backlog`
- `ci` (for W4-CI-001, W4-PR-001)
- `docs` (for W4-DOC-001)

