---
name: LATS Self-Refine Evaluator — Agentic Workflow (Standardized)
description: Standardized, best-practice agentic workflow variant of the LATS Self-Refine evaluator. Expands agent roles, assigns tools, provides multi-run plans, and includes example configurations and templates for automated development teams.
type: how_to
---

## Purpose

This document provides a standardized, best-practice agentic workflow based on the LATS Self-Refine pattern. It is focused on producing consistent, reproducible, and measurable agent-driven refinement runs suitable for automated development teams (CI, prompt engineering pipelines, and workflow automation).

## High-level summary

- Outer loop: iterate until a quality threshold or max iterations reached.
- Inner branches (parallel): Criteria Validation (CoVe), Scoring & Feedback (G-Eval), Implementation & Test (ReAct).
- Additions: clearly defined agent roles, explicit tool assignments per role, multi-run orchestration plans, and specialized workflow variants (e.g., Business Process Redesigner).

## Design principles (values)

- Reproducibility: deterministic inputs, versioned prompts, and run manifests.
- Verifiability: independent verification of claims and citations for research-backed criteria.
- Modularity: clear separation of concerns between agents and tools.
- Measurability: quantitative scoring, confidence intervals, and test harnesses.
- Safety: guardrails for sensitive content and rate limits for external calls.

## Defined grading criteria (recommended)

Below is a curated set of well-defined grading criteria recommended for most agentic refinement runs. Each criterion includes a short definition, suggested scoring range, and example checks or tests the Evaluator should run.

1. Clarity (weightable)
  - Definition: How clear and unambiguous the prompt is for the target model/agent.
  - Score range: 0–100
  - Example checks: presence of role statement, explicit output format, and constraint language; automated parse of instructions for ambiguity.

2. Effectiveness (weightable)
  - Definition: Degree to which produced outputs satisfy the user's functional goal.
  - Score range: 0–100
  - Example checks: match against expected-output examples, metric-based comparison (BLEU/ROUGE where applicable), and human-validated correctness samples.

3. Specificity
  - Definition: How targeted and prescriptive the prompt is about desired output structure and content.
  - Score range: 0–100
  - Example checks: presence of template fields, example outputs, and explicit constraints (length, tone, format).

4. Robustness
  - Definition: Performance stability across varied inputs and adversarial cases.
  - Score range: 0–100
  - Example checks: run against adversarial or edge-case inputs, measure variance in outputs, and regression failures.

5. Safety / Compliance
  - Definition: Absence of harmful, biased, or non-compliant content in outputs and adherence to policy.
  - Score range: 0–100
  - Example checks: automated toxicity classification, compliance rule checks, and human review flags for high-risk cases.

6. Conciseness / Efficiency
  - Definition: Prompt yields sufficiently compact outputs and minimizes unnecessary model tokens while preserving correctness.
  - Score range: 0–100
  - Example checks: average token usage per sample, redundancy detection, and brevity vs completeness trade-offs.

7. Interpretability / Traceability
  - Definition: How well the prompt and pipeline produce auditable reasoning or steps that can be traced and validated.
  - Score range: 0–100
  - Example checks: presence of reasoning traces (when required), citation of sources, and structured outputs enabling validation.

8. Maintainability
  - Definition: How easy it is to update the prompt, criteria, and tests over time (clear structure, templating).
  - Score range: 0–100
  - Example checks: use of templates, small diffs between versions, and test coverage for prompt behavior.

9. User Alignment / Stakeholder Fit (for business workflows)
  - Definition: Degree to which output aligns with stated stakeholder requirements and KPIs.
  - Score range: 0–100
  - Example checks: stakeholder acceptance tests, KPI mapping (e.g., time/cost/quality), and expert reviews.

10. Feasibility / Implementability
   - Definition: For process redesign or code-generation prompts, how feasible the proposed outputs are to implement.
   - Score range: 0–100
   - Example checks: sanity checks, resource estimates, and developer acceptance tests.

Usage note: keep the set of active criteria manageable (5–8 for most runs). For specialized workflows (e.g., Business Process Redesigner) include domain-specific criteria such as `process_completeness` or `stakeholder_alignment`.

## Agent roles (expanded)

1. Orchestrator (Coordinator)
   - Purpose: manage iterations, schedule branches, aggregate results, and enforce run-time constraints.
   - Tools: workflow engine (e.g., GitHub Actions/CI, Airflow, Prefect), run manifest (JSON/YAML), logging service.
   - Inputs/Outputs: receives `PROMPT_CONTENT`, run parameters; outputs iteration summary and final artifact.

2. Criteria Validator (CoVe Agent)
   - Purpose: validate grading criteria against literature and internal guidelines; propose adjustments.
   - Tools: citation search (scholar APIs or curated docs), knowledge-base query, document retrieval, ephemeral web fetch (with caching).
   - Behaviour: generate verification questions, independently answer them, and emit `effective_criteria` JSON.

3. Scoring & Feedback Agent (G-Eval Agent)
   - Purpose: run guarded evaluations (G-Eval), produce per-criterion scores, and prioritized feedback.
   - Tools: evaluation harness (local evaluator or cloud G-Eval), test harness for sample input/expected output pairs, metrics calculator.
   - Behaviour: produce weighted score, confidence, failure modes, and prioritized fixes.

4. Implementation Agent (ReAct Agent)
   - Purpose: apply the highest-priority fix, create candidate prompt edits, and run immediate smoke tests.
   - Tools: text diff utilities, prompt templating library, unit test runner for behavior checks, sandboxed model runner.
   - Behaviour: produce before/after diffs, an `updated_prompt`, and `observation` with validation results.

5. Verifier & Monitor (Reflexion Agent)
   - Purpose: observe iteration outcomes, log reflexions, and propose strategy adjustments for next iterations.
   - Tools: telemetry store, run-history DB, visual report generator.

6. Human-in-the-loop Gatekeeper
   - Purpose: approve high-risk changes, review citations, and sign off final artifacts before production.
   - Tools: PR interface, review checklist, automated change summaries.

## Tools & capabilities mapping (per role)

- Orchestrator: CI (GitHub Actions), Prefect/Airflow, run-manifest YAML, centralized logs (ELK/Datadog).
- Criteria Validator: scholarly APIs or cached canonical docs, vector DB (for internal research), citation templates.
- Scoring Agent: g-eval harness (local or cloud), unit tests, adversarial example generator, metric calculator (precision/recall/robustness).
- Implementation Agent: templating libs (Jinja2), diff/patch tools, automated prompt formatter, sandboxed model endpoint.
- Verifier & Monitor: grafana/dashboards, run-history JSONL store, reflexion logger for qualitative notes.

## Run configuration (manifest)

Create a run manifest (example `run-manifest.yaml`) that the Orchestrator uses for reproducible runs.

Example manifest:

```yaml
run_id: lats-selfrefine-2026-01-28
prompt_source: prompts/advanced/my-prompt.md
quality_threshold: 85
max_iterations: 5
batch_size: 8 # number of samples to eval per iteration
grading_criteria:
  clarity: 25
  effectiveness: 30
  specificity: 20
  robustness: 15
  safety: 10
tools:
  citation_db: v1.2
  model_endpoint: local:thot-1
  evaluator: g-eval-local
human_gate: true
notify_on_complete: team-prompteng@org
```

## Multi-run orchestration and workflows

Plan for three execution modes:

1. Exploratory Run (fast, low-cost)
   - Max iterations: 2
   - Batch size: 4
   - Use: quick iterations to find low-hanging improvements.

2. Full Refinement Run (recommended)
   - Max iterations: 5
   - Batch size: 16
   - Use: full improvement cycle with verification and human gate.

3. Regression & Robustness Run (extended)
   - Max iterations: 3
   - Batch size: 64
   - Use: stress testing, adversarial prompts, robustification.

Orchestrator responsibilities:
- schedule runs (cron or manual trigger)
- snapshot `prompt_source` and `run-manifest`
- provision sandbox models and test inputs
- store artifacts and metrics in run-history

## Specialized workflow: Business Process Redesigner

Purpose: repurpose the same agentic loop to redesign/document business processes.

Adaptations:
- Grading criteria: add `process_completeness`, `stakeholder_alignment`, `implementation_feasibility`.
- Tools: BPMN modeler, process mining dataset connectors, stakeholder interview templates.
- Implementation agent: generates process diagrams, role-responsibility matrices, and migration plans.
- Evaluation: run simulation-based validation and KPI mapping (e.g., time-to-complete, cost delta).

Example variables for Business Process run-manifest:

```yaml
grading_criteria:
  clarity: 15
  process_completeness: 30
  stakeholder_alignment: 25
  feasibility: 20
  safety: 10
```

## Example iteration (concise)

Input: `PROMPT_CONTENT` asking the assistant to "Generate deployment checklist for a Django app".

Iteration 1 (branch outputs):
- A (Criteria Validator): finds `robustness` missing; proposes adding `robustness: 10`.
- B (Scoring): rates clarity 60, effectiveness 50, specificity 40 → weighted score 51%.
- C (Implementation): applies a role definition + output format example; produces updated prompt with exact checklist format.
- Synthesis: weighted score 71% (below threshold) → reflexion: next iteration to improve edge-case handling and security checks.

## Templates: JSON outputs

1. Effective criteria (example)

```json
{
  "criteria_valid": true,
  "effective_criteria": {
    "clarity": 25,
    "effectiveness": 30,
    "specificity": 20,
    "robustness": 15,
    "safety": 10
  },
  "adjustments_needed": []
}
```

2. Iteration result

```json
{
  "iteration": 2,
  "weighted_score": 71,
  "per_criterion": {"clarity": 80, "effectiveness": 70, "specificity": 60, "robustness": 60, "safety": 80},
  "top_actions": [
    {"action":"Add edge-case handling and explicit security checks","estimated_improvement":8}
  ],
  "updated_prompt_path":"prompts/advanced/my-prompt.v2.md"
}
```

## Best-practice examples & templates

- Provide clear role/context lines: "You are a concise, expert deployment assistant."
- Always include output format examples and constraints (length, tone, tense).
- Add test cases and an expected-output example for the Scoring Agent to run.

Example prompt snippet (before/after):

<!-- BEFORE -->
Summarize the release notes.

<!-- AFTER -->
You are an expert release-note summarizer.
Summarize the following release notes into 5 bullet points. Each bullet should be 8–15 words, focus on user-visible changes, and include an impact statement.

[RELEASE_NOTES]

Example expected output:

```
- Redesigned login flow reduces average auth time by 20% (UX improvement).
```

## Safety and human gating

- Always route high-impact or novel changes to the Human-in-the-loop Gatekeeper.
- Log all external knowledge fetches and citations used by the Criteria Validator for audit.

## Running locally (quick start)

1. Create `run-manifest.yaml` in the repo.
2. Trigger the Orchestrator (CI job or local runner) with the manifest.
3. Inspect `results/<run_id>/` for iteration artifacts and metrics.

## Metrics to collect

- Weighted score (0–100)
- Per-criterion scores and confidence
- Time per iteration
- Number of human interventions
- Regression test pass rate after edits

## FAQs

- Q: How many parallel branches should I run? A: The canonical LATS + Self-Refine pattern runs three: CoVe, G-Eval, ReAct. You may expand branches for specialized tasks (security, fairness) but keep orchestration overhead in mind.
- Q: When should I stop? A: When weighted score >= quality_threshold OR when human gate requests manual review OR when `max_iterations` reached.

## References (short)

- LATS, Self-Refine, ToT, ReAct, CoVe, Reflexion (see original prompt references for full citations).

---

Variables

| Variable | Required | Description |
|---|---:|---|
| PROMPT_CONTENT | Yes | The prompt text to evaluate |
| QUALITY_THRESHOLD | No | Termination threshold (default: 85) |
| MAX_ITERATIONS | No | Max refinement loops (default: 5) |
| GRADING_CRITERIA | No | JSON/YAML map of criteria and weights |
---
name: LATS Self-Refine Evaluator — Agentic Workflow (Standardized)
description: |-
  A standardized, best-practice variant of the LATS Self-Refine iterative prompt evaluator.
  Expands agent roles, specifies tools per role, and provides execution plans for multiple
  runs and alternative workflows (e.g., business process redesigner). Grounded in proven
  methods (LATS, Self-Refine, ToT, ReAct, CoVe, Reflexion) and designed for reproducible
  multi-agent evaluation and refinement cycles.
type: how_to
---

# LATS Self-Refine Evaluator — Agentic Workflow (Standardized)

## Purpose
Provide a standardized, operational agentic workflow for iterative prompt evaluation and
refinement. The workflow formalizes agent roles, the tools each agent should use, run
planning for multiple executions, and variants for different use-cases such as
business-process redesign. Emphasis is on reproducibility, measurable progress, and
alignment to research-backed patterns.

## Key Principles (Best Practices)
- Clear role separation: minimize overlapping responsibilities to reduce ambiguity.
- Tool-specification per role: list concrete capabilities and expected outputs.
- Iterative orchestration: repeat until objective metric reached or max iterations hit.
- Independent verification: use CoVe-style checks and external sources to reduce hallucination.
- Reflexive learning: capture "what worked / what didn't" to improve next runs.
- Reproducibility: record seeds, system prompts, criteria, and tool versions.

## Agent Roles (Expanded)
Each role is a focused agent with a clear input/output contract.

1. Orchestrator (Coordinator)
   - Responsibility: Manage iteration loop, route artifacts between agents, evaluate termination.
   - Tools: Workflow engine / script (e.g., Python orchestration), task queue, logging.
   - Inputs: PROMPT_CONTENT, GRADING_CRITERIA, CONFIG.
   - Outputs: Iteration plan, consolidated results, termination decision.

2. Researcher (Verifier)
   - Responsibility: Run CoVe-style verification of criteria and claims; gather citations.
   - Tools: Web search / bibliographic search (browser, scholarly APIs), internal knowledge base,
     citation formatter.
   - Outputs: Evidence table mapping criteria/claims to sources, confidence score per claim.

3. Evaluator (Scorer)
   - Responsibility: Apply the grading rubric (G-Eval or other) and produce scores + feedback.
   - Tools: Large language model (configurable), evaluation harness (G-Eval style), automated
     test cases for prompt behavior.
   - Outputs: Per-criterion scores, weighted overall score, prioritized improvement list.

4. Implementer (Editor)
   - Responsibility: Take prioritized fixes and produce concrete edits to the prompt.
   - Tools: LLM for text edits, diff/patch generator, optional code/text validators.
   - Outputs: Updated prompt + change log (before/after snippets), estimated impact.

5. Synthesizer (Integrator)
   - Responsibility: Merge branches (A/B/C), resolve conflicts, propose final candidate.
   - Tools: Merge heuristics, LLM-assisted synthesis, CI checks.
   - Outputs: Synthesized prompt candidate, rationale for selection.

6. Validator (Acceptance Tester)
   - Responsibility: Run the updated prompt on representative inputs, check metrics.
   - Tools: Test harness, sample corpus, unit tests, human-in-the-loop checks.
   - Outputs: Validation report, pass/fail, observed scores.

7. Recorder (Audit & Reflexion)
   - Responsibility: Log iteration artifacts, produce reflexion notes (what worked/didn't), and
     recommended strategy changes.
   - Tools: Structured logging (JSONL), version control tags, experiment tracker.
   - Outputs: Iteration history, reflexion summary.

## Tools Matrix (per role)
- Orchestrator: Python orchestration script, Airflow/Prefect optional, structured logs (JSONL).
- Researcher: Browsing-capable LLM agent or search APIs, semantic search over internal docs.
- Evaluator: Scoring LLM, G-Eval harness, rubric parser, automated metrics calculator.
- Implementer: LLM editor, diff tool, prompt templating engine.
- Synthesizer: LLM summarizer/merger, conflict resolution rules.
- Validator: Test harness, evaluation dataset, A/B testing harness, human review interface.
- Recorder: Experiment DB (MLFlow-like), JSONL artifacts, reproducible run metadata.

## Standardized Iteration Plan (Outer Loop)
1. Orchestrator: start iteration N, provide PROMPT_CONTENT and EFFECTIVE_CRITERIA to agents.
2. Researcher (Branch A): verify criteria and produce adjustments_needed + evidence table.
3. Evaluator (Branch B): score current prompt, produce prioritized fixes and expected impact.
4. Implementer (Branch C): apply top prioritized fix and produce updated prompt candidate.
5. Synthesizer: reconcile outputs, produce synthesized candidate + combined rationale.
6. Validator: run candidate on test set, report scores and regressions.
7. Recorder: save artifacts and generate Reflexion notes.
8. Orchestrator: decide termination (Score >= QUALITY_THRESHOLD or MAX_ITERATIONS reached) or loop.

Notes:
- Branches A/B/C run in parallel where infrastructure allows; their outputs must follow
  clearly defined artifact schemas.
- Each branch should include a short, machine-readable summary at the top of its output
  so the synthesizer can merge without heavy parsing.

## Artifact Schemas (Minimal)
- Evidence table (Researcher): [{criterion, support: true|false, citation, confidence:0-1}]
- Score report (Evaluator): {criterion_scores: {..}, weighted_score:0-100, issues:[..]}
- Patch (Implementer): {before_snippet, after_snippet, change_summary, estimated_delta}
- Validation (Validator): {observed_scores: {...}, regressions:[..], pass:boolean}
- Reflexion (Recorder): {iteration, what_worked:[..], what_failed:[..], next_strategy:[..]}

## Multi-Run Planning
When running multiple executions (e.g., to explore variance or run different workflows):
- Define a run-plan matrix: vary seeds, model versions, grading criteria, or implementation heuristics.
- Track each run with a unique run_id and store full artifacts for later comparison.
- Use paired comparisons (A/B) or statistical tests when comparing variants.
- Recommended: run each configuration at least 3 times with different RNG seeds to assess variance.

## Workflow Variants (Examples)
1. Business Process Redesigner
   - Goal: Transform an existing business process description into an optimized process map.
   - Adjustments:
     - GRADING_CRITERIA: add business metrics (cost, time, compliance, customer impact) and
       weight accordingly.
     - Validator: include domain experts or simulated KPIs.
     - Researcher: use industry standards and regulations as evidence sources.
   - Agents: keep the same roles; Implementer produces process maps (e.g., BPMN snippets) and
     step-level changes; Validator runs scenario-based simulations.

2. Rapid A/B Prompt Tuning
   - Goal: Quickly iterate on variants for production prompts.
   - Adjustments:
     - Shorten MAX_ITERATIONS, prefer high-confidence Evaluator thresholds.
     - Implementer generates multiple parallel candidate patches per iteration.
     - Validator runs live or synthetic A/B tests and captures user metrics.

3. Exploratory Creativity Mode
   - Goal: maximize creative diversity rather than strict scoring.
   - Adjustments:
     - Use diversity-aware scoring in Evaluator (novelty metric).
     - Orchestrator expands branch count to explore multiple divergent edits.

## Termination & Acceptance Criteria
- Primary: weighted_score >= QUALITY_THRESHOLD (configurable).
- Secondary: no meaningful improvement after K consecutive iterations (patience parameter).
- Manual override allowed with documented rationale.

## Logging & Reproducibility
- Always record: model versions, prompts (system + user), seeds, tool versions, and run metadata.
- Persist artifacts in versioned storage and tag runs with human-readable summaries.

## Reflexion Template (each iteration)
- Iteration: N
- Key Change: [short summary]
- Observed Effect: +X% (metric)
- What Worked: [list]
- What Didn't Work: [list]
- Next Strategy: [planned change for next iteration]

## Example: Business Process Redesigner (Run Plan)
```yaml
run_id: bp-redesign-2026-01-28
QUALITY_THRESHOLD: 85
MAX_ITERATIONS: 6
GRADING_CRITERIA:
  cost: 30
  time: 30
  compliance: 20
  customer_experience: 20
seeds: [42, 99, 123]
variant_matrix:
  - model: gpt-4o
    implementer_style: conservative
  - model: gpt-4o-mini
    implementer_style: aggressive
```

## Example Prompt (Orchestrator -> Agents)
Use this exact text — paste as a single message into the chat UI (replace placeholders in square brackets):

```text
You are the Orchestrator. Run one iteration of the LATS Self-Refine Evaluator workflow (Researcher → Evaluator → Implementer → Synthesizer → Validator) on the PROMPT_CONTENT below, using the RUN_MANIFEST and GRADING_CRITERIA provided. Produce machine-readable JSON only, with keys: evidence_table, score_report, patch, validation, synthesis_decision.

RUN_MANIFEST:
quality_threshold: 85
max_iterations: 1
batch_size: 8
human_gate: false

GRADING_CRITERIA:
clarity: 20
specificity: 15
robustness: 15
actionability: 10
testability: 10
alignment_safety: 10
efficiency: 5
reproducibility: 5
business_impact: 10

PROMPT_CONTENT:
[PASTE here the specific prompt text you want evaluated or paste the PROMPT_CONTENT section from `lats-self-refine-evaluator-agentic-workflow.md`]

Instructions:
1) Researcher: verify criteria and return an evidence_table array of objects {criterion, support, citation, confidence}.
2) Evaluator: run the rubric and return score_report {criterion_scores:{...}, weighted_score, rationales:[...]}.
3) Implementer: propose one prioritized patch and return patch {before_snippet, after_snippet, change_summary, estimated_delta}.
4) Validator: run the patch on representative inputs and return validation {observed_scores, regressions, pass}.
5) Synthesizer: return synthesis_decision {decision: continue|stop|human_review, rationale}.

Output format: single JSON object with keys evidence_table, score_report, patch, validation, synthesis_decision. No extra commentary.
```

## Example Minimal Output (Iteration Summary)
- weighted_score: 72
- top_issue: "Missing compliance checkpoints"
- selected_fix: "Insert compliance checkpoint after step 3"
- estimated_improvement: +12%
- decision: continue (MAX_ITERATIONS not reached)

## Implementation Checklist (for teams)
- [ ] Implement Orchestrator with run metadata recording
- [ ] Provide Investigator/Researcher with browsing or KB access
- [ ] Integrate an automated Evaluator harness (G-Eval or similar)
- [ ] Provide Implementer with an edit/patch interface and tests
- [ ] Add Validator test cases and sample corpus
- [ ] Ensure Recorder logs JSONL artifacts and tags runs

## References (Research Foundation)
- LATS, Self-Refine, ToT, ReAct, CoVe, Reflexion and core evaluation literature.
- Use the same canonical citations as the original LATS Self-Refine prompt; include
  domain-specific references for specialized workflows (e.g., BPMN best practices).

## Variables
- PROMPT_CONTENT (required): the raw text to be evaluated/edited.
- QUALITY_THRESHOLD (optional, default 80): numeric threshold to stop.
- MAX_ITERATIONS (optional, default 5): cap on iterations.
- GRADING_CRITERIA (optional): JSON or YAML mapping of criteria to weights.
- RUN_PLAN (optional): matrix describing variants for multi-run experiments.

## Notes for Use
- This variant emphasizes operational clarity: every agent must produce machine-readable
  artifacts so the Orchestrator and Synthesizer can operate programmatically.
- For human-in-the-loop usage, present Synthesizer's candidate and Recorder's reflexion
  to reviewers for acceptance.
- For safety-critical or regulated workflows, include mandatory human approval in the
  Orchestrator termination step.

## JSON Analysis Summary

### Agents
- **Requirements Analyst Pro**: Focused on extracting structured requirements with precision.
- **Technical Architect v2**: Designs scalable and secure system architectures.
- **Autonomous Developer**: Implements specifications with clean code principles.
- **Audit & Security Agent**: Identifies vulnerabilities and ensures code quality.
- **Test Engineering Specialist**: Generates high-coverage test suites.

### Orchestration
- **Task Order**: Sequential execution from requirements analysis to testing.
- **Dependency Graph**: Clear dependencies between agents, with retry policies and rollback plans.
- **Validation Checks**: Schema validation, checksum verification, and security scans.

### Artifacts
- **Templates**: Includes analysis and code generation templates.
- **Expected Files**: Requirements, architecture docs, models, and tests.

### Tests
- **Unit Tests**: Focused on individual agent outputs.
- **Integration Tests**: Validates the pipeline from requirements to testing.
- **E2E Tests**: Ensures the full workflow operates as expected.

### Monitoring
- **Metrics**: Agent pass rate, average loop iterations, and token-to-SLOC ratio.
- **Alerts**: Security gate failures and model latency thresholds.

### Rollout
- **Canary Steps**: Gradual rollout from shadow mode to production.
- **Validation Gate**: Requires high average scores in staging.

### Risks
- **Model Instability**: Mitigated with automated benchmarking.
- **Schema Evolution Friction**: Addressed with versioned schemas.

### Branch Evaluations
- **STRICT_SCHEMA_CONTRACT**: Chosen for its strong auditability.
- **RECURSIVE_REFINEMENT**: High code quality but slower execution.
- **DECOUPLED_EVENT_STREAM**: Scalable but complex infrastructure.

### Role Alignment
- **Orchestrator**: Manages the task order and dependency graph defined in the JSON orchestration section.
- **Researcher**: Corresponds to the Requirements Analyst Pro agent, focusing on structured requirements extraction.
- **Evaluator**: Matches the Audit & Security Agent, ensuring code quality and identifying vulnerabilities.
- **Implementer**: Aligned with the Autonomous Developer agent, implementing clean and modular code.
- **Synthesizer**: Represents the Technical Architect v2 agent, integrating system designs and resolving conflicts.
- **Validator**: Matches the Test Engineering Specialist, generating and running high-coverage test suites.
- **Recorder**: Captures logs and reflexion notes, ensuring reproducibility and auditability.

### Output Mapping
- **Evidence Table**: Generated by the Researcher agent, mapping criteria to sources.
- **Score Report**: Produced by the Evaluator agent, detailing scores and prioritized improvements.
- **Patch**: Created by the Implementer agent, summarizing code changes and their impact.
- **Validation**: Generated by the Validator agent, reporting observed scores and regressions.
- **Synthesis Decision**: Managed by the Synthesizer agent, deciding on the next steps.

### Workflow Enhancements
- **Retry Policy**: Ensures robustness with exponential backoff and fallback mechanisms.
- **Validation Checks**: Strengthened with schema validation, checksum verification, and security scans.
- **Branch Evaluations**: Provides flexibility to choose the best strategy based on trade-offs.

## Combined Machine-readable Analysis
The JSON below merges the external agent/config specification provided by the user with the latest single-iteration run analysis produced by the Orchestrator and additional analysis results supplied by the user. Use this block for programmatic ingestion or to seed a runner.

```json
{
  "agents_config": {
    "agents": [
      {"id":"requirements_agent","name":"Requirements Analyst Pro","role":"Business Requirements Parser","category":"Analysis","recommended_model":"gh:openai/gpt-4o-mini","recommended_temperature":0.1,"max_tokens":4096,"tier":"standard","notes":"Focused on extraction precision and Given/When/Then story formatting."},
      {"id":"architect_agent","name":"Technical Architect v2","role":"System Architecture Designer","category":"Design","recommended_model":"gh:openai/o3-mini","recommended_temperature":0.2,"max_tokens":8192,"tier":"premium","notes":"Uses recursive reasoning to validate architectural trade-offs."},
      {"id":"coder_agent","name":"Autonomous Developer","role":"Code Generation Specialist","category":"Build","recommended_model":"gh:openai/gpt-4o","recommended_temperature":0.0,"max_tokens":16384,"tier":"premium","notes":"Zero temperature for maximum determinism and code consistency."},
      {"id":"reviewer_agent","name":"Audit & Security Agent","role":"Security and Quality Analyst","category":"Quality","recommended_model":"gh:openai/o4-mini","recommended_temperature":0.3,"max_tokens":8192,"tier":"premium","notes":"Optimized for identifying subtle logic flaws and security anti-patterns."},
      {"id":"test_agent","name":"Test Engineering Specialist","role":"Test Suite Creator","category":"Quality","recommended_model":"gh:openai/gpt-4o","recommended_temperature":0.1,"max_tokens":8192,"tier":"standard","notes":"Generates idempotent unit and integration tests with high coverage."},
      {"id":"vision_analyst","name":"Vision Analyst","role":"Requirement Extraction","category":"analysis","recommended_model":"gh:openai/gpt-4o","recommended_temperature":0.2,"max_tokens":4096,"tier":"cloud_premium","notes":"Extracts text and UI components from mockup images."},
      {"id":"business_analyst","name":"Business Analyst","role":"Requirement Synthesis","category":"analysis","recommended_model":"gh:openai/o1","recommended_temperature":0.3,"max_tokens":8192,"tier":"cloud_reasoning","notes":"Synthesizes raw inputs into structured user stories and acceptance criteria."},
      {"id":"system_architect","name":"System Architect","role":"System Design","category":"design","recommended_model":"gh:deepseek/deepseek-r1","recommended_temperature":0.2,"max_tokens":8192,"tier":"cloud_reasoning","notes":"Defines tech stack, DB schema, and API specifications."},
      {"id":"backend_dev","name":"Backend Engineer","role":"Implementation","category":"build","recommended_model":"gh:deepseek/deepseek-v3","recommended_temperature":0.1,"max_tokens":8192,"tier":"cloud_coding","notes":"Implements API endpoints and business logic."},
      {"id":"frontend_dev","name":"Frontend Engineer","role":"Implementation","category":"build","recommended_model":"gh:deepseek/deepseek-v3","recommended_temperature":0.1,"max_tokens":8192,"tier":"cloud_coding","notes":"Implements UI components and integrates with API."},
      {"id":"qa_engineer","name":"QA Engineer","role":"Quality Assurance","category":"quality","recommended_model":"gh:openai/gpt-4o","recommended_temperature":0.0,"max_tokens":4096,"tier":"cloud_std","notes":"Generates test cases and validates implementation against requirements."},
      {"id":"project_judge","name":"Project Judge","role":"Final Evaluation","category":"quality","recommended_model":"gh:openai/gpt-5","recommended_temperature":0.0,"max_tokens":2048,"tier":"cloud_premium","notes":"Provides final pass/fail grade and quality assessment."}
    ],
    "agent_prompts": {
      "requirements_agent": {"system_prompt":"You are a senior business analyst. Parse the user requirements into a strictly structured JSON containing user_stories, entities, and non_functional_requirements. Use Gherkin syntax for acceptance criteria.","user_instructions":"Analyze the following text and extract structured requirements: {input_text}","input_schema":{"type":"object","properties":{"input_text":{"type":"string"}},"required":["input_text"]},"output_schema":{"type":"object","properties":{"user_stories":{"type":"array","items":{"type":"object"}},"entities":{"type":"array","items":{"type":"string"}}}},"safety_and_privacy":"Ensure all PII and sensitive internal project names are anonymized before output."},
      "architect_agent": {"system_prompt":"You are a lead system architect. Given a set of user stories, design a decoupled system architecture including tech stack and database schema. Focus on scalability and security boundaries.","user_instructions":"Design architecture for stories: {user_stories}","input_schema":{"type":"object","properties":{"user_stories":{"type":"array"}}},"output_schema":{"type":"object","properties":{"tech_stack":{"type":"object"},"schema_ddl":{"type":"string"},"components":{"type":"array"}}},"safety_and_privacy":"Abide by Least Privilege principle in all architectural designs."},
      "coder_agent": {"system_prompt":"You are a high-performance software engineer. Implement the provided specifications using clean code principles and comprehensive type annotations. Ensure all code is modular and testable.","user_instructions":"Implement the following component: {component_name} in {language} with specs: {specs}","input_schema":{"type":"object","properties":{"component_name":{"type":"string"},"language":{"type":"string"},"specs":{"type":"object"}}},"output_schema":{"type":"object","properties":{"code":{"type":"string"},"file_path":{"type":"string"},"imports":{"type":"array"}}},"safety_and_privacy":"Never include API keys or secrets in the generated code."},
      "reviewer_agent": {"system_prompt":"You are a code auditor. Check the submitted code for OWASP vulnerabilities, performance bottlenecks, and adherence to DRY/SOLID principles. Rate each review with clear severity levels.","user_instructions":"Audit this code: {code_content}","input_schema":{"type":"object","properties":{"code_content":{"type":"string"}}},"output_schema":{"type":"object","properties":{"score":{"type":"integer"},"issues":{"type":"array","items":{"type":"object"}},"approved":{"type":"boolean"}}},"safety_and_privacy":"Only output metadata about vulnerabilities, do not repeat sensitive logic in logs."},
      "test_agent": {"system_prompt":"You are a QA automation engineer. Generate high-coverage test suites (Pytest/Jest) that include unit, integration, and edge-case tests. Use Arrange-Act-Assert pattern.","user_instructions":"Write tests for: {code_content} at {file_path}","input_schema":{"type":"object","properties":{"code_content":{"type":"string"},"file_path":{"type":"string"}}},"output_schema":{"type":"object","properties":{"test_code":{"type":"string"},"test_path":{"type":"string"}}},"safety_and_privacy":"Do not hardcode production data paths in test fixtures."},
      "vision_analyst": {"system_prompt":"You are an expert Vision Analyst specialized in UI/UX decomposition. Your goal is to extract every visual element, text label, and layout pattern from the provided mockup images. Output a structured JSON describing the component hierarchy.","user_instructions":"Analyze the attached image(s) and produce a component map.","input_schema":{"type":"object","properties":{"images":{"type":"array","items":{"type":"string","format":"base64"}}}},"output_schema":{"type":"object","properties":{"components":{"type":"array","items":{"type":"object","properties":{"name":{"type":"string"},"type":{"type":"string"},"description":{"type":"string"}}}},"layout_description":{"type":"string"}}},"safety_and_privacy":"Do not extract PII if present in mockups. obscure names/emails."},
      "business_analyst": {"system_prompt":"You are a Senior Business Analyst. Transform raw requirements and vision analysis into a formal requirements specification. Include functional requirements, non-functional requirements, and user stories with acceptance criteria.","user_instructions":"Convert these inputs into a formalized project specification.","input_schema":{"type":"object","properties":{"raw_text":{"type":"string"},"vision_analysis":{"type":"object"}}},"output_schema":{"type":"object","properties":{"functional_requirements":{"type":"array","items":{"type":"string"}},"user_stories":{"type":"array","items":{"type":"object"}}}},"safety_and_privacy":"Ensure no business-critical secrets are leaked in the output."},
      "system_architect": {"system_prompt":"You are a Principal System Architect. Based on the requirements, design the system architecture. You MUST output: 1. The Technology Stack. 2. The Database Schema (SQL). 3. The API Specification (OpenAPI 3.1 JSON). Ensure the design is scalable and secure.","user_instructions":"Design the system architecture for the provided requirements.","input_schema":{"type":"object","properties":{"requirements":{"type":"object"}}},"output_schema":{"type":"object","properties":{"tech_stack":{"type":"object"},"database_schema_sql":{"type":"string"},"openapi_spec":{"type":"object"}}},"safety_and_privacy":"Adhere to secure-by-design principles."},
      "backend_dev": {"system_prompt":"You are a Senior Backend Engineer. Implement the application logic based EXACTLY on the provided OpenAPI specification and Database Schema. Write clean, tested code.","user_instructions":"Generate the backend codebase.","input_schema":{"type":"object","properties":{"openapi_spec":{"type":"object"},"db_schema":{"type":"string"},"stack":{"type":"string"}}},"output_schema":{"type":"object","properties":{"file_structure":{"type":"object"},"files":{"type":"array","items":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}}}}}},"safety_and_privacy":"Sanitize all SQL inputs. No hardcoded credentials."},
      "frontend_dev": {"system_prompt":"You are a Senior Frontend Engineer. Implement UI components per the design and integrate with the provided OpenAPI endpoints. Produce modular, accessible components.","user_instructions":"Generate frontend code for components: {component_specs}","input_schema":{"type":"object","properties":{"component_specs":{"type":"array"}}},"output_schema":{"type":"object","properties":{"file_structure":{"type":"object"},"files":{"type":"array","items":{"type":"object","properties":{"path":{"type":"string"},"content":{"type":"string"}}}}}},"safety_and_privacy":"Do not include production secrets in front-end code."},
      "qa_engineer": {"system_prompt":"You are a QA Engineer. Generate test plans and execute validation against the provided implementation outputs. Ensure feature parity with requirements.","user_instructions":"Run tests for: {file_structure} and return results.","input_schema":{"type":"object","properties":{"file_structure":{"type":"object"}}},"output_schema":{"type":"object","properties":{"results":{"type":"object"},"coverage":{"type":"number"}}},"safety_and_privacy":"Do not include sensitive test data in logs."},
      "project_judge": {"system_prompt":"You are a Project Judge. Evaluate final artifacts and provide a pass/fail decision with reasoning and key metrics.","user_instructions":"Assess the project deliverables and return a verdict.","input_schema":{"type":"object","properties":{"artifacts":{"type":"object"}}},"output_schema":{"type":"object","properties":{"verdict":{"type":"string"},"score":{"type":"number"},"notes":{"type":"string"}}},"safety_and_privacy":"Ensure evaluation does not leak confidential info."}
    },
    "orchestration": {
      "task_order": ["requirements_agent","architect_agent","coder_agent","reviewer_agent","test_agent"],
      "dependency_graph": {
        "edges": [
          {"from":"requirements_agent","to":"architect_agent"},
          {"from":"architect_agent","to":"coder_agent"},
          {"from":"coder_agent","to":"reviewer_agent"},
          {"from":"reviewer_agent","to":"coder_agent","condition":"approved == false"},
          {"from":"reviewer_agent","to":"test_agent","condition":"approved == true"},
          {"from":"vision_analyst","to":"business_analyst"},
          {"from":"business_analyst","to":"system_architect"},
          {"from":"system_architect","to":"backend_dev"},
          {"from":"system_architect","to":"frontend_dev"},
          {"from":"backend_dev","to":"qa_engineer"},
          {"from":"frontend_dev","to":"qa_engineer"},
          {"from":"qa_engineer","to":"project_judge"}
        ]
      },
      "retry_policy":"Exponential backoff: 3 retries, base 2s, factor 2.0. Secondary fallback to local models on 401/429 errors.",
      "rollback_plan":"Atomic artifact deletion: All files generated in the current execution session are deleted upon unrecoverable error; state is rolled back to the last passing step checkpoint.",
      "validation_checks": [
        {"name":"Strict Schema Validation","type":"schema","pass_criteria":"JSON output matches agent.output_schema exactly."},
        {"name":"Checksum Verification","type":"checksum","pass_criteria":"SHA-256 of generated files matches written byte-stream."},
        {"name":"Unit Test Coverage","type":"test","pass_criteria":"Generated tests pass and branch coverage >= 90%."},
        {"name":"Static Analysis","type":"lint","pass_criteria":"Zero errors from language-appropriate linters (ESLint/Pyright)."},
        {"name":"Security Policy Scan","type":"security","pass_criteria":"Zero High/Critical vulnerabilities detected by automated scanner agent."},
        {"name":"OpenAPI Validity","type":"lint","pass_criteria":"Generated OpenAPI spec must be valid according to Swagger/OpenAPI 3.1 standards."},
        {"name":"Dependency Check","type":"security","pass_criteria":"No vulnerable dependencies (CVE check) in generated package.json/requirements.txt."}
      ],
      "seed": 12345
    },
    "artifacts": {
      "templates": {"prompt_templates":["multiagent_workflows/templates/analysis.j2","multiagent_workflows/templates/code_gen.j2","Analysis Template v2.1","Architecture Decision Record (ADR) Template"],"code_snippets":["fastapi_base_router","react_component_skeleton","Standard Dockerfile","CI/CD Pipeline YAML"]},
    "expected_files":["specs/requirements.json","docs/architecture.md","src/models.py","tests/test_logic.py","README.md","openapi.json","schema.sql","src/main.","tests/test_"]
    },
    "tests": {
      "unit":[{"agent":"coder_agent","input":{"component_name":"Auth","language":"python"},"expected_output":"class AuthController"},{"agent":"requirements_agent","input":{"input_text":"Users can reset passwords via email."},"expected_output_contains":"Password Reset"},{"agent":"reviewer_agent","input":{"code_content":"import subprocess; subprocess.call(cmd)"},"expected_output_contains":"severity: High"}],
      "integration":["test_requirements_to_arch_pipeline","test_coder_reviewer_feedback_loop","Architect output (Spec) is consumable by Backend Agent","Backend output (Code) passes QA Agent's generated tests"],
      "e2e":["test_full_fullstack_gen_workflow","Full flow: 'Create a Todo App' -> Working Python/React code","Full flow: 'Create a Landing Page for Pet Store' -> HTML/CSS","Full flow: 'Refactor this code' -> Improved code with diff"],
      "test_coverage_targets":{"percent":90},
      "ci_instructions":"npm test && pytest tests/ --cov=src --cov-fail-under=90; Run pytest tests/workflow -n auto"
    },
    "monitoring": {
      "metrics":[{"name":"Agent Pass Rate","target":">95%","collection_method":"Workflow execution logs"},{"name":"Average Loop Iterations","target":"<1.5","collection_method":"Trace analysis of reviewer feedback"},{"name":"Token-to-SLOC Ratio","target":"<200:1","collection_method":"Token counting middleware"},{"name":"stage_latency_ms","target":"300000","collection_method":"trace_span"},{"name":"total_cost_usd","target":"2.00","collection_method":"token_counter"},{"name":"validation_failure_rate","target":"0.1","collection_method":"log_aggregation"}],
      "alerts":[{"name":"Security Gate Failure","threshold":">0","action":"Immediate workflow halt and human notification"},{"name":"Model Latency P99","threshold":">120s","action":"Redirect traffic to fallback tier"},{"name":"High Cost Alert","threshold":"3.00 USD per run","action":"Notify Administrator & Pause Workflow"},{"name":"Stalled Workflow","threshold":"No activity for 10 minutes","action":"Kill & Retry"}],
      "dashboards":["Agent Reliability Matrix","Cost Per Workflow Run","Code Quality Progress","Workflow Overview (Grafana)","Cost Analysis (Metabase)"]
    },
    "rollout": {"canary_steps":["10% Shadow Mode","30% Internal Beta","100% Production","50%"],"validation_gate":"Minimum average score of 8/10 across 50 consecutive runs in staging.","rollback_criteria":"Error rate > 5% within any 15-minute window."},
    "risks": [{"id":"model_instability","description":"Upstream API changes break prompt grounding.","severity":"High","mitigation":"Frequent automated benchmarking with HumanEval datasets.","residual_risk":"Low"},{"id":"schema_evolution_friction","description":"Rigid schemas prevent rapid feature adaptation.","severity":"Medium","mitigation":"Versioned schemas and semantic fallback logic.","residual_risk":"Medium"},{"id":"R01","description":"Model hallucination in API contracts leading to integration failure","severity":"High","mitigation":"Strict OpenAPI schema enforcement and 'Contract-First' gating.","residual_risk":"Medium"},{"id":"R02","description":"Infinite loops in self-correction","severity":"Medium","mitigation":"Hard limit of 2 retries per stage.","residual_risk":"Low"},{"id":"R03","description":"Code generation introduces security vulnerabilities","severity":"High","mitigation":"Automated security scanning (SAST) in the QA loop.","residual_risk":"Low"}],
    "branch_evaluations": [{"branch_id":"STRICT_SCHEMA_CONTRACT","score":94,"rationale":"Strongest auditability. Enforcing JSON schemas between every agent minimizes 'silent failures'.","trade_offs":"Adds development overhead; requires predefined schemas for all tasks.","chosen":true},{"branch_id":"RECURSIVE_REFINEMENT","score":88,"rationale":"Produces higher code quality via iterative loops, but latency is 3x higher.","trade_offs":"High cost and unpredictable execution duration; better for batch tasks.","chosen":false},{"branch_id":"DECOUPLED_EVENT_STREAM","score":82,"rationale":"High horizontal scalability and fault tolerance; every agent step is a standalone message.","trade_offs":"Increased infrastructure complexity (Redis/RabbitMQ required).","chosen":false},{"branch_id":"Branch A (Waterfall)","score":75,"rationale":"High reliability but too slow and expensive due to excessive gating.","chosen":false},{"branch_id":"Branch B (Swarm)","score":80,"rationale":"Fastest latency but high risk of integration failure due to loose coupling.","chosen":false},{"branch_id":"Branch D (Hybrid Contract-First)","score":88,"rationale":"Balances speed (parallel build) with reliability (gated API design). Best trade-off for complex full-stack apps.","chosen":true}],
    "reproducible_seed":4022
  },
  "latest_run_analysis": {
    "evidence_table": [
      {"criterion":"clarity","support":true,"citation":"OpenAI. \"Best practices for prompt design.\" 2024.","confidence":0.9},
      {"criterion":"specificity","support":true,"citation":"DAIR.AI Prompting Guide. 2024.","confidence":0.85},
      {"criterion":"robustness","support":true,"citation":"Madaan et al., \"Self-Refine\", 2023.","confidence":0.82},
      {"criterion":"actionability","support":true,"citation":"Anthropic / Industry prompt engineering guides (2023-2024).","confidence":0.8},
      {"criterion":"testability","support":true,"citation":"G-Eval / evaluation-harness literature (2023-2024).","confidence":0.85},
      {"criterion":"alignment_safety","support":true,"citation":"Dhuliawala et al., \"Chain-of-Verification\", 2023; Shinn et al., \"Reflexion\", 2023.","confidence":0.88},
      {"criterion":"efficiency","support":true,"citation":"Operational cost & latency best-practices (OpenAI/DAIR 2024).","confidence":0.75},
      {"criterion":"reproducibility","support":true,"citation":"ML experiment tracking best-practices (MLFlow docs, 2022-2024).","confidence":0.9},
      {"criterion":"business_impact","support":true,"citation":"DAIR.AI / industry case studies linking prompts to KPIs (2023-2024).","confidence":0.78}
    ],
    "score_report": {"criterion_scores":{"clarity":85,"specificity":70,"robustness":65,"actionability":75,"testability":60,"alignment_safety":80,"efficiency":70,"reproducibility":65,"business_impact":60},"weighted_score":71.5,"rationales":["Clarity (85): Roles and goals are well described, but some operational steps lack explicit examples.","Specificity (70): Many responsibilities and artifacts are listed, but few concrete templates or examples are provided.","Robustness (65): Mentions edge-case handling and verification but does not provide explicit fallback behaviors or error modes.","Actionability (75): Prompt defines roles and artifacts, enabling implementation, but lacks ready-to-run templates and test harness snippets.","Testability (60): Specifies validator role and test harness conceptually, but contains no representative test cases or pass/fail criteria.","Alignment & Safety (80): Addresses safety and manual gates; missing detailed guardrail templates for regulated workflows.","Efficiency (70): Reasonable structure but verbose in places; could be more concise to lower cost/latency.","Reproducibility (65): Recommends recording metadata but lacks explicit reproducible run templates (system prompts, seeds).","Business Impact (60): Mentions business variants but does not embed KPI templates or measurement guidance in the main flow."]},
    "patch": {"before_snippet":"## Example Prompt (Orchestrator -> Agents)\\n- PROMPT_CONTENT: full original business process description\\n- EFFECTIVE_CRITERIA: derived from Researcher or defaults\\n- TASK: run iteration N using branches A/B/C and return the standard artifact schemas","after_snippet":"## Example Prompt (Orchestrator -> Agents) — Chat-ready & Runner-friendly\\n- PROMPT_CONTENT: <full original business process description or prompt under test>\\n- EFFECTIVE_CRITERIA: use provided GRADING_CRITERIA YAML or Researcher-adjusted criteria\\n- TASK: Run one iteration (N=1) with branches A/B/C in parallel where possible. Return the standard artifact schemas (evidence_table, score_report, patch, validation, synthesis_decision) as machine-readable JSON.\\n\\nRepresentative test cases (include at least 3):\\n1) Minimal input: short process description (expected: high-level map + 3 optimizations)\\n2) Complex input: multi-step process with compliance constraints (expected: insert checkpoints)\\n3) Edge case: missing actors or ambiguous steps (expected: clarifying questions or fallback)\\n\\nRepresentative KPI template (for Business Impact):\\n- KPI_name: \"Average cycle time (min)\"; baseline: <value>; expected_delta: -X%\\n- KPI_name: \"Cost per transaction ($)\"; baseline: <value>; expected_delta: -Y%\\n- KPI_name: \"Compliance failures per 1000\"; baseline: <value>; expected_delta: 0 or lower\\n\\nRunner notes:\\n- Provide seed, model version, and system prompts in run metadata.\\n- Return brief machine-readable summaries at top of each branch output for easy synthesis.\\n\\nExample single-turn chat payload (copy/paste):\\n\"You are the Researcher/Evaluator/Implementer/Validator as assigned. Use PROMPT_CONTENT and GRADING_CRITERIA. Return the required artifact schema as JSON only.\"","change_summary":"Expand a terse example prompt into a chat-ready, runner-friendly block: add representative test cases, KPI template for business impact, runner notes (seed/model metadata), and an example single-turn chat payload. These additions make the prompt actionable, testable, and more specific for automated runs.","estimated_delta":12},
    "validation": {"observed_scores":{"clarity":90,"specificity":82,"robustness":70,"actionability":85,"testability":78,"alignment_safety":82,"efficiency":72,"reproducibility":75,"business_impact":74},"weighted_score":80.05,"regressions":[],"pass":false},
    "synthesis_decision": {"decision":"human_review","rationale":"Patch produced measurable improvements (weighted_score 80.05 → up ~8.6 points) but did not reach the quality_threshold (85). max_iterations=1 reached, human_gate=false but threshold unmet; recommend human review or schedule additional automated iterations with expanded testcases, stronger KPI mapping, and explicit reproducibility templates."}
  }
}
```

## Improvements Made (iteration 1)
- Patch applied: expanded the "Example Prompt (Orchestrator -> Agents)" into a chat-ready, runner-friendly block (added representative test cases, KPI template for business impact, runner notes including seed/model metadata, and an example single-turn chat payload).
- Observed effect: estimated weighted-score improvement +12 (from 71.5 → 80.05). Validation shows no regressions but did not reach quality_threshold (85); `pass`: false.
- Artifacts produced: machine-readable evidence_table, score_report, patch, validation, and synthesis_decision (see JSON block above).

## Pending Improvements / Next Actions

Below are concrete templates, examples, and implementation notes that address the pending improvements. These are copy-paste-ready to include in run manifests, validator harnesses, and orchestration scripts.

### 1) KPI & Measurement: Business Impact baselines and examples (owner: Business Analyst)

Add a `business_kpis` block to run manifests so validators can compute deltas programmatically and report statistical significance.

Example manifest snippet:

```yaml
business_kpis:
  baseline_conversion_rate: 0.12            # current conversion rate (12%)
  target_delta_pct: 0.05                    # expected relative improvement (5%)
  baseline_time_to_task_minutes: 18        # baseline minutes to complete task
  target_time_reduction_pct: 0.10          # expected relative reduction (10%)
  baseline_error_rate: 0.035               # baseline error rate (3.5%)
  target_error_rate_abs: 0.02              # absolute error-rate target (2%)
  measurement_window: 1000                 # number of validation samples for KPI measurement
  business_metric_examples:
    - name: "conversion_rate"
      description: "Percent of users completing desired action after using generated artifact"
    - name: "time_to_complete"
      description: "Median minutes to complete task using generated instructions"
    - name: "error_rate"
      description: "Percent of outputs flagged as incorrect by validators"
```

Validator guidance: compute observed KPI values over `measurement_window` samples, report delta = (observed - baseline) / baseline and a 95% confidence interval; flag statistical significance if CI excludes zero.

### 2) Reproducibility Templates: system prompts, seeds, model-version (owner: Orchestrator)

Ensure the `run-manifest` records system prompts, exact model identifiers, and RNG seeds. Example:

```yaml
run_id: lats-selfrefine-2026-01-28
prompt_source: prompts/advanced/my-prompt.md
system_prompt: |
  You are an expert prompt engineering verifier. Provide concise, auditable JSON outputs only.
model_version: "gpt-4o-mini@2026-01-28"  # record exact model id and version/date
seeds: [42, 99, 123]                       # RNG seeds to run for variance estimation
quality_threshold: 85
max_iterations: 5
batch_size: 8
grading_criteria: { clarity: 25, effectiveness: 30, specificity: 20, robustness: 15, safety: 10 }
tools:
  citation_db: v1.2
  model_endpoint: local:thot-1
  evaluator: g-eval-local
human_gate: true
notify_on_complete: team-prompteng@org
```

Orchestrator requirement: snapshot and persist `system_prompt`, `model_version`, and `seeds` with every run artifact so runs are fully reproducible.

### 3) Validator Expansion: test cases and automatic pass/fail criteria (owner: QA Engineer)

Provide a validator output schema and clear pass/fail rules. Example output schema (JSON):

```json
{
  "run_id": "string",
  "iteration": 1,
  "observed_scores": {"clarity": 0, "effectiveness": 0},
  "weighted_score": 0,
  "kpis": {"conversion_rate": 0.0, "time_to_complete": 0.0, "error_rate": 0.0},
  "pass": true,
  "reasons": ["list of failing checks"],
  "confidence_intervals": {"conversion_rate": [0.0,0.0]}
}
```

Pass/fail rules (configurable):
- Weighted score >= quality_threshold -> pass
- AND required business KPI deltas meet targets (e.g., conversion delta >= target_delta_pct) -> pass
- AND no regression in critical criteria (e.g., safety drop > 5 points) -> pass

Representative validator test sets (place under `validator/tests/`):
- functional_samples.jsonl (100 labeled I/O pairs, expected pass rate >= 90%)
- adversarial_samples.jsonl (50 adversarial/edge cases, allowed weighted_score drop <= 8 points)
- safety_samples.jsonl (30 safety/red-team cases, zero high-severity violations allowed)

Add a `validator_tests` manifest block:

```yaml
validator_tests:
  functional_tests: data/validator/functional_samples.jsonl
  adversarial_tests: data/validator/adversarial_samples.jsonl
  safety_tests: data/validator/safety_samples.jsonl
  required_pass_rates:
    functional: 0.9
    adversarial: 0.7
    safety: 1.0
```

Implementation note: build test runners that aggregate sample-level metrics, compute weighted_score, KPIs, and set `pass` according to the rules. Persist raw outputs to `results/<run_id>/validator/`.

### 4) Safety & Compliance guardrails and human gate (owner: Reviewer Agent / Human Gatekeeper)

Add a `compliance` block to run-manifests and require human approval for regulated workflows.

```yaml
compliance:
  regulated: true
  regulations: ["GDPR","HIPAA"]
  mandatory_human_gate: true
  approval_template:
    approver_role: "Reviewer Agent / Human Gatekeeper"
    checklist:
      - "Verify citations for external claims"
      - "Confirm no PII leakage in outputs"
      - "Confirm risk assessment document attached"
      - "Sign-off: APPROVE | REJECT | REQUEST_CHANGES"
```

Human gate behaviour: if `mandatory_human_gate` is true the Orchestrator must open a review ticket or PR containing run artifacts and the compliance checklist. Only `APPROVE` moves artifacts to production.

### 5) Additional Iterations: seeds and model tiers orchestration (owner: Orchestrator)

Add an `iteration_plan` manifest to run multiple seeds and model tiers automatically.

```yaml
iteration_plan:
  seeds: [42,99,123]
  model_tiers: ["gpt-4o-mini@2026-01-28","local:thot-1@2026-01-28"]
  runs_per_variant: 1
  max_iterations: 3
  stop_on_threshold: true
```

Orchestrator behavior: for each model_tier and seed, run the iteration loop, append results to `results/<run_id>/matrix_results.jsonl`, then compute mean and variance across seeds/tiers. If mean weighted_score >= quality_threshold then success; otherwise initiate human review.

Example local runner (PowerShell):

```powershell
# from repository root
python -m tools.prompteval prompts/advanced/lats-self-refine-evaluator-agentic-workflow.md \
  --manifest run-manifest.yaml --iteration-plan iteration-plan.yaml --output results/lats-matrix.jsonl
```

### 6) Human Review: decision process & checklist when threshold not met (owner: Human Gatekeeper)

If after the iteration_plan the best mean weighted_score < QUALITY_THRESHOLD, the Orchestrator should create a human-review ticket including:

- Summary: run_id, best_weighted_score, best_model_tier, best_seed
- Attachments: evidence_table.json, score_report.json, patch.diff, validation_report.json, KPI report
- Reviewer checklist:
  - [ ] Confirm `system_prompt` and `model_version` are appropriate
  - [ ] Review top 3 failing criteria and suggested patches
  - [ ] Verify KPI measurement methodology and data quality
  - [ ] Assess safety/compliance risks and confirm mitigations
  - [ ] Provide actionable edits or request targeted iteration
  - [ ] Approve or request changes (use approval template)

Escalation: if reviewers request changes, Orchestrator runs a focused iteration with reviewer edits until approval or `max_manual_review_cycles` exceeded (default 3).

---

These additions are intended to be direct, implementable artifacts for run manifests, the Validator harness, and the Orchestrator. Implementers should wire the Orchestrator to persist artifacts and open PRs/tickets when human gates are required.

## Run History (recorded runs)
The table below lists recorded automated runs and their key outcomes — use these entries for audit and trend analysis.

```json
{
  "run_history": [
    {
      "run_id": "initial_eval_2026-01-28_0",
      "description": "Initial single-iteration evaluation of PROMPT_CONTENT before applying patch",
      "run_manifest": {"quality_threshold":85, "max_iterations":1, "batch_size":8, "human_gate":false},
      "scores": {"weighted_score":71.5, "per_criterion": {"clarity":85, "specificity":70, "robustness":65, "actionability":75, "testability":60, "alignment_safety":80, "efficiency":70, "reproducibility":65, "business_impact":60}},
      "artifacts": ["evidence_table","score_report"],
      "decision": "continue",
      "notes": "Identified need for template examples and KPI mapping"
    },
    {
      "run_id": "patch_applied_eval_2026-01-28_1",
      "description": "Applied Implementer patch (chat-ready runner block) and re-ran validation",
      "run_manifest": {"quality_threshold":85, "max_iterations":1, "batch_size":8, "human_gate":false},
      "scores": {"weighted_score":80.05, "per_criterion": {"clarity":90, "specificity":82, "robustness":70, "actionability":85, "testability":78, "alignment_safety":82, "efficiency":72, "reproducibility":75, "business_impact":74}},
      "artifacts": ["evidence_table","score_report","patch","validation"],
      "decision": "human_review",
      "notes": "Patch improved scores but did not cross threshold; recommended human review or further automated iterations"
    }
  ],
  "planned_runs": [
    {"run_id":"multi_seed_refinement","seeds":[42,99,123],"max_iterations":3,"notes":"Run 3 configurations to measure variance and aim to reach threshold 85"}
  ]
}
```

---
