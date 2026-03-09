# Implementation Plan: Commit-Driven A/B Agent Evaluation Harness

## Overview

This tool evaluates the effectiveness of different agents, workflows, and prompts for code
generation by using real git commits as ground truth. Given a commit, it extracts the
requirements, spins up an isolated git worktree at the pre-commit state, runs two strategies
sequentially, extracts git patches, and scores both against the gold standard using
LLM-as-judge + rubric scoring.

**No Docker. One worktree, sequential.** Creates one `git worktree` at `<sha>~1`, runs
Contestant A, resets, runs Contestant B, then removes the worktree. The working directory
is never touched.

**Architecture Decision Records:**

- [ADR-010](../adr/ADR-010-eval-harness-methodology.md) — Methodology & design (commit-as-ground-truth, worktree over Docker, two-layer scoring)
- [ADR-011](../adr/ADR-011-eval-harness-api-interface.md) — API & interface design (hexagonal architecture, WebSocket, data contracts)
- [ADR-012](../adr/ADR-012-ui-evaluation-hub.md) — UI overhaul (evaluation hub, 2-step wizard, single-page result, deferred pipeline builder)

---

## Data Flow

```
Repo path + Commit SHA
         ↓
CommitExtractor  →  TaskInstance
  • git show <sha>        →  commit message + full diff
  • LLM extracts          →  requirements_prompt
  • Records               →  gold_patch, affected_files, test_oracle_files
  • pre_commit_sha        =  <sha>~1
         ↓
git worktree add /tmp/eval-{uuid} <sha>~1
         ↓
Run Contestant A in /tmp/eval-{uuid}
  → agent/workflow/prompt writes files
  → git diff HEAD          →  patch_a
  → run test oracle        →  test_results_a
  → git checkout -f HEAD   (reset — clean slate for B)
         ↓
Run Contestant B in /tmp/eval-{uuid}
  → agent/workflow/prompt writes files
  → git diff HEAD          →  patch_b
  → run test oracle        →  test_results_b
         ↓
git worktree remove /tmp/eval-{uuid} --force
         ↓
EvalHarness
  • evaluate_with_llm(requirements, patch_a, gold_patch)  → EvaluationResult A
  • evaluate_with_llm(requirements, patch_b, gold_patch)  → EvaluationResult B
  • Scorer(rubric).score(patch_a)  → rubric_score_a
  • Scorer(rubric).score(patch_b)  → rubric_score_b
  • diff patch_a vs patch_b        → patch_delta
         ↓
ComparisonReporter  →  HTML + Markdown report
  • Side-by-side scores per dimension
  • Patch diff visualization
  • Winner + margin
  • Test results (pass/fail)
  • LLM judge improvement suggestions
```

---

## New Module: `tools/commit_eval/`

Located in `tools/` (the shared utilities package, installed as `prompts-tools`).

| File | Lines | Purpose |
|------|-------|---------|
| `__init__.py` | 10 | Package exports |
| `models.py` | 80 | Pydantic: `TaskInstance`, `Contestant`, `Trial`, `ComparisonResult` |
| `extractor.py` | 120 | `CommitExtractor`: `git show` → LLM → `TaskInstance` |
| `sandbox.py` | 80 | `SandboxManager`: git worktree lifecycle (context manager) |
| `runner.py` | 140 | `ContestantRunner`: dispatches to workflow / prompt / agent |
| `patch.py` | 100 | `PatchExtractor` + `TestRunner` (git diff, pytest) |
| `evaluator.py` | 100 | `EvalHarness`: two-layer scoring (LLM judge + rubric) |
| `comparator.py` | 150 | `Comparator`: main orchestrator |
| `reporter.py` | 200 | `ComparisonReporter`: wraps existing HTML/MD reporters |
| `cli.py` | 100 | typer CLI (`agentic-eval compare`) |

### Key Models (`models.py`)

```python
class TaskInstance(BaseModel):
    repo_path: Path
    commit_sha: str
    pre_commit_sha: str          # = commit_sha + "~1"
    commit_message: str
    gold_patch: str              # actual git diff of the commit
    requirements_prompt: str     # LLM-extracted from message + diff
    affected_files: list[str]
    test_oracle_files: list[str] # test files added/modified by commit

class Contestant(BaseModel):
    label: str
    type: Literal["workflow", "prompt", "agent"]
    ref: str | None = None       # workflow name, file path, or agent class
    model: str | None = None
    prompt_text: str | None = None
    temperature: float = 0.7
    system_prompt: str | None = None

class Trial(BaseModel):
    contestant: Contestant
    worktree_path: Path
    generated_patch: str
    modified_files: list[str]
    test_results: dict[str, Any]
    elapsed_seconds: float
    raw_output: str

class ComparisonResult(BaseModel):
    run_id: str
    task: TaskInstance
    trial_a: Trial
    trial_b: Trial
    score_a: dict[str, Any]
    score_b: dict[str, Any]
    rubric_score_a: float
    rubric_score_b: float
    patch_delta: str
    winner: Literal["A", "B", "tie"]
    margin: float
    created_at: str
```

---

## CLI

```bash
# Inline args
agentic-eval compare \
  --repo /path/to/repo \
  --commit abc123 \
  --contestant-a "workflow:code_review" \
  --contestant-b "prompt:prompts/experimental.md" \
  --rubric coding_standards \
  --output-format html \
  --output report.html

# Config file
agentic-eval compare --config eval.yaml
```

```yaml
# eval.yaml
repo: /path/to/repo
commit: abc123
rubric: coding_standards
contestants:
  a:
    type: workflow
    ref: code_review
  b:
    type: prompt
    text: |
      You are an expert Python developer. Implement the following:
      {requirements}
    model: claude:claude-sonnet-4-6
    temperature: 0.3
output:
  format: html
  path: report.html
```

---

## API (`agentic-workflows-v2/agentic_v2/server/routes/eval.py`)

```
POST /eval/compare          → { run_id }
GET  /eval/runs             → list[ComparisonRunSummary]
GET  /eval/runs/{run_id}    → ComparisonResult
WS   /ws/eval/{run_id}      → event stream
```

**WebSocket event vocabulary:**

```json
{ "type": "eval_start",  "run_id": "..." }
{ "type": "phase_start", "phase": "extract|run_a|run_b|score" }
{ "type": "phase_end",   "phase": "...", "status": "done|error", "elapsed_ms": 3200 }
{ "type": "eval_complete", "winner": "A", "score_a": 7.8, "score_b": 6.4, "result": {...} }
{ "type": "error",       "message": "..." }
```

---

## UI Overhaul (`agentic-workflows-v2/ui/`)

### New Files

| File | Lines | Purpose |
|------|-------|---------|
| `pages/eval/NewComparisonPage.tsx` | 140 | 2-step wizard (`/evaluations/compare/new`) |
| `pages/eval/ComparisonRunPage.tsx` | 170 | Progress + result (`/evaluations/compare/:id`) |
| `components/eval/ComparisonWizard.tsx` | 100 | Wizard step logic |
| `components/eval/ContestantConfig.tsx` | 70 | Type pill toggle + ref input |
| `components/eval/ContestantPropertiesForm.tsx` | 90 | Expanded fields per type |
| `components/eval/EvalProgressTracker.tsx` | 80 | 4-step linear progress |
| `components/eval/ComparisonResultView.tsx` | 130 | Winner banner + dimension bars |
| `components/eval/PatchDiff.tsx` | 80 | Collapsible unified diff viewer |
| `hooks/useEvalStream.ts` | 70 | WebSocket hook (mirrors `useWorkflowStream`) |
| `api/eval.ts` | 50 | Typed fetch wrappers for eval API |

### Modified Files

| File | Change |
|------|--------|
| `pages/EvaluationsPage.tsx` | Add "Compare Agents →" CTA + Comparisons tab |
| `App.tsx` | Add routes: `/evaluations/compare/new`, `/evaluations/compare/:id` |

---

## Reused Components (do not rewrite)

| Component | File | Used For |
|-----------|------|----------|
| `LLMClient.generate_text()` | `tools/llm/llm_client.py` | Requirement extraction + prompt runner |
| `evaluate_with_llm()` | `tools/agents/benchmarks/llm_evaluator.py` | LLM-as-judge scoring |
| `Scorer` | `agentic-v2-eval/src/agentic_v2_eval/scorer.py` | Rubric-driven scoring |
| Rubric YAMLs | `agentic-v2-eval/src/agentic_v2_eval/rubrics/` | `coding_standards`, `code`, `agent` |
| `HtmlReporter`, `MarkdownReporter` | `agentic-v2-eval/src/agentic_v2_eval/reporters/` | Base report formatting |
| `WorkflowRunner.run()` | `agentic-workflows-v2/agentic_v2/workflows/runner.py:46` | Workflow contestant |
| `ClaudeAgent` | `agentic-workflows-v2/agentic_v2/agents/implementations/claude_agent.py:65` | Agent contestant |
| `connectExecutionStream()` | `agentic-workflows-v2/ui/src/api/websocket.ts` | WebSocket real-time streaming |

---

## Files to Modify

| File | Change |
|------|--------|
| `tools/__init__.py` | Add `commit_eval` export |
| `tools/pyproject.toml` | Add `typer>=0.12`, `pytest-json-report>=1.5` deps |
| `agentic-workflows-v2/agentic_v2/server/app.py` | Register eval router |

---

## Verification Plan

1. **Unit** — `CommitExtractor` against a known commit on `main` (verify `gold_patch` matches `git show`)
2. **Unit** — `SandboxManager` — create worktree at HEAD~1, verify SHA, run `reset()`, verify clean state, cleanup
3. **Integration** — `Comparator` on a small commit (1–2 files changed) with two prompt variants
4. **End-to-end** — `agentic-eval compare` CLI on a real commit — verify HTML report is generated and both scores are non-zero
5. **UI** — load `/evaluations`, click "Compare Agents", complete 2-step wizard, verify WebSocket progress events update the tracker, verify result renders on completion

Test files: `tools/tests/test_commit_eval/`

---

## Long-Term Roadmap (not this sprint)

In-app visual workflow pipeline builder:

- **Where**: `/workflows/new` and `/workflows/:name/edit`
- **Visual mode**: React Flow drag-and-drop (already installed in `WorkflowDAG.tsx`)
- **YAML mode**: Monaco/CodeMirror with JSON schema validation
- **Bidirectional sync**: edit graph ↔ edit YAML
- **Backend needed**: `POST /workflows`, `PUT /workflows/:name`, `GET /workflows/:name/schema`
- **Deferred rationale**: eval harness provides evidence for which workflow patterns work before committing to a builder UI
