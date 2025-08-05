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
    debug_mode: bool = False
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.trace_names is not None and not isinstance(self.trace_names, list):
            raise ValueError("trace_names must be a list or None")
        
        if not isinstance(self.show_values, bool):
            raise ValueError("show_values must be a boolean")
        
        if not isinstance(self.functions_only, bool):
            raise ValueError("functions_only must be a boolean")
        
        if not isinstance(self.debug_mode, bool):
            raise ValueError("debug_mode must be a boolean")
