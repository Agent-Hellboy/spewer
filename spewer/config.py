"""Configuration module for spewer debugging library."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class SpewConfig:
    """Configuration for spewer debugging."""

    trace_names: Optional[list[str]] = None
    show_values: bool = True
    functions_only: bool = False

    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.trace_names is not None and not isinstance(self.trace_names, list):
            msg = "trace_names must be a list or None"
            raise TypeError(msg)

        if not isinstance(self.show_values, bool):
            msg = "show_values must be a boolean"
            raise TypeError(msg)

        if not isinstance(self.functions_only, bool):
            msg = "functions_only must be a boolean"
            raise TypeError(msg)
