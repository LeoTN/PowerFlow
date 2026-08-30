from unittest.mock import patch

import pytest

from powerrules.platform.macos.power import MacOSPowerProvider


def test_macos_power_provider_shutdown() -> None:
    with patch(
        "powerrules.platform.macos.power.subprocess.run",
    ) as mock_run:
        provider = MacOSPowerProvider()

        provider.shutdown()

        mock_run.assert_called_once_with(
            ["shutdown", "-h", "now"],
            check=True,
        )


def test_macos_power_provider_sleep() -> None:
    with patch(
        "powerrules.platform.macos.power.subprocess.run",
    ) as mock_run:
        provider = MacOSPowerProvider()

        provider.sleep()

        mock_run.assert_called_once_with(
            ["pmset", "sleepnow"],
            check=True,
        )


def test_macos_power_provider_reboot() -> None:
    with patch(
        "powerrules.platform.macos.power.subprocess.run",
    ) as mock_run:
        provider = MacOSPowerProvider()

        provider.reboot()

        mock_run.assert_called_once_with(
            ["shutdown", "-r", "now"],
            check=True,
        )


def test_macos_power_provider_hibernate_is_not_supported() -> None:
    provider = MacOSPowerProvider()

    with pytest.raises(
        NotImplementedError,
        match="Hibernation is not directly supported",
    ):
        provider.hibernate()
