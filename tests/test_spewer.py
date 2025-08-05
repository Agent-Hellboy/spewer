"""Tests for the spewer library."""

import inspect

import pytest

from spewer import SpewConfig, SpewContext, TraceHook, spew, unspew


class TestSpewConfig:
    """Test cases for the SpewConfig class."""

    def test_spew_config_initialization(self):
        """Test SpewConfig initialization."""
        config = SpewConfig()
        assert config.trace_names is None
        assert config.show_values is True
        assert config.functions_only is False

    def test_spew_config_with_trace_names(self):
        """Test SpewConfig with specific trace names."""
        trace_names = ["test_module"]
        config = SpewConfig(trace_names=trace_names, show_values=False)
        assert config.trace_names == trace_names
        assert config.show_values is False

    def test_spew_config_with_invalid_trace_names(self):
        """Test SpewConfig with invalid trace names."""
        with pytest.raises(TypeError):
            SpewConfig(trace_names=1)

    def test_spew_config_with_invalid_show_values(self):
        """Test SpewConfig with invalid show_values."""
        with pytest.raises(TypeError):
            SpewConfig(show_values="invalid")

    def test_spew_config_with_invalid_functions_only(self):
        """Test SpewConfig with invalid functions_only."""
        with pytest.raises(TypeError):
            SpewConfig(functions_only="invalid")


class TestTraceHook:
    """Test cases for the TraceHook class."""

    def test_trace_hook_initialization(self):
        """Test TraceHook initialization."""
        hook = TraceHook(SpewConfig())
        assert hook.config.trace_names is None
        assert hook.config.show_values is True

    def test_trace_hook_with_trace_names(self):
        """Test TraceHook with specific trace names."""
        trace_names = ["test_module"]
        hook = TraceHook(SpewConfig(trace_names=trace_names, show_values=False))
        assert hook.config.trace_names == trace_names
        assert hook.config.show_values is False

    def test_trace_hook_call_with_line_event(self):
        """Test TraceHook __call__ method with line event."""
        hook = TraceHook(SpewConfig(show_values=False))

        # Create a mock frame
        class MockFrame:
            def __init__(self):
                self.f_lineno = 10
                self.f_globals = {"__file__": "test.py", "__name__": "test"}
                self.f_locals = {}
                self.f_code = type(
                    "MockCode", (), {"co_name": "test_func", "co_lasti": 0}
                )()

        frame = MockFrame()
        result = hook(frame, "line", None)
        assert result is hook

    def test_trace_hook_call_with_function_event(self):
        """Test TraceHook __call__ method with function event."""
        hook = TraceHook(SpewConfig(show_values=True, functions_only=True))

        # Create a mock frame
        class MockFrame:
            def __init__(self):
                self.f_lineno = 20
                self.f_globals = {"__file__": "test.py", "__name__": "test"}
                self.f_locals = {"arg1": 42, "arg2": "hello"}
                self.f_code = type(
                    "MockCode", (), {"co_name": "test_func", "co_lasti": 0}
                )()

        frame = MockFrame()
        result = hook(frame, "call", None)
        assert result is hook

    def test_trace_hook_call_with_other_event(self):
        """Test TraceHook __call__ method with non-line event."""
        hook = TraceHook(SpewConfig())
        frame = type("MockFrame", (), {})()
        result = hook(frame, "call", None)
        assert result is hook

    def test_show_variable_values(self):
        """Test _show_variable_values method."""
        hook = TraceHook(SpewConfig(show_values=True))

        # Create a mock frame with variables
        class MockFrame:
            def __init__(self):
                self.f_globals = {"global_var": "global_value"}
                self.f_locals = {"local_var": 42, "x": 10, "y": 20}

        frame = MockFrame()
        line = "result = x + y"

        # Test that variable values are extracted correctly
        hook._show_variable_values(frame, line)
        # This should print: x=10 y=20

    def test_show_variable_values_with_problematic_objects(self):
        """Test _show_variable_values with problematic objects."""
        hook = TraceHook(SpewConfig(show_values=True))

        # Create a mock frame with problematic objects
        class ProblematicObject:
            def __repr__(self):
                msg = "Infinite recursion"
                raise RecursionError(msg)

        class MockFrame:
            def __init__(self):
                self.f_globals = {}
                self.f_locals = {"problematic": ProblematicObject()}

        frame = MockFrame()
        line = "x = problematic"

        # This should not raise an exception
        hook._show_variable_values(frame, line)

    def test_show_function_args(self):
        """Test _show_function_args method."""
        hook = TraceHook(SpewConfig(show_values=True))

        # Create a mock frame with function arguments
        class MockFrame:
            def __init__(self):
                self.f_locals = {
                    "x": 10,
                    "y": "hello",
                    "__builtins__": "builtins",  # Should be ignored
                    "arg1": 42,
                }

        frame = MockFrame()

        # Test that function arguments are extracted correctly
        hook._show_function_args(frame)
        # This should print: x=10 y='hello' arg1=42

    def test_show_function_args_with_problematic_objects(self):
        """Test _show_function_args with problematic objects."""
        hook = TraceHook(SpewConfig(show_values=True))

        # Create a mock frame with problematic objects
        class ProblematicObject:
            def __repr__(self):
                msg = "Cannot represent"
                raise TypeError(msg)

        class MockFrame:
            def __init__(self):
                self.f_locals = {"normal": "value", "problematic": ProblematicObject()}

        frame = MockFrame()

        # This should not raise an exception
        hook._show_function_args(frame)

    def test_handle_line_execution_with_unknown_file(self):
        """Test _handle_line_execution with unknown file."""
        hook = TraceHook(SpewConfig(show_values=False))

        # Create a mock frame without __file__
        class MockCode:
            def __init__(self):
                self.co_name = "unknown_func"
                self.co_lasti = 5

        class MockFrame:
            def __init__(self):
                self.f_lineno = 10
                self.f_globals = {}  # No __file__ key
                self.f_code = MockCode()
                self.f_lasti = 5

        frame = MockFrame()

        # Mock inspect.getsourcelines to raise OSError
        original_getsourcelines = inspect.getsourcelines
        try:
            inspect.getsourcelines = lambda _: (_ for _ in ()).throw(
                OSError("File not found")
            )

            # This should handle the OSError gracefully
            hook._handle_line_execution(frame)
        finally:
            inspect.getsourcelines = original_getsourcelines

    def test_tracehook_with_pyc_file(self):
        """Test TraceHook with a .pyc file."""
        hook = TraceHook(SpewConfig(show_values=False))

        # Create a mock frame with a .pyc file
        class MockFrame:
            def __init__(self):
                self.f_lineno = 10
                self.f_globals = {"__file__": "test.pyc", "__name__": "test"}
                self.f_locals = {}
                self.f_code = type(
                    "MockCode", (), {"co_name": "test_func", "co_lasti": 0}
                )()

        frame = MockFrame()
        hook._handle_line_execution(frame)

    def test_tracehook_with_pyo_file(self):
        """Test TraceHook with a .pyo file."""
        hook = TraceHook(SpewConfig(show_values=False))

        # Create a mock frame with a .pyo file
        class MockFrame:
            def __init__(self):
                self.f_lineno = 10
                self.f_globals = {"__file__": "test.pyo", "__name__": "test"}
                self.f_locals = {}
                self.f_code = type(
                    "MockCode", (), {"co_name": "test_func", "co_lasti": 0}
                )()

        frame = MockFrame()
        hook._handle_line_execution(frame)

    def test_handle_function_call_with_unknown_file(self):
        """Test _handle_function_call with unknown file."""
        hook = TraceHook(SpewConfig(show_values=True))

        # Create a mock frame without __file__
        class MockCode:
            def __init__(self):
                self.co_name = "unknown_func"
                self.co_lasti = 5

        class MockFrame:
            def __init__(self):
                self.f_lineno = 20
                self.f_globals = {}  # No __file__ key
                self.f_locals = {"x": 10, "y": 20}
                self.f_code = MockCode()
                self.f_lasti = 5

        frame = MockFrame()

        # This should handle the unknown file case gracefully
        hook._handle_function_call(frame)


class TestSpewContext:
    """Test cases for SpewContext class."""

    def test_spew_context_initialization(self):
        """Test spew and unspew functions."""
        # Test that unspew doesn't raise an error
        unspew()

        # Test spew with default parameters
        spew()
        unspew()

        # Test spew with custom parameters
        spew(trace_names=["test"], show_values=True)
        unspew()

    def test_spew_context_manager(self):
        """Test SpewContext context manager."""
        with SpewContext():
            # Context manager should work without errors
            pass


class TestIntegration:
    """Integration tests for the spewer library."""

    def test_basic_tracing(self):
        """Test basic tracing functionality."""

        def test_function():
            x = 10
            y = 20
            return x + y

    def test_basic_tracing_with_context_manager(self):
        """Test basic tracing functionality with context manager."""

        def test_function():
            x = 10
            y = 20
            return x + y

        # Test with context manager
        with SpewContext(show_values=False):
            result = test_function()
            assert result == 30

    def test_module_filtering_with_context_manager(self):
        """Test module filtering functionality."""

        def test_function():
            return "test"

        # Test with specific trace names
        with SpewContext(trace_names=["__main__"], show_values=False):
            result = test_function()
            assert result == "test"


if __name__ == "__main__":
    pytest.main([__file__])
