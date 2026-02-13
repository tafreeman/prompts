# Workflow Eval Backlog (Wave 2-4)

Last updated: 2026-02-10
Source of truth: `docs/planning/workflow-eval-consolidated-plan.md`
Wave 4 extracted plan: `docs/planning/workflow-eval-wave4-extracted.md`

## Current Snapshot

- Completed: Foundation, Wave 1, most of Wave 2, most of Wave 3.
- Partial:
  - `W2-UI-001` Compatibility matrix UI
  - `W3-UI-001` Iteration timeline UI (artifact explorer/drill-in not complete)
- Pending:
  - `W4-CI-001` CI benchmark gating
  - `W4-PR-001` Promotion policy automation
  - `W4-DOC-001` Rollout runbooks + tooling map

## Prioritized Backlog

| Priority | ID | Title | Why it remains |
|---|---|---|---|
| P0 | W2-UI-001 | Compatibility matrix UI | Compatibility filtering exists, but full matrix UX is incomplete. |
| P0 | W3-UI-001 | Iteration timeline UI | Base component/tests exist, but expandable artifact explorer is incomplete. |
| P1 | W4-CI-001 | CI benchmark gating | No final automated benchmark gate in CI yet. |
| P1 | W4-PR-001 | Promotion policy automation | No automatic promotion decision flow wired to scoring thresholds. |
| P1 | W4-DOC-001 | Rollout runbooks + tooling map | Final operational docs and rollout playbooks still open. |

## Backlog Item Details

### W2-UI-001 — Compatibility matrix UI

- Scope:
  - Add matrix view showing workflow-to-dataset compatibility outcomes.
  - Surface reasons for incompatibility per workflow input/output contract.
  - Keep existing dataset filtering behavior.
- Suggested tests:
  - Renders matrix rows/columns for workflows and datasets.
  - Displays compatible vs incompatible state.
  - Shows mismatch reason details on selection.

### W3-UI-001 — Iteration timeline UI (complete pass)

- Scope:
  - Integrate `IterationTimeline` into run/live pages for iterative runs.
  - Add expandable attempt details (logs, patches, judge output, failed steps).
  - Wire artifact explorer to `runs/<run_id>/attempts/<N>/`.
- Suggested tests:
  - Timeline renders from run payload.
  - Expanding an attempt shows artifact links/details.
  - Empty artifact state handled.

### W4-CI-001 — CI benchmark gating

- Scope:
  - Add benchmark job to CI with threshold-based pass/fail gate.
  - Store and compare baseline metrics by workflow/profile.
- Suggested tests:
  - CI job fails when benchmark is below threshold.
  - CI job passes when benchmark meets threshold.

### W4-PR-001 — Promotion policy automation

- Scope:
  - Codify promotion policy using weighted score, grade, hard gates, and floors.
  - Publish promotion decision artifacts (machine-readable + markdown).
- Suggested tests:
  - Promotion denied on hard-gate/floor violation.
  - Promotion granted when all policy checks pass.

### W4-DOC-001 — Rollout runbooks + tooling map

- Scope:
  - Create runbooks for enablement, rollback, and incident handling.
  - Publish final tooling map linking active components and owners.
- Suggested tests:
  - Docs lint and link-check pass.
  - Runbook checklists cover success/failure paths.

## GitHub Backlog Option

You can mirror this file into GitHub Issues as a backlog board. This environment currently has no `gh` CLI installed, so use one of these approaches:

- GitHub web UI:
  - Create one issue per backlog item using the IDs above.
  - Add labels: `wave-2`, `wave-3`, `wave-4`, `backlog`, `ui`, `ci`, `docs`.
- GitHub CLI (if installed locally):
  - `gh issue create --title "W2-UI-001: Compatibility matrix UI" --body-file <file>`
  - Repeat for each ID.
- GitHub Projects:
  - Create fields for `Wave`, `Status`, `Priority`, `Depends On`.
  - Add the five backlog issues and track progression there.
