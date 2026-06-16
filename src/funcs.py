from textnode import TextNode, TextType
from block import block_to_block_type, BlockType, RE_HEADING
from htmlnode import HTMLNode, text_node_to_html_node
import re
from typing import Callable


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        match old_node.text_type:
            case TextType.PLAIN:
                split = old_node.text.split(delimiter)
                if len(split) % 2 != 1:
                    raise ValueError(
                        f"matching closing delimiter not found, got {len(split)} split pieces"
                    )
                for i, s in enumerate(split):
                    if not s:
                        continue

                    if i % 2 == 0:
                        new_nodes.append(TextNode(s))
                    else:
                        new_nodes.append(TextNode(s, text_type))
            case _:
                new_nodes.append(old_node)

    return new_nodes


def split_nodes_bold(nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_delimiter(nodes, "**", TextType.BOLD)


def split_nodes_italic(nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_delimiter(nodes, "_", TextType.ITALIC)


def split_nodes_code(nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_delimiter(nodes, "`", TextType.CODE)


def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]+)\)", text)


def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for n in old_nodes:
        match n.text_type:
            case TextType.PLAIN:
                txt = n.text
                for img_alt, img_link in extract_markdown_images(txt):
                    pre, txt = txt.split(f"![{img_alt}]({img_link})", 1)
                    if pre:
                        new_nodes.append(TextNode(pre))
                    new_nodes.append(TextNode(img_alt, TextType.IMAGE, img_link))
                if txt:
                    new_nodes.append(TextNode(txt))
            case _:
                new_nodes.append(n)

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for n in old_nodes:
        match n.text_type:
            case TextType.PLAIN:
                txt = n.text
                for link_alt, link_url in extract_markdown_links(txt):
                    pre, txt = txt.split(f"[{link_alt}]({link_url})", 1)
                    if pre:
                        new_nodes.append(TextNode(pre))
                    new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
                if txt:
                    new_nodes.append(TextNode(txt))
            case _:
                new_nodes.append(n)

    return new_nodes


split_funcs: list[Callable[[list[TextNode]], list[TextNode]]] = [
    split_nodes_bold,
    split_nodes_italic,
    split_nodes_code,
    split_nodes_image,  # process before links
    split_nodes_link,
]


def text_to_textnodes(text: str) -> list[TextNode]:
    res: list[TextNode] = [TextNode(text)]
    for f in split_funcs:
        res = f(res)

    return res


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []
    for b in markdown.split("\n\n"):
        if block := b.strip("\n"):
            blocks.append(block)
    return blocks


def markdown_to_html_node(markdown: str) -> HTMLNode:
    p = HTMLNode("div")
    for block in markdown_to_blocks(markdown):
        tp = block_to_block_type(block)
        match tp:
            case BlockType.PARAGRAPH:
                p.children.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                p.children.append(heading_to_html_node(block))
            case BlockType.CODE:
                p.children.append(code_to_html_node(block))
            case BlockType.ORDERED_LIST:
                p.children.append(olist_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                p.children.append(ulist_to_html_node(block))
            case BlockType.QUOTE:
                p.children.append(quote_to_html_node(block))
            case _:
                raise ValueError("invalid block type")

    return p


def text_to_children(text: str) -> list[HTMLNode]:
    return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(text)]


def paragraph_to_html_node(block: str) -> HTMLNode:
    return HTMLNode("p", children=text_to_children(" ".join(block.split("\n"))))


def heading_to_html_node(block: str) -> HTMLNode:
    m = RE_HEADING.match(block)
    if not m:
        raise ValueError(f"invalid heading: {block}")

    level = len(m.group(1))
    text = block[level + 1 :]
    return HTMLNode(f"h{level}", children=text_to_children(text))


def code_to_html_node(block: str) -> HTMLNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    return HTMLNode(
        "pre",
        children=[
            HTMLNode(
                "code",
                children=[
                    text_node_to_html_node(TextNode(block[4:-3], TextType.PLAIN))
                ],
            )
        ],
    )


def olist_to_html_node(block: str) -> HTMLNode:
    return HTMLNode(
        "ol",
        children=[
            HTMLNode("li", children=text_to_children(item.split(". ", 1)[1]))
            for item in block.split("\n")
        ],
    )


def ulist_to_html_node(block: str) -> HTMLNode:
    return HTMLNode(
        "ul",
        children=[
            HTMLNode("li", children=text_to_children(item[2:]))
            for item in block.split("\n")
        ],
    )


def quote_to_html_node(block: str) -> HTMLNode:
    new_lines: list[str] = []
    for line in block.split("\n"):
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    return HTMLNode("blockquote", children=text_to_children(" ".join(new_lines)))


def extract_title(markdown: str) -> str:
    if not markdown.startswith("# "):
        raise Exception("not a valid title header")

    return markdown.removeprefix("# ")
