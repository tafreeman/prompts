"""Lightweight LangChain-style orchestrator skeleton (dry-run).

This script reads `workflows/langchain_workflow.yaml`, `run-manifest.yaml`, and
an iteration plan, then executes a simulated run by invoking local stub
implementations for each role. It is intentionally dependency-free so it can be
used as a starting point for wiring real LangChain chains.

Usage:
  python workflows/langchain_orchestrator.py --manifest run-manifest.yaml --iteration-plan iteration-plan.yaml --dry-run

Outputs a small run summary JSON into `results/<run_id>/langchain_dryrun_<timestamp>.json`.
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
from datetime import datetime
from pathlib import Path

import yaml


def load_yaml(p: Path):
    with p.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def stub_criteria_validator(manifest: dict):
    # Return effective criteria (possibly adjusted) and evidence list
    base = manifest.get("grading_criteria") or {}
    effective = {k: v for k, v in base.items()}
    evidence = [f"Checked {k}" for k in effective.keys()]
    return {
        "criteria_valid": True,
        "effective_criteria": effective,
        "evidence": evidence,
    }


def stub_scoring(prompt_path: str, effective_criteria: dict):
    # Produce random-ish per-criterion scores (0-10) and weighted overall
    per = {
        k: round(max(0.0, min(10.0, random.gauss(7.0, 1.0))), 2)
        for k in effective_criteria.keys()
        or ["clarity", "effectiveness", "specificity"]
    }
    weights = list(effective_criteria.values()) if effective_criteria else [30, 30, 40]
    # Normalize weights if needed
    if sum(weights) == 0:
        weights = [1] * len(per)
    total_weight = sum(weights)
    weighted = 0.0
    for i, (k, score) in enumerate(per.items()):
        w = weights[i % len(weights)]
        weighted += score * (w / total_weight)
    return {"per_criterion": per, "weighted_score": round(weighted, 2)}


def stub_implementer(per_criterion: dict):
    # Return a trivial updated prompt candidate and top action
    top_action = "Add explicit output format and 1-2 examples."
    updated_prompt = "[UPDATED PROMPT - added output format]\n" + "\n".join(
        [f"# Criterion {k}: target {v}" for k, v in per_criterion.items()]
    )
    return {"updated_prompt": updated_prompt, "top_action": top_action}


def stub_validator(updated_prompt: str):
    # Simulate validation results
    passed = "output format" in updated_prompt.lower()
    observed = {
        "passed": passed,
        "issues": [] if passed else ["missing explicit JSON schema"],
    }
    return observed


def orchestrate(
    manifest: dict,
    iteration_plan: dict,
    workflow_map: dict,
    prompt_path: str,
    run_dir: Path,
    run_id: str,
    timestamp: str,
):
    # Orchestrator high-level flow (single iteration dry-run)
    out = {"run_id": run_id, "timestamp": timestamp, "prompt": prompt_path, "steps": []}

    # Criteria validation
    cv = stub_criteria_validator(manifest)
    out["steps"].append({"role": "criteria_validator", "result": cv})

    # Scoring
    scoring = stub_scoring(prompt_path, cv.get("effective_criteria", {}))
    out["steps"].append({"role": "scoring", "result": scoring})

    # Implementer
    impl = stub_implementer(scoring.get("per_criterion", {}))
    out["steps"].append({"role": "implementer", "result": impl})

    # Validator
    val = stub_validator(impl.get("updated_prompt", ""))
    out["steps"].append({"role": "validator", "result": val})

    # Recorder: summarize
    all_scores = list(scoring.get("per_criterion", {}).values())
    summary = {
        "weighted_score": scoring.get("weighted_score"),
        "per_criterion_mean": (
            round(statistics.mean(all_scores), 2) if all_scores else None
        ),
        "validator_passed": val.get("passed"),
    }
    out["summary"] = summary

    # write summary
    out_path = run_dir / f"langchain_dryrun_{timestamp}.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out_path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", default="run-manifest.yaml")
    p.add_argument("--iteration-plan", default="iteration-plan.yaml")
    p.add_argument("--workflow", default="workflows/langchain_workflow.yaml")
    p.add_argument(
        "--prompt-path",
        default="prompts/advanced/lats-self-refine-evaluator-agentic-workflow.md",
    )
    p.add_argument("--output-dir", default="results")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    manifest_path = Path(args.manifest)
    iteration_plan_path = Path(args.iteration_plan)
    workflow_path = Path(args.workflow)
    prompt_path = args.prompt_path

    manifest = load_yaml(manifest_path) if manifest_path.exists() else {}
    iteration_plan = (
        load_yaml(iteration_plan_path) if iteration_plan_path.exists() else {}
    )
    workflow_map = load_yaml(workflow_path) if workflow_path.exists() else {}

    run_id = (
        manifest.get("run_id")
        or f"dryrun_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}"
    )
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    run_dir = Path(args.output_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    out_path = orchestrate(
        manifest, iteration_plan, workflow_map, prompt_path, run_dir, run_id, timestamp
    )
    print("Dry-run complete. Summary written to", out_path)


if __name__ == "__main__":
    main()
