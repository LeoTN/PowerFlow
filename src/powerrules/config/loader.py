from pathlib import Path

import yaml

from powerrules.config.models import RuleSetConfiguration


class ConfigurationLoader:
    """Load and validate PowerRules configuration files."""

    def load(self, path: Path) -> RuleSetConfiguration:
        """Load and validate a PowerRules configuration file.

        Args:
            path: Path to the YAML configuration file.

        Returns:
            Validated PowerRules configuration.

        Raises:
            OSError: If the configuration file cannot be read.
            yaml.YAMLError: If the YAML cannot be parsed.
            ValidationError: If the configuration is invalid.
        """
        with path.open("r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        return RuleSetConfiguration.model_validate(data)
