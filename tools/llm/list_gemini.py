import sys
from pathlib import Path

# Add repo root to path
repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(repo_root))

from tools.llm.llm_client import LLMClient

try:
    print("Checking for Gemini models...")
    models = LLMClient.list_gemini_models()
    if models:
        print(f"Found {len(models)} Gemini models:")
        for m in models:
            print(f"- {m}")
    else:
        print("No Gemini models found. Check GEMINI_API_KEY env var.")
except Exception as e:
    print(f"Error listing models: {e}")
