import pytest

from powerrules.engine.models import Rule


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
