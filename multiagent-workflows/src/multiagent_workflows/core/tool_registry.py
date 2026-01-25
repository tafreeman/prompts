"""
Tool Registry

Provides registration and invocation of tools for agents.
Tools can be:
- Python functions
- MCP servers
- External APIs
"""

from __future__ import annotations

import asyncio
import inspect
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union


@dataclass
class ToolDefinition:
    """Definition of a registered tool."""
    name: str
    description: str
    handler: Callable
    parameters: Dict[str, Any]
    is_async: bool = False


class ToolRegistry:
    """
    Registry for tools that agents can invoke.
    
    Example:
        registry = ToolRegistry()
        
        @registry.register("read_file", "Read contents of a file")
        async def read_file(path: str) -> str:
            with open(path) as f:
                return f.read()
        
        # In agent:
        content = await self.use_tool("read_file", {"path": "README.md"})
    """
    
    def __init__(self):
        """Initialize empty registry."""
        self._tools: Dict[str, ToolDefinition] = {}
    
    def register(
        self,
        name: str,
        description: str,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> Callable:
        """
        Decorator to register a tool.
        
        Args:
            name: Tool name
            description: Human-readable description
            parameters: Optional parameter schema
            
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            self._tools[name] = ToolDefinition(
                name=name,
                description=description,
                handler=func,
                parameters=parameters or {},
                is_async=asyncio.iscoroutinefunction(func),
            )
            return func
        return decorator
    
    def add_tool(
        self,
        name: str,
        handler: Callable,
        description: str = "",
        parameters: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Add a tool directly (not as decorator).
        
        Args:
            name: Tool name
            handler: Tool function
            description: Human-readable description
            parameters: Optional parameter schema
        """
        self._tools[name] = ToolDefinition(
            name=name,
            description=description,
            handler=handler,
            parameters=parameters or {},
            is_async=asyncio.iscoroutinefunction(handler),
        )
    
    async def invoke(
        self,
        name: str,
        params: Dict[str, Any],
    ) -> Any:
        """
        Invoke a registered tool.
        
        Args:
            name: Tool name
            params: Tool parameters
            
        Returns:
            Tool result
            
        Raises:
            KeyError: If tool not registered
        """
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not registered")
        
        tool = self._tools[name]
        
        if tool.is_async:
            return await tool.handler(**params)
        else:
            return await asyncio.to_thread(tool.handler, **params)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all registered tools."""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters,
            }
            for tool in self._tools.values()
        ]
    
    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get a tool definition by name."""
        return self._tools.get(name)
    
    def has_tool(self, name: str) -> bool:
        """Check if a tool is registered."""
        return name in self._tools


# Default registry with built-in tools
_default_registry = ToolRegistry()


def get_default_registry() -> ToolRegistry:
    """Get the default tool registry."""
    return _default_registry


# ============================================================================
# Built-in Tools
# ============================================================================

@_default_registry.register("file_read", "Read contents of a file")
async def file_read(path: str, encoding: str = "utf-8") -> str:
    """Read a file and return its contents."""
    from pathlib import Path
    return Path(path).read_text(encoding=encoding)


@_default_registry.register("file_write", "Write contents to a file")
async def file_write(path: str, content: str, encoding: str = "utf-8") -> bool:
    """Write content to a file."""
    from pathlib import Path
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding=encoding)
    return True


@_default_registry.register("file_list", "List files in a directory")
async def file_list(
    directory: str,
    pattern: str = "*",
    recursive: bool = False,
) -> List[str]:
    """List files matching a pattern in a directory."""
    from pathlib import Path
    p = Path(directory)
    if recursive:
        return [str(f) for f in p.rglob(pattern) if f.is_file()]
    return [str(f) for f in p.glob(pattern) if f.is_file()]


@_default_registry.register("run_command", "Execute a shell command")
async def run_command(
    command: str,
    cwd: Optional[str] = None,
    timeout: int = 60,
) -> Dict[str, Any]:
    """Run a shell command and return output."""
    import subprocess
    
    result = await asyncio.to_thread(
        subprocess.run,
        command,
        shell=True,
        capture_output=True,
        text=True,
        cwd=cwd,
        timeout=timeout,
    )
    
    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "success": result.returncode == 0,
    }


@_default_registry.register("json_parse", "Parse JSON string")
async def json_parse(text: str) -> Any:
    """Parse a JSON string."""
    import json
    return json.loads(text)


@_default_registry.register("json_stringify", "Convert object to JSON string")
async def json_stringify(obj: Any, indent: int = 2) -> str:
    """Convert an object to JSON string."""
    import json
    return json.dumps(obj, indent=indent, default=str)
