from click.testing import CliRunner
from tools.cli.main import cli
import json

def test_create_command():
    runner = CliRunner()
    variables = json.dumps({"project_name": "Test Project", "budget": "$10k"})
    
    print("Testing 'create' command...")
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
