#!/usr/bin/env python3
"""
Autonomous Evaluation Agent
===========================

A fully autonomous agent that executes the complete prompt library evaluation
pipeline without human intervention. It handles:

1. Generating eval files for all categories
2. Running evaluations with multiple models
3. Cross-validating results
4. Identifying failing prompts
5. Generating improvement recommendations
6. Creating comprehensive reports

Usage:
    # Full autonomous run
    python tools/evaluation_agent.py --full

    # Run specific phase
    python tools/evaluation_agent.py --phase 1

    # Dry run (show what would be done)
    python tools/evaluation_agent.py --full --dry-run

    # Resume from last checkpoint
    python tools/evaluation_agent.py --resume

Author: Prompts Library Team
Version: 1.0
"""

import argparse
import json
import subprocess
import sys
import time
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import logging


# =============================================================================
# CONFIGURATION
# =============================================================================
class AgentConfig:
    """Central configuration for the evaluation agent."""

    # Paths - go up 3 levels from tools/archive/ to repo root
    ROOT_DIR = Path(__file__).parent.parent.parent
    PROMPTS_DIR = ROOT_DIR / "prompts"
    EVALS_DIR = ROOT_DIR / "testing" / "evals"
    RESULTS_DIR = EVALS_DIR / "results"
    REPORTS_DIR = ROOT_DIR / "docs" / "reports"
    CHECKPOINT_FILE = ROOT_DIR / ".eval_checkpoint.json"

    # Categories in evaluation order
    CATEGORIES = [
        "analysis",
        "business",
        "m365",
        "developers",
        "system",
        "advanced",
        "creative",
        "governance",
    ]

    # Model configuration per category
    # Updated 2025-12-03 - Using MINI models for faster execution
    # All models validated via `gh models run`
    CATEGORY_CONFIG = {
        "analysis":    {"model": "openai/gpt-5-mini",   "runs": 3, "priority": 1},
        "business":    {"model": "xai/grok-3-mini",     "runs": 3, "priority": 1},
        "m365":        {"model": "openai/gpt-5-mini",   "runs": 3, "priority": 2},
        "developers":  {"model": "openai/o4-mini",      "runs": 3, "priority": 2},
        "system":      {"model": "openai/gpt-4.1-mini", "runs": 3, "priority": 3},
        "advanced":    {"model": "openai/o3-mini",      "runs": 3, "priority": 3},
        "creative":    {"model": "xai/grok-3-mini",     "runs": 3, "priority": 4},
        "governance":  {"model": "openai/gpt-5-mini",   "runs": 3, "priority": 4},
    }

    # Thresholds
    PASS_THRESHOLD = 7.0
    MIN_CRITERION_SCORE = 5.0
    CROSS_VALIDATION_THRESHOLD = 1.5  # Max allowed score difference between models
    TARGET_PASS_RATE = 0.90  # 90%

    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY_SECONDS = 10

    # Timeouts (increased for reliability)
    EVAL_TIMEOUT_SECONDS = 600  # 10 minutes per eval
    COMMAND_TIMEOUT_SECONDS = 900  # 15 minutes for batch commands

    # Rate limiting (avoid API throttling)
    DELAY_BETWEEN_EVALS_SECONDS = 1
    DELAY_BETWEEN_CATEGORIES_SECONDS = 5

    # Parallel execution
    MAX_PARALLEL_EVALS = 3  # Run up to 3 evals concurrently


class TaskStatus(Enum):
    """Status of individual tasks."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class TaskResult:
    """Result of a single task execution."""
    task_name: str
    status: TaskStatus
    start_time: str
    end_time: Optional[str] = None
    duration_seconds: float = 0
    output: Optional[str] = None
    error: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with proper enum serialization."""
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass
class CategoryResult:
    """Evaluation results for a single category."""
    category: str
    prompts_evaluated: int = 0
    prompts_passed: int = 0
    prompts_failed: int = 0
    average_score: float = 0.0
    pass_rate: float = 0.0
    model_used: str = ""
    runs_completed: int = 0
    eval_file_path: str = ""
    results_file_path: str = ""
    failing_prompts: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class AgentState:
    """Persistent state for the evaluation agent."""
    started_at: str
    current_phase: int = 0
    current_category: str = ""
    completed_categories: List[str] = field(default_factory=list)
    category_results: Dict[str, CategoryResult] = field(default_factory=dict)
    task_history: List[TaskResult] = field(default_factory=list)
    total_prompts: int = 0
    total_passed: int = 0
    total_failed: int = 0
    overall_pass_rate: float = 0.0
    status: str = "running"
    last_error: Optional[str] = None


# =============================================================================
# LOGGING SETUP
# =============================================================================
def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure logging for the agent."""
    log_level = logging.DEBUG if verbose else logging.INFO

    # Create logger
    logger = logging.getLogger("EvalAgent")
    logger.setLevel(log_level)

    # Console handler with colors
    console = logging.StreamHandler()
    console.setLevel(log_level)

    # Format with timestamps
    formatter = logging.Formatter(
        '%(asctime)s │ %(levelname)-8s │ %(message)s',
        datefmt='%H:%M:%S'
    )
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler for full logs
    log_file = AgentConfig.ROOT_DIR / "logs" / f"eval_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s'
    ))
    logger.addHandler(file_handler)

    return logger


# =============================================================================
# CHECKPOINT MANAGEMENT
# =============================================================================
def save_checkpoint(state: AgentState):
    """Save agent state to checkpoint file for resume capability."""
    checkpoint_data = {
        "started_at": state.started_at,
        "current_phase": state.current_phase,
        "current_category": state.current_category,
        "completed_categories": state.completed_categories,
        "category_results": {k: asdict(v) for k, v in state.category_results.items()},
        "task_history": [task.to_dict() for task in state.task_history],
        "total_prompts": state.total_prompts,
        "total_passed": state.total_passed,
        "total_failed": state.total_failed,
        "overall_pass_rate": state.overall_pass_rate,
        "status": state.status,
        "last_error": state.last_error,
        "checkpoint_time": datetime.now().isoformat(),
    }

    AgentConfig.CHECKPOINT_FILE.write_text(
        json.dumps(checkpoint_data, indent=2, default=str),
        encoding='utf-8'
    )


def load_checkpoint() -> Optional[AgentState]:
    """Load agent state from checkpoint file."""
    if not AgentConfig.CHECKPOINT_FILE.exists():
        return None

    try:
        data = json.loads(AgentConfig.CHECKPOINT_FILE.read_text(encoding='utf-8'))

        state = AgentState(
            started_at=data["started_at"],
            current_phase=data["current_phase"],
            current_category=data["current_category"],
            completed_categories=data["completed_categories"],
            total_prompts=data["total_prompts"],
            total_passed=data["total_passed"],
            total_failed=data["total_failed"],
            overall_pass_rate=data["overall_pass_rate"],
            status=data["status"],
            last_error=data.get("last_error"),
        )

        # Reconstruct category results
        for cat, result_data in data.get("category_results", {}).items():
            state.category_results[cat] = CategoryResult(**result_data)

        # Reconstruct task history
        for task_data in data.get("task_history", []):
            task_data["status"] = TaskStatus(task_data["status"])
            state.task_history.append(TaskResult(**task_data))

        return state
    except Exception as e:
        print(f"Warning: Could not load checkpoint: {e}")
        return None


def clear_checkpoint():
    """Remove checkpoint file."""
    if AgentConfig.CHECKPOINT_FILE.exists():
        AgentConfig.CHECKPOINT_FILE.unlink()


# =============================================================================
# COMMAND EXECUTION
# =============================================================================
def run_command(
    cmd: List[str],
    logger: logging.Logger,
    timeout: int = 600,
    capture_output: bool = True
) -> Tuple[bool, str, str]:
    """
    Execute a shell command with retry logic.

    Returns: (success, stdout, stderr)
    """
    for attempt in range(AgentConfig.MAX_RETRIES):
        try:
            logger.debug(f"Running: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                timeout=timeout,
                encoding='utf-8',
                errors='replace',
                cwd=str(AgentConfig.ROOT_DIR)
            )

            if result.returncode == 0:
                return True, result.stdout or "", result.stderr or ""
            else:
                logger.warning(f"Command failed (attempt {attempt + 1}): {result.stderr[:200]}")
                if attempt < AgentConfig.MAX_RETRIES - 1:
                    time.sleep(AgentConfig.RETRY_DELAY_SECONDS)

        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout}s")
            if attempt < AgentConfig.MAX_RETRIES - 1:
                time.sleep(AgentConfig.RETRY_DELAY_SECONDS)

        except Exception as e:
            logger.error(f"Command error: {e}")
            if attempt < AgentConfig.MAX_RETRIES - 1:
                time.sleep(AgentConfig.RETRY_DELAY_SECONDS)

    return False, "", f"Failed after {AgentConfig.MAX_RETRIES} attempts"


def check_prerequisites(logger: logging.Logger) -> bool:
    """Verify all required tools are available."""
    logger.info("Checking prerequisites...")

    # Check Python
    success, stdout, _ = run_command(["python", "--version"], logger)
    if not success:
        logger.error("Python not found")
        return False
    logger.debug(f"Python: {stdout.strip()}")

    # Check gh CLI
    success, stdout, _ = run_command(["gh", "--version"], logger)
    if not success:
        logger.error("GitHub CLI (gh) not found. Install from: https://cli.github.com/")
        return False
    logger.debug(f"GitHub CLI: {stdout.strip().split(chr(10))[0]}")

    # Check gh models extension
    success, stdout, _ = run_command(["gh", "models", "--help"], logger)
    if not success:
        logger.error("gh-models extension not found. Install with: gh extension install github/gh-models")
        return False
    logger.debug("gh-models extension: installed")

    # Check required directories
    if not AgentConfig.PROMPTS_DIR.exists():
        logger.error(f"Prompts directory not found: {AgentConfig.PROMPTS_DIR}")
        return False

    # Check required scripts (now in tools/archive/)
    required_scripts = [
        AgentConfig.ROOT_DIR / "tools" / "archive" / "generate_eval_files.py",
        AgentConfig.ROOT_DIR / "tools" / "archive" / "run_gh_eval.py",
        AgentConfig.ROOT_DIR / "tools" / "archive" / "evaluate_library.py",
        AgentConfig.ROOT_DIR / "tools" / "archive" / "improve_prompts.py",
    ]

    for script in required_scripts:
        if not script.exists():
            logger.error(f"Required script not found: {script}")
            return False
        logger.debug(f"Found: {script.name}")

    logger.info("✅ All prerequisites satisfied")
    return True


# =============================================================================
# EVALUATION TASKS
# =============================================================================
def count_prompts_in_category(category: str) -> int:
    """Count the number of prompt files in a category."""
    category_dir = AgentConfig.PROMPTS_DIR / category
    if not category_dir.exists():
        return 0

    excluded = {'index.md', 'readme.md'}
    count = sum(
        1 for f in category_dir.glob("*.md")
        if f.name.lower() not in excluded
    )
    return count


def generate_eval_files(
    category: str,
    logger: logging.Logger,
    dry_run: bool = False
) -> TaskResult:
    """Generate .prompt.yml eval files for a category."""
    task = TaskResult(
        task_name=f"generate_eval_files:{category}",
        status=TaskStatus.RUNNING,
        start_time=datetime.now().isoformat()
    )

    logger.info(f"📝 Generating eval files for {category}...")

    if dry_run:
        task.status = TaskStatus.SKIPPED
        task.output = "Dry run - skipped"
        return task

    output_dir = AgentConfig.EVALS_DIR / category
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "python", str(AgentConfig.ROOT_DIR / "testing" / "evals" / "generate_eval_files.py"),
        str(AgentConfig.PROMPTS_DIR / category),
        "--output", str(output_dir)
    ]

    success, stdout, stderr = run_command(cmd, logger)

    task.end_time = datetime.now().isoformat()
    task.duration_seconds = (
        datetime.fromisoformat(task.end_time) -
        datetime.fromisoformat(task.start_time)
    ).total_seconds()

    if success:
        task.status = TaskStatus.COMPLETED
        task.output = stdout

        # Count generated files
        eval_files = list(output_dir.glob("*.prompt.yml"))
        task.metrics["files_generated"] = len(eval_files)
        logger.info(f"   ✅ Generated {len(eval_files)} eval files")
    else:
        task.status = TaskStatus.FAILED
        task.error = stderr
        logger.error(f"   ❌ Failed to generate eval files: {stderr[:200]}")

    return task


def run_evaluations(
    category: str,
    model: str,
    runs: int,
    logger: logging.Logger,
    dry_run: bool = False
) -> TaskResult:
    """Run gh models eval for a category."""
    task = TaskResult(
        task_name=f"run_evaluations:{category}:{model}",
        status=TaskStatus.RUNNING,
        start_time=datetime.now().isoformat()
    )

    logger.info(f"🔬 Running evaluations for {category} with {model} ({runs} runs)...")

    if dry_run:
        task.status = TaskStatus.SKIPPED
        task.output = "Dry run - skipped"
        return task

    eval_dir = AgentConfig.EVALS_DIR / category
    eval_files = list(eval_dir.glob("*.prompt.yml"))

    if not eval_files:
        task.status = TaskStatus.FAILED
        task.error = "No eval files found"
        return task

    results_dir = AgentConfig.RESULTS_DIR / model / category
    results_dir.mkdir(parents=True, exist_ok=True)

    all_results = []

    def run_single_eval(eval_file, run_num):
        """Run a single evaluation (for parallel execution)."""
        cmd = ["gh", "models", "eval", str(eval_file), "--json"]
        success, stdout, stderr = run_command(cmd, logger, timeout=AgentConfig.EVAL_TIMEOUT_SECONDS)

        if success and stdout:
            try:
                result = json.loads(stdout)
                result["run_number"] = run_num
                result["eval_file"] = eval_file.name
                return result
            except json.JSONDecodeError:
                logger.warning(f"   Could not parse JSON from {eval_file.name}")
        return None

    # Build list of all eval tasks
    eval_tasks = [
        (eval_file, run_num)
        for eval_file in eval_files
        for run_num in range(1, runs + 1)
    ]

    logger.info(f"   📊 Running {len(eval_tasks)} evaluations with {AgentConfig.MAX_PARALLEL_EVALS} parallel workers...")

    # Run evaluations in parallel
    with ThreadPoolExecutor(max_workers=AgentConfig.MAX_PARALLEL_EVALS) as executor:
        futures = {
            executor.submit(run_single_eval, ef, rn): (ef, rn)
            for ef, rn in eval_tasks
        }

        completed = 0
        for future in as_completed(futures):
            eval_file, run_num = futures[future]
            completed += 1

            try:
                result = future.result()
                if result:
                    all_results.append(result)
                logger.debug(f"   [{completed}/{len(eval_tasks)}] {eval_file.name} run {run_num}")
            except Exception as e:
                logger.warning(f"   Error in {eval_file.name} run {run_num}: {e}")

            # Small delay to avoid rate limiting
            time.sleep(AgentConfig.DELAY_BETWEEN_EVALS_SECONDS)

    # Save results
    results_file = results_dir / f"{category}_results.json"
    results_file.write_text(json.dumps(all_results, indent=2), encoding='utf-8')

    task.end_time = datetime.now().isoformat()
    task.duration_seconds = (
        datetime.fromisoformat(task.end_time) -
        datetime.fromisoformat(task.start_time)
    ).total_seconds()

    task.status = TaskStatus.COMPLETED
    task.metrics["total_runs"] = len(all_results)
    task.metrics["results_file"] = str(results_file)

    logger.info(f"   ✅ Completed {len(all_results)} evaluation runs")

    return task


def parse_evaluation_results(
    category: str,
    logger: logging.Logger
) -> CategoryResult:
    """Parse evaluation results and calculate metrics."""
    result = CategoryResult(category=category)

    # Find results files
    for model_dir in AgentConfig.RESULTS_DIR.iterdir():
        if not model_dir.is_dir():
            continue

        results_file = model_dir / category / f"{category}_results.json"
        if results_file.exists():
            result.results_file_path = str(results_file)
            result.model_used = model_dir.name

            try:
                data = json.loads(results_file.read_text(encoding='utf-8'))

                # Extract scores from each test result
                prompt_scores = {}

                for run_result in data:
                    for test_result in run_result.get("testResults", []):
                        prompt_title = test_result.get("testCase", {}).get("promptTitle", "unknown")
                        response = test_result.get("modelResponse", "")

                        # Parse the grader's JSON response
                        try:
                            import re
                            json_match = re.search(r'\{.*\}', response, re.DOTALL)
                            if json_match:
                                parsed = json.loads(json_match.group())
                                score = parsed.get("overall_score", 0)
                                passed = parsed.get("pass", False)

                                if prompt_title not in prompt_scores:
                                    prompt_scores[prompt_title] = {
                                        "scores": [],
                                        "passed": [],
                                        "improvements": parsed.get("improvements", [])
                                    }

                                prompt_scores[prompt_title]["scores"].append(score)
                                prompt_scores[prompt_title]["passed"].append(passed)
                        except:
                            pass

                # Calculate final scores
                for title, data in prompt_scores.items():
                    if data["scores"]:
                        avg_score = sum(data["scores"]) / len(data["scores"])
                        passed = avg_score >= AgentConfig.PASS_THRESHOLD

                        result.prompts_evaluated += 1
                        if passed:
                            result.prompts_passed += 1
                        else:
                            result.prompts_failed += 1
                            result.failing_prompts.append({
                                "title": title,
                                "score": round(avg_score, 2),
                                "improvements": data["improvements"][:3]
                            })

                if result.prompts_evaluated > 0:
                    result.pass_rate = result.prompts_passed / result.prompts_evaluated
                    # Calculate average score across all prompts
                    all_scores = [
                        sum(d["scores"]) / len(d["scores"])
                        for d in prompt_scores.values() if d["scores"]
                    ]
                    if all_scores:
                        result.average_score = sum(all_scores) / len(all_scores)

            except Exception as e:
                logger.error(f"Error parsing results for {category}: {e}")

    return result


def generate_improvement_plan(
    failing_prompts: List[Dict[str, Any]],
    logger: logging.Logger,
    dry_run: bool = False
) -> TaskResult:
    """Generate improvement recommendations for failing prompts."""
    task = TaskResult(
        task_name="generate_improvement_plan",
        status=TaskStatus.RUNNING,
        start_time=datetime.now().isoformat()
    )

    logger.info(f"📋 Generating improvement plan for {len(failing_prompts)} failing prompts...")

    if dry_run:
        task.status = TaskStatus.SKIPPED
        return task

    cmd = [
        "python", str(AgentConfig.ROOT_DIR / "tools" / "improve_prompts.py"),
        "--all",
        "--output", str(AgentConfig.REPORTS_DIR / "IMPROVEMENT_PLAN.md")
    ]

    success, stdout, stderr = run_command(cmd, logger, timeout=300)

    task.end_time = datetime.now().isoformat()
    task.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
    task.output = stdout
    task.error = stderr if not success else None

    return task


def generate_final_report(
    state: AgentState,
    logger: logging.Logger,
    dry_run: bool = False
) -> TaskResult:
    """Generate the final comprehensive evaluation report."""
    task = TaskResult(
        task_name="generate_final_report",
        status=TaskStatus.RUNNING,
        start_time=datetime.now().isoformat()
    )

    logger.info("📊 Generating final evaluation report...")

    if dry_run:
        task.status = TaskStatus.SKIPPED
        return task

    # Run evaluate_library.py
    report_path = AgentConfig.REPORTS_DIR / "EVALUATION_REPORT.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "python", str(AgentConfig.ROOT_DIR / "tools" / "evaluate_library.py"),
        "--all",
        "--output", str(report_path)
    ]

    success, stdout, stderr = run_command(cmd, logger, timeout=600)

    # Also generate agent summary report
    summary_path = AgentConfig.REPORTS_DIR / "AGENT_EXECUTION_SUMMARY.md"
    generate_agent_summary(state, summary_path)

    task.end_time = datetime.now().isoformat()
    task.status = TaskStatus.COMPLETED if success else TaskStatus.FAILED
    task.metrics["report_path"] = str(report_path)
    task.metrics["summary_path"] = str(summary_path)

    return task


def generate_agent_summary(state: AgentState, output_path: Path):
    """Generate a summary of the agent's execution."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "# 🤖 Evaluation Agent Execution Summary",
        "",
        f"**Execution Started**: {state.started_at}",
        f"**Execution Completed**: {now}",
        f"**Status**: {state.status}",
        "",
        "---",
        "",
        "## 📊 Overall Results",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total Prompts Evaluated | {state.total_prompts} |",
        f"| Prompts Passed | {state.total_passed} |",
        f"| Prompts Failed | {state.total_failed} |",
        f"| Overall Pass Rate | {state.overall_pass_rate:.1%} |",
        f"| Target Pass Rate | {AgentConfig.TARGET_PASS_RATE:.1%} |",
        f"| Target Met | {'✅ Yes' if state.overall_pass_rate >= AgentConfig.TARGET_PASS_RATE else '❌ No'} |",
        "",
        "---",
        "",
        "## 📁 Category Results",
        "",
        "| Category | Evaluated | Passed | Failed | Pass Rate | Avg Score |",
        "|----------|-----------|--------|--------|-----------|-----------|",
    ]

    for cat in AgentConfig.CATEGORIES:
        if cat in state.category_results:
            r = state.category_results[cat]
            status = "✅" if r.pass_rate >= AgentConfig.TARGET_PASS_RATE else "⚠️"
            lines.append(
                f"| {status} {cat} | {r.prompts_evaluated} | {r.prompts_passed} | "
                f"{r.prompts_failed} | {r.pass_rate:.1%} | {r.average_score:.1f} |"
            )

    lines.extend([
        "",
        "---",
        "",
        "## ❌ Failing Prompts Requiring Attention",
        "",
    ])

    all_failing = []
    for cat, result in state.category_results.items():
        for fp in result.failing_prompts:
            fp["category"] = cat
            all_failing.append(fp)

    all_failing.sort(key=lambda x: x.get("score", 0))

    if all_failing:
        lines.extend([
            "| # | Category | Prompt | Score | Top Improvement |",
            "|---|----------|--------|-------|-----------------|",
        ])
        for i, fp in enumerate(all_failing[:20], 1):
            improvement = fp.get("improvements", ["General improvements"])[0][:40]
            lines.append(
                f"| {i} | {fp['category']} | {fp['title'][:30]} | "
                f"{fp.get('score', 'N/A')} | {improvement}... |"
            )
    else:
        lines.append("🎉 No failing prompts!")

    lines.extend([
        "",
        "---",
        "",
        "## 📋 Task Execution Log",
        "",
        "| Task | Status | Duration |",
        "|------|--------|----------|",
    ])

    for task in state.task_history:
        status_icon = {
            TaskStatus.COMPLETED: "✅",
            TaskStatus.FAILED: "❌",
            TaskStatus.SKIPPED: "⏭️",
            TaskStatus.PENDING: "⏳",
            TaskStatus.RUNNING: "🔄",
        }.get(task.status, "❓")

        lines.append(
            f"| {task.task_name} | {status_icon} {task.status.value} | "
            f"{task.duration_seconds:.1f}s |"
        )

    lines.extend([
        "",
        "---",
        "",
        f"*Generated by Evaluation Agent at {now}*",
    ])

    output_path.write_text("\n".join(lines), encoding='utf-8')


# =============================================================================
# MAIN AGENT LOOP
# =============================================================================
class EvaluationAgent:
    """
    Autonomous agent that runs the complete evaluation pipeline.
    """

    def __init__(
        self,
        logger: logging.Logger,
        dry_run: bool = False,
        resume: bool = False
    ):
        self.logger = logger
        self.dry_run = dry_run
        self.resume = resume
        self.state: Optional[AgentState] = None

    def initialize(self) -> bool:
        """Initialize the agent state."""
        if self.resume:
            self.state = load_checkpoint()
            if self.state:
                self.logger.info(f"📂 Resuming from checkpoint (phase {self.state.current_phase})")
                return True
            else:
                self.logger.warning("No checkpoint found, starting fresh")

        self.state = AgentState(
            started_at=datetime.now().isoformat()
        )
        return True

    def run_phase(self, phase: int) -> bool:
        """Run a specific evaluation phase."""
        # Get categories for this phase
        categories = [
            cat for cat, config in AgentConfig.CATEGORY_CONFIG.items()
            if config["priority"] == phase
        ]

        if not categories:
            self.logger.warning(f"No categories found for phase {phase}")
            return True

        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"📦 PHASE {phase}: {', '.join(categories)}")
        self.logger.info(f"{'='*60}\n")

        for category in categories:
            if category in self.state.completed_categories:
                self.logger.info(f"⏭️  Skipping {category} (already completed)")
                continue

            self.state.current_category = category
            save_checkpoint(self.state)

            success = self.evaluate_category(category)

            if success:
                self.state.completed_categories.append(category)
                save_checkpoint(self.state)
            else:
                self.logger.error(f"Failed to evaluate {category}")
                return False

            # Delay between categories
            if not self.dry_run:
                time.sleep(AgentConfig.DELAY_BETWEEN_CATEGORIES_SECONDS)

        return True

    def evaluate_category(self, category: str) -> bool:
        """Run full evaluation for a single category."""
        config = AgentConfig.CATEGORY_CONFIG[category]

        self.logger.info(f"\n{'─'*50}")
        self.logger.info(f"📂 Evaluating: {category}")
        self.logger.info(f"   Model: {config['model']}, Runs: {config['runs']}")
        self.logger.info(f"{'─'*50}\n")

        # Step 1: Generate eval files
        task = generate_eval_files(category, self.logger, self.dry_run)
        self.state.task_history.append(task)

        if task.status == TaskStatus.FAILED:
            return False

        # Step 2: Run evaluations
        task = run_evaluations(
            category,
            config["model"],
            config["runs"],
            self.logger,
            self.dry_run
        )
        self.state.task_history.append(task)

        if task.status == TaskStatus.FAILED:
            return False

        # Step 3: Parse results
        if not self.dry_run:
            result = parse_evaluation_results(category, self.logger)
            self.state.category_results[category] = result

            # Update totals
            self.state.total_prompts += result.prompts_evaluated
            self.state.total_passed += result.prompts_passed
            self.state.total_failed += result.prompts_failed

            if self.state.total_prompts > 0:
                self.state.overall_pass_rate = (
                    self.state.total_passed / self.state.total_prompts
                )

            # Log category results
            self.logger.info(f"\n   📈 Results for {category}:")
            self.logger.info(f"      Evaluated: {result.prompts_evaluated}")
            self.logger.info(f"      Passed: {result.prompts_passed}")
            self.logger.info(f"      Failed: {result.prompts_failed}")
            self.logger.info(f"      Pass Rate: {result.pass_rate:.1%}")
            self.logger.info(f"      Avg Score: {result.average_score:.1f}")

        return True

    def run_full_pipeline(self) -> bool:
        """Run the complete evaluation pipeline."""
        self.logger.info("\n" + "="*60)
        self.logger.info("🚀 STARTING AUTONOMOUS EVALUATION AGENT")
        self.logger.info("="*60 + "\n")

        # Check prerequisites
        if not check_prerequisites(self.logger):
            self.state.status = "failed"
            self.state.last_error = "Prerequisites not met"
            return False

        # Count total prompts
        total_expected = sum(
            count_prompts_in_category(cat)
            for cat in AgentConfig.CATEGORIES
        )
        self.logger.info(f"📚 Total prompts to evaluate: ~{total_expected}")

        # Run phases
        start_phase = self.state.current_phase or 1
        for phase in range(start_phase, 5):
            self.state.current_phase = phase
            save_checkpoint(self.state)

            success = self.run_phase(phase)
            if not success:
                self.state.status = "failed"
                self.state.last_error = f"Phase {phase} failed"
                save_checkpoint(self.state)
                return False

        # Generate improvement plan for failing prompts
        all_failing = []
        for result in self.state.category_results.values():
            all_failing.extend(result.failing_prompts)

        if all_failing:
            task = generate_improvement_plan(all_failing, self.logger, self.dry_run)
            self.state.task_history.append(task)

        # Generate final report
        task = generate_final_report(self.state, self.logger, self.dry_run)
        self.state.task_history.append(task)

        # Mark complete
        self.state.status = "completed"
        save_checkpoint(self.state)

        # Print final summary
        self.print_final_summary()

        # Clear checkpoint on successful completion
        if not self.dry_run:
            clear_checkpoint()

        return True

    def print_final_summary(self):
        """Print final execution summary."""
        self.logger.info("\n" + "="*60)
        self.logger.info("✅ EVALUATION AGENT COMPLETED")
        self.logger.info("="*60)
        self.logger.info(f"\n📊 Final Results:")
        self.logger.info(f"   Total Prompts: {self.state.total_prompts}")
        self.logger.info(f"   Passed: {self.state.total_passed}")
        self.logger.info(f"   Failed: {self.state.total_failed}")
        self.logger.info(f"   Pass Rate: {self.state.overall_pass_rate:.1%}")
        self.logger.info(f"   Target: {AgentConfig.TARGET_PASS_RATE:.1%}")

        target_met = self.state.overall_pass_rate >= AgentConfig.TARGET_PASS_RATE
        if target_met:
            self.logger.info(f"\n🎉 TARGET ACHIEVED!")
        else:
            self.logger.info(f"\n⚠️  Target not met - see improvement plan")

        self.logger.info(f"\n📁 Reports generated:")
        self.logger.info(f"   - docs/reports/EVALUATION_REPORT.md")
        self.logger.info(f"   - docs/reports/AGENT_EXECUTION_SUMMARY.md")
        if self.state.total_failed > 0:
            self.logger.info(f"   - docs/reports/IMPROVEMENT_PLAN.md")

        self.logger.info("\n" + "="*60 + "\n")


# =============================================================================
# CLI ENTRY POINT
# =============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Autonomous Evaluation Agent for Prompt Library",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full autonomous evaluation
  python tools/evaluation_agent.py --full

  # Run specific phase only
  python tools/evaluation_agent.py --phase 1

  # Dry run (show what would happen)
  python tools/evaluation_agent.py --full --dry-run

  # Resume from checkpoint
  python tools/evaluation_agent.py --resume

  # Verbose output
  python tools/evaluation_agent.py --full --verbose
        """
    )

    parser.add_argument(
        "--full",
        action="store_true",
        help="Run full evaluation pipeline"
    )
    parser.add_argument(
        "--phase",
        type=int,
        choices=[1, 2, 3, 4],
        help="Run specific phase (1-4)"
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from last checkpoint"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--clear-checkpoint",
        action="store_true",
        help="Clear existing checkpoint and start fresh"
    )

    args = parser.parse_args()

    # Setup logging
    logger = setup_logging(args.verbose)

    # Clear checkpoint if requested
    if args.clear_checkpoint:
        clear_checkpoint()
        logger.info("Checkpoint cleared")
        return 0

    # Validate arguments
    if not args.full and not args.phase and not args.resume:
        parser.print_help()
        return 1

    # Create and run agent
    agent = EvaluationAgent(
        logger=logger,
        dry_run=args.dry_run,
        resume=args.resume
    )

    if not agent.initialize():
        return 1

    if args.full or args.resume:
        success = agent.run_full_pipeline()
    elif args.phase:
        success = agent.run_phase(args.phase)
    else:
        success = False

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
