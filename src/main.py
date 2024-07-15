from textnode import TextNode
from htmlnode import HTMLNode, LeafNode

def main():
    l_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    l_node2 = LeafNode("p", "This is a paragraph of text.")
    print(l_node2.to_html())
    print(l_node.to_html())

main()
