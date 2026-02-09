## Getting Started

This quick tutorial shows how to install and run a minimal orchestrator example.

1. Install in editable mode:

```bash
pip install -e .
```

2. Run the simple orchestrator (async runner or `python -m` example):

```python
from agentic_v2 import Orchestrator, Task
import asyncio

async def main():
    orch = Orchestrator()
    task = Task(name="hello", tier=0, input={"text":"hello"})
    res = await orch.run(task)
    print(res)

asyncio.run(main())
```

See `../examples/` for runnable examples.
