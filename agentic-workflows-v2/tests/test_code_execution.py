"""Tests for CodeExecutionTool with sandboxing."""

from __future__ import annotations

import pytest

from agentic_v2.tools.builtin.code_execution import CodeExecutionTool


class TestCodeSafetyChecker:
    """Tests for _check_code_safety blocklist."""

    def test_dangerous_import_blocked(self) -> None:
        """import subprocess is blocked."""
        tool = CodeExecutionTool(sandbox=True)
        result = tool._check_code_safety("import subprocess")
        assert result is not None
        assert "subprocess" in result

    def test_dangerous_from_import_blocked(self) -> None:
        """from subprocess import run is blocked."""
        tool = CodeExecutionTool(sandbox=True)
        result = tool._check_code_safety("from subprocess import run")
        assert result is not None
        assert "subprocess" in result

    def test_dangerous_pattern_os_system_blocked(self) -> None:
        """os.system is blocked."""
        tool = CodeExecutionTool(sandbox=True)
        result = tool._check_code_safety("os.system('ls')")
        assert result is not None
        assert "os.system" in result

    def test_open_call_blocked(self) -> None:
        """open() is blocked in sandbox mode."""
        tool = CodeExecutionTool(sandbox=True)
        result = tool._check_code_safety("f = open('file.txt')")
        assert result is not None
        assert "open(" in result

    def test_pathlib_blocked(self) -> None:
        """pathlib.Path() is blocked."""
        tool = CodeExecutionTool(sandbox=True)
        result = tool._check_code_safety("pathlib.Path('/etc/passwd')")
        assert result is not None
        assert "pathlib.Path(" in result

    def test_safe_code_passes(self) -> None:
        """Regular math code passes safety check."""
        tool = CodeExecutionTool(sandbox=True)
        result = tool._check_code_safety("x = 2 + 2\nprint(x)")
        assert result is None

    def test_safe_import_passes(self) -> None:
        """import math is allowed."""
        tool = CodeExecutionTool(sandbox=True)
        result = tool._check_code_safety("import math\nprint(math.pi)")
        assert result is None

    def test_sandbox_disabled_allows_all(self) -> None:
        """When sandbox=False, no code is blocked."""
        tool = CodeExecutionTool(sandbox=False)
        result = tool._check_code_safety("import subprocess; subprocess.run(['ls'])")
        assert result is None

    def test_syntax_error_passes_safety(self) -> None:
        """Syntax errors pass safety check (caught at execution time)."""
        tool = CodeExecutionTool(sandbox=True)
        result = tool._check_code_safety("def foo(:")
        assert result is None

    def test_socket_import_blocked(self) -> None:
        """import socket is blocked."""
        tool = CodeExecutionTool(sandbox=True)
        result = tool._check_code_safety("import socket")
        assert result is not None
        assert "socket" in result

    def test_importlib_pattern_blocked(self) -> None:
        """importlib pattern is blocked."""
        tool = CodeExecutionTool(sandbox=True)
        result = tool._check_code_safety("importlib.import_module('os')")
        assert result is not None


class TestCodeExecution:
    """Tests for CodeExecutionTool.execute."""

    @pytest.mark.asyncio
    async def test_simple_print(self) -> None:
        """print('hello') captures stdout."""
        tool = CodeExecutionTool(sandbox=True)
        result = await tool.execute("print('hello')", timeout=10.0)
        assert result.success
        assert "hello" in result.data["stdout"]

    @pytest.mark.asyncio
    async def test_result_variable_captured(self) -> None:
        """Variable named 'result' is captured in output."""
        tool = CodeExecutionTool(sandbox=True)
        result = await tool.execute("result = [1, 2, 3]", timeout=10.0)
        assert result.success
        assert result.data["result"] is not None
        assert "1" in result.data["result"]

    @pytest.mark.asyncio
    async def test_syntax_error_reported(self) -> None:
        """Syntax error in user code returns structured error."""
        tool = CodeExecutionTool(sandbox=True)
        result = await tool.execute("def foo(:", timeout=10.0)
        assert not result.success
        assert result.error is not None

    @pytest.mark.asyncio
    async def test_runtime_error_reported(self) -> None:
        """1/0 returns error with traceback."""
        tool = CodeExecutionTool(sandbox=True)
        result = await tool.execute("x = 1/0", timeout=10.0)
        assert not result.success
        assert "ZeroDivisionError" in result.error

    @pytest.mark.asyncio
    async def test_blocked_import_returns_safety_error(self) -> None:
        """import subprocess returns safety error without executing."""
        tool = CodeExecutionTool(sandbox=True)
        result = await tool.execute("import subprocess", timeout=10.0)
        assert not result.success
        assert "Blocked" in result.error

    @pytest.mark.asyncio
    async def test_safe_import_allowed(self) -> None:
        """import math is allowed and works."""
        tool = CodeExecutionTool(sandbox=True)
        result = await tool.execute("import math\nprint(math.pi)", timeout=10.0)
        assert result.success
        assert "3.14" in result.data["stdout"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(15)
    async def test_timeout_handling(self) -> None:
        """Long-running code is killed after timeout."""
        tool = CodeExecutionTool(sandbox=False)
        result = await tool.execute(
            "import time\ntime.sleep(60)",
            timeout=2.0,
        )
        assert not result.success
        assert "timed out" in result.error

    @pytest.mark.asyncio
    async def test_multiple_print_statements(self) -> None:
        """Multiple prints are all captured."""
        tool = CodeExecutionTool(sandbox=True)
        result = await tool.execute("print('a')\nprint('b')\nprint('c')", timeout=10.0)
        assert result.success
        assert "a" in result.data["stdout"]
        assert "b" in result.data["stdout"]
        assert "c" in result.data["stdout"]

    @pytest.mark.asyncio
    async def test_tool_properties(self) -> None:
        """Tool has correct name, description, and tier."""
        tool = CodeExecutionTool()
        assert tool.name == "execute_python"
        assert "Python" in tool.description
        assert tool.tier == 0
        assert len(tool.examples) > 0
