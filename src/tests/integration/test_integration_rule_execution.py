from datetime import datetime
from pathlib import Path

from powerrules.actions.power import ShutdownAction
from powerrules.config.builder import ConfigurationBuilder
from powerrules.config.loader import ConfigurationLoader
from powerrules.engine.models import Rule
from powerrules.engine.rule_engine import RuleEngine


class Dummy_ClockProvider:
    def __init__(self, current_datetime: datetime):
        self.current_datetime = current_datetime

    def now(self) -> datetime:
        return self.current_datetime


class Dummy_ProcessProvider:
    def __init__(self, is_running: bool = False):
        self.is_running_result = is_running

    def is_running(self, process_name: str) -> bool:
        return self.is_running_result


class Dummy_PowerProvider:
    def __init__(self):
        self.shutdown_count = 0
        self.sleep_count = 0
        self.hibernate_count = 0
        self.reboot_count = 0

    def shutdown(self) -> None:
        self.shutdown_count += 1

    def sleep(self) -> None:
        self.sleep_count += 1

    def hibernate(self) -> None:
        self.hibernate_count += 1

    def reboot(self) -> None:
        self.reboot_count += 1


def test_rule_execution_from_yaml_configuration(tmp_path: Path) -> None:
    configuration_file = tmp_path / "powerrules.yaml"
    configuration_file.write_text(
        """
rules:
  - name: "Shutdown after backup"
    conditions:
      and:
        - process:
            name: "backup.exe"
            running: false
        - datetime:
            between:
                start: "23:00"
                end: "6:00"
    action:
      type: shutdown
""",
        encoding="utf-8",
    )

    # REMOVE
    clock_provider = Dummy_ClockProvider(datetime(2026, 8, 22, 1, 30))
    process_provider = Dummy_ProcessProvider(is_running=False)
    power_provider = Dummy_PowerProvider()

    configuration = ConfigurationLoader().load(configuration_file)

    rule_set = ConfigurationBuilder(
        clock_provider=clock_provider,
        process_provider=process_provider,
        power_provider=power_provider,
    ).build(configuration)

    result = RuleEngine(rule_set.rules).evaluate()

    assert result.matched_rule is not None
    assert result.matched_rule.name == "Shutdown after backup"
    assert isinstance(result.matched_rule, Rule)
    assert isinstance(result.matched_rule.action, ShutdownAction)
    assert power_provider.shutdown_count == 1


def test_rule_execution_from_yaml_configuration_returns_no_match(
    tmp_path: Path,
) -> None:
    configuration_file = tmp_path / "powerrules.yaml"
    configuration_file.write_text(
        """
rules:
  - name: "Shutdown after backup"
    conditions:
      and:
        - process:
            name: "backup.exe"
            running: false
        - datetime:
            between:
                start: "23:00"
                end: "6:00"
    action:
      type: shutdown
""",
        encoding="utf-8",
    )

    clock_provider = Dummy_ClockProvider(datetime(2026, 8, 22, 22, 30))
    process_provider = Dummy_ProcessProvider(is_running=False)
    power_provider = Dummy_PowerProvider()

    configuration = ConfigurationLoader().load(configuration_file)

    rule_set = ConfigurationBuilder(
        clock_provider=clock_provider,
        process_provider=process_provider,
        power_provider=power_provider,
    ).build(configuration)

    result = RuleEngine(rule_set.rules).evaluate()

    assert result.matched_rule is None
    assert power_provider.shutdown_count == 0


def test_rule_execution_uses_first_matching_rule(tmp_path: Path) -> None:
    configuration_file = tmp_path / "powerrules.yaml"
    configuration_file.write_text(
        """
rules:
  - name: "Sleep"
    conditions:
      datetime:
        between:
          start: "22:00"
          end: "0:00"
    action:
      type: sleep

  - name: "Shutdown"
    conditions:
      datetime:
        between:
          start: "23:00"
          end: "6:00"
    action:
      type: shutdown
""",
        encoding="utf-8",
    )

    clock_provider = Dummy_ClockProvider(datetime(2026, 8, 22, 23, 30))
    power_provider = Dummy_PowerProvider()

    configuration = ConfigurationLoader().load(configuration_file)

    rule_set = ConfigurationBuilder(
        clock_provider=clock_provider,
        process_provider=Dummy_ProcessProvider(),
        power_provider=power_provider,
    ).build(configuration)

    result = RuleEngine(rule_set.rules).evaluate()

    assert result.matched_rule is not None
    assert result.matched_rule.name == "Sleep"
    assert power_provider.sleep_count == 1
    assert power_provider.shutdown_count == 0
