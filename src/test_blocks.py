import unittest

from block import block_to_block_type, BlockType


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        txt = "### This is a heading"
        tp = block_to_block_type(txt)
        self.assertEqual(tp, BlockType.HEADING)

    def test_code_block(self):
        txt = """```
{
  "firstName": "John",
  "lastName": "Smith",
  "age": 25
}
```"""
        tp = block_to_block_type(txt)
        self.assertEqual(tp, BlockType.CODE)

    def test_quote_block(self):
        txt = """> Dorothy followed her through many of the
> beautiful rooms in her castle."""
        tp = block_to_block_type(txt)
        self.assertEqual(tp, BlockType.QUOTE)

    def test_unordered_list(self):
        txt = """- First item
- Second item
- Third item
- Fourth item"""
        tp = block_to_block_type(txt)
        self.assertEqual(tp, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        txt = """1. First item
2. Second item
3. Third item
4. Fourth item"""
        tp = block_to_block_type(txt)
        self.assertEqual(tp, BlockType.ORDERED_LIST)

    def test_paragraph(self):
        txt = "I really like using Markdown."
        tp = block_to_block_type(txt)
        self.assertEqual(tp, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
