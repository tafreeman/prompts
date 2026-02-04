# agentic-workflows-v2

Tier-based multi-model AI workflow orchestration.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from agentic_v2 import Orchestrator, Task

# Create orchestrator
orch = Orchestrator()

# Define a task
task = Task(
    name="analyze_code",
    tier=2,  # Medium complexity
    input={"code": "def hello(): pass"}
)

# Run
result = await orch.run(task)
```

## Features

- **Tier-based routing**: Route tasks to appropriate model sizes
- **Smart fallback**: Automatic retry with different models
- **Pydantic contracts**: Type-safe inputs/outputs
- **Async-first**: Built for concurrent execution
