import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("this is a text node", TextType.bold.value)
        node2 = TextNode("this is a text node",  TextType.bold.value)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("this is a text node",  TextType.bold.value)
        node2 = TextNode("this is a node", TextType.bold.value)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("this is a text node", TextType.bold.value)
        node2 = TextNode("this is a node", TextType.text.value)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("this is a node", TextType.text.value, "www.google.com")
        node2 = TextNode("this is a node", TextType.text.value, "www.google.com")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("this is a text node", TextType.bold.value)
        self.assertEqual(str(node), 'TextNode(this is a text node, bold, None)')


