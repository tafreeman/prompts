"""Timing helpers."""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator


@contextmanager
def timed() -> Iterator[float]:
    """Yield start time and compute elapsed on exit."""
    start = time.perf_counter()
    try:
        yield start
    finally:
        _ = time.perf_counter() - start
