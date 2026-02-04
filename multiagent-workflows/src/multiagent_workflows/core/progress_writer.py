"""Live Workflow Progress Writer.

Writes workflow execution state to a JSON file that can be read by the
web-based dashboard for live visualization.
"""

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DASHBOARD_DATA_DIR = Path(__file__).parent.parent / "dashboard_data"


@dataclass
class StepProgress:
    """Progress information for a single workflow step."""

    step_id: str
    step_name: str
    agent_name: str
    model_id: str
    status: str = "pending"  # pending, running, complete, error
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_ms: Optional[float] = None
    input_preview: str = ""
    output_preview: str = ""
    full_output: str = ""
    error_message: Optional[str] = None
    tokens_used: int = 0
    cost_estimate: float = 0.0


@dataclass
class WorkflowRun:
    """A complete workflow execution run."""

    run_id: str
    workflow_name: str
    started_at: str
    status: str = "running"  # running, complete, error
    completed_at: Optional[str] = None
    total_duration_ms: Optional[float] = None
    steps: List[StepProgress] = field(default_factory=list)
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    current_step_index: int = 0


class DashboardProgressWriter:
    """Writes workflow progress to JSON files for dashboard consumption.

    Usage:
        writer = DashboardProgressWriter()
        run_id = writer.start_run("defect_resolution", inputs={...})
        writer.start_step(run_id, "intake", "IntakeAgent", "gpt-4o-mini")
        writer.complete_step(run_id, "intake", output="...", tokens=150)
        writer.complete_run(run_id, outputs={...})
    """

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or DASHBOARD_DATA_DIR
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.runs_file = self.data_dir / "runs.json"
        self.current_run_file = self.data_dir / "current_run.json"
        self._load_runs()

    def _load_runs(self):
        """Load existing runs from disk."""
        if self.runs_file.exists():
            try:
                with open(self.runs_file, "r") as f:
                    data = json.load(f)
                    self.runs: List[Dict] = data.get("runs", [])
            except Exception:
                self.runs = []
        else:
            self.runs = []

    def _save_runs(self):
        """Save runs index to disk."""
        with open(self.runs_file, "w") as f:
            json.dump(
                {"runs": self.runs, "updated_at": datetime.now().isoformat()},
                f,
                indent=2,
            )

    def _save_run_detail(self, run: WorkflowRun):
        """Save detailed run data to its own file."""
        run_file = self.data_dir / f"run_{run.run_id}.json"
        with open(run_file, "w") as f:
            json.dump(asdict(run), f, indent=2)

        # Also update current run file if this is the active run
        if run.status == "running":
            with open(self.current_run_file, "w") as f:
                json.dump(asdict(run), f, indent=2)

    def start_run(
        self,
        workflow_name: str,
        inputs: Dict[str, Any],
        steps_config: List[Dict[str, str]],
    ) -> str:
        """Start a new workflow run.

        Args:
            workflow_name: Name of the workflow
            inputs: Input parameters
            steps_config: List of step configurations with keys: step_id, step_name, agent_name, model_id

        Returns:
            run_id: Unique identifier for this run
        """
        run_id = f"{workflow_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        steps = [
            StepProgress(
                step_id=s["step_id"],
                step_name=s["step_name"],
                agent_name=s["agent_name"],
                model_id=s["model_id"],
            )
            for s in steps_config
        ]

        run = WorkflowRun(
            run_id=run_id,
            workflow_name=workflow_name,
            started_at=datetime.now().isoformat(),
            steps=steps,
            inputs=inputs,
        )

        # Add to runs index
        self.runs.insert(
            0,
            {
                "run_id": run_id,
                "workflow_name": workflow_name,
                "started_at": run.started_at,
                "status": "running",
            },
        )

        # Keep only last 50 runs
        self.runs = self.runs[:50]

        self._save_runs()
        self._save_run_detail(run)

        # Store in memory for quick access
        self._current_run = run

        return run_id

    def start_step(self, run_id: str, step_id: str, input_preview: str = ""):
        """Mark a step as started."""
        run = self._load_run_detail(run_id)
        if not run:
            return

        for i, step in enumerate(run.steps):
            if step.step_id == step_id:
                step.status = "running"
                step.started_at = datetime.now().isoformat()
                step.input_preview = input_preview[:500] if input_preview else ""
                run.current_step_index = i
                break

        self._save_run_detail(run)

    def complete_step(
        self,
        run_id: str,
        step_id: str,
        output: str = "",
        tokens: int = 0,
        cost: float = 0.0,
        error: Optional[str] = None,
    ):
        """Mark a step as complete."""
        run = self._load_run_detail(run_id)
        if not run:
            return

        for step in run.steps:
            if step.step_id == step_id:
                step.status = "error" if error else "complete"
                step.completed_at = datetime.now().isoformat()
                step.output_preview = output[:500] if output else ""
                step.full_output = output
                step.tokens_used = tokens
                step.cost_estimate = cost
                step.error_message = error

                if step.started_at:
                    start = datetime.fromisoformat(step.started_at)
                    end = datetime.fromisoformat(step.completed_at)
                    step.duration_ms = (end - start).total_seconds() * 1000
                break

        self._save_run_detail(run)

    def complete_run(
        self, run_id: str, outputs: Dict[str, Any], error: Optional[str] = None
    ):
        """Mark a run as complete."""
        run = self._load_run_detail(run_id)
        if not run:
            return

        run.status = "error" if error else "complete"
        run.completed_at = datetime.now().isoformat()
        run.outputs = outputs

        start = datetime.fromisoformat(run.started_at)
        end = datetime.fromisoformat(run.completed_at)
        run.total_duration_ms = (end - start).total_seconds() * 1000

        # Update runs index
        for r in self.runs:
            if r["run_id"] == run_id:
                r["status"] = run.status
                r["completed_at"] = run.completed_at
                break

        self._save_runs()
        self._save_run_detail(run)

    def _load_run_detail(self, run_id: str) -> Optional[WorkflowRun]:
        """Load detailed run data from file."""
        # Check in-memory cache first
        if hasattr(self, "_current_run") and self._current_run.run_id == run_id:
            return self._current_run

        run_file = self.data_dir / f"run_{run_id}.json"
        if not run_file.exists():
            return None

        try:
            with open(run_file, "r") as f:
                data = json.load(f)

            steps = [StepProgress(**s) for s in data.get("steps", [])]
            run = WorkflowRun(
                run_id=data["run_id"],
                workflow_name=data["workflow_name"],
                started_at=data["started_at"],
                status=data.get("status", "running"),
                completed_at=data.get("completed_at"),
                total_duration_ms=data.get("total_duration_ms"),
                steps=steps,
                inputs=data.get("inputs", {}),
                outputs=data.get("outputs", {}),
                current_step_index=data.get("current_step_index", 0),
            )
            return run
        except Exception:
            return None


# Singleton instance for easy access
_writer_instance: Optional[DashboardProgressWriter] = None


def get_progress_writer() -> DashboardProgressWriter:
    """Get the global progress writer instance."""
    global _writer_instance
    if _writer_instance is None:
        _writer_instance = DashboardProgressWriter()
    return _writer_instance
