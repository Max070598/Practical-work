from .leaf import Leaf

class Paragraph(Leaf):
    """Class representing a paragraph of text."""
    
    def render(self) -> str:
        """Render the paragraph as plain text."""
        return self.content
    
    def render_toc(self, indent: int = 0) -> str:
        """Paragraphs do not appear in the table of contents."""
        return ""