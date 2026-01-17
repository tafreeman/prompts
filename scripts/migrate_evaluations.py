import json
import os
import sys

# Add the project root to the python path so we can import tools
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.prompt_db import PromptDatabase  # noqa: E402


def migrate():
    db = PromptDatabase()
    
    eval_log_path = os.path.join('results', 'eval-logs', 'evaluations.jsonl')
    if not os.path.exists(eval_log_path):
        print(f"No evaluation log found at {eval_log_path}")
        return

    print(f"Reading evaluations from {eval_log_path}...")
    
    with open(eval_log_path, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
                
            prompt_filename = entry.get('prompt_file')
            if not prompt_filename:
                continue
                
            # Try to find the prompt file to get content
            # Assuming prompts are in 'prompts/' or subdirectories. 
            # Since we don't know the exact path, we might need to search or just store the filename.
            # For this migration, let's try to find it in 'prompts/' recursively or just use the filename as the name.
            
            # Check if prompt already exists in DB
            existing_prompt = db.get_prompt_by_name(prompt_filename)
            prompt_id = None
            
            if existing_prompt:
                prompt_id = existing_prompt['id']
            else:
                # Create a new prompt entry. 
                # We don't have the content readily available here without searching, 
                # so we'll just store the filename as the name and empty content for now.
                # A separate step could populate the content.
                prompt_id = db.add_prompt(name=prompt_filename, content="", metadata={"migrated": True})
            
            # Map evaluation data
            # The existing log has 'criteria' which maps to our rubric dimensions.
            # We'll use the 'standard-v1' rubric ID for now, assuming these evaluations follow that roughly.
            
            eval_data = {
                "prompt_id": prompt_id,
                "prompt_version": "1.0",  # Default for migrated data
                "rubric_id": "standard-v1",
                "timestamp": entry.get('timestamp'),
                "model": entry.get('model'),
                "scores": entry.get('criteria', {}),
                "total_score": entry.get('score'),
                "feedback": entry.get('improvements', {}),
                "metadata": {
                    "original_key": entry.get('key'),
                    "origin": entry.get('origin'),
                    "run": entry.get('run'),
                    "duration": entry.get('duration'),
                    "error": entry.get('error')
                }
            }
            
            db.add_evaluation(eval_data)
            
    print("Migration complete.")
    print(f"Total prompts: {len(db.prompts)}")
    print(f"Total evaluations: {len(db.evaluations)}")


if __name__ == "__main__":
    migrate()
