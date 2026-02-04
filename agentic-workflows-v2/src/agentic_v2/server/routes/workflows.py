"""Workflow routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from ...engine import DAGExecutor, ExecutionContext
from ...workflows import WorkflowLoader
from ..models import (ListWorkflowsResponse, WorkflowRunRequest,
                      WorkflowRunResponse)

router = APIRouter(tags=["workflows"])
loader = WorkflowLoader()
executor = DAGExecutor()


@router.get("/workflows", response_model=ListWorkflowsResponse)
async def list_workflows():
    """List available workflows."""
    workflows = loader.list_workflows()
    return ListWorkflowsResponse(workflows=workflows)


@router.post("/run", response_model=WorkflowRunResponse)
async def run_workflow(request: WorkflowRunRequest):
    """Execute a workflow."""
    try:
        workflow_def = loader.load(request.workflow)
        dag = workflow_def.dag

        # Execute workflow
        # Note: In a production app, this should be handled by a task queue
        ctx = ExecutionContext(workflow_id=workflow_def.name)
        for key, value in request.input_data.items():
            ctx.set_sync(key, value)

        result = await executor.execute(dag, ctx=ctx)

        return WorkflowRunResponse(
            run_id=result.workflow_id, status=result.overall_status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
