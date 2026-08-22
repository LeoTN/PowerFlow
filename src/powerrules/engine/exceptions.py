class PowerRulesError(Exception):
    """Base exception for PowerRules errors."""


class ConditionEvaluationError(PowerRulesError):
    """Raised when a condition cannot be evaluated."""


class ActionExecutionError(PowerRulesError):
    """Raised when an action cannot be executed."""


class ConfigurationError(PowerRulesError):
    """Raised when a configuration cannot be converted into a rule set."""
