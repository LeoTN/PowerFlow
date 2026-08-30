import pytest

from powerrules.engine.exceptions import ActionExecutionError, ConditionEvaluationError
from powerrules.engine.rule_engine import Rule, RuleEngine
from tests.dummies import Dummy_Action, Dummy_Condition


def test_rule_engine_executes_action_when_condition_matches() -> None:
    condition = Dummy_Condition(given_result=True)
    action = Dummy_Action()

    rule = Rule(
        name="Test rule",
        condition=condition,
        action=action,
    )

    result = RuleEngine((rule,)).evaluate()

    assert result.matched_rule is rule
    assert condition.evaluation_count == 1
    assert action.execution_count == 1


def test_rule_engine_skips_non_matching_rule() -> None:
    condition = Dummy_Condition(given_result=False)
    action = Dummy_Action()

    rule = Rule(
        name="Test rule",
        condition=condition,
        action=action,
    )

    result = RuleEngine((rule,)).evaluate()

    assert result.matched_rule is None
    assert condition.evaluation_count == 1
    assert action.execution_count == 0


def test_rule_engine_evaluates_rules_from_top_to_bottom() -> None:
    first_condition = Dummy_Condition(given_result=False)
    first_action = Dummy_Action()

    second_condition = Dummy_Condition(given_result=True)
    second_action = Dummy_Action()

    rules = (
        Rule(
            name="First test rule",
            condition=first_condition,
            action=first_action,
        ),
        Rule(
            name="Second test rule",
            condition=second_condition,
            action=second_action,
        ),
    )

    result = RuleEngine(rules).evaluate()

    assert result.matched_rule is rules[1]
    assert first_condition.evaluation_count == 1
    assert first_action.execution_count == 0
    assert second_condition.evaluation_count == 1
    assert second_action.execution_count == 1


def test_rule_engine_stops_after_first_matching_rule() -> None:
    first_condition = Dummy_Condition(given_result=True)
    first_action = Dummy_Action()

    second_condition = Dummy_Condition(given_result=True)
    second_action = Dummy_Action()

    rules = (
        Rule(
            name="First test rule",
            condition=first_condition,
            action=first_action,
        ),
        Rule(
            name="Second test rule",
            condition=second_condition,
            action=second_action,
        ),
    )

    result = RuleEngine(rules).evaluate()

    assert result.matched_rule is rules[0]
    assert first_action.execution_count == 1
    # The second rule should not even be evaluated
    assert second_condition.evaluation_count == 0
    assert second_action.execution_count == 0


def test_rule_engine_skips_disabled_rules() -> None:
    condition = Dummy_Condition(given_result=True)
    action = Dummy_Action()

    rule = Rule(
        name="Disabled test rule",
        condition=condition,
        action=action,
        enabled=False,
    )

    result = RuleEngine((rule,)).evaluate()

    assert result.matched_rule is None
    assert condition.evaluation_count == 0
    assert action.execution_count == 0


def test_rule_engine_returns_no_match_when_no_rule_matches() -> None:
    first_condition = Dummy_Condition(given_result=False)
    first_action = Dummy_Action()

    second_condition = Dummy_Condition(given_result=False)
    second_action = Dummy_Action()

    rules = (
        Rule(
            name="First test rule",
            condition=first_condition,
            action=first_action,
        ),
        Rule(
            name="Second test rule",
            condition=second_condition,
            action=second_action,
        ),
    )

    result = RuleEngine(rules).evaluate()

    assert result.matched_rule is None
    assert first_action.execution_count == 0
    assert second_action.execution_count == 0


# This should not happen in practice due to YAML validation
def test_rule_engine_returns_no_match_for_empty_rule_list() -> None:
    result = RuleEngine(()).evaluate()

    assert result.matched_rule is None


######################
# Error handling tests
######################


def test_rule_engine_propagates_condition_evaluation_error() -> None:
    action = Dummy_Action()

    rule = Rule(
        name="Failing test rule",
        condition=Dummy_Condition(
            given_result=True,
            given_exception=ConditionEvaluationError("Test condition failed"),
        ),
        action=action,
    )

    with pytest.raises(ConditionEvaluationError, match="Test condition failed"):
        RuleEngine((rule,)).evaluate()

    assert action.execution_count == 0


def test_rule_engine_stops_after_condition_evaluation_error() -> None:
    first_rule = Rule(
        name="Failing test rule",
        condition=Dummy_Condition(
            given_result=True,
            given_exception=ConditionEvaluationError("Test condition failed"),
        ),
        action=Dummy_Action(),
    )

    second_condition = Dummy_Condition(given_result=True)
    second_action = Dummy_Action()

    second_rule = Rule(
        name="Second test rule",
        condition=second_condition,
        action=second_action,
    )

    with pytest.raises(ConditionEvaluationError):
        RuleEngine((first_rule, second_rule)).evaluate()

    assert second_condition.evaluation_count == 0
    assert second_action.execution_count == 0


def test_rule_engine_propagates_action_execution_error() -> None:
    condition = Dummy_Condition(given_result=True)

    rule = Rule(
        name="Failing test rule",
        condition=condition,
        action=Dummy_Action(given_exception=ActionExecutionError("Test action failed")),
    )

    with pytest.raises(ActionExecutionError, match="Test action failed"):
        RuleEngine((rule,)).evaluate()


def test_rule_engine_stops_after_action_execution_error() -> None:
    first_rule = Rule(
        name="Failing test rule",
        condition=Dummy_Condition(given_result=True),
        action=Dummy_Action(given_exception=ActionExecutionError("Test action failed")),
    )

    second_condition = Dummy_Condition(given_result=True)
    second_action = Dummy_Action()

    second_rule = Rule(
        name="Second test rule",
        condition=second_condition,
        action=second_action,
    )

    with pytest.raises(ActionExecutionError):
        RuleEngine((first_rule, second_rule)).evaluate()

    assert second_condition.evaluation_count == 0
    assert second_action.execution_count == 0


def test_rule_engine_find_match_returns_matching_rule() -> None:
    condition = Dummy_Condition(given_result=True)
    action = Dummy_Action()

    rule = Rule(
        name="Test rule",
        condition=condition,
        action=action,
    )

    matched_rule = RuleEngine((rule,)).find_match()

    assert matched_rule is rule
    assert condition.evaluation_count == 1
    assert action.execution_count == 0


def test_rule_engine_find_match_returns_none_when_no_rule_matches() -> None:
    rule = Rule(
        name="Test rule",
        condition=Dummy_Condition(given_result=False),
        action=Dummy_Action(),
    )

    matched_rule = RuleEngine((rule,)).find_match()

    assert matched_rule is None


def test_rule_engine_find_match_returns_first_matching_rule() -> None:
    first_rule = Rule(
        name="First rule",
        condition=Dummy_Condition(given_result=True),
        action=Dummy_Action(),
    )

    second_rule = Rule(
        name="Second rule",
        condition=Dummy_Condition(given_result=True),
        action=Dummy_Action(),
    )

    matched_rule = RuleEngine((first_rule, second_rule)).find_match()

    assert matched_rule is first_rule
    assert second_rule.condition.evaluation_count == 0  # type: ignore (a "real" condition does not have this attribute, but the dummy condition does)
