# cli/command_interface.py
from enum import Enum
import sys
from typing import Dict, Callable
from text_system.managers.text_factory import TextFactory
from game_system.managers.game import Game
from cli.commands.text_commands import TextCommands
from cli.commands.game_commands import GameCommands


class Mode(Enum):
    TEXT = "text"
    CHARACTERS = "chars"


class CLI:
    """Command Line Interface for managing text and game systems."""
    
    def __init__(self, displayer=None, repository=None):
        from infra.display.console_displayer import ConsoleDisplayer
        from infra.data.json_repository import JsonFileRepository
        
        self.displayer = displayer or ConsoleDisplayer()
        self.repository = repository or JsonFileRepository()
        self.text_factory = TextFactory(self.displayer, self.repository)
        self.game = Game(self.displayer, self.repository)
        self.commands: Dict[str, Callable[[list], str]] = {}
        self.current_mode = None
        self.text_cmd = TextCommands(self.text_factory)
        self.game_cmd = GameCommands(self.game)

    def _register_text_commands(self):
        """Register commands for TEXT mode."""
        self.commands.update({
            "save": lambda args: self.text_cmd.save(args),
            "load": lambda args: self.text_cmd.load(args),
            "pwd": lambda args: self.text_cmd.pwd(args),
            "print": lambda args: self.text_cmd.print(args),
            "add_text": lambda args: self.text_cmd.add_text(args),
            "rm": lambda args: self.text_cmd.rm(args),
            "up": lambda args: self.text_cmd.up(args),
            "cd": lambda args: self.text_cmd.cd(args)
        })

    def _register_game_commands(self):
        """Register commands for CHARACTERS mode."""
        self.commands.update({
            "create": lambda args: self.game_cmd.create(args),
            "add_to_char": lambda args: self.game_cmd.add_to_char(args),
            "act": lambda args: self.game_cmd.act(args),
            "ls": lambda args: self.game_cmd.ls(args),
            "list": lambda args: self.game_cmd.list(args),
            "save": lambda args: self.game_cmd.save(args),
            "load": lambda args: self.game_cmd.load(args),
            "print": lambda args: self.game_cmd.print_char(args)
        })

    def _register_commands(self):
        """Register commands based on selected mode."""
        if self.current_mode == Mode.TEXT:
            self._register_text_commands()
        elif self.current_mode == Mode.CHARACTERS:
            self._register_game_commands()

    def parse_args(self, args: list) -> None:
        """Parse command-line arguments to set mode."""
        mode_set = False
        for arg in args:
            if arg in ["--text", "-t"]:
                self.current_mode = Mode.TEXT
                mode_set = True
                break
            elif arg in ["--chars", "-c"]:
                self.current_mode = Mode.CHARACTERS
                mode_set = True
                break

        if not mode_set:
            self._interactive_mode_prompt()
        else:
            self._register_commands()
            self._start_interpreter()

    def _interactive_mode_prompt(self):
        """Prompt user to select mode interactively."""
        print("Select mode: 1) Text, 2) Characters")
        choice = input("> ").strip()
        self.current_mode = Mode.TEXT if choice == "1" else Mode.CHARACTERS
        self._register_commands()
        self._start_interpreter()

    def _start_interpreter(self):
        """Start the command interpreter loop."""
        print(f"Entered {self.current_mode.value} mode. Type 'exit' to quit.")
        while True:
            try:
                command = input("> ").strip()
                if not command:
                    continue
                parts = command.split()
                cmd = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []

                if cmd == "exit":
                    break

                self._execute_command(cmd, args)
            except EOFError:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")

    def _execute_command(self, cmd: str, args: list) -> None:
        """Execute the selected command."""
        if cmd in self.commands:
            try:
                result = self.commands[cmd](args)
                if result:
                    print(result)
            except Exception as e:
                print(f"Command error: {e}")
        else:
            print("Unknown command. Use 'exit' to quit.")


if __name__ == "__main__":
    cli = CLI()
    cli.parse_args(sys.argv[1:])