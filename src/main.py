from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from helper import text_node_to_html_node

def main():
    t_node = TextNode("this is a bold text", TextType.text_type_bold.value)
    t_node2 = TextNode("this is a link text", TextType.text_type_link.value, "https://google.com")
    l_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    l_node2 = LeafNode("p", "This is a paragraph of text.")
    print(t_node2)
    print(text_node_to_html_node(t_node2).to_html())
    print(l_node2.to_html())
    print(l_node.to_html())
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            ParentNode(
            "p",
            [
                LeafNode("b", "Bold text inside"),
                LeafNode(None, "Normal text inside"),
                LeafNode("i", "italic text inside"),
                LeafNode(None, "Normal text inside"),
            ]
            ),
            LeafNode(None, "Normal text"),
        ]
    )
    print(node.to_html())
    print(TextType.text_type_bold.value)
main()
