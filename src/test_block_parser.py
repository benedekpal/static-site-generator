import unittest

from block_markdown_parser import markdown_to_blocks

class TestTextNode(unittest.TestCase):

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

if __name__ == "__main__":
    unittest.main()