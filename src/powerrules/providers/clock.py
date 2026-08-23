from datetime import datetime
from typing import Protocol


class ClockProvider(Protocol):
    def now(self) -> datetime:
        """Return the current date and time."""
        ...


class SystemClockProvider:
    def now(self) -> datetime:
        """Return the current system date and time."""
        return datetime.now()
