from typing import Protocol


class WindowProvider(Protocol):
    @property
    def is_available(self) -> bool:
        """Whether the provider is available on the current platform."""
        ...

    def window_exists(self, window_title: str) -> bool:
        """Return whether a window with the given title exists."""
        ...
