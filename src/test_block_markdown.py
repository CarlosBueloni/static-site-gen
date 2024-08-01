import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_type_paragraph(self):
        text = "this is a text"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_block_to_block_type_headings_1(self):
        text = "# this is a text"
        self.assertEqual(block_to_block_type(text), "heading")

    def test_block_to_block_type_headings_6(self):
        text = "###### this is a text"
        self.assertEqual(block_to_block_type(text), "heading")

    def test_block_to_block_type_headings_wrong_syntax(self):
        text = "################ this is a text"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_block_to_block_type_code(self):
        text = "```print(this is code)```"
        self.assertEqual(block_to_block_type(text), "code")


    def test_block_to_block_type_code_wrong_syntax(self):
        text = "```print(this is code)``"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_block_to_block_type_quote(self):
        text = ">this is a\n>quote"
        self.assertEqual(block_to_block_type(text), "quote")

    def test_block_to_block_type_quote_wrong_syntax(self):
        text = ">this is a\nquote"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_block_to_block_type_ul_dash(self):
        text = "- this is a\n- unordered list"
        self.assertEqual(block_to_block_type(text), "unordered_list")

    def test_block_to_block_type_ul_dash_wrong_syntax(self):
        text = "-this is a\n*unordered list"
        self.assertEqual(block_to_block_type(text), "paragraph")


    def test_block_to_block_type_ul_star(self):
        text = "* this is a\n* unordered list"
        self.assertEqual(block_to_block_type(text), "unordered_list")

    def test_block_to_block_type_ul_star_wrong_syntax(self):
        text = "*this is a\n-unordered list"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_block_to_block_type_ol(self):
        text = "1. this is a\n2. unordered list"
        self.assertEqual(block_to_block_type(text), "ordered_list")

    def test_block_to_block_type_ol_wrong_syntax(self):
        text = "1. this is a\n3. unordered list"
        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_paragraph(self):
        text = """
This is **bolded** paragraph
text in a p
tag here

"""
        node = markdown_to_html_node(text)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>")
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    
    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    if __name__ == "__main__":
        unittest.main()
