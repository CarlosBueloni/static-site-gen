import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_values_default(self):
        h_node= HTMLNode()
        self.assertEqual(h_node.tag, None)
        self.assertEqual(h_node.value, None)
        self.assertEqual(h_node.children, None)
        self.assertEqual(h_node.props, None)

    def test_eq(self):
        node1 = HTMLNode("p", "text")
        node2 = HTMLNode("p", "text")
        self.assertEqual(node1, node2)


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

    def test_to_html_parent_no_tag(self):
        p_node = ParentNode(None, [LeafNode("b", "bold text"), LeafNode(None, "normal text")],)
        with self.assertRaises(ValueError, msg="All parent nodes must have a tag"):
            p_node.to_html()

    def test_to_html_parent_no_children(self):
        p_node = ParentNode("a", None)
        with self.assertRaises(ValueError, msg="All parent nodes must have children"):
            p_node.to_html()

    def test_to_html_parent(self):
        p_node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
                )
        self.assertEqual(p_node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_parent_2(self):
        p_node = ParentNode(
                "p",
                [
                    LeafNode(None, "text"),
                    ParentNode(
                    "div",
                    [LeafNode(None, "text inside div")]
                    )
                ]
                )
        self.assertEqual(p_node.to_html(), "<p>text<div>text inside div</div></p>")

    def test_to_html_parent_with_props(self):
        p_node = ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                    LeafNode("i", "italic text"),
                    LeafNode(None, "Normal text"),
                ],
                {"href": "https://www.google.com"}
                )
        self.assertEqual(p_node.to_html(), '<p href="https://www.google.com"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_props_to_html(self):
        h_node = HTMLNode("p", "text", None, {
            "href": "https://www.google.com", 
            "target": "_blank",
        })
        self.assertEqual(h_node.props_to_html(),  ' href="https://www.google.com" target="_blank"')

    def test_rpr(self):
        h_node = HTMLNode("p", "this is a paragraph")
        self.assertEqual(str(h_node), "HTMLNode(p, this is a paragraph, None, None)")

