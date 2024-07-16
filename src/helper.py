from textnode import TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.text_type_text.value:
            return LeafNode(None, text_node.text)
        case TextType.text_type_bold.value:
            return LeafNode("b", text_node.text)
        case TextType.text_type_italic.value:
            return LeafNode("i", text_node.text)
        case TextType.text_type_code.value:
            return LeafNode("code", text_node.text)
        case TextType.text_type_link.value:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.text_type_image.value:
            return LeafNode("img", "", {"src":text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Text type not found")
