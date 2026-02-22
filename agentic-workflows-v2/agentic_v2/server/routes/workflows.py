"""Workflow routes."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse

from ...contracts import StepResult, StepStatus, WorkflowResult
from ...integrations.otel import create_trace_adapter
from ...langchain import WorkflowRunner as LangChainRunner
from ...langchain import list_workflows as lc_list_workflows
from ...langchain import load_workflow_config
from ...utils.path_safety import is_within_base
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
    """Compatibility shim for tests importing this helper directly."""
    return is_within_base(path, base_dir)


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


def _as_dict(value: Any) -> dict[str, Any]:
    """Normalize an arbitrary value into a JSON-object payload."""
    if isinstance(value, dict):
        return value
    if value is None:
        return {}
    return {"value": value}


def _coerce_step_status(value: Any) -> StepStatus:
    """Map status-like values into StepStatus."""
    if isinstance(value, StepStatus):
        return value
    normalized = str(value or "").strip().lower()
    if normalized in {"success", "succeeded", "completed"}:
        return StepStatus.SUCCESS
    if normalized in {"skipped", "skip"}:
        return StepStatus.SKIPPED
    if normalized in {"pending", "queued"}:
        return StepStatus.PENDING
    if normalized in {"running", "in_progress"}:
        return StepStatus.RUNNING
    return StepStatus.FAILED


def _extract_tokens(metadata: Mapping[str, Any]) -> int | None:
    """Return total tokens from step metadata when available."""
    direct = metadata.get("tokens_used")
    if isinstance(direct, int):
        return direct
    input_tokens = metadata.get("input_tokens")
    output_tokens = metadata.get("output_tokens")
    if isinstance(input_tokens, int) or isinstance(output_tokens, int):
        return int(input_tokens or 0) + int(output_tokens or 0)
    return None


def _build_step_results(
    steps_map: Mapping[str, Any],
    *,
    token_counts: Mapping[str, Any] | None = None,
    models_used: Mapping[str, Any] | None = None,
) -> list[StepResult]:
    """Convert LangGraph step mappings to contract StepResult objects."""
    results: list[StepResult] = []
    token_counts = token_counts or {}
    models_used = models_used or {}

    for step_name, step_data in steps_map.items():
        if not isinstance(step_data, Mapping):
            continue

        metadata_raw = step_data.get("metadata")
        metadata: dict[str, Any] = (
            dict(metadata_raw) if isinstance(metadata_raw, Mapping) else {}
        )

        token_meta = token_counts.get(step_name)
        if isinstance(token_meta, Mapping):
            input_tokens = int(token_meta.get("input") or 0)
            output_tokens = int(token_meta.get("output") or 0)
            metadata.setdefault("input_tokens", input_tokens)
            metadata.setdefault("output_tokens", output_tokens)
            metadata.setdefault("tokens_used", input_tokens + output_tokens)

        model_used = models_used.get(step_name)
        if model_used is None:
            model_used = step_data.get("model_used")
        if not isinstance(model_used, str):
            model_used = None

        error_val = step_data.get("error")
        error_text = str(error_val) if error_val else None

        start_ts = step_data.get("start_time")
        start_time = (
            datetime.fromisoformat(start_ts)
            if isinstance(start_ts, str)
            else datetime.now(timezone.utc)
        )

        end_ts = step_data.get("end_time")
        end_time = (
            datetime.fromisoformat(end_ts)
            if isinstance(end_ts, str)
            else None
        )

        results.append(
            StepResult(
                step_name=str(step_name),
                status=_coerce_step_status(step_data.get("status")),
                agent_role=(
                    str(step_data.get("agent_role"))
                    if step_data.get("agent_role") is not None
                    else None
                ),
                tier=(
                    int(step_data["tier"])
                    if isinstance(step_data.get("tier"), int)
                    else None
                ),
                model_used=model_used,
                input_data=_as_dict(step_data.get("inputs")),
                output_data=_as_dict(step_data.get("outputs")),
                error=error_text,
                metadata=metadata,
                start_time=start_time,
                end_time=end_time,
            )
        )

    return results


def _normalize_workflow_result(
    result: Any,
    *,
    workflow_name: str,
    run_id: str,
) -> WorkflowResult:
    """Normalize either runner result shape into contracts.WorkflowResult."""
    if isinstance(result, WorkflowResult):
        return result

    steps_map = getattr(result, "steps", {})
    if not isinstance(steps_map, Mapping):
        steps_map = {}

    token_counts = getattr(result, "token_counts", {})
    if not isinstance(token_counts, Mapping):
        token_counts = {}
    models_used = getattr(result, "models_used", {})
    if not isinstance(models_used, Mapping):
        models_used = {}

    steps = _build_step_results(
        steps_map,
        token_counts=token_counts,
        models_used=models_used,
    )

    raw_errors = getattr(result, "errors", [])
    if isinstance(raw_errors, list):
        errors = [str(e) for e in raw_errors if e]
    elif raw_errors:
        errors = [str(raw_errors)]
    else:
        errors = []

    overall_source = getattr(result, "overall_status", None)
    if overall_source is not None:
        overall_status = _coerce_step_status(overall_source)
    else:
        status_text = str(getattr(result, "status", "")).lower()
        overall_status = (
            StepStatus.SUCCESS
            if status_text == "success" and not errors
            else StepStatus.FAILED
        )

    elapsed_seconds = getattr(result, "elapsed_seconds", 0.0)
    try:
        elapsed_seconds = float(elapsed_seconds)
    except Exception:
        elapsed_seconds = 0.0

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(seconds=max(elapsed_seconds, 0.0))

    final_output = _as_dict(
        getattr(result, "final_output", None) or getattr(result, "outputs", None)
    )
    metadata: dict[str, Any] = {}
    langgraph_run_id = getattr(result, "run_id", None)
    if isinstance(langgraph_run_id, str) and langgraph_run_id:
        metadata["langgraph_run_id"] = langgraph_run_id
    if errors:
        metadata["errors"] = errors

    return WorkflowResult(
        workflow_id=run_id,
        workflow_name=workflow_name,
        steps=steps,
        overall_status=overall_status,
        start_time=start_time,
        end_time=end_time,
        final_output=final_output,
        metadata=metadata,
    )


def _merge_stream_state(aggregated: dict[str, Any], node_update: Mapping[str, Any]) -> None:
    """Merge a streamed LangGraph update payload into an aggregate state."""
    for payload in node_update.values():
        if not isinstance(payload, Mapping):
            continue

        context = payload.get("context")
        if isinstance(context, Mapping):
            aggregated["context"].update(context)

        outputs = payload.get("outputs")
        if isinstance(outputs, Mapping):
            aggregated["outputs"].update(outputs)

        steps = payload.get("steps")
        if isinstance(steps, Mapping):
            for step_name, step_data in steps.items():
                if not isinstance(step_data, Mapping):
                    continue
                existing = aggregated["steps"].get(step_name)
                if isinstance(existing, dict):
                    merged = dict(existing)
                    merged.update(step_data)
                    aggregated["steps"][step_name] = merged
                else:
                    aggregated["steps"][step_name] = dict(step_data)

        errors = payload.get("errors")
        if isinstance(errors, list):
            for err in errors:
                if err:
                    aggregated["errors"].append(str(err))


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
    base_dir = run_logger.runs_dir
    candidate = (base_dir / filename).resolve()
    if not _is_within_base(candidate, base_dir):
        # Do not leak filesystem layout; treat as not found
        raise HTTPException(status_code=404, detail=f"Run not found: {filename}")
    if not Path(candidate).exists():
        raise HTTPException(status_code=404, detail=f"Run not found: {filename}")
    
    run_data = run_logger.load_run(candidate)

    # Best-effort retroactive model identification
    # If model_used is missing in the run log, try to infer it from current workflow config
    workflow_name = run_data.get("workflow_name")
    if workflow_name:
        try:
            config = load_workflow_config(workflow_name)
            steps_cfg = {s.name: s for s in config.steps}
            
            for step in run_data.get("steps", []):
                # Skip if we already have a model
                if step.get("model_used"):
                    continue
                
                # Skip tier 0 (no model)
                if step.get("tier") == 0:
                    continue

                s_name = step.get("step_name")
                if s_name in steps_cfg:
                    step_cfg = steps_cfg[s_name]
                    
                    # 1. Check specific model override
                    if step_cfg.model_override:
                        val = step_cfg.model_override
                        # Handle "env:VAR|fallback"
                        if val.startswith("env:"):
                            parts = val.split("|", 1)
                            if len(parts) > 1:
                                env_key = parts[0][4:]
                                val = os.environ.get(env_key, parts[1])
                            else:
                                env_key = val[4:]
                                val = os.environ.get(env_key, val)
                        
                        step["model_used"] = val
                        # Mark as inferred (optional, maybe distinct UI style?)
                        step["metadata"] = step.get("metadata", {})
                        step["metadata"]["model_inferred"] = True
        except Exception:
            # Workflow definition might have changed or been deleted; ignore errors
            pass

    return run_data


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
) -> WorkflowResult:
    """Stream LangGraph node events to WebSocket, then return final WorkflowResult."""
    import time

    started_at = datetime.now(timezone.utc)
    started_perf = time.perf_counter()
    step_start_times: dict[str, float] = {}
    last_status_by_step: dict[str, str] = {}
    aggregated_state: dict[str, Any] = {
        "context": {},
        "steps": {},
        "outputs": {},
        "errors": [],
    }

    try:
        async for node_update in lc_runner.astream(
            workflow_name,
            thread_id=run_id,
            **workflow_inputs,
        ):
            if not isinstance(node_update, Mapping):
                continue

            _merge_stream_state(aggregated_state, node_update)
            now = datetime.now(timezone.utc).isoformat()

            for step_state in node_update.values():
                if not isinstance(step_state, Mapping):
                    continue
                step_map = step_state.get("steps")
                if not isinstance(step_map, Mapping):
                    continue

                for step_name, step_data in step_map.items():
                    if not isinstance(step_data, Mapping):
                        continue

                    status = str(step_data.get("status", "running")).strip().lower()
                    previous_status = last_status_by_step.get(str(step_name))

                    if status in {"running", "pending"}:
                        if previous_status == "running":
                            continue
                        last_status_by_step[str(step_name)] = "running"
                        step_start_times.setdefault(str(step_name), time.time())
                        await websocket.manager.broadcast(
                            run_id,
                            {
                                "type": "step_start",
                                "run_id": run_id,
                                "step": str(step_name),
                                "timestamp": now,
                            },
                        )
                        continue

                    if status not in {"success", "failed", "skipped"}:
                        continue
                    if previous_status == status:
                        continue

                    last_status_by_step[str(step_name)] = status
                    duration_ms = int(
                        (
                            time.time()
                            - step_start_times.pop(str(step_name), time.time())
                        )
                        * 1000
                    )

                    metadata_raw = step_data.get("metadata")
                    metadata = metadata_raw if isinstance(metadata_raw, Mapping) else {}
                    model_used = metadata.get("model")
                    if not isinstance(model_used, str):
                        model_used = None
                    tokens_used = _extract_tokens(metadata)
                    error_val = step_data.get("error")

                    await websocket.manager.broadcast(
                        run_id,
                        {
                            "type": "step_end",
                            "run_id": run_id,
                            "step": str(step_name),
                            "status": status,
                            "duration_ms": duration_ms,
                            "model_used": model_used,
                            "tokens_used": tokens_used,
                            "tier": step_data.get("tier"),
                            "input": _as_dict(step_data.get("inputs")),
                            "output": _as_dict(step_data.get("outputs")),
                            # Backward-compatible alias for older UIs.
                            "outputs": _as_dict(step_data.get("outputs")),
                            "error": str(error_val) if error_val else None,
                            "timestamp": now,
                        },
                    )

        workflow_cfg = load_workflow_config(workflow_name)
        resolved_outputs = lc_runner._resolve_outputs(workflow_cfg, aggregated_state)
        if not isinstance(resolved_outputs, dict):
            resolved_outputs = {}
        if not resolved_outputs:
            resolved_outputs = _as_dict(aggregated_state.get("outputs"))

        token_counts, models_used = lc_runner._extract_metadata(aggregated_state)
        step_results = _build_step_results(
            aggregated_state.get("steps", {}),
            token_counts=token_counts,
            models_used=models_used,
        )
        errors = [
            str(err)
            for err in aggregated_state.get("errors", [])
            if err
        ]

        overall_status = StepStatus.SUCCESS
        if errors or any(step.status == StepStatus.FAILED for step in step_results):
            overall_status = StepStatus.FAILED

        ended_at = datetime.now(timezone.utc)
        metadata: dict[str, Any] = {}
        if errors:
            metadata["errors"] = errors
        metadata["elapsed_seconds"] = max(0.0, time.perf_counter() - started_perf)

        return WorkflowResult(
            workflow_id=run_id,
            workflow_name=workflow_name,
            steps=step_results,
            overall_status=overall_status,
            start_time=started_at,
            end_time=ended_at,
            final_output=resolved_outputs,
            metadata=metadata,
        )
    except Exception as stream_err:
        logger.warning("Streaming failed (%s); falling back to invoke", stream_err)
        fallback = await lc_runner.run(
            workflow_name,
            thread_id=run_id,
            **workflow_inputs,
        )
        return _normalize_workflow_result(
            fallback,
            workflow_name=workflow_name,
            run_id=run_id,
        )


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
        await websocket.manager.broadcast(
            run_id,
            {
                "type": "workflow_start",
                "run_id": run_id,
                "workflow_name": workflow_name,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )
        result = await _stream_and_run(workflow_name, run_id, workflow_inputs)

        status = result.overall_status.value
        workflow_errors = [
            step.error
            for step in result.steps
            if step.status == StepStatus.FAILED and step.error
        ]
        metadata_errors = result.metadata.get("errors")
        if isinstance(metadata_errors, list):
            workflow_errors.extend(str(err) for err in metadata_errors if err)

        await websocket.manager.broadcast(
            run_id,
            {
                "type": "workflow_end",
                "run_id": run_id,
                "status": status,
                "outputs": result.final_output,
                "elapsed_seconds": (
                    (result.total_duration_ms or 0.0) / 1000.0
                    if result.total_duration_ms is not None
                    else 0.0
                ),
                "errors": workflow_errors,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
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
        logger.error(
            "Error in background execution for run_id=%s: %s",
            run_id,
            e,
            exc_info=True,
        )
        await websocket.manager.broadcast(
            run_id,
            {"type": "error", "run_id": run_id, "error": str(e)},
        )


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
