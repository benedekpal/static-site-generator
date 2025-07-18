import unittest

from block_markdown_parser import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node, extract_title

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

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_block(self):
        md = """
    ### This is a heading with **bold**
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading with <b>bold</b></h3></div>",
        )

    def test_quote_block(self):
        md = """
    > This is a quote with _emphasis_
    > And a second line
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <i>emphasis</i> And a second line</blockquote></div>",
        )

    def test_unordered_list_block(self):
        md = """
    - Item one with `code`
    - Item **two**
    - _Item three_
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item one with <code>code</code></li><li>Item <b>two</b></li><li><i>Item three</i></li></ul></div>",
        )

    def test_ordered_list_block(self):
        md = """
    1. First item
    2. Second with **bold**
    3. Third with _italic_
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second with <b>bold</b></li><li>Third with <i>italic</i></li></ol></div>",
        )

    def test_get_heading_from_markdown(self):
        md = """
    # This is the title

    ## This is a heading with **bold**

    """
        title = extract_title(md)
        self.assertEqual(title, "This is the title")

    def test_get_no_heading_from_markdown(self):
        md = """
    ## This is a heading with **bold**
    
    """
        with self.assertRaises(Exception):
            title = extract_title(md)
    

if __name__ == "__main__":
    unittest.main()