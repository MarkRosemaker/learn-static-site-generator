from enum import Enum


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    # BLOCK = "block"


class TextNode:
    text: str  # The text content of the node
    text_type: TextType  # The type of text this node contains
    # The URL of the link or image, if the text is a link. Default to None if nothing is passed in.
    url: None | str

    def __init__(self, text: str, text_type: TextType, url: None | str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
