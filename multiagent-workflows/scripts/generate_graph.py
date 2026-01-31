
import sys
import os
from pathlib import Path

# Add src to python path
src_path = Path(__file__).resolve().parent.parent / "src"
sys.path.append(str(src_path))

from multiagent_workflows.workflows.fullstack_workflow import FullStackWorkflow
from multiagent_workflows.core.model_manager import ModelManager
from multiagent_workflows.core.logger import VerboseLogger

def main():
    print("Initializing workflow...")
    # Using defaults for minimal setup
    model_manager = ModelManager()
    logger = VerboseLogger(workflow_id="graph_gen")
    
    workflow = FullStackWorkflow(
        model_manager=model_manager,
        logger=logger
    )
    
    output_file = "fullstack_workflow.mermaid"
    print(f"Generating LangGraph export to {output_file}...")
    
    graph = workflow.to_langgraph(output_path=output_file)
    
    if graph:
        print(f"✅ Successfully exported graph to {output_file}")
        print("Content preview:")
        with open(output_file, "r") as f:
            print(f.read()[:500] + "...")
    else:
        print("❌ Failed to export graph. Ensure 'langgraph' is installed.")

if __name__ == "__main__":
    main()
