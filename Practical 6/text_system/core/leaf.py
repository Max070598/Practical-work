from .text_element import ITextElement

class Leaf(ITextElement):
    """Abstract base class for leaf elements that hold content."""
    
    def __init__(self, content: str):
        self._content = content if content else ""
    
    @property
    def content(self) -> str:
        """Get the content of the leaf element."""
        return self._content

    def render(self) -> str:
        """Render the leaf content."""
        return self._content
    
    def render_toc(self, indent: int = 0) -> str:
        """Leaf elements do not appear in the table of contents by default."""
        return ""