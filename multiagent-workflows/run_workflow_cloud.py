#!/usr/bin/env python
"""Test script to run the full workflow with GitHub Models (cloud)."""

import asyncio
import os
import sys
import time

sys.path.insert(0, "src")

from multiagent_workflows.workflows.fullstack_workflow import FullStackWorkflow


class GenerateResult:
    """Wrapper for generate result with .text attribute."""

    def __init__(self, text: str):
        self.text = text


class GitHubModelManager:
    """GitHub Models API manager."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.base_url = "https://models.inference.ai.azure.com"
        self.token = os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable required")

    def get_optimal_model(self, preference: str = None, complexity: int = 5) -> str:
        """Return the configured model."""
        return f"gh:{self.model}"

    async def generate(self, prompt: str, **kwargs) -> str:
        """Generate response using GitHub Models."""
        import aiohttp

        # Truncate prompt for faster response
        if len(prompt) > 3000:
            prompt = prompt[:3000] + "\n\n[Truncated for brevity]"

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Always respond with valid JSON only. No markdown code fences, no explanation.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 1500,
        }

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=60),
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    text = data["choices"][0]["message"]["content"]
                    return GenerateResult(text)
                else:
                    error = await resp.text()
                    print(f"  ⚠ API error: {resp.status}")
                    return GenerateResult('{"error": "Generation failed"}')


async def main():
    print("=" * 60)
    print("  FULL-STACK WORKFLOW WITH GITHUB MODELS (gpt-4o-mini)")
    print("=" * 60)
    print()

    # Create workflow with GitHub Models
    try:
        model_manager = GitHubModelManager(model="gpt-4o-mini")
    except ValueError as e:
        print(f"❌ {e}")
        print("Set GITHUB_TOKEN in your environment.")
        return

    workflow = FullStackWorkflow(model_manager=model_manager)

    # Simple requirements for faster processing
    context = {"requirements": """
        Build a simple todo app:
        - User login with email/password
        - Create, edit, delete todos
        - Mark todos as complete
        Tech stack: FastAPI backend, React frontend, PostgreSQL database
        """}

    print("Requirements:", context["requirements"].strip())
    print()
    print("Starting workflow (10 steps)...")
    print("-" * 60)

    start_time = time.time()

    # Run workflow
    result = await workflow.execute(context)

    elapsed = time.time() - start_time

    print("-" * 60)
    print()
    print(f"✅ Workflow completed in {elapsed:.1f}s")
    print(f"   Steps executed: {len(result.get('artifacts', {}))}")
    print()

    # Show artifacts
    print("Generated Artifacts:")
    print("=" * 60)
    artifacts = result.get("artifacts", {})
    for key, value in artifacts.items():
        print(f"\n📦 {key}:")
        if isinstance(value, dict):
            for k, v in list(value.items())[:3]:
                preview = str(v)[:150] + "..." if len(str(v)) > 150 else str(v)
                print(f"    {k}: {preview}")
            if len(value) > 3:
                print(f"    ... and {len(value) - 3} more keys")
        elif isinstance(value, list):
            for item in value[:3]:
                preview = str(item)[:150] + "..." if len(str(item)) > 150 else str(item)
                print(f"    - {preview}")
            if len(value) > 3:
                print(f"    ... and {len(value) - 3} more items")
        else:
            preview = str(value)[:300] + "..." if len(str(value)) > 300 else str(value)
            print(f"    {preview}")

    print()
    print("=" * 60)
    print("  WORKFLOW COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
