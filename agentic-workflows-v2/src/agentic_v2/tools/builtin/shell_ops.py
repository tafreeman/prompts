"""Tier 0 Shell execution tools - No LLM required."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from ..base import BaseTool, ToolResult


class ShellTool(BaseTool):
    """Execute shell commands securely."""

    @property
    def name(self) -> str:
        return "shell"

    @property
    def description(self) -> str:
        return "Execute shell commands with security controls and output capture"

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "command": {
                "type": "string",
                "description": "Shell command to execute",
                "required": True,
            },
            "cwd": {
                "type": "string",
                "description": "Working directory for command execution",
                "required": False,
                "default": ".",
            },
            "timeout": {
                "type": "number",
                "description": "Command timeout in seconds",
                "required": False,
                "default": 60,
            },
            "capture_output": {
                "type": "boolean",
                "description": "Whether to capture stdout/stderr",
                "required": False,
                "default": True,
            },
        }

    @property
    def tier(self) -> int:
        return 0

    @property
    def examples(self) -> list[str]:
        return [
            "shell(command='ls -la') → List directory contents",
            "shell(command='echo hello') → Echo a string",
            "shell(command='python --version') → Check Python version",
        ]

    async def execute(
        self,
        command: str,
        cwd: str = ".",
        timeout: float = 60.0,
        capture_output: bool = True,
    ) -> ToolResult:
        """Execute shell command."""
        try:
            # Basic security checks
            if any(
                dangerous in command.lower()
                for dangerous in ["rm -rf /", ":(){ :|:& };:", "mkfs", "dd if="]
            ):
                return ToolResult(
                    success=False,
                    error="Command contains potentially dangerous operations and was blocked",
                )

            # Verify working directory
            cwd_path = Path(cwd)
            if not cwd_path.exists():
                return ToolResult(
                    success=False, error=f"Working directory does not exist: {cwd}"
                )

            # Execute command
            if capture_output:
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    cwd=str(cwd_path),
                )

                try:
                    stdout, stderr = await asyncio.wait_for(
                        process.communicate(), timeout=timeout
                    )

                    stdout_str = stdout.decode("utf-8", errors="replace")
                    stderr_str = stderr.decode("utf-8", errors="replace")

                    return ToolResult(
                        success=process.returncode == 0,
                        data={
                            "stdout": stdout_str,
                            "stderr": stderr_str,
                            "exit_code": process.returncode,
                            "command": command,
                        },
                        metadata={
                            "cwd": cwd,
                            "timeout": timeout,
                        },
                    )

                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()
                    return ToolResult(
                        success=False,
                        error=f"Command timed out after {timeout} seconds",
                        metadata={"command": command, "timeout": timeout},
                    )

            else:
                # Fire and forget mode
                process = await asyncio.create_subprocess_shell(
                    command, cwd=str(cwd_path)
                )

                return ToolResult(
                    success=True,
                    data={
                        "pid": process.pid,
                        "command": command,
                        "message": "Command started (output not captured)",
                    },
                    metadata={"cwd": cwd},
                )

        except Exception as e:
            return ToolResult(
                success=False, error=f"Failed to execute shell command: {str(e)}"
            )


class ShellExecTool(BaseTool):
    """Execute shell commands with automatic argument escaping."""

    @property
    def name(self) -> str:
        return "shell_exec"

    @property
    def description(self) -> str:
        return "Execute shell commands with automatic argument escaping for safety"

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "program": {
                "type": "string",
                "description": "Program/command to execute",
                "required": True,
            },
            "args": {
                "type": "array",
                "description": "Arguments to pass to the program",
                "required": False,
                "default": [],
            },
            "cwd": {
                "type": "string",
                "description": "Working directory",
                "required": False,
                "default": ".",
            },
            "timeout": {
                "type": "number",
                "description": "Command timeout in seconds",
                "required": False,
                "default": 60,
            },
        }

    async def execute(
        self,
        program: str,
        args: list[str] | None = None,
        cwd: str = ".",
        timeout: float = 60.0,
    ) -> ToolResult:
        """Execute command with escaped arguments."""
        try:
            cwd_path = Path(cwd)
            if not cwd_path.exists():
                return ToolResult(
                    success=False, error=f"Working directory does not exist: {cwd}"
                )

            cmd_list = [program]
            if args:
                cmd_list.extend(args)

            process = await asyncio.create_subprocess_exec(
                *cmd_list,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(cwd_path),
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=timeout
                )

                return ToolResult(
                    success=process.returncode == 0,
                    data={
                        "stdout": stdout.decode("utf-8", errors="replace"),
                        "stderr": stderr.decode("utf-8", errors="replace"),
                        "exit_code": process.returncode,
                        "program": program,
                        "args": args or [],
                    },
                    metadata={"cwd": cwd},
                )

            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return ToolResult(
                    success=False, error=f"Command timed out after {timeout} seconds"
                )

        except Exception as e:
            return ToolResult(
                success=False, error=f"Failed to execute command: {str(e)}"
            )
