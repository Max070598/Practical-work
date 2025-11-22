import json
import os
from .irepository import IRepository
from typing import Any

class JsonFileRepository(IRepository):
    def __init__(self, folder: str = "data"):
        self.folder = folder
        os.makedirs(folder, exist_ok=True)

    def _get_path(self, key: str) -> str:
        return os.path.join(self.folder, f"{key}.json")

    def save(self, key: str, data: Any) -> None:
        path = self._get_path(key)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self, key: str) -> Any:
        path = self._get_path(key)
        if not os.path.exists(path):
            return None
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)