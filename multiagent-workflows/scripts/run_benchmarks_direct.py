import asyncio
import json
import logging
from pathlib import Path

from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.workflow_engine import WorkflowEngine

# Setup basic logging to console
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("benchmark_runner")


async def run_benchmarks():
    logger.info("Starting Direct Benchmark Execution")

    # 1. Load Dataset
    dataset_path = Path("ui/data/humaneval.json")
    if not dataset_path.exists():
        logger.error(f"Dataset not found: {dataset_path}")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    tasks = data.get("tasks", [])[:3]  # Run first 3 tasks
    logger.info(f"Loaded {len(tasks)} tasks from HumanEval")

    # 2. Setup Engine
    model_manager = ModelManager()
    engine = WorkflowEngine(model_manager=model_manager)

    results = []

    # 3. Execute Loop
    for i, task in enumerate(tasks):
        task_id = task.get("task_id")
        logger.info(f"--- Running Task {i+1}/{len(tasks)}: {task_id} ---")

        # Wrap prompt to ensure Analyst understands it's a coding task
        problem_statement = f"Implement the following Python function. The solution must match the signature and docstring provided:\n\n{task['prompt']}"

        inputs = {
            "problem_statement": problem_statement,
            "test_cases": task.get("test", ""),
        }

        try:
            # Execute "automated_debugging" workflow
            result = await engine.execute_workflow("automated_debugging", inputs)

            status = "SUCCESS" if result.success else "FAILED"
            logger.info(
                f"Task {task_id} finished: {status}. Log ID: {result.workflow_id}"
            )

            results.append(
                {
                    "task_id": task_id,
                    "workflow_id": result.workflow_id,
                    "status": status,
                    "error": result.error if not result.success else None,
                }
            )

        except Exception as e:
            logger.error(f"Error running task {task_id}: {e}")
            results.append({"task_id": task_id, "status": "CRASHED", "error": str(e)})

    # 4. Summary
    logger.info("\n=== Benchmark Summary ===")
    for r in results:
        logger.info(
            f"{r['task_id']}: {r['status']} (ID: {r.get('workflow_id', 'N/A')})"
        )


if __name__ == "__main__":
    # Ensure src is in path
    import sys

    sys.path.append(str(Path.cwd() / "src"))

    asyncio.run(run_benchmarks())
