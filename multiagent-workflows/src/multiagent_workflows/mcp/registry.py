"""MCP Server Registry.

Manages MCP server clients and integrates them with the ToolRegistry.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Type

from multiagent_workflows.core.tool_registry import ToolRegistry, get_default_registry
from multiagent_workflows.mcp.base import MCPClient, MCPResponse, MCPServerConfig

# Registry of available MCP client implementations
MCP_CLIENT_REGISTRY: Dict[str, Type[MCPClient]] = {}


def register_mcp_client(server_type: str):
    """Decorator to register an MCP client implementation."""

    def decorator(cls: Type[MCPClient]):
        MCP_CLIENT_REGISTRY[server_type] = cls
        return cls

    return decorator


# Register built-in clients
try:
    from multiagent_workflows.mcp.filesystem import FilesystemMCPClient

    MCP_CLIENT_REGISTRY["filesystem"] = FilesystemMCPClient
except ImportError:
    pass

try:
    from multiagent_workflows.mcp.github import GitHubMCPClient

    MCP_CLIENT_REGISTRY["github"] = GitHubMCPClient
except ImportError:
    pass

try:
    from multiagent_workflows.mcp.base import StdioMCPClient

    MCP_CLIENT_REGISTRY["stdio"] = StdioMCPClient
except ImportError:
    pass

try:
    from multiagent_workflows.mcp.memory import MemoryMCPClient

    MCP_CLIENT_REGISTRY["memory"] = MemoryMCPClient
except ImportError:
    pass


class MCPRegistry:
    """Registry for MCP server clients.

    Manages connections to MCP servers and integrates their tools with
    the ToolRegistry for use by agents.
    """

    def __init__(self, tool_registry: Optional[ToolRegistry] = None):
        self.tool_registry = tool_registry or get_default_registry()
        self._clients: Dict[str, MCPClient] = {}
        self._connected: Dict[str, bool] = {}

    def register_server(
        self,
        config: MCPServerConfig,
        client_class: Optional[Type[MCPClient]] = None,
        **client_kwargs,
    ) -> None:
        """Register an MCP server configuration.

        Args:
            config: Server configuration
            client_class: Optional client class (auto-detected from server_type if not provided)
            **client_kwargs: Additional keyword arguments passed to client constructor
        """
        if client_class is None:
            client_class = MCP_CLIENT_REGISTRY.get(config.server_type)
            if client_class is None:
                raise ValueError(
                    f"No client registered for server type: {config.server_type}"
                )

        # Pass config to constructor - some clients need additional kwargs
        self._clients[config.name] = client_class(config=config, **client_kwargs)
        self._connected[config.name] = False

    async def connect(self, server_name: str) -> bool:
        """Connect to an MCP server.

        Args:
            server_name: Name of the server to connect to

        Returns:
            True if connection successful
        """
        if server_name not in self._clients:
            raise ValueError(f"No server registered with name: {server_name}")

        client = self._clients[server_name]

        try:
            await client.connect()
            self._connected[server_name] = True

            # Register tools from this server
            await self._register_server_tools(server_name)

            return True
        except Exception as e:
            self._connected[server_name] = False
            raise ConnectionError(f"Failed to connect to {server_name}: {e}")

    async def connect_all(self) -> Dict[str, bool]:
        """Connect to all registered servers.

        Returns:
            Dict mapping server names to connection status
        """
        results = {}

        for name in self._clients:
            try:
                results[name] = await self.connect(name)
            except Exception:
                results[name] = False

        return results

    async def disconnect(self, server_name: str) -> None:
        """Disconnect from an MCP server."""
        if server_name in self._clients:
            await self._clients[server_name].disconnect()
            self._connected[server_name] = False

    async def disconnect_all(self) -> None:
        """Disconnect from all servers."""
        for name in self._clients:
            await self.disconnect(name)

    async def _register_server_tools(self, server_name: str) -> None:
        """Register tools from an MCP server with the ToolRegistry."""
        client = self._clients[server_name]
        tools = await client.list_tools()

        for tool in tools:
            # Create a wrapper function for this tool
            tool_handler = self._create_tool_handler(server_name, tool.name)

            # Register with prefixed name to avoid conflicts
            tool_name = f"{server_name}_{tool.name}"

            self.tool_registry.add_tool(
                name=tool_name,
                handler=tool_handler,
                description=tool.description,
                parameters=tool.input_schema,
            )

    def _create_tool_handler(
        self,
        server_name: str,
        tool_name: str,
    ) -> Callable:
        """Create a handler function for an MCP tool."""

        async def handler(**kwargs) -> Any:
            client = self._clients.get(server_name)
            if not client:
                raise ValueError(f"Server {server_name} not found")

            if not self._connected.get(server_name, False):
                raise ConnectionError(f"Server {server_name} not connected")

            response = await client.invoke_tool(tool_name, kwargs)

            if not response.success:
                raise Exception(response.error or "Tool invocation failed")

            return response.result

        return handler

    async def invoke_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> MCPResponse:
        """Invoke a tool on a specific MCP server.

        Args:
            server_name: Name of the server
            tool_name: Name of the tool
            arguments: Tool arguments

        Returns:
            MCPResponse with result
        """
        if server_name not in self._clients:
            return MCPResponse(
                success=False,
                result=None,
                error=f"Server {server_name} not found",
            )

        if not self._connected.get(server_name, False):
            return MCPResponse(
                success=False,
                result=None,
                error=f"Server {server_name} not connected",
            )

        return await self._clients[server_name].invoke_tool(tool_name, arguments)

    def list_servers(self) -> List[Dict[str, Any]]:
        """List all registered servers."""
        return [
            {
                "name": name,
                "server_type": client.config.server_type,
                "connected": self._connected.get(name, False),
                "capabilities": client.config.capabilities,
            }
            for name, client in self._clients.items()
        ]

    def list_tools(self, server_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """List available tools.

        Args:
            server_name: Optional filter by server name

        Returns:
            List of tool definitions
        """
        all_tools = []

        for name, client in self._clients.items():
            if server_name and name != server_name:
                continue

            for tool in client.tools:
                all_tools.append(
                    {
                        "server": name,
                        "name": tool.name,
                        "full_name": f"{name}_{tool.name}",
                        "description": tool.description,
                        "input_schema": tool.input_schema,
                    }
                )

        return all_tools

    def get_client(self, server_name: str) -> Optional[MCPClient]:
        """Get a specific MCP client."""
        return self._clients.get(server_name)

    def is_connected(self, server_name: str) -> bool:
        """Check if a server is connected."""
        return self._connected.get(server_name, False)


# Global MCP registry instance
_mcp_registry: Optional[MCPRegistry] = None


def get_mcp_registry(
    tool_registry: Optional[ToolRegistry] = None,
) -> MCPRegistry:
    """Get or create the global MCP registry."""
    global _mcp_registry

    if _mcp_registry is None:
        _mcp_registry = MCPRegistry(tool_registry)

    return _mcp_registry


async def setup_default_mcp_servers(
    allowed_directories: Optional[List[str]] = None,
    github_token: Optional[str] = None,
    enable_memory: bool = True,
    memory_path: Optional[str] = None,
) -> MCPRegistry:
    """Set up default MCP servers.

    Args:
        allowed_directories: Directories for filesystem access
        github_token: GitHub API token

    Returns:
        Configured MCPRegistry
    """
    registry = get_mcp_registry()

    # Register filesystem server
    from multiagent_workflows.mcp.filesystem import FilesystemMCPClient

    fs_config = MCPServerConfig(
        name="filesystem",
        server_type="filesystem",
        capabilities=["read", "write", "search"],
    )

    fs_client = FilesystemMCPClient(
        allowed_directories=allowed_directories,
        config=fs_config,
    )
    registry._clients["filesystem"] = fs_client

    # Register memory server (local persistent KV store)
    if enable_memory:
        from multiagent_workflows.mcp.memory import MemoryMCPClient

        mem_config = MCPServerConfig(
            name="memory",
            server_type="memory",
            capabilities=["store", "search"],
        )

        mem_client = MemoryMCPClient(storage_path=memory_path, config=mem_config)
        registry._clients["memory"] = mem_client

    # Register GitHub server if token provided
    if github_token:
        from multiagent_workflows.mcp.github import GitHubMCPClient

        gh_config = MCPServerConfig(
            name="github",
            server_type="github",
            capabilities=["repos", "issues", "pulls", "search"],
        )

        gh_client = GitHubMCPClient(token=github_token, config=gh_config)
        registry._clients["github"] = gh_client

    # Connect all servers
    await registry.connect_all()

    return registry
