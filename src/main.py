from block_markdown import block_to_block_type,  markdown_to_html_node
from inline_markdown import (
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_links,
    split_nodes_images,
    text_to_textnode,
)
from textnode import TextNode, TextType
from htmlnode import ParentNode, LeafNode

def main():
    text = "* **bold text**\n* new text"
    t = "this is a paragraph"
    text_ol = """1. first\n2. second
3. third"""
    print(markdown_to_html_node(t).to_html())

main()
