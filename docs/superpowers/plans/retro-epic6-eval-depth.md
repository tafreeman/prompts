# Retro — Epic 6: Evaluation & Data Depth

> **Status:** COMPLETED 2026-04-22. Retrospective plan — Epic 6 shipped without a prospective plan. Written after the fact to preserve decision history.
> **Audience:** Evaluation framework maintainers, UI contributors touching the rubric or dataset surfaces, API consumers of the evaluation endpoints.
> **Last verified:** 2026-04-22

---

## Goal

Close the gap between "the eval framework computes scores" and "a user of the product can understand *why* a score is what it is, see the data it was scored against, and compare runs over time." Ship additive contracts, real endpoints, and UI surfaces that make the eval data inspectable at the same depth as the execution data.

---

## Stories (shipped)

### 6.1 — Epic 6 additive contracts + TS mirrors
- **Commit:** `515f521 feat(contracts): Epic 6 additive models and TS mirrors`
- **Change:** New Pydantic v2 models — `EvaluationCriterionDetail`, `ScoreLayersModel`, `HardGatesModel`, `FloorViolationModel`, `RunEvaluationDetail`, `DatasetSampleSummary`. `EvaluationCompleteEvent` extended with `passed`, `pass_threshold`, `criteria`. TS interfaces mirrored in `ui/src/api/types.ts`.
- **Outcome:** Every new field shipped in Epic 6 is on a wire-format contract with schema-drift protection via the Epic 1 gate.

### 6.2 — `GET /runs/{filename}/evaluation` detail route
- **Commit:** `55f76b5 feat(server): add GET /runs/{filename}/evaluation detail route`
- **Change:** Returns the full rubric breakdown for a stored run — criterion scores, score layers, hard gates, floor violations.
- **Outcome:** UI can load evaluation details on demand without loading the entire run payload up front.

### 6.3 — Dataset sample endpoints
- **Commit:** `c990538 feat(server): add dataset sample-list and sample-detail endpoints`
- **Change:** `GET /eval/datasets/sample-list?dataset_id=…&limit=…` and `GET /eval/datasets/sample-detail?dataset_id=…&sample_index=…`.
- **Outcome:** A UI (or any client) can paginate dataset samples without loading the whole dataset.

### 6.4 — `tokens_30d` run-summary aggregation
- **Commit:** `d23dfea feat(server): add tokens_30d to run summary aggregation` followed by `dcdadae feat(ui): wire Tokens-30d live stat to dashboard`.
- **Change:** `RunsSummaryResponse` gains `tokens_30d`; `run_logger.summary()` aggregates tokens across all runs started in the last 30 days.
- **Outcome:** Dashboard "Tokens (30d)" tile shows real data, not placeholder text.

### 6.5 — Evaluations page: rubric accordion
- **Commit:** `4844c0c feat(ui): evaluations rubric accordion with lazy criterion detail`
- **Change:** `EvaluationRubricAccordion` with lazy `[+]` / `[-]` expansion. Criterion table renders normalized % + ASCII progress bar + `[FLOOR]` badge, score layers, hard gate `[OK]`/`[FAIL]` rows, floor violation list.
- **Outcome:** A user can see the top-level pass/fail at a glance and drill into any criterion without a page navigation.

### 6.6 — Datasets page: 3-pane browser
- **Commit:** `81887a3 feat(ui): datasets 3-pane browser with sample index and detail`
- **Change:** Dataset catalog → `SampleIndexGrid` (paginated `[<]` / `[>]`) → `DatasetDetailPane` (collapsible `[meta +/-]`, field rendering, JSON viewer, workflow preview badge).
- **Outcome:** Dataset inspection became a first-class product surface rather than a server-side debug tool.

### 6.7 — Stabilization pass
- **Commit:** `145e10f chore(epic6): stabilization pass and CHANGELOG update`
- **Outcome:** Rolling up the per-story CHANGELOG entries, small fixes surfaced in integration testing.

---

## Three load-bearing decisions worth calling out

Because Epic 6 shipped without a prospective plan, three decisions were made inline with the commits. They are load-bearing and deserve explicit preservation.

### 1. Dataset ID as query parameter, not path parameter

Dataset identifiers can contain slashes (`huggingface/swe-bench`). A path-based route (`/datasets/{dataset_id}/samples`) would require percent-encoding the slash, and the generated OpenAPI schema breaks on some clients when a path parameter contains `/`. Using a query parameter (`?dataset_id=huggingface/swe-bench`) sidesteps the encoding issue entirely.

**Cost:** inconsistent with `GET /runs/{filename}/evaluation`, which does use a path parameter. A user reading the API surface will notice the asymmetry.

**Review trigger:** Sprint B will revisit with real usage data. If the asymmetry produces actual confusion, we move to path-param-with-encoding; if not, the query-param stays. Documented in [`../../KNOWN_LIMITATIONS.md`](../../KNOWN_LIMITATIONS.md) §2.1.

### 2. Rubric accordion lazy expansion

The `EvaluationRubricAccordion` does not render criterion detail, score layers, or floor violations until the user clicks `[+]`. A naive render would layout every criterion's progress bar and every hard gate row on mount — measurable lag on runs with 10+ criteria.

**Cost:** tab / keyboard navigation semantics require extra care. Shipped with `aria-expanded` and an input-focus-guarded `useHotkeys` binding so keyboard users can still navigate efficiently.

**Benefit:** Dashboard initial paint stays fast regardless of rubric depth.

### 3. `tokens_30d` aggregation in the server, not the UI

The 30-day token aggregation is computed in `run_logger.summary()` on the server and surfaced as a single number. An alternative was to ship the full run list to the UI and aggregate client-side.

**Decision rationale:** run payloads are large; shipping 30 days of runs to compute one number would dominate dashboard load time. Server-side aggregation is O(N) once per summary request; UI-side aggregation would be O(N) per dashboard load per user.

**Cost:** adding or changing the aggregation window requires a server deploy. Acceptable.

---

## Lessons

### What worked

- **Additive contracts with schema-drift protection.** Every new field landed through `contracts/` and the Epic 1 drift gate. Zero wire-format incidents during the epic.
- **Ship API before UI.** Every UI story depended on an already-merged API story. The commit order forces this naturally: `feat(server): …` → `feat(ui): …`.
- **ASCII rubric detail.** The `[OK]` / `[FAIL]` / `[FLOOR]` badge vocabulary carried over from Epic 5. A single visual language across execution and evaluation surfaces pays off in user scan time.

### What would have been better with a plan

- **Dataset ID query-param decision was inline.** Had this been a story in a prospective plan, it would have earned a proper ADR at commit time instead of a post-hoc call-out. It is non-obvious and will surprise a future maintainer.
- **`tokens_30d` aggregation window is hardcoded.** 30 days was picked because "dashboards usually show 30 days." A plan would have asked whether 7 / 30 / 90 should all be available — now we have one, and changing it is a schema change.
- **Evaluation-endpoint scope grew mid-epic.** The evaluation detail route (6.2) started as "return evaluations" and grew fields through the epic as the UI needed them. A prospective plan would have frozen the response shape earlier.

### Process notes for future eval epics

1. Dataset-ID-as-query-param is now convention. Document it in [`../../api-contracts-runtime.md`](../../api-contracts-runtime.md).
2. Any new aggregation window (`tokens_7d`, `tokens_90d`) should be added in the same PR as the UI that consumes it — do not ship aggregations on spec.
3. Rubric UI components should be treated as a family — reuse `EvaluationRubricAccordion` primitives before building a parallel component for a new eval surface.

---

## Links

- CHANGELOG: [`../../../CHANGELOG.md`](../../../CHANGELOG.md) — Epic 6 entries under `[0.3.0]`.
- Contracts: `agentic-workflows-v2/agentic_v2/contracts/` (see Epic 6 models)
- ADR-014 (wire format ratification): [`../../adr/ADR-014-pydantic-wire-format.md`](../../adr/ADR-014-pydantic-wire-format.md)
- Known Limitations §2.1 (query-param quirk): [`../../KNOWN_LIMITATIONS.md`](../../KNOWN_LIMITATIONS.md)
