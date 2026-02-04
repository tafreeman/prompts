"""
MCP (Model Context Protocol) Base Classes

Provides abstract base class for MCP server clients.
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type


@dataclass
class MCPToolSchema:
    """Schema for an MCP tool."""
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Optional[Dict[str, Any]] = None


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server."""
    name: str
    server_type: str
    endpoint: Optional[str] = None
    command: Optional[str] = None
    args: List[str] = field(default_factory=list)
    env: Dict[str, str] = field(default_factory=dict)
    capabilities: List[str] = field(default_factory=list)


@dataclass
class MCPResponse:
    """Response from an MCP tool invocation."""
    success: bool
    result: Any
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class MCPClient(ABC):
    """
    Abstract base class for MCP server clients.
    
    Subclasses should implement:
    - connect(): Establish connection to the MCP server
    - disconnect(): Close the connection
    - list_tools(): Get available tools from the server
    - invoke_tool(): Call a tool on the server
    """
    
    def __init__(self, config: MCPServerConfig):
        self.config = config
        self.connected = False
        self._tools: List[MCPToolSchema] = []
    
    @property
    def name(self) -> str:
        return self.config.name
    
    @property
    def tools(self) -> List[MCPToolSchema]:
        return self._tools
    
    @abstractmethod
    async def connect(self) -> bool:
        """
        Establish connection to the MCP server.
        
        Returns:
            True if connection successful
        """
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        """Close the connection to the MCP server."""
        pass
    
    @abstractmethod
    async def list_tools(self) -> List[MCPToolSchema]:
        """
        Get available tools from the server.
        
        Returns:
            List of tool schemas
        """
        pass
    
    @abstractmethod
    async def invoke_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> MCPResponse:
        """
        Invoke a tool on the server.
        
        Args:
            tool_name: Name of the tool to invoke
            arguments: Tool arguments
            
        Returns:
            MCPResponse with result or error
        """
        pass
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()


class StdioMCPClient(MCPClient):
    """
    MCP client that communicates via stdio with a subprocess.
    
    This is the standard way to communicate with MCP servers that
    are launched as external processes.
    """
    
    def __init__(self, config: MCPServerConfig):
        super().__init__(config)
        self._process: Optional[asyncio.subprocess.Process] = None
        self._reader_task: Optional[asyncio.Task] = None
        self._pending_requests: Dict[str, asyncio.Future] = {}
        self._request_id = 0
    
    async def connect(self) -> bool:
        """Start the MCP server process and establish connection."""
        if not self.config.command:
            raise ValueError("StdioMCPClient requires a command in config")
        
        try:
            # Start the subprocess
            self._process = await asyncio.create_subprocess_exec(
                self.config.command,
                *self.config.args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env={**os.environ, **self.config.env} if self.config.env else None,
            )
            
            # Start reader task
            self._reader_task = asyncio.create_task(self._read_responses())
            
            # Initialize the connection
            await self._send_initialize()
            
            # List available tools
            self._tools = await self.list_tools()
            
            self.connected = True
            return True
            
        except Exception as e:
            self.connected = False
            raise ConnectionError(f"Failed to connect to MCP server: {e}")
    
    async def disconnect(self) -> None:
        """Stop the MCP server process."""
        self.connected = False
        
        if self._reader_task:
            self._reader_task.cancel()
            try:
                await self._reader_task
            except asyncio.CancelledError:
                pass
        
        if self._process:
            self._process.terminate()
            await self._process.wait()
    
    async def list_tools(self) -> List[MCPToolSchema]:
        """Request tool list from the server."""
        response = await self._send_request("tools/list", {})
        
        tools = []
        for tool_data in response.get("tools", []):
            tools.append(MCPToolSchema(
                name=tool_data["name"],
                description=tool_data.get("description", ""),
                input_schema=tool_data.get("inputSchema", {}),
                output_schema=tool_data.get("outputSchema"),
            ))
        
        return tools
    
    async def invoke_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> MCPResponse:
        """Invoke a tool on the MCP server."""
        try:
            response = await self._send_request("tools/call", {
                "name": tool_name,
                "arguments": arguments,
            })
            
            return MCPResponse(
                success=True,
                result=response.get("content", []),
                metadata=response.get("metadata", {}),
            )
            
        except Exception as e:
            return MCPResponse(
                success=False,
                result=None,
                error=str(e),
            )
    
    async def _send_initialize(self) -> Dict[str, Any]:
        """Send initialization request."""
        return await self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "multiagent-workflows",
                "version": "1.0.0",
            },
        })
    
    async def _send_request(
        self,
        method: str,
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Send a JSON-RPC request and wait for response."""
        import json
        
        self._request_id += 1
        request_id = str(self._request_id)
        
        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": method,
            "params": params,
        }
        
        # Create future for response
        future = asyncio.get_event_loop().create_future()
        self._pending_requests[request_id] = future
        
        # Send request
        if self._process and self._process.stdin:
            message = json.dumps(request) + "\n"
            self._process.stdin.write(message.encode())
            await self._process.stdin.drain()
        
        # Wait for response
        try:
            result = await asyncio.wait_for(future, timeout=30.0)
            return result
        finally:
            self._pending_requests.pop(request_id, None)
    
    async def _read_responses(self) -> None:
        """Read responses from the subprocess."""
        import json
        
        while self._process and self._process.stdout:
            try:
                line = await self._process.stdout.readline()
                if not line:
                    break
                
                message = json.loads(line.decode())
                request_id = message.get("id")
                
                if request_id and request_id in self._pending_requests:
                    future = self._pending_requests[request_id]
                    
                    if "error" in message:
                        future.set_exception(
                            Exception(message["error"].get("message", "Unknown error"))
                        )
                    else:
                        future.set_result(message.get("result", {}))
                        
            except asyncio.CancelledError:
                break
            except Exception:
                continue


# Import os for environment variable handling
import os
