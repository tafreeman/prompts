
import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

import sys
from pathlib import Path

# Add the project root to the path to allow importing the cli module
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Now we can import the cli from the correct path
from tools.cli.main import cli


@pytest.fixture
def mock_generator():
    """Fixture to mock the UniversalCodeGenerator."""
    with patch('tools.cli.main.UniversalCodeGenerator') as mock_gen_class:
        mock_instance = MagicMock()
        mock_result = MagicMock()
        mock_result.final = "Generated Content"
        mock_result.review = {'score': 95}
        mock_instance.generate.return_value = mock_result
        mock_gen_class.return_value = mock_instance
        yield mock_instance


def test_create_command_stdout(mock_generator):
    """Test the 'create' command writing to stdout."""
    runner = CliRunner()
    result = runner.invoke(cli, [
        'create',
        '--category', 'test-cat',
        '--use-case', 'test-uc',
        '--variables', '{"key": "value"}',
        '--no-auto-refine'
    ])
    assert result.exit_code == 0
    assert "Generating content for: test-uc" in result.output
    assert "Generation Complete!" in result.output
    assert "Review Score: 95" in result.output
    assert "--- Generated Content ---" in result.output
    assert "Generated Content" in result.output
    mock_generator.generate.assert_called_once_with(
        category='test-cat',
        use_case='test-uc',
        variables={'key': 'value'},
        auto_refine=False
    )


def test_create_command_file_output(mock_generator, tmp_path):
    """Test the 'create' command writing to a file."""
    runner = CliRunner()
    output_file = tmp_path / "output.txt"
    result = runner.invoke(cli, [
        'create',
        '--category', 'test-cat',
        '--use-case', 'test-uc',
        '--variables', '{"key": "value"}',
        '--output', str(output_file)
    ])
    assert result.exit_code == 0
    assert f"Saved to: {output_file}" in result.output
    assert output_file.read_text() == "Generated Content"


def test_create_command_invalid_json(mock_generator):
    """Test the 'create' command with invalid JSON."""
    runner = CliRunner()
    result = runner.invoke(cli, [
        'create',
        '--category', 'test-cat',
        '--use-case', 'test-uc',
        '--variables', '{"key": "value"'  # Invalid JSON
    ])
    assert result.exit_code == 0  # Current implementation exits gracefully
    assert "Error: Variables must be valid JSON." in result.output

@patch('tools.cli.main.interactive_wizard')
def test_interactive_command_stdout(mock_wizard, mock_generator):
    """Test the 'interactive' command writing to stdout."""
    mock_wizard.return_value = {
        'category': 'interactive-cat',
        'use_case': 'interactive-uc',
        'variables': {'k': 'v'},
        'auto_refine': True
    }
    runner = CliRunner()
    # Simulate user skipping the file save prompt
    result = runner.invoke(cli, ['interactive'], input='\n')
    
    assert result.exit_code == 0
    assert "Generating content for: interactive-uc" in result.output
    assert "--- Generated Content ---" in result.output
    assert "Generated Content" in result.output
    mock_generator.generate.assert_called_once_with(
        category='interactive-cat',
        use_case='interactive-uc',
        variables={'k': 'v'},
        auto_refine=True
    )

@patch('tools.cli.main.interactive_wizard')
def test_interactive_command_file_output(mock_wizard, mock_generator, tmp_path):
    """Test the 'interactive' command writing to a file."""
    mock_wizard.return_value = {
        'category': 'interactive-cat',
        'use_case': 'interactive-uc',
        'variables': {'k': 'v'},
        'auto_refine': False
    }
    runner = CliRunner()
    output_file = tmp_path / "interactive_output.txt"
    # Simulate user providing a filename at the prompt
    result = runner.invoke(cli, ['interactive'], input=f'{str(output_file)}\n')

    assert result.exit_code == 0
    assert f"Saved to: {output_file}" in result.output
    assert output_file.read_text() == "Generated Content"
