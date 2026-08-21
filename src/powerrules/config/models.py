from dataclasses import dataclass

from powerrules.engine.models import Rule


@dataclass(frozen=True)
class Configuration:
    """PowerRules configuration which will be imported from the YAML file."""

    rules: tuple[Rule, ...]
