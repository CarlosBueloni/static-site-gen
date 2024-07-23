import unittest
from helper import (
        text_node_to_html_node,
        split_nodes_delimiter,
        extract_markdown_links,
        extract_markdown_images,
        split_nodes_images,
        split_nodes_links,
)
from textnode import TextNode, TextType
from htmlnode import LeafNode

class TestHelper(unittest.TestCase):
    def test_tnode_to_hnode(self):
        tnode_text = TextNode("this is a text", TextType.text.value)
        tnode_bold = TextNode("this is bold", TextType.bold.value)
        tnode_italic = TextNode("this is italic", TextType.italic.value)
        tnode_code = TextNode("print('hello world')", TextType.code.value)
        tnode_link = TextNode("google", TextType.link.value, "https://www.google.com")
        tnode_img = TextNode("dog", TextType.image.value, "/pics/dog.png")
        tnode_type_not_found = TextNode("this dosen't have a type", None)

        self.assertEqual(text_node_to_html_node(tnode_text), 
                         LeafNode(None, "this is a text", None))
        self.assertEqual(text_node_to_html_node(tnode_bold), 
                         LeafNode("b", "this is bold", None))
        self.assertEqual(text_node_to_html_node(tnode_italic), 
                         LeafNode("i", "this is italic", None))
        self.assertEqual(text_node_to_html_node(tnode_code), 
                         LeafNode("code","print('hello world')", None))
        self.assertEqual(text_node_to_html_node(tnode_link), 
                         LeafNode("a", "google", {"href": "https://www.google.com"}))
        self.assertEqual(text_node_to_html_node(tnode_img), 
                         LeafNode("img", "", {"src":"/pics/dog.png", "alt": "dog"}))
        with self.assertRaises(ValueError):
            text_node_to_html_node(tnode_type_not_found)

    def test_split_nodes_delimiter(self):
        node_code = TextNode("This is a text with a `code block` word", 
                             TextType.text.value)
        node_bold = TextNode("This is a text with a **bold block** word", 
                             TextType.text.value)
        nodes = split_nodes_delimiter([node_code], "`", TextType.code.value)
        nodes2 = split_nodes_delimiter([node_bold], "**", TextType.bold.value)
        self.assertEqual(nodes, [
            TextNode("This is a text with a ", TextType.text.value),
            TextNode("code block", TextType.code.value),
            TextNode(" word", TextType.text.value),
        ]) 
        self.assertEqual(nodes2, [
            TextNode("This is a text with a ", TextType.text.value),
            TextNode("bold block", TextType.bold.value),
            TextNode(" word", TextType.text.value),
        ]) 

    def test_split_nodes_delimiter_error(self):
        t_node = TextNode("This is a text ` without closing delimiter", TextType.code.value)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([t_node], "`", TextType.code.value)

    def test_split_nodes_delimiter_old_node_not_text(self):
        node1 = TextNode("`code`", TextType.code.value)
        node2 = TextNode("*italic*", TextType.italic.value)
        node3 = TextNode("**bold**", TextType.bold.value)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "*", TextType.italic.value)
        self.assertEqual(new_nodes, [node1, node2, node3])

    def test_extract_markdow_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])    

    def test_extract_markdow_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text),
                         [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_nodes_links_empty_list(self):
        text = TextNode("", TextType.text.value)
        self.assertEqual(split_nodes_links([text]), [])

    def test_split_nodes_links_one_node_and_link(self):
        node = TextNode("to access google go to [google](https://www.google.com)", TextType.link.value)
        self.assertEqual(split_nodes_links([node]),
                         [
                            TextNode("to access google go to ", TextType.text.value), 
                            TextNode("google", TextType.link.value, "https://www.google.com"),
                         ])
    def test_split_nodes_links_one_node_multiple_links(self):
        node = TextNode("cat [cat](cat.com) dog [dog](dog.com)", TextType.link.value)
        self.assertEqual(split_nodes_links([node]),
                         [
                            TextNode("cat ", TextType.text.value),
                            TextNode("cat", TextType.link.value, "cat.com"),
                            TextNode(" dog ", TextType.text.value),
                            TextNode("dog", TextType.link.value, "dog.com"),
                         ])

    def test_split_nodes_links_multiple_nodes(self):
        node2 = TextNode("dog [dog](dog.com)", TextType.link.value)
        node = TextNode("cat [cat](cat.com)", TextType.link.value)
        self.assertEqual(split_nodes_links([node, node2]),
                         [
                            TextNode("cat ", TextType.text.value),
                            TextNode("cat", TextType.link.value, "cat.com"),
                            TextNode("dog ", TextType.text.value),
                            TextNode("dog", TextType.link.value, "dog.com"),
                         ])

    def test_split_nodes_links_nodes_without_link(self):
        node = TextNode("this node has no links", TextType.text.value)
        node2 = TextNode("this is a link [google](https://www.google.com)", TextType.link.value)
        self.assertEqual(split_nodes_links([node, node2]),
                         [
                            TextNode("this node has no links", TextType.text.value),
                            TextNode("this is a link ", TextType.text.value),
                            TextNode("google", TextType.link.value, "https://www.google.com"),
                         ])

    def test_split_nodes_images_empty_list(self):
        text = TextNode("", TextType.text.value)
        self.assertEqual(split_nodes_images([text]), [])

    def test_split_nodes_images_one_node_and_image(self):
        i_node = TextNode("to access google go to ![google](https://www.google.com)", TextType.image.value)
        self.assertEqual(split_nodes_images([i_node]),
                         [
                            TextNode("to access google go to ", TextType.text.value), 
                            TextNode("google", TextType.image.value, "https://www.google.com"),
                         ])

    def test_split_nodes_images_one_node_multiple_images(self):
        node = TextNode("cat ![cat](cat.com) dog ![dog](dog.com)", TextType.image.value)
        self.assertEqual(split_nodes_images([node]),
                         [
                            TextNode("cat ", TextType.text.value),
                            TextNode("cat", TextType.image.value, "cat.com"),
                            TextNode(" dog ", TextType.text.value),
                            TextNode("dog", TextType.image.value, "dog.com"),
                         ])

    def test_split_nodes_images_multiple_nodes(self):
        node2 = TextNode("dog ![dog](dog.com)", TextType.image.value)
        node = TextNode("cat ![cat](cat.com)", TextType.image.value)
        self.assertEqual(split_nodes_images([node, node2]),
                         [
                            TextNode("cat ", TextType.text.value),
                            TextNode("cat", TextType.image.value, "cat.com"),
                            TextNode("dog ", TextType.text.value),
                            TextNode("dog", TextType.image.value, "dog.com"),
                         ])

    def test_split_nodes_images_nodes_without_image(self):
        node = TextNode("this node has no images", TextType.text.value)
        node2 = TextNode("this is a image ![google](https://www.google.com)", TextType.image.value)
        self.assertEqual(split_nodes_images([node, node2]),
                         [
                            TextNode("this node has no images", TextType.text.value),
                            TextNode("this is a image ", TextType.text.value),
                            TextNode("google", TextType.image.value, "https://www.google.com"),
                         ])
