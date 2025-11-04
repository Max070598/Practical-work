from .idisplayer import IDisplayer

class ConsoleDisplayer(IDisplayer):
    def write(self, message: str) -> None:
        print(message, end="")

    def write_line(self, message: str = "") -> None:
        print(message)