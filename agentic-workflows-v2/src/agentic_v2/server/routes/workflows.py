"""Workflow routes."""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse

from ...contracts import StepStatus
from ...engine import ExecutionContext
from ...workflows import WorkflowLoader, WorkflowRunner
from ...workflows.run_logger import RunLogger
from ..evaluation import (
    adapt_sample_to_workflow_inputs,
    list_local_datasets,
    list_repository_datasets,
    load_local_dataset_sample,
    load_repository_dataset_sample,
    match_workflow_dataset,
    score_workflow_result,
    validate_required_inputs_present,
)
from .. import websocket
from ..models import (
    ListEvaluationDatasetsResponse,
    ListWorkflowsResponse,
    WorkflowRunRequest,
    WorkflowRunResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["workflows"])
loader = WorkflowLoader()
runner = WorkflowRunner(run_logger=False)
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


@router.get("/workflows/{name}/capabilities")
async def get_workflow_capabilities(name: str):
    """Return workflow capability declarations (inputs/outputs)."""
    try:
        wf = loader.load(name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "workflow": wf.name,
        "capabilities": {
            "inputs": list(wf.capabilities.inputs),
            "outputs": list(wf.capabilities.outputs),
        },
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
            extra = record.get("extra") if isinstance(record.get("extra"), dict) else {}
            evaluation = (
                extra.get("evaluation")
                if isinstance(extra.get("evaluation"), dict)
                else {}
            )
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
                "evaluation_score": evaluation.get("weighted_score"),
                "evaluation_grade": evaluation.get("grade"),
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
                    if event.get("type") in {"evaluation_complete", "workflow_end"}:
                        break
                except asyncio.TimeoutError:
                    yield f"data: {json.dumps({'type': 'keepalive'})}\n\n"
        finally:
            websocket.manager.unregister_sse_listener(run_id, queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/eval/datasets", response_model=ListEvaluationDatasetsResponse)
async def list_evaluation_datasets(workflow: Optional[str] = None):
    """List repository and local dataset options for workflow evaluation."""
    repository = list_repository_datasets()
    local = list_local_datasets()

    if workflow:
        try:
            workflow_def = loader.load(workflow)
        except Exception as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        filtered_local: list[dict[str, Any]] = []
        for dataset in local:
            try:
                sample, _ = load_local_dataset_sample(dataset["id"], sample_index=0)
            except Exception:
                continue
            compatible, _ = match_workflow_dataset(workflow_def, sample)
            if compatible:
                filtered_local.append(dataset)

        filtered_repository: list[dict[str, Any]] = []
        for dataset in repository:
            try:
                sample, _ = load_repository_dataset_sample(dataset["id"], sample_index=0)
            except Exception:
                # Repository datasets may be unavailable in local dev; skip when
                # compatibility cannot be determined.
                continue
            compatible, _ = match_workflow_dataset(workflow_def, sample)
            if compatible:
                filtered_repository.append(dataset)

        repository = filtered_repository
        local = filtered_local

    return ListEvaluationDatasetsResponse(
        repository=repository,
        local=local,
    )


@router.post("/run", response_model=WorkflowRunResponse)
async def run_workflow(request: WorkflowRunRequest, background_tasks: BackgroundTasks):
    """Execute a workflow asynchronously."""
    try:
        workflow_def = loader.load(request.workflow)

        # Determine run_id
        run_id = request.run_id or f"{workflow_def.name}-{uuid.uuid4().hex[:8]}"
        workflow_inputs = dict(request.input_data)
        evaluation = request.evaluation
        dataset_sample: dict[str, Any] | None = None
        dataset_meta: dict[str, Any] | None = None

        if evaluation and evaluation.enabled:
            try:
                if evaluation.dataset_source == "repository":
                    if not evaluation.dataset_id:
                        raise HTTPException(
                            status_code=422,
                            detail="evaluation.dataset_id is required for repository datasets",
                        )
                    dataset_sample, dataset_meta = load_repository_dataset_sample(
                        evaluation.dataset_id,
                        sample_index=evaluation.sample_index,
                    )
                elif evaluation.dataset_source == "local":
                    dataset_ref = evaluation.local_dataset_path or evaluation.dataset_id
                    if not dataset_ref:
                        raise HTTPException(
                            status_code=422,
                            detail=(
                                "evaluation.dataset_id or evaluation.local_dataset_path is "
                                "required for local datasets"
                            ),
                        )
                    dataset_sample, dataset_meta = load_local_dataset_sample(
                        dataset_ref,
                        sample_index=evaluation.sample_index,
                    )
            except ValueError as exc:
                raise HTTPException(status_code=422, detail=str(exc)) from exc

            if dataset_sample:
                compatible, reasons = match_workflow_dataset(workflow_def, dataset_sample)
                if not compatible:
                    raise HTTPException(
                        status_code=422,
                        detail={
                            "message": "Dataset sample is incompatible with workflow inputs",
                            "reasons": reasons,
                        },
                    )

                adapted_inputs = adapt_sample_to_workflow_inputs(
                    workflow_def.inputs,
                    dataset_sample,
                    run_id=run_id,
                    artifacts_dir=run_logger.runs_dir / "_inputs",
                )
                # Request input_data takes precedence over adapted dataset inputs
                workflow_inputs = {**adapted_inputs, **workflow_inputs}
                dataset_meta = {
                    **(dataset_meta or {}),
                    "dataset_workflow_compatible": True,
                    "dataset_mismatch_reasons": [],
                }

                missing_required = validate_required_inputs_present(
                    workflow_def.inputs,
                    workflow_inputs,
                )
                if missing_required:
                    raise HTTPException(
                        status_code=422,
                        detail={
                            "message": "Missing required workflow inputs after dataset adaptation",
                            "missing_inputs": missing_required,
                        },
                    )

        # Execute workflow — put inputs under "inputs" namespace
        # so YAML ${inputs.code_file} expressions resolve correctly.
        ctx = ExecutionContext(workflow_id=run_id)
        ctx.set_sync("inputs", workflow_inputs)
        # Also set top-level for backwards compat
        for key, value in workflow_inputs.items():
            ctx.set_sync(key, value)

        async def event_callback(event: dict[str, Any]):
            await websocket.manager.broadcast(run_id, event)

        async def _run_workflow_task():
            try:
                logger.info(f"Starting background execution for run_id={run_id}")
                result = await runner.run(
                    request.workflow,
                    ctx=ctx,
                    on_update=event_callback,
                    **workflow_inputs,
                )

                scored_evaluation: dict[str, Any] | None = None
                if evaluation and evaluation.enabled:
                    await websocket.manager.broadcast(
                        run_id,
                        {
                            "type": "evaluation_start",
                            "run_id": run_id,
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        },
                    )
                    scored_evaluation = score_workflow_result(
                        result,
                        dataset_meta=dataset_meta,
                        dataset_sample=dataset_sample,
                        rubric=(evaluation.rubric_id or evaluation.rubric),
                        workflow_definition=workflow_def,
                        enforce_hard_gates=evaluation.enforce_hard_gates,
                    )
                    await websocket.manager.broadcast(
                        run_id,
                        {
                            "type": "evaluation_complete",
                            "run_id": run_id,
                            "rubric": scored_evaluation["rubric"],
                            "rubric_id": scored_evaluation["rubric_id"],
                            "rubric_version": scored_evaluation["rubric_version"],
                            "weighted_score": scored_evaluation["weighted_score"],
                            "overall_score": scored_evaluation["overall_score"],
                            "grade": scored_evaluation["grade"],
                            "passed": scored_evaluation["passed"],
                            "pass_threshold": scored_evaluation["pass_threshold"],
                            "criteria": scored_evaluation["criteria"],
                            "hard_gates": scored_evaluation["hard_gates"],
                            "hard_gate_failures": scored_evaluation["hard_gate_failures"],
                            "step_scores": scored_evaluation["step_scores"],
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                        },
                    )

                run_logger.log(
                    result,
                    dataset_meta=dataset_meta,
                    workflow_inputs=workflow_inputs,
                    extra={
                        "evaluation_requested": bool(evaluation and evaluation.enabled),
                        "evaluation": scored_evaluation,
                    },
                )
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
