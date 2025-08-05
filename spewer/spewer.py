"""Main spewer debugging module."""

from __future__ import annotations

import sys
from typing import Optional

from .config import SpewConfig
from .trace import TraceHook


def spew(
    trace_names: Optional[list[str]] = None,
    show_values: bool = False,
    functions_only: bool = False,
) -> None:
    """Install a trace hook for detailed code execution logging."""
    config = SpewConfig(
        trace_names=trace_names,
        show_values=show_values,
        functions_only=functions_only,
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
    ):
        self.config = SpewConfig(
            trace_names=trace_names,
            show_values=show_values,
            functions_only=functions_only,
        )

    def __enter__(self):
        spew(
            self.config.trace_names,
            self.config.show_values,
            self.config.functions_only,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        unspew()
