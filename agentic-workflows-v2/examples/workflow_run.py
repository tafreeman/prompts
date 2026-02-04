"""Minimal workflow run example.

Run with: python examples/workflow_run.py
"""

import asyncio

from agentic_v2 import Orchestrator


async def main():
    orch = Orchestrator()
    # Assumes a workflow file exists at workflows/sample_pipeline.yaml
    try:
        res = await orch.run_workflow("workflows/sample_pipeline.yaml")
        print(res)
    except FileNotFoundError:
        print(
            "No workflow file found. Create workflows/sample_pipeline.yaml to try this example."
        )


if __name__ == "__main__":
    asyncio.run(main())
