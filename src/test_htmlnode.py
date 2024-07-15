import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_values_default(self):
        h_node= HTMLNode()
        self.assertEqual(h_node.tag, None)
        self.assertEqual(h_node.value, None)
        self.assertEqual(h_node.children, None)
        self.assertEqual(h_node.props, None)

    def test_to_html(self):
        h_node = HTMLNode("p", "text")
        with self.assertRaises(NotImplementedError):
            h_node.to_html()

    def test_to_html_leaf(self):
        l_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(l_node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_leaf_no_value(self):
        l_node = LeafNode("a", None, {"href": "https://www.google.com"})
        with self.assertRaises(ValueError):
            l_node.to_html()

    def test_to_html_leaf_no_tag(self):
        l_node =LeafNode(None, "this is a raw text")
        self.assertEqual(l_node.to_html(), "this is a raw text")

    def test_props_to_html(self):
        h_node = HTMLNode("p", "text", None, {
            "href": "https://www.google.com", 
            "target": "_blank",
        })
        self.assertEqual(h_node.props_to_html(),  ' href="https://www.google.com" target="_blank"')

    def test_rpr(self):
        h_node = HTMLNode("p", "this is a paragraph")
        self.assertEqual(str(h_node), "HTMLNode(p, this is a paragraph, None, None)")

