"""
Workflow Dashboard API Server (Example)

Serves the static dashboard UI and a small REST API for:
- Listing workflows
- Starting a workflow "run"
- Reading run status/progress JSON files

Run with: `python3 dashboard_server.py`
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from threading import Thread
from typing import Any, Dict, List, Optional

import yaml
from flask import Flask, jsonify, request, send_from_directory


EXAMPLES_DIR = Path(__file__).resolve().parent
BASE_DIR = EXAMPLES_DIR.parent

# Ensure `multiagent_workflows` package is importable when running this file directly.
sys.path.insert(0, str(BASE_DIR / "src"))

from multiagent_workflows.core.progress_writer import DashboardProgressWriter


app = Flask(__name__)

# Dashboard data location (kept alongside the repo, not under src/)
DASHBOARD_DATA = BASE_DIR / "dashboard_data"
DASHBOARD_DATA.mkdir(parents=True, exist_ok=True)

# Shared writer instance that persists runs to `DASHBOARD_DATA`
PROGRESS_WRITER = DashboardProgressWriter(data_dir=DASHBOARD_DATA)


# Available workflows (for the UI selector)
WORKFLOWS = {
    "bug_fixing": {
        "name": "🔧 Defect Resolution",
        "description": "Analyze bugs, find root cause, and generate patches",
        "inputs": ["bug_report", "codebase_path"],
        "estimated_time": "3-5 min",
    },
    "fullstack_generation": {
        "name": "🏗️ Fullstack Generation",
        "description": "Generate complete fullstack applications from specs",
        "inputs": ["specification", "tech_stack"],
        "estimated_time": "5-10 min",
    },
    "architecture_evolution": {
        "name": "🏛️ System Design",
        "description": "Evolve system architecture with best practices",
        "inputs": ["codebase_path", "goals"],
        "estimated_time": "4-8 min",
    },
    "code_grading": {
        "name": "📊 Code Grading",
        "description": "Evaluate code quality across multiple dimensions",
        "inputs": ["codebase_path"],
        "estimated_time": "2-4 min",
    },
}


def _safe_read_json(path: Path, default: Any) -> Any:
    try:
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        return default
    return default


def _resolve_model_preference(preference: str) -> str:
    # Keep in sync with `multiagent_workflows.langchain.orchestrator.WorkflowOrchestrator._resolve_model`
    preference_map = {
        "vision": "gh:openai/gpt-4o",
        "reasoning": "gh:openai/gpt-4o",
        "reasoning_complex": "gh:openai/o3-mini",
        "code_gen": "gh:openai/gpt-4o",
        "code_gen_fast": "gh:openai/gpt-4o-mini",
        "code_gen_premium": "gh:openai/gpt-4o",
        "code_review": "gh:openai/o4-mini",
        "documentation": "gh:openai/gpt-4o-mini",
        "coordination": "gh:openai/gpt-4o-mini",
        "local_efficient": "local:phi4",
    }
    return preference_map.get(preference or "", "gh:openai/gpt-4o-mini")


def get_step_configs(workflow_id: str) -> List[Dict[str, str]]:
    """Load steps from `config/workflows.yaml` and format for the progress writer."""
    config_path = BASE_DIR / "config" / "workflows.yaml"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    except Exception:
        config = {}

    wf = (config.get("workflows") or {}).get(workflow_id) or {}
    raw_steps = wf.get("steps") or []

    steps: List[Dict[str, str]] = []
    for idx, s in enumerate(raw_steps[:30]):
        step_id = str(s.get("id") or f"step_{idx+1}")
        step_name = str(s.get("name") or step_id.replace("_", " ").title())
        agent_name = str(s.get("agent") or "agent")
        model_id = _resolve_model_preference(str(s.get("model_preference") or ""))
        steps.append(
            {
                "step_id": step_id,
                "step_name": step_name,
                "agent_name": agent_name,
                "model_id": model_id,
            }
        )

    if steps:
        return steps

    # Minimal fallback so the UI always renders something.
    return [
        {"step_id": "step_1", "step_name": "Initialize", "agent_name": "system", "model_id": "gh:openai/gpt-4o-mini"},
        {"step_id": "step_2", "step_name": "Process", "agent_name": "agent", "model_id": "gh:openai/gpt-4o-mini"},
        {"step_id": "step_3", "step_name": "Finalize", "agent_name": "system", "model_id": "gh:openai/gpt-4o-mini"},
    ]


@app.route("/")
def index():
    return send_from_directory(str(EXAMPLES_DIR), "workflow_visualizer.html")


@app.route("/dashboard_data/<path:filename>")
def dashboard_data_file(filename: str):
    # Convenience route for direct browser access to run JSON.
    return send_from_directory(str(DASHBOARD_DATA), filename)


@app.route("/api/health")
def api_health():
    return jsonify({"ok": True, "time": datetime.now().isoformat()})


@app.route("/api/workflows")
def api_list_workflows():
    return jsonify({"workflows": [{"id": k, **v} for k, v in WORKFLOWS.items()]})


@app.route("/api/runs")
def api_list_runs():
    return jsonify(_safe_read_json(DASHBOARD_DATA / "runs.json", {"runs": []}))


@app.route("/api/runs/<run_id>")
def api_get_run(run_id: str):
    data = _safe_read_json(DASHBOARD_DATA / f"run_{run_id}.json", None)
    if data is None:
        return jsonify({"error": "Run not found"}), 404
    return jsonify(data)


@app.route("/api/runs/compare")
def api_compare_runs():
    a = request.args.get("a")
    b = request.args.get("b")
    if not a or not b:
        return jsonify({"error": "Please provide run ids 'a' and 'b'"}), 400

    ra = _safe_read_json(DASHBOARD_DATA / f"run_{a}.json", None)
    rb = _safe_read_json(DASHBOARD_DATA / f"run_{b}.json", None)
    if ra is None or rb is None:
        return jsonify({"error": "One or both runs not found"}), 404

    def run_summary(r: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "run_id": r.get("run_id"),
            "workflow_name": r.get("workflow_name"),
            "status": r.get("status"),
            "started_at": r.get("started_at"),
            "completed_at": r.get("completed_at"),
            "total_steps": len(r.get("steps", []) or []),
        }

    steps_a = {s.get("step_id"): s for s in (ra.get("steps") or []) if s.get("step_id")}
    steps_b = {s.get("step_id"): s for s in (rb.get("steps") or []) if s.get("step_id")}
    all_step_ids = sorted(set(steps_a.keys()) | set(steps_b.keys()))

    step_diffs = []
    for sid in all_step_ids:
        a_step = steps_a.get(sid)
        b_step = steps_b.get(sid)
        step_diffs.append(
            {
                "step_id": sid,
                "a_status": (a_step or {}).get("status"),
                "b_status": (b_step or {}).get("status"),
                "a_output": (a_step or {}).get("output_preview") or (a_step or {}).get("output"),
                "b_output": (b_step or {}).get("output_preview") or (b_step or {}).get("output"),
            }
        )

    return jsonify({"a": run_summary(ra), "b": run_summary(rb), "step_diffs": step_diffs})


@app.route("/api/start", methods=["POST"])
def api_start_workflow():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON body"}), 400

    workflow_id = str(data.get("workflow_id") or "")
    if workflow_id not in WORKFLOWS:
        return jsonify({"error": "Unknown workflow"}), 400

    inputs = data.get("inputs") or {}
    if not isinstance(inputs, dict):
        return jsonify({"error": "inputs must be an object"}), 400

    steps_config = get_step_configs(workflow_id)

    run_id = PROGRESS_WRITER.start_run(
        workflow_name=workflow_id,
        inputs=inputs,
        steps_config=steps_config,
    )

    def run_workflow() -> None:
        asyncio.run(execute_workflow_async(workflow_id, inputs, run_id, steps_config))

    Thread(target=run_workflow, daemon=True).start()

    return jsonify({"success": True, "run_id": run_id, "message": f"Started {workflow_id}"})


async def execute_workflow_async(
    workflow_id: str,
    inputs: Dict[str, Any],
    run_id: str,
    steps_config: List[Dict[str, str]],
) -> None:
    """Best-effort execution: run the engine if available, otherwise simulate progress."""
    simulate_only = os.environ.get("DASHBOARD_SIMULATE_ONLY", "").strip().lower() in {"1", "true", "yes"}
    sim_delay = float(os.environ.get("DASHBOARD_SIM_DELAY_SECONDS", "1.0"))

    try:
        if not steps_config:
            steps_config = get_step_configs(workflow_id)

        # Mark first step as running so the UI shows activity.
        if steps_config:
            PROGRESS_WRITER.start_step(run_id, steps_config[0]["step_id"])

        if simulate_only:
            raise RuntimeError("Simulation mode enabled (DASHBOARD_SIMULATE_ONLY=1)")

        from multiagent_workflows.core.model_manager import ModelManager
        from multiagent_workflows.core.workflow_engine import WorkflowEngine

        engine = WorkflowEngine(ModelManager())
        result = await engine.execute_workflow(workflow_id, inputs)

        # Fill step outputs after execution (we don't currently have step-level callbacks).
        for step_cfg in steps_config:
            sid = step_cfg["step_id"]
            step_result = (result.step_results or {}).get(sid)
            if step_result is None:
                PROGRESS_WRITER.complete_step(run_id, sid, output="(no recorded output)")
                continue
            PROGRESS_WRITER.complete_step(
                run_id,
                sid,
                output=json.dumps(step_result.output, indent=2, ensure_ascii=False),
                tokens=int(getattr(step_result, "tokens_used", 0) or 0),
                cost=float(0.0),
                error=str(step_result.error) if not step_result.success else None,
            )

        PROGRESS_WRITER.complete_run(
            run_id,
            outputs={"success": bool(result.success), "outputs": result.outputs},
            error=str(result.error) if not result.success else None,
        )

    except Exception as e:
        # Fall back to lightweight simulation so the UI stays usable in minimal envs.
        for idx, step_cfg in enumerate(steps_config):
            sid = step_cfg["step_id"]
            PROGRESS_WRITER.start_step(run_id, sid, input_preview="")
            await asyncio.sleep(max(0.05, sim_delay))
            PROGRESS_WRITER.complete_step(
                run_id,
                sid,
                output=f"Simulated output for {sid} (step {idx+1}/{len(steps_config)})\n\nError/Reason: {e}",
                tokens=0,
                cost=0.0,
                error=None,
            )

        PROGRESS_WRITER.complete_run(
            run_id,
            outputs={"success": True, "result": "simulated"},
            error=None,
        )


def main() -> None:
    port = int(os.environ.get("DASHBOARD_PORT", "5050"))
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
