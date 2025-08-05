"""Main spewer debugging module."""

from __future__ import annotations

import sys
from typing import Optional

from .config import SpewConfig
from .trace import TraceHook


class Spewer:
    """A trace hook class that provides detailed debugging information."""

    def __init__(
        self, 
        trace_names: Optional[list[str]] = None, 
        show_values: bool = True, 
        functions_only: bool = False,
        debug_mode: bool = False
    ):
        """Initialize the Spewer."""
        config = SpewConfig(
            trace_names=trace_names,
            show_values=show_values,
            functions_only=functions_only,
            debug_mode=debug_mode
        )
        self.trace_hook = TraceHook(config)

    def __call__(self, frame, event, arg):
        """Delegate to the trace hook."""
        return self.trace_hook(frame, event, arg)


def spew(
    trace_names: Optional[list[str]] = None, 
    show_values: bool = False, 
    functions_only: bool = False,
    debug_mode: bool = False
) -> None:
    """Install a trace hook for detailed code execution logging."""
    config = SpewConfig(
        trace_names=trace_names,
        show_values=show_values,
        functions_only=functions_only,
        debug_mode=debug_mode
    )
    sys.settrace(TraceHook(config))


def unspew() -> None:
    """Remove the trace hook installed by spew."""
    sys.settrace(None)


class SpewContext:
    """Context manager for automatic spew/unspew operations."""

    def __init__(
        self, 
        trace_names: Optional[list[str]] = None, 
        show_values: bool = False, 
        functions_only: bool = False,
        debug_mode: bool = False
    ):
        self.config = SpewConfig(
            trace_names=trace_names,
            show_values=show_values,
            functions_only=functions_only,
            debug_mode=debug_mode
        )

    def __enter__(self):
        spew(
            self.config.trace_names,
            self.config.show_values,
            self.config.functions_only,
            self.config.debug_mode
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        unspew()
