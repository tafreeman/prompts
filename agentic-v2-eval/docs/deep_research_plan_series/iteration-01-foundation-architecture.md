# Iteration 01 - Foundation Architecture

## Objective
Establish a first-pass deep-research architecture with clear agent responsibilities, iterative quality control, and report + RAG outputs [R1][R2][R9][R10][R11].

## Complexity Delta vs No Plan
1. Moves from idea-level request to a concrete 10-component system.
2. Introduces explicit research methodology stages (planning, retrieval, analysis, verification, synthesis).
3. Defines initial stop condition using confidence target (`CI >= 0.80`) [R1][R6].

## Core Agent Topology
1. Intake/Scoping Agent.
2. Research Planner (ToT branch planning).
3. Research Executor(s) with tool usage.
4. Evidence Normalizer (claim/evidence extraction).
5. Domain Analysts (AI and software/devops).
6. Verifier Agent (CoVe flow).
7. Coverage/Confidence Auditor.
8. Supervisor loop controller.
9. Final Synthesis Agent.
10. RAG Packager.

This topology aligns with modern multi-agent orchestration patterns and decomposition guidance [R9][R10][R11].

## Initial Design Decisions
1. All workflows should have tooling access, but bounded by per-agent/step allowlists [R2][R5].
2. Source governance should occur during retrieval, not only final synthesis [R1][R3][R8].
3. Final output must preserve citation traceability [R1][R6][R7].

## Initial Success Criteria
1. Comprehensive research artifact for a given goal.
2. Structured citations and explicit references.
3. Confidence threshold-driven iteration.
4. Deliverable report plus RAG-ready evidence package.

## Risks Identified in Iteration 01
1. Hallucination propagation between agents without structured outputs.
2. Weak or stale sources if recency is not enforced.
3. Tool misuse without allowlist and policy controls.

## References Used in This Iteration
[R1], [R2], [R5], [R6], [R7], [R8], [R9], [R10], [R11]

See `docs/deep_research_plan_series/reference-map.md`.
