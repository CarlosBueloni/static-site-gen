from block_markdown import block_to_block_type, markdown_to_blocks
from inline_markdown import (
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_links,
    split_nodes_images,
    text_to_textnode,
)
from textnode import TextNode, TextType

def main():
    text = ">new\n>job"
    print(block_to_block_type(text))     


main()
