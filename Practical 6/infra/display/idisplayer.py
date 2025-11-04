from abc import ABC, abstractmethod

class IDisplayer(ABC):
    @abstractmethod
    def write(self, message: str) -> None:
        pass

    @abstractmethod
    def write_line(self, message: str = "") -> None:
        pass