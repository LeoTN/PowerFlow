import psutil


# psutil already makes everything platform independent
class PsUtilProcessProvider:
    """Provide process information on Windows, Linux and macOS."""

    def is_running(self, process_name: str) -> bool:
        """Return whether a process with the given name is running.

        Args:
            process_name: Name of the process to search for.

        Returns:
            True if at least one matching process is running, otherwise False.
        """
        for process in psutil.process_iter(["name"]):
            if process.info["name"] == process_name:
                return True

        return False
