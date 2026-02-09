import asyncio
import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.workflow_engine import WorkflowEngine


async def run_fullstack():
    # Setup logger
    logger = VerboseLogger(workflow_id="fullstack_pilot", config={"level": "INFO"})

    # Initialize components
    model_manager = ModelManager(logger=logger)

    # Check model availability
    print("Checking model availability...")
    await model_manager.check_availability("gh:openai/gpt-4o")

    engine = WorkflowEngine(model_manager=model_manager)

    requirements = """
    Create a Personal Finance Dashboard application.
    
    Core Features:
    1. Transaction Management: Add, edit, delete income and expense transactions.
    2. Dashboard: Visual overview of current balance, monthly spending, and category breakdown (Pie chart).
    3. Categories: Manage custom categories (e.g., Food, Rent, Salary).
    4. Budgeting: Set monthly budgets per category and alerting when close to limit.
    
    Technical Non-functional Requirements:
    - Modern, responsive UI with dark mode support.
    - Fast loading times.
    - Secure data storage (even if local for now).
    """

    inputs = {
        "requirements": requirements,
        "tech_stack": {
            "frontend": "React + Vite + TailwindCSS",
            "backend": "FastAPI + SQLite",
        },
    }

    print("\nRunning Fullstack Generation Workflow...")
    print(f"Requirements: {requirements.splitlines()[1]}")

    try:
        # Run workflow: fullstack_generation
        result = await engine.execute_workflow("fullstack_generation", inputs)

        # Save results
        output_dir = Path("evaluation/results/fullstack")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"app_{result.workflow_id}.json"

        model_manager.logger.save_logs(output_dir / f"logs_{result.workflow_id}.json")

        output_dict = {
            "workflow_id": result.workflow_id,
            "workflow_name": result.workflow_name,
            "success": result.success,
            "outputs": result.outputs,
            "step_results": {k: v.output for k, v in result.step_results.items()},
            "error": result.error,
            "duration_ms": result.duration_ms,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_dict, f, indent=2, default=str)

        print(f"\n✅ Workflow Complete! Results saved to {output_file}")

    except Exception as e:
        print(f"\n❌ Workflow Failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check availability only")
    args = parser.parse_args()

    if args.check:
        # Just check models
        async def check():
            logger = VerboseLogger(workflow_id="check", config={"level": "INFO"})
            manager = ModelManager(logger=logger)
            print("Checking updated model routing...")
            available = await manager.check_availability("gh:openai/gpt-4o")
            print(f"gh:openai/gpt-4o available: {available}")

            # Check env var directly
            import os

            token = os.environ.get("GITHUB_TOKEN")
            print(f"GITHUB_TOKEN present: {bool(token)}")

            print("Check complete.")

        asyncio.run(check())
    else:
        asyncio.run(run_fullstack())
