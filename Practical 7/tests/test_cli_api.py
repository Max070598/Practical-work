from cli.commands.game_commands import GameCommands
from unittest.mock import Mock, patch

def test_list_chars(mocker):
    game = Mock()
    cmd = GameCommands(game)
    mocker.patch.object(cmd.api, "get_characters_list", return_value=["Zhongli", "Raiden"])
    result = cmd.list(["chars"])
    assert "Zhongli" in result

def test_create_api_char(mocker):
    game = Mock()
    cmd = GameCommands(game)
    mock_char = Mock(name="Zhongli", rarity=5)
    mocker.patch("game_system.core.character.Character.from_api", return_value=mock_char)
    result = cmd.create(["char", "--api", "zhongli"])
    assert "Zhongli" in result