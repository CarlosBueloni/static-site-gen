from textnode import TextNode
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    l_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    l_node2 = LeafNode("p", "This is a paragraph of text.")
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
main()
