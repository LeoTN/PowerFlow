import pytest

from powerrules.conditions.window import WindowCondition
from powerrules.engine.exceptions import ConditionEvaluationError
from tests.dummies import Dummy_WindowProvider


def test_window_condition_matches_existing_window() -> None:
    provider = Dummy_WindowProvider(given_window_exists=True)

    condition = WindowCondition(
        window_title="Test window title",
        expected_exists=True,
        window_provider=provider,
    )

    assert condition.evaluate() is True


def test_window_condition_does_not_match_existing_window() -> None:
    provider = Dummy_WindowProvider(given_window_exists=True)

    condition = WindowCondition(
        window_title="Test window title",
        expected_exists=False,
        window_provider=provider,
    )

    assert condition.evaluate() is False


def test_window_condition_matches_missing_window() -> None:
    provider = Dummy_WindowProvider(given_window_exists=False)

    condition = WindowCondition(
        window_title="Test window title",
        expected_exists=False,
        window_provider=provider,
    )

    assert condition.evaluate() is True


def test_window_condition_does_not_match_missing_window() -> None:
    provider = Dummy_WindowProvider(given_window_exists=False)

    condition = WindowCondition(
        window_title="Test window title",
        expected_exists=True,
        window_provider=provider,
    )

    assert condition.evaluate() is False


def test_window_condition_uses_configured_window_title() -> None:
    provider = Dummy_WindowProvider(given_window_exists=True)

    condition = WindowCondition(
        window_title="My window title",
        expected_exists=True,
        window_provider=provider,
    )

    condition.evaluate()

    assert provider.given_window_title == "My window title"


def test_window_condition_raises_evaluation_error() -> None:
    provider = Dummy_WindowProvider(
        given_window_exists=True,
        given_exception=RuntimeError("Test window enumeration failure"),
    )

    condition = WindowCondition(
        window_title="Test window title",
        expected_exists=True,
        window_provider=provider,
    )

    # Make sure the exception type is correct
    with pytest.raises(ConditionEvaluationError) as exc_info:
        condition.evaluate()

    # Make sure the exception message is used from the underlying exception
    assert (
        str(exc_info.value)
        == "Failed to determine whether window 'Test window title' exists."
    )
