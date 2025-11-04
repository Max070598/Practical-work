# cli/commands/game_commands.py
from game_system.managers.game import Game
from game_system.core.character import Character
from game_system.core.item import Item
from game_system.core.ability import Ability

class GameCommands:
    def __init__(self, game: Game):
        self.game = game
        self.characters = {}
        self.items = {}
        self.abilities = {}

    def create(self, args: list) -> str:
        if not args:
            return "Usage: create <char|item|ability>"
        obj_type = args[0].lower()
        if obj_type == "char":
            name = input("Enter character name: ")
            health = int(input("Enter health: "))
            armor = int(input("Enter armor: "))
            attack = int(input("Enter attack: "))
            char = Character(name, health, armor, attack)
            self.game.add_character(char)
            self.characters[name] = char
            return f"Created character: {name}"
        elif obj_type == "item":
            name = input("Enter item name: ")
            health_bonus = int(input("Enter health bonus: "))
            armor_bonus = int(input("Enter armor bonus (0 if none): "))
            attack_bonus = int(input("Enter attack bonus (0 if none): "))
            self.items[name] = Item(name, health_bonus, armor_bonus, attack_bonus)
            return f"Created item: {name}"
        elif obj_type == "ability":
            name = input("Enter ability name: ")
            self.abilities[name] = Ability(name, lambda u, t: None)
            return f"Created ability: {name}"
        return "Unsupported type"

    def add_to_char(self, args: list) -> str:
        if "--char_id" not in args or "--id" not in args:
            return "Usage: add_to_char --char_id <id/name> --id <item/ability_id>"
        char_id_idx = args.index("--char_id") + 1
        id_idx = args.index("--id") + 1
        if char_id_idx >= len(args) or id_idx >= len(args):
            return "Invalid IDs"
        char_id = args[char_id_idx]
        item_id = args[id_idx]
        if char_id in self.characters and item_id in self.items:
            item = self.items[item_id]
            self.characters[char_id].equip_item(item)
            return f"Added {item_id} to {char_id}"
        elif char_id in self.characters and item_id in self.abilities:
            self.characters[char_id].add_ability(self.abilities[item_id])
            return f"Added ability {item_id} to {char_id}"
        return "Invalid IDs"

    def act(self, args: list) -> str:
        if len(args) < 2:
            return "Usage: act <attack|heal|ability> <actor> [<target>] [--id <id/name>]"
        action = args[0].lower()
        actor = args[1]
        if actor not in self.characters:
            return "Invalid actor"
        if action == "heal" and len(args) == 2:
            self.characters[actor].heal(10)
            return f"{actor} healed for 10"
        elif len(args) < 3:
            return "Usage: act <attack|heal|ability> <actor> <target> [--id <id/name>]"
        target = args[2]
        if target not in self.characters:
            return "Invalid target"
        if "--id" in args:
            id_idx = args.index("--id") + 1
            if id_idx < len(args):
                ability_id = args[id_idx]
                if ability_id in self.abilities:
                    self.abilities[ability_id](self.characters[actor], self.characters[target])
                    return f"{actor} used ability {ability_id} on {target}"
        if action == "attack" and actor != target:
            damage = self.characters[actor].attack_target(self.characters[target])
            return f"{actor} attacked {target} for {damage} damage"
        elif action == "attack" and actor == target:
            return "Cannot attack yourself!"
        return "Invalid action"

    def ls(self, args: list) -> str:
        if not args:
            return "\n".join([f"Char: {k}" for k in self.characters.keys()] +
                           [f"Item: {k}" for k in self.items.keys()] +
                           [f"Ability: {k}" for k in self.abilities.keys()])
        if "--id" in args:
            id_idx = args.index("--id") + 1
            if id_idx < len(args):
                id_val = args[id_idx]
                if id_val in self.characters:
                    char = self.characters[id_val]
                    return f"Char {id_val}: Name={char.name}, Health={char.health}, Armor={char.armor}, Attack={char.attack}"
                elif id_val in self.items:
                    item = self.items[id_val]
                    return f"Item {id_val}: Name={item.name}, Health Bonus={item.health_bonus}, Armor Bonus={item.armor_bonus}, Attack Bonus={item.attack_bonus}"
                elif id_val in self.abilities:
                    return f"Ability {id_val}: Name={self.abilities[id_val].name}"
        return "Invalid ID"
    
    def save(self, args: list) -> str:
        if not args:
            return "Usage: save <name>"
        self.game.save_game(args[0])
        return ""

    def load(self, args: list) -> str:
        if not args:
            return "Usage: load <name>"
        self.game.load_game(args[0])
        return ""    