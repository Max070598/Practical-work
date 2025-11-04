from .managers.game import Game
from .core.character import Character

def main():
    """Demonstrate the refactored game system functionality."""
    game = Game()
    warrior = Character("Warrior", health=100, armor=10, attack=15)
    mage = Character("Mage", health=80, armor=5, attack=10)
    game.add_character(warrior)
    game.add_character(mage)
    game.setup_battle()
    game.run_battle()
    
    for message in game.get_combat_log():
        print(message)

if __name__ == "__main__":
    main()