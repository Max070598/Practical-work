# cli/commands/text_commands.py
from text_system.managers.text_factory import TextFactory
import uuid

class TextCommands:
    def __init__(self, text_factory: TextFactory):
        self.text_factory = text_factory
        self.current_path = ["/"]

    def pwd(self, args: list) -> str:
        normalized_path = "/" + "/".join(self.current_path[1:]).lstrip("/") if len(self.current_path) > 1 else "/"
        return f"Current path: {normalized_path}"

    def print(self, args: list) -> str:
        if "--whole" in args:
            result = self.text_factory.render()
            return f"{result} [ID: {uuid.uuid4()}]" if result else "Document is empty"
        if "--id" in args:
            id_idx = args.index("--id") + 1
            if id_idx < len(args):
                return f"Element with ID {args[id_idx]}"
        result = self.text_factory.render()
        return f"{result} [ID: {uuid.uuid4()}]" if result else "Current element is empty"

    def add(self, args: list) -> str:
        if len(args) < 2:
            return "Usage: add <container|leaf> <type>"
        element_type = args[0].lower()
        specific_type = args[1].lower()
        if element_type == "container" and specific_type == "heading":
            content = input("Enter heading content: ")
            self.text_factory.add_heading(content, 1)
            return f"Added heading: {content}"
        elif element_type == "leaf" and specific_type == "paragraph":
            content = input("Enter paragraph content: ")
            self.text_factory.add_paragraph(content)
            return f"Added paragraph: {content}"
        return "Unsupported type combination"

    def rm(self, args: list) -> str:
        if args:
            confirm = input(f"Remove {args[0]}? (y/n): ")
            if confirm.lower() == "y":
                return f"Removed {args[0]}"
            return "Removal cancelled"
        confirm = input("Remove current element? (y/n): ")
        if confirm.lower() == "y":
            return "Removed current element"
        return "Removal cancelled"

    def up(self, args: list) -> str:
        if len(self.current_path) > 1:
            self.current_path.pop()
        normalized_path = "/" + "/".join(self.current_path[1:]).lstrip("/") if len(self.current_path) > 1 else "/"
        return f"Moved up to: {normalized_path}"

    def cd(self, args: list) -> str:
        if not args:
            return "Usage: cd <path> or --id <container_id>"
        if "--id" in args:
            id_idx = args.index("--id") + 1
            if id_idx < len(args):
                return f"Changed to container with ID {args[id_idx]}"
        path = args[0].lstrip("/") if "--id" not in args else args[args.index("--id") - 1].lstrip("/")
        if path and path not in self.current_path[-1:]:
            self.current_path.append(path)
        normalized_path = "/" + "/".join(self.current_path[1:]).lstrip("/") if len(self.current_path) > 1 else "/"
        return f"Changed to: {normalized_path}"