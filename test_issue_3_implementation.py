#!/usr/bin/env python3
"""
Test script to demonstrate the new return and exception event tracing.
"""

from spewer import SpewContext, spew, unspew

def test_function_with_return():
    """Test function that returns a value."""
    x = 10
    y = 20
    result = x + y
    return result

def test_function_with_exception():
    """Test function that raises an exception."""
    x = 10
    y = 0
    result = x / y  # This will raise ZeroDivisionError
    return result

def test_function_with_try_except():
    """Test function with exception handling."""
    try:
        x = 10
        y = 0
        result = x / y
        return result
    except ZeroDivisionError as e:
        print(f"Caught exception: {e}")
        return None

def test_nested_functions():
    """Test nested function calls."""
    def inner_function(x, y):
        return x * y
    
    def outer_function(a, b):
        result = inner_function(a, b)
        return result + 10
    
    return outer_function(5, 3)

def main():
    """Main function to test return and exception events."""
    
    print("=== Testing Return Events (functions_only=True) ===")
    with SpewContext(functions_only=True, show_values=True):
        result = test_function_with_return()
        print(f"Result: {result}")
    
    print("\n=== Testing Exception Events (functions_only=True) ===")
    try:
        with SpewContext(functions_only=True, show_values=True):
            result = test_function_with_exception()
            print(f"Result: {result}")
    except ZeroDivisionError as e:
        print(f"Exception caught: {e}")
    
    print("\n=== Testing Exception Handling (functions_only=True) ===")
    with SpewContext(functions_only=True, show_values=True):
        result = test_function_with_try_except()
        print(f"Result: {result}")
    
    print("\n=== Testing Nested Functions (functions_only=True) ===")
    with SpewContext(functions_only=True, show_values=True):
        result = test_nested_functions()
        print(f"Result: {result}")
    
    print("\n=== Testing Return Events (line-by-line) ===")
    with SpewContext(functions_only=False, show_values=True):
        result = test_function_with_return()
        print(f"Result: {result}")
    
    print("\n=== Testing with trace_returns=False ===")
    with SpewContext(functions_only=True, show_values=True, trace_returns=False):
        result = test_function_with_return()
        print(f"Result: {result}")
    
    print("\n=== Testing with trace_exceptions=False ===")
    try:
        with SpewContext(functions_only=True, show_values=True, trace_exceptions=False):
            result = test_function_with_exception()
            print(f"Result: {result}")
    except ZeroDivisionError as e:
        print(f"Exception caught: {e}")

if __name__ == "__main__":
    main()
