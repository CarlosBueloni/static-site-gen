import unittest
from helper import extract_title

class TestHelper(unittest.TestCase):
    def test_extract_title_multiple_lines(self):
        md = """
# This is the title

This is text
this is another text"""
        self.assertEqual(extract_title(md), "This is the title")

    def test_extract_title_no_title(self):
        md = "## this is not a title"
        with self.assertRaises(ValueError):
            extract_title(md)

