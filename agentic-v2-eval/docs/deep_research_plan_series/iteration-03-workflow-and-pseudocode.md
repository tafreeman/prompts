# Iteration 03 - Workflow Mapping and Planned Pseudocode

## Objective
Translate policy-level planning into a concrete, repository-mapped implementation specification with planned code and pseudocode [R2][R10][R11][R12][R13][R14].

## Complexity Delta vs Iteration 02
1. Adds concrete file-level change plan.
2. Adds workflow YAML structure and round-based step graph.
3. Adds typed contract model pseudocode.
4. Adds orchestration and gate evaluation pseudocode.
5. Adds RAG packaging contract pseudocode.

## Planned Repository Additions
1. `agentic-workflows-v2/agentic_v2/workflows/definitions/deep_research.yaml`
2. `agentic-workflows-v2/agentic_v2/workflows/deep_research_contracts.py`
3. Prompt files for planner/retriever/analysts/verifier/synthesizer.
4. Tests for loader, CI+recency behavior, and RAG packaging.

## Planned Workflow DAG
1. `intake_scope`
2. `source_policy`
3. `retrieval_round1`
4. `analyst_ai_round1`
5. `analyst_swe_round1`
6. `verify_cove_round1`
7. `audit_round1`
8. Repeat for rounds 2-4 via `when` gates.
9. `final_synthesis`
10. `rag_package`

Method mapping:
1. ToT in planning steps [R13].
2. ReAct in retrieval steps [R12].
3. CoVe in verification steps [R14].

## Planned Contracts (Pseudocode Summary)
1. `SourceRecord`
2. `EvidenceItem`
3. `AnalysisNote`
4. `VerificationResult`
5. `ConfidenceReport`

Core gate pseudocode:
```python
def should_continue(ci_report, min_ci=0.80, min_recent_sources=10):
    if ci_report["ci_score"] < min_ci:
        return True
    if ci_report["recent_sources_count"] < min_recent_sources:
        return True
    if ci_report["critical_contradictions"] > 0:
        return True
    return False
```

## Planned Tooling Allowlists
1. Planning/analysis/verifier: `http_get`, `search`, `grep`, structured data tools, memory tools.
2. Retrieval: add `http`, `http_post`, `file_read`, `file_write`.
3. Packaging: `directory_create`, `template_render`, `config_merge`, `json_dump`.
4. High-risk defaults off: `shell`, `shell_exec`, unrestricted git mutation.

## Planned Output Artifacts
1. `rag_manifest.json`
2. `evidence_chunks.jsonl`
3. `citations.json`
4. `claim_graph.json`
5. `final_report.md`

## References Used in This Iteration
[R2], [R3], [R4], [R10], [R11], [R12], [R13], [R14]

See `docs/deep_research_plan_series/reference-map.md`.
