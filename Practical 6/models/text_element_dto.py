from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TextElementDTO:
    type: str
    content: str
    level: Optional[int] = None
    url: Optional[str] = None
    children: List['TextElementDTO'] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []