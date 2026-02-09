"""LangChain Bootstrap Helper This file provides a standardized way to
initialize the Multi-Agent system for use with LangChain.

It leverages the configurations in multiagent-workflows/config and
REPO_MANIFEST.json.
"""

import json
from pathlib import Path
from typing import Any, Dict

from multiagent_workflows import ModelManager
from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.langchain.orchestrator import LangChainOrchestrator


def load_repo_manifest() -> Dict[str, Any]:
    """Loads the repository manifest for context."""
    manifest_path = Path(__file__).parent / "REPO_MANIFEST.json"
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def bootstrap_orchestrator(
    allow_remote: bool = True, prefer_local: bool = False, verbose: bool = True
) -> LangChainOrchestrator:
    """Initializes the LangChainOrchestrator with default repo
    configurations."""
    # 1. Initialize Model Manager
    model_manager = ModelManager(allow_remote=allow_remote, prefer_local=prefer_local)

    # 2. Setup Logging
    logger = VerboseLogger(name="LangChainBootstrap", verbose=verbose)

    # 3. Define Config Paths
    repo_root = Path(__file__).parent
    workflow_config = repo_root / "multiagent-workflows" / "config" / "workflows.yaml"
    agent_config = repo_root / "multiagent-workflows" / "config" / "agents.yaml"

    # 4. Initialize Orchestrator
    orchestrator = LangChainOrchestrator(
        model_manager=model_manager,
        logger=logger,
        config_path=str(workflow_config),
        agent_config_path=str(agent_config),
    )

    return orchestrator


async def run_example(workflow_name: "fullstack_generation", requirements: str):
    """Example of running a workflow via LangChain."""
    orchestrator = bootstrap_orchestrator()

    print(f"Executing LangChain-backed workflow: {workflow_name}")
    result = await orchestrator.execute_workflow(
        workflow_name=workflow_name, inputs={"requirements": requirements}
    )

    if result["success"]:
        print("\nWorkflow succeeded!")
        print(f"Duration: {result['duration_ms']:.2f}ms")
    else:
        print(f"\nWorkflow failed: {result.get('error')}")


if __name__ == "__main__":
    # Example usage
    test_reqs = "Build a simple markdown note-taking app with a Python FastAPI backend."
    # asyncio.run(run_example("fullstack_generation", test_reqs))
    print("Bootstrap script ready. Import 'bootstrap_orchestrator' to start.")
