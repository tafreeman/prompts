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


async def run_system_design():
    # Setup logger
    logger = VerboseLogger(workflow_id="system_design_pilot", config={"level": "INFO"})

    # Initialize components
    model_manager = ModelManager(logger=logger)

    # Check model availability
    print("Checking model availability...")
    await model_manager.check_availability("gh:openai/o1")
    await model_manager.check_availability("gh:deepseek/deepseek-r1")

    engine = WorkflowEngine(model_manager=model_manager)

    # Target: The multiagent-workflows source code itself
    target_codebase = str(Path(__file__).parent.parent / "src")

    inputs = {
        "codebase_path": target_codebase,
        "business_context": """
        We want to evolve this multi-agent workflow system to be more distributed and scalable.
        Currently it runs as a single process.
        We want to support running agents on different machines or containers.
        We also want to add a proper database for storing workflow state and history (replacing in-memory dicts).
        """,
    }

    print(f"\nRunning System Design Workflow on {target_codebase}...")

    try:
        # Run workflow: architecture_evolution
        result = await engine.execute_workflow("architecture_evolution", inputs)

        # Save results
        output_dir = Path("evaluation/results/system_design")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"design_{result.workflow_id}.json"

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
    asyncio.run(run_system_design())
