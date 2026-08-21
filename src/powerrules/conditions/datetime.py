from dataclasses import dataclass
from datetime import time

from powerrules.providers.clock import ClockProvider


@dataclass(frozen=True)
class TimeRange:
    """Represents a range of time within a day."""

    start: time
    end: time

    def contains(self, current_time: time) -> bool:
        """Return whether the given time is within the range.

        The start time is inclusive and the end time is exclusive (6:00 is in the range 23:00-7:00, but 7:00 is not).

        Ranges crossing midnight are supported.

        Args:
            current_time: Time to check.

        Returns:
            True if the time is within the range, otherwise False.
        """
        # The range does not cross midnight
        if self.start <= self.end:
            # Does the current_time fall within the range?
            return self.start <= current_time < self.end

        # The range crosses midnight (e.g., 23:00-7:00)
        # Does the current_time fall within the range?
        return current_time >= self.start or current_time < self.end


class DateTimeCondition:
    def __init__(
        self,
        time_range: TimeRange,
        clock_provider: ClockProvider,
    ):
        self.time_range = time_range
        self.clock_provider = clock_provider

    def evaluate(self) -> bool:
        """Evaluate whether the current time is within the configured range.

        Returns:
            True if the current time is within the configured range,
            otherwise False.
        """
        current_time = self.clock_provider.now().time()

        return self.time_range.contains(current_time)
