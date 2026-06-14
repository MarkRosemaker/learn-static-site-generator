from __future__ import annotations

from textnode import TextNode, TextType


class HTMLNode:
    # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
    tag: str
    # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
    value: str
    # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
    props: dict[str, str]
    # A list of HTMLNode objects representing the children of this node
    children: list[HTMLNode]

    def __init__(
        self,
        tag: str,
        value: str = "",
        props: dict[str, str] | None = None,
        children: list[HTMLNode] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.props = props if props else {}
        self.children = children if children else []

    def to_html(self) -> str:
        elems = ["<", self.tag, self.props_to_html(), ">", self.value]
        for c in self.children:
            elems.append(c.to_html())
        elems.extend(["</", self.tag, ">"])

        return "".join(elems)

    def props_to_html(self) -> str:
        elems: list[str] = []
        for k, v in self.props.items():
            elems.append(f' {k}="{v}"')
        return "".join(elems)

    def __repr__(self) -> str:
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] = {},
    ):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("parent node is missing a tag")

        if not self.children:
            raise ValueError("parent node is missing children")

        cHTML: list[str] = []
        for c in self.children:
            cHTML.append(c.to_html())

        return f"<{self.tag}{self.props_to_html()}>{"".join(cHTML)}</{self.tag}>"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: dict[str, str] = {},
    ):
        super().__init__(tag, value, props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("leaf node is missing a value")

        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


def text_node_to_html_node(n: TextNode) -> LeafNode:
    match n.text_type:
        case TextType.PLAIN:
            return LeafNode("", n.text)
        case TextType.BOLD:
            return LeafNode("b", n.text)
        case TextType.ITALIC:
            return LeafNode("i", n.text)
        case TextType.CODE:
            return LeafNode("code", n.text)
        case TextType.LINK:
            return LeafNode("a", n.text, {"href": n.url or ""})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": n.url or "", "alt": n.text})
        case _:
            raise ValueError(f"unknown text type {n.text_type}")
