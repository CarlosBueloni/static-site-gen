import unittest
from block_markdown import markdown_to_blocks, block_to_block_type


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
        text = "-this is a\n-unordered list"
        self.assertEqual(block_to_block_type(text), "unordered_list")

    def test_block_to_block_type_ul_dash_wrong_syntax(self):
        text = "-this is a\n*unordered list"
        self.assertEqual(block_to_block_type(text), "paragraph")


    def test_block_to_block_type_ul_star(self):
        text = "*this is a\n*unordered list"
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

if __name__ == "__main__":
    unittest.main()
