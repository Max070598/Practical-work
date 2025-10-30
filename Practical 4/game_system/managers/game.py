from ..core.character import Character
from ..core.item import Item
from ..core.ability import Ability
from ..core.combat_log import CombatLog

class Game:
    """Class to manage the game flow and interactions."""
    
    def __init__(self):
        self._characters = []
        self._combat_log = CombatLog()

    def add_character(self, character: Character) -> None:
        """Add a character to the game."""
        self._characters.append(character)

    def setup_battle(self) -> None:
        """Setup initial battle conditions (e.g., equip items, assign abilities)."""
        if len(self._characters) < 2:
            raise ValueError("At least two characters are required for a battle.")
        
        warrior = self._characters[0]
        mage = self._characters[1]
        warrior.equip_item(Item("Iron Armor", armor_bonus=5))
        mage.equip_item(Item("Magic Wand", attack_bonus=5))
        warrior._abilities.append(Ability("Shield Bash", lambda u, t: t._set_health(t._get_health() - 10)))
        mage._abilities.append(Ability("Fireball", lambda u, t: t._set_health(t._get_health() - 20)))

    def run_battle(self) -> None:
        """Simulate a battle between characters."""
        self._combat_log.clear()
        self._combat_log.add_message("Battle Start!")
        
        warrior, mage = self._characters
        damage = warrior.attack_target(mage)
        self._combat_log.add_message(f"{warrior.name} attacks {mage.name} for {damage} damage. {mage.name}'s health: {mage._get_health()}")
        self._combat_log.add_message(f"{mage.name} uses Fireball on {warrior.name}")
        mage.use_ability(mage._abilities[0], warrior)
        warrior.heal(10)
        self._combat_log.add_message(f"{warrior.name} heals for 10. Health: {warrior._get_health()}")
        self._combat_log.add_message(f"{warrior.name} uses Shield Bash on {mage.name}")
        warrior.use_ability(warrior._abilities[0], mage)
        damage = mage.attack_target(warrior)
        self._combat_log.add_message(f"{mage.name} attacks {warrior.name} for {damage} damage. {warrior.name}'s health: {warrior._get_health()}")

    def get_combat_log(self) -> list:
        """Get the combat log."""
        return self._combat_log.get_log()