"""
MCP Connection Manager - orchestrates server connections and lifecycle.

Handles connection memoization, reconnection with exponential backoff,
auth failure suppression, and capability-driven discovery.
"""

import asyncio
import hashlib
import logging
import time
from typing import Dict, Optional, Tuple

from agentic_v2.integrations.mcp.protocol.client import McpProtocolClient, McpProtocolError
from agentic_v2.integrations.mcp.runtime.backoff import ExponentialBackoff
from agentic_v2.integrations.mcp.transports.stdio import StdioTransport
from agentic_v2.integrations.mcp.transports.websocket import WebSocketTransport
from agentic_v2.integrations.mcp.types import (
    McpConnectionState,
    McpServerConfig,
    McpServerInfo,
    McpStdioConfig,
    McpWebSocketConfig,
)

logger = logging.getLogger(__name__)

# Auth failure suppression: cache 401s for 15 minutes
AUTH_FAILURE_CACHE_DURATION = 15 * 60  # 15 minutes in seconds


class ConnectionMetadata:
    """Metadata for a managed connection."""

    def __init__(
        self,
        name: str,
        config: McpServerConfig,
        client: McpProtocolClient,
        backoff: ExponentialBackoff,
    ) -> None:
        self.name = name
        self.config = config
        self.client = client
        self.backoff = backoff
        self.state = McpConnectionState.CONNECTING
        self.server_info: Optional[McpServerInfo] = None
        self.last_error: Optional[str] = None
        self.auth_failure_timestamp: Optional[float] = None

    def is_auth_suppressed(self) -> bool:
        """Check if auth failures are being suppressed (within cache window)."""
        if not self.auth_failure_timestamp:
            return False
        elapsed = time.time() - self.auth_failure_timestamp
        return elapsed < AUTH_FAILURE_CACHE_DURATION

    def record_auth_failure(self) -> None:
        """Record an auth failure timestamp."""
        self.auth_failure_timestamp = time.time()
        self.state = McpConnectionState.NEEDS_AUTH
        logger.warning(
            f"Auth failure recorded for {self.name}, suppressing retries for {AUTH_FAILURE_CACHE_DURATION}s"
        )

    def clear_auth_failure(self) -> None:
        """Clear auth failure suppression."""
        self.auth_failure_timestamp = None


class McpConnectionManager:
    """
    Manages MCP server connections with lifecycle control.

    Features:
    - Connection memoization (one connection per server signature)
    - Exponential backoff on failures
    - Auth failure suppression (15-minute cache)
    - Capability-driven initialization
    - Graceful cleanup
    """

    def __init__(self) -> None:
        """Initialize connection manager."""
        self._connections: Dict[str, ConnectionMetadata] = {}
        self._lock = asyncio.Lock()

    def _compute_server_signature(self, config: McpServerConfig) -> str:
        """
        Compute unique signature for server config.

        Two configs with same signature = same server, reuse connection.

        Args:
            config: Server configuration

        Returns:
            Hex digest signature
        """
        if isinstance(config, McpStdioConfig):
            key = f"stdio:{config.command}:{':'.join(config.args)}"
        elif isinstance(config, McpWebSocketConfig):
            key = f"ws:{config.url}"
        else:
            # Generic fallback
            key = f"{config.type}:{config.model_dump_json()}"

        return hashlib.sha256(key.encode()).hexdigest()[:16]

    async def connect(
        self,
        name: str,
        config: McpServerConfig,
        force_new: bool = False,
    ) -> McpProtocolClient:
        """
        Connect to an MCP server (or return existing connection).

        Args:
            name: Server name (for logging)
            config: Server configuration
            force_new: Force new connection even if one exists

        Returns:
            Connected protocol client

        Raises:
            ConnectionError: If connection fails after retries
            RuntimeError: If auth is suppressed due to recent 401
        """
        async with self._lock:
            signature = self._compute_server_signature(config)

            # Check for existing connection
            if not force_new and signature in self._connections:
                metadata = self._connections[signature]

                # Check auth suppression
                if metadata.is_auth_suppressed():
                    raise RuntimeError(
                        f"Auth failures suppressed for {name} (retry after {AUTH_FAILURE_CACHE_DURATION}s)"
                    )

                # Return existing if connected
                if metadata.state == McpConnectionState.CONNECTED:
                    logger.debug(f"Reusing existing connection: {name}")
                    return metadata.client

            # Create new connection
            logger.info(f"Creating new connection: {name}")
            return await self._create_connection(name, config, signature)

    async def _create_connection(
        self,
        name: str,
        config: McpServerConfig,
        signature: str,
    ) -> McpProtocolClient:
        """
        Create and initialize a new MCP connection.

        Args:
            name: Server name
            config: Server config
            signature: Server signature (for memoization)

        Returns:
            Connected and initialized protocol client

        Raises:
            ConnectionError: If connection fails
        """
        # Create transport based on config type
        if isinstance(config, McpStdioConfig):
            transport = StdioTransport(
                command=config.command,
                args=config.args,
                env=config.env,
            )
        elif isinstance(config, McpWebSocketConfig):
            transport = WebSocketTransport(
                url=config.url,
                headers=config.headers,
            )
        else:
            raise ValueError(f"Unsupported transport type: {config.type}")

        # Create protocol client
        client = McpProtocolClient(transport)
        backoff = ExponentialBackoff(max_attempts=5)

        # Store metadata
        metadata = ConnectionMetadata(
            name=name,
            config=config,
            client=client,
            backoff=backoff,
        )
        self._connections[signature] = metadata

        # Attempt connection with backoff
        last_error: Optional[Exception] = None

        while not backoff.is_exhausted:
            try:
                # Start transport
                await client.connect()

                # Perform initialize handshake
                server_info = await client.initialize()
                metadata.server_info = server_info
                metadata.state = McpConnectionState.CONNECTED
                metadata.last_error = None
                backoff.reset()

                logger.info(
                    f"Successfully connected to {name}: {server_info.name} v{server_info.version}"
                )
                return client

            except asyncio.TimeoutError as e:
                last_error = e
                metadata.last_error = f"Timeout: {e}"
                metadata.state = McpConnectionState.RECONNECTING

                delay = backoff.next_delay()
                if delay:
                    logger.warning(
                        f"Connection timeout for {name}, retrying in {delay:.1f}s (attempt {backoff.attempt_count})"
                    )
                    await asyncio.sleep(delay)
                else:
                    break

            except McpProtocolError as e:
                last_error = e
                metadata.last_error = f"Protocol error: {e}"

                # Check if auth error (401)
                if "401" in str(e) or "Unauthorized" in str(e):
                    metadata.record_auth_failure()
                    raise RuntimeError(f"Auth failure for {name}: {e}") from e

                # Other protocol errors: retry with backoff
                metadata.state = McpConnectionState.RECONNECTING
                delay = backoff.next_delay()
                if delay:
                    logger.warning(
                        f"Protocol error for {name}, retrying in {delay:.1f}s: {e}"
                    )
                    await asyncio.sleep(delay)
                else:
                    break

            except Exception as e:
                last_error = e
                metadata.last_error = f"Unexpected error: {e}"
                metadata.state = McpConnectionState.FAILED
                logger.error(f"Unexpected error connecting to {name}: {e}")
                break

        # All retries exhausted
        metadata.state = McpConnectionState.FAILED
        raise ConnectionError(
            f"Failed to connect to {name} after {backoff.attempt_count} attempts: {last_error}"
        )

    async def disconnect(self, name: str) -> None:
        """
        Disconnect from a server by name.

        Args:
            name: Server name
        """
        async with self._lock:
            # Find connection by name
            for signature, metadata in list(self._connections.items()):
                if metadata.name == name:
                    logger.info(f"Disconnecting from {name}")
                    await metadata.client.close()
                    metadata.state = McpConnectionState.DISCONNECTED
                    del self._connections[signature]
                    return

            logger.warning(f"No connection found for {name}")

    async def disconnect_all(self) -> None:
        """Disconnect from all servers."""
        async with self._lock:
            logger.info(f"Disconnecting from {len(self._connections)} servers")

            for metadata in self._connections.values():
                try:
                    await metadata.client.close()
                except Exception as e:
                    logger.error(
                        f"Error closing connection {metadata.name}: {e}"
                    )

            self._connections.clear()

    def get_connection(self, name: str) -> Optional[McpProtocolClient]:
        """
        Get existing connection by name (if connected).

        Args:
            name: Server name

        Returns:
            Protocol client if connected, None otherwise
        """
        for metadata in self._connections.values():
            if (
                metadata.name == name
                and metadata.state == McpConnectionState.CONNECTED
            ):
                return metadata.client
        return None

    def get_connection_state(self, name: str) -> Optional[McpConnectionState]:
        """
        Get connection state by name.

        Args:
            name: Server name

        Returns:
            Connection state if exists, None otherwise
        """
        for metadata in self._connections.values():
            if metadata.name == name:
                return metadata.state
        return None

    def list_connections(self) -> Dict[str, Tuple[McpConnectionState, Optional[str]]]:
        """
        List all connections with their states.

        Returns:
            Dict mapping server name to (state, error_message)
        """
        return {
            metadata.name: (metadata.state, metadata.last_error)
            for metadata in self._connections.values()
        }
