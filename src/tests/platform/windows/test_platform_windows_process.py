from unittest.mock import patch

import pytest

from powerrules.platform.windows.process import WindowsProcessProvider


class Dummy_Process:
    def __init__(self, process_name: str | None):
        self.info = {
            "name": process_name,
        }


def test_windows_process_provider_detects_running_process() -> None:
    processes = [
        Dummy_Process("explorer.exe"),
        Dummy_Process("backup.exe"),
    ]

    with patch(
        "powerrules.platform.windows.process.psutil.process_iter",
        return_value=processes,
    ):
        provider = WindowsProcessProvider()

        assert provider.is_running("backup.exe") is True


def test_windows_process_provider_returns_false_for_missing_process() -> None:
    processes = [
        Dummy_Process("explorer.exe"),
        Dummy_Process("notepad.exe"),
    ]

    with patch(
        "powerrules.platform.windows.process.psutil.process_iter",
        return_value=processes,
    ):
        provider = WindowsProcessProvider()

        assert provider.is_running("backup.exe") is False


def test_windows_process_provider_propagates_process_iterator_error() -> None:
    original_error = RuntimeError("Test process enumeration failure")

    with patch(
        "powerrules.platform.windows.process.psutil.process_iter",
        side_effect=original_error,
    ):
        provider = WindowsProcessProvider()

        with pytest.raises(RuntimeError) as exc_info:
            provider.is_running("backup.exe")

        assert exc_info.value is original_error
