import pytest

from powerrules.conditions.process import ProcessCondition
from powerrules.engine.exceptions import ConditionEvaluationError


class Dummy_ProcessProvider:
    def __init__(self, is_running: bool):
        self.is_running_result = is_running
        self.requested_process_name = None

    def is_running(self, process_name: str) -> bool:
        self.requested_process_name = process_name
        return self.is_running_result


class Dummy_FailingProcessProvider:
    def is_running(self, process_name: str) -> bool:
        raise OSError("Test OSError")


def test_process_condition_matches_running_process() -> None:
    provider = Dummy_ProcessProvider(is_running=True)

    condition = ProcessCondition(
        process_name="test.exe",
        expected_running=True,
        process_provider=provider,
    )

    assert condition.evaluate() is True
    assert provider.requested_process_name == "test.exe"


def test_process_condition_does_not_match_stopped_process() -> None:
    provider = Dummy_ProcessProvider(is_running=False)

    condition = ProcessCondition(
        process_name="test.exe",
        expected_running=True,
        process_provider=provider,
    )

    assert condition.evaluate() is False


def test_process_condition_matches_stopped_process() -> None:
    provider = Dummy_ProcessProvider(is_running=False)

    condition = ProcessCondition(
        process_name="test.exe",
        expected_running=False,
        process_provider=provider,
    )

    assert condition.evaluate() is True


def test_process_condition_does_not_match_running_process() -> None:
    provider = Dummy_ProcessProvider(is_running=True)

    condition = ProcessCondition(
        process_name="test.exe",
        expected_running=False,
        process_provider=provider,
    )

    assert condition.evaluate() is False


def test_process_condition_uses_configured_process_name() -> None:
    provider = Dummy_ProcessProvider(is_running=True)

    condition = ProcessCondition(
        process_name="my-process.exe",
        expected_running=True,
        process_provider=provider,
    )

    condition.evaluate()

    assert provider.requested_process_name == "my-process.exe"


def test_process_condition_raises_evaluation_error() -> None:
    condition = ProcessCondition(
        process_name="test.exe",
        expected_running=True,
        process_provider=Dummy_FailingProcessProvider(),
    )

    # Make sure the exception type is correct
    with pytest.raises(ConditionEvaluationError) as exc_info:
        condition.evaluate()

    # Make sure the exception message is used from the underlying exception
    assert str(exc_info.value) == (
        "Failed to determine whether process 'test.exe' is running."
    )
