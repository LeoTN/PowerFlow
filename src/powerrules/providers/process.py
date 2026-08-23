from typing import Protocol


class ProcessProvider(Protocol):
    def is_running(self, process_name: str) -> bool:
        """Return whether a process with the given name is running."""
        ...
