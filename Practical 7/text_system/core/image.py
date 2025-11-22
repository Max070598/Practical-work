from .leaf import Leaf

class Image(Leaf):
    """Class representing an image with a caption and URL."""
    
    def __init__(self, caption: str, url: str):
        super().__init__(caption)
        self._url = url
    
    def render(self) -> str:
        """Render the image in markdown format."""
        return f"![{self.content}]({self._url})"
    
    def render_toc(self, indent: int = 0) -> str:
        """Images do not appear in the table of contents."""
        return ""