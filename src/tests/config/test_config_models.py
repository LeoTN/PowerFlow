import pytest

from powerrules.config.models import Configuration
from powerrules.engine.models import Rule


class Dummy_Condition:
    def evaluate(self) -> bool:
        return True


class Dummy_Action:
    def execute(self) -> None:
        pass


def test_configuration_contains_rules() -> None:
    rule = Rule(
        name="Test rule",
        condition=Dummy_Condition(),
        action=Dummy_Action(),
    )

    configuration = Configuration(rules=(rule,))

    assert configuration.rules == (rule,)


def test_configuration_can_contain_multiple_rules() -> None:
    first_rule = Rule(
        name="First rule",
        condition=Dummy_Condition(),
        action=Dummy_Action(),
    )

    second_rule = Rule(
        name="Second rule",
        condition=Dummy_Condition(),
        action=Dummy_Action(),
    )

    configuration = Configuration(
        rules=(first_rule, second_rule),
    )

    assert configuration.rules == (
        first_rule,
        second_rule,
    )


def test_configuration_is_immutable() -> None:
    configuration = Configuration(rules=())

    with pytest.raises(AttributeError):
        configuration.rules = ()  # type: ignore (ignore this Pylance error even though it is correct)
