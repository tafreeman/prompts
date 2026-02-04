"""Lightweight pytest helper to run async test functions when pytest-asyncio
is not installed in the environment.

This shim is intentionally small: it detects coroutine test functions and
executes them using asyncio.run so the test-suite can be executed in CI or
developer environments without the full async test plugin installed.

Note: If you have pytest-asyncio installed, this file is harmless.
"""
import inspect
import asyncio
from pathlib import Path

# Load .env file if it exists (for API keys, etc.)
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv not installed, skip


def pytest_pyfunc_call(pyfuncitem):
    """Run coroutine test functions with asyncio.run when necessary.

    Returning True tells pytest that we've executed the test and it should
    not attempt to run it again.
    """
    testfunc = pyfuncitem.obj
    if inspect.iscoroutinefunction(testfunc):
        # Resolve fixtures/arguments via the pytest item and execute
        kwargs = {name: pyfuncitem.funcargs[name] for name in pyfuncitem._fixtureinfo.argnames}
        asyncio.run(testfunc(**kwargs))
        return True

    # For non-coroutine functions, let pytest handle execution normally.
    return None
