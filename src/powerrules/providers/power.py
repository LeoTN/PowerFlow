from typing import Protocol


class PowerProvider(Protocol):
    def shutdown(self) -> None:
        """Shut down the computer."""
        ...

    def sleep(self) -> None:
        """Put the computer into sleep mode."""
        ...

    def hibernate(self) -> None:
        """Put the computer into hibernation."""
        ...

    def reboot(self) -> None:
        """Reboot the computer."""
        ...
