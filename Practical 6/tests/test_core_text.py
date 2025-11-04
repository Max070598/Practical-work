from text_system.core.container import Container
from text_system.core.heading import Heading
from text_system.core.paragraph import Paragraph

def test_container_render():
    container = Container()
    container.add_child(Heading("H1", 1))
    container.add_child(Paragraph("Text"))
    assert container.render() == "# H1\nText"

def test_heading_render():
    assert Heading("Title", 2).render() == "## Title"

def test_paragraph_render():
    assert Paragraph("Hello").render() == "Hello"