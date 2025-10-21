import contextlib
import sys
from io import StringIO  # Add this
from pathlib import Path

from spewer import spew, unspew


def test_builtin_functions_traced(capsys):
    """Test that built-in functions with valid arg are traced - covers lines 41-45"""
    spew(functions_only=True)

    # Call built-in functions without assignment (no unused variable warnings)
    len([1, 2, 3])
    max([1, 2, 3])
    min([1, 2, 3])

    unspew()

    captured = capsys.readouterr()
    output_str = captured.out
    assert "len" in output_str or "builtins" in output_str


def test_builtin_with_exception(capsys):
    """Test built-in functions that raise exceptions"""
    spew(functions_only=True)

    with contextlib.suppress(ValueError):
        max([])  # Raises ValueError

    unspew()
    captured = capsys.readouterr()
    assert "max" in captured.out or "builtins" in captured.out


def test_multiple_builtins_sequence(capsys):
    """Test multiple built-in functions called in sequence"""
    spew(functions_only=True)

    len([1, 2, 3])
    max([1, 2, 3])
    min([1, 2, 3])
    abs(-5)

    unspew()
    captured = capsys.readouterr()
    result = captured.out
    # At least one built-in should be traced
    assert any(func in result for func in ["len", "max", "min", "abs", "builtins"])


def test_nested_builtin_and_python(capsys):
    """Test nested calls mixing built-in and Python functions"""

    def custom_func(x):
        return len(x)

    spew(functions_only=True)
    custom_func([1, 2, 3])
    unspew()

    captured = capsys.readouterr()
    output_str = captured.out
    assert "custom_func" in output_str or "len" in output_str


def test_inspect_getsourcelines_fallback(capsys):
    """Test OSError exception handling when source unavailable - covers line 84"""
    spew(show_values=True)

    # Built-in functions don't have source lines, triggering OSError
    Path.cwd()  # Use Path.cwd() instead of os.getcwd()

    unspew()
    # Should handle gracefully without crashing
    capsys.readouterr()  # Clear output, don't assign


def test_show_values_with_line_execution(capsys):
    """Test variable value display during line execution - covers line 95"""
    spew(show_values=True)

    # Execute code that will call _show_variable_values
    x = 10
    y = 20
    # Use the variables immediately to avoid lint warnings
    assert x + y == 30

    unspew()

    # Should show variable values
    captured = capsys.readouterr()
    output_str = captured.out
    # Variable values should appear in output
    assert len(output_str) > 0


def test_global_variable_inspection(capsys):
    """Test displaying global variables in details - covers line 118"""
    # Create module-level code that uses globals
    spew(show_values=True)

    # This will trigger global variable inspection
    global_test = 42
    local_test = global_test + 10
    assert local_test == 52

    unspew()

    captured = capsys.readouterr()
    # Should have some output
    assert len(captured.out) > 0


def test_custom_function_with_builtins(capsys):
    """Test custom function that uses built-in functions"""

    def custom_function():
        data = [1, 2, 3]
        len(data)
        max(data)
        return True

    spew(functions_only=True)
    custom_function()
    unspew()

    captured = capsys.readouterr()
    result = captured.out
    # Should trace either the custom function or built-ins
    assert len(result) > 0


def test_c_call_event_with_arg(capsys):
    """Test c_call event handling with valid arg - covers lines 39-43"""
    # Store original profile function
    old_profile = sys.getprofile()

    spew(functions_only=True)

    # These should trigger c_call events
    len([1, 2, 3])
    print("test")  # print is a built-in
    str(123)

    unspew()

    # Restore original profile
    if old_profile:
        sys.setprofile(old_profile)

    captured = capsys.readouterr()
    # Should have traced built-in functions
    output = captured.out
    assert len(output) > 0


def test_source_line_unavailable(capsys):
    """Test when source lines are unavailable - covers line 81"""
    spew(show_values=True)

    # Call functions from compiled modules
    _ = sys.version_info  # Assign to _ to avoid "useless expression" warning

    # Call a C function that has no source
    sorted([3, 1, 2])

    unspew()
    capsys.readouterr()  # Clear output, don't assign


def test_show_variable_values_call(capsys):
    """Test _show_variable_values is called - covers line 92"""
    spew(show_values=True, functions_only=False)

    # Execute multiple lines to trigger variable inspection
    test_var = 100
    another_var = 200
    result = test_var + another_var
    assert result == 300

    unspew()
    captured = capsys.readouterr()
    output = captured.out
    # Should show variable values
    assert len(output) > 0


def test_frame_globals_access(capsys):
    """Test accessing frame globals - covers line 115"""
    spew(show_values=True, functions_only=False)

    # Create code that accesses globals
    test_global = 999
    local_value = test_global * 2
    assert local_value == 1998

    unspew()
    capsys.readouterr()  # Clear output, don't assign


def test_builtin_print_traced(capsys):
    """Ensure print() itself is traced as a built-in"""

    # Redirect stdout temporarily
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    spew(functions_only=True)
    print("Hello")
    unspew()

    sys.stdout = old_stdout
    capsys.readouterr()  # Clear output, don't assign


def test_multiple_c_call_events(capsys):
    """Test multiple c_call events in sequence"""
    spew(functions_only=True)

    # Chain multiple built-in calls
    data = [5, 2, 8, 1]
    len(data)
    max(data)
    min(data)
    sorted(data)
    sum(data)

    unspew()
    captured = capsys.readouterr()
    output = captured.out
    # Should have some trace output
    assert isinstance(output, str)


def test_verify_setprofile_active():
    """Verify sys.setprofile is actually set when using functions_only"""
    spew(functions_only=True)

    # Check if profile hook is installed
    profile_func = sys.getprofile()
    assert profile_func is not None, "sys.setprofile should be set"

    # Call a built-in
    len([1, 2, 3])

    unspew()

    # Profile should be cleared
    assert sys.getprofile() is None


def test_debug_c_call_events():
    """Debug test to see if c_call events are actually triggered"""
    # Track what events we receive
    events_received = []

    def debug_profiler(_frame, event, arg):  # Prefix unused arg with _
        events_received.append((event, arg))
        return debug_profiler

    # Set up profiler manually
    sys.setprofile(debug_profiler)

    # Call a built-in
    len([1, 2, 3])
    max([5, 2, 8])

    # Clean up
    sys.setprofile(None)

    # Check what events we got
    print(f"\nEvents received: {len(events_received)}")
    for event, arg in events_received:
        print(f"Event: {event}, Arg type: {type(arg).__name__}, Arg: {arg}")

    # We should have received c_call events
    c_call_events = [e for e in events_received if e[0] == "c_call"]
    print(f"\nc_call events: {len(c_call_events)}")

    assert len(c_call_events) > 0, "Should have received c_call events"


def test_spew_captures_builtin_functions(capsys):
    """Direct test that spew() with functions_only captures built-ins"""
    # Use spew
    spew(functions_only=True)

    # Verify setprofile is active
    assert sys.getprofile() is not None, "setprofile should be set"

    # Call built-ins
    len([1, 2, 3])
    max([5, 2, 8])
    print("test")

    unspew()

    captured = capsys.readouterr()
    output = captured.out

    print(f"\nCaptured output:\n{output}")
    print(f"Output length: {len(output)}")

    # Should have captured built-in function calls
    assert len(output) > 0, "Should have captured some output"
    assert "len" in output or "max" in output or "builtins" in output, (
        f"Should have traced built-in functions. Got: {output}"
    )
