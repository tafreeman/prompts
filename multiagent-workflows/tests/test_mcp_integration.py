"""Tests for MCP (Model Context Protocol) Integration.

Tests the MCP base classes, filesystem client, GitHub client, and
registry.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# =============================================================================
# Test MCP Base Classes
# =============================================================================


class TestMCPToolSchema:
    """Test MCPToolSchema dataclass."""

    def test_tool_schema_creation(self):
        """Test creating an MCPToolSchema."""
        from multiagent_workflows.mcp.base import MCPToolSchema

        schema = MCPToolSchema(
            name="test_tool",
            description="A test tool",
            input_schema={
                "type": "object",
                "properties": {"input": {"type": "string"}},
            },
        )

        assert schema.name == "test_tool"
        assert schema.description == "A test tool"
        assert schema.output_schema is None

    def test_tool_schema_with_output(self):
        """Test MCPToolSchema with output schema."""
        from multiagent_workflows.mcp.base import MCPToolSchema

        schema = MCPToolSchema(
            name="transform_tool",
            description="Transforms data",
            input_schema={"type": "string"},
            output_schema={"type": "object"},
        )

        assert schema.output_schema == {"type": "object"}


class TestMCPServerConfig:
    """Test MCPServerConfig dataclass."""

    def test_server_config_minimal(self):
        """Test creating minimal MCPServerConfig."""
        from multiagent_workflows.mcp.base import MCPServerConfig

        config = MCPServerConfig(
            name="test_server",
            server_type="local",
        )

        assert config.name == "test_server"
        assert config.server_type == "local"
        assert config.endpoint is None
        assert config.args == []
        assert config.env == {}
        assert config.capabilities == []

    def test_server_config_full(self):
        """Test MCPServerConfig with all fields."""
        from multiagent_workflows.mcp.base import MCPServerConfig

        config = MCPServerConfig(
            name="github_server",
            server_type="stdio",
            endpoint="https://api.github.com",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={"GITHUB_TOKEN": "test"},
            capabilities=["repos", "issues"],
        )

        assert config.command == "npx"
        assert len(config.args) == 2
        assert config.env["GITHUB_TOKEN"] == "test"
        assert "repos" in config.capabilities


class TestMCPResponse:
    """Test MCPResponse dataclass."""

    def test_successful_response(self):
        """Test creating a successful MCPResponse."""
        from multiagent_workflows.mcp.base import MCPResponse

        response = MCPResponse(
            success=True,
            result={"content": "test data"},
        )

        assert response.success is True
        assert response.result == {"content": "test data"}
        assert response.error is None
        assert response.metadata == {}

    def test_error_response(self):
        """Test creating an error MCPResponse."""
        from multiagent_workflows.mcp.base import MCPResponse

        response = MCPResponse(
            success=False,
            result=None,
            error="File not found",
        )

        assert response.success is False
        assert response.result is None
        assert response.error == "File not found"


class TestMCPClientBase:
    """Test MCPClient abstract base class."""

    def test_client_properties(self):
        """Test MCPClient properties."""
        from multiagent_workflows.mcp.base import MCPClient, MCPServerConfig

        # Create a concrete implementation for testing
        class TestClient(MCPClient):
            async def connect(self):
                self.connected = True
                return True

            async def disconnect(self):
                self.connected = False

            async def list_tools(self):
                return []

            async def invoke_tool(self, tool_name, arguments):
                from multiagent_workflows.mcp.base import MCPResponse

                return MCPResponse(success=True, result={})

        config = MCPServerConfig(name="test", server_type="local")
        client = TestClient(config)

        assert client.name == "test"
        assert client.tools == []
        assert client.connected is False


# =============================================================================
# Test Filesystem MCP Client
# =============================================================================


class TestFilesystemMCPClient:
    """Test FilesystemMCPClient implementation."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def fs_client(self, temp_dir):
        """Create a FilesystemMCPClient for testing."""
        from multiagent_workflows.mcp.filesystem import FilesystemMCPClient

        return FilesystemMCPClient(allowed_directories=[temp_dir])

    @pytest.mark.asyncio
    async def test_connect(self, fs_client):
        """Test filesystem client connection."""
        result = await fs_client.connect()

        assert result is True
        assert fs_client.connected is True

    @pytest.mark.asyncio
    async def test_disconnect(self, fs_client):
        """Test filesystem client disconnection."""
        await fs_client.connect()
        await fs_client.disconnect()

        assert fs_client.connected is False

    @pytest.mark.asyncio
    async def test_list_tools(self, fs_client):
        """Test listing filesystem tools."""
        tools = await fs_client.list_tools()

        assert len(tools) > 0
        tool_names = [t.name for t in tools]

        assert "read_file" in tool_names
        assert "write_file" in tool_names
        assert "list_directory" in tool_names

    @pytest.mark.asyncio
    async def test_read_write_file(self, fs_client, temp_dir):
        """Test reading and writing files."""
        await fs_client.connect()

        # Write a file
        test_path = os.path.join(temp_dir, "test.txt")
        write_response = await fs_client.invoke_tool(
            "write_file",
            {
                "path": test_path,
                "content": "Hello, World!",
            },
        )

        assert write_response.success is True

        # Read it back
        read_response = await fs_client.invoke_tool(
            "read_file",
            {
                "path": test_path,
            },
        )

        assert read_response.success is True
        assert read_response.result["content"] == "Hello, World!"

    @pytest.mark.asyncio
    async def test_list_directory(self, fs_client, temp_dir):
        """Test listing directory contents."""
        await fs_client.connect()

        # Create some files
        Path(temp_dir, "file1.txt").write_text("content1")
        Path(temp_dir, "file2.txt").write_text("content2")
        Path(temp_dir, "subdir").mkdir()

        response = await fs_client.invoke_tool(
            "list_directory",
            {
                "path": temp_dir,
            },
        )

        assert response.success is True
        entries = response.result["entries"]

        assert "[FILE] file1.txt" in entries
        assert "[FILE] file2.txt" in entries
        assert "[DIR] subdir" in entries

    @pytest.mark.asyncio
    async def test_create_directory(self, fs_client, temp_dir):
        """Test creating directories."""
        await fs_client.connect()

        new_dir = os.path.join(temp_dir, "new_folder", "nested")
        response = await fs_client.invoke_tool(
            "create_directory",
            {
                "path": new_dir,
            },
        )

        assert response.success is True
        assert Path(new_dir).exists()

    @pytest.mark.asyncio
    async def test_edit_file(self, fs_client, temp_dir):
        """Test editing files with replacements."""
        await fs_client.connect()

        # Write initial content
        test_path = os.path.join(temp_dir, "edit_test.txt")
        await fs_client.invoke_tool(
            "write_file",
            {
                "path": test_path,
                "content": "Hello World",
            },
        )

        # Edit it
        response = await fs_client.invoke_tool(
            "edit_file",
            {
                "path": test_path,
                "edits": [{"oldText": "World", "newText": "Python"}],
            },
        )

        assert response.success is True

        # Verify edit
        read_response = await fs_client.invoke_tool("read_file", {"path": test_path})
        assert read_response.result["content"] == "Hello Python"

    @pytest.mark.asyncio
    async def test_search_files(self, fs_client, temp_dir):
        """Test searching for files."""
        await fs_client.connect()

        # Create some files
        Path(temp_dir, "test1.py").write_text("print('hello')")
        Path(temp_dir, "test2.py").write_text("print('world')")
        Path(temp_dir, "readme.md").write_text("# README")

        response = await fs_client.invoke_tool(
            "search_files",
            {
                "path": temp_dir,
                "pattern": "*.py",
            },
        )

        assert response.success is True
        matches = response.result["matches"]

        assert len(matches) == 2
        assert any("test1.py" in m for m in matches)
        assert any("test2.py" in m for m in matches)

    @pytest.mark.asyncio
    async def test_get_file_info(self, fs_client, temp_dir):
        """Test getting file information."""
        await fs_client.connect()

        test_path = os.path.join(temp_dir, "info_test.txt")
        Path(test_path).write_text("test content")

        response = await fs_client.invoke_tool(
            "get_file_info",
            {
                "path": test_path,
            },
        )

        assert response.success is True
        info = response.result

        assert info["name"] == "info_test.txt"
        assert info["size"] == 12  # "test content"
        assert info["isFile"] is True
        assert info["isDirectory"] is False

    @pytest.mark.asyncio
    async def test_path_validation(self, fs_client, temp_dir):
        """Test that paths outside allowed directories are rejected."""
        await fs_client.connect()

        # Try to access a path outside allowed directories
        response = await fs_client.invoke_tool(
            "read_file",
            {
                "path": "/etc/passwd",  # Outside allowed directory
            },
        )

        assert response.success is False
        assert (
            "outside allowed directories" in response.error.lower()
            or "not found" in response.error.lower()
        )

    @pytest.mark.asyncio
    async def test_directory_tree(self, fs_client, temp_dir):
        """Test getting directory tree."""
        await fs_client.connect()

        # Create structure
        Path(temp_dir, "src").mkdir()
        Path(temp_dir, "src", "main.py").write_text("# main")
        Path(temp_dir, "tests").mkdir()
        Path(temp_dir, "tests", "test_main.py").write_text("# tests")

        response = await fs_client.invoke_tool(
            "directory_tree",
            {
                "path": temp_dir,
            },
        )

        assert response.success is True
        tree = response.result["tree"]

        assert "src" in tree
        assert "main.py" in tree
        assert "tests" in tree


# =============================================================================
# Test Memory MCP Client
# =============================================================================


class TestMemoryMCPClient:
    """Test MemoryMCPClient implementation."""

    @pytest.mark.asyncio
    async def test_upsert_get_list_search(self, tmp_path: Path):
        from multiagent_workflows.mcp.memory import MemoryMCPClient

        storage_path = tmp_path / "memory.json"
        client = MemoryMCPClient(storage_path=str(storage_path))
        await client.connect()

        # Upsert
        up = await client.invoke_tool(
            "upsert",
            {"key": "agentic/workflows", "value": {"status": "ok"}, "tags": ["test"]},
        )
        assert up.success is True

        # Get
        got = await client.invoke_tool("get", {"key": "agentic/workflows"})
        assert got.success is True
        assert got.result["found"] is True
        assert got.result["entry"]["value"]["status"] == "ok"

        # List
        listed = await client.invoke_tool("list", {"prefix": "agentic/", "limit": 10})
        assert listed.success is True
        assert "agentic/workflows" in listed.result["keys"]

        # Search
        searched = await client.invoke_tool(
            "search", {"query": "workflows", "limit": 10}
        )
        assert searched.success is True
        assert searched.result["count"] >= 1
        assert any(r["key"] == "agentic/workflows" for r in searched.result["results"])


# =============================================================================
# Test GitHub MCP Client
# =============================================================================


class TestGitHubMCPClient:
    """Test GitHubMCPClient implementation."""

    @pytest.fixture
    def gh_client(self):
        """Create a GitHubMCPClient for testing."""
        from multiagent_workflows.mcp.github import GitHubMCPClient

        return GitHubMCPClient(token="test-token-123")

    @pytest.mark.asyncio
    async def test_connect_with_token(self, gh_client):
        """Test GitHub client connection with token."""
        result = await gh_client.connect()

        assert result is True
        assert gh_client.connected is True

    @pytest.mark.asyncio
    async def test_connect_without_token(self):
        """Test GitHub client fails without token."""
        from multiagent_workflows.mcp.github import GitHubMCPClient

        # Clear environment variable
        with patch.dict(os.environ, {}, clear=True):
            client = GitHubMCPClient(token=None)

            with pytest.raises(ValueError, match="token required"):
                await client.connect()

    @pytest.mark.asyncio
    async def test_list_tools(self, gh_client):
        """Test listing GitHub tools."""
        tools = await gh_client.list_tools()

        assert len(tools) > 0
        tool_names = [t.name for t in tools]

        assert "search_repositories" in tool_names
        assert "get_file_contents" in tool_names
        assert "create_issue" in tool_names
        assert "create_pull_request" in tool_names

    @pytest.mark.asyncio
    async def test_headers(self, gh_client):
        """Test that headers include authorization."""
        headers = gh_client._headers()

        assert "Authorization" in headers
        assert "Bearer test-token-123" in headers["Authorization"]
        assert headers["Accept"] == "application/vnd.github.v3+json"


# =============================================================================
# Test MCP Registry
# =============================================================================


class TestMCPRegistry:
    """Test MCPRegistry class."""

    @pytest.fixture
    def registry(self):
        """Create an MCPRegistry for testing."""
        from multiagent_workflows.core.tool_registry import ToolRegistry
        from multiagent_workflows.mcp.registry import MCPRegistry

        tool_registry = ToolRegistry()
        return MCPRegistry(tool_registry)

    def test_registry_creation(self, registry):
        """Test creating an MCPRegistry."""
        assert registry._clients == {}
        assert registry._connected == {}

    def test_register_server(self, registry):
        """Test registering an MCP server."""
        from multiagent_workflows.mcp.base import MCPServerConfig
        from multiagent_workflows.mcp.filesystem import FilesystemMCPClient

        config = MCPServerConfig(
            name="test_fs",
            server_type="filesystem",
        )

        registry.register_server(config, FilesystemMCPClient, allowed_directories=[])

        assert "test_fs" in registry._clients
        assert registry._connected["test_fs"] is False

    @pytest.mark.asyncio
    async def test_connect_server(self, registry):
        """Test connecting to a registered server."""
        from multiagent_workflows.mcp.base import MCPServerConfig
        from multiagent_workflows.mcp.filesystem import FilesystemMCPClient

        config = MCPServerConfig(name="fs", server_type="filesystem")
        registry.register_server(config, FilesystemMCPClient, allowed_directories=[])

        result = await registry.connect("fs")

        assert result is True
        assert registry.is_connected("fs") is True

    @pytest.mark.asyncio
    async def test_connect_unknown_server(self, registry):
        """Test connecting to unknown server raises error."""
        with pytest.raises(ValueError, match="No server registered"):
            await registry.connect("nonexistent")

    def test_list_servers(self, registry):
        """Test listing registered servers."""
        from multiagent_workflows.mcp.base import MCPServerConfig
        from multiagent_workflows.mcp.filesystem import FilesystemMCPClient

        config = MCPServerConfig(
            name="test_server",
            server_type="filesystem",
            capabilities=["read", "write"],
        )
        registry.register_server(config, FilesystemMCPClient, allowed_directories=[])

        servers = registry.list_servers()

        assert len(servers) == 1
        assert servers[0]["name"] == "test_server"
        assert servers[0]["connected"] is False
        assert "read" in servers[0]["capabilities"]

    @pytest.mark.asyncio
    async def test_list_tools(self, registry):
        """Test listing tools from registered servers."""
        from multiagent_workflows.mcp.base import MCPServerConfig
        from multiagent_workflows.mcp.filesystem import FilesystemMCPClient

        config = MCPServerConfig(name="fs", server_type="filesystem")
        registry.register_server(config, FilesystemMCPClient, allowed_directories=[])
        await registry.connect("fs")

        tools = registry.list_tools()

        assert len(tools) > 0
        assert all("server" in t for t in tools)
        assert all("name" in t for t in tools)

    @pytest.mark.asyncio
    async def test_invoke_tool(self, registry):
        """Test invoking a tool on a connected server."""
        import tempfile

        from multiagent_workflows.mcp.base import MCPServerConfig
        from multiagent_workflows.mcp.filesystem import FilesystemMCPClient

        with tempfile.TemporaryDirectory() as tmpdir:
            # Register and connect
            config = MCPServerConfig(name="fs", server_type="filesystem")
            client = FilesystemMCPClient(allowed_directories=[tmpdir], config=config)
            registry._clients["fs"] = client
            await registry.connect("fs")

            # Create a test file
            test_file = os.path.join(tmpdir, "test.txt")
            Path(test_file).write_text("hello")

            # Invoke tool through registry
            response = await registry.invoke_tool(
                "fs", "read_file", {"path": test_file}
            )

            assert response.success is True
            assert response.result["content"] == "hello"

    @pytest.mark.asyncio
    async def test_invoke_tool_disconnected(self, registry):
        """Test invoking tool on disconnected server fails."""
        from multiagent_workflows.mcp.base import MCPServerConfig
        from multiagent_workflows.mcp.filesystem import FilesystemMCPClient

        config = MCPServerConfig(name="fs", server_type="filesystem")
        registry.register_server(config, FilesystemMCPClient, allowed_directories=[])
        # Don't connect

        response = await registry.invoke_tool("fs", "read_file", {"path": "/tmp/test"})

        assert response.success is False
        assert "not connected" in response.error.lower()


class TestMCPRegistryGlobal:
    """Test global MCP registry functions."""

    def test_get_mcp_registry(self):
        """Test getting global MCP registry."""
        # Reset global
        import multiagent_workflows.mcp.registry as registry_module
        from multiagent_workflows.mcp.registry import get_mcp_registry

        registry_module._mcp_registry = None

        registry1 = get_mcp_registry()
        registry2 = get_mcp_registry()

        assert registry1 is registry2  # Same instance
