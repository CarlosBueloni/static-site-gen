from textnode import TextType, TextNode
from htmlnode import LeafNode
import re

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.text.value:
            return LeafNode(None, text_node.text)
        case TextType.bold.value:
            return LeafNode("b", text_node.text)
        case TextType.italic.value:
            return LeafNode("i", text_node.text)
        case TextType.code.value:
            return LeafNode("code", text_node.text)
        case TextType.link.value:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.image.value:
            return LeafNode("img", "", {"src":text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Text type not found")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError("Invalid markdown syntax, please close all delimters")
        if node.text_type != TextType.text.value:
            new_nodes.append(node)
        else:
            new_nodes.extend(
                [TextNode(n, TextType.text.value) if i % 2 == 0 
                    else TextNode(n, text_type) 
                        for i, n in enumerate(node.text.split(delimiter)) if len(n) > 0
                ]
            )

    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text.value:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, please close link section")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.text.value))
            new_nodes.append(TextNode(link[0], TextType.link.value, link[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.text.value))
        return new_nodes

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.text.value:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, please close image section")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.text.value))
            new_nodes.append(TextNode(image[0], TextType.image.value, image[1]))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, TextType.text.value))
        return new_nodes

def extract_markdown_images(text):
    texts = re.findall(r"!\[(.*?)\]", text)
    urls = re.findall(r"\((.*?)\)", text)
    return list(zip(texts, urls))

def extract_markdown_links(text):
    texts = re.findall(r"\[(.*?)\]", text)
    urls = re.findall(r"\((.*?)\)", text)
    return list(zip(texts, urls))

