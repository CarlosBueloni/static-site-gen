from re import T
import unittest
from inline_markdown import (
        text_node_to_html_node,
        split_nodes_delimiter,
        extract_markdown_links,
        extract_markdown_images,
        split_nodes_images,
        split_nodes_links,
        text_to_textnode,
)
from textnode import TextNode, TextType
from htmlnode import LeafNode

class TestHelper(unittest.TestCase):

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

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.text.value,
        )
        self.assertEqual(split_nodes_links([node]),
                         [
                             TextNode("This is text with a link ", TextType.text.value),
                             TextNode("to boot dev", TextType.link.value, "https://www.boot.dev"),
                             TextNode(" and ", TextType.text.value),
                             TextNode("to youtube", TextType.link.value, "https://www.youtube.com/@bootdotdev"),
                         ])

    def test_split_nodes_links2(self):
        node = TextNode( "before [link](https://link.com) after", TextType.text.value)
        self.assertEqual(split_nodes_links([node]),
                         [
                            TextNode("before ", TextType.text.value),
                            TextNode("link", TextType.link.value, "https://link.com"),
                            TextNode(" after", TextType.text.value),
                         ])

    def test_split_nodes_not_closed(self):
        node = TextNode( "before [link]asdasd(https://link.com after)", TextType.text.value)
        with self.assertRaises(ValueError):
            split_nodes_links([node])

    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with a image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.text.value,
        )
        self.assertEqual(split_nodes_images([node]),
                         [
                             TextNode("This is text with a image ", TextType.text.value),
                             TextNode("to boot dev", TextType.image.value, "https://www.boot.dev"),
                             TextNode(" and ", TextType.text.value),
                             TextNode("to youtube", TextType.image.value, "https://www.youtube.com/@bootdotdev"),
                         ])

    def test_split_nodes_images2(self):
        node = TextNode( "before ![image](https://image.com) after", TextType.text.value)
        self.assertEqual(split_nodes_images([node]),
                         [
                            TextNode("before ", TextType.text.value),
                            TextNode("image", TextType.image.value, "https://image.com"),
                            TextNode(" after", TextType.text.value),
                         ])

    def test_split_nodes_images_not_closed(self):
        node = TextNode( "before ![link]asdasd(https://link.com after)", TextType.text.value)
        with self.assertRaises(ValueError):
            split_nodes_images([node])

    def test_text_to_textnode(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnode(text),
                         [
                             TextNode("This is ", TextType.text.value),
                             TextNode("text", TextType.bold.value), 
                             TextNode(" with an ", TextType.text.value),
                             TextNode("italic", TextType.italic.value),
                             TextNode(" word and a ", TextType.text.value),
                             TextNode("code block", TextType.code.value),
                             TextNode(" and an ", TextType.text.value),
                             TextNode("obi wan image", TextType.image.value, "https://i.imgur.com/fJRm4Vk.jpeg"),
                             TextNode(" and a ", TextType.text.value),
                             TextNode("link", TextType.link.value, "https://boot.dev"),
                         ])

    def test_text_to_textnode_only_text(self):
        text = "this is text"
        self.assertEqual(text_to_textnode(text),[TextNode("this is text", TextType.text.value)])

    def test_text_to_textnode_only_bold(self):
        text = "**bold**"
        self.assertEqual(text_to_textnode(text),[TextNode("bold", TextType.bold.value)])

    def test_text_to_textnode_only_italic(self):
        text = "*italic*"
        self.assertEqual(text_to_textnode(text),[TextNode("italic", TextType.italic.value)])

    def test_text_to_textnode_only_code(self):
        text = "`code`"
        self.assertEqual(text_to_textnode(text),[TextNode("code", TextType.code.value)])

    def test_text_to_textnode_only_image(self):
        text = "![cute dog](/imgs/dog.png)"
        self.assertEqual(text_to_textnode(text),[TextNode("cute dog", TextType.image.value, "/imgs/dog.png")])

    def test_text_to_textnode_only_link(self):
        text = "[cute dog](www.images.com/imgs/dog.png)"
        self.assertEqual(text_to_textnode(text),[TextNode("cute dog", TextType.link.value, "www.images.com/imgs/dog.png")])






































