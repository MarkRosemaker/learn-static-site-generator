from textnode import TextNode, TextType
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
