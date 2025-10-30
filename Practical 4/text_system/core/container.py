from typing import List
from .text_element import ITextElement

class Container(ITextElement):
    """Abstract base class for container elements that hold other elements."""
    
    def __init__(self):
        self._children: List[ITextElement] = []
    
    def add_child(self, element: ITextElement) -> None:
        """Add a child element to the container."""
        self._children.append(element)
    
    def remove_child(self, index: int) -> None:
        """Remove a child element by index."""
        if 0 <= index < len(self._children):
            self._children.pop(index)
    
    def swap_children(self, index1: int, index2: int) -> None:
        """Swap two child elements by their indices."""
        if 0 <= index1 < len(self._children) and 0 <= index2 < len(self._children):
            self._children[index1], self._children[index2] = self._children[index2], self._children[index1]
    
    def render(self) -> str:
        """Render all child elements as a single string."""
        return "\n".join(child.render() for child in self._children)
    
    def render_toc(self, indent: int = 0) -> str:
        """Render the table of contents for all children with indentation."""
        return "\n".join(child.render_toc(indent + 1) for child in self._children if child.render_toc(indent + 1))