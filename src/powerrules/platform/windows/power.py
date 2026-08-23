import ctypes
import subprocess


class WindowsPowerProvider:
    """Provide power management operations on Windows."""

    def shutdown(self) -> None:
        """Shut down the computer."""
        subprocess.run(
            ["shutdown.exe", "/s", "/t", "0"],
            check=True,
        )

    def sleep(self) -> None:
        """Put the computer into sleep mode."""
        self._set_suspend_state(hibernate=False)

    def hibernate(self) -> None:
        """Put the computer into hibernation."""
        self._set_suspend_state(hibernate=True)

    def reboot(self) -> None:
        """Reboot the computer."""
        subprocess.run(
            ["shutdown.exe", "/r", "/t", "0"],
            check=True,
        )

    @staticmethod
    def _set_suspend_state(hibernate: bool) -> None:
        """Set the Windows suspend state.

        Args:
            hibernate: True to hibernate, False to enter sleep mode.

        Raises:
            OSError: If Windows cannot change the system power state.
        """
        result = ctypes.windll.powrprof.SetSuspendState(
            hibernate,
            False,
            False,
        )

        if not result:
            error_code = ctypes.get_last_error()
            raise OSError(
                error_code,
                f"Failed to change the Windows power state, error code {error_code}",
            )
