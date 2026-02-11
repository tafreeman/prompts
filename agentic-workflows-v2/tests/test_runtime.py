"""Tests for runtime abstraction and factory behavior."""

from __future__ import annotations

from pathlib import Path

import pytest

from agentic_v2.engine.runtime import (
    DockerRuntime,
    RuntimeExecutionError,
    SubprocessRuntime,
    create_runtime,
)


@pytest.mark.asyncio
async def test_subprocess_runtime_echo():
    runtime = SubprocessRuntime()
    await runtime.setup()
    try:
        result = await runtime.execute("echo hello")
        assert "hello" in result.stdout
    finally:
        await runtime.cleanup()


@pytest.mark.asyncio
async def test_subprocess_runtime_failure():
    runtime = SubprocessRuntime()
    await runtime.setup()
    try:
        with pytest.raises(RuntimeExecutionError) as exc:
            await runtime.execute("echo boom >&2; exit 7")
        assert exc.value.exit_code == 7
        assert "boom" in exc.value.stderr
    finally:
        await runtime.cleanup()


@pytest.mark.asyncio
async def test_subprocess_runtime_cleanup():
    runtime = SubprocessRuntime()
    await runtime.setup()
    await runtime.execute("echo cleanup")

    artifacts = await runtime.collect_artifacts()
    assert artifacts["workdirs"], "Expected at least one managed workdir"

    workdir = Path(artifacts["workdirs"][0])
    assert workdir.exists()

    await runtime.cleanup()
    assert not workdir.exists()


@pytest.mark.asyncio
async def test_docker_runtime_not_available(monkeypatch):
    monkeypatch.setattr("agentic_v2.engine.runtime.shutil.which", lambda _name: None)
    runtime = DockerRuntime()
    with pytest.raises(RuntimeError, match="Docker runtime requested"):
        await runtime.setup()


def test_runtime_factory_default_subprocess():
    runtime = create_runtime()
    assert isinstance(runtime, SubprocessRuntime)


def test_runtime_factory_docker_opt_in():
    runtime = create_runtime({"runtime": "docker"})
    assert isinstance(runtime, DockerRuntime)
