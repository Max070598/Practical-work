# game_system/managers/game.py
from ..core.character import Character
from ..core.item import Item
from ..core.ability import Ability
from models.character_dto import CharacterDTO, ItemDTO, AbilityDTO
from infra.display.idisplayer import IDisplayer
from infra.data.irepository import IRepository
from dataclasses import asdict
from typing import List


class Game:
    def __init__(self, displayer: IDisplayer, repository: IRepository):
        self._characters: List[Character] = []
        self._displayer = displayer
        self._repository = repository

    def _to_dto(self, char: Character) -> CharacterDTO:
        """Convert Character to DTO."""
        return CharacterDTO(
            name=char.name,
            health=char.health,
            max_health=char._max_health,
            armor=char.armor,
            attack=char.attack,
            items=[ItemDTO(i._name, i.health_bonus, i.armor_bonus, i.attack_bonus) for i in char._items],
            abilities=[AbilityDTO(a.name) for a in char._abilities]
        )

    def add_character(self, character: Character) -> None:
        """Add a character to the game."""
        self._characters.append(character)
        self._displayer.write_line(f"Added character: {character.name}")

    def save_game(self, name: str) -> None:
        """Save game with 'game_' prefix (without .json)."""
        filename = f"game_{name}"
        dto_list = [asdict(self._to_dto(char)) for char in self._characters]
        self._repository.save(filename, dto_list)
        self._displayer.write_line(f"Game saved: data/{filename}.json")

    def load_game(self, name: str) -> None:
        """Load game with 'game_' prefix (without .json)."""
        filename = f"game_{name}" 
        data = self._repository.load(filename)
        if not data:
            self._displayer.write_line("No saved game found.")
            return

        self._characters = []
        for d in data:
            char = Character(d["name"], d["max_health"], d["armor"], d["attack"])
            char._set_health(d["health"])
            for item in d["items"]:
                char.equip_item(Item(item["name"], item["health_bonus"], item["armor_bonus"], item["attack_bonus"]))
            for ab in d["abilities"]:
                char._abilities.append(Ability(ab["name"], lambda u, t: None))
            self.add_character(char)
        self._displayer.write_line(f"Loaded game: {filename}.json")