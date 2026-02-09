"""Filesystem MCP Server Client.

Provides file system access via MCP protocol.
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Dict, List, Optional

from multiagent_workflows.mcp.base import (
    MCPClient,
    MCPResponse,
    MCPServerConfig,
    MCPToolSchema,
)


class FilesystemMCPClient(MCPClient):
    """MCP client for filesystem operations.

    This is a local implementation that doesn't require an external
    server. It implements the standard MCP filesystem tools directly.
    """

    # Standard filesystem operations
    TOOLS = [
        MCPToolSchema(
            name="read_file",
            description="Read the complete contents of a file from the file system",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute path to the file to read",
                    },
                },
                "required": ["path"],
            },
        ),
        MCPToolSchema(
            name="read_multiple_files",
            description="Read the contents of multiple files simultaneously",
            input_schema={
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of absolute file paths to read",
                    },
                },
                "required": ["paths"],
            },
        ),
        MCPToolSchema(
            name="write_file",
            description="Create a new file or completely overwrite an existing file with new content",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute path where to write the file",
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to write to the file",
                    },
                },
                "required": ["path", "content"],
            },
        ),
        MCPToolSchema(
            name="edit_file",
            description="Make line-based edits to a text file",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute path to the file to edit",
                    },
                    "edits": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "oldText": {"type": "string"},
                                "newText": {"type": "string"},
                            },
                            "required": ["oldText", "newText"],
                        },
                        "description": "List of edit operations",
                    },
                    "dryRun": {
                        "type": "boolean",
                        "description": "If true, preview changes without applying",
                    },
                },
                "required": ["path", "edits"],
            },
        ),
        MCPToolSchema(
            name="create_directory",
            description="Create a new directory or ensure a directory exists",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute path of the directory to create",
                    },
                },
                "required": ["path"],
            },
        ),
        MCPToolSchema(
            name="list_directory",
            description="List directory contents with [FILE] or [DIR] indicators",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute path of the directory to list",
                    },
                },
                "required": ["path"],
            },
        ),
        MCPToolSchema(
            name="directory_tree",
            description="Get a recursive tree view of files and directories",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute path of the directory to display",
                    },
                },
                "required": ["path"],
            },
        ),
        MCPToolSchema(
            name="move_file",
            description="Move or rename files and directories",
            input_schema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "Source path",
                    },
                    "destination": {
                        "type": "string",
                        "description": "Destination path",
                    },
                },
                "required": ["source", "destination"],
            },
        ),
        MCPToolSchema(
            name="search_files",
            description="Search for files using glob patterns",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Directory to search in",
                    },
                    "pattern": {
                        "type": "string",
                        "description": "Glob pattern to match",
                    },
                    "excludePatterns": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Patterns to exclude",
                    },
                },
                "required": ["path", "pattern"],
            },
        ),
        MCPToolSchema(
            name="get_file_info",
            description="Get detailed metadata about a file or directory",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to get info for",
                    },
                },
                "required": ["path"],
            },
        ),
    ]

    def __init__(
        self,
        allowed_directories: Optional[List[str]] = None,
        config: Optional[MCPServerConfig] = None,
    ):
        if config is None:
            config = MCPServerConfig(
                name="filesystem",
                server_type="local",
                capabilities=["read", "write", "search"],
            )
        super().__init__(config)

        self.allowed_directories = [
            Path(d).resolve() for d in (allowed_directories or [])
        ]
        self._tools = self.TOOLS.copy()

    def _validate_path(self, path: str) -> Path:
        """Validate that a path is within allowed directories."""
        resolved = Path(path).resolve()

        if self.allowed_directories:
            if not any(
                self._is_subpath(resolved, allowed)
                for allowed in self.allowed_directories
            ):
                raise PermissionError(f"Path {path} is outside allowed directories")

        return resolved

    def _is_subpath(self, path: Path, parent: Path) -> bool:
        """Check if path is under parent directory."""
        try:
            path.relative_to(parent)
            return True
        except ValueError:
            return False

    async def connect(self) -> bool:
        """No connection needed for local filesystem."""
        self.connected = True
        return True

    async def disconnect(self) -> None:
        """No disconnection needed for local filesystem."""
        self.connected = False

    async def list_tools(self) -> List[MCPToolSchema]:
        """Return available filesystem tools."""
        return self._tools

    async def invoke_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> MCPResponse:
        """Invoke a filesystem tool."""
        try:
            handlers = {
                "read_file": self._read_file,
                "read_multiple_files": self._read_multiple_files,
                "write_file": self._write_file,
                "edit_file": self._edit_file,
                "create_directory": self._create_directory,
                "list_directory": self._list_directory,
                "directory_tree": self._directory_tree,
                "move_file": self._move_file,
                "search_files": self._search_files,
                "get_file_info": self._get_file_info,
            }

            handler = handlers.get(tool_name)
            if not handler:
                return MCPResponse(
                    success=False,
                    result=None,
                    error=f"Unknown tool: {tool_name}",
                )

            result = await asyncio.to_thread(handler, arguments)
            return MCPResponse(success=True, result=result)

        except PermissionError as e:
            return MCPResponse(success=False, result=None, error=str(e))
        except FileNotFoundError as e:
            return MCPResponse(success=False, result=None, error=str(e))
        except Exception as e:
            return MCPResponse(success=False, result=None, error=str(e))

    def _read_file(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Read a file's contents."""
        path = self._validate_path(args["path"])
        content = path.read_text(encoding="utf-8")
        return {"content": content}

    def _read_multiple_files(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Read multiple files."""
        results = {}
        for file_path in args["paths"]:
            try:
                path = self._validate_path(file_path)
                results[file_path] = path.read_text(encoding="utf-8")
            except Exception as e:
                results[file_path] = f"Error: {e}"
        return {"files": results}

    def _write_file(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Write content to a file."""
        path = self._validate_path(args["path"])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(args["content"], encoding="utf-8")
        return {"success": True, "path": str(path)}

    def _edit_file(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Apply line-based edits to a file."""
        path = self._validate_path(args["path"])
        content = path.read_text(encoding="utf-8")

        changes = []
        for edit in args["edits"]:
            old_text = edit["oldText"]
            new_text = edit["newText"]
            if old_text in content:
                content = content.replace(old_text, new_text, 1)
                changes.append({"from": old_text[:50], "to": new_text[:50]})

        if not args.get("dryRun", False):
            path.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "changes": changes,
            "dryRun": args.get("dryRun", False),
        }

    def _create_directory(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a directory."""
        path = self._validate_path(args["path"])
        path.mkdir(parents=True, exist_ok=True)
        return {"success": True, "path": str(path)}

    def _list_directory(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """List directory contents."""
        path = self._validate_path(args["path"])
        entries = []

        for item in sorted(path.iterdir()):
            prefix = "[DIR]" if item.is_dir() else "[FILE]"
            entries.append(f"{prefix} {item.name}")

        return {"entries": entries}

    def _directory_tree(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get directory tree."""
        path = self._validate_path(args["path"])

        def build_tree(directory: Path, prefix: str = "") -> List[str]:
            lines = []
            items = sorted(directory.iterdir())

            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{item.name}")

                if item.is_dir():
                    extension = "    " if is_last else "│   "
                    lines.extend(build_tree(item, prefix + extension))

            return lines

        tree = [str(path)] + build_tree(path)
        return {"tree": "\n".join(tree)}

    def _move_file(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Move or rename a file."""
        source = self._validate_path(args["source"])
        dest = self._validate_path(args["destination"])
        source.rename(dest)
        return {"success": True, "source": str(source), "destination": str(dest)}

    def _search_files(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Search for files matching a pattern."""
        path = self._validate_path(args["path"])
        pattern = args["pattern"]
        exclude = args.get("excludePatterns", [])

        matches = []
        for match in path.rglob(pattern):
            # Check exclusions
            skip = False
            for exc in exclude:
                if match.match(exc):
                    skip = True
                    break

            if not skip:
                matches.append(str(match))

        return {"matches": matches}

    def _get_file_info(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get file metadata."""
        path = self._validate_path(args["path"])
        stat = path.stat()

        return {
            "path": str(path),
            "name": path.name,
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "isDirectory": path.is_dir(),
            "isFile": path.is_file(),
        }
