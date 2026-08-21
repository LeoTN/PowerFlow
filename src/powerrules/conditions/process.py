from powerrules.engine.exceptions import ConditionEvaluationError
from powerrules.providers.processes import ProcessProvider


class ProcessCondition:
    def __init__(
        self,
        process_name: str,
        expected_running: bool,
        # Basically a wrapper object to interact with the OS to provide information about the running processes
        process_provider: ProcessProvider,
    ):
        self.process_name = process_name
        self.expected_running = expected_running
        self.process_provider = process_provider

    def evaluate(self) -> bool:
        """Evaluate whether the configured process is in the expected state.

        Returns:
            True if the process state matches the expected state.

        Raises:
            ConditionEvaluationError: If the process state cannot be determined.
        """
        try:
            is_running = self.process_provider.is_running(self.process_name)
        except Exception as e:
            raise ConditionEvaluationError(
                f"Failed to determine whether process '{self.process_name}' is running."
            ) from e

        return is_running == self.expected_running
