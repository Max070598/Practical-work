from .leaf import Leaf

class Heading(Leaf):
    """Class representing a heading with a specified level."""
    
    def __init__(self, content: str, level: int):
        super().__init__(content)
        self._level = max(1, min(level, 6))  # Ensure level is between 1 and 6
    
    def render(self) -> str:
        """Render the heading with markdown-style prefix."""
        return f"{'#' * self._level} {self.content}"
    
    def render_toc(self, indent: int = 0) -> str:
        """Render the heading for table of contents with indentation."""
        return "  " * indent + f"- {self.content}"