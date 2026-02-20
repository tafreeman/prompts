"""Workflow routes."""

from __future__ import annotations

import asyncio
import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Optional
import os

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse

from ...contracts import StepStatus
from ...integrations.otel import create_trace_adapter
from ...langchain import WorkflowRunner as LangChainRunner
from ...langchain import list_workflows as lc_list_workflows
from ...langchain import load_workflow_config
from ...workflows.run_logger import RunLogger
from ..evaluation import (
    adapt_sample_to_workflow_inputs,
    list_local_datasets,
    list_repository_datasets,
    list_eval_sets,
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
# LangChain runner — primary execution engine for this branch
lc_runner = LangChainRunner(trace_adapter=create_trace_adapter())
run_logger = RunLogger()


def _is_within_base(path, base_dir) -> bool:
    """
    Return True if ``path`` is within ``base_dir`` after resolution.

    Uses pathlib's is_relative_to when available, with a safe fallback
    for older Python versions.
    """
    from pathlib import Path

    resolved_base = Path(base_dir).resolve()
    resolved_path = Path(path).resolve()
    try:
        return resolved_path.is_relative_to(resolved_base)
    except AttributeError:
        base_str = os.fspath(resolved_base)
        path_str = os.fspath(resolved_path)
        if path_str == base_str:
            return True
        return path_str.startswith(base_str + os.sep)


def _is_effectively_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) == 0
    return False


def _merge_dataset_and_request_inputs(
    adapted_inputs: dict[str, Any],
    request_inputs: dict[str, Any],
) -> dict[str, Any]:
    """
    Merge adapted dataset inputs with request inputs.

    Request inputs normally take precedence, except when a request value is
    effectively empty and an adapted value already exists for that key.
    This prevents blank form fields from overriding dataset-derived values.
    """
    merged = dict(adapted_inputs)
    for key, value in request_inputs.items():
        if _is_effectively_empty(value) and key in merged:
            continue
        merged[key] = value
    return merged


@router.get("/workflows", response_model=ListWorkflowsResponse)
async def list_workflows():
    """List available workflows."""
    workflows = lc_list_workflows()
    return ListWorkflowsResponse(workflows=workflows)


@router.get("/workflows/{name}/dag")
async def get_workflow_dag(name: str):
    """Return the DAG structure for visualization."""
    try:
        wf = load_workflow_config(name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    nodes = []
    edges = []
    for step in wf.steps:
        nodes.append({
            "id": step.name,
            "agent": step.agent,
            "description": step.description,
            "depends_on": list(step.depends_on),
            "tier": None,  # tier is embedded in agent name (e.g. tier2_reviewer)
        })
        for dep in step.depends_on:
            edges.append({"source": dep, "target": step.name})

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
        wf = load_workflow_config(name)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return {
        "workflow": wf.name,
        "capabilities": wf.capabilities,
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
    from pathlib import Path

    base_dir = run_logger.runs_dir
    candidate = (base_dir / filename).resolve()
    if not _is_within_base(candidate, base_dir):
        # Do not leak filesystem layout; treat as not found
        raise HTTPException(status_code=404, detail=f"Run not found: {filename}")
    if not Path(candidate).exists():
        raise HTTPException(status_code=404, detail=f"Run not found: {filename}")
    return run_logger.load_run(candidate)


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
    eval_sets = list_eval_sets()

    if workflow:
        try:
            workflow_def = load_workflow_config(workflow)
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
        eval_sets=eval_sets,
    )


@router.get("/workflows/{workflow_name}/preview-dataset-inputs")
async def preview_dataset_inputs(
    workflow_name: str,
    dataset_source: str,
    dataset_id: str,
    sample_index: int = 0,
):
    """Preview how dataset sample fields will map to workflow inputs."""
    try:
        workflow_def = load_workflow_config(workflow_name)
    except Exception as exc:
        raise HTTPException(status_code=404, detail=f"Workflow not found: {exc}") from exc

    try:
        if dataset_source == "repository":
            dataset_sample, dataset_meta = load_repository_dataset_sample(
                dataset_id,
                sample_index=sample_index,
            )
        elif dataset_source == "local":
            dataset_sample, dataset_meta = load_local_dataset_sample(
                dataset_id,
                sample_index=sample_index,
            )
        else:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid dataset_source: {dataset_source}",
            )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    compatible, reasons = match_workflow_dataset(workflow_def, dataset_sample)
    if not compatible:
        return {
            "compatible": False,
            "reasons": reasons,
            "adapted_inputs": {},
            "dataset_meta": dataset_meta,
        }

    adapted_inputs = adapt_sample_to_workflow_inputs(
        workflow_def.inputs,
        dataset_sample,
        run_id="preview",
        artifacts_dir=run_logger.runs_dir / "_inputs",
    )

    return {
        "compatible": True,
        "reasons": [],
        "adapted_inputs": adapted_inputs,
        "dataset_meta": dataset_meta,
    }


def _load_dataset_sample(evaluation: Any) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    """Load a dataset sample based on evaluation config. Returns (sample, meta)."""
    if evaluation.dataset_source == "repository":
        if not evaluation.dataset_id:
            raise HTTPException(
                status_code=422,
                detail="evaluation.dataset_id is required for repository datasets",
            )
        return load_repository_dataset_sample(
            evaluation.dataset_id,
            sample_index=evaluation.sample_index,
        )
    if evaluation.dataset_source == "local":
        dataset_ref = evaluation.local_dataset_path or evaluation.dataset_id
        if not dataset_ref:
            raise HTTPException(
                status_code=422,
                detail=(
                    "evaluation.dataset_id or evaluation.local_dataset_path is "
                    "required for local datasets"
                ),
            )
        return load_local_dataset_sample(dataset_ref, sample_index=evaluation.sample_index)
    return None, None


def _resolve_evaluation_inputs(
    workflow_def: Any,
    evaluation: Any,
    run_id: str,
    workflow_inputs: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any] | None, dict[str, Any] | None]:
    """Load + adapt dataset sample; return (merged_inputs, dataset_sample, dataset_meta)."""
    try:
        dataset_sample, dataset_meta = _load_dataset_sample(evaluation)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if not dataset_sample:
        return workflow_inputs, dataset_sample, dataset_meta

    compatible, reasons = match_workflow_dataset(workflow_def, dataset_sample)
    if not compatible:
        raise HTTPException(
            status_code=422,
            detail={"message": "Dataset sample is incompatible with workflow inputs", "reasons": reasons},
        )

    adapted = adapt_sample_to_workflow_inputs(
        workflow_def.inputs,
        dataset_sample,
        run_id=run_id,
        artifacts_dir=run_logger.runs_dir / "_inputs",
    )
    merged = _merge_dataset_and_request_inputs(adapted, workflow_inputs)
    dataset_meta = {**(dataset_meta or {}), "dataset_workflow_compatible": True, "dataset_mismatch_reasons": []}

    missing = validate_required_inputs_present(workflow_def.inputs, merged)
    if missing:
        raise HTTPException(
            status_code=422,
            detail={"message": "Missing required workflow inputs after dataset adaptation", "missing_inputs": missing},
        )
    return merged, dataset_sample, dataset_meta


async def _stream_and_run(
    workflow_name: str,
    run_id: str,
    workflow_inputs: dict[str, Any],
) -> Any:
    """Stream LangGraph node events to WebSocket, then return final WorkflowResult."""
    import time

    step_start_times: dict[str, float] = {}
    try:
        async for node_update in lc_runner.astream(workflow_name, thread_id=run_id, **workflow_inputs):
            for step_name, step_state in node_update.items():
                if not isinstance(step_state, dict):
                    continue
                step_data = step_state.get("steps", {}).get(step_name, {})
                status = step_data.get("status", "running")
                now = datetime.now(timezone.utc).isoformat()
                if status == "running":
                    step_start_times[step_name] = time.time()
                    await websocket.manager.broadcast(
                        run_id, {"type": "step_start", "run_id": run_id, "step": step_name, "timestamp": now}
                    )
                elif status in ("success", "failed"):
                    duration_ms = int((time.time() - step_start_times.pop(step_name, time.time())) * 1000)
                    await websocket.manager.broadcast(
                        run_id,
                        {
                            "type": "step_complete" if status == "success" else "step_error",
                            "run_id": run_id,
                            "step": step_name,
                            "status": status,
                            "outputs": step_data.get("outputs", {}),
                            "duration_ms": duration_ms,
                            "timestamp": now,
                        },
                    )
        return await lc_runner.run(workflow_name, use_cache=True, **workflow_inputs)
    except Exception as stream_err:
        logger.warning("Streaming failed (%s); falling back to invoke", stream_err)
        return await lc_runner.run(workflow_name, **workflow_inputs)


async def _run_and_evaluate(
    workflow_name: str,
    run_id: str,
    workflow_inputs: dict[str, Any],
    workflow_def: Any,
    evaluation: Any,
    dataset_sample: dict[str, Any] | None,
    dataset_meta: dict[str, Any] | None,
) -> None:
    """Execute workflow, broadcast events, optionally evaluate, and log the run."""
    try:
        logger.info("Starting background execution for run_id=%s", run_id)
        result = await _stream_and_run(workflow_name, run_id, workflow_inputs)

        # Handle both new LangChain WorkflowResult (status) and legacy (overall_status)
        status = getattr(result, 'status', None) or getattr(result, 'overall_status', 'unknown')
        await websocket.manager.broadcast(
            run_id,
            {
                "type": "workflow_end",
                "run_id": run_id,
                "status": status,
                "outputs": getattr(result, 'outputs', None) or getattr(result, 'final_output', {}),
                "elapsed_seconds": getattr(result, 'elapsed_seconds', 0.0),
                "errors": getattr(result, 'errors', []),
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

        scored_evaluation: dict[str, Any] | None = None
        if evaluation and evaluation.enabled:
            await websocket.manager.broadcast(
                run_id, {"type": "evaluation_start", "run_id": run_id, "timestamp": datetime.now(timezone.utc).isoformat()}
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
                    **{k: scored_evaluation[k] for k in (
                        "rubric", "rubric_id", "rubric_version", "weighted_score",
                        "overall_score", "grade", "passed", "pass_threshold",
                        "criteria", "hard_gates", "hard_gate_failures", "step_scores",
                    )},
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
        logger.info("Completed background execution for run_id=%s", run_id)
    except Exception as e:
        logger.error("Error in background execution for run_id=%s: %s", run_id, e, exc_info=True)
        await websocket.manager.broadcast(run_id, {"type": "error", "run_id": run_id, "error": str(e)})


@router.post("/run", response_model=WorkflowRunResponse)
async def run_workflow(request: WorkflowRunRequest, background_tasks: BackgroundTasks):
    """Execute a workflow asynchronously."""
    try:
        workflow_def = load_workflow_config(request.workflow)
        run_id = request.run_id or f"{workflow_def.name}-{uuid.uuid4().hex[:8]}"
        workflow_inputs = dict(request.input_data)
        evaluation = request.evaluation
        dataset_sample: dict[str, Any] | None = None
        dataset_meta: dict[str, Any] | None = None

        if evaluation and evaluation.enabled:
            workflow_inputs, dataset_sample, dataset_meta = _resolve_evaluation_inputs(
                workflow_def, evaluation, run_id, workflow_inputs
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
        )
        return WorkflowRunResponse(run_id=run_id, status=StepStatus.PENDING)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
