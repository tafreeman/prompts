"""Workflow routes."""

from __future__ import annotations

import logging
import uuid
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException

from ...engine import DAGExecutor, ExecutionContext, StepStatus
from ...workflows import WorkflowLoader
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


@router.get("/workflows", response_model=ListWorkflowsResponse)
async def list_workflows():
    """List available workflows."""
    workflows = loader.list_workflows()
    return ListWorkflowsResponse(workflows=workflows)


@router.post("/run", response_model=WorkflowRunResponse)
async def run_workflow(request: WorkflowRunRequest, background_tasks: BackgroundTasks):
    """Execute a workflow asynchronously."""
    try:
        workflow_def = loader.load(request.workflow)
        dag = workflow_def.dag

        # Determine run_id
        run_id = request.run_id or f"{workflow_def.name}-{uuid.uuid4().hex[:8]}"

        # Execute workflow
        ctx = ExecutionContext(workflow_id=run_id)
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
                logger.error(f"Error in background execution for run_id={run_id}: {e}", exc_info=True)
                # Emit error event
                await websocket.manager.broadcast(run_id, {
                    "type": "error",
                    "run_id": run_id,
                    "error": str(e)
                })

        background_tasks.add_task(_run_workflow_task)

        return WorkflowRunResponse(
            run_id=run_id, status=StepStatus.PENDING
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
