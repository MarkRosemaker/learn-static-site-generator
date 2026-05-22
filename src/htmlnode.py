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
        props: dict[str, str] = {},
        children: list[HTMLNode] = [],
    ):
        self.tag = tag
        self.value = value
        self.props = props
        self.children = children

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        elems: list[str] = []
        for k, v in self.props.items():
            elems.append(f' {k}="{v}"')
        return "".join(elems)

    def __repr__(self) -> str:
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


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
