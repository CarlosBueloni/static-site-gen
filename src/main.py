from block_markdown import markdown_to_html_node
from helper import copy_content, extract_title, generate_page, generate_pages_recursive
from htmlnode import LeafNode, ParentNode

def main():
    copy_content("static", "public")
    generate_pages_recursive("content", "template.html", "public")
main()
