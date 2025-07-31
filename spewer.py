"""
Spewer - A Python debugging library for detailed code execution tracing.

This module provides utilities for tracing Python code execution with detailed
information about variables, function calls, and execution flow.

Based on the Gunicorn debug module:
https://github.com/benoitc/gunicorn/blob/master/gunicorn/debug.py

Original Gunicorn debug module:
Copyright (c) 2009-2024 Benoît Chesneau <benoitc@gunicorn.org>
Copyright (c) 2009-2015 Paul J. Davis <paul.joseph.davis@gmail.com>
"""

import sys
import linecache
import re
import inspect
from typing import Optional, List, Any

__version__ = "0.1.0"
__all__ = ['Spewer', 'spew', 'unspew']

_token_splitter = re.compile(r'\W+')


class Spewer:
    """
    A trace hook class that provides detailed debugging information.
    
    This class can be used to trace Python code execution, showing line-by-line
    execution with variable values and function calls.
    """
    
    def __init__(self, trace_names: Optional[List[str]] = None, show_values: bool = True):
        """
        Initialize the Spewer.
        
        Args:
            trace_names: List of module names to trace. If None, traces all modules.
            show_values: Whether to show variable values during tracing.
        """
        self.trace_names = trace_names
        self.show_values = show_values

    def __call__(self, frame: Any, event: str, arg: Any) -> 'Spewer':
        """
        Trace hook callback that processes execution events.
        
        Args:
            frame: The current execution frame
            event: The event type ('line', 'call', 'return', etc.)
            arg: Additional event arguments
            
        Returns:
            self for method chaining
        """
        if event == 'line':
            lineno = frame.f_lineno
            
            # Get filename and handle compiled files
            if '__file__' in frame.f_globals:
                filename = frame.f_globals['__file__']
                if filename.endswith(('.pyc', '.pyo')):
                    filename = filename[:-1]
                name = frame.f_globals['__name__']
                line = linecache.getline(filename, lineno)
            else:
                name = '[unknown]'
                try:
                    src = inspect.getsourcelines(frame)
                    line = src[lineno]
                except OSError:
                    line = f'Unknown code named [{frame.f_code.co_name}]. VM instruction #{frame.f_lasti}'
            
            # Check if we should trace this module
            if self.trace_names is None or name in self.trace_names:
                print(f'{name}:{lineno}: {line.rstrip()}')
                
                if not self.show_values:
                    return self
                
                # Show variable values
                details = []
                tokens = _token_splitter.split(line)
                
                for tok in tokens:
                    try:
                        if tok in frame.f_globals:
                            details.append(f'{tok}={repr(frame.f_globals[tok])}')
                        if tok in frame.f_locals:
                            details.append(f'{tok}={repr(frame.f_locals[tok])}')
                    except (AttributeError, TypeError, RecursionError):
                        # TODO: explore how to handle this better
                        pass
                
                if details:
                    print(f"\t{' '.join(details)}")
        
        return self


def spew(trace_names: Optional[List[str]] = None, show_values: bool = False) -> None:
    """
    Install a trace hook which writes incredibly detailed logs about what code is being executed.
    
    Args:
        trace_names: List of module names to trace. If None, traces all modules.
        show_values: Whether to show variable values during tracing.
    """
    sys.settrace(Spewer(trace_names, show_values))


def unspew() -> None:
    """Remove the trace hook installed by spew."""
    sys.settrace(None)


class SpewContext:
    """
    Context manager for automatic spew/unspew operations.
    
    Usage:
        with SpewContext():
            # Code to trace
            pass
    """
    
    def __init__(self, trace_names: Optional[List[str]] = None, show_values: bool = False):
        self.trace_names = trace_names
        self.show_values = show_values
    
    def __enter__(self):
        spew(self.trace_names, self.show_values)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        unspew()


__all__.append('SpewContext') 