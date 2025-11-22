# game_system/core/character.py
from typing import List
from game_system.core.ability import Ability
from .item import Item


class Character:
    def __init__(self, name: str, max_health: int, armor: int, base_attack: int,
                 rarity: int = 1, description: str = "", abilities=None, element: str = ""):
        self._name = name
        self._max_health = max_health
        self._health = max_health
        self._armor = armor
        self._base_attack = base_attack
        self.rarity = rarity
        self.description = description
        self.abilities = abilities or []
        self.element = element
        self._items: List[Item] = []
        self._abilities: List[Ability] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def health(self) -> int:
        return self._get_health()

    @property
    def armor(self) -> int:
        return self._armor

    @property
    def attack(self) -> int:
        return self._base_attack + sum(item.attack_bonus for item in self._items)

    def _get_health(self) -> int:
        return self._health

    def _set_health(self, value: int) -> None:
        self._health = max(0, min(self._max_health, value))

    def equip_item(self, item: Item) -> None:
        if item in self._items:
            return
        self._items.append(item)
        self._max_health += item.health_bonus
        self._health = min(self._health + item.health_bonus, self._max_health)
        self._armor += item.armor_bonus

    def take_damage(self, damage: int) -> None:
        self._set_health(self._get_health() - damage)

    def attack_target(self, target: 'Character') -> int:
        damage = max(0, self.attack - target.armor)
        target.take_damage(damage)
        return damage

    def heal(self, amount: int) -> None:
        self._set_health(self._get_health() + amount)

    def add_ability(self, ability: Ability) -> None:
        if ability not in self._abilities:
            self._abilities.append(ability)

    def use_ability(self, ability, target: 'Character') -> None:
        if isinstance(ability, str):
            for ab in self._abilities:
                if ab.name == ability:
                    ability = ab
                    break
        if hasattr(ability, 'use'):
            ability.use(self, target)

    def is_alive(self) -> bool:
        return self._health > 0

    @classmethod
    def from_api(cls, name: str):
        from infra.api.genshin_api import GenshinAPI
        api = GenshinAPI()
        data = api.get_character(name)
        stats = data["generated_stats"]
        return cls(
            name=data["name"],
            max_health=stats["health"],
            armor=stats["armor"],
            base_attack=stats["attack"],
            rarity=data["rarity"],
            description=data.get("description", "No description available"),
            abilities=data.get("skills", []),
            element=data.get("element", "Unknown")
        )