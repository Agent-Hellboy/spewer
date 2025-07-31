#!/usr/bin/env python3
"""
Example usage of the spewer debugging library.
"""

from spewer import spew, unspew, SpewContext


def example_function():
    """A simple function to demonstrate spewer functionality."""
    x = 10
    y = 20
    result = x + y
    print(f"Result: {result}")
    return result


def main():
    """Main function demonstrating different ways to use spewer."""
    
    print("=== Basic spew usage ===")
    spew(show_values=True)
    example_function()
    unspew()
    
    print("\n=== Spew with specific module tracing ===")
    spew(trace_names=['__main__'], show_values=True)
    example_function()
    unspew()
    
    print("\n=== Using context manager ===")
    with SpewContext(show_values=True):
        example_function()
    
    print("\n=== Spew without variable values ===")
    with SpewContext(show_values=False):
        example_function()


if __name__ == "__main__":
    main() 