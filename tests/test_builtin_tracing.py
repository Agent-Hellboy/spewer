"""Tests for built-in function tracing."""

import sys
from io import StringIO

from spewer import spew, unspew


def test_builtin_functions_traced_with_functions_only():
    """Test that built-in functions are traced when functions_only=True."""
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    try:
        spew(functions_only=True)
        len([1, 2, 3])
        max([1, 5, 3])
        min([1, 2, 3])
        unspew()
    finally:
        # Restore stdout
        sys.stdout = old_stdout
    
    output = captured_output.getvalue()
    
    # Verify built-ins were traced
    assert "len()" in output, "len() should be traced"
    assert "max()" in output, "max() should be traced"
    assert "min()" in output, "min() should be traced"


def test_builtin_and_user_functions_traced():
    """Test that both built-in and user-defined functions are traced."""
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()
    
    def custom_function():
        return len([1, 2])
    
    try:
        spew(functions_only=True)
        result = custom_function()
        unspew()
    finally:
        sys.stdout = old_stdout
    
    output = captured_output.getvalue()
    
    # Both types should be traced
    assert "len()" in output, "Built-in len() should be traced"
    assert "custom_function()" in output, "User function should be traced"
