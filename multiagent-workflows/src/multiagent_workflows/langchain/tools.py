"""
LangChain Tool Bindings

Converts ToolRegistry functions to LangChain-compatible Tool objects.
Ensures proper schema generation and function-calling compatibility.
"""

from __future__ import annotations

import asyncio
import inspect
from typing import Any, Callable, Dict, List, Optional, Type

from multiagent_workflows.core.tool_registry import ToolRegistry, ToolDefinition, get_default_registry


def _get_type_string(annotation: Any) -> str:
    """Convert Python type annotation to JSON schema type string."""
    if annotation is inspect.Parameter.empty:
        return "string"
    
    origin = getattr(annotation, "__origin__", None)
    if origin is list or origin is List:
        return "array"
    if origin is dict or origin is Dict:
        return "object"
    
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
    }
    return type_map.get(annotation, "string")


def _generate_schema_from_function(func: Callable) -> Dict[str, Any]:
    """Generate JSON schema from function signature."""
    sig = inspect.signature(func)
    properties = {}
    required = []
    
    for name, param in sig.parameters.items():
        prop = {
            "type": _get_type_string(param.annotation),
            "description": f"Parameter: {name}",
        }
        properties[name] = prop
        
        if param.default is inspect.Parameter.empty:
            required.append(name)
    
    return {
        "type": "object",
        "properties": properties,
        "required": required,
    }


def tool_definition_to_langchain(tool_def: ToolDefinition) -> Any:
    """
    Convert a ToolDefinition to a LangChain Tool.
    
    Returns a LangChain Tool object if langchain is available,
    otherwise returns a compatible dict structure.
    """
    try:
        from langchain_core.tools import StructuredTool
        
        # Generate schema if not provided
        if not tool_def.parameters:
            schema = _generate_schema_from_function(tool_def.handler)
        else:
            schema = tool_def.parameters
        
        # Create a sync wrapper for async functions
        if tool_def.is_async:
            def sync_wrapper(**kwargs):
                return asyncio.get_event_loop().run_until_complete(
                    tool_def.handler(**kwargs)
                )
            func = sync_wrapper
        else:
            func = tool_def.handler
        
        return StructuredTool.from_function(
            func=func,
            name=tool_def.name,
            description=tool_def.description,
            args_schema=None,  # Will use function signature
        )
    
    except ImportError:
        # Fallback: return dict-based tool definition
        return {
            "name": tool_def.name,
            "description": tool_def.description,
            "parameters": tool_def.parameters or _generate_schema_from_function(tool_def.handler),
            "handler": tool_def.handler,
        }


def tool_registry_to_langchain(
    registry: Optional[ToolRegistry] = None,
    tool_names: Optional[List[str]] = None,
) -> List[Any]:
    """
    Convert all or selected tools from ToolRegistry to LangChain tools.
    
    Args:
        registry: ToolRegistry instance (uses default if None)
        tool_names: Optional list of specific tool names to convert
        
    Returns:
        List of LangChain Tool objects
    """
    if registry is None:
        registry = get_default_registry()
    
    tools = []
    for tool_info in registry.list_tools():
        name = tool_info["name"]
        if tool_names and name not in tool_names:
            continue
        
        tool_def = registry.get_tool(name)
        if tool_def:
            lc_tool = tool_definition_to_langchain(tool_def)
            tools.append(lc_tool)
    
    return tools


def create_langchain_tools(
    additional_tools: Optional[List[Callable]] = None,
    registry: Optional[ToolRegistry] = None,
) -> List[Any]:
    """
    Create a complete set of LangChain tools for agent use.
    
    Combines:
    - Built-in tools from ToolRegistry
    - Any additional tools passed in
    
    Args:
        additional_tools: Optional list of functions to wrap as tools
        registry: ToolRegistry instance (uses default if None)
        
    Returns:
        List of LangChain Tool objects
    """
    tools = tool_registry_to_langchain(registry)
    
    if additional_tools:
        try:
            from langchain_core.tools import tool as tool_decorator
            
            for func in additional_tools:
                if not hasattr(func, "__langchain_tool__"):
                    # Wrap with LangChain tool decorator
                    wrapped = tool_decorator(func)
                    tools.append(wrapped)
                else:
                    tools.append(func)
        except ImportError:
            # Fallback: create dict-based tools
            for func in additional_tools:
                tools.append({
                    "name": func.__name__,
                    "description": func.__doc__ or f"Tool: {func.__name__}",
                    "parameters": _generate_schema_from_function(func),
                    "handler": func,
                })
    
    return tools


# Pre-defined tool schemas for common agent operations
AGENT_TOOL_SCHEMAS = {
    "analyze_code": {
        "name": "analyze_code",
        "description": "Analyze source code for patterns, issues, or structure",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Source code to analyze"},
                "analysis_type": {
                    "type": "string",
                    "enum": ["structure", "security", "performance", "quality"],
                    "description": "Type of analysis to perform"
                },
            },
            "required": ["code", "analysis_type"],
        },
    },
    "generate_code": {
        "name": "generate_code",
        "description": "Generate code based on specifications",
        "parameters": {
            "type": "object",
            "properties": {
                "specification": {"type": "string", "description": "What to generate"},
                "language": {"type": "string", "description": "Programming language"},
                "framework": {"type": "string", "description": "Framework to use"},
            },
            "required": ["specification", "language"],
        },
    },
    "review_code": {
        "name": "review_code",
        "description": "Review code for issues and improvements",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Code to review"},
                "focus_areas": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Areas to focus review on"
                },
            },
            "required": ["code"],
        },
    },
    "run_tests": {
        "name": "run_tests",
        "description": "Execute tests and return results",
        "parameters": {
            "type": "object",
            "properties": {
                "test_path": {"type": "string", "description": "Path to tests"},
                "framework": {"type": "string", "description": "Test framework"},
            },
            "required": ["test_path"],
        },
    },
}
