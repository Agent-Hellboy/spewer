"""Unit tests for new trace features: return and exception events."""

from unittest.mock import Mock, patch

from spewer import SpewConfig, TraceHook


class TestTraceReturnEvents:
    """Test cases for return event handling."""

    def test_handle_function_return_with_values(self):
        """Test _handle_function_return with show_values=True."""
        config = SpewConfig(show_values=True, trace_returns=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test return value
        return_value = 42

        # Should not raise exception
        hook._handle_function_return(frame, return_value)

    def test_handle_function_return_without_values(self):
        """Test _handle_function_return with show_values=False."""
        config = SpewConfig(show_values=False, trace_returns=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test return value
        return_value = 42

        # Should not raise exception
        hook._handle_function_return(frame, return_value)

    def test_handle_function_return_unknown_file(self):
        """Test _handle_function_return with unknown file."""
        config = SpewConfig(show_values=True, trace_returns=True)
        hook = TraceHook(config)

        # Create mock frame without __file__
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {}  # No __file__ key

        # Test return value
        return_value = 42

        # Should not raise exception
        hook._handle_function_return(frame, return_value)

    def test_handle_function_return_pyc_file(self):
        """Test _handle_function_return with .pyc file."""
        config = SpewConfig(show_values=True, trace_returns=True)
        hook = TraceHook(config)

        # Create mock frame with .pyc file
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {"__file__": "test.pyc", "__name__": "test"}

        # Test return value
        return_value = 42

        # Should not raise exception
        hook._handle_function_return(frame, return_value)

    def test_handle_function_return_pyo_file(self):
        """Test _handle_function_return with .pyo file."""
        config = SpewConfig(show_values=True, trace_returns=True)
        hook = TraceHook(config)

        # Create mock frame with .pyo file
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {"__file__": "test.pyo", "__name__": "test"}

        # Test return value
        return_value = 42

        # Should not raise exception
        hook._handle_function_return(frame, return_value)

    def test_handle_line_return_with_values(self):
        """Test _handle_line_return with show_values=True."""
        config = SpewConfig(show_values=True, trace_returns=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test return value
        return_value = 42

        # Mock linecache.getline
        with patch("spewer.trace.linecache.getline", return_value="return result"):
            # Should not raise exception
            hook._handle_line_return(frame, return_value)

    def test_handle_line_return_without_values(self):
        """Test _handle_line_return with show_values=False."""
        config = SpewConfig(show_values=False, trace_returns=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test return value
        return_value = 42

        # Mock linecache.getline
        with patch("spewer.trace.linecache.getline", return_value="return result"):
            # Should not raise exception
            hook._handle_line_return(frame, return_value)

    def test_handle_line_return_unknown_file(self):
        """Test _handle_line_return with unknown file."""
        config = SpewConfig(show_values=True, trace_returns=True)
        hook = TraceHook(config)

        # Create mock frame without __file__
        frame = Mock()
        frame.f_lineno = 10
        frame.f_globals = {}  # No __file__ key
        frame.f_code.co_name = "test_func"
        frame.f_lasti = 5

        # Test return value
        return_value = 42

        # Mock inspect.getsourcelines to raise OSError
        with patch(
            "spewer.trace.inspect.getsourcelines", side_effect=OSError("File not found")
        ):
            # Should not raise exception
            hook._handle_line_return(frame, return_value)


class TestTraceExceptionEvents:
    """Test cases for exception event handling."""

    def test_handle_function_exception_with_values(self):
        """Test _handle_function_exception with show_values=True."""
        config = SpewConfig(show_values=True, trace_exceptions=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test exception tuple
        exc_type = ValueError
        exc_value = ValueError("test error")
        exc_tb = None
        exception_arg = (exc_type, exc_value, exc_tb)

        # Should not raise exception
        hook._handle_function_exception(frame, exception_arg)

    def test_handle_function_exception_without_values(self):
        """Test _handle_function_exception with show_values=False."""
        config = SpewConfig(show_values=False, trace_exceptions=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test exception tuple
        exc_type = ValueError
        exc_value = ValueError("test error")
        exc_tb = None
        exception_arg = (exc_type, exc_value, exc_tb)

        # Should not raise exception
        hook._handle_function_exception(frame, exception_arg)

    def test_handle_function_exception_unknown_file(self):
        """Test _handle_function_exception with unknown file."""
        config = SpewConfig(show_values=True, trace_exceptions=True)
        hook = TraceHook(config)

        # Create mock frame without __file__
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {}  # No __file__ key

        # Test exception tuple
        exc_type = ValueError
        exc_value = ValueError("test error")
        exc_tb = None
        exception_arg = (exc_type, exc_value, exc_tb)

        # Should not raise exception
        hook._handle_function_exception(frame, exception_arg)

    def test_handle_line_exception_with_values(self):
        """Test _handle_line_exception with show_values=True."""
        config = SpewConfig(show_values=True, trace_exceptions=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test exception tuple
        exc_type = ValueError
        exc_value = ValueError("test error")
        exc_tb = None
        exception_arg = (exc_type, exc_value, exc_tb)

        # Mock linecache.getline
        with patch(
            "spewer.trace.linecache.getline", return_value="raise ValueError('test')"
        ):
            # Should not raise exception
            hook._handle_line_exception(frame, exception_arg)

    def test_handle_line_exception_without_values(self):
        """Test _handle_line_exception with show_values=False."""
        config = SpewConfig(show_values=False, trace_exceptions=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test exception tuple
        exc_type = ValueError
        exc_value = ValueError("test error")
        exc_tb = None
        exception_arg = (exc_type, exc_value, exc_tb)

        # Mock linecache.getline
        with patch(
            "spewer.trace.linecache.getline", return_value="raise ValueError('test')"
        ):
            # Should not raise exception
            hook._handle_line_exception(frame, exception_arg)

    def test_handle_line_exception_unknown_file(self):
        """Test _handle_line_exception with unknown file."""
        config = SpewConfig(show_values=True, trace_exceptions=True)
        hook = TraceHook(config)

        # Create mock frame without __file__
        frame = Mock()
        frame.f_lineno = 10
        frame.f_globals = {}  # No __file__ key
        frame.f_code.co_name = "test_func"
        frame.f_lasti = 5

        # Test exception tuple
        exc_type = ValueError
        exc_value = ValueError("test error")
        exc_tb = None
        exception_arg = (exc_type, exc_value, exc_tb)

        # Mock inspect.getsourcelines to raise OSError
        with patch(
            "spewer.trace.inspect.getsourcelines", side_effect=OSError("File not found")
        ):
            # Should not raise exception
            hook._handle_line_exception(frame, exception_arg)


class TestTraceHookEventHandling:
    """Test cases for TraceHook event handling with new features."""

    def test_call_with_return_event_functions_only(self):
        """Test __call__ with return event in functions_only mode."""
        config = SpewConfig(functions_only=True, trace_returns=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test return event
        result = hook(frame, "return", 42)
        assert result is hook

    def test_call_with_exception_event_functions_only(self):
        """Test __call__ with exception event in functions_only mode."""
        config = SpewConfig(functions_only=True, trace_exceptions=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test exception event
        exc_type = ValueError
        exc_value = ValueError("test error")
        exc_tb = None
        exception_arg = (exc_type, exc_value, exc_tb)

        result = hook(frame, "exception", exception_arg)
        assert result is hook

    def test_call_with_return_event_line_mode(self):
        """Test __call__ with return event in line mode."""
        config = SpewConfig(functions_only=False, trace_returns=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test return event
        result = hook(frame, "return", 42)
        assert result is hook

    def test_call_with_exception_event_line_mode(self):
        """Test __call__ with exception event in line mode."""
        config = SpewConfig(functions_only=False, trace_exceptions=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test exception event
        exc_type = ValueError
        exc_value = ValueError("test error")
        exc_tb = None
        exception_arg = (exc_type, exc_value, exc_tb)

        result = hook(frame, "exception", exception_arg)
        assert result is hook

    def test_call_with_return_event_trace_returns_false(self):
        """Test __call__ with return event when trace_returns=False."""
        config = SpewConfig(functions_only=True, trace_returns=False)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test return event - should not be handled
        result = hook(frame, "return", 42)
        assert result is hook

    def test_call_with_exception_event_trace_exceptions_false(self):
        """Test __call__ with exception event when trace_exceptions=False."""
        config = SpewConfig(functions_only=True, trace_exceptions=False)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test exception event - should not be handled
        exc_type = ValueError
        exc_value = ValueError("test error")
        exc_tb = None
        exception_arg = (exc_type, exc_value, exc_tb)

        result = hook(frame, "exception", exception_arg)
        assert result is hook


class TestTraceModuleFiltering:
    """Test cases for module filtering with new features."""

    def test_handle_function_return_with_trace_names(self):
        """Test _handle_function_return with specific trace names."""
        config = SpewConfig(trace_names=["test"], show_values=True, trace_returns=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Should not raise exception
        hook._handle_function_return(frame, 42)

    def test_handle_function_return_with_trace_names_excluded(self):
        """Test _handle_function_return with excluded trace names."""
        config = SpewConfig(trace_names=["other"], show_values=True, trace_returns=True)
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Should not raise exception
        hook._handle_function_return(frame, 42)

    def test_handle_function_exception_with_trace_names(self):
        """Test _handle_function_exception with specific trace names."""
        config = SpewConfig(
            trace_names=["test"], show_values=True, trace_exceptions=True
        )
        hook = TraceHook(config)

        # Create mock frame
        frame = Mock()
        frame.f_lineno = 10
        frame.f_code.co_name = "test_func"
        frame.f_globals = {"__file__": "test.py", "__name__": "test"}

        # Test exception tuple
        exc_type = ValueError
        exc_value = ValueError("test error")
        exc_tb = None
        exception_arg = (exc_type, exc_value, exc_tb)

        # Should not raise exception
        hook._handle_function_exception(frame, exception_arg)
