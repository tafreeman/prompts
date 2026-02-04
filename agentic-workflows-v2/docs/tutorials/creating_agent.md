## Creating an Agent

This guide shows a minimal agent implementation and how to register it with the framework.

1. Create a new agent class in `src/agentic_v2/agents/`:

```python
from agentic_v2.agents.base import BaseAgent

class EchoAgent(BaseAgent):
    async def run(self, input):
        return {"echo": input}
```

2. Register in your config or import path and use `Orchestrator` to call it.

3. Unit test example (pytest):

```python
def test_echo_agent():
    agent = EchoAgent()
    assert asyncio.run(agent.run({"x":1})) == {"echo":{"x":1}}
```
