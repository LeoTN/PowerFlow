from collections.abc import Sequence

from powerrules.conditions.base import Condition


class AndCondition:
    def __init__(self, conditions: Sequence[Condition]):
        self.conditions = tuple(conditions)

    def evaluate(self) -> bool:
        """Evaluate all conditions using logical AND.

        Returns:
            True if all conditions match, otherwise False.

        Raises:
            ConditionEvaluationError: If a condition cannot be evaluated.
        """
        return all(condition.evaluate() for condition in self.conditions)


class OrCondition:
    def __init__(self, conditions: Sequence[Condition]):
        self.conditions = tuple(conditions)

    def evaluate(self) -> bool:
        """Evaluate all conditions using logical OR.

        Returns:
            True if at least one condition matches, otherwise False.

        Raises:
            ConditionEvaluationError: If a condition cannot be evaluated.
        """
        return any(condition.evaluate() for condition in self.conditions)
