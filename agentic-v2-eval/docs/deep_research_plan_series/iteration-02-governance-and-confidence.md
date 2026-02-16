# Iteration 02 - Governance and Confidence Controls

## Objective
Upgrade the foundation plan with explicit source trust policy, freshness constraints, confidence scoring, and bounded supervision loops [R1][R3][R8][R10].

## Complexity Delta vs Iteration 01
1. Adds hard governance constraints (trust tiers, provenance requirements).
2. Adds quantitative stop/continue logic with CI components.
3. Adds explicit recency requirement (`>=10` sources in last 183 days).
4. Adds stronger anti-hallucination controls at claim level.

## Source Governance Model
1. Tier A default: official docs/blogs, peer-reviewed publications, recognized institutional sources [R1][R8][R10].
2. Tier B conditional: high-signal community/industry sources with corroboration.
3. Tier C blocked by default: unverifiable/low-signal sources.

Per-source required metadata:
1. URL
2. Publisher
3. Retrieval timestamp
4. Date signal and parsed date
5. Trust tier
6. Claim-to-evidence binding

## Freshness and Recency Policy
1. Recency window: 183 days.
2. Hard gate before success: at least 10 recent sources.
3. Date precedence for counting: HTTP `Last-Modified`, then HTML metadata, then in-text date.

Conversation-derived recency audit found 16 eligible sources in-window as of February 15-16, 2026 [R23]-[R38].

## Confidence Index Policy
Use CI components:
1. Coverage score.
2. Source quality score.
3. Cross-source agreement score.
4. Verification score.
5. Recency score.

Default weighted formula:
`CI = 0.25*coverage + 0.20*source_quality + 0.20*agreement + 0.20*verification + 0.15*recency`.

Stop policy:
1. `CI >= 0.80`
2. `recent_sources_count >= 10`
3. `critical_contradictions == 0`

## Anti-Hallucination and Reliability Controls
1. Critical claims require at least two independent high-trust sources.
2. No uncited factual claims in final report.
3. Contradiction detection before synthesis.
4. Structured intermediate objects between steps.

These controls align with verification-first and grounded-agent guidance [R5][R6][R7][R14].

## References Used in This Iteration
[R1], [R3], [R5], [R6], [R7], [R8], [R10], [R23]-[R38]

See `docs/deep_research_plan_series/reference-map.md`.
