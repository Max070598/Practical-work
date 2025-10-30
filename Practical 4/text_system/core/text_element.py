from abc import ABC, abstractmethod

class ITextElement(ABC):
    """Abstract base class representing a text element."""
    
    @abstractmethod
    def render(self) -> str:
        """Render the element as a string."""
        pass
    
    @abstractmethod
    def render_toc(self, indent: int = 0) -> str:
        """Render the element for table of contents with indentation."""
        pass