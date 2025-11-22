from cli.command_interface import CLI
import sys

if __name__ == "__main__":
    cli = CLI()
    cli.parse_args(sys.argv)