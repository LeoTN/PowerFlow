import pytest

from powerrules.actions.power import (
    HibernateAction,
    RebootAction,
    ShutdownAction,
    SleepAction,
)
from powerrules.engine.exceptions import ActionExecutionError
from tests.dummies import Dummy_PowerProvider


def test_shutdown_action_calls_power_provider() -> None:
    power_provider = Dummy_PowerProvider()

    action = ShutdownAction(power_provider)
    action.execute()

    assert power_provider.shutdown_count == 1


def test_sleep_action_calls_power_provider() -> None:
    power_provider = Dummy_PowerProvider()

    action = SleepAction(power_provider)
    action.execute()

    assert power_provider.sleep_count == 1


def test_hibernate_action_calls_power_provider() -> None:
    power_provider = Dummy_PowerProvider()

    action = HibernateAction(power_provider)
    action.execute()

    assert power_provider.hibernate_count == 1


def test_reboot_action_calls_power_provider() -> None:
    power_provider = Dummy_PowerProvider()

    action = RebootAction(power_provider)
    action.execute()

    assert power_provider.reboot_count == 1


######################
# Error handling tests
######################


def test_shutdown_action_raises_action_execution_error() -> None:
    action = ShutdownAction(
        Dummy_PowerProvider(given_exception=OSError("Test shutdown failure"))
    )

    with pytest.raises(
        ActionExecutionError,
        match="Failed to shut down the computer",
    ):
        action.execute()


def test_sleep_action_raises_action_execution_error() -> None:
    action = SleepAction(
        Dummy_PowerProvider(given_exception=OSError("Test sleep failure"))
    )

    with pytest.raises(
        ActionExecutionError,
        match="Failed to put the computer into sleep mode",
    ):
        action.execute()


def test_hibernate_action_raises_action_execution_error() -> None:
    action = HibernateAction(
        Dummy_PowerProvider(given_exception=OSError("Test hibernate failure"))
    )

    with pytest.raises(
        ActionExecutionError,
        match="Failed to put the computer into hibernation",
    ):
        action.execute()


def test_reboot_action_raises_action_execution_error() -> None:
    action = RebootAction(
        Dummy_PowerProvider(given_exception=OSError("Test reboot failure"))
    )

    with pytest.raises(
        ActionExecutionError,
        match="Failed to reboot the computer",
    ):
        action.execute()
