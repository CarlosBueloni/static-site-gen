from helper import (
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_links,
    split_nodes_images,
    text_to_textnode,
)
from textnode import TextNode, TextType
def main():
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)" 
    print(split_nodes_links([TextNode(text, TextType.text.value)]))
main()
