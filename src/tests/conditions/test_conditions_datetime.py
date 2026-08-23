from datetime import datetime, time

from powerrules.conditions.datetime import DateTimeCondition, TimeRange, Weekday


# Dummy clock which returns the given time
class Dummy_ClockProvider:
    def __init__(self, current_time: datetime):
        self.current_time = current_time

    def now(self) -> datetime:
        return self.current_time


#################
# TimeRange tests
#################


def test_time_range_matches_time_inside_normal_range() -> None:
    time_range = TimeRange(
        start=time(10, 0),
        end=time(18, 0),
    )

    assert time_range.contains(time(12, 0)) is True


def test_time_range_does_not_match_time_before_normal_range() -> None:
    time_range = TimeRange(
        start=time(10, 0),
        end=time(18, 0),
    )

    assert time_range.contains(time(9, 59)) is False


def test_time_range_does_not_match_time_after_normal_range() -> None:
    time_range = TimeRange(
        start=time(10, 0),
        end=time(18, 0),
    )

    assert time_range.contains(time(18, 1)) is False


def test_time_range_includes_start_time() -> None:
    time_range = TimeRange(
        start=time(10, 0),
        end=time(18, 0),
    )

    assert time_range.contains(time(10, 0)) is True


def test_time_range_excludes_end_time() -> None:
    time_range = TimeRange(
        start=time(10, 0),
        end=time(18, 0),
    )

    assert time_range.contains(time(18, 0)) is False


def test_time_range_matches_time_after_midnight_when_crossing_midnight() -> None:
    time_range = TimeRange(
        start=time(22, 0),
        end=time(6, 0),
    )

    assert time_range.contains(time(2, 0)) is True


def test_time_range_matches_time_before_midnight_when_crossing_midnight() -> None:
    time_range = TimeRange(
        start=time(22, 0),
        end=time(6, 0),
    )

    assert time_range.contains(time(23, 0)) is True


def test_time_range_does_not_match_time_outside_midnight_range() -> None:
    time_range = TimeRange(
        start=time(22, 0),
        end=time(6, 0),
    )

    assert time_range.contains(time(12, 0)) is False


def test_time_range_excludes_end_time_when_crossing_midnight() -> None:
    time_range = TimeRange(
        start=time(22, 0),
        end=time(6, 0),
    )

    assert time_range.contains(time(6, 0)) is False


# Special case: start and end are equal, which means no time is in the range
def test_time_range_with_equal_start_and_end_matches_no_time() -> None:
    time_range = TimeRange(
        start=time(10, 0),
        end=time(10, 0),
    )

    assert time_range.contains(time(10, 0)) is False
    assert time_range.contains(time(12, 0)) is False


#########################
# DateTimeCondition tests
#########################


def test_datetime_condition_matches_current_time_in_range() -> None:
    clock_provider = Dummy_ClockProvider(
        datetime(2026, 8, 21, 23, 30),
    )

    condition = DateTimeCondition(
        time_range=TimeRange(
            start=time(22, 0),
            end=time(6, 0),
        ),
        clock_provider=clock_provider,
    )

    assert condition.evaluate() is True


def test_datetime_condition_does_not_match_current_time_outside_range() -> None:
    clock_provider = Dummy_ClockProvider(
        datetime(2026, 8, 21, 12, 0),
    )

    condition = DateTimeCondition(
        time_range=TimeRange(
            start=time(22, 0),
            end=time(6, 0),
        ),
        clock_provider=clock_provider,
    )

    assert condition.evaluate() is False


def test_datetime_condition_matches_configured_weekday() -> None:
    clock_provider = Dummy_ClockProvider(datetime(2026, 8, 21, 12, 0))

    condition = DateTimeCondition(
        clock_provider=clock_provider,
        weekdays=frozenset({Weekday.FRIDAY}),
    )

    assert condition.evaluate() is True


def test_datetime_condition_does_not_match_unconfigured_weekday() -> None:
    clock_provider = Dummy_ClockProvider(datetime(2026, 8, 21, 12, 0))

    condition = DateTimeCondition(
        clock_provider=clock_provider,
        weekdays=frozenset({Weekday.MONDAY}),
    )

    assert condition.evaluate() is False


def test_datetime_condition_matches_one_of_multiple_weekdays() -> None:
    clock_provider = Dummy_ClockProvider(datetime(2026, 8, 21, 12, 0))

    condition = DateTimeCondition(
        clock_provider=clock_provider,
        weekdays=frozenset(
            {
                Weekday.MONDAY,
                Weekday.FRIDAY,
                Weekday.SUNDAY,
            }
        ),
    )

    assert condition.evaluate() is True


def test_datetime_condition_does_not_match_when_current_weekday_is_not_configured() -> (
    None
):
    clock_provider = Dummy_ClockProvider(datetime(2026, 8, 21, 12, 0))

    condition = DateTimeCondition(
        clock_provider=clock_provider,
        weekdays=frozenset(
            {
                Weekday.MONDAY,
                Weekday.TUESDAY,
            }
        ),
    )

    assert condition.evaluate() is False
