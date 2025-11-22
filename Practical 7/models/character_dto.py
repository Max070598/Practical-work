from dataclasses import dataclass
from typing import List

@dataclass
class ItemDTO:
    name: str
    health_bonus: int = 0
    armor_bonus: int = 0
    attack_bonus: int = 0

@dataclass
class AbilityDTO:
    name: str

@dataclass
class CharacterDTO:
    name: str
    health: int
    max_health: int
    armor: int
    attack: int
    items: List[ItemDTO] = None
    abilities: List[AbilityDTO] = None

    def __post_init__(self):
        if self.items is None:
            self.items = []
        if self.abilities is None:
            self.abilities = []