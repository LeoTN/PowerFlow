import typer


class PyWinCtlWindowProvider:
    """Provide window information using PyWinCtl."""

    def __init__(self):
        self.is_available = False
        self._pywinctl = None

        try:
            import pywinctl

            self.is_available = True
            self._pywinctl = pywinctl

        # This exception is common on headless systems (e.g. Ubuntu Server)
        except Exception:
            typer.echo(
                "[WARNING] Failed to load window provider. Window conditions will not be available",
                err=True,
            )

    def window_exists(self, window_title: str) -> bool:
        """Return whether a window with the given title exists.

        Args:
            window_title: Title of the window to search for.

        Returns:
            True if at least one window has the exact title, otherwise False.

        Raises:
            RuntimeError: If the window provider is not available.
        """

        if not self.is_available or self._pywinctl is None:
            raise RuntimeError("Window provider is not available")

        return any(
            window.title == window_title for window in self._pywinctl.getAllWindows()
        )
