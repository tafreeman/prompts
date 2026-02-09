"""Runtime abstractions for isolated task execution.

Wave 1 runtime policy:
- Subprocess runtime is the default.
- Docker runtime is opt-in through execution_profile.runtime="docker".
"""

from __future__ import annotations

import asyncio
import os
import shutil
import tempfile
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


DEFAULT_DOCKER_IMAGE = "python:3.11-slim"


@dataclass(slots=True)
class RuntimeExecutionResult:
    """Result from a single runtime command execution."""

    command: str
    exit_code: int
    stdout: str
    stderr: str
    workdir: str


class RuntimeExecutionError(RuntimeError):
    """Raised when a runtime command exits with a non-zero status."""

    def __init__(
        self,
        command: str,
        exit_code: int,
        stdout: str,
        stderr: str,
    ) -> None:
        message = (
            f"Command failed (exit code {exit_code}): {command}\n"
            f"stderr: {stderr.strip() or '<empty>'}"
        )
        super().__init__(message)
        self.command = command
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr


class IsolatedTaskRuntime(ABC):
    """Abstract runtime lifecycle for command execution."""

    @abstractmethod
    async def setup(self) -> None:
        """Initialize runtime dependencies/resources."""

    @abstractmethod
    async def execute(self, cmd: str, workdir: Path | str | None = None) -> RuntimeExecutionResult:
        """Execute a command in an isolated environment."""

    @abstractmethod
    async def collect_artifacts(self) -> dict[str, Any]:
        """Collect runtime artifacts produced during execution."""

    @abstractmethod
    async def cleanup(self) -> None:
        """Release runtime resources."""


def _host_shell_command(command: str) -> tuple[str, ...]:
    """Return host shell invocation args while still using subprocess_exec."""
    if os.name == "nt":
        return ("cmd", "/c", command)
    shell = os.environ.get("SHELL", "/bin/bash")
    return (shell, "-lc", command)


class SubprocessRuntime(IsolatedTaskRuntime):
    """Default runtime: run commands in host subprocesses."""

    def __init__(self) -> None:
        self._is_setup = False
        self._managed_workdirs: list[Path] = []
        self._executions: list[RuntimeExecutionResult] = []

    async def setup(self) -> None:
        self._is_setup = True

    async def execute(self, cmd: str, workdir: Path | str | None = None) -> RuntimeExecutionResult:
        if not self._is_setup:
            await self.setup()

        cwd = self._resolve_workdir(workdir)
        proc = await asyncio.create_subprocess_exec(
            *_host_shell_command(cmd),
            cwd=str(cwd),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout_bytes, stderr_bytes = await proc.communicate()
        stdout = stdout_bytes.decode("utf-8", errors="replace")
        stderr = stderr_bytes.decode("utf-8", errors="replace")

        result = RuntimeExecutionResult(
            command=cmd,
            exit_code=int(proc.returncode or 0),
            stdout=stdout,
            stderr=stderr,
            workdir=str(cwd),
        )
        self._executions.append(result)

        if result.exit_code != 0:
            raise RuntimeExecutionError(cmd, result.exit_code, stdout, stderr)

        return result

    async def collect_artifacts(self) -> dict[str, Any]:
        return {
            "executions": [asdict(execution) for execution in self._executions],
            "workdirs": [str(path) for path in self._managed_workdirs],
        }

    async def cleanup(self) -> None:
        for path in self._managed_workdirs:
            shutil.rmtree(path, ignore_errors=True)
        self._managed_workdirs.clear()
        self._is_setup = False

    def _resolve_workdir(self, workdir: Path | str | None) -> Path:
        if workdir is not None:
            return Path(workdir)
        tmp = Path(tempfile.mkdtemp(prefix="agentic-runtime-"))
        self._managed_workdirs.append(tmp)
        return tmp


class DockerRuntime(IsolatedTaskRuntime):
    """Optional runtime: run commands inside Docker."""

    def __init__(self, container_image: str | None = None) -> None:
        self._container_image = container_image or DEFAULT_DOCKER_IMAGE
        self._is_setup = False
        self._managed_workdirs: list[Path] = []
        self._executions: list[RuntimeExecutionResult] = []

    @staticmethod
    def is_available() -> bool:
        return shutil.which("docker") is not None

    async def setup(self) -> None:
        if not self.is_available():
            raise RuntimeError(
                "Docker runtime requested but Docker was not found on PATH."
            )
        self._is_setup = True

    async def execute(self, cmd: str, workdir: Path | str | None = None) -> RuntimeExecutionResult:
        if not self._is_setup:
            await self.setup()

        cwd = self._resolve_workdir(workdir)
        command = self._docker_command(cmd, cwd)
        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout_bytes, stderr_bytes = await proc.communicate()
        stdout = stdout_bytes.decode("utf-8", errors="replace")
        stderr = stderr_bytes.decode("utf-8", errors="replace")

        result = RuntimeExecutionResult(
            command=cmd,
            exit_code=int(proc.returncode or 0),
            stdout=stdout,
            stderr=stderr,
            workdir=str(cwd),
        )
        self._executions.append(result)

        if result.exit_code != 0:
            raise RuntimeExecutionError(cmd, result.exit_code, stdout, stderr)

        return result

    async def collect_artifacts(self) -> dict[str, Any]:
        return {
            "container_image": self._container_image,
            "executions": [asdict(execution) for execution in self._executions],
            "workdirs": [str(path) for path in self._managed_workdirs],
        }

    async def cleanup(self) -> None:
        for path in self._managed_workdirs:
            shutil.rmtree(path, ignore_errors=True)
        self._managed_workdirs.clear()
        self._is_setup = False

    def _resolve_workdir(self, workdir: Path | str | None) -> Path:
        if workdir is not None:
            return Path(workdir).resolve()
        tmp = Path(tempfile.mkdtemp(prefix="agentic-runtime-docker-")).resolve()
        self._managed_workdirs.append(tmp)
        return tmp

    def _docker_command(self, cmd: str, workdir: Path) -> Sequence[str]:
        args: list[str] = [
            "docker",
            "run",
            "--rm",
            "-w",
            "/workspace",
            "-v",
            f"{workdir}:/workspace",
            self._container_image,
        ]
        if os.name == "nt":
            args.extend(["cmd", "/c", cmd])
        else:
            args.extend(["/bin/sh", "-lc", cmd])
        return args


def create_runtime(
    execution_profile: Mapping[str, Any] | None = None,
) -> IsolatedTaskRuntime:
    """Runtime factory from execution profile settings."""

    profile = dict(execution_profile or {})
    runtime_name = str(profile.get("runtime", "subprocess")).strip().lower()

    if runtime_name == "subprocess":
        return SubprocessRuntime()
    if runtime_name == "docker":
        return DockerRuntime(container_image=profile.get("container_image"))

    raise ValueError(
        f"Unsupported runtime '{runtime_name}'. Expected 'subprocess' or 'docker'."
    )
