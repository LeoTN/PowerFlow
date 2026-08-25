import pytest

from powerrules.conditions.operators import AndCondition, NotCondition, OrCondition
from powerrules.engine.exceptions import ConditionEvaluationError
from tests.dummies import Dummy_Condition


def test_nested_conditions_are_evaluated_correctly() -> None:
    condition = AndCondition(
        conditions=(
            Dummy_Condition(given_result=True),
            NotCondition(
                condition=OrCondition(
                    conditions=(
                        Dummy_Condition(given_result=False),
                        Dummy_Condition(given_result=False),
                    )
                )
            ),
        )
    )

    assert condition.evaluate() is True


####################
# AndCondition tests
####################


def test_and_condition_matches_when_all_conditions_match() -> None:
    condition = AndCondition(
        conditions=(
            Dummy_Condition(given_result=True),
            Dummy_Condition(given_result=True),
            Dummy_Condition(given_result=True),
        )
    )

    assert condition.evaluate() is True


def test_and_condition_does_not_match_when_one_condition_does_not_match() -> None:
    condition = AndCondition(
        conditions=(
            Dummy_Condition(given_result=True),
            Dummy_Condition(given_result=False),
            Dummy_Condition(given_result=True),
        )
    )

    assert condition.evaluate() is False


# Does the evaluation stop after the first false condition is found?
def test_and_condition_short_circuits_after_first_false_condition() -> None:
    first_condition = Dummy_Condition(given_result=False)
    second_condition = Dummy_Condition(given_result=True)

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
    condition = AndCondition(
        conditions=(
            Dummy_Condition(
                given_result=True,
                given_exception=ConditionEvaluationError("Test condition failed"),
            ),
        )
    )

    with pytest.raises(ConditionEvaluationError):
        condition.evaluate()


###################
# OrCondition tests
###################


def test_or_condition_matches_when_one_condition_matches() -> None:
    condition = OrCondition(
        conditions=(
            Dummy_Condition(given_result=False),
            Dummy_Condition(given_result=True),
            Dummy_Condition(given_result=False),
        )
    )

    assert condition.evaluate() is True


def test_or_condition_does_not_match_when_no_condition_matches() -> None:
    condition = OrCondition(
        conditions=(
            Dummy_Condition(given_result=False),
            Dummy_Condition(given_result=False),
            Dummy_Condition(given_result=False),
        )
    )

    assert condition.evaluate() is False


# Does the evaluation stop after the first true condition is found?
def test_or_condition_short_circuits_after_first_true_condition() -> None:
    first_condition = Dummy_Condition(given_result=True)
    second_condition = Dummy_Condition(given_result=False)

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
    condition = OrCondition(
        conditions=(
            Dummy_Condition(
                given_result=True,
                given_exception=ConditionEvaluationError("Test condition failed"),
            ),
        )
    )

    with pytest.raises(ConditionEvaluationError):
        condition.evaluate()


####################
# NotCondition tests
####################


def test_not_condition_matches_when_child_does_not_match() -> None:
    condition = NotCondition(
        condition=Dummy_Condition(given_result=False),
    )

    assert condition.evaluate() is True


def test_not_condition_does_not_match_when_child_matches() -> None:
    condition = NotCondition(
        condition=Dummy_Condition(given_result=True),
    )

    assert condition.evaluate() is False


def test_not_condition_propagates_condition_evaluation_error() -> None:
    condition = NotCondition(
        condition=Dummy_Condition(
            given_result=True,
            given_exception=ConditionEvaluationError("Test condition failed"),
        ),
    )

    with pytest.raises(
        ConditionEvaluationError,
        match="Test condition failed",
    ):
        condition.evaluate()
