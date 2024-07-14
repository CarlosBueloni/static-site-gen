from textnode import TextNode

def main():
    node = TextNode("this is text", "bold", "www.google.com")
    print(node)
    print(node == TextNode("this is text", "bold", "www.google.com"))

main()
