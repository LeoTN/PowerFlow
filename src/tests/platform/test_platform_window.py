from unittest.mock import Mock, patch

import pytest

from powerrules.platform.window import PyWinCtlWindowProvider


def test_pywinctl_window_provider_detects_existing_window() -> None:
    window_title = "Test window title"
    provider = PyWinCtlWindowProvider()

    with patch("pywinctl.getAllWindows", return_value=[Mock(title=window_title)]):
        assert provider.window_exists(window_title) is True


def test_pywinctl_window_provider_returns_false_for_missing_window() -> None:
    window_title = "Test window title"
    provider = PyWinCtlWindowProvider()

    with patch("pywinctl.getAllWindows", return_value=[]):
        assert provider.window_exists(window_title) is False


def test_pywinctl_window_provider_propagates_get_all_windows_error() -> None:
    window_title = "Test window title"
    original_error = RuntimeError("Test window enumeration failure")

    with patch("pywinctl.getAllWindows", side_effect=original_error):
        provider = PyWinCtlWindowProvider()

        with pytest.raises(RuntimeError) as exc_info:
            provider.window_exists(window_title)

        assert exc_info.value is original_error


def test_pywinctl_window_provider_is_not_available_when_import_fails() -> None:
    original_import = __import__

    def failing_import(
        name: str,
        globals: dict | None = None,
        locals: dict | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ):
        if name == "pywinctl":
            raise ImportError("Test import failure on non-supported platform")

        return original_import(name, globals, locals, fromlist, level)

    with patch("builtins.__import__", side_effect=failing_import):
        provider = PyWinCtlWindowProvider()

    assert provider.is_available is False
