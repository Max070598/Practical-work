from .managers.text_factory import TextFactory

def main():
    """Demonstrate the refactored text system functionality."""
    factory = TextFactory()
    
    # Build a document
    factory.add_heading("Introduction", 1)
    factory.add_paragraph("This is an introductory paragraph about the project.")
    factory.add_link("Learn More", "https://example.com")
    factory.add_heading("Details", 2)
    factory.add_image("Project Diagram", "https://example.com/diagram.png")
    
    # Render the document
    print("Full Document:")
    print(factory.render())
    print("\nTable of Contents:")
    print(factory.render_toc())
    
    # Swap elements for demonstration
    factory.swap_elements(0, 1)
    print("\nAfter swapping elements:")
    print(factory.render())

if __name__ == "__main__":
    main()