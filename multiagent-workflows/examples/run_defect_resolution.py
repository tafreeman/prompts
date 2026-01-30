
import asyncio
import os
import sys
from pathlib import Path
import json

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from multiagent_workflows.core.workflow_engine import WorkflowEngine
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.logger import VerboseLogger

async def run_defect_resolution():
    # Setup logger
    logger = VerboseLogger(workflow_id="defect_resolution_pilot", config={"level": "INFO"})
    
    # Initialize components
    model_manager = ModelManager(logger=logger)
    
    # Check model availability first
    print("Checking model availability...")
    await model_manager.check_availability("local:phi4")
    await model_manager.check_availability("gh:openai/gpt-4o")
    await model_manager.check_availability("gh:openai/gpt-4o-mini")
    
    engine = WorkflowEngine(model_manager=model_manager)
    
    # Define inputs
    bug_report = """
    Title: 500 Internal Server Error on Contact Form
    
    Description:
    When submitting the contact form, if I include an emoji (e.g. 🚀) in the message body, the server returns a 500 Internal Server Error.
    Standard text works fine.
    
    Steps to Reproduce:
    1. Send a POST request to /contact
    2. Body: {"message": "Hello 🚀"}
    3. Observer 500 Error
    """
    
    codebase_path = str(Path(__file__).parent / "buggy_app")
    
    inputs = {
        "bug_report": bug_report,
        "codebase_path": codebase_path
    }
    
    print(f"\nRunning Defect Resolution Workflow on {codebase_path}...")
    print(f"Bug Report: {bug_report.splitlines()[1]}")
    
    try:
        # Run workflow
        # Note: The ID in config/workflows.yaml is "bug_fixing"
        result = await engine.execute_workflow("bug_fixing", inputs)
        
        # Save results
        output_dir = Path("evaluation/results/defect_resolution")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"resolution_{result.workflow_id}.json"
        
        model_manager.logger.save_logs(output_dir / f"logs_{result.workflow_id}.json")
        
        # Need to handle WorkflowResult object
        output_dict = {
            "workflow_id": result.workflow_id,
            "workflow_name": result.workflow_name,
            "success": result.success,
            "outputs": result.outputs,
            "step_results": {k: v.output for k, v in result.step_results.items()},
            "error": result.error,
            "duration_ms": result.duration_ms
        }
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_dict, f, indent=2, default=str)
            
        print(f"\n✅ Workflow Complete! Results saved to {output_file}")
        
        # Print summary
        if result.success:
            outputs = result.outputs
            if "root_cause_analysis" in outputs:
                rca = outputs["root_cause_analysis"].get("root_cause", "N/A")
                print(f"\nRoot Cause Identified:\n{rca[:200]}...")
            
            if "fix_patch" in outputs:
                patch = outputs["fix_patch"]
                print(f"\nPatch Generated: {patch is not None}")
            
    except Exception as e:
        print(f"\n❌ Workflow Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_defect_resolution())
