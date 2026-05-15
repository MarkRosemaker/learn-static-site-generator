from textnode import TextNode, TextType


def main():
    node = TextNode("It worked!", TextType.BOLD)
    print(node)


if __name__ == "__main__":
    main()
