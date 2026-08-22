from datetime import time
from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from powerrules.config.loader import ConfigurationLoader


def test_configuration_loader_loads_valid_configuration(tmp_path: Path) -> None:
    configuration_file = tmp_path / "powerrules.yaml"
    configuration_file.write_text(
        """
rules:
  - name: "Shutdown after backup"
    conditions:
      process:
        name: "backup.exe"
        running: false
    action:
      type: shutdown
""",
        encoding="utf-8",
    )

    configuration = ConfigurationLoader().load(configuration_file)

    assert len(configuration.rules) == 1
    assert configuration.rules[0].name == "Shutdown after backup"
    assert configuration.rules[0].enabled is True


def test_configuration_loader_parses_datetime_values(tmp_path: Path) -> None:
    configuration_file = tmp_path / "powerrules.yaml"
    configuration_file.write_text(
        """
rules:
  - name: "Night rule"
    conditions:
      datetime:
        between:
          start: "22:30:15"
          end: "7"
    action:
      type: shutdown
""",
        encoding="utf-8",
    )

    configuration = ConfigurationLoader().load(configuration_file)

    condition = configuration.rules[0].conditions.datetime

    assert condition is not None
    assert condition.between is not None
    assert condition.between.start == time(22, 30, 15)
    assert condition.between.end == time(7, 0)


def test_configuration_loader_rejects_invalid_configuration(tmp_path: Path) -> None:
    configuration_file = tmp_path / "powerrules.yaml"
    configuration_file.write_text(
        """
rules:
  - name: "Invalid rule"
    conditions:
      process:
        name: "backup.exe"
        running: "false"
    action:
      type: shutdown
""",
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        ConfigurationLoader().load(configuration_file)


def test_configuration_loader_rejects_invalid_yaml(tmp_path: Path) -> None:
    configuration_file = tmp_path / "powerrules.yaml"
    configuration_file.write_text(
        # The missing closing quote is intentional
        """
rules:
  - name: "Broken rule
    action:
      type: shutdown
""",
        encoding="utf-8",
    )

    with pytest.raises(yaml.YAMLError):
        ConfigurationLoader().load(configuration_file)


def test_configuration_loader_raises_for_missing_file(tmp_path: Path) -> None:
    configuration_file = tmp_path / "missing.yaml"

    with pytest.raises(FileNotFoundError):
        ConfigurationLoader().load(configuration_file)
