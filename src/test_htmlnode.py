import unittest

from htmlnode import HTMLNode, ParentNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.props_to_html(), "")
        self.assertEqual(f"{node}", "<p>This is a paragraph</p>")

    def test_link(self):
        node = HTMLNode(
            "a", "Visit Google", {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )
        self.assertEqual(
            f"{node}",
            '<a href="https://www.google.com" target="_blank">Visit Google</a>',
        )

    def test_heading(self):
        node = HTMLNode("h1", "My Heading", {"id": "my-heading"})
        self.assertEqual(node.props_to_html(), ' id="my-heading"')
        self.assertEqual(
            f"{node}",
            '<h1 id="my-heading">My Heading</h1>',
        )


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

        node = ParentNode(
            "p",
            list[HTMLNode](
                [
                    LeafNode("b", "Bold text"),
                    LeafNode("", "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode("", "Normal text"),
                ]
            ),
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_link(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


if __name__ == "__main__":
    unittest.main()
