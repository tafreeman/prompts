# Examples

Minimal runnable examples for `agentic_v2`.

## Files

| File | Description | API keys? |
|------|-------------|-----------|
| `simple_agent.py` | Tiny async agent usage example | Yes |
| `workflow_run.py` | Load a built-in workflow and execute a demo run | Yes |
| `yaml_workflow.py` | Load a YAML workflow definition, validate, and execute | No |
| `custom_tool.py` | Implement a custom tool, register it, and verify protocol conformance | No |

## Run

```bash
python examples/simple_agent.py
python examples/workflow_run.py
python examples/yaml_workflow.py
python examples/custom_tool.py
```

## Notes

- `workflow_run.py` creates a temporary file named `dummy_code.py` when running `code_review`. The file is cleaned up automatically at the end of the run.
- `yaml_workflow.py` and `custom_tool.py` are fully deterministic (tier-0) and require no API keys.
