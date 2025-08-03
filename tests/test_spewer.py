"""Tests for the spewer library."""

import pytest

from spewer.spewer import SpewContext, Spewer, spew, unspew


class TestSpewer:
    """Test cases for the Spewer class."""

    def test_spewer_initialization(self):
        """Test Spewer initialization."""
        spewer = Spewer()
        assert spewer.trace_names is None
        assert spewer.show_values is True

    def test_spewer_with_trace_names(self):
        """Test Spewer with specific trace names."""
        trace_names = ["test_module"]
        spewer = Spewer(trace_names=trace_names, show_values=False)
        assert spewer.trace_names == trace_names
        assert spewer.show_values is False

    def test_spewer_call_with_line_event(self):
        """Test Spewer __call__ method with line event."""
        spewer = Spewer(show_values=False)

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
        result = spewer(frame, "line", None)
        assert result is spewer

    def test_spewer_call_with_function_event(self):
        """Test Spewer __call__ method with function event."""
        spewer = Spewer(show_values=True, functions_only=True)

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
        result = spewer(frame, "call", None)
        assert result is spewer

    def test_spewer_call_with_other_event(self):
        """Test Spewer __call__ method with non-line event."""
        spewer = Spewer()
        frame = type("MockFrame", (), {})()
        result = spewer(frame, "call", None)
        assert result is spewer


class TestSpewFunctions:
    """Test cases for spew and unspew functions."""

    def test_spew_and_unspew(self):
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

        # Test with context manager
        with SpewContext(show_values=False):
            result = test_function()
            assert result == 30

    def test_module_filtering(self):
        """Test module filtering functionality."""

        def test_function():
            return "test"

        # Test with specific trace names
        with SpewContext(trace_names=["__main__"], show_values=False):
            result = test_function()
            assert result == "test"


if __name__ == "__main__":
    pytest.main([__file__])
