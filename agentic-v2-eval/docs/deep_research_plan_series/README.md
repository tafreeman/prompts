# Deep Research Plan Series (Compiled from Conversation)

## Purpose
This document set compiles and normalizes the planning progression captured in `agentic-v2-eval/chatlg.md` into a tracked, implementation-ready series.

The series is intentionally iterative: each iteration increases architectural depth and decision completeness.

## Source Conversation
- Source log: `agentic-v2-eval/chatlg.md`
- Compilation date: February 16, 2026
- Planning horizon uses explicit date anchors from the conversation (for example, August 15, 2025 six-month cutoff and February 15-16, 2026 planning updates).

## Iteration Ladder
| Iteration | Primary Focus | Complexity Increase | Output Maturity |
|---|---|---|---|
| 01 | Foundation architecture | Agent roles + high-level flow | Conceptual system blueprint |
| 02 | Governance and confidence | Source trust tiers, recency gate, CI formula | Policy-ready plan |
| 03 | Workflow and pseudocode | Repo mapping, YAML shape, contracts, orchestration pseudocode | Engineering-ready technical spec |
| 04 | Unit tests and ADR program | Full test matrix + ADR decision log and template | Delivery governance spec |
| 05 | LLM-agnostic execution blueprint | Provider abstraction, capability routing, workstreams, rollout | Implementation master plan |

## Documents
1. `docs/deep_research_plan_series/iteration-01-foundation-architecture.md`
2. `docs/deep_research_plan_series/iteration-02-governance-and-confidence.md`
3. `docs/deep_research_plan_series/iteration-03-workflow-and-pseudocode.md`
4. `docs/deep_research_plan_series/iteration-04-tests-and-adr-program.md`
5. `docs/deep_research_plan_series/iteration-05-llm-agnostic-execution-blueprint.md`
6. `docs/deep_research_plan_series/reference-map.md`

## How to Use This Series
1. Read Iteration 01-05 in order.
2. Treat Iteration 05 as the current implementation baseline.
3. Use Iteration 04 as the governance and verification contract for implementation quality.
4. Use `reference-map.md` for source traceability for all inline reference tags (for example, `[R10]`).

## Tracking Checklist
- [ ] Confirm final scope for V1 domain (`ai_software` only).
- [ ] Approve CI formula and gate thresholds.
- [ ] Approve ADR set `0004..0023`.
- [ ] Approve provider-agnostic interface contract.
- [ ] Begin implementation from Iteration 05 with Iteration 04 tests as quality gates.
