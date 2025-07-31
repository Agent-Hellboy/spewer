"""
Spewer - A Python debugging library for detailed code execution tracing.

This library provides utilities for tracing Python code execution with detailed
information about variables, function calls, and execution flow.

Based on the Gunicorn debug module:
https://github.com/benoitc/gunicorn/blob/master/gunicorn/debug.py

Original Gunicorn debug module:
Copyright (c) 2009-2024 Benoît Chesneau <benoitc@gunicorn.org>
Copyright (c) 2009-2015 Paul J. Davis <paul.joseph.davis@gmail.com>
"""

from .spewer import SpewContext, Spewer, spew, unspew

__version__ = "0.1.0"
__all__ = ["SpewContext", "Spewer", "spew", "unspew"]
