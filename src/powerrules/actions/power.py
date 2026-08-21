from powerrules.engine.exceptions import ActionExecutionError
from powerrules.providers.power import PowerProvider


class ShutdownAction:
    def __init__(self, power_provider: PowerProvider):
        self.power_provider = power_provider

    def execute(self) -> None:
        """Shut down the computer.

        Raises:
            ActionExecutionError: If the computer cannot be shut down.
        """
        try:
            self.power_provider.shutdown()
        except Exception as e:
            raise ActionExecutionError("Failed to shut down the computer") from e


class SleepAction:
    def __init__(self, power_provider: PowerProvider):
        self.power_provider = power_provider

    def execute(self) -> None:
        """Put the computer into sleep mode.

        Raises:
            ActionExecutionError: If the computer cannot be put into sleep mode.
        """
        try:
            self.power_provider.sleep()
        except Exception as e:
            raise ActionExecutionError(
                "Failed to put the computer into sleep mode"
            ) from e


class HibernateAction:
    def __init__(self, power_provider: PowerProvider):
        self.power_provider = power_provider

    def execute(self) -> None:
        """Put the computer into hibernation.

        Raises:
            ActionExecutionError: If the computer cannot be put into hibernation.
        """
        try:
            self.power_provider.hibernate()
        except Exception as e:
            raise ActionExecutionError(
                "Failed to put the computer into hibernation"
            ) from e


class RebootAction:
    def __init__(self, power_provider: PowerProvider):
        self.power_provider = power_provider

    def execute(self) -> None:
        """Reboot the computer.

        Raises:
            ActionExecutionError: If the computer cannot be rebooted.
        """
        try:
            self.power_provider.reboot()
        except Exception as e:
            raise ActionExecutionError("Failed to reboot the computer") from e
