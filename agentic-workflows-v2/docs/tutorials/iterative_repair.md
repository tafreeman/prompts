# Iterative repair tutorial

This tutorial demonstrates the iterative repair execution pattern: re-running a DAG until it succeeds or a configured attempt limit is reached.

## When to use

Use iterative repair when a workflow may transiently fail (external services, flaky steps, or model-based steps that may produce correct results on a subsequent attempt) and it is acceptable to re-run the DAG from the same baseline inputs.

## Basic example (in-process)

The example below shows a small in-process DAG with a step that fails on the first attempt and succeeds on the second. We run the DAG using the `IterativeRepairStrategy` with `max_attempts=3` and capture attempt events.

```python
import asyncio
from agentic_v2 import DAG, StepDefinition
from agentic_v2.engine import IterativeRepairStrategy, ExecutionContext

async def flaky_step(ctx: ExecutionContext) -> dict:
    attempt = int(await ctx.get("attempt_number", 1))
    if attempt == 1:
        raise RuntimeError("transient failure")
    return {"ok": True}

# Build a single-step DAG
dag = DAG("flaky").add(StepDefinition(name="flaky", func=flaky_step))

# Capture attempt-level events
events = []
async def on_update(event: dict):
    events.append(event)

strategy = IterativeRepairStrategy(max_attempts=3)
result = await strategy.execute(dag, ExecutionContext(workflow_id="wf-flaky"), on_update=on_update)

print(result.overall_status)
print(result.metadata)
print([e for e in events if e.get("type") in ("attempt_start", "attempt_end")])
```

## Using with WorkflowRunner and YAML workflows

When running higher-level YAML-defined workflows with `WorkflowRunner`, pass an `execution_profile` to select iterative repair indirectly:

```python
from agentic_v2.workflows.runner import WorkflowRunner

runner = WorkflowRunner()
result = await runner.run("my_workflow", execution_profile={"max_attempts": 3})
```

`create_execution_strategy` will choose `IterativeRepairStrategy` by default when `max_attempts > 1` (unless `strategy` is explicitly provided in the profile).

## Observability

- `attempt_start` and `attempt_end` events are emitted when running under `IterativeRepairStrategy` and are delivered via the `on_update` callback.
- Workflow result metadata contains `attempt_history`, `attempts_used`, and `max_attempts` to help audit runs.

## Best practices

- Keep attempts small and idempotent: the strategy resets the context variables to the baseline input state before each attempt.
- Use `attempt_number` in step logic only for transient repair heuristics — prefer deterministic recovery where possible.
- Log attempt artifacts using a `RunLogger` if persistent artifacts are required for debugging.

