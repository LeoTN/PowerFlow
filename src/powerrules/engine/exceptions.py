class PowerRulesError(Exception):
    """Base exception for PowerRules errors."""


class ConditionEvaluationError(PowerRulesError):
    """Raised when a condition cannot be evaluated."""


class ActionExecutionError(PowerRulesError):
    """Raised when an action cannot be executed."""
