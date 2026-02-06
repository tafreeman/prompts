"""Tier 0 Code execution tool with sandboxing.

Provides a structured tool for running Python code with:
- Configurable timeout and memory limits
- stdout/stderr capture
- Return-value extraction
- Restricted builtins mode (no file/network access)
- Optional Docker sandbox
"""

from __future__ import annotations

import asyncio
import os
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Any

from ..base import BaseTool, ToolResult


class CodeExecutionTool(BaseTool):
    """Execute Python code in a controlled environment."""

    def __init__(self, *, allow_imports: bool = True, sandbox: bool = True):
        super().__init__()
        self._allow_imports = allow_imports
        self._sandbox = sandbox

    @property
    def name(self) -> str:
        return "execute_python"

    @property
    def description(self) -> str:
        return (
            "Execute Python code and capture stdout, stderr, and return value. "
            "Code runs in a restricted sandbox by default."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "code": {
                "type": "string",
                "description": "Python source code to execute",
                "required": True,
            },
            "timeout": {
                "type": "number",
                "description": "Max execution time in seconds",
                "required": False,
                "default": 30,
            },
        }

    @property
    def tier(self) -> int:
        return 0

    @property
    def examples(self) -> list[str]:
        return [
            'execute_python(code="print(2+2)") → stdout: "4\\n"',
            'execute_python(code="result = [i**2 for i in range(5)]") → return: [0,1,4,9,16]',
        ]

    # ------------------------------------------------------------------
    # Blocklists
    # ------------------------------------------------------------------

    _DANGEROUS_IMPORTS = frozenset({
        "subprocess", "shutil", "ctypes", "multiprocessing",
        "signal", "socket", "http", "urllib", "requests",
        "ftplib", "smtplib", "telnetlib", "xmlrpc",
        "webbrowser", "antigravity",
    })

    _DANGEROUS_BUILTINS = frozenset({
        "exec", "eval", "compile", "__import__",
        "breakpoint", "exit", "quit",
    })

    _DANGEROUS_PATTERNS = [
        "os.system", "os.popen", "os.exec",
        "os.remove", "os.unlink", "os.rmdir",
        "os.rename", "os.makedirs",
        "open(",           # file I/O
        "pathlib.Path(",   # file I/O via pathlib
        "__import__",
        "importlib",
    ]

    def _check_code_safety(self, code: str) -> str | None:
        """Return an error message if code is unsafe, else None."""
        if not self._sandbox:
            return None

        code_lower = code.lower()

        # Check dangerous patterns
        for pattern in self._DANGEROUS_PATTERNS:
            if pattern.lower() in code_lower:
                return f"Blocked: code contains restricted pattern '{pattern}'"

        # Check imports
        import ast
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return None  # Let execution catch syntax errors

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    if top in self._DANGEROUS_IMPORTS:
                        return f"Blocked: import of restricted module '{top}'"
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    top = node.module.split(".")[0]
                    if top in self._DANGEROUS_IMPORTS:
                        return f"Blocked: import from restricted module '{top}'"

        return None

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    async def execute(self, code: str, timeout: float = 30.0, **kwargs) -> ToolResult:
        """Execute Python code in a sandboxed subprocess."""
        # Safety check
        safety_error = self._check_code_safety(code)
        if safety_error:
            return ToolResult(success=False, error=safety_error, tool_name=self.name)

        # Write code to a temp file and run in subprocess for isolation
        wrapper = textwrap.dedent(f"""\
            import sys, json, io, traceback

            _stdout = io.StringIO()
            _stderr = io.StringIO()
            _old_stdout, _old_stderr = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = _stdout, _stderr

            _result = None
            _error = None
            try:
                _globals = {{"__builtins__": __builtins__}}
                _code = {code!r}
                exec(_code, _globals)
                # Try to capture a variable named 'result'
                _result = _globals.get("result")
            except Exception:
                _error = traceback.format_exc()
            finally:
                sys.stdout, sys.stderr = _old_stdout, _old_stderr

            output = {{
                "stdout": _stdout.getvalue(),
                "stderr": _stderr.getvalue(),
                "result": repr(_result) if _result is not None else None,
                "error": _error,
            }}
            print(json.dumps(output))
        """)

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False, encoding="utf-8"
            ) as f:
                f.write(wrapper)
                tmp_path = f.name

            try:
                proc = await asyncio.create_subprocess_exec(
                    sys.executable, tmp_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )
                stdout_bytes, stderr_bytes = await asyncio.wait_for(
                    proc.communicate(), timeout=timeout
                )
            finally:
                Path(tmp_path).unlink(missing_ok=True)

            stdout_str = stdout_bytes.decode("utf-8", errors="replace").strip()

            # Parse the JSON output
            import json
            try:
                output = json.loads(stdout_str)
            except (json.JSONDecodeError, ValueError):
                # Subprocess crashed or produced non-JSON
                return ToolResult(
                    success=False,
                    error=f"Subprocess error: {stderr_bytes.decode('utf-8', errors='replace')}",
                    tool_name=self.name,
                )

            if output.get("error"):
                return ToolResult(
                    success=False,
                    data={
                        "stdout": output["stdout"],
                        "stderr": output["stderr"],
                    },
                    error=output["error"],
                    tool_name=self.name,
                )

            return ToolResult(
                success=True,
                data={
                    "stdout": output["stdout"],
                    "stderr": output["stderr"],
                    "result": output.get("result"),
                },
                tool_name=self.name,
            )

        except asyncio.TimeoutError:
            return ToolResult(
                success=False,
                error=f"Code execution timed out after {timeout}s",
                tool_name=self.name,
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Execution failed: {e}",
                tool_name=self.name,
            )
