"""DAG executor with dynamic parallel scheduling.

Executes steps as soon as their dependencies are satisfied.
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
    """Execute a DAG with maximum parallelism."""

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
        """Execute DAG with dynamic scheduling and concurrency limits."""
        if ctx is None:
            ctx = get_context()

        dag.validate()

        result = WorkflowResult(
            workflow_id=ctx.workflow_id,
            workflow_name=dag.name,
            overall_status=StepStatus.RUNNING,
        )
        
        if on_update:
            await on_update({
                "type": "workflow_start",
                "run_id": result.workflow_id,
                "workflow": result.workflow_name,
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

        def cascade_skip(start_step: str, reason: str) -> None:
            queue = deque([start_step])
            while queue:
                current = queue.popleft()
                for dependent in adjacency.get(current, []):
                    if dependent in completed or dependent in skipped:
                        continue
                    mark_skipped(dependent, reason)
                    queue.append(dependent)

        tasks: set[asyncio.Task] = set()

        while len(completed) < len(dag.steps):
            while ready and len(running) < max_concurrency:
                step_name = ready.popleft()
                if step_name in completed or step_name in skipped:
                    continue
                running.add(step_name)
                self._state_manager.transition(step_name, StepState.READY)
                tasks.add(asyncio.create_task(run_step(step_name)))

            if not tasks:
                remaining = set(dag.steps.keys()) - completed - skipped
                for step_name in remaining:
                    mark_skipped(step_name, "unmet dependencies")
                break

            done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

            for task in done:
                step_name, step_result = task.result()
                running.discard(step_name)
                results[step_name] = step_result
                result.add_step(step_result)
                completed.add(step_name)
                
                if on_update:
                    await on_update({
                        "type": "step_end",
                        "run_id": result.workflow_id,
                        "step": step_name,
                        "status": step_result.status.value,
                        "duration_ms": step_result.duration_ms,
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    })

                if step_result.status == StepStatus.SUCCESS:
                    self._state_manager.transition(step_name, StepState.SUCCESS)
                elif step_result.status == StepStatus.SKIPPED:
                    self._state_manager.transition(step_name, StepState.SKIPPED)
                else:
                    self._state_manager.transition(step_name, StepState.FAILED)

                if step_result.is_failed:
                    result.overall_status = StepStatus.FAILED
                    cascade_skip(step_name, "dependency failed")
                    continue

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
