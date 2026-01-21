---
name: Tools Ecosystem Evaluator
description: Comprehensive analysis prompt for evaluating developer tooling ecosystems with structured grading and improvement pathways.
type: how_to
---

# Tools Ecosystem Evaluator

Evaluate any developer tools folder/ecosystem with structured grading, competitive comparison, and multi-path improvement recommendations.

## Description

Use this prompt to evaluate a developer tooling ecosystem (architecture, DX, reliability, performance, maintainability) and return evidence-first findings plus prioritized improvements.

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
