"""Spewer debugging module."""

from __future__ import annotations

import inspect
import linecache
import re
import sys
from typing import Any, Optional

_token_splitter = re.compile(r"\W+")


class Spewer:
    """A trace hook class that provides detailed debugging information."""

    def __init__(
        self, trace_names: Optional[list[str]] = None, show_values: bool = True
    ):
        """Initialize the Spewer."""
        self.trace_names = trace_names
        self.show_values = show_values

    def __call__(self, frame: Any, event: str, arg: Any) -> Spewer:
        """Trace hook callback that processes execution events."""
        if event == "line":
            lineno = frame.f_lineno

            # Get filename and handle compiled files
            if "__file__" in frame.f_globals:
                filename = frame.f_globals["__file__"]
                if filename.endswith((".pyc", ".pyo")):
                    filename = filename[:-1]
                name = frame.f_globals["__name__"]
                line = linecache.getline(filename, lineno)
            else:
                name = "[unknown]"
                try:
                    src = inspect.getsourcelines(frame)
                    line = src[lineno]
                except OSError:
                    line = f"Unknown code named [{frame.f_code.co_name}]. VM instruction #{frame.f_lasti}"

            # Check if we should trace this module
            if self.trace_names is None or name in self.trace_names:
                print(f"{name}:{lineno}: {line.rstrip()}")

                if not self.show_values:
                    return self

                # Show variable values
                details = []
                tokens = _token_splitter.split(line)

                for tok in tokens:
                    try:
                        if tok in frame.f_globals:
                            details.append(f"{tok}={frame.f_globals[tok]!r}")
                        if tok in frame.f_locals:
                            details.append(f"{tok}={frame.f_locals[tok]!r}")
                    except (AttributeError, TypeError, RecursionError):
                        # TODO: explore how to handle this better
                        pass

                if details:
                    print(f"\t{' '.join(details)}")

        return self


def spew(trace_names: Optional[list[str]] = None, show_values: bool = False) -> None:
    """Install a trace hook for detailed code execution logging."""
    sys.settrace(Spewer(trace_names, show_values))


def unspew() -> None:
    """Remove the trace hook installed by spew."""
    sys.settrace(None)


class SpewContext:
    """Context manager for automatic spew/unspew operations."""

    def __init__(
        self, trace_names: Optional[list[str]] = None, show_values: bool = False
    ):
        self.trace_names = trace_names
        self.show_values = show_values

    def __enter__(self):
        spew(self.trace_names, self.show_values)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        unspew()
