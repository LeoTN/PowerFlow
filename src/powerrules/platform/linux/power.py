import subprocess


class LinuxPowerProvider:
    """Provide power management operations on Linux."""

    def shutdown(self) -> None:
        """Shut down the computer."""
        subprocess.run(
            ["systemctl", "poweroff"],
            check=True,
        )

    def sleep(self) -> None:
        """Put the computer into sleep mode."""
        subprocess.run(
            ["systemctl", "suspend"],
            check=True,
        )

    def hibernate(self) -> None:
        """Hibernate the computer."""
        subprocess.run(
            ["systemctl", "hibernate"],
            check=True,
        )

    def reboot(self) -> None:
        """Reboot the computer."""
        subprocess.run(
            ["systemctl", "reboot"],
            check=True,
        )
