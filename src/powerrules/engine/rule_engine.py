from collections.abc import Sequence

from powerrules.engine.models import Rule, RuleEvaluationResult


class RuleEngine:
    def __init__(self, rules: Sequence[Rule]):
        self.rules = tuple(rules)

    def find_match(self) -> Rule | None:
        """Find the first enabled rule whose condition matches.

        Returns:
            The first matching rule, or None if no rule matches.

        Raises:
            ConditionEvaluationError: If a condition cannot be evaluated.
        """
        for rule in self.rules:
            if not rule.enabled:
                continue

            if rule.condition.evaluate():
                return rule

        return None

    def evaluate(self) -> RuleEvaluationResult:
        """Evaluate rules and execute the first matching action.

        Returns:
            The result of the rule evaluation.

        Raises:
            ConditionEvaluationError: If a condition cannot be evaluated.
            ActionExecutionError: If a matching action cannot be executed.
        """
        matched_rule = self.find_match()

        if matched_rule is None:
            return RuleEvaluationResult(matched_rule=None)

        # Execute the action, e.g. reboot or shutdown etc.
        matched_rule.action.execute()

        return RuleEvaluationResult(matched_rule=matched_rule)
