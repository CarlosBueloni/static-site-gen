from block_markdown import markdown_to_blocks
from inline_markdown import (
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_links,
    split_nodes_images,
    text_to_textnode,
)
from textnode import TextNode, TextType

def main():
    text =  """
    # This is a heading

    This is a paragraph of text. It has some **bold** and *italic* words inside of it.

    * This is the first list item in a list block
    * This is a list item
    * This is another list item
    """
    print(markdown_to_blocks(text))


main()
