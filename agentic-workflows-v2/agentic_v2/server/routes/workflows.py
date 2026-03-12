"""Workflow execution, DAG visualization, and evaluation routes.

This is the primary route module, providing:

* ``GET /api/workflows`` -- list available workflow definitions.
* ``GET /api/workflows/{name}/dag`` -- return DAG nodes, edges, and input
  schema for React Flow visualization.
* ``GET /api/workflows/{name}/capabilities`` -- return workflow I/O declarations.
* ``POST /api/run`` -- execute a workflow asynchronously with optional
  dataset-backed evaluation scoring.

Run-history routes (``GET /api/runs``, ``GET /api/runs/summary``,
``GET /api/runs/{filename}``, ``GET /api/runs/{run_id}/stream``) are provided
by :mod:`~agentic_v2.server.routes.runs`.

Evaluation routes (``GET /api/eval/datasets``,
``GET /api/workflows/{name}/preview-dataset-inputs``) are provided by
:mod:`~agentic_v2.server.routes.evaluation_routes`.

Execution orchestration is provided by :mod:`~agentic_v2.server.execution`.
Pure result helpers live in :mod:`~agentic_v2.server.result_normalization`.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException

from ...contracts import StepStatus
from ...workflows.run_logger import RunLogger
from ..execution import _run_and_evaluate
from ..models import (
    ListWorkflowsResponse,
    WorkflowRunRequest,
    WorkflowRunResponse,
)
from ..result_normalization import _resolve_evaluation_inputs

# LangChain imports — optional at the package level.  Guard so the
# server module can be imported even without langchain extras.
try:
    from ...langchain import list_workflows as lc_list_workflows
    from ...langchain import load_workflow_config

    _LANGCHAIN_AVAILABLE = True
except ImportError:
    _LANGCHAIN_AVAILABLE = False

logger = logging.getLogger(__name__)
router = APIRouter(tags=["workflows"])
run_logger = RunLogger()


def _require_langchain() -> None:
    """Raise 501 if langchain extras are missing."""
    if not _LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="LangChain extras not installed. Install with: pip install -e '.[langchain]'",
        )


@router.get("/workflows", response_model=ListWorkflowsResponse)
async def list_workflows():
    """List available workflows."""
    _require_langchain()
    workflows = lc_list_workflows()
    return ListWorkflowsResponse(workflows=workflows)


@router.get("/adapters")
async def list_adapters():
    """List available execution engine adapters.

    Returns:
        JSON object with ``adapters`` key containing a list of registered
        adapter names (e.g. ``["native", "langchain"]``).
    """
    from ...adapters import get_registry

    registry = get_registry()
    names = registry.list_adapters()
    return {"adapters": names}


@router.get("/workflows/{name}/dag")
async def get_workflow_dag(name: str):
    """Return the DAG structure for visualization."""
    _require_langchain()
    try:
        wf = load_workflow_config(name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    nodes = []
    edges = []
    for step in wf.steps:
        nodes.append(
            {
                "id": step.name,
                "agent": step.agent,
                "description": step.description,
                "depends_on": list(step.depends_on),
                "tier": None,  # tier is embedded in agent name (e.g. tier2_reviewer)
            }
        )
        for dep in step.depends_on:
            edges.append({"source": dep, "target": step.name})

    # Include input schema so the UI can render a proper form
    input_schema = []
    for inp_name, inp in wf.inputs.items():
        input_schema.append(
            {
                "name": inp_name,
                "type": inp.type,
                "description": inp.description,
                "default": inp.default,
                "required": inp.required,
                "enum": inp.enum,
            }
        )

    return {
        "name": wf.name,
        "description": wf.description,
        "nodes": nodes,
        "edges": edges,
        "inputs": input_schema,
    }


@router.get("/workflows/{name}/capabilities")
async def get_workflow_capabilities(name: str):
    """Return workflow capability declarations (inputs/outputs)."""
    _require_langchain()
    try:
        wf = load_workflow_config(name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "workflow": wf.name,
        "capabilities": wf.capabilities,
    }


@router.post("/run", response_model=WorkflowRunResponse)
async def run_workflow(request: WorkflowRunRequest, background_tasks: BackgroundTasks):
    """Execute a workflow asynchronously."""
    adapter_name = request.adapter
    from ...adapters import get_registry as _get_adapter_registry

    try:
        _get_adapter_registry().get_adapter(adapter_name)
    except Exception:
        raise HTTPException(
            status_code=422,
            detail=f"Unknown adapter: {adapter_name!r}. "
            f"Available: {_get_adapter_registry().list_adapters()}",
        )

    if adapter_name == "langchain":
        _require_langchain()
    try:
        workflow_def = load_workflow_config(request.workflow)
        run_id = request.run_id or f"{workflow_def.name}-{uuid.uuid4().hex[:8]}"
        workflow_inputs = dict(request.input_data)
        evaluation = request.evaluation
        dataset_sample: dict[str, Any] | None = None
        dataset_meta: dict[str, Any] | None = None

        if evaluation and evaluation.enabled:
            workflow_inputs, dataset_sample, dataset_meta = _resolve_evaluation_inputs(
                workflow_def,
                evaluation,
                run_id,
                workflow_inputs,
                artifacts_dir=run_logger.runs_dir / "_inputs",
            )

        background_tasks.add_task(
            _run_and_evaluate,
            request.workflow,
            run_id,
            workflow_inputs,
            workflow_def,
            evaluation,
            dataset_sample,
            dataset_meta,
            adapter_name,
        )
        return WorkflowRunResponse(run_id=run_id, status=StepStatus.PENDING)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
