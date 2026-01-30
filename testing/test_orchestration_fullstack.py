"""
Orchestration test for FullStackWorkflow.
Verifies the workflow execution and LangGraph export capabilities.
"""

import sys
import os
import asyncio
import json
import random

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../multiagent-workflows/src')))

from multiagent_workflows.core.logger import VerboseLogger
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.workflows.fullstack_workflow import FullStackWorkflow


# Use swebench.json for more realistic, business-style requirements
DATASET_PATH = os.path.join(os.path.dirname(__file__), '../multiagent-workflows/ui/data/swebench.json')

DEFAULT_REQUIREMENTS = """
Create a Todo List application with the following features:
1. Add, edit, delete todos
2. Mark todos as complete
3. Filter by status (all, active, completed)
4. Persist data to local storage
"""

def load_random_prompt():
    if not os.path.exists(DATASET_PATH):
        print(f"Dataset not found at {DATASET_PATH}, using default requirements.")
        return DEFAULT_REQUIREMENTS
        
    try:
        with open(DATASET_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        tasks = data.get('tasks', [])
        if not tasks:
            return DEFAULT_REQUIREMENTS
        sample = random.choice(tasks)
        return sample.get('problem_statement', '')
    except Exception as e:
        print(f"Error loading dataset: {e}, using default requirements.")
        return DEFAULT_REQUIREMENTS

async def run_orchestration_test():
    print("=== Starting Orchestration Test ===")
    
    # 1. Setup
    requirements = load_random_prompt()
    print(f"\nRequirements length: {len(requirements)} chars")
    
    logger = VerboseLogger(workflow_id="orchestration-test")
    model_manager = ModelManager()
    workflow = FullStackWorkflow(model_manager=model_manager, logger=logger)
    
    # 2. Test LangGraph Export (New Feature)
    print("\n--- Testing LangGraph Export ---")
    try:
        graph = workflow.to_langgraph()
        if graph:
            print("✅ LangGraph export successful")
        else:
            print("⚠️ LangGraph export returned None (LangGraph might not be installed)")
    except Exception as e:
        print(f"❌ LangGraph export failed: {e}")

    # 3. Execute Workflow
    print("\n--- Executing Workflow ---")
    try:
        checkpoint_dir = os.path.join(os.path.dirname(__file__), "_recovery/orch_test_checkpoints")
        results = await workflow.execute(
            {"requirements": requirements}, 
            checkpoint_dir=checkpoint_dir
        )
        
        print("\n=== Orchestration Test Results ===")
        for k, v in results["artifacts"].items():
            print(f"{k}: {str(v)[:200]}{'...' if len(str(v)) > 200 else ''}")
        print("\n=== Step Results ===")
        for step, res in results["step_results"].items():
            print(f"{step}: {list(res.keys())}")
            
    except Exception as e:
        print(f"\n❌ Workflow execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_orchestration_test())
