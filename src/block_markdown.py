import re

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
        is_ul_dash = is_ul_dash and line.startswith("-")
        is_ul_star = is_ul_star and line.startswith("*")
        is_ol = is_ol and line.startswith(f"{count+1}. ") 

    if is_quote:
        return "quote"
    if is_ul_star or is_ul_dash:
        return "unordered_list"
    if is_ol:
        return "ordered_list"

    return "paragraph"
