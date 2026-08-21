import pytest

from powerrules.conditions.operators import AndCondition, OrCondition
from powerrules.engine.exceptions import ConditionEvaluationError


# Dummy condition which returns a fixed evaluation result
class Dummy_Condition:
    def __init__(self, result: bool):
        self.result = result

    def evaluate(self) -> bool:
        return self.result


# This condition keeps track of how many times it has been evaluated
class Dummy_TrackingCondition:
    def __init__(self, result: bool):
        self.result = result
        self.evaluation_count = 0

    def evaluate(self) -> bool:
        self.evaluation_count += 1
        return self.result


class Dummy_FailingCondition:
    def evaluate(self) -> bool:
        raise ConditionEvaluationError("Test condition failed")


####################
# AndCondition tests
####################


def test_and_condition_matches_when_all_conditions_match() -> None:
    condition = AndCondition(
        conditions=(
            Dummy_Condition(True),
            Dummy_Condition(True),
            Dummy_Condition(True),
        )
    )

    assert condition.evaluate() is True


def test_and_condition_does_not_match_when_one_condition_does_not_match() -> None:
    condition = AndCondition(
        conditions=(
            Dummy_Condition(True),
            Dummy_Condition(False),
            Dummy_Condition(True),
        )
    )

    assert condition.evaluate() is False


# Does the evaluation stop after the first false condition is found?
def test_and_condition_short_circuits_after_first_false_condition() -> None:
    first_condition = Dummy_TrackingCondition(False)
    second_condition = Dummy_TrackingCondition(True)

    condition = AndCondition(
        conditions=(
            first_condition,
            second_condition,
        )
    )

    assert condition.evaluate() is False
    assert first_condition.evaluation_count == 1
    assert second_condition.evaluation_count == 0


def test_and_condition_propagates_condition_evaluation_error() -> None:
    condition = AndCondition(conditions=(Dummy_FailingCondition(),))

    with pytest.raises(ConditionEvaluationError):
        condition.evaluate()


###################
# OrCondition tests
###################


def test_or_condition_matches_when_one_condition_matches() -> None:
    condition = OrCondition(
        conditions=(
            Dummy_Condition(False),
            Dummy_Condition(True),
            Dummy_Condition(False),
        )
    )

    assert condition.evaluate() is True


def test_or_condition_does_not_match_when_no_condition_matches() -> None:
    condition = OrCondition(
        conditions=(
            Dummy_Condition(False),
            Dummy_Condition(False),
            Dummy_Condition(False),
        )
    )

    assert condition.evaluate() is False


# Does the evaluation stop after the first true condition is found?
def test_or_condition_short_circuits_after_first_true_condition() -> None:
    first_condition = Dummy_TrackingCondition(True)
    second_condition = Dummy_TrackingCondition(False)

    condition = OrCondition(
        conditions=(
            first_condition,
            second_condition,
        )
    )

    assert condition.evaluate() is True
    assert first_condition.evaluation_count == 1
    assert second_condition.evaluation_count == 0


def test_or_condition_propagates_condition_evaluation_error() -> None:
    condition = OrCondition(conditions=(Dummy_FailingCondition(),))

    with pytest.raises(ConditionEvaluationError):
        condition.evaluate()
