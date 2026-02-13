# Execution strategies reference

This document describes the high-level execution strategies available in the engine, how they are selected, what metadata they populate, and what observability events they emit.

## Overview

An execution strategy defines how a workflow DAG is executed. Two primary strategies are provided:

- DagOnceStrategy — the default, single-pass execution: run the DAG once and return the result.
- IterativeRepairStrategy — re-run the DAG multiple times (with a capped number of attempts) until it succeeds or the maximum attempts are exhausted.

Both strategies use the same underlying DAG executor and step execution primitives; they differ in orchestration, retry/feedback mechanics, and emitted events.

## Strategy selection

The factory function `create_execution_strategy(execution_profile)` chooses a strategy from the provided execution profile. Behavior:

- If `execution_profile` contains an explicit `strategy` name, that strategy is used.
- Otherwise, the factory selects `iterative_repair` when `max_attempts > 1`, and `dag_once` when `max_attempts == 1` (backward-compatible default).

Configuration keys:

- `max_attempts` (int) — maximum number of attempts. Defaults to 1.
- `strategy` (str) — optional explicit strategy name (e.g. `"dag_once"`, `"iterative_repair"`).

See: agentic_v2.engine.create_execution_strategy

## IterativeRepairStrategy

Purpose:
- Execute the DAG repeatedly until the overall workflow succeeds or `max_attempts` is reached.

Key behavior:
- Before the first attempt the context variables are captured as a baseline.
- Before each attempt the `ExecutionContext` is reset to the baseline (so attempts start from the same inputs).
- The strategy sets `attempt_number` and `max_attempts` in the context for step logic to inspect.
- After each failed attempt a feedback object may be built and stored in the context as `iterative_feedback` for the next attempt.
- The strategy returns early if an attempt completes with overall status `success`.

Result metadata added by the strategy:

- `strategy`: `"iterative_repair"`
- `attempts_used`: number of attempts actually performed
- `max_attempts`: configured cap
- `attempt_history`: list of per-attempt dictionaries with keys:
  - `attempt_number` (int)
  - `status` (`"success"` / `"failed"`)
  - `duration_ms` (float)
  - `failed_steps` (list[str])

Events emitted via `on_update` callback:
- `attempt_start` — sent before each DAG attempt. Includes `attempt_number`, `max_attempts`, and `timestamp`.
- `attempt_end` — sent after each DAG attempt. Includes `attempt_number`, `max_attempts`, `status`, `duration_ms`, `failed_steps`, and `timestamp`.

These are emitted in addition to the standard DAG lifecycle events (`workflow_start`, `step_start`, `step_end`, `workflow_end`).

## DagOnceStrategy

Purpose:
- Execute the DAG exactly once and return the resulting WorkflowResult. No attempt events are emitted.

## Feature flags and environment

A runtime feature flag may gate availability or behavior of strategies. See `agentic_v2.feature_flags` for runtime overrides. An environment variable shown in tests is `AGENTIC_FF_ITERATIVE_STRATEGY` which can influence strategy selection and is reset/checked by `reset_flags()` in tests.

## Example

A short example shows using an execution profile to run with iterative repair (in a test or small script):

```python
from agentic_v2 import DAG, StepDefinition
from agentic_v2.engine import IterativeRepairStrategy, ExecutionContext

async def my_step(ctx: ExecutionContext) -> dict:
    # step logic that may inspect ctx.get("attempt_number")
    return {"ok": True}

# Run the DAG with retries
strategy = IterativeRepairStrategy(max_attempts=3)
result = await strategy.execute(dag, ExecutionContext(workflow_id="wf-iter"))
```

For higher-level workflow execution via YAML definitions, pass an `execution_profile` to `WorkflowRunner` or `WorkflowRunner.run`/`run_definition` to control `max_attempts` and strategy selection.


For implementation details, see:
- agentic_v2.engine.IterativeRepairStrategy
- agentic_v2.engine.DagOnceStrategy
- agentic_v2.engine.create_execution_strategy
- agentic_v2.workflows.runner.WorkflowRunner


