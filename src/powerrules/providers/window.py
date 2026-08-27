from typing import Protocol


class WindowProvider(Protocol):
    def window_exists(self, window_title: str) -> bool:
        """Return whether a window with the given title exists."""
        ...
