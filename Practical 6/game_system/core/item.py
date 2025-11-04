class Item:
    """Class representing an equippable item with encapsulated bonuses."""
    
    def __init__(self, name: str, health_bonus: int = 0, armor_bonus: int = 0, attack_bonus: int = 0):
        self._name = name
        self._health_bonus = health_bonus
        self._armor_bonus = armor_bonus
        self._attack_bonus = attack_bonus

    @property
    def health_bonus(self) -> int:
        """Public accessor for health bonus."""
        return self._health_bonus

    @property
    def armor_bonus(self) -> int:
        """Public accessor for armor bonus."""
        return self._armor_bonus

    @property
    def attack_bonus(self) -> int:
        """Public accessor for attack bonus."""
        return self._attack_bonus