"""DAG executor with dynamic parallel scheduling.

Executes workflow steps as soon as their upstream dependencies are satisfied,
achieving maximum parallelism without artificial layer barriers.

Key design decisions:
- **Kahn's algorithm** for in-degree tracking at runtime (not just ordering).
- **asyncio.wait(FIRST_COMPLETED)** to unblock downstream steps the instant
  an upstream finishes, rather than waiting for an entire "wave" to complete.
- **Cascade skip** via BFS: when a step fails, all transitive dependents are
  marked SKIPPED so the executor can still finish cleanly.
- **Deadlock detection**: if no tasks are running and steps remain, unmet
  dependencies are flagged and the remaining steps are skipped.
"""

from __future__ import annotations

import asyncio
from collections import deque
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, Optional

from ..contracts import StepResult, StepStatus, WorkflowResult
from .context import ExecutionContext, get_context
from .dag import DAG
from .step import StepExecutor
from .step_state import StepState, StepStateManager


class DAGExecutor:
    """Execute a DAG with maximum parallelism.

    Orchestrates the full lifecycle of a workflow run: validation,
    scheduling, parallel execution, failure propagation, and result
    assembly.  Uses :class:`StepExecutor` for individual step runs and
    :class:`StepStateManager` for lifecycle state tracking.

    Attributes:
        _step_executor: Delegate that handles single-step execution
            (input mapping, retry, timeout, hooks).
        _state_manager: Tracks ``PENDING → READY → RUNNING → SUCCESS``
            (or FAILED/SKIPPED) transitions per step.
    """

    def __init__(self, step_executor: Optional[StepExecutor] = None):
        self._step_executor = step_executor or StepExecutor()
        self._state_manager = StepStateManager()

    async def execute(
        self,
        dag: DAG,
        ctx: Optional[ExecutionContext] = None,
        max_concurrency: int = 10,
        on_update: Optional[Callable[[dict[str, Any]], Awaitable[None]]] = None,
    ) -> WorkflowResult:
        """Execute a validated DAG with dynamic scheduling and concurrency limits.

        Execution proceeds in a tight loop:

        1. **Schedule** — pop ready steps (in-degree 0) up to *max_concurrency*.
        2. **Deadlock check** — if no tasks running and steps remain, skip them.
        3. **Await** — ``asyncio.wait(FIRST_COMPLETED)`` for the next result.
        4. **Handle outcome** — on success, decrement downstream in-degrees;
           on failure, cascade-skip all transitive dependents.
        5. **Repeat** until every step is completed or skipped.

        Args:
            dag: Validated DAG definition to execute.
            ctx: Shared execution context.  A new one is created if *None*.
            max_concurrency: Upper bound on simultaneously running steps.
            on_update: Optional async callback invoked on every lifecycle
                event (``workflow_start``, ``step_start``, ``step_end``,
                ``workflow_end``).  Used by the server layer to broadcast
                real-time updates via WebSocket/SSE.

        Returns:
            :class:`WorkflowResult` with per-step results, overall status,
            and the final merged context as ``final_output``.
        """
        if ctx is None:
            ctx = get_context()

        dag.validate()

        # Fresh state manager per execution to avoid cross-run pollution
        self._state_manager = StepStateManager()

        result = WorkflowResult(
            workflow_id=ctx.workflow_id,
            workflow_name=dag.name,
            overall_status=StepStatus.RUNNING,
        )
        
        if on_update:
            await on_update({
                "type": "workflow_start",
                "run_id": result.workflow_id,
                "workflow_name": result.workflow_name,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        adjacency = dag.build_adjacency_list()
        in_degree = {name: len(step.depends_on) for name, step in dag.steps.items()}

        ready = deque([name for name, deg in in_degree.items() if deg == 0])
        running: set[str] = set()
        completed: set[str] = set()
        skipped: set[str] = set()
        results: dict[str, StepResult] = {}

        async def run_step(step_name: str) -> tuple[str, StepResult]:
            """Execute a single step and return its name + result tuple."""
            self._state_manager.transition(step_name, StepState.RUNNING)
            if on_update:
                await on_update({
                    "type": "step_start",
                    "run_id": result.workflow_id,
                    "step": step_name,
                    "timestamp": datetime.now(timezone.utc).isoformat()
                })
            step_def = dag.steps[step_name]
            step_result = await self._step_executor.execute(step_def, ctx)
            return step_name, step_result

        def mark_skipped(step_name: str, reason: str) -> None:
            """Record a step as SKIPPED with a human-readable reason."""
            if step_name in completed or step_name in skipped:
                return
            step_result = StepResult(step_name=step_name, status=StepStatus.SKIPPED)
            step_result.metadata["skip_reason"] = reason
            step_result.end_time = datetime.now(timezone.utc)
            results[step_name] = step_result
            result.add_step(step_result)
            completed.add(step_name)
            skipped.add(step_name)
            self._state_manager.set_state(step_name, StepState.SKIPPED)
            # Mark as complete in ctx so downstream should_run() dependency
            # checks pass.  Skipped steps are logically "done" — they just
            # didn't produce output.
            if step_name not in ctx.completed_steps:
                ctx.completed_steps.append(step_name)

        def cascade_skip(start_step: str, reason: str) -> None:
            """BFS from *start_step* to skip all transitive dependents."""
            queue = deque([start_step])
            while queue:
                current = queue.popleft()
                for dependent in adjacency.get(current, []):
                    if dependent in completed or dependent in skipped:
                        continue
                    mark_skipped(dependent, reason)
                    queue.append(dependent)

        tasks: set[asyncio.Task] = set()

        # Phase 2: Execution Loop
        # We continue until every step in the DAG is either completed or skipped.
        while len(completed) < len(dag.steps):
            
            # 1. Schedule all currently 'ready' steps (those with in-degree 0)
            # obeying the max_concurrency limit.
            while ready and len(running) < max_concurrency:
                step_name = ready.popleft()
                if step_name in completed or step_name in skipped:
                    continue
                    
                running.add(step_name)
                # Move state to READY before spawning task
                self._state_manager.transition(step_name, StepState.READY)
                tasks.add(asyncio.create_task(run_step(step_name)))

            # 2. Deadlock detection
            # If no tasks are running but we aren't done, some steps are unreachable.
            if not tasks:
                remaining = set(dag.steps.keys()) - completed - skipped
                for step_name in remaining:
                    mark_skipped(step_name, "unmet dependencies")
                break

            # 3. Wait for the next task to complete
            done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                step_name, step_result = task.result()
                running.discard(step_name)
                results[step_name] = step_result
                result.add_step(step_result)
                completed.add(step_name)
                
                # Signal step completion to external observers (e.g., UI/WebSockets)
                if on_update:
                    await on_update({
                        "type": "step_end",
                        "run_id": result.workflow_id,
                        "step": step_name,
                        "status": step_result.status.value,
                        "duration_ms": step_result.duration_ms,
                        "model_used": step_result.model_used,
                        "tokens_used": step_result.metadata.get("tokens_used"),
                        "tier": step_result.tier,
                        "input": step_result.input_data,
                        "output": step_result.output_data,
                        "error": step_result.error,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })

                # 4. Handle step outcome
                if step_result.status == StepStatus.SUCCESS:
                    self._state_manager.transition(step_name, StepState.SUCCESS)
                elif step_result.status == StepStatus.SKIPPED:
                    self._state_manager.transition(step_name, StepState.SKIPPED)
                    # Skipped via should_run() (condition not met).  Mark
                    # complete in ctx so downstream dependencies can proceed.
                    if step_name not in ctx.completed_steps:
                        ctx.completed_steps.append(step_name)
                    skipped.add(step_name)
                else:
                    self._state_manager.transition(step_name, StepState.FAILED)

                # 5. Failure propagation
                # If a step fails, we must skip all steps that depend on it.
                if step_result.is_failed:
                    result.overall_status = StepStatus.FAILED
                    cascade_skip(step_name, "dependency failed")
                    continue

                # 6. Unlock downstream steps
                # Decrement in-degree of all direct dependents.
                # If a dependent's in-degree reaches 0, it is now 'ready'.
                for dependent in adjacency.get(step_name, []):
                    if dependent in completed or dependent in skipped:
                        continue
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        ready.append(dependent)

        if result.overall_status == StepStatus.RUNNING:
            result.overall_status = StepStatus.SUCCESS

        result.final_output = ctx.all_variables()
        result.mark_complete(result.overall_status == StepStatus.SUCCESS)

        if on_update:
            await on_update({
                "type": "workflow_end",
                "run_id": result.workflow_id,
                "status": result.overall_status.value,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })

        return result
