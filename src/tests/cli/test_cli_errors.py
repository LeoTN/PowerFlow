import pytest
import typer
from pydantic import ValidationError

from powerrules.cli.errors import (
    EXIT_POLICY_ERROR,
    EXIT_RUNTIME_ERROR,
    cli_command,
    handle_cli_error,
)
from powerrules.engine.exceptions import ConditionEvaluationError
from tests.dummies import Dummy_Model


def test_cli_error_handler_handles_missing_policy() -> None:
    error = FileNotFoundError(2, "File not found", "policy.yaml")

    with pytest.raises(typer.Exit) as exc_info:
        handle_cli_error(error)

    assert exc_info.value.exit_code == EXIT_POLICY_ERROR


def test_cli_error_handler_reports_missing_policy(
    capsys: pytest.CaptureFixture[str],
) -> None:
    error = FileNotFoundError(2, "File not found", "policy.yaml")

    with pytest.raises(typer.Exit):
        handle_cli_error(error)

    captured = capsys.readouterr()

    assert "[ERROR] Policy file not found: policy.yaml" in captured.err


def test_cli_error_handler_handles_validation_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(ValidationError) as exc_info:
        Dummy_Model.model_validate({"enabled": "invalid"})

    with pytest.raises(typer.Exit) as exit_info:
        handle_cli_error(exc_info.value)

    captured = capsys.readouterr()

    assert exit_info.value.exit_code == EXIT_POLICY_ERROR
    assert "[ERROR] Policy validation failed" in captured.err
    assert "enabled" in captured.err


def test_cli_error_handler_handles_condition_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    error = ConditionEvaluationError("Test condition failed")

    with pytest.raises(typer.Exit) as exc_info:
        handle_cli_error(error)

    captured = capsys.readouterr()

    assert exc_info.value.exit_code == EXIT_RUNTIME_ERROR
    # The message is wrapped by "handle_cli_error()"
    assert "[ERROR] Failed to evaluate condition: Test condition failed" in captured.err


def test_cli_command_handles_command_exception(
    capsys: pytest.CaptureFixture[str],
) -> None:
    @cli_command
    def failing_command() -> None:
        raise ConditionEvaluationError("Test condition failed")

    with pytest.raises(typer.Exit) as exc_info:
        failing_command()

    captured = capsys.readouterr()

    assert exc_info.value.exit_code == EXIT_RUNTIME_ERROR
    # The message is wrapped by "handle_cli_error()"
    assert "[ERROR] Failed to evaluate condition: Test condition failed" in captured.err


def test_cli_command_does_not_intercept_typer_exit() -> None:
    @cli_command
    def exiting_command() -> None:
        raise typer.Exit(code=42)

    with pytest.raises(typer.Exit) as exc_info:
        exiting_command()

    assert exc_info.value.exit_code == 42
