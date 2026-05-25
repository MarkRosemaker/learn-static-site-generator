from textnode import TextNode, TextType


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
