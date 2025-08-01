# Spewer

[![CI](https://github.com/Agent-Hellboy/spewer/actions/workflows/ci.yml/badge.svg)](https://github.com/Agent-Hellboy/spewer/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Agent-Hellboy/spewer/graph/badge.svg?token=O54FUXGQDM)](https://codecov.io/gh/Agent-Hellboy/spewer)
[![PyPI - Version](https://img.shields.io/pypi/v/spewer.svg)](https://pypi.org/project/spewer/)


A Python debugging library for detailed code execution tracing. This library provides utilities for tracing Python code execution with detailed information about variables, function calls, and execution flow.

## Features

- **Line-by-line execution tracing**: See exactly which lines are being executed
- **Function/method call tracing**: Trace only function and method calls without line details
- **Variable value inspection**: View the values of variables at each execution step
- **Module filtering**: Trace only specific modules or all modules
- **Context manager support**: Use with `with` statements for automatic cleanup
- **Lightweight**: Minimal overhead and dependencies

Note: Implemented to avoid using pdb manual effort. This is not going to replace pyinstrument, py-spy, and several other performance and profiling debugging tools. This is a simple tool just to counter manual effort of pdb, and it can go deep inside the dependency and print those traces in a basic format which can be done by pyinstrument and other profiling tools as well, but again this is targeting a basic pdb flaw of manual inspection. This is just an inspection tool.

## Installation

### From PyPI (when published)

```bash
pip install spewer
```

### From source

```bash
git clone https://github.com/Agent-Hellboy/spewer.git
cd spewer
pip install -e .
```

## Usage

### Basic Usage

```python
from spewer import spew, unspew

# Start tracing
spew(show_values=True)

# Your code here
def my_function():
    x = 10
    y = 20
    return x + y

result = my_function()

# Stop tracing
unspew()
```

### Using Context Manager

```python
from spewer import SpewContext

# Automatic start/stop of tracing
with SpewContext(show_values=True):
    def my_function():
        x = 10
        y = 20
        return x + y
    
    result = my_function()
```

### Module-Specific Tracing

```python
from spewer import spew, unspew

# Only trace specific modules
spew(trace_names=['my_module'], show_values=True)

# Your code here
import my_module
my_module.some_function()

unspew()
```

### Tracing Without Variable Values

```python
from spewer import SpewContext

# Trace execution without showing variable values
with SpewContext(show_values=False):
    def my_function():
        x = 10
        y = 20
        return x + y
    
    result = my_function()
```

### Function-Only Tracing

```python
from spewer import SpewContext

# Trace only function/method calls without line details
with SpewContext(functions_only=True, show_values=True):
    def my_function(x, y):
        result = x + y
        return result
    
    result = my_function(10, 20)
```

This will output:
```
__main__:15: my_function()
    args: x=10, y=20
```

## API Reference

### Functions

#### `spew(trace_names=None, show_values=False, functions_only=False)`

Install a trace hook which writes detailed logs about code execution.

**Parameters:**
- `trace_names` (Optional[List[str]]): List of module names to trace. If None, traces all modules.
- `show_values` (bool): Whether to show variable values during tracing.
- `functions_only` (bool): Whether to trace only function/method calls instead of line-by-line execution.

#### `unspew()`

Remove the trace hook installed by `spew()`.

### Classes

#### `Spewer(trace_names=None, show_values=True, functions_only=False)`

A trace hook class that provides detailed debugging information.

**Parameters:**
- `trace_names` (Optional[List[str]]): List of module names to trace. If None, traces all modules.
- `show_values` (bool): Whether to show variable values during tracing.
- `functions_only` (bool): Whether to trace only function/method calls instead of line-by-line execution.

#### `SpewContext(trace_names=None, show_values=False, functions_only=False)`

Context manager for automatic spew/unspew operations.

**Parameters:**
- `trace_names` (Optional[List[str]]): List of module names to trace. If None, traces all modules.
- `show_values` (bool): Whether to show variable values during tracing.
- `functions_only` (bool): Whether to trace only function/method calls instead of line-by-line execution.

## Example Output

When tracing with `show_values=True`, you'll see output like:

```
__main__:15: x = 10
    x=10
__main__:16: y = 20
    y=20
__main__:17: result = x + y
    x=10 y=20 result=30
__main__:18: print(f"Result: {result}")
    result=30
```

## Notes

- The library uses Python's `sys.settrace()` which can impact performance
- Only one trace hook can be active at a time
- The context manager automatically handles cleanup even if exceptions occur
- Variable inspection works best with simple variable names (avoid complex expressions)

## License

This library is based on the Gunicorn debug module released under the MIT license. The original Gunicorn debug module is Copyright (c) 2009-2024 Benoît Chesneau and Copyright (c) 2009-2015 Paul J. Davis.

### Attribution

This project builds upon the excellent debugging utilities from the Gunicorn web server project. The core tracing functionality was adapted from Gunicorn's debug module, which provides robust execution tracing capabilities. We've enhanced the original implementation with:

- **Type hints** for better IDE support
- **Context manager integration** for automatic cleanup
- **Enhanced error handling** for problematic objects
- **Improved documentation** and examples
- **Modern Python packaging** structure

The original Gunicorn debug module can be found at: https://github.com/benoitc/gunicorn/blob/master/gunicorn/debug.py

**Future Enhancements**: We plan to further enhance this library with additional features to improve usability, including more output formats, advanced filtering options, and better integration with existing debugging workflows. 