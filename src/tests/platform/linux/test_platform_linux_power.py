from unittest.mock import patch

from powerrules.platform.linux.power import LinuxPowerProvider


def test_linux_power_provider_shutdown() -> None:
    with patch(
        "powerrules.platform.linux.power.subprocess.run",
    ) as mock_run:
        provider = LinuxPowerProvider()

        provider.shutdown()

        mock_run.assert_called_once_with(
            ["systemctl", "poweroff"],
            check=True,
        )


def test_linux_power_provider_sleep() -> None:
    with patch(
        "powerrules.platform.linux.power.subprocess.run",
    ) as mock_run:
        provider = LinuxPowerProvider()

        provider.sleep()

        mock_run.assert_called_once_with(
            ["systemctl", "suspend"],
            check=True,
        )


def test_linux_power_provider_hibernate() -> None:
    with patch(
        "powerrules.platform.linux.power.subprocess.run",
    ) as mock_run:
        provider = LinuxPowerProvider()

        provider.hibernate()

        mock_run.assert_called_once_with(
            ["systemctl", "hibernate"],
            check=True,
        )


def test_linux_power_provider_reboot() -> None:
    with patch(
        "powerrules.platform.linux.power.subprocess.run",
    ) as mock_run:
        provider = LinuxPowerProvider()

        provider.reboot()

        mock_run.assert_called_once_with(
            ["systemctl", "reboot"],
            check=True,
        )
