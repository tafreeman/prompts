"""Full-Stack Generation Example.

Demonstrates how to use the multi-agent workflow system to generate a
complete full-stack application from business requirements.
"""

import asyncio

# Add parent to path for imports
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from multiagent_workflows import ModelManager, VerboseLogger
from multiagent_workflows.workflows.fullstack_workflow import run_fullstack_workflow

# Example requirements for a simple task management app
EXAMPLE_REQUIREMENTS = """
# Task Management Application

## Overview
Build a web-based task management application for teams.

## Core Features

### User Management
- User registration with email verification
- Login/logout with JWT authentication
- User profile with avatar

### Task Management
- Create, read, update, delete tasks
- Assign tasks to team members
- Set due dates and priorities (low, medium, high, critical)
- Add labels/tags to tasks
- Task status: todo, in_progress, review, done

### Team Features
- Create teams and invite members
- Team dashboard with task overview
- Activity feed showing recent changes

### Notifications
- Email notifications for task assignments
- In-app notifications for updates

## Technical Requirements
- Mobile-responsive design
- REST API with OpenAPI documentation
- PostgreSQL database
- React frontend with TypeScript
- Python FastAPI backend
"""


async def main():
    """Run the full-stack generation workflow."""
    print("=" * 60)
    print("Multi-Agent Full-Stack Generation Demo")
    print("=" * 60)
    print()

    # Create model manager
    print("Initializing model manager...")
    model_manager = ModelManager(allow_remote=True)

    # List available models
    print("\nAvailable models:")
    models = await model_manager.list_models()
    for m in models[:5]:  # Show first 5
        print(f"  - {m.get('model', m.get('id', 'unknown'))}")
    print()

    # Create logger
    logger = VerboseLogger(
        workflow_id="demo-fullstack",
        config={"level": "INFO"},
    )

    # Run workflow
    print("Starting full-stack generation workflow...")
    print(f"Requirements: {len(EXAMPLE_REQUIREMENTS)} characters")
    print()

    try:
        result = await run_fullstack_workflow(
            requirements=EXAMPLE_REQUIREMENTS,
            model_manager=model_manager,
            logger=logger,
        )

        print("\n" + "=" * 60)
        print("Workflow Complete!")
        print("=" * 60)

        # Show results
        artifacts = result.get("artifacts", {})
        print(f"\nGenerated {len(artifacts)} artifacts:")
        for name, content in artifacts.items():
            size = len(str(content)) if content else 0
            print(f"  - {name}: {size} bytes")

        # Export logs
        logs_dir = Path("evaluation/results/logs")
        logs_dir.mkdir(parents=True, exist_ok=True)

        logger.export_to_json(logs_dir / "demo_fullstack.json")
        logger.export_to_markdown(logs_dir / "demo_fullstack.md")
        print(f"\nLogs exported to {logs_dir}")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback

        traceback.print_exc()


async def simple_demo():
    """Simpler demo that just tests the model manager."""
    print("Testing Model Manager...")

    manager = ModelManager()

    # Test availability
    models_to_check = [
        "local:phi4mini",
        "ollama:qwen2.5-coder:14b",
        "gh:gpt-4o-mini",
    ]

    print("\nChecking model availability:")
    for model_id in models_to_check:
        available = await manager.check_availability(model_id)
        status = "✅" if available else "❌"
        print(f"  {status} {model_id}")

    # Test generation with available model
    print("\nTesting generation...")
    optimal = manager.get_optimal_model("code_gen", 3, prefer_local=True)
    print(f"Selected model: {optimal}")

    try:
        result = await manager.generate(
            model_id=optimal,
            prompt="Write a Python function that adds two numbers. Keep it simple.",
            max_tokens=200,
        )
        print(f"\nGeneration result ({result.tokens_used} tokens):")
        print("-" * 40)
        print(result.text[:500])
        print("-" * 40)
    except Exception as e:
        print(f"Generation failed: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Full-stack generation example")
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Run simple model manager test only",
    )
    args = parser.parse_args()

    if args.simple:
        asyncio.run(simple_demo())
    else:
        asyncio.run(main())
