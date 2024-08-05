import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_links,
    text_to_textnode,
    extract_markdown_links,
    extract_markdown_images,
)

from textnode import (
    TextNode,
    TextType,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.text.value)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold.value)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text.value),
                TextNode("bolded", TextType.bold.value),
                TextNode(" word", TextType.text.value),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.text.value
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold.value)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text.value),
                TextNode("bolded", TextType.bold.value),
                TextNode(" word and ", TextType.text.value),
                TextNode("another", TextType.bold.value),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.text.value
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold.value)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text.value),
                TextNode("bolded word", TextType.bold.value),
                TextNode(" and ", TextType.text.value),
                TextNode("another", TextType.bold.value),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.text.value)
        new_nodes = split_nodes_delimiter([node], "*", TextType.italic.value)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text.value),
                TextNode("italic", TextType.italic.value),
                TextNode(" word", TextType.text.value),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.text.value)
        new_nodes = split_nodes_delimiter([node], "**", TextType.bold.value)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.italic.value)
        self.assertEqual(
            [
                TextNode("bold", TextType.bold.value),
                TextNode(" and ", TextType.text.value),
                TextNode("italic", TextType.italic.value),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.text.value)
        new_nodes = split_nodes_delimiter([node], "`", TextType.code.value)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text.value),
                TextNode("code block", TextType.code.value),
                TextNode(" word", TextType.text.value),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.text.value,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text.value),
                TextNode("image", TextType.image.value, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            TextType.text.value,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.image.value, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.text.value,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.text.value),
                TextNode("image", TextType.image.value, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.text.value),
                TextNode(
                    "second image", TextType.image.value, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.text.value,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.text.value),
                TextNode("link", TextType.link.value, "https://boot.dev"),
                TextNode(" and ", TextType.text.value),
                TextNode("another link", TextType.link.value, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.text.value),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnode(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.text.value),
                TextNode("text", TextType.bold.value),
                TextNode(" with an ", TextType.text.value),
                TextNode("italic", TextType.italic.value),
                TextNode(" word and a ", TextType.text.value),
                TextNode("code block", TextType.code.value),
                TextNode(" and an ", TextType.text.value),
                TextNode("image", TextType.image.value, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.text.value),
                TextNode("link", TextType.link.value, "https://boot.dev"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
