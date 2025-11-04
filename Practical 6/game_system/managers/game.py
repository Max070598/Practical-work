from ..core.character import Character
from ..core.item import Item
from ..core.ability import Ability
from models.character_dto import CharacterDTO, ItemDTO, AbilityDTO
from infra.display.idisplayer import IDisplayer
from infra.data.irepository import IRepository
from dataclasses import asdict

class Game:
    def __init__(self, displayer: IDisplayer, repository: IRepository):
        self._characters = []
        self._displayer = displayer
        self._repository = repository

    def _to_dto(self, char: Character) -> CharacterDTO:
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
        self._characters.append(character)
        self._displayer.write_line(f"Added character: {character.name}")

    def save_game(self, name: str):
        dto_list = [asdict(self._to_dto(char)) for char in self._characters]
        self._repository.save(f"game_{name}", dto_list)
        self._displayer.write_line(f"Game saved: data/game_{name}.json")

    def load_game(self, name: str):
        data = self._repository.load(f"game_{name}")
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
        self._displayer.write_line(f"Loaded game: game_{name}.json")