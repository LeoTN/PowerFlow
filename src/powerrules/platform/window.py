import pywinctl


class PyWinCtlWindowProvider:
    """Provide window information using PyWinCtl."""

    def window_exists(self, window_title: str) -> bool:
        """Return whether a window with the given title exists.

        Args:
            window_title: Title of the window to search for.

        Returns:
            True if at least one window has the exact title, otherwise False.
        """
        return any(window.title == window_title for window in pywinctl.getAllWindows())
