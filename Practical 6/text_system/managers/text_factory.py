from ..core.container import Container
from ..core.paragraph import Paragraph
from ..core.heading import Heading
from ..core.link import Link
from ..core.image import Image
from models.text_element_dto import TextElementDTO
from infra.display.idisplayer import IDisplayer
from infra.data.irepository import IRepository
from dataclasses import asdict
import uuid

class TextFactory:
    def __init__(self, displayer: IDisplayer, repository: IRepository):
        self._document = Container()
        self.elements = {}
        self._displayer = displayer
        self._repository = repository

    def _to_dto(self, element) -> TextElementDTO:
        if isinstance(element, Heading):
            return TextElementDTO("heading", element.content, level=element._level)
        elif isinstance(element, Paragraph):
            return TextElementDTO("paragraph", element.content)
        elif isinstance(element, Link):
            return TextElementDTO("link", element.content, url=element._url)
        elif isinstance(element, Image):
            return TextElementDTO("image", element.content, url=element._url)
        return TextElementDTO("unknown", str(element))

    def add_paragraph(self, content: str) -> str:
        paragraph = Paragraph(content)
        element_id = str(uuid.uuid4())
        self.elements[element_id] = paragraph
        self._document.add_child(paragraph)
        self._displayer.write_line(f"Added paragraph: {content}")
        return element_id

    def add_heading(self, content: str, level: int) -> str:
        heading = Heading(content, level)
        element_id = str(uuid.uuid4())
        self.elements[element_id] = heading
        self._document.add_child(heading)
        self._displayer.write_line(f"Added heading: {content}")
        return element_id

    def remove_element(self, index: int) -> None:
        if 0 <= index < len(self._document._children):
            self._document.remove_child(index)
            self._displayer.write_line(f"Removed element at index {index}")

    def swap_elements(self, index1: int, index2: int) -> None:
        self._document.swap_children(index1, index2)
        self._displayer.write_line(f"Swapped elements {index1} <-> {index2}")

    def render(self) -> str:
        return self._document.render()

    def render_toc(self) -> str:
        return self._document.render_toc()

    def save_document(self, name: str):
        dto_list = [asdict(self._to_dto(child)) for child in self._document._children]
        self._repository.save(f"text_{name}", dto_list)
        self._displayer.write_line(f"Document saved: data/text_{name}.json")

    def load_document(self, name: str):
        data = self._repository.load(f"text_{name}")
        if not data:
            self._displayer.write_line("No saved document found.")
            return
        self._document = Container()
        self.elements.clear()
        for item in data:
            if item["type"] == "heading":
                self.add_heading(item["content"], item["level"] or 1)
            elif item["type"] == "paragraph":
                self.add_paragraph(item["content"])
        self._displayer.write_line(f"Loaded document: text_{name}.json")