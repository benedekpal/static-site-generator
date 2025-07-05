import unittest

from block_markdown_parser import markdown_to_blocks, block_to_block_type, BlockType

class TestBlockParser(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_multiple_empty_lines(self):
        md = """

This is the first paragraph


This is the second paragraph after multiple breaks



- Item 1
- Item 2

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is the first paragraph",
                "This is the second paragraph after multiple breaks",
                "- Item 1\n- Item 2",
            ],
        )

    def test_single_block(self):
        md = "This is a single paragraph with **bold**, _italic_, and `code`."
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This is a single paragraph with **bold**, _italic_, and `code`."],
        )

    def test_heading_block(self):
        text = "# This is a heading"
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_code_block(self):
        text = "```\ndef hello():\n    return 'world'\n```"
        self.assertEqual(block_to_block_type(text), BlockType.CODE)

    def test_quote_block(self):
        text = "> This is a quote\n> Spanning multiple lines"
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)

    def test_unordered_list_block(self):
        text = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(text), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        text = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(text), BlockType.ORDERED_LIST)

    def test_paragraph_block(self):
        text = "This is a paragraph that doesn't match any other block type."
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()