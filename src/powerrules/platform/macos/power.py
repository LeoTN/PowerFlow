import subprocess


class MacOSPowerProvider:
    """Provide power management operations on macOS."""

    def shutdown(self) -> None:
        """Shut down the computer."""
        subprocess.run(
            ["shutdown", "-h", "now"],
            check=True,
        )

    def sleep(self) -> None:
        """Put the computer into sleep mode."""
        subprocess.run(
            ["pmset", "sleepnow"],
            check=True,
        )

    def hibernate(self) -> None:
        """Hibernate the computer."""
        raise NotImplementedError(
            "Hibernation is not directly supported by the macOS power provider"
        )

    def reboot(self) -> None:
        """Reboot the computer."""
        subprocess.run(
            ["shutdown", "-r", "now"],
            check=True,
        )
