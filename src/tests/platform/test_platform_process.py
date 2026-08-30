from unittest.mock import patch

import pytest

from powerrules.platform.process import PsUtilProcessProvider
from tests.dummies import Dummy_Process


def test_psutil_process_provider_detects_running_process() -> None:
    processes = [
        Dummy_Process("explorer.exe"),
        Dummy_Process("backup.exe"),
    ]

    with patch(
        "powerrules.platform.process.psutil.process_iter",
        return_value=processes,
    ):
        provider = PsUtilProcessProvider()

        assert provider.is_running("backup.exe") is True


def test_psutil_process_provider_returns_false_for_missing_process() -> None:
    processes = [
        Dummy_Process("explorer.exe"),
        Dummy_Process("notepad.exe"),
    ]

    with patch(
        "powerrules.platform.process.psutil.process_iter",
        return_value=processes,
    ):
        provider = PsUtilProcessProvider()

        assert provider.is_running("backup.exe") is False


def test_psutil_process_provider_propagates_process_iterator_error() -> None:
    original_error = RuntimeError("Test process enumeration failure")

    with patch(
        "powerrules.platform.process.psutil.process_iter",
        side_effect=original_error,
    ):
        provider = PsUtilProcessProvider()

        with pytest.raises(RuntimeError) as exc_info:
            provider.is_running("backup.exe")

        assert exc_info.value is original_error
