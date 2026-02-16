# Iteration 05 - LLM-Agnostic Execution Blueprint (Master Plan)

## Objective
Produce the final implementation baseline that is provider-neutral, traceable, and execution-ready with workstreams, deliverables, and quality gates [R2][R3][R6][R10][R11][R16].

## Complexity Delta vs Iteration 04
1. Integrates architecture, governance, tests, and ADR controls into a single execution master plan.
2. Formalizes provider abstraction and capability-based routing.
3. Adds workstream decomposition with Definition of Done and gate-aligned testing.
4. Preserves all prior constraints while removing vendor lock-in assumptions.

## LLM-Agnostic Design
1. Define `ModelProvider` interface adapters by capability, not vendor identity [R11].
2. Normalize provider outputs into shared structures for messages, tool calls, citations, and usage [R2][R6].
3. Route steps via capability requirements (`reasoning`, `tool_use`, `long_context`, `structured_output`) [R11].
4. Keep workflow policies independent of provider-specific API shapes [R10][R11].

## Master Workstreams
| Workstream | Deliverable | Definition of Done | Quality Gates |
|---|---|---|---|
| WS1 | Deep research workflow YAML | Step graph + gates + outputs valid | Loader + round-gating tests |
| WS2 | Contracts and CI metrics | Typed schema + CI helpers implemented | Contract + formula tests |
| WS3 | Prompt set | Role-separated prompt files complete | Prompt and output-contract tests |
| WS4 | Governance controls | Source/citation/critical-claim rules active | Citation + critical-claim tests |
| WS5 | RAG packaging | Manifest/chunks/claim graph emitted | RAG contract tests |
| WS6 | ADR program | ADR set + lint checks operational | ADR quality and lifecycle tests |

## Acceptance Gates
1. Citation completeness is required for successful final outputs.
2. Critical claims fail without two independent Tier-A sources.
3. CI/recency/contradiction gates control iteration and stop behavior.
4. Partial outputs are explicit when max rounds are exhausted.
5. ADR compliance tests pass for governance completeness.

## Rollout Plan
1. Phase 1: create tracked plan artifact and approve scope.
2. Phase 2: implement workflow + contracts + round gates.
3. Phase 3: implement synthesis + RAG packaging.
4. Phase 4: implement ADR files + ADR quality tests.
5. Phase 5: baseline evals and reliability hardening.

## Operational Defaults
1. Domain for V1: `ai_software`.
2. Recency window: 183 days.
3. Recent source minimum: 10.
4. Max rounds: 4.
5. Engine-core change avoided in V1 (bounded unrolled rounds).

## References Used in This Iteration
[R1], [R2], [R3], [R4], [R5], [R6], [R7], [R8], [R9], [R10], [R11], [R12], [R13], [R14], [R15], [R16], [R17], [R18], [R19], [R20], [R21], [R22]

See `docs/deep_research_plan_series/reference-map.md`.
