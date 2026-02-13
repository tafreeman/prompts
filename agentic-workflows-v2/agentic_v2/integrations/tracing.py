"""Concrete trace adapter implementations."""

import json
import logging
from pathlib import Path
from typing import Optional

from .base import TraceAdapter, CanonicalEvent


logger = logging.getLogger(__name__)


class ConsoleTraceAdapter(TraceAdapter):
    """Trace adapter that emits events to console/logging.

    Useful for development and debugging. Events are logged at INFO level.
    """

    def __init__(self, pretty_print: bool = True):
        """Initialize console trace adapter.

        Args:
            pretty_print: If True, format JSON output with indentation
        """
        self.pretty_print = pretty_print

    def emit(self, event: CanonicalEvent) -> None:
        """Emit event to console via logging."""
        if self.pretty_print:
            event_str = json.dumps(event.to_dict(), indent=2, default=str)
        else:
            event_str = event.to_json()

        logger.info(f"[TRACE] {event.type} | {event_str}")


class FileTraceAdapter(TraceAdapter):
    """Trace adapter that appends events to a JSON lines file.

    Each event is written as a single-line JSON object, making it easy to
    process with tools like jq or stream into analysis pipelines.
    """

    def __init__(self, file_path: Path, buffer_size: int = 1):
        """Initialize file trace adapter.

        Args:
            file_path: Path to the output file (will be created if doesn't exist)
            buffer_size: Number of events to buffer before flushing (default: 1 = no buffering)
        """
        self.file_path = Path(file_path)
        self.buffer_size = buffer_size
        self._buffer = []

        # Ensure parent directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event: CanonicalEvent) -> None:
        """Emit event to file."""
        self._buffer.append(event.to_json())

        if len(self._buffer) >= self.buffer_size:
            self._flush()

    def _flush(self) -> None:
        """Flush buffered events to file."""
        if not self._buffer:
            return

        with open(self.file_path, 'a', encoding='utf-8') as f:
            for line in self._buffer:
                f.write(line + '\n')

        self._buffer.clear()

    def __del__(self):
        """Ensure buffer is flushed on cleanup."""
        try:
            self._flush()
        except Exception:
            pass  # Suppress errors during cleanup


class CompositeTraceAdapter(TraceAdapter):
    """Trace adapter that forwards events to multiple adapters.

    Useful for emitting to console and file simultaneously, or to multiple backends.
    """

    def __init__(self, *adapters: TraceAdapter):
        """Initialize composite adapter.

        Args:
            *adapters: One or more trace adapters to forward events to
        """
        self.adapters = list(adapters)

    def emit(self, event: CanonicalEvent) -> None:
        """Emit event to all registered adapters."""
        for adapter in self.adapters:
            try:
                adapter.emit(event)
            except Exception as e:
                logger.error(f"Error emitting event to {type(adapter).__name__}: {e}")


class NullTraceAdapter(TraceAdapter):
    """No-op trace adapter that discards events.

    Useful as a default when tracing is disabled.
    """

    def emit(self, event: CanonicalEvent) -> None:
        """Discard event."""
        pass
