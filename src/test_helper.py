import unittest
from helper import text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import LeafNode

class TestHelper(unittest.TestCase):
    def test_tnode_to_hnode(self):
        tnode_text = TextNode("this is a text", TextType.text_type_text.value)
        tnode_bold = TextNode("this is bold", TextType.text_type_bold.value)
        tnode_italic = TextNode("this is italic", TextType.text_type_italic.value)
        tnode_code = TextNode("print('hello world')", TextType.text_type_code.value)
        tnode_link = TextNode("google", TextType.text_type_link.value, "https://www.google.com")
        tnode_img = TextNode("dog", TextType.text_type_image.value, "/pics/dog.png")
        tnode_type_not_found = TextNode("this dosen't have a type", None)
        
        self.assertEqual(text_node_to_html_node(tnode_text), LeafNode(None, "this is a text", None))
        self.assertEqual(text_node_to_html_node(tnode_bold), LeafNode("b", "this is bold", None))
        self.assertEqual(text_node_to_html_node(tnode_italic), LeafNode("i", "this is italic", None))
        self.assertEqual(text_node_to_html_node(tnode_code), LeafNode("code","print('hello world')", None))
        self.assertEqual(text_node_to_html_node(tnode_link), LeafNode("a", "google", {"href": "https://www.google.com"}))
        self.assertEqual(text_node_to_html_node(tnode_img), LeafNode("img", "", {"src":"/pics/dog.png", "alt": "dog"}))
        with self.assertRaises(ValueError):
            text_node_to_html_node(tnode_type_not_found)
