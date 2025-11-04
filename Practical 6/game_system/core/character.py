# game_system/core/character.py
from typing import List

from game_system.core.ability import Ability
from .item import Item

class Character:
    """Class representing a game character with encapsulated attributes."""
    
    def __init__(self, name: str, health: int, armor: int, attack: int):
        self._name = name
        self._max_health = health
        self._health = health
        self._armor = armor
        self._attack = attack
        self._items: List[Item] = []
        self._abilities: List['Ability'] = []

    @property
    def name(self) -> str:
        """Public accessor for name."""
        return self._name

    @property
    def health(self) -> int:
        """Public accessor for current health."""
        return self._get_health()

    @property
    def armor(self) -> int:
        """Public accessor for armor."""
        return self._armor

    @property
    def attack(self) -> int:
        """Public accessor for attack."""
        return self._attack

    def _get_health(self) -> int:
        """Get current health (protected accessor)."""
        return self._health

    def _set_health(self, value: int) -> None:
        """Set health with validation (protected modifier)."""
        self._health = max(0, min(self._max_health, value))

    def equip_item(self, item: Item) -> None:
        """Equip an item and apply its bonuses."""
        self._items.append(item)
        self._max_health += item.health_bonus
        self._set_health(self._health + item.health_bonus)
        self._armor += item.armor_bonus
        self._attack += item.attack_bonus

    def attack_target(self, target: 'Character') -> int:
        """Attack another character and return damage."""
        damage = max(0, self._attack - target._armor)
        target._set_health(target._get_health() - damage)
        return damage

    def heal(self, amount: int) -> None:
        """Heal the character up to max health."""
        self._set_health(self._get_health() + amount)

    def use_ability(self, ability, target: 'Character') -> None:
        """Use a specific ability on a target."""
        from .ability import Ability
        if isinstance(ability, str):
            for ab in self._abilities:
                if ab.name == ability:
                    ability = ab
                    break
        if hasattr(ability, 'use'):
            ability.use(self, target)

    def is_alive(self) -> bool:
        """Check if the character is alive."""
        return self._health > 0