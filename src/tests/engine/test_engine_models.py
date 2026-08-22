import pytest

from powerrules.engine.models import Rule, RuleSet


class Dummy_Condition:
    def evaluate(self) -> bool:
        return True


class Dummy_Action:
    def execute(self) -> None:
        pass


def test_rule_uses_expected_defaults() -> None:
    condition = Dummy_Condition()
    action = Dummy_Action()

    rule = Rule(
        name="Test rule",
        condition=condition,
        action=action,
    )

    assert rule.name == "Test rule"
    assert rule.condition is condition
    assert rule.action is action
    assert rule.enabled is True


def test_rule_can_be_disabled() -> None:
    rule = Rule(
        name="Disabled test rule",
        condition=Dummy_Condition(),
        action=Dummy_Action(),
        enabled=False,
    )

    assert rule.enabled is False


def test_rule_is_immutable() -> None:
    rule = Rule(
        name="Test rule",
        condition=Dummy_Condition(),
        action=Dummy_Action(),
    )

    with pytest.raises(AttributeError):
        rule.name = "Modified rule"  # type: ignore (ignore this Pylance error even though it is correct)


###############
# RuleSet tests
###############


def test_rule_set_contains_rules() -> None:
    rule = Rule(
        name="Test rule",
        condition=Dummy_Condition(),
        action=Dummy_Action(),
    )

    rule_set = RuleSet(rules=(rule,))

    assert rule_set.rules == (rule,)


def test_rule_set_can_contain_multiple_rules() -> None:
    first_rule = Rule(
        name="First test rule",
        condition=Dummy_Condition(),
        action=Dummy_Action(),
    )

    second_rule = Rule(
        name="Second test rule",
        condition=Dummy_Condition(),
        action=Dummy_Action(),
    )

    rule_set = RuleSet(rules=(first_rule, second_rule))

    assert rule_set.rules == (
        first_rule,
        second_rule,
    )


def test_rule_set_is_immutable() -> None:
    rule_set = RuleSet(rules=())

    with pytest.raises(AttributeError):
        rule_set.rules = ()  # type: ignore (ignore this Pylance error even though it is correct)
