"""MCP (Model Context Protocol) Integration Module.

Provides MCP server clients for integrating external tools and services
with the multi-agent workflow system.

Available clients:
- FilesystemMCPClient: Local filesystem operations
- GitHubMCPClient: GitHub API operations
- StdioMCPClient: External MCP servers via stdio

Usage:
    from multiagent_workflows.mcp import MCPRegistry, setup_default_mcp_servers

    # Set up default servers
    registry = await setup_default_mcp_servers(
        allowed_directories=["/path/to/project"],
        github_token="ghp_..."
    )

    # Or manually register servers
    registry = MCPRegistry()
    registry.register_server(MCPServerConfig(
        name="filesystem",
        server_type="filesystem",
    ))
    await registry.connect("filesystem")
"""

from multiagent_workflows.mcp.base import (
    MCPClient,
    MCPResponse,
    MCPServerConfig,
    MCPToolSchema,
    StdioMCPClient,
)
from multiagent_workflows.mcp.filesystem import FilesystemMCPClient
from multiagent_workflows.mcp.github import GitHubMCPClient
from multiagent_workflows.mcp.memory import MemoryMCPClient
from multiagent_workflows.mcp.registry import (
    MCPRegistry,
    get_mcp_registry,
    register_mcp_client,
    setup_default_mcp_servers,
)

__all__ = [
    # Base classes
    "MCPClient",
    "MCPServerConfig",
    "MCPToolSchema",
    "MCPResponse",
    "StdioMCPClient",
    # Client implementations
    "FilesystemMCPClient",
    "GitHubMCPClient",
    "MemoryMCPClient",
    # Registry
    "MCPRegistry",
    "get_mcp_registry",
    "setup_default_mcp_servers",
    "register_mcp_client",
]
