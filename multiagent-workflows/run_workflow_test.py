"""
Test script to run the full-stack workflow and display results.
"""
import sys
sys.path.insert(0, 'src')

import asyncio
import json
from multiagent_workflows.workflows.fullstack_workflow import FullStackWorkflow
from multiagent_workflows.core.model_manager import ModelManager
from unittest.mock import MagicMock

print("=== Running Full-Stack Workflow ===")
print()

# Create mock model manager
mm = MagicMock(spec=ModelManager)
mm.get_optimal_model = MagicMock(return_value='mock:test')

# Track calls to return step-appropriate outputs
call_count = [0]

STEP_OUTPUTS = {
    1: {"user_stories": [{"id": "US001", "title": "User Login"}], "data_entities": [{"name": "User"}]},
    2: {"architecture": {"pattern": "layered"}, "tech_stack": {"backend": "FastAPI", "db": "PostgreSQL"}},
    3: {"schema": "CREATE TABLE users...", "migrations": ["001_users.sql"]},
    4: {"api_spec": {"openapi": "3.0.0"}, "endpoints": [{"path": "/login", "method": "POST"}]},
    5: {"backend_code": "from fastapi import FastAPI\napp = FastAPI()", "backend_files": [{"path": "main.py"}]},
    6: {"frontend_code": "import React from 'react'", "frontend_files": [{"path": "Login.tsx"}]},
    7: {"review_results": {"security": "PASS"}, "issues": [{"severity": "low", "msg": "Add validation"}]},
    8: {"backend_code": "# Refined", "frontend_code": "// Refined"},
    9: {"tests": "def test_login(): pass", "test_files": [{"path": "test_main.py"}]},
    10: {"readme": "# Todo App", "api_docs": "## API Docs"},
}

async def mock_generate(*args, **kwargs):
    call_count[0] += 1
    step = min(call_count[0], 10)
    
    result = MagicMock()
    result.text = json.dumps(STEP_OUTPUTS.get(step, {"result": "ok"}))
    return result

mm.generate = mock_generate

async def main():
    workflow = FullStackWorkflow(model_manager=mm)
    result = await workflow.execute({"requirements": "Build a simple todo app with user authentication"})
    return result

result = asyncio.run(main())

print("Workflow Result:")
print(f"  Success: {result.get('success', 'N/A')}")
print(f"  Steps completed: {len(result.get('step_results', {}))}")
print()

# Show artifacts
artifacts = result.get('artifacts', {})
print("Generated Artifacts:")
for key in sorted(artifacts.keys()):
    value = artifacts[key]
    if isinstance(value, str):
        preview = value[:60].replace('\n', ' ')
        if len(value) > 60:
            preview += "..."
    elif isinstance(value, dict):
        preview = str(list(value.keys()))
    elif isinstance(value, list):
        preview = f"[{len(value)} items]"
    else:
        preview = str(value)[:60]
    print(f"  {key}: {preview}")

print()
print("=== Workflow Complete ===")
