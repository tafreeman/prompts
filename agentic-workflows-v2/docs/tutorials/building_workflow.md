## Building a Workflow

This tutorial demonstrates a simple workflow definition and execution.

1. Write a YAML workflow in `workflows/` (example):

```yaml
name: sample_pipeline
steps:
  - id: analyze
    agent: Analyst
    input: {text: "analyze this"}
  - id: summarize
    agent: Writer
    input: {previous: "${steps.analyze.output}"}
```

2. Load with the orchestrator and run:

```python
from agentic_v2 import Orchestrator
orch = Orchestrator()
res = await orch.run_workflow("workflows/sample_pipeline.yaml")
```

3. Inspect logs in `logs/` for step-level outputs.
