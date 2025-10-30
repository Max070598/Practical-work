from .leaf import Leaf

class Link(Leaf):
    """Class representing a hyperlink."""
    
    def __init__(self, text: str, url: str):
        super().__init__(text)
        self._url = url
    
    def render(self) -> str:
        """Render the link in markdown format."""
        return f"[{self.content}]({self._url})"
    
    def render_toc(self, indent: int = 0) -> str:
        """Links do not appear in the table of contents."""
        return ""