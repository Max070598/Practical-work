from game_system.core.character import Character
from game_system.core.item import Item

def test_character_attack():
    warrior = Character("Warrior", 100, 10, 15)
    mage = Character("Mage", 80, 5, 10)
    damage = warrior.attack_target(mage)
    assert damage == 10
    assert mage.health == 70

def test_equip_item():
    char = Character("Hero", 100, 10, 15)
    char.equip_item(Item("Sword", attack_bonus=5))
    assert char.attack == 20