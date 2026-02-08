"""Workflow routes."""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from typing import Any, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse

from ...contracts import StepStatus
from ...engine import DAGExecutor, ExecutionContext
from ...workflows import WorkflowLoader
from ...workflows.run_logger import RunLogger
from .. import websocket
from ..models import (
    ListWorkflowsResponse,
    WorkflowRunRequest,
    WorkflowRunResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["workflows"])
loader = WorkflowLoader()
executor = DAGExecutor()
run_logger = RunLogger()


@router.get("/workflows", response_model=ListWorkflowsResponse)
async def list_workflows():
    """List available workflows."""
    workflows = loader.list_workflows()
    return ListWorkflowsResponse(workflows=workflows)


@router.get("/workflows/{name}/dag")
async def get_workflow_dag(name: str):
    """Return the DAG structure for visualization."""
    try:
        wf = loader.load(name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    dag = wf.dag
    nodes = []
    edges = []
    for step_name, step in dag.steps.items():
        nodes.append({
            "id": step_name,
            "agent": step.metadata.get("agent"),
            "description": step.description,
            "depends_on": list(step.depends_on),
            "tier": step.tier.name if step.tier else None,
        })
        for dep in step.depends_on:
            edges.append({"source": dep, "target": step_name})

    # Include input schema so the UI can render a proper form
    input_schema = []
    for inp_name, inp in wf.inputs.items():
        input_schema.append({
            "name": inp_name,
            "type": inp.type,
            "description": inp.description,
            "default": inp.default,
            "required": inp.required,
            "enum": inp.enum,
        })

    return {
        "name": wf.name,
        "description": wf.description,
        "nodes": nodes,
        "edges": edges,
        "inputs": input_schema,
    }


@router.get("/runs")
async def list_runs(
    workflow: Optional[str] = None,
    limit: int = 50,
):
    """List past workflow runs with summary data."""
    paths = run_logger.list_runs(workflow_name=workflow)[-limit:]
    results = []
    for p in reversed(paths):
        try:
            record = run_logger.load_run(p)
            results.append({
                "filename": p.name,
                **{
                    k: v
                    for k, v in record.items()
                    if k
                    in (
                        "run_id",
                        "workflow_name",
                        "status",
                        "success_rate",
                        "total_duration_ms",
                        "step_count",
                        "failed_step_count",
                        "start_time",
                        "end_time",
                    )
                },
            })
        except Exception as e:
            logger.warning("Failed to load run %s: %s", p.name, e)
    return results


@router.get("/runs/summary")
async def runs_summary(workflow: Optional[str] = None):
    """Aggregate stats across runs."""
    return run_logger.summary(workflow_name=workflow)


@router.get("/runs/{filename}")
async def get_run(filename: str):
    """Get full run detail including all step data."""
    path = run_logger.runs_dir / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Run not found: {filename}")
    return run_logger.load_run(path)


@router.get("/runs/{run_id}/stream")
async def stream_run_events(run_id: str):
    """SSE stream of execution events for a running workflow."""

    async def event_generator():
        queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        websocket.manager.register_sse_listener(run_id, queue)
        try:
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=30)
                    yield f"data: {json.dumps(event)}\n\n"
                    if event.get("type") == "workflow_end":
                        break
                except asyncio.TimeoutError:
                    yield f"data: {json.dumps({'type': 'keepalive'})}\n\n"
        finally:
            websocket.manager.unregister_sse_listener(run_id, queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/run", response_model=WorkflowRunResponse)
async def run_workflow(request: WorkflowRunRequest, background_tasks: BackgroundTasks):
    """Execute a workflow asynchronously."""
    try:
        workflow_def = loader.load(request.workflow)
        dag = workflow_def.dag

        # Determine run_id
        run_id = request.run_id or f"{workflow_def.name}-{uuid.uuid4().hex[:8]}"

        # Execute workflow — put inputs under "inputs" namespace
        # so YAML ${inputs.code_file} expressions resolve correctly.
        ctx = ExecutionContext(workflow_id=run_id)
        ctx.set_sync("inputs", request.input_data)
        # Also set top-level for backwards compat
        for key, value in request.input_data.items():
            ctx.set_sync(key, value)

        async def event_callback(event: dict[str, Any]):
            await websocket.manager.broadcast(run_id, event)

        async def _run_workflow_task():
            try:
                logger.info(f"Starting background execution for run_id={run_id}")
                await executor.execute(dag, ctx=ctx, on_update=event_callback)
                logger.info(f"Completed background execution for run_id={run_id}")
            except Exception as e:
                logger.error(
                    f"Error in background execution for run_id={run_id}: {e}",
                    exc_info=True,
                )
                await websocket.manager.broadcast(
                    run_id, {"type": "error", "run_id": run_id, "error": str(e)}
                )

        background_tasks.add_task(_run_workflow_task)

        return WorkflowRunResponse(run_id=run_id, status=StepStatus.PENDING)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
