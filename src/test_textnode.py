import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()