import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_code,
    text_type_link,
    text_type_image,
    text_type_italic
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("this is a text node", text_type_bold)
        node2 = TextNode("this is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("this is a text node", text_type_bold)
        node2 = TextNode("this is a node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("this is a text node", text_type_bold)
        node2 = TextNode("this is a node", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("this is a node", text_type_text, "www.google.com")
        node2 = TextNode("this is a node", text_type_text, "www.google.com")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("this is a text node", text_type_bold)
        self.assertEqual(str(node), 'TextNode(this is a text node, bold, None)')


