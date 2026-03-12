"""Evaluation dataset listing and preview routes.

Provides:

* ``GET /api/eval/datasets`` -- list repository and local datasets for the
  evaluation picker UI.
* ``GET /api/workflows/{workflow_name}/preview-dataset-inputs`` -- preview
  dataset-to-input field mapping before execution.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from fastapi import APIRouter, HTTPException

from ...workflows.run_logger import RunLogger
from ..evaluation import (
    adapt_sample_to_workflow_inputs,
    list_eval_sets,
    list_local_datasets,
    list_repository_datasets,
    load_local_dataset_sample,
    load_repository_dataset_sample,
    match_workflow_dataset,
)
from ..models import ListEvaluationDatasetsResponse

# LangChain imports — optional.
try:
    from ...langchain import load_workflow_config

    _LANGCHAIN_AVAILABLE = True
except ImportError:
    _LANGCHAIN_AVAILABLE = False

logger = logging.getLogger(__name__)
router = APIRouter(tags=["evaluation"])
run_logger = RunLogger()


def _require_langchain() -> None:
    """Raise 501 if langchain extras are missing."""
    if not _LANGCHAIN_AVAILABLE:
        raise HTTPException(
            status_code=501,
            detail="LangChain extras not installed. Install with: pip install -e '.[langchain]'",
        )


@router.get("/eval/datasets", response_model=ListEvaluationDatasetsResponse)
async def list_evaluation_datasets(workflow: Optional[str] = None):
    """List repository and local dataset options for workflow evaluation."""
    if workflow:
        _require_langchain()
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
                sample, _ = load_repository_dataset_sample(
                    dataset["id"], sample_index=0
                )
            except Exception:
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
    _require_langchain()
    try:
        workflow_def = load_workflow_config(workflow_name)
    except Exception as exc:
        raise HTTPException(
            status_code=404, detail=f"Workflow not found: {exc}"
        ) from exc

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
