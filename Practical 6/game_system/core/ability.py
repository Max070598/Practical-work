from typing import Callable

class Ability:
    """Class representing a character's unique ability."""
    
    def __init__(self, name: str, effect: Callable):
        self._name = name
        self._effect = effect

    def use(self, user, target):
        """Apply the ability's effect."""
        self._effect(user, target)

    @property
    def name(self) -> str:
        """Public accessor for ability name."""
        return self._name