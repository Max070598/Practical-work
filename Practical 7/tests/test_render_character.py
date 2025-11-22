from text_system.managers.text_factory import TextFactory
from game_system.core.character import Character
from unittest.mock import Mock

def test_render_character():
    factory = TextFactory(Mock(), Mock())
    char = Character("Test", 100, 10, 15, rarity=5, description="Hero", element="Pyro")
    result = factory.render_character(char)
    assert "# Test (★★★★★)" in result
    assert "Health | 100" in result
    assert "Pyro" in result