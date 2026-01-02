# Evaluation Framework Plan (Phased)

> This file is the source-of-truth plan for improving and/or restructuring the prompt evaluation framework in this repo.
> 
> Scope includes: evaluation runners, model selection/inventory, result schemas + reporting, reliability, CI tasks, and optional Windows AI (Phi Silica) support.

## Why this exists

We have *multiple* overlapping evaluation entrypoints and “tiers” across the repo:

- `tools/prompteval/` (documented as the unified evaluator)
- `tools/tiered_eval.py` (tiered runner wired into CLI flows)
- `tools/batch_free_eval.py` (ad-hoc batch runner used for recent advanced runs)
- `testing/evals/**` (`.prompt.yml` test cases + `dual_eval.py`)

The result: evaluations work, but reliability and consistency suffer (different scoring schemas, model availability surprises, duplicated logic, and unclear “golden path”).

## Goals (what “best results” means)

1. **Single canonical evaluation entrypoint** for humans + CI.
2. **Consistent result schema** (JSON) + consistent human report (Markdown).
3. **Reliable model execution** (probe + caching; automatically skip unavailable/403/unrunnable models).
4. **Free-first evaluation** by default (local ONNX + GitHub Models), with optional escalation.
5. **Repeatability**: multi-run stats (mean/stdev), deterministic configs, and saved metadata.
6. **Extensibility**: easy to add new model providers (GitHub Models, local ONNX, Windows AI, Azure Foundry).

## Known facts (current state)

### Evidence from the latest advanced batch run

The most recent “advanced” batch run results are captured in `batch_eval_results.json` (timestamp `2025-12-31T21:38:07`).

**Coverage / success rate**

- Evaluated **3** files under `testing/evals/advanced/`.
- Attempted **7 models per file** = **21 total** eval attempts.
- **12 succeeded**, **9 failed** (systemic, repeatable failures).

**Per-model performance (mean over 3 files, from the JSON summary)**

- `local:mistral-7b-instruct`: **9.7** (3/3)
- `openai/gpt-4o`: **8.33** (3/3)
- `openai/gpt-4o-mini`: **8.0** (3/3)
- `openai/gpt-4.1-nano`: **6.93** (3/3)

**Systemic failures observed**

- `openai/gpt-5-nano`: `unavailable_model` (listed, but not runnable)
- `openai/o1`, `openai/o3`: `403 Forbidden` (entitlement/permission blocked)

**What this run tells us about the framework**

- ✅ The **“single file × multiple models”** evaluation loop is structurally correct.
- ✅ For successful cloud models, the **evaluation prompt format yields parseable JSON** (scores + overall + summary).
- ⚠️ **Model list ≠ runnable model**. We need a probe/caching step (Phase 2) to prevent known-failing models from consuming runs.
- ⚠️ The current “evaluate `.prompt.yml`” approach is effectively evaluating the **YAML/template text** rather than the **rendered prompt/messages** as executed.
  - This is OK for “template linting”, but it is not the same as evaluating the prompt as the model actually sees it.
  - We should support parsing/rendering `.prompt.yml` and optionally using `gh models run --file` for true as-executed behavior (Phase 4).
- ⚠️ Local ONNX scores look **inflated** vs cloud scores; treat local as triage or calibrate (Phase 3).
- ⚠️ Complexity scoring in the run lands around **20–22** and always labels prompts as **reasoning**; the scale likely needs rebalancing/capping (Phase 3).

### Canonical-ish evaluator already exists
- `tools/prompteval/README.md` explicitly describes PromptEval as the unified tool.
- `tools/README.md` also claims PromptEval “replaces `tiered_eval.py`, `evaluate_library.py`, and `batch_evaluate.py`”.
- `tools/prompteval/__main__.py` has CLI support including tiers, `--all-local`, `--all-cloud`, and inventory-based skipping.

### Tiered runner is widely wired in
- `tools/tiered_eval.py` is referenced by VS Code tasks and by interactive tooling (`prompt.py`, `tools/cli/main.py`).

### Phi Silica (Windows AI) is integrated but currently blocked
- Python wrapper: `tools/windows_ai.py` (calls the C# bridge via `dotnet run`).
- C# bridge: `tools/windows_ai_bridge/Program.cs`.
- On this machine, bridge checks report:
  - `--check`: **Access is denied**
  - `--info`: `available=false` and `error="Limited Access Feature - requires unlock token"`
- **Important:** the current bridge does **not** read any env var like `PHI_SILICA_UNLOCK_TOKEN`.

### Additional advanced eval cases to add (to expose framework gaps)

To broaden coverage beyond “reasoning-heavy” prompts and force evaluator improvements to prove themselves, add a few `.prompt.yml` cases like:

- **Tool-use / routing**: choose between tools (search vs compute vs summarize) and return a structured action plan.
- **Strict schema extraction**: output must conform to a JSON schema with constraints.
- **Long-context compression + faithfulness**: summarize long input while obeying must-include / must-not-include facts.
- **Safety boundary test**: an “advanced wrapper” that includes refusal policy + tricky user instruction.
- **Code change request + tests**: prompt asks for a patch + unit tests (actionability/completeness).

## Decision gate: migrate structure vs update in-place

We will decide in **Phase 1** whether to:

### Option A — Update in-place (recommended default)
Make `prompteval` the canonical evaluator *without* moving repo folders. Deprecate/redirect other runners to it.

**Pros:** minimal churn, preserves existing docs/paths, fastest to stabilize.

**Cons:** legacy files remain (but can be left as thin wrappers).

### Option B — Migrate to a new evaluation structure
Create a clean `eval/` (or `tools/eval/`) spine with a single CLI + library, and move/retire older entrypoints.

**Pros:** clean architecture long-term.

**Cons:** bigger diff, breaks scripts/tasks, higher regression risk.

**Decision criteria:**
- If we can make `prompteval` cover all needed scenarios (GitHub Models + local ONNX + result/report needs) with modest changes → **Option A**.
- If `prompteval` is fundamentally mismatched to `.prompt.yml` / our scoring approach and would need a rewrite anyway → **Option B**.

---

## Ordered work plan (dependency-aware)

This is the **implementation order**. Items are grouped by phase, and the numbering reflects dependencies.

### Phase 0 — Define the contract (must be first) ✅ COMPLETED

- [x] **(P0.1) Document canonical result schema**
  - Define the JSON fields for: prompt identity/path, input type (`md` vs `.prompt.yml`), model/provider, run index, rubric scores, overall, summary, error classification, raw stderr/stdout pointers, duration, tool versions.
  - Include a small example JSON object and a "minimum required fields" list.
- [x] **(P0.2) Define standard outputs**
  - Markdown: summary + per-file/per-model breakdown.
  - CSV (optional but recommended): row-per-(file,model,run).
- [x] **(P0.3) Confirm supported input types + acceptance criteria**
  - Inputs: `prompts/**` markdown and `testing/evals/**.prompt.yml`.
  - Acceptance: one command can evaluate either input and produce the same schema.

> **📄 Output:** [EVALUATION_SCHEMA.md](EVALUATION_SCHEMA.md) — Contains the canonical schema, output formats, and acceptance criteria.

### Phase 1 — Choose the spine and stop duplicating logic ✅ COMPLETED

- [x] **(P1.1) Pick the canonical evaluator**
  - **Decision: Option A — Update in-place with `prompteval`**
  - `python -m prompteval` is feature-complete (tiers 0-7, model probing, JSON/MD output, CI mode)
  - Already documented in `tools/prompteval/README.md` as the unified evaluator
  - `tiered_eval.py` already archived to `tools/archive/`
- [x] **(P1.2) Make other entrypoints thin wrappers**
  - Updated entrypoints to delegate to prompteval:
    - `tools/cli/main.py` (`prompt eval`) → calls `prompteval.evaluate()`
    - `prompt.py` `eval_prompts()` → calls `prompteval.evaluate_directory()`
    - VS Code tasks updated to use `python -m prompteval`

> **Canonical CLI:** `python -m prompteval <path> [options]`

### Phase 2 — Reliability (fix the failures exposed by advanced runs) ✅ COMPLETED

- [x] **(P2.1) Centralize model inventory**
  - One module that can answer: "what models are configured?" and "what models are usable *here*?"
  - Implemented in `tools/model_probe.py` with `ModelProbe` class
- [x] **(P2.2) Add a probe + cache for cloud models**
  - Detect `403 Forbidden` and `unavailable_model` and persist results.
  - Filter tiers to the runnable intersection before running a batch.
  - Cache TTLs: 24h for permanent errors, 5min for transient, 1h for success
- [x] **(P2.3) Retry/backoff + error classification**
  - Transient errors retry; entitlement/availability errors do not.
  - Exponential backoff with jitter (max 2 retries)

> **📄 Output:** [tools/model_probe.py](../tools/model_probe.py) — Model probing, caching, and error classification

### Phase 4 — Input correctness (evaluate what actually runs)

- [ ] **(P4.1) Unify prompt discovery rules**
  - Same excludes everywhere (`README.md`, `index.md`, `*.agent.md`, `*.instructions.md`, etc.).
- [ ] **(P4.2) First-class `.prompt.yml` parsing + rendering**
  - Extract messages/prompts from YAML.
  - Optionally render variables.
  - Optionally support “as executed” via `gh models run --file`.

### Phase 3 — Scoring quality (stability + comparability)

- [ ] **(P3.1) Multi-run aggregation**
  - `--runs N` with mean/stdev and instability flags.
- [ ] **(P3.2) Calibration / normalization**
  - Local ONNX is currently generous; treat as triage or calibrate against cloud anchors.
  - Rebalance/cap complexity scoring so tiers separate meaningfully.

### Phase 5 — Phi Silica (Windows AI) is a single, time-boxed integration

- [ ] **(P5.1) Capability gating (skip when unavailable)**
  - Always call bridge `--info` / `--check` and exclude Windows AI models automatically when not available.
- [ ] **(P5.2) Decide unlock mechanism**
  - If the platform supports programmatic unlock, wire `--unlock-token` (or env) through.
  - If it does not, document entitlement-only behavior clearly.

### Phase 6 — Tooling polish (after behavior stabilizes)

- [ ] **(P6.1) Update VS Code tasks** to call the canonical spine.
- [ ] **(P6.2) CI mode + unit tests** for schema, discovery, and inventory filtering.

---

## Phase 0 — Baseline & acceptance criteria ✅ COMPLETED (2026-01-01)

**Objective:** establish what "done" looks like and lock down baseline behavior.

### Tasks
- [x] Define the canonical result JSON schema (fields for prompt path, model, run, score, rubric breakdown, error, timings, tool versions).
- [x] Define report outputs (Markdown summary + CSV optional).
- [x] Choose the primary evaluation inputs we must support:
  - Markdown prompts under `prompts/**`
  - GitHub `.prompt.yml` eval cases under `testing/evals/**`
- [x] Confirm which runner is currently used in CI/automation (VS Code tasks + `tools/cli/main.py`).

### Exit criteria
- [x] A documented schema + acceptance checklist exists in this file.

---

## Phase 1 — Choose the "spine" and simplify entrypoints ✅ COMPLETED (2026-01-01)

**Objective:** pick the canonical evaluator and make everything else route to it.

### Decision: Option A — Update in-place with `prompteval`

After evaluating the existing entrypoints:
- `tools/prompteval/` — Feature-complete CLI with tiers 0-7, model probing, JSON/MD output, CI mode
- `tools/tiered_eval.py` — Already archived to `tools/archive/`
- `tools/batch_free_eval.py` — Ad-hoc batch runner (low usage)

**Chosen:** `python -m prompteval` is the **canonical evaluator**.

### Tasks
- [x] Evaluated feature coverage: prompteval covers all required scenarios
- [x] Decided **Option A** (update in-place)
- [x] Canonical CLI: `python -m prompteval <path> [options]`
- [x] Updated entrypoints to delegate to prompteval:
  - `tools/cli/main.py` `eval` command → calls `prompteval.evaluate()`
  - `prompt.py` `eval_prompts()` → calls `prompteval.evaluate_directory()`
  - VS Code tasks → now use `python -m prompteval`

### Exit criteria
- [x] Docs and one "golden path" command are aligned.
- [x] All evaluation tasks route through prompteval.

---

## Phase 2 — Reliability: model inventory + runnable probing ✅ COMPLETED (2026-01-01)

**Objective:** stop wasting runs on models we can't actually call.

### Tasks
- [x] Centralize a **model inventory** module (GitHub Models + local ONNX + Windows AI) and cache results.
- [x] Add a **probe step** for cloud models (detect 403/unavailable) and record "unusable reasons".
- [x] Ensure evaluators automatically skip unusable models (with clear reporting).
- [x] Add retry/backoff for transient errors.

### Exit criteria
- [x] Running eval across a folder no longer produces systematic failures from known-unusable models.

### Implementation Notes
- Created `tools/model_probe.py` with `ModelProbe` class
- Integrated into `prompteval/__main__.py` via `run_evaluation()` function
- Probe cache stored at `~/.cache/prompts-eval/model-probes/probe_cache.json`
- Error classification matches schema in `EVALUATION_SCHEMA.md`

---

## Phase 3 — Scoring quality: calibration and multi-run stats ✅ COMPLETED (2026-01-01)

**Objective:** make scores comparable and less noisy.

### Tasks
- [x] Implement multi-run aggregation: $\mu$ (mean), $\sigma$ (stdev), and outlier detection.
- [x] Normalize scoring across providers (local ONNX tends to score high; calibrate/adjust or label as "triage").
- [x] Add rubric versioning (so rubric changes don't invalidate historical comparisons).
- [x] Add AI Toolkit support (`aitk:` provider) for free local ONNX models.
- [ ] Add "hard fail" checks (missing sections, invalid frontmatter, unsafe patterns) that override LLM score.

### Implementation Notes
- Added `std_dev`, `is_stable`, `outlier_count` fields to `PromptResult` dataclass
- Added `RUBRIC_VERSION = "1.0"` constant for tracking rubric changes
- Added `CALIBRATION` config dict with offsets for local vs cloud models
- Updated aggregation logic with proper standard deviation calculation
- Stability threshold: `std_dev < 5.0` marks result as stable
- Added `aitk:` provider to `model_probe.py` for AI Toolkit local models
- AI Toolkit models discovered from `~/.aitk/models/` directory

### Exit criteria
- [x] Scores are stable across 2–3 runs and reported with variance.

---

## Phase 4 — Input support: `.prompt.yml` and prompt discovery ✅ COMPLETED (2026-01-01)

**Objective:** treat `.prompt.yml` evals as first-class inputs, not a special-case script.

### Tasks
- [x] Implement `.prompt.yml` parsing and rendering into the evaluator pipeline.
- [x] Unify prompt discovery rules (exclude `README.md`, `index.md`, `*.agent.md`, `*.instructions.md`, etc.).
- [x] Ensure all inputs produce the same result schema.

### Implementation Notes

**Core Changes:**
- Added `yaml` import to `tools/prompteval/__main__.py`
- Updated `find_prompts()` to discover `.prompt.yml` files in addition to `.md` files
- Implemented `evaluate_yaml_prompt()` to handle YAML-based evaluation:
  - Parses YAML structure (testData, messages)
  - Renders message templates with variable substitution
  - Executes each test case via LLMClient
  - Aggregates scores across multiple test cases
  - Returns standardized ModelResult schema
- Updated `evaluate_structural()` to handle YAML files:
  - Scores based on presence of testData and messages (100% if complete)
  - Different rubric than Markdown (40% structure, 30% test data, 30% messages)
  - Returns same result schema as Markdown evaluation
- Updated `evaluate_with_model()` to dispatch to YAML handler when file extension detected

**Discovery Rules:**
- Markdown files: `prompts/**/*.md` (excluding README.md, index.md, archives)
- YAML files: `testing/evals/**/*.prompt.yml`
- Both file types excluded if in `archive/` directories

**Schema Consistency:**
- Both Markdown and YAML evaluations produce identical `ModelResult` dataclass:
  - `model`: str (provider:model format)
  - `run`: int (run number for multi-run stats)
  - `score`: float (0-100)
  - `criteria`: Dict[str, float] (rubric breakdown)
  - `duration`: float (execution time in seconds)
  - `error`: Optional[str] (error message if failed)
- Structural evaluation produces identical dict schema:
  - `score`: float
  - `criteria`: Dict[str, float]
  - `title`: str
  - `category`: str

**Variable Substitution:**
YAML messages support `{{variable}}` syntax for template rendering:
```yaml
testData:
  - promptContent: "Test prompt"
messages:
  - role: user
    content: "Evaluate: {{promptContent}}"
```

### Exit criteria
- [x] One command can evaluate both `prompts/**` and `testing/evals/**`.
- [x] YAML and Markdown evaluations produce identical output schemas.
- [x] Variable substitution works correctly in YAML messages.

---

## Phase 5 — Phi Silica (Windows AI) as *one* step (time-boxed)

**Objective:** make Windows AI evaluation either work reliably **or** fail fast with excellent guidance.

### Known changes needed (from code + observed behavior)
- The bridge (`tools/windows_ai_bridge/Program.cs`) reports `UnauthorizedAccessException` as:
  - `error: "Limited Access Feature - requires unlock token"`
- The Python integration (`tools/windows_ai.py`) always calls the bridge via `dotnet run`.
- There is **no** current path for providing an unlock token (env var or argument) to the bridge.

### Tasks
- [ ] Add a *first-class* “capability check” path used by evaluators:
  - `dotnet run ... --info` parsed and cached
  - if `available=false`, Windows AI models are excluded from model lists automatically
- [ ] Decide whether an unlock token can be provided programmatically:
  - If Windows provides an API/mechanism, implement `--unlock-token` (or env-based) wiring.
  - If not, explicitly document that access is entitlement-based and cannot be unlocked at runtime.
- [ ] Improve errors surfaced to users:
  - show readiness state, OS build, and link to request access (`https://aka.ms/phi-silica-unlock` is already referenced in `tools/README.md`).

### Exit criteria
- Evaluations never “mysteriously fail” due to Phi Silica; they either run or are skipped with a clear reason.

---

## Phase 6 — CI + developer ergonomics (half day)

**Objective:** make it easy to run the right evals and hard to run the wrong ones.

### Tasks
- [ ] Update VS Code tasks to call the canonical CLI.
- [ ] Add a CI-friendly mode: non-zero exit if any prompt fails threshold.
- [ ] Add minimal unit tests for:
  - prompt discovery
  - schema validation
  - model inventory filtering

### Exit criteria
- `🧪 Run Python Tests` passes and there’s a stable “Eval Tier 1/2/3” workflow for PRs.

---

## Phase 7 — (Optional) repo restructure (only if chosen)

If Phase 1 selects **Option B**, we will:
- create `tools/eval/` (or `eval/`) as the only supported entrypoint
- relocate/deprecate older scripts
- update docs and tasks accordingly

---

## Worklog

| Date | Phase | Notes |
|------|-------|-------|
| 2026-01-01 | P0 | Phase 0 completed. Schema, output formats, and acceptance criteria documented in [EVALUATION_SCHEMA.md](EVALUATION_SCHEMA.md) |
| 2026-01-01 | P1 | Phase 1 completed. `prompteval` chosen as canonical spine (Option A). Updated `cli/main.py`, `prompt.py`, and VS Code tasks. |
| 2026-01-01 | P2 | Phase 2 completed. Model probing, caching, and retry logic implemented in [tools/model_probe.py](../tools/model_probe.py) |
| 2026-01-01 | P3 | Phase 3 completed. Added multi-run stats (std_dev, mean), calibration config, rubric versioning, and AI Toolkit support. |
| 2026-01-01 | P4 | Phase 4 completed. Implemented `.prompt.yml` parsing, unified discovery, and schema consistency across Markdown and YAML evaluations. |
| 2026-01-01 | — | Phi Silica bridge reports `Limited Access Feature - requires unlock token` on this machine via `--info` |

