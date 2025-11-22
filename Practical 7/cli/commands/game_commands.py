# cli/commands/game_commands.py
from game_system.managers.game import Game
from game_system.core.character import Character
from game_system.core.item import Item
from game_system.core.ability import Ability
from infra.api.genshin_api import GenshinAPI
from typing import Dict, List


class GameCommands:
    def __init__(self, game: Game):
        self.game = game
        self.characters: Dict[str, Character] = {}
        self.items: Dict[str, Item] = {}
        self.abilities: Dict[str, Ability] = {}
        self.api = GenshinAPI()  # ← Для тестів

    def create(self, args: List[str]) -> str:
        if not args:
            return "Usage: create <char|item|ability> [--api <name>]"

        obj_type = args[0].lower()
        use_api = "--api" in args
        api_name = None
        if use_api:
            idx = args.index("--api") + 1
            if idx < len(args):
                api_name = args[idx]

        if use_api and api_name:
            if obj_type == "char":
                try:
                    char = Character.from_api(api_name)
                    char_id = char.name
                    self.game.add_character(char)
                    self.characters[char_id] = char
                    return f"Created character from API: {char.name} (ID: {char_id})"
                except Exception as e:
                    return f"Failed to create from API: {e}"
            elif obj_type == "item":
                try:
                    item = Item.from_api(api_name)
                    item_id = item._name
                    self.items[item_id] = item
                    return f"Created weapon from API: {item._name} (ID: {item_id})"
                except Exception as e:
                    return f"Failed to create weapon from API: {e}"

        if obj_type == "char":
            name = input("Enter character name: ")
            health = int(input("Enter health: "))
            armor = int(input("Enter armor: "))
            attack = int(input("Enter attack: "))
            char = Character(name, health, armor, attack)
            char_id = name
            self.game.add_character(char)
            self.characters[char_id] = char
            return f"Created character: {name} (ID: {char_id})"

        elif obj_type == "item":
            name = input("Enter item name: ")
            health_bonus = int(input("Enter health bonus: "))
            armor_bonus = int(input("Enter armor bonus (0 if none): "))
            attack_bonus = int(input("Enter attack bonus (0 if none): "))
            item = Item(name, health_bonus, armor_bonus, attack_bonus)
            item_id = name
            self.items[item_id] = item
            return f"Created item: {name} (ID: {item_id})"

        elif obj_type == "ability":
            name = input("Enter ability name: ")
            ability = Ability(name, lambda u, t: None)
            ability_id = name
            self.abilities[ability_id] = ability
            return f"Created ability: {name} (ID: {ability_id})"

        return "Unsupported type"

    def add_to_char(self, args: List[str]) -> str:
        if "--char_id" not in args or "--id" not in args:
            return "Usage: add_to_char --char_id <char_name> --id <item_or_ability_name>"

        try:
            char_id_idx = args.index("--char_id") + 1
            id_idx = args.index("--id") + 1
        except ValueError:
            return "Invalid flags"

        if char_id_idx >= len(args) or id_idx >= len(args):
            return "Missing ID values"

        char_id = args[char_id_idx]
        item_id_parts = args[id_idx:]
        if not item_id_parts:
            return "Item/Ability ID required"
        item_id = " ".join(item_id_parts)

        if char_id not in self.characters:
            return f"Character '{char_id}' not found"
        if item_id not in self.items and item_id not in self.abilities:
            return f"Item/Ability '{item_id}' not found"

        if item_id in self.items:
            item = self.items[item_id]
            self.characters[char_id].equip_item(item)
            return f"Added item '{item_id}' to '{char_id}' (Attack: {self.characters[char_id].attack})"

        elif item_id in self.abilities:
            ability = self.abilities[item_id]
            self.characters[char_id].add_ability(ability)
            return f"Added ability '{item_id}' to '{char_id}'"

        return "Error"

    def act(self, args: List[str]) -> str:
        if len(args) < 3:
            return "Usage: act <attack|heal> <char_id> [target_id]"

        action = args[0].lower()
        char_id = args[1]
        target_id = args[2] if len(args) > 2 else None

        if char_id not in self.characters:
            return f"Character '{char_id}' not found"

        char = self.characters[char_id]

        if action == "attack":
            if not target_id or target_id not in self.characters:
                return "Target not found"
            target = self.characters[target_id]
            damage = max(1, char.attack - target.armor)
            target.take_damage(damage)
            return f"{char.name} attacked {target.name} for {damage} damage"

        elif action == "heal":
            char.heal(10)
            return f"{char.name} healed for 10"

        return "Unknown action"

    def ls(self, args: List[str]) -> str:
        if not args:
            lines = []
            lines.extend([f"Char: {k} (ID: {k})" for k in self.characters.keys()])
            lines.extend([f"Item: {k} (ID: {k})" for k in self.items.keys()])
            lines.extend([f"Ability: {k} (ID: {k})" for k in self.abilities.keys()])
            return "\n".join(lines) if lines else "No objects"

        if "--id" in args:
            try:
                id_idx = args.index("--id") + 1
            except ValueError:
                return "Invalid --id flag"
            if id_idx >= len(args):
                return "Missing ID"

            search_id = " ".join(args[id_idx:])

            if search_id in self.characters:
                char = self.characters[search_id]
                return (f"Char {search_id}:\n"
                        f"  Name: {char.name}\n"
                        f"  Health: {char.health}\n"
                        f"  Armor: {char.armor}\n"
                        f"  Attack: {char.attack}")

            elif search_id in self.items:
                item = self.items[search_id]
                return (f"Item {search_id}:\n"
                        f"  Health Bonus: {item.health_bonus}\n"
                        f"  Armor Bonus: {item.armor_bonus}\n"
                        f"  Attack Bonus: {item.attack_bonus}")

            elif search_id in self.abilities:
                return f"Ability {search_id}: {self.abilities[search_id].name}"

            return f"ID '{search_id}' not found"

        return "Invalid command"

    def list(self, args: List[str]) -> str:
        if not args or args[0] != "chars":
            return "Usage: list chars"
        try:
            chars = self.api.get_characters_list()
            return "Available characters:\n" + "\n".join([f"- {c}" for c in chars])
        except Exception as e:
            return f"Failed to fetch characters: {e}"

    def print_char(self, args: List[str]) -> str:
        if len(args) < 2 or args[0] != "char":
            return "Usage: print char <id/name>"
        char_id = " ".join(args[1:])
        if char_id not in self.characters:
            return f"Character '{char_id}' not found"
        from text_system.managers.text_factory import TextFactory
        factory = TextFactory(self.game._displayer, self.game._repository)
        return factory.render_character(self.characters[char_id])

    def save(self, args: List[str]) -> str:
        if not args:
            return "Usage: save <name>"
        self.game.save_game(args[0])
        return f"Game saved as {args[0]}"

    def load(self, args: List[str]) -> str:
        if not args:
            return "Usage: load <name>"
        self.game.load_game(args[0])
        return f"Game loaded: {args[0]}"