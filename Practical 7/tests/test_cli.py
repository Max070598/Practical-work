from cli.command_interface import CLI
from unittest.mock import Mock

def test_cli_add_heading(mocker):
    displayer = Mock()
    repo = Mock()
    repo.load.return_value = None

    cli = CLI(displayer=displayer, repository=repo)

    mocker.patch('builtins.input', side_effect=[
        "add_text container heading", "Test", "1", "exit"
    ])

    cli.parse_args(["--text"])

    displayer.write_line.assert_any_call("Added heading: Test")


def test_cli_save(mocker):
    displayer = Mock()
    repo = Mock()

    cli = CLI(displayer=displayer, repository=repo)

    mocker.patch('builtins.input', side_effect=[
        "add_text container heading", "Doc", "1", "save test", "exit"
    ])

    cli.parse_args(["--text"])

    repo.save.assert_called_once()
    args = repo.save.call_args[0]
    assert args[0] == "text_test"  