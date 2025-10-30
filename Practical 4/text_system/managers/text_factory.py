# text_system/managers/text_factory.py
from ..core.container import Container
from ..core.paragraph import Paragraph
from ..core.heading import Heading
from ..core.link import Link
from ..core.image import Image
import uuid

class TextFactory:
    """Factory class to manage the creation of structured text with unique identifiers."""
    
    def __init__(self):
        self._document = Container()
        self.elements = {}
    
    def add_paragraph(self, content: str) -> str:
        """Add a paragraph to the document and return its unique ID."""
        paragraph = Paragraph(content)
        element_id = str(uuid.uuid4())
        self.elements[element_id] = paragraph
        self._document.add_child(paragraph)
        return element_id
    
    def add_heading(self, content: str, level: int) -> str:
        """Add a heading to the document and return its unique ID."""
        heading = Heading(content, level)
        element_id = str(uuid.uuid4())
        self.elements[element_id] = heading
        self._document.add_child(heading)
        return element_id
    
    def add_link(self, text: str, url: str) -> str:
        """Add a link to the document and return its unique ID."""
        link = Link(text, url)
        element_id = str(uuid.uuid4())
        self.elements[element_id] = link
        self._document.add_child(link)
        return element_id
    
    def add_image(self, caption: str, url: str) -> str:
        """Add an image to the document and return its unique ID."""
        image = Image(caption, url)
        element_id = str(uuid.uuid4())
        self.elements[element_id] = image
        self._document.add_child(image)
        return element_id
    
    def remove_element(self, index: int) -> None:
        """Remove an element from the document by index."""
        child = self._document.get_child(index)
        if child:
            for id_key, elem in list(self.elements.items()):
                if elem == child:
                    del self.elements[id_key]
                    break
            self._document.remove_child(index)
    
    def swap_elements(self, index1: int, index2: int) -> None:
        """Swap two elements in the document."""
        self._document.swap_children(index1, index2)
    
    def render(self) -> str:
        """Render the entire document."""
        return self._document.render()
    
    def render_toc(self) -> str:
        """Render the table of contents."""
        return self._document.render_toc()
    
    def get_element_by_id(self, element_id: str) -> object:
        """Return element by its unique ID."""
        return self.elements.get(element_id)