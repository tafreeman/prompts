"""
Pytest Configuration and Fixtures

Provides common fixtures for testing the multiagent-workflows package.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import asyncio
import pytest
from pathlib import Path
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_model_response() -> str:
    """Sample model response for testing."""
    return """Here is the generated code:

```python
def hello_world():
    \"\"\"Print hello world.\"\"\"
    print("Hello, World!")
```

This function prints a greeting message."""


@pytest.fixture
def mock_model_manager(mock_model_response):
    """Mock ModelManager for testing without real API calls."""
    from multiagent_workflows.core.model_manager import ModelManager, GenerationResult
    
    manager = MagicMock(spec=ModelManager)
    manager.generate = AsyncMock(return_value=GenerationResult(
        text=mock_model_response,
        model_id="mock:test",
        tokens_used=100,
        timing_ms=50.0,
        cost_estimate=0.0,
    ))
    manager.check_availability = AsyncMock(return_value=True)
    manager.get_optimal_model = MagicMock(return_value="mock:test")
    
    return manager


@pytest.fixture
def logger():
    """Create a VerboseLogger for testing."""
    from multiagent_workflows.core.logger import VerboseLogger
    
    return VerboseLogger(
        workflow_id="test-workflow",
        config={"level": "DEBUG"},
    )


@pytest.fixture
def tool_registry():
    """Create a ToolRegistry with test tools."""
    from multiagent_workflows.core.tool_registry import ToolRegistry
    
    registry = ToolRegistry()
    
    @registry.register("test_tool", "A test tool")
    async def test_tool(input: str) -> str:
        return f"processed: {input}"
    
    return registry


@pytest.fixture
def sample_requirements() -> str:
    """Sample requirements for testing."""
    return """
    Build a simple web API with the following features:
    - User authentication
    - CRUD operations for items
    - RESTful endpoints
    """


@pytest.fixture
def sample_architecture() -> Dict[str, Any]:
    """Sample architecture for testing."""
    return {
        "tech_stack": {
            "frontend": {"framework": "React", "justification": "Popular and well-supported"},
            "backend": {"framework": "FastAPI", "justification": "Fast and modern"},
            "database": {"type": "PostgreSQL", "justification": "Robust and scalable"},
        },
        "api_strategy": {
            "type": "REST",
            "versioning": "URL-based (/api/v1/...)",
        },
    }


@pytest.fixture
def temp_output_dir(tmp_path) -> Path:
    """Create a temporary directory for test outputs."""
    output_dir = tmp_path / "test_outputs"
    output_dir.mkdir()
    return output_dir
