from datetime import datetime

from powerrules.platform.clock import SystemClockProvider


def test_system_clock_provider_returns_datetime() -> None:
    current_time = SystemClockProvider().now()

    assert isinstance(current_time, datetime)


def test_system_clock_provider_returns_current_time() -> None:
    before = datetime.now()
    current_time = SystemClockProvider().now()
    after = datetime.now()

    # The returned time should be in between the time before and after the call
    assert before <= current_time <= after
