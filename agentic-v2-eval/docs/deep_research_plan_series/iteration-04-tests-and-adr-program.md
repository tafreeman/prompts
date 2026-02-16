# Iteration 04 - Unit Tests and ADR Program

## Objective
Add delivery governance with a full test matrix and architecture decision record program, including rationale and traceability for each major design choice [R15][R16][R17][R18][R19][R20][R22].

## Complexity Delta vs Iteration 03
1. Moves from implementation spec to quality-governed delivery framework.
2. Defines deterministic test coverage requirements across contracts, logic, workflow, citations, and RAG outputs.
3. Defines ADR lifecycle, template, numbering, and supersession model.
4. Adds testable compliance checks for ADR quality itself.

## Unit Test Matrix
### Contracts
1. Source schema validation.
2. Evidence schema validation.
3. Confidence report schema validation.
4. RAG chunk schema validation.

### Metrics and Gate Logic
1. CI formula exactness.
2. Continue when CI below threshold.
3. Continue when recent source count below threshold.
4. Continue when contradictions present.
5. Stop when all gates pass.

### Recency
1. 183-day boundary behavior.
2. Unknown-date handling.
3. Source uniqueness counting.
4. Date precedence handling.

### Workflow and Output Integrity
1. Workflow YAML loads.
2. Tool allowlist parsing.
3. Round gate `when` expressions.
4. Final output mapping.

### Citation and Critical Claims
1. No uncited factual claims allowed.
2. Critical claims require 2 independent Tier-A sources.
3. Contradicted claims not marked verified.

### RAG
1. Manifest count integrity.
2. Chunk metadata completeness.
3. Claim graph source-ID integrity.

## ADR Program
Planned ADR set: `0004..0023`.

Coverage includes:
1. ADR process/lifecycle.
2. Template and governance.
3. Workflow-shape and gating decisions.
4. Source governance and citation policies.
5. Tooling policy.
6. Test strategy.

## ADR Template (Planned)
```md
# ADR 00XX — Title
Status: Proposed|Accepted|Rejected|Deprecated|Superseded
Date: YYYY-MM-DD
Deciders: ...
Consulted: ...
Informed: ...
Tags: ...
Supersedes: ...
Superseded-By: ...

## Context and Problem Statement
## Decision Drivers
## Considered Options
## Decision Outcome
## Why This Decision
## Consequences
## Validation Plan
## References
```

## ADR Quality Tests
1. Required metadata and section checks.
2. Status transition checks.
3. Supersession reciprocity checks.
4. Numbering and uniqueness checks.
5. Validation plan and references presence checks.

## References Used in This Iteration
[R15], [R16], [R17], [R18], [R19], [R20], [R21], [R22]

See `docs/deep_research_plan_series/reference-map.md`.
