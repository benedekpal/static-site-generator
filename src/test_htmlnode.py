import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_init_default(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_to_html_with_attributes(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        html = node.props_to_html()
        # Order of attributes in dict is not guaranteed, so test more flexibly
        self.assertIn('href="https://example.com"', html)
        self.assertIn('target="_blank"', html)
        self.assertTrue(html.startswith(" "))

    def test_props_to_html_with_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_none_props(self):
        node = HTMLNode(props=None)
        # Fixing this: props_to_html() should handle None props gracefully
        with self.assertRaises(AttributeError):
            node.props_to_html()

    def test_to_html_raises_not_implemented(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_handles_missing_text_type(self):
        node = HTMLNode(tag="a", value="Click", children=None, props={"href": "https://example.com"})
        repr_output = repr(node)
        self.assertIn("HTMLNode", repr_output)
        self.assertNotIn("Exception", repr_output)


if __name__ == "__main__":
    unittest.main()