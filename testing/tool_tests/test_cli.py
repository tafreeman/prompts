import sys
import os
import json
from pathlib import Path
from unittest.mock import patch
from click.testing import CliRunner

# Add project root to path for imports
ROOT_DIR = Path(__file__).parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from tools.cli.main import cli

def test_create_command():
    runner = CliRunner()
    variables = json.dumps({"project_name": "Test Project", "budget": "$10k"})
    
    print("Testing 'create' command...")
    
    # Enable remote providers for this test (the generator defaults to gpt-4o-mini)
    with patch.dict(os.environ, {"PROMPTEVAL_ALLOW_REMOTE": "1"}):
        result = runner.invoke(cli, [
            'create',
            '--category', 'business',
            '--use-case', 'Test Use Case',
            '--variables', variables,
            '--no-auto-refine'
        ])
    
    if result.exit_code != 0:
        print(f"FAILED: {result.output}")
        print(result.exception)
    
    assert result.exit_code == 0
    assert "Generating content for: Test Use Case" in result.output
    assert "Generation Complete!" in result.output
    print("✅ 'create' command passed!")

if __name__ == '__main__':
    test_create_command()
