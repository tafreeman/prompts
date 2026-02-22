# Examples

Minimal runnable examples for `agentic_v2`.

## Files

- `examples/simple_agent.py`: tiny async agent usage example
- `examples/workflow_run.py`: loads a built-in workflow and executes a demo run

## Run

```bash
python examples/simple_agent.py
python examples/workflow_run.py
```

## Notes

- `examples/workflow_run.py` creates a temporary file named dummy_code.py when running `code_review`.
- The file is cleaned up automatically at the end of the run.
