"""
Workflow Dashboard API Server

Provides REST endpoints for:
- Listing available workflows
- Starting workflow executions
- Getting run status

Run with: python dashboard_server.py
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from threading import Thread

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

# Paths
BASE_DIR = Path(__file__).parent.parent
DASHBOARD_DATA = BASE_DIR / "dashboard_data"
DASHBOARD_DATA.mkdir(exist_ok=True)

# Available workflows
WORKFLOWS = {
    "bug_fixing": {
        "name": "🔧 Defect Resolution",
        "description": "Analyze bugs, find root cause, and generate patches",
        "inputs": ["bug_report", "codebase_path"],
        "estimated_time": "3-5 min"
    },
    "fullstack_generation": {
        "name": "🏗️ Fullstack Generation", 
        "description": "Generate complete fullstack applications from specs",
        "inputs": ["specification", "tech_stack"],
        "estimated_time": "5-10 min"
    },
    "architecture_evolution": {
        "name": "🏛️ System Design",
        "description": "Evolve system architecture with best practices",
        "inputs": ["codebase_path", "goals"],
        "estimated_time": "4-8 min"
    },
    "code_grading": {
        "name": "📊 Code Grading",
        "description": "Evaluate code quality across multiple dimensions",
        "inputs": ["codebase_path"],
        "estimated_time": "2-4 min"
    }
}


@app.route('/')
def index():
    return send_from_directory('.', 'workflow_visualizer.html')


@app.route('/api/workflows')
def list_workflows():
    """List available workflows."""
    return jsonify({
        "workflows": [
            {"id": k, **v} for k, v in WORKFLOWS.items()
        ]
    })


@app.route('/api/health')
def handle_health():
    """Simple health check used by the UI to mark API online/offline."""
    return jsonify({"ok": True, "time": datetime.now().isoformat()})


@app.route('/api/models')
def handle_models():
    """Return a minimal model inventory so the UI has something to show.

    The real project uses a richer model probe; this endpoint provides a
    baseline for the static UI and example server.
    """
    models = [
        {"id": "", "label": "(Gold baseline — no model call)", "selectable": True}
    ]
    return jsonify({"models": models})


@app.route('/api/tasks')
def handle_tasks():
    """Return lightweight task lists for requested benchmark_id.

    The real server loads full datasets; for the dashboard example we return
    a small fallback set so the UI can render items.
    """
    benchmark = request.args.get('benchmark_id', 'custom')
    limit = int(request.args.get('limit', '50'))

    fallback = []
    for i in range(min(limit, 20)):
        fallback.append({
            "id": f"{benchmark}_task_{i+1}",
            "name": f"{benchmark} task {i+1}",
            "source": benchmark,
            "difficulty": ["Easy", "Medium", "Hard"][i % 3]
        })

    return jsonify({"tasks": fallback, "benchmark_id": benchmark})


@app.route('/api/runs')
def list_runs():
    """List all workflow runs."""
    runs_file = DASHBOARD_DATA / "runs.json"
    if runs_file.exists():
        with open(runs_file) as f:
            return jsonify(json.load(f))
    return jsonify({"runs": []})


@app.route('/api/runs/<run_id>')
def get_run(run_id):
    """Get details for a specific run."""
    run_file = DASHBOARD_DATA / f"run_{run_id}.json"
    if run_file.exists():
        with open(run_file) as f:
            return jsonify(json.load(f))
    return jsonify({"error": "Run not found"}), 404


@app.route('/api/start', methods=['POST'])
def start_workflow():
    """Start a new workflow execution."""
    data = request.json
    workflow_id = data.get('workflow_id')
    inputs = data.get('inputs', {})
    
    if workflow_id not in WORKFLOWS:
        return jsonify({"error": "Unknown workflow"}), 400
    
    # Generate run ID
    run_id = f"{workflow_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Create initial run entry
    run_data = {
        "run_id": run_id,
        "workflow_name": workflow_id,
        "started_at": datetime.now().isoformat(),
        "status": "starting",
        "inputs": inputs,
        "steps": [],
        "current_step_index": 0
    }
    
    # Save to file
    run_file = DASHBOARD_DATA / f"run_{run_id}.json"
    with open(run_file, 'w') as f:
        json.dump(run_data, f, indent=2)
    
    # Update runs index
    runs_file = DASHBOARD_DATA / "runs.json"
    if runs_file.exists():
        with open(runs_file) as f:
            runs_data = json.load(f)
    else:
        runs_data = {"runs": []}
    
    runs_data["runs"].insert(0, {
        "run_id": run_id,
        "workflow_name": workflow_id,
        "started_at": run_data["started_at"],
        "status": "starting"
    })
    runs_data["runs"] = runs_data["runs"][:50]  # Keep last 50
    
    with open(runs_file, 'w') as f:
        json.dump(runs_data, f, indent=2)
    
    # Start workflow in background thread
    def run_workflow():
        asyncio.run(execute_workflow_async(workflow_id, inputs, run_id))
    
    thread = Thread(target=run_workflow, daemon=True)
    thread.start()
    
    return jsonify({
        "success": True,
        "run_id": run_id,
        "message": f"Started {workflow_id}"
    })


async def execute_workflow_async(workflow_id: str, inputs: dict, run_id: str):
    """Execute a workflow and update progress."""
    try:
        from multiagent_workflows.core.workflow_engine import WorkflowEngine
        from multiagent_workflows.core.progress_writer import get_progress_writer
        from multiagent_workflows.core.model_manager import ModelManager
        
        # Initialize engine
        mm = ModelManager()
        engine = WorkflowEngine(mm)
        writer = get_progress_writer()
        
        # Define step configs based on workflow
        step_configs = get_step_configs(workflow_id)
        
        # Start the run
        writer.start_run(workflow_id, inputs, step_configs)
        
        # Update status to running
        update_run_status(run_id, "running")
        
        # Execute workflow
        result = await engine.execute_workflow(workflow_id, inputs)
        
        if not result.success:
            print(f"Workflow execution failed: {result.error}")
            with open("last_workflow_failure.txt", "w") as f:
                f.write(f"Workflow failed: {result.error}\n")
        
        # Complete run
        writer.complete_run(run_id, {"result": "success" if result.success else "failed"})
        update_run_status(run_id, "complete" if result.success else "error")
        
    except Exception as e:
        import traceback
        with open("last_error.txt", "w") as f:
            f.write(f"Error: {e}\n")
            traceback.print_exc(file=f)
        print(f"Workflow error: {e}")
        update_run_status(run_id, "error")


import yaml

def get_step_configs(workflow_id: str):
    """Get step configurations for a workflow."""
    # Try to load from workflows.yaml
    try:
        config_path = BASE_DIR / "config" / "workflows.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                wf_def = data.get("workflows", {}).get(workflow_id)
                if wf_def:
                    steps = []
                    for s in wf_def.get("steps", []):
                        steps.append({
                            "step_id": s.get("id"),
                            "step_name": s.get("name"),
                            "agent_name": s.get("agent"),
                            "model_id": s.get("model_preference") or "auto"
                        })
                    return steps
    except Exception as e:
        print(f"Error loading workflow config: {e}")

    # Fallback to hardcoded configs
    configs = {
        "bug_fixing": [
            {"step_id": "bug_intake", "step_name": "Bug Intake", "agent_name": "IntakeAgent", "model_id": "gpt-4o-mini"},
            {"step_id": "codebase_search", "step_name": "Codebase Search", "agent_name": "SearchAgent", "model_id": "gpt-4o-mini"},
            {"step_id": "root_cause_analysis", "step_name": "Root Cause Analysis", "agent_name": "AnalystAgent", "model_id": "deepseek-v3.2:cloud"},
            {"step_id": "fix_generation", "step_name": "Fix Generation", "agent_name": "PatchAgent", "model_id": "deepseek-v3.2:cloud"},
            {"step_id": "test_generation", "step_name": "Test Generation", "agent_name": "TestAgent", "model_id": "gpt-4o"},
            {"step_id": "fix_validation", "step_name": "Fix Validation", "agent_name": "ReviewerAgent", "model_id": "gpt-4o"},
        ],
        "fullstack_generation": [
            {"step_id": "vision_analysis", "step_name": "Analyze UI Mockups", "agent_name": "VisionAgent", "model_id": "gpt-4o"},
            {"step_id": "requirements_parsing", "step_name": "Parse Requirements", "agent_name": "SpecParser", "model_id": "gpt-4o-mini"},
            {"step_id": "architecture_design", "step_name": "System Design", "agent_name": "Architect", "model_id": "deepseek-v3.2:cloud"},
            {"step_id": "database_design", "step_name": "Database Design", "agent_name": "DBArchitect", "model_id": "deepseek-v3.2:cloud"},
            {"step_id": "api_design", "step_name": "API Design", "agent_name": "APIArchitect", "model_id": "gpt-4o-mini"},
            {"step_id": "frontend_generation", "step_name": "Frontend Generation", "agent_name": "FrontendDev", "model_id": "deepseek-v3.2:cloud"},
            {"step_id": "backend_generation", "step_name": "Backend Generation", "agent_name": "BackendDev", "model_id": "deepseek-v3.2:cloud"},
        ],
        "architecture_evolution": [
            {"step_id": "analyze", "step_name": "Codebase Analysis", "agent_name": "Analyzer", "model_id": "deepseek-v3.2:cloud"},
            {"step_id": "assess", "step_name": "Quality Assessment", "agent_name": "Assessor", "model_id": "gpt-4o"},
            {"step_id": "propose", "step_name": "Propose Changes", "agent_name": "Architect", "model_id": "deepseek-v3.2:cloud"},
            {"step_id": "validate", "step_name": "Validate Design", "agent_name": "Validator", "model_id": "gpt-4o"},
        ],
        "code_grading": [
            {"step_id": "static_analysis", "step_name": "Static Analysis", "agent_name": "StaticAnalyst", "model_id": "gpt-4o-mini"},
            {"step_id": "test_analysis", "step_name": "Test Analysis", "agent_name": "TestAnalyst", "model_id": "gpt-4o-mini"},
            {"step_id": "documentation_review", "step_name": "Doc Review", "agent_name": "DocReviewer", "model_id": "gpt-4o-mini"},
            {"step_id": "security_audit", "step_name": "Security Audit", "agent_name": "SecAuditor", "model_id": "gpt-4o"},
            {"step_id": "dependency_audit", "step_name": "Dependency Audit", "agent_name": "DepAuditor", "model_id": "gpt-4o"},
            {"step_id": "performance_review", "step_name": "Performance Review", "agent_name": "PerfReviewer", "model_id": "deepseek-v3.2:cloud"},
            {"step_id": "architecture_check", "step_name": "Architecture Check", "agent_name": "ArchReviewer", "model_id": "gpt-4o"},
            {"step_id": "maintainability_score", "step_name": "Maintainability", "agent_name": "MaintReviewer", "model_id": "o3-mini"},
            {"step_id": "best_practices", "step_name": "Best Practices", "agent_name": "BPReviewer", "model_id": "gpt-4o-mini"},
            {"step_id": "final_grading", "step_name": "Final Grading", "agent_name": "HeadJudge", "model_id": "gpt-4o"},
        ]
    }
    return configs.get(workflow_id, [])


def update_run_status(run_id: str, status: str):
    """Update run status in files."""
    run_file = DASHBOARD_DATA / f"run_{run_id}.json"
    if run_file.exists():
        with open(run_file) as f:
            data = json.load(f)
        data["status"] = status
        if status in ("complete", "error"):
            data["completed_at"] = datetime.now().isoformat()
        with open(run_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    # Update index too
    runs_file = DASHBOARD_DATA / "runs.json"
    if runs_file.exists():
        with open(runs_file) as f:
            runs_data = json.load(f)
        for run in runs_data.get("runs", []):
            if run["run_id"] == run_id:
                run["status"] = status
                break
        with open(runs_file, 'w') as f:
            json.dump(runs_data, f, indent=2)


if __name__ == '__main__':
    print("Starting Workflow Dashboard Server (fixed)...")
    print("   Open http://localhost:5050 in your browser")
    print("   Press Ctrl+C to stop")
    print()
    # Allow overriding the port via environment for parallel instances/tests
    port = int(os.environ.get("DASHBOARD_PORT", "5050"))
    app.run(host='0.0.0.0', port=port, debug=False)
