import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
