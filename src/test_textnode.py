import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


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


    def test_split_nodes_delimiter_basic_bold(self):
        node = TextNode("Hello **world**!", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("!", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_ignores_non_text(self):
        node = TextNode("Already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_split_nodes_delimiter_raises_on_unmatched(self):
        node = TextNode("This is **broken", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertIn("Invalid Markdown syntax", str(context.exception))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_basic(self):
        matches = extract_markdown_images(
            "This is ![alt text](http://example.com/image.png)"
        )
        self.assertListEqual(
            [("alt text", "http://example.com/image.png")], matches
        )

    def test_extract_markdown_images_multiple(self):
        text = "First ![one](url1.png) and second ![two](url2.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("one", "url1.png"), ("two", "url2.jpg")], matches
        )

    def test_extract_markdown_images_no_alt_text(self):
        matches = extract_markdown_images("Image: ![](noalt.png)")
        self.assertListEqual([("", "noalt.png")], matches)

    def test_extract_markdown_links_basic(self):
        matches = extract_markdown_links(
            "Click [here](http://example.com) for more."
        )
        self.assertListEqual(
            [("here", "http://example.com")], matches
        )

    def test_extract_markdown_links_skips_images(self):
        matches = extract_markdown_links(
            "Here is an image: ![alt](img.png) and a [link](url.com)"
        )
        self.assertListEqual(
            [("link", "url.com")], matches
        )

    def test_extract_markdown_links_no_text(self):
        matches = extract_markdown_links("A bare link: [](empty.com)")
        self.assertListEqual([("", "empty.com")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "Check this [link](https://example.com) and another [second](https://second.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check this ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second", TextType.LINK, "https://second.com"),
            ],
            new_nodes,
        )

    def test_complex_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(result, expected)

    def test_only_bold_and_italic(self):
        text = "**Bold** text and *italic* text."
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" text and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(result, expected)

    def test_images_and_links(self):
        text = "Image: ![alt text](http://example.com/image.png) and link: [Example](http://example.com)"
        expected = [
            TextNode("Image: ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "http://example.com/image.png"),
            TextNode(" and link: ", TextType.TEXT),
            TextNode("Example", TextType.LINK, "http://example.com"),
        ]
        result = text_to_textnodes(text)
        self.assertListEqual(result, expected)


if __name__ == "__main__":
    unittest.main()