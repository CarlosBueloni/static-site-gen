from textnode import TextNode
from htmlnode import HTMLNode

def main():
    node = HTMLNode("p", "text", None, {
        "href": "https://www.google.com", 
        "target": "_blank",
        })
    print(f"{node.props_to_html()}")
    print(node)

main()
