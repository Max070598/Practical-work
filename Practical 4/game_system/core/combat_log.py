class CombatLog:
    """Class to manage combat log messages."""
    
    def __init__(self):
        self._log = []

    def add_message(self, message: str) -> None:
        """Add a message to the log."""
        self._log.append(message)

    def get_log(self) -> list:
        """Get all log messages."""
        return self._log

    def clear(self) -> None:
        """Clear the log."""
        self._log = []