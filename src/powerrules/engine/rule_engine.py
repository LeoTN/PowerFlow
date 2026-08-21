from collections.abc import Sequence

from powerrules.engine.models import Rule, RuleEvaluationResult


class RuleEngine:
    def __init__(self, rules: Sequence[Rule]):
        self.rules = tuple(rules)

    def evaluate(self) -> RuleEvaluationResult:
        """Evaluate rules from top to bottom.

        Returns:
            The result of the rule evaluation.

        Raises:
            ConditionEvaluationError: If a condition cannot be evaluated.
            ActionExecutionError: If an action cannot be executed.
        """
        for rule in self.rules:
            if not rule.enabled:
                continue

            if not rule.condition.evaluate():
                continue

            rule.action.execute()

            return RuleEvaluationResult(matched_rule=rule)

        return RuleEvaluationResult(matched_rule=None)
