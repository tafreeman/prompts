import asyncio
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager


async def test_cloud():
    print("Testing Cloud Model (GitHub Models)...")

    logger = VerboseLogger(workflow_id="test_cloud", config={"level": "DEBUG"})
    manager = ModelManager(logger=logger)

    model_id = "gh:openai/gpt-4o"

    # Check availability
    available = await manager.check_availability(model_id)
    print(f"Model {model_id} available: {available}")

    if available:
        print("Sending request to cloud model...")
        try:
            result = await manager.generate(
                model_id=model_id,
                prompt="What is the capital of France? Answer in one word.",
                system_prompt="You are a helpful assistant.",
            )
            print(f"Response: {result.text}")
            print("✅ Cloud model call successful.")
        except Exception as e:
            print(f"❌ Error calling cloud model: {e}")
            import traceback

            traceback.print_exc()
    else:
        print("❌ Cloud model not available. Check GITHUB_TOKEN.")


if __name__ == "__main__":
    asyncio.run(test_cloud())
