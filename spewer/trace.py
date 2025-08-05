"""Trace module for spewer debugging library."""

from __future__ import annotations

import inspect
import linecache
import re
from typing import Any

from .config import SpewConfig  # noqa: TC001

_token_splitter = re.compile(r"\W+")


class TraceHook:
    """Core trace hook implementation."""

    def __init__(self, config: SpewConfig):
        """Initialize the trace hook with configuration."""
        self.config = config

    def __call__(self, frame: Any, event: str, arg: Any) -> TraceHook:
        """Trace hook callback that processes execution events."""
        if self.config.functions_only and event == "call":
            self._handle_function_call(frame)
        elif not self.config.functions_only and event == "line":
            self._handle_line_execution(frame)

        return self

    def _handle_function_call(self, frame: Any) -> None:
        """Handle function call events."""
        lineno = frame.f_lineno
        func_name = frame.f_code.co_name

        # Get filename and handle compiled files
        if "__file__" in frame.f_globals:
            filename = frame.f_globals["__file__"]
            if filename.endswith((".pyc", ".pyo")):
                filename = filename[:-1]
            name = frame.f_globals["__name__"]
        else:
            name = "[unknown]"
            filename = "[unknown]"

        # Check if we should trace this module
        if self.config.trace_names is None or name in self.config.trace_names:
            print(f"{name}:{lineno}: {func_name}()")

            if self.config.show_values:
                self._show_function_args(frame)

    def _handle_line_execution(self, frame: Any) -> None:
        """Handle line-by-line execution events."""
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
        if self.config.trace_names is None or name in self.config.trace_names:
            print(f"{name}:{lineno}: {line.rstrip()}")

            if not self.config.show_values:
                return

            self._show_variable_values(frame, line)

    def _show_function_args(self, frame: Any) -> None:
        """Show function arguments if available."""
        if frame.f_locals:
            args = []
            for key, value in frame.f_locals.items():
                if not key.startswith("__"):
                    try:
                        args.append(f"{key}={value!r}")
                    except (AttributeError, TypeError, RecursionError):
                        args.append(f"{key}=<{type(value).__name__} object>")
            if args:
                print(f"\targs: {', '.join(args)}")

    def _show_variable_values(self, frame: Any, line: str) -> None:
        """Show variable values for line execution."""
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
