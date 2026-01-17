import os
import sys

# Add the project root to the python path so we can import tools
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.prompt_db import PromptDatabase  # noqa: E402


def test_db():
    db = PromptDatabase()
    
    print(f"Prompts: {len(db.prompts)}")
    print(f"Evaluations: {len(db.evaluations)}")
    
    # Test getting a prompt
    if db.prompts:
        prompt = db.prompts[0]
        print(f"\nSample Prompt: {prompt['name']}")
        
        # Test getting evaluations for this prompt
        evals = db.get_evaluations_for_prompt(prompt['id'])
        print(f"Evaluations for this prompt: {len(evals)}")
        if evals:
            print(f"Sample Score: {evals[0]['total_score']}")
            
    # Test getting evaluations by model
    model_evals = db.get_evaluations_by_model("gpt-4o-mini")
    print(f"\nEvaluations by gpt-4o-mini: {len(model_evals)}")


if __name__ == "__main__":
    test_db()
