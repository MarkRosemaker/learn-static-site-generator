import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is node has a different text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_type(self):
        node = TextNode("Hi!", TextType.BOLD)
        node2 = TextNode("Hi!", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_no_type_is_plain(self):
        node = TextNode("Just plain text", TextType.PLAIN)
        node2 = TextNode("Just plain text")
        self.assertEqual(node, node2)

    def test_no_type_is_plain(self):
        node = TextNode("Just plain text", TextType.PLAIN)
        node2 = TextNode("Just plain text")
        self.assertEqual(node, node2)

    def test_url(self):
        link = TextNode("Check out this link", TextType.LINK, "example.com")
        link2 = TextNode("Check out this link", TextType.LINK, "example.com")
        linkMissing = TextNode("Check out this link", TextType.LINK)
        self.assertEqual(link, link2)
        self.assertNotEqual(link, linkMissing)


if __name__ == "__main__":
    unittest.main()
