"""
Step-by-step workflow step tester for FullStackWorkflow.
Prints outputs after each step to find where outputs become empty or fail.
"""
import sys
import os
import asyncio
import json
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../multiagent-workflows/src')))
from multiagent_workflows.workflows.fullstack_workflow import FullStackWorkflow
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.logger import VerboseLogger

DATASET_PATH = os.path.join(os.path.dirname(__file__), '../multiagent-workflows/ui/data/swebench.json')

# Load a random problem_statement as requirements
def load_random_prompt():
    with open(DATASET_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    tasks = data.get('tasks', [])
    if not tasks:
        raise ValueError('No tasks found in dataset')
    sample = random.choice(tasks)
    return sample.get('problem_statement', '')

async def run_step_by_step():
    requirements = load_random_prompt()
    logger = VerboseLogger(workflow_id="step-by-step-test")
    model_manager = ModelManager()
    workflow = FullStackWorkflow(model_manager=model_manager, logger=logger)

    steps = workflow.define_steps()
    step_map = {step.name: step for step in steps}
    step_deps = workflow.step_dependencies

    artifacts = {"requirements": requirements}
    completed = set()

    print("\nInitial requirements:\n", requirements[:500], "...\n")

    while len(completed) < len(steps):
        ready_steps = [
            s_name for s_name in step_map
            if s_name not in completed and all(dep in completed for dep in step_deps.get(s_name, []))
        ]

        if not ready_steps:
            pending = set(step_map.keys()) - completed
            print(f"\n[ERROR] Deadlock detected. Cannot proceed.")
            print(f"  Completed steps: {completed}")
            print(f"  Pending steps: {pending}")
            for s_name in pending:
                missing_deps = set(step_deps.get(s_name, [])) - completed
                if missing_deps:
                    print(f"    - '{s_name}' is waiting for: {missing_deps}")
            break

        print(f"\n--- Running parallel batch: {ready_steps} ---")

        async def run_step(step_name):
            step = step_map[step_name]
            print(f"\n=== Starting step: {step.name} ===")
            step_inputs = {k: artifacts[k] for k in step.required_inputs if k in artifacts}

            missing_inputs = set(step.required_inputs) - set(step_inputs.keys())
            if missing_inputs:
                print(f"[SKIP] Step '{step.name}' missing inputs: {missing_inputs}.")
                return None

            agent = await workflow._create_agent(step)
            if not agent:
                print(f"[SKIP] No agent for step '{step.name}'.")
                return None

            result = await agent.execute(step_inputs, {"artifacts": artifacts})
            print(f"Output from {step.name}: {json.dumps(result.output, indent=2)[:800]}{'...' if len(json.dumps(result.output)) > 800 else ''}")
            if not result.output and not step.optional:
                raise RuntimeError(f"Step '{step.name}' produced empty output.")
            return result.output

        results = await asyncio.gather(*(run_step(s_name) for s_name in ready_steps), return_exceptions=True)

        for step_name, result in zip(ready_steps, results):
            if isinstance(result, Exception):
                print(f"\n[FATAL] Step '{step_name}' failed: {result}")
                return
            if result:
                artifacts.update(result)
            completed.add(step_name)

    print("\n=== Workflow finished ===")
    print("Final artifacts:", list(artifacts.keys()))

if __name__ == "__main__":
    asyncio.run(run_step_by_step())
