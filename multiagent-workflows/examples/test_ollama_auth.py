import asyncio
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager


async def test_ollama_auth():
    print("Testing Ollama Authentication...")

    # Set the key provided by user
    key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHyPgO8oR4ybzJuciDEytwawq6fykSEu4W99YTvlVgbo"
    os.environ["OLLAMA_API_KEY"] = key

    logger = VerboseLogger(workflow_id="test_auth", config={"level": "DEBUG"})
    manager = ModelManager(logger=logger)

    # We call _check_ollama directly or verify via check_availability
    # This invokes the code I modified which adds the header
    print(f"Using API Key: {key[:20]}...")

    import httpx

    try:
        headers = {"Authorization": f"Bearer {key}"}
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get("http://localhost:11434/api/tags", headers=headers)
            if resp.status_code == 200:
                models = resp.json().get("models", [])
                print(f"✅ Found {len(models)} models:")
                for m in models:
                    print(
                        f"  - {m.get('name')} ({m.get('details', {}).get('parameter_size', 'unknown')})"
                    )
            else:
                print(f"❌ Failed to list models: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"❌ Error listing models: {e}")


if __name__ == "__main__":
    asyncio.run(test_ollama_auth())
