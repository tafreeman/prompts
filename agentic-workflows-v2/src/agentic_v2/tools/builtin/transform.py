"""Tier 0 transformation tools - No LLM required."""
from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

import jmespath
import yaml
from jinja2 import Template

from ..base import BaseTool, ToolResult


class JsonTransformTool(BaseTool):
    """Apply JMESPath query to JSON data."""
    
    @property
    def name(self) -> str:
        return "json_transform"
    
    @property
    def description(self) -> str:
        return "Apply a JMESPath query to transform JSON data"
    
    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "data": {
                "type": "object",
                "description": "JSON data to transform",
                "required": True,
            },
            "query": {
                "type": "string",
                "description": "JMESPath query expression",
                "required": True,
            },
        }
    
    @property
    def examples(self) -> list[str]:
        return [
            "json_transform(data={'a': [1, 2, 3]}, query='a[0]') → 1",
            "json_transform(data={'users': [{'name': 'Alice'}]}, query='users[0].name') → 'Alice'",
        ]
    
    async def execute(self, data: dict | list, query: str) -> ToolResult:
        """Execute JMESPath query."""
        try:
            result = jmespath.search(query, data)
            return ToolResult(
                success=True,
                data=result,
                metadata={"query": query}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"JMESPath query failed: {str(e)}"
            )


class TemplateRenderTool(BaseTool):
    """Render a Jinja2 template with variables."""
    
    @property
    def name(self) -> str:
        return "template_render"
    
    @property
    def description(self) -> str:
        return "Render a Jinja2 template string with provided variables"
    
    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "template": {
                "type": "string",
                "description": "Jinja2 template string",
                "required": True,
            },
            "variables": {
                "type": "object",
                "description": "Variables to render the template with",
                "required": True,
            },
        }
    
    @property
    def examples(self) -> list[str]:
        return [
            "template_render(template='Hello {{ name }}!', variables={'name': 'World'}) → 'Hello World!'",
        ]
    
    async def execute(self, template: str, variables: dict[str, Any]) -> ToolResult:
        """Execute template rendering."""
        try:
            tmpl = Template(template)
            rendered = tmpl.render(**variables)
            return ToolResult(
                success=True,
                data=rendered,
                metadata={"template_length": len(template), "output_length": len(rendered)}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Template rendering failed: {str(e)}"
            )


class ConfigMergeTool(BaseTool):
    """Deep merge multiple configuration dictionaries."""
    
    @property
    def name(self) -> str:
        return "config_merge"
    
    @property
    def description(self) -> str:
        return "Deep merge multiple configuration dictionaries (later configs override earlier ones)"
    
    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "configs": {
                "type": "array",
                "description": "List of config dictionaries to merge (in order)",
                "required": True,
            },
        }
    
    @property
    def examples(self) -> list[str]:
        return [
            "config_merge(configs=[{'a': 1}, {'b': 2}]) → {'a': 1, 'b': 2}",
            "config_merge(configs=[{'a': 1}, {'a': 2}]) → {'a': 2}",
        ]
    
    def _deep_merge(self, base: dict, override: dict) -> dict:
        """Deep merge two dictionaries."""
        result = deepcopy(base)
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = deepcopy(value)
        return result
    
    async def execute(self, configs: list[dict[str, Any]]) -> ToolResult:
        """Execute config merge."""
        try:
            if not configs:
                return ToolResult(
                    success=False,
                    error="No configs provided to merge"
                )
            
            result = {}
            for config in configs:
                result = self._deep_merge(result, config)
            
            return ToolResult(
                success=True,
                data=result,
                metadata={"num_configs": len(configs)}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Config merge failed: {str(e)}"
            )


class YamlLoadTool(BaseTool):
    """Load YAML string to dictionary."""
    
    @property
    def name(self) -> str:
        return "yaml_load"
    
    @property
    def description(self) -> str:
        return "Parse a YAML string into a Python dictionary"
    
    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "yaml_string": {
                "type": "string",
                "description": "YAML content to parse",
                "required": True,
            },
        }
    
    async def execute(self, yaml_string: str) -> ToolResult:
        """Execute YAML parsing."""
        try:
            data = yaml.safe_load(yaml_string)
            return ToolResult(
                success=True,
                data=data,
                metadata={"input_length": len(yaml_string)}
            )
        except yaml.YAMLError as e:
            return ToolResult(
                success=False,
                error=f"YAML parsing failed: {str(e)}"
            )


class YamlDumpTool(BaseTool):
    """Dump dictionary to YAML string."""
    
    @property
    def name(self) -> str:
        return "yaml_dump"
    
    @property
    def description(self) -> str:
        return "Convert a Python dictionary to a YAML string"
    
    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "data": {
                "type": "object",
                "description": "Data to convert to YAML",
                "required": True,
            },
            "indent": {
                "type": "number",
                "description": "Indentation level (default: 2)",
                "required": False,
                "default": 2,
            },
        }
    
    async def execute(self, data: Any, indent: int = 2) -> ToolResult:
        """Execute YAML dumping."""
        try:
            yaml_string = yaml.dump(data, indent=indent, default_flow_style=False)
            return ToolResult(
                success=True,
                data=yaml_string,
                metadata={"output_length": len(yaml_string)}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"YAML dumping failed: {str(e)}"
            )


class JsonLoadTool(BaseTool):
    """Parse JSON string to Python object."""
    
    @property
    def name(self) -> str:
        return "json_load"
    
    @property
    def description(self) -> str:
        return "Parse a JSON string into a Python object"
    
    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "json_string": {
                "type": "string",
                "description": "JSON content to parse",
                "required": True,
            },
        }
    
    async def execute(self, json_string: str) -> ToolResult:
        """Execute JSON parsing."""
        try:
            data = json.loads(json_string)
            return ToolResult(
                success=True,
                data=data,
                metadata={"input_length": len(json_string)}
            )
        except json.JSONDecodeError as e:
            return ToolResult(
                success=False,
                error=f"JSON parsing failed: {str(e)}"
            )


class JsonDumpTool(BaseTool):
    """Convert Python object to JSON string."""
    
    @property
    def name(self) -> str:
        return "json_dump"
    
    @property
    def description(self) -> str:
        return "Convert a Python object to a JSON string"
    
    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "data": {
                "type": "object",
                "description": "Data to convert to JSON",
                "required": True,
            },
            "indent": {
                "type": "number",
                "description": "Indentation level (default: 2, None for compact)",
                "required": False,
                "default": 2,
            },
        }
    
    async def execute(self, data: Any, indent: int | None = 2) -> ToolResult:
        """Execute JSON dumping."""
        try:
            json_string = json.dumps(data, indent=indent)
            return ToolResult(
                success=True,
                data=json_string,
                metadata={"output_length": len(json_string)}
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"JSON dumping failed: {str(e)}"
            )
