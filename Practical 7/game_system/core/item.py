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

    @classmethod
    def from_api(cls, name: str):
        """Create item from Genshin API weapon data."""
        from infra.api.genshin_api import GenshinAPI
        api = GenshinAPI()
        data = api.get_weapon(name)
        bonuses = data["bonuses"]
        return cls(
            name=data["name"],
            health_bonus=bonuses["health_bonus"],
            armor_bonus=bonuses["armor_bonus"],
            attack_bonus=bonuses["attack_bonus"]
        )