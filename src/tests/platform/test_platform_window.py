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
