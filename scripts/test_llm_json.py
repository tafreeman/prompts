#!/usr/bin/env python3
"""Quick debug script for LLMClient JSON responses."""

import sys
sys.path.insert(0, "tools")

from llm_client import LLMClient

prompt = """Return ONLY this JSON object (no markdown, no explanation):

{"run_id": "test123", "mode": "COLLECT", "needs_more": false, "next_requests": [], "observations": [{"tag": "Observed", "claim": "Test", "evidence": []}]}
"""

print("Testing LLMClient.generate_text...")
raw = LLMClient.generate_text("gh:openai/gpt-4o-mini", prompt, max_tokens=500)

print(f"RAW TYPE: {type(raw)}")
print(f"RAW LEN: {len(raw) if raw else 0}")
print(f"RAW CONTENT:\n{raw[:800] if raw else 'NONE'}")

# Try to parse
import json
try:
    from tools_ecosystem_evaluator import extract_first_json_object
    data = extract_first_json_object(raw)
    print(f"\nPARSED OK: {data}")
except Exception as e:
    print(f"\nPARSE ERROR: {e}")
