from datetime import datetime, time

from powerrules.actions.power import (
    HibernateAction,
    RebootAction,
    ShutdownAction,
    SleepAction,
)
from powerrules.conditions.datetime import DateTimeCondition, TimeRange, Weekday
from powerrules.conditions.operators import AndCondition, OrCondition
from powerrules.conditions.process import ProcessCondition
from powerrules.config.builder import ConfigurationBuilder
from powerrules.config.models import (
    ActionConfiguration,
    ConditionConfiguration,
    DateTimeConditionConfiguration,
    ProcessConditionConfiguration,
    RuleConfiguration,
    RuleSetConfiguration,
    TimeRangeConfiguration,
)
from powerrules.engine.models import RuleSet
from tests.dummies import (
    Dummy_ClockProvider,
    Dummy_PowerProvider,
    Dummy_ProcessProvider,
)


def test_configuration_builder_builds_rule_set() -> None:
    configuration = RuleSetConfiguration(
        rules=[
            RuleConfiguration(
                name="Test rule",
                conditions=ConditionConfiguration(
                    process=ProcessConditionConfiguration(
                        name="backup.exe",
                        running=False,
                    )
                ),
                action=ActionConfiguration(
                    type="shutdown",
                ),
            )
        ]
    )

    builder = ConfigurationBuilder(
        clock_provider=Dummy_ClockProvider(datetime(2026, 8, 22, 12, 0)),
        process_provider=Dummy_ProcessProvider(given_is_running=True),
        power_provider=Dummy_PowerProvider(),
    )

    rule_set = builder.build(configuration)

    assert isinstance(rule_set, RuleSet)
    assert len(rule_set.rules) == 1


def test_configuration_builder_preserves_rule_properties() -> None:
    configuration = RuleSetConfiguration(
        rules=[
            RuleConfiguration(
                name="Test rule",
                enabled=False,
                conditions=ConditionConfiguration(
                    process=ProcessConditionConfiguration(
                        name="backup.exe",
                        running=False,
                    )
                ),
                action=ActionConfiguration(
                    type="shutdown",
                ),
            )
        ]
    )

    builder = ConfigurationBuilder(
        clock_provider=Dummy_ClockProvider(datetime(2026, 8, 22, 12, 0)),
        process_provider=Dummy_ProcessProvider(given_is_running=True),
        power_provider=Dummy_PowerProvider(),
    )

    rule_set = builder.build(configuration)

    rule = rule_set.rules[0]

    assert rule.name == "Test rule"
    assert rule.enabled is False


def test_configuration_builder_builds_process_condition() -> None:
    process_provider = Dummy_ProcessProvider(given_is_running=True)

    configuration = RuleSetConfiguration(
        rules=[
            RuleConfiguration(
                name="Process test rule",
                conditions=ConditionConfiguration(
                    process=ProcessConditionConfiguration(
                        name="backup.exe",
                        running=False,
                    )
                ),
                action=ActionConfiguration(
                    type="shutdown",
                ),
            )
        ]
    )

    builder = ConfigurationBuilder(
        clock_provider=Dummy_ClockProvider(datetime(2026, 8, 22, 12, 0)),
        process_provider=process_provider,
        power_provider=Dummy_PowerProvider(),
    )

    rule = builder.build(configuration).rules[0]

    assert isinstance(rule.condition, ProcessCondition)
    assert rule.condition.process_name == "backup.exe"
    assert rule.condition.expected_running is False
    assert rule.condition.process_provider is process_provider


#########################
# DateTimeCondition tests
#########################


def test_configuration_builder_builds_datetime_between_condition() -> None:
    clock_provider = Dummy_ClockProvider(datetime(2026, 8, 22, 12, 0))

    configuration = RuleSetConfiguration(
        rules=[
            RuleConfiguration(
                name="Datetime rule",
                conditions=ConditionConfiguration(
                    datetime=DateTimeConditionConfiguration(
                        between=TimeRangeConfiguration(
                            start=time(22, 0),
                            end=time(6, 0),
                        ),
                    )
                ),
                action=ActionConfiguration(
                    type="shutdown",
                ),
            )
        ]
    )

    builder = ConfigurationBuilder(
        clock_provider=clock_provider,
        process_provider=Dummy_ProcessProvider(given_is_running=True),
        power_provider=Dummy_PowerProvider(),
    )

    rule = builder.build(configuration).rules[0]

    assert isinstance(rule.condition, DateTimeCondition)
    assert rule.condition.clock_provider is clock_provider
    assert rule.condition.time_range == TimeRange(
        start=time(22, 0),
        end=time(6, 0),
    )


def test_configuration_builder_builds_datetime_weekday_condition() -> None:
    configuration = RuleSetConfiguration(
        rules=[
            RuleConfiguration(
                name="Weekend test rule",
                conditions=ConditionConfiguration(
                    datetime=DateTimeConditionConfiguration(
                        weekday=[
                            Weekday.SATURDAY,
                            Weekday.SUNDAY,
                        ]
                    )
                ),
                action=ActionConfiguration(
                    type="sleep",
                ),
            )
        ]
    )

    builder = ConfigurationBuilder(
        clock_provider=Dummy_ClockProvider(datetime(2026, 8, 22, 12, 0)),
        process_provider=Dummy_ProcessProvider(given_is_running=True),
        power_provider=Dummy_PowerProvider(),
    )

    rule = builder.build(configuration).rules[0]

    assert isinstance(rule.condition, DateTimeCondition)
    assert rule.condition.weekdays == frozenset(
        {
            Weekday.SATURDAY,
            Weekday.SUNDAY,
        }
    )


##############
# Action tests
##############


def test_configuration_builder_builds_shutdown_action() -> None:
    power_provider = Dummy_PowerProvider()

    configuration = RuleSetConfiguration(
        rules=[
            RuleConfiguration(
                name="Shutdown test rule",
                conditions=ConditionConfiguration(
                    process=ProcessConditionConfiguration(
                        name="backup.exe",
                        running=False,
                    )
                ),
                action=ActionConfiguration(type="shutdown"),
            ),
        ]
    )

    builder = ConfigurationBuilder(
        clock_provider=Dummy_ClockProvider(datetime(2026, 8, 22, 12, 0)),
        process_provider=Dummy_ProcessProvider(given_is_running=True),
        power_provider=power_provider,
    )

    rule = builder.build(configuration).rules[0]

    assert isinstance(rule.action, ShutdownAction)
    assert rule.action.power_provider is power_provider


def test_configuration_builder_builds_sleep_action() -> None:
    power_provider = Dummy_PowerProvider()

    configuration = RuleSetConfiguration(
        rules=[
            RuleConfiguration(
                name="Sleep test rule",
                conditions=ConditionConfiguration(
                    process=ProcessConditionConfiguration(
                        name="backup.exe",
                        running=False,
                    )
                ),
                action=ActionConfiguration(type="sleep"),
            ),
        ]
    )

    builder = ConfigurationBuilder(
        clock_provider=Dummy_ClockProvider(datetime(2026, 8, 22, 12, 0)),
        process_provider=Dummy_ProcessProvider(given_is_running=True),
        power_provider=power_provider,
    )

    rule = builder.build(configuration).rules[0]

    assert isinstance(rule.action, SleepAction)
    assert rule.action.power_provider is power_provider


def test_configuration_builder_builds_hibernate_action() -> None:
    power_provider = Dummy_PowerProvider()

    configuration = RuleSetConfiguration(
        rules=[
            RuleConfiguration(
                name="Hibernate test rule",
                conditions=ConditionConfiguration(
                    process=ProcessConditionConfiguration(
                        name="backup.exe",
                        running=False,
                    )
                ),
                action=ActionConfiguration(type="hibernate"),
            ),
        ]
    )

    builder = ConfigurationBuilder(
        clock_provider=Dummy_ClockProvider(datetime(2026, 8, 22, 12, 0)),
        process_provider=Dummy_ProcessProvider(given_is_running=True),
        power_provider=power_provider,
    )

    rule = builder.build(configuration).rules[0]

    assert isinstance(rule.action, HibernateAction)
    assert rule.action.power_provider is power_provider


def test_configuration_builder_builds_reboot_action() -> None:
    power_provider = Dummy_PowerProvider()

    configuration = RuleSetConfiguration(
        rules=[
            RuleConfiguration(
                name="Reboot test rule",
                conditions=ConditionConfiguration(
                    process=ProcessConditionConfiguration(
                        name="backup.exe",
                        running=False,
                    )
                ),
                action=ActionConfiguration(type="reboot"),
            ),
        ]
    )

    builder = ConfigurationBuilder(
        clock_provider=Dummy_ClockProvider(datetime(2026, 8, 22, 12, 0)),
        process_provider=Dummy_ProcessProvider(given_is_running=True),
        power_provider=power_provider,
    )

    rule = builder.build(configuration).rules[0]

    assert isinstance(rule.action, RebootAction)
    assert rule.action.power_provider is power_provider


######################
# Multiple rules tests
######################


def test_configuration_builder_preserves_rule_order() -> None:
    configuration = RuleSetConfiguration(
        rules=[
            RuleConfiguration(
                name="First test rule",
                conditions=ConditionConfiguration(
                    process=ProcessConditionConfiguration(
                        name="first.exe",
                        running=False,
                    )
                ),
                action=ActionConfiguration(
                    type="shutdown",
                ),
            ),
            RuleConfiguration(
                name="Second test rule",
                conditions=ConditionConfiguration(
                    process=ProcessConditionConfiguration(
                        name="second.exe",
                        running=False,
                    )
                ),
                action=ActionConfiguration(
                    type="sleep",
                ),
            ),
        ]
    )

    builder = ConfigurationBuilder(
        clock_provider=Dummy_ClockProvider(datetime(2026, 8, 22, 12, 0)),
        process_provider=Dummy_ProcessProvider(given_is_running=True),
        power_provider=Dummy_PowerProvider(),
    )

    rule_set = builder.build(configuration)

    assert [rule.name for rule in rule_set.rules] == [
        "First test rule",
        "Second test rule",
    ]


def test_configuration_builder_builds_nested_conditions() -> None:
    configuration = RuleSetConfiguration(
        rules=[
            RuleConfiguration(
                name="Nested test rule",
                conditions=ConditionConfiguration(
                    and_conditions=[
                        ConditionConfiguration(
                            process=ProcessConditionConfiguration(
                                name="backup.exe",
                                running=False,
                            )
                        ),
                        ConditionConfiguration(
                            or_conditions=[
                                ConditionConfiguration(
                                    datetime=DateTimeConditionConfiguration(
                                        between=TimeRangeConfiguration(
                                            start=time(23, 0),
                                            end=time(0, 0),
                                        ),
                                    )
                                ),
                                ConditionConfiguration(
                                    process=ProcessConditionConfiguration(
                                        name="maintenance.exe",
                                        running=True,
                                    )
                                ),
                            ]
                        ),
                    ]
                ),
                action=ActionConfiguration(
                    type="shutdown",
                ),
            )
        ]
    )

    builder = ConfigurationBuilder(
        clock_provider=Dummy_ClockProvider(datetime(2026, 8, 22, 12, 0)),
        process_provider=Dummy_ProcessProvider(given_is_running=True),
        power_provider=Dummy_PowerProvider(),
    )

    rule = builder.build(configuration).rules[0]

    assert isinstance(rule.condition, AndCondition)
    assert isinstance(rule.condition.conditions[0], ProcessCondition)
    assert isinstance(rule.condition.conditions[1], OrCondition)
    assert isinstance(rule.condition.conditions[1].conditions[0], DateTimeCondition)
    assert isinstance(rule.condition.conditions[1].conditions[1], ProcessCondition)
