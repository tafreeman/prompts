---
title: Tools Ecosystem Evaluator
shortTitle: Tools Evaluator
intro: Comprehensive analysis prompt for evaluating developer tooling ecosystems with structured grading and improvement pathways.
type: reference
difficulty: advanced
audience:
  - senior-engineer
  - solution-architect
platforms:
  - github-copilot
  - claude
  - chatgpt
author: Prompts Library Team
version: "2.2"
date: "2026-01-10"
techniques:
  - chain-of-thought
  - structured-output
  - cross-validation
governance_tags:
  - PII-safe
dataClassification: internal
reviewStatus: draft
---

# Tools Ecosystem Evaluator

Evaluate any developer tools folder/ecosystem with structured grading, competitive comparison, and multi-path improvement recommendations.

## Description

Use this prompt to evaluate a developer tooling ecosystem (architecture, DX, reliability, performance, maintainability) and return evidence-first findings plus prioritized improvements.

---

## Consolidated Evaluation (Merged Notes)

This section merges:

- findings verified in this workspace (code searches + file reads + a test run), and
- an additional evaluation write-up pasted from another chat.

Where the two disagree, the reconciliation notes call it out explicitly.

### Executive Summary (merged)

The tools ecosystem is feature-rich but technically fragmented: it offers broad multi-provider LLM abstraction, a tiered evaluation concept, and strong safety defaults (remote providers gated by explicit opt-in). However, maintainability and product cohesion are undermined by widespread import/path manipulation (`sys.path.insert/append`), duplicated subsystems (notably `tools/enterprise-evaluator/core/`), and multiple overlapping CLIs.

Immediate value comes from: fixing CLI drift/broken imports, aligning evaluation expectations to the actual prompt frontmatter used in `prompts/`, and implementing/activating parallel evaluation for directory runs.

### Key reconciliation notes

- Parallelization: the codebase contains parallel infrastructure in some places (e.g., agent runners / benchmarks), but core evaluation paths are not consistently parallelized.
- Tests: a `pytest` task exists and collects tests, but the run currently fails with a capture teardown crash (`ValueError: I/O operation on closed file.`), which should be treated as a reliability blocker until resolved.

### Phase 1 Results (merged inventory highlights)

#### Architecture mapping (high-level)

- Core runtime: `tools/llm_client.py`, `tools/local_model.py`, `tools/model_probe.py`, `tools/windows_ai.py`
- Evaluation: `tools/prompteval/` (primary) + `tools/evaluation_agent.py` (pipeline orchestration)
- Validation: `tools/validators/*` (multiple validators with overlapping schema assumptions)
- Enterprise fork: `tools/enterprise-evaluator/` includes `core/` that duplicates the main runtime modules
- CLI surfaces: `prompt.py`, `tools/cli/main.py`, `python -m prompteval`, plus many script-level entry points

#### Code hygiene audit (verified signals)

| Anti-pattern                 | Evidence                                                                                    | Severity |
| ---------------------------- | ------------------------------------------------------------------------------------------- | -------- |
| `sys.path.insert/append`     | 29 matches across `tools/**/*.py` in this workspace scan                                    | Critical |
| Duplicate `ErrorCode`        | Defined in `tools/model_probe.py` and `tools/tool_init.py`                                  | Medium   |
| Duplicate `classify_error()` | Defined in `tools/model_probe.py`, `tools/tool_init.py`, and `tools/prompteval/__main__.py` | Medium   |
| Duplicated runtime modules   | `tools/enterprise-evaluator/core/` duplicates llm client / local model / Windows AI         | Critical |

#### Capability matrix (condensed)

| Category             | Tools                      | Maturity |   Docs | Duplicates? |
| -------------------- | -------------------------- | -------: | -----: | ----------- |
| LLM integration      | `tools/llm_client.py`      |     High |   High | Yes         |
| Model discovery      | `tools/model_probe.py`     |     High |   High | No          |
| Evaluation           | `tools/prompteval/`        |     High |   High | Yes         |
| Validation           | `tools/validators/`        |   Medium | Medium | Overlap     |
| Analysis/improvement | `tools/improve_prompts.py` |   Medium | Medium | No          |
| Execution safety     | `tools/tool_init.py`       |     High |   High | No          |

#### Provider/integration support (as implemented)

The dispatcher/probe stack supports local and remote providers; remote usage is gated behind explicit opt-in.

### Phase 2 Results (scoring)

The merged inputs contain two different score baselines:

- Prior chat scorecard: total 76.2/100 (C+), with Performance as the main weakness.
- Workspace-evidence adjustment: until (a) tests run cleanly and (b) CLI drift is resolved, overall confidence should be reduced (especially for Reliability/DX).

### Phase 4 Results (improvement pathways that both sources converge on)

1. Enable/implement parallel directory evaluation (high ROI).
2. Reduce duplication drift: a single source of truth for runtime modules.
3. Replace `sys.path` hacks by making `tools/` importable/installable.
4. Add deterministic response caching in the central dispatch path.
5. Unify the CLI surface (canonical entry point + wrappers).

### Phase 5 Results (prioritized actions)

Immediate actions (highest ROI):

1. Fix correctness drift: resolve missing imports/symbol references in CLIs (e.g., `prompteval.tiers.TIERS`, `tiered_eval.find_prompts`).
2. Restore a passing test signal: fix the current `pytest` capture teardown crash.
3. Remove duplication drift: refactor `tools/enterprise-evaluator/core/` to reuse shared modules.

## 📋 Quick Copy: The Prompt

Copy everything inside the code block below and paste it into your AI assistant:

## Prompt

`````markdown
You are an expert software architect and developer tooling analyst. Your task is to perform a comprehensive evaluation of a developer tools ecosystem and provide actionable insights.

## Script execution contract (for Python runners)

This prompt is designed to be executed by a Python script that may call the model in a loop with partial inputs.

### Execution header

The runner will prepend an `# EXECUTION` header like:

RUN_ID: <string>
MODE: COLLECT | SYNTHESIZE
CHUNK_INDEX: <int>
CHUNK_COUNT: <int | "unknown">
FOCUS_AREAS: <optional string>
COMPARISON_TARGETS: <optional string>

Treat this header as authoritative.

### Modes

#### MODE: COLLECT

Goal: extract **evidence-first notes** from the provided `{TOOLS_STRUCTURE}` + `{KEY_FILES}`.

Return **ONLY JSON** matching the schema below, and keep it compact. Do NOT output Markdown in this mode.

If you need more evidence to complete the evaluation, set `needs_more=true` and provide `next_requests`.

#### MODE: SYNTHESIZE

Goal: generate the final evaluation report using `COLLECTED_NOTES_JSON` provided by the runner.

Return **ONLY JSON** including a `report_markdown` field.

### Output JSON schema

Return a single JSON object. No code fences.

Required fields:

- `run_id` (string)
- `mode` ("COLLECT" | "SYNTHESIZE")
- `needs_more` (boolean)
- `next_requests` (array)

In COLLECT mode, also include:

- `observations` (array of objects)

In SYNTHESIZE mode, also include:

- `report_markdown` (string) — must follow the **Output Format** structure below

`next_requests` item format (runner may or may not satisfy all requests):

{ "path": "tools/llm_client.py", "reason": "Need dispatcher contract", "max_chars": 12000 }

`observations` item format:

{ "tag": "Observed" | "Inferred" | "Hypothesis", "claim": "…", "evidence": [{"path":"…","lines":"~10-40","snippet":"…"}] }

## Critical rules for this evaluation

1. **Evidence-first**: Every non-trivial claim must include (a) the file path(s) and (b) either a short quoted snippet or an approximate line range. If you cannot verify a claim, label it **Hypothesis**.
2. **Separate observed vs inferred**: Use **Observed** / **Inferred** tags when describing behavior.
3. **No hallucinated execution**: If you did not run tests or commands, say so.
4. **Delta-aware**: If a prior evaluation is provided, explicitly call out what changed (fixed/regressed/new risks).

## Context

I will provide you with:
1. The structure of a `tools/` folder or developer tooling ecosystem
2. Key file contents (documentation, core modules, configuration)
3. Optional: Reference ecosystems for comparison

This particular ecosystem (the one you are evaluating) is expected to include:
- A **model availability / discovery** layer (e.g., a “model probe” module)
- A **central LLM dispatcher/client** layer
- A **tiered evaluation** CLI and/or VS Code tasks for running evaluations
- **Fail-fast** prerequisites checks before any LLM calls
- **Iterative logging** (e.g., JSONL) for long-running evals
- Windows-friendly **UTF-8 output handling**

If any of these are missing, treat that as a potential design gap (and score accordingly).

## Your Analysis Framework

### Inputs you should request if missing

If the user only provides a folder tree, request (or infer from workspace) the contents of:
- The main dispatcher/client module
- The model discovery/probe module
- The evaluation CLI entry point(s)
- Any init/preflight module (env/model checks)
- The validators folder (schemas and rules)
- Project config (`pyproject.toml`, `requirements.txt`) and key docs
- VS Code tasks (`.vscode/tasks.json`) if present

### Phase 1: Discovery & Inventory

Create a complete inventory answering:

**Architecture Mapping**
- What are the major subsystems/modules?
- How do they interact (dependency graph)?
- What is the entry point hierarchy (CLI → Core → Helpers)?
- Are there circular dependencies or orphaned modules?
- Is the tools layer installable/importable without `sys.path` hacks?
- What are the canonical “golden paths” a developer should use?
- List the top **3 supported workflows** a developer should run, with their canonical command(s) or VS Code task(s).
- Identify any alternate entry points as **Legacy/Compat** and explain the risk of drift.

**Capability Matrix**
| Category | Tools | Maturity | Documentation |
|----------|-------|----------|---------------|
| (fill in) | | | |

**Provider/Integration Support**
- Which external services/APIs are supported?
- What is the abstraction level (direct calls vs. unified interface)?
- Are there fallback mechanisms?

**Preflight Contract Checklist**
- Environment variables required (and whether they are documented)
- Model availability checks happen **before** any LLM call
- Fail-fast behavior: missing prerequisites stop early with actionable errors
- Windows UTF-8 console/output handling is present (and not copy-pasted everywhere)
- Long-running evals persist progress (JSONL/logging, checkpoints, resumability)

**Code Hygiene Checks** (search for these patterns)
- `sys.path.insert` or `sys.path.append` usage (indicates fragile imports)
- Duplicate implementations of same functionality across modules
- Multiple CLI entry points doing similar things
- Direct provider calls that bypass unified dispatcher
- Schema/validation overlap between different validators
- Duplicate error taxonomies (`ErrorCode`, `classify_error`, etc.) and drift between them
- Duplicated “core runtime” modules across folders (forked copies)
- Any test harness issues that prevent a clean `pytest` run (treat as a reliability red flag)

### Phase 2: Quality Grading (0-100 per dimension)

Grade each dimension with specific evidence:

**Scoring discipline**
- For each dimension: list 2–4 concrete positives and 2–4 concrete negatives with evidence.
- Call out **blockers** (issues that should cap the score) vs **nits** (non-blocking polish).
- If tests are failing in CI/local runs, cap **Reliability & Safety** at **70/100** unless you can prove (with evidence) the failure is unrelated to the tools ecosystem.

#### 2.1 Architecture Quality (Weight: 20%)
- **Modularity** (0-25): Are concerns separated? Can components be used independently?
- **Cohesion** (0-25): Do modules have single, clear responsibilities?
- **Coupling** (0-25): How dependent are modules on each other?
- **Extensibility** (0-25): How easy is it to add new providers/features?

#### 2.2 Developer Experience (Weight: 25%)
- **Onboarding** (0-20): Can a new developer start in <15 minutes?
- **CLI Ergonomics** (0-20): Are commands intuitive and consistent?
- **Error Messages** (0-20): Are errors actionable with clear remediation?
- **Documentation** (0-20): Is there comprehensive, up-to-date documentation?
- **IDE Integration** (0-20): Are there tasks, snippets, or extensions?

#### 2.3 Reliability & Safety (Weight: 20%)
- **Fail-Fast** (0-25): Does the system detect problems early?
- **Error Handling** (0-25): Are errors classified and handled appropriately?
- **Idempotency** (0-25): Can operations be safely retried?
- **Data Integrity** (0-25): Is progress saved? Can work resume after failure?

#### 2.4 Performance & Efficiency (Weight: 15%)
- **Caching** (0-25): Are expensive operations cached?
- **Parallelization** (0-25): Can independent operations run concurrently?
- **Resource Usage** (0-25): Is memory/CPU usage reasonable?
- **Cost Optimization** (0-25): Are there free/cheap defaults?

When evaluating Performance for this ecosystem specifically, check for:
- Response caching in the central dispatcher (not just model discovery caching)
- Concurrency actually wired into the main evaluation loop (not only in benchmarks)
- Whether any `parallel`/`workers` flags exist but are unused (configuration drift)

#### 2.5 Maintainability (Weight: 15%)
- **Code Quality** (0-20): Is code readable, typed, and well-structured?
- **Test Coverage** (0-20): Are there unit/integration tests? What's the coverage?
- **Consistency** (0-20): Are patterns applied uniformly? Check for duplicate implementations.
- **Technical Debt** (0-20): Are there TODOs, hacks, deprecated code, or `sys.path` hacks?
- **Version Control** (0-20): Is there proper versioning, changelog, and migration docs?

#### 2.6 Innovation & Completeness (Weight: 5%)
- **Feature Coverage** (0-50): Does it solve the stated problem completely?
- **Novel Approaches** (0-50): Are there unique/innovative techniques?

### Phase 3: Comparative Analysis

Compare against these reference ecosystems (if known):

| Ecosystem | Strengths to Adopt | Weaknesses to Avoid |
|-----------|-------------------|---------------------|
| Hugging Face Transformers | Unified pipeline API, model hub | Complex tokenizer setup |
| LangChain | Extensive integrations, chains | Over-abstraction, hard to debug |
| LlamaIndex | Query engines, data connectors | Steep learning curve |
| Instructor (Python) | Structured output, validation | Limited to specific use cases |
| DSPy | Programmatic prompting, optimization | Experimental, less stable |

For each reference:
1. What patterns does the target ecosystem already implement well?
2. What patterns are missing that would add value?
3. What anti-patterns should be avoided?

### Phase 4: Improvement Pathways

Generate **3-5 distinct improvement paths**, each with:

For this ecosystem, prefer pathways that are **PR-sized and testable**, and include:
- The smallest safe “first PR” slice
- Migration/compatibility strategy for CLI changes
- How you will prove improvement (tests, benchmarks, reduced duplication, fewer path hacks)

#### Path Template
```
## Path [N]: [Name]

**Theme**: [One-sentence description]
**Effort**: [Low/Medium/High]
**Impact**: [Low/Medium/High]
**Risk**: [Low/Medium/High]

### Changes Required
1. [Specific change with file paths]
2. [Specific change with file paths]
...

### Expected Outcomes
- [Measurable improvement]
- [Measurable improvement]

### Dependencies
- [What must exist first]

### Trade-offs
- Pros: [Benefits]
- Cons: [Costs/risks]
```

#### Required Path Types
1. **Quick Wins** (Low effort, Medium-High impact) - e.g., fix docs, enable existing params
2. **Architecture Refactor** (High effort, High impact) - e.g., consolidate CLIs, unify dispatch
3. **Developer Experience** (Medium effort, High impact) - e.g., doctor command, onboarding wizard
4. **Performance Optimization** (Medium effort, Medium impact) - e.g., caching, parallelization
5. **Innovation/Differentiation** (Variable effort, Variable impact) - e.g., novel techniques, contracts
6. **Technical Debt Reduction** (Medium effort, Medium impact) - e.g., remove duplicates, fix imports

### Phase 5: Scorecard & Recommendations

#### Final Scorecard
```
┌─────────────────────────────────────────────────────────────┐
│                    TOOLS ECOSYSTEM SCORECARD                 │
├─────────────────────────────────────────────────────────────┤
│ Dimension              │ Score │ Weight │ Weighted │ Grade  │
├────────────────────────┼───────┼────────┼──────────┼────────┤
│ Architecture Quality   │  /100 │  20%   │          │        │
│ Developer Experience   │  /100 │  25%   │          │        │
│ Reliability & Safety   │  /100 │  20%   │          │        │
│ Performance            │  /100 │  15%   │          │        │
│ Maintainability        │  /100 │  15%   │          │        │
│ Innovation             │  /100 │   5%   │          │        │
├────────────────────────┼───────┼────────┼──────────┼────────┤
│ TOTAL                  │       │ 100%   │    /100  │        │
└─────────────────────────────────────────────────────────────┘

Grade Scale: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)
```

#### Top 3 Immediate Actions
1. [Highest ROI action]
2. [Second highest ROI action]
3. [Third highest ROI action]

#### Top 3 Strategic Investments
1. [Long-term high-impact investment]
2. [Second long-term investment]
3. [Third long-term investment]

#### Red Flags / Critical Issues
- [Any blocking issues that need immediate attention]

## Output Format

Provide your analysis in this exact structure:
1. **Executive Summary** (3-5 sentences)
2. **Phase 1 Results** (Tables and lists)
3. **Phase 2 Results** (Scores with evidence)
4. **Phase 3 Results** (Comparison table)
5. **Phase 4 Results** (Improvement paths)
6. **Phase 5 Results** (Scorecard and recommendations)

In **Executive Summary**, include a short **“Delta since last evaluation”** paragraph if a prior eval is provided.

If a prior evaluation is provided, include a **Delta Table** in the Executive Summary section:

| Area | Before | After | Evidence | Impact | Risk |
|------|--------|-------|----------|--------|------|
| (fill in) | | | | | |

In **Phase 5**, include:
- **Blockers (must-fix)**: items that prevent trustworthy eval results or safe CI
- **Next two PRs**: concrete, sequenced pull requests to deliver the highest ROI

## Input

[PASTE TOOLS FOLDER STRUCTURE AND KEY FILE CONTENTS HERE]

## Comparison Targets (Optional)

[SPECIFY WHICH ECOSYSTEMS TO COMPARE AGAINST, OR USE DEFAULTS]

`````

**End of prompt - copy everything above within the code block.**

---

## Variables

| Variable               | Description                                     | Example                               |
| ---------------------- | ----------------------------------------------- | ------------------------------------- |
| `{TOOLS_STRUCTURE}`    | Directory tree of tools folder                  | `tools/\n├── cli/\n├── core/\n...`    |
| `{KEY_FILES}`          | Contents of main documentation and entry points | `README.md`, `__init__.py`, main CLI  |
| `{COMPARISON_TARGETS}` | Reference ecosystems to compare against         | `LangChain`, `Hugging Face`           |
| `{FOCUS_AREAS}`        | Specific aspects to emphasize                   | `performance`, `developer experience` |
| `{PRIOR_EVAL}`         | Prior scorecard and findings (if any)           | `last_run.md`                         |

## Example Usage

### Basic Analysis

```text
[Paste the prompt above]

## Input

{TOOLS_STRUCTURE}

Key files:
- tools/llm_client.py: (paste)
- tools/model_probe.py: (paste)
- tools/prompteval/core.py: (paste)

## Comparison Targets

Compare against: LangChain, DSPy, Instructor
```

### Delta Analysis (After an Update)

```text
[Paste the prompt above]

## Input

{TOOLS_STRUCTURE}

Key files (current):
- (paste the same set of key files)

## Prior Evaluation

{PRIOR_EVAL}

Focus on:
1) What changed
2) What got better/worse
3) New risks introduced by the update
```

## Tips for Best Results

1. **Include entry points**: CLIs, `__main__.py`, and any VS Code tasks are crucial for DX scoring.
2. **Include preflight/init**: A tools ecosystem should fail fast before expensive runs.
3. **Include logs/checkpoints**: Show how long-running evals record progress (JSONL, checkpoints).
4. **Include test output**: If tests fail, paste the failure output so the analysis can classify it as blocker vs unrelated.

## Follow-Up Prompts

### Code Hygiene Audit

```text
Search the codebase for these anti-patterns and quantify:
1. `sys.path.insert` or `sys.path.append` usage (fragile imports)
2. Duplicate class/function definitions across modules
3. Multiple CLI entry points with overlapping functionality
4. Direct API calls that bypass the unified dispatcher
5. Inconsistent error handling patterns
Provide counts and specific file locations for each.
```

### PR Plan Generator

```text
Convert the top 2 improvement paths into:
1) Two pull requests with titles
2) File-by-file change list
3) Acceptance criteria for each PR
4) Test plan (unit/integration) and rollback notes
```
