from datetime import datetime
from typing import Protocol


class ClockProvider(Protocol):
    def now(self) -> datetime:
        """Return the current date and time."""
        ...
