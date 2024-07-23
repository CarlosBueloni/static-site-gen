from helper import (
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_links,
    split_nodes_images
)
from textnode import TextNode, TextType
def main():
    text = "[link](https://google.com) This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    img_text = "a dog ![dog image](/imgs/dog.png) and a cat ![cat image](/images/cat.png)"
    node =  TextNode(
        text,
        TextType.link.value,)
    img_node = TextNode(
            img_text,
            TextType.image.value)
    print(split_nodes_images([img_node]))
main()
