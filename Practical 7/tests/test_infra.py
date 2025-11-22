from infra.display.console_displayer import ConsoleDisplayer
from infra.data.json_repository import JsonFileRepository
import tempfile
import os

def test_console_displayer(mocker):
    mock_print = mocker.patch('builtins.print')
    ConsoleDisplayer().write_line("Hello")
    mock_print.assert_called_with("Hello")

def test_json_repository():
    with tempfile.TemporaryDirectory() as tmp:
        repo = JsonFileRepository(folder=tmp)
        data = {"key": "value"}
        repo.save("test", data)
        assert repo.load("test") == data
        assert os.path.exists(os.path.join(tmp, "test.json"))