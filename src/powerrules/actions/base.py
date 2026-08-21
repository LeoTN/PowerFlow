from typing import Protocol


class Action(Protocol):
    def execute(self) -> None:
        """Execute the action.

        Raises:
            ActionExecutionError: If the action cannot be executed.
        """
        ...
