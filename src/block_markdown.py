import re
from inline_markdown import text_node_to_html_node, text_to_textnode
from htmlnode import ParentNode, LeafNode

def markdown_to_blocks(text):
    blocks = [block.strip() for block in text.split("\n\n") if len(block.strip()) > 0]
    return blocks

def block_to_block_type(block):
    headings_re = r"#{1,6} "
    if re.match(headings_re, block):
         return "heading"
    if block.startswith("```") and block.endswith("```"):
        return "code"
    is_quote = True
    is_ul_dash = True
    is_ul_star = True
    is_ol = True
    for count, line in enumerate(block.splitlines()):
        is_quote = is_quote and line.startswith(">")
        is_ul_dash = is_ul_dash and line.startswith("- ")
        is_ul_star = is_ul_star and line.startswith("* ")
        is_ol = is_ol and line.startswith(f"{count+1}. ") 
    if is_quote:
        return "quote"
    if is_ul_star or is_ul_dash:
        return "unordered_list"
    if is_ol:
        return "ordered_list"
    return "paragraph"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        html_nodes.append(block_to_html_node(block))
    return ParentNode("div", html_nodes)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == "heading":
        heading, text = block.split(" ", 1)
        text = text_to_children(text)
        return ParentNode(f"h{heading.count("#")}", text)
    if block_type == "code":
        text = text_to_children(block.strip("```").lstrip("\n"))
        return ParentNode("pre", [ParentNode("code", text)])
    if block_type == "quote":
        lines = block.splitlines()
        new_lines = []
        for line in lines:
            new_lines.append(line.split(" ",1)[1].strip())
        text = ' '.join(new_lines)
        text = text_to_children(text)
        return ParentNode("blockquote", text)
    if block_type == "unordered_list":
        children = []
        for line in block.splitlines():
            children.append(ParentNode("li",text_to_children(line.split(" ", 1)[1])))
        return ParentNode("ul", children)
    if block_type == "ordered_list":
        children = []
        for line in block.splitlines():
            children.append(ParentNode("li", text_to_children(line.split(" ", 1)[1])))
        return ParentNode("ol", children)
    if block_type == "paragraph":
        lines = block.splitlines()
        paragraph = ' '.join(lines)
        children = text_to_children(paragraph)
        return ParentNode("p", children)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnode(text)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

