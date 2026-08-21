import pytest

from powerrules.actions.power import (
    HibernateAction,
    RebootAction,
    ShutdownAction,
    SleepAction,
)
from powerrules.engine.exceptions import ActionExecutionError


# Keep track of the number of times each action is executed
class Dummy_PowerProvider:
    def __init__(self):
        self.shutdown_count = 0
        self.sleep_count = 0
        self.hibernate_count = 0
        self.reboot_count = 0

    def shutdown(self) -> None:
        self.shutdown_count += 1

    def sleep(self) -> None:
        self.sleep_count += 1

    def hibernate(self) -> None:
        self.hibernate_count += 1

    def reboot(self) -> None:
        self.reboot_count += 1


class Dummy_FailingPowerProvider:
    def shutdown(self) -> None:
        raise OSError("Test shutdown failure")

    def sleep(self) -> None:
        raise OSError("Test sleep failure")

    def hibernate(self) -> None:
        raise OSError("Test hibernate failure")

    def reboot(self) -> None:
        raise OSError("Test reboot failure")


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
    action = ShutdownAction(Dummy_FailingPowerProvider())

    with pytest.raises(
        ActionExecutionError,
        match="Failed to shut down the computer",
    ):
        action.execute()


def test_sleep_action_raises_action_execution_error() -> None:
    action = SleepAction(Dummy_FailingPowerProvider())

    with pytest.raises(
        ActionExecutionError,
        match="Failed to put the computer into sleep mode",
    ):
        action.execute()


def test_hibernate_action_raises_action_execution_error() -> None:
    action = HibernateAction(Dummy_FailingPowerProvider())

    with pytest.raises(
        ActionExecutionError,
        match="Failed to put the computer into hibernation",
    ):
        action.execute()


def test_reboot_action_raises_action_execution_error() -> None:
    action = RebootAction(Dummy_FailingPowerProvider())

    with pytest.raises(
        ActionExecutionError,
        match="Failed to reboot the computer",
    ):
        action.execute()
