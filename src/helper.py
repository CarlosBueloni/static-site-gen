import os
from os.path import isfile
import shutil
import pathlib

from block_markdown import markdown_to_blocks, markdown_to_html_node

def copy_content(source, destination):
    if(os.path.exists(destination)):
        shutil.rmtree(destination)
    os.mkdir(destination)
    make_copies(source, destination)

def make_copies(source, destination):
    for item in os.listdir(source):
        new_path = os.path.join(source, item)
        if os.path.isfile(new_path):
            print(f"Copying: {new_path} to {shutil.copy(new_path, destination)}")
        else:
            new_dest = os.path.join(destination, item)
            if(not os.path.exists(new_dest)):
                os.mkdir(new_dest)
            copy_content(new_path, new_dest)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:]
    raise ValueError("Invalid syntax: there is no title")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    source = read_from_source(from_path)
    template = read_from_source(template_path)
    html_body = markdown_to_html_node(source).to_html()
    title = extract_title(source)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_body)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as my_file:
        my_file.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        current_path = pathlib.Path(os.path.join(dir_path_content, item))
        dest_path = pathlib.Path(os.path.join(dest_dir_path, item))
        if os.path.isfile(current_path) and str(pathlib.Path(current_path))[-2:] == "md":
            dest_path = pathlib.Path(os.path.join(dest_dir_path, item[:-2] + "html"))
            generate_page(current_path, template_path, dest_path)
        else:
            generate_pages_recursive(current_path, template_path, dest_path)

def read_from_source(source):
    with open(source, "r") as my_file:
        return my_file.read()
