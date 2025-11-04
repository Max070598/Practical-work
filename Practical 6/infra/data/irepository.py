from abc import ABC, abstractmethod
from typing import Any

class IRepository(ABC):
    @abstractmethod
    def save(self, key: str, data: Any) -> None:
        pass

    @abstractmethod
    def load(self, key: str) -> Any:
        pass