import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from block_markdown_parser import markdown_to_blocks

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is an another text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node1 = TextNode("Link text", TextType.LINK, url="http://example.com")
        node2 = TextNode("Link text", TextType.LINK, url="http://example.com")
        self.assertEqual(node1, node2)

    def test_not_eq_different_url(self):
        node1 = TextNode("Link text", TextType.LINK, url="http://example.com")
        node2 = TextNode("Link text", TextType.LINK, url="http://different.com")
        self.assertNotEqual(node1, node2)

    def test_not_eq_url_none_vs_value(self):
        node1 = TextNode("Link text", TextType.LINK, url=None)
        node2 = TextNode("Link text", TextType.LINK, url="http://example.com")
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_text_type(self):
        node1 = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_text(self):
        node1 = TextNode("Text A", TextType.TEXT)
        node2 = TextNode("Text B", TextType.TEXT)
        self.assertNotEqual(node1, node2)

    def test_not_eq_everything_different(self):
        node1 = TextNode("A", TextType.BOLD, url="http://a.com")
        node2 = TextNode("B", TextType.ITALIC, url="http://b.com")
        self.assertNotEqual(node1, node2)

    def test_eq_all_none_optional(self):
        node1 = TextNode("Plain text", TextType.TEXT, url=None)
        node2 = TextNode("Plain text", TextType.TEXT, url=None)
        self.assertEqual(node1, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
    
    def test_link(self):
        node = TextNode("Click here", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("An image", TextType.IMAGE, url="https://img.com/cat.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {
            "src": "https://img.com/cat.png",
            "alt": "An image"
        })
    
    def test_invalid_text_type(self):
        class FakeTextType:
            pass
        node = TextNode("Oops", FakeTextType())
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertIn("Invalid TextType", str(context.exception))


if __name__ == "__main__":
    unittest.main()