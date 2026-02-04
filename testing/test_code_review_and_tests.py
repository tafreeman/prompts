"""Minimal test for code review and test generation agents with raw backend
code."""

import asyncio
import os
import sys
import textwrap

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../multiagent-workflows/src")
    ),
)
from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.workflows.fullstack_workflow import FullStackWorkflow

RAW_CODE = textwrap.dedent("""
    from fastapi import FastAPI, HTTPException

    app = FastAPI()

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        if item_id < 0:
            raise HTTPException(status_code=400, detail="Invalid item_id")
        return {"item_id": item_id, "name": f"Item {item_id}"}
""").strip()


async def test_code_review_and_tests():
    logger = VerboseLogger(workflow_id="raw-code-test")
    model_manager = ModelManager()
    workflow = FullStackWorkflow(model_manager=model_manager, logger=logger)

    # Define the sequence of steps to test, respecting the new refinement loop
    steps_to_run = ["code_review", "code_refinement", "test_generation"]
    step_map = {step.name: step for step in workflow.define_steps()}

    # Initial artifacts for the test. Provide an empty frontend_code for compatibility.
    artifacts = {"backend_code": RAW_CODE, "frontend_code": ""}

    for step_name in steps_to_run:
        step = step_map.get(step_name)
        if not step:
            print(f"Step '{step_name}' not found in workflow definition.")
            continue

        print(f"\n=== Running step: {step.name} ===")
        agent = await workflow._create_agent(step)
        if not agent:
            print(f"Warning: No agent created for step {step.name}")
            continue

        # Gather inputs for this step from the artifacts
        step_inputs = {k: artifacts[k] for k in step.required_inputs if k in artifacts}

        missing_inputs = set(step.required_inputs) - set(step_inputs.keys())
        if missing_inputs:
            print(
                f"Error: Missing required inputs for step '{step.name}': {missing_inputs}"
            )
            break

        try:
            result = await agent.execute(step_inputs, {"artifacts": artifacts})
            print(f"Output: {result.output}\n")
            if result.output:
                artifacts.update(result.output)
        except Exception as e:
            print(f"Error during {step.name}: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(test_code_review_and_tests())
