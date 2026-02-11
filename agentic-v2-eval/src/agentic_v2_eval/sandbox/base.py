"""Sandbox environment interface."""

from __future__ import annotations

import abc
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class ExecutionResult:
    """Result of searching/executing code in sandbox."""

    exit_code: int
    stdout: str
    stderr: str
    duration_ms: float
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return self.exit_code == 0 and not self.error


class Sandbox(abc.ABC):
    """Abstract base class for code execution sandboxes."""

    @abc.abstractmethod
    def run_command(
        self,
        command: List[str],
        cwd: Optional[str] = None,
        timeout: Optional[int] = None,
        env: Optional[dict] = None,
    ) -> ExecutionResult:
        """Run a command in the sandbox.

        Args:
            command: Command and arguments list
            cwd: Working directory (relative to sandbox root)
            timeout: Timeout in seconds
            env: Environment variables

        Returns:
            ExecutionResult
        """
        pass

    @abc.abstractmethod
    def write_file(self, path: str, content: str):
        """Write content to a file in the sandbox."""
        pass

    @abc.abstractmethod
    def read_file(self, path: str) -> str:
        """Read content from a file in the sandbox."""
        pass
