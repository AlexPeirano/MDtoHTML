import os
from textnode import markdown_to_html_node
from htmlnode import *

def extract_title(markdown: str)->str:
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            line = line[2:]
            return line
    raise Exception('no first header was found')



def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path) as file:
        stored_file = file.read()

    with open(template_path) as template_file:
        stored_template = template_file.read()

    html_node = markdown_to_html_node(stored_file)
    html_html = html_node.to_html() 
    
    title = extract_title(stored_file)

    html_title = stored_template.replace('{{ Title }}', title)
    html_content = html_title.replace('{{ Content }}', html_html)

    path = os.path.dirname(dest_path)
    if os.path.exists(path):
        with open(dest_path, 'w') as file:
            file.write(html_content)
    else:
        os.makedirs(path)
        with open(dest_path, 'w') as file:
            file.write(html_content)
            

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for file in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, file)
        if os.path.isfile(path):
            if file.endswith(".md"):
                file = file.replace(".md", ".html")
                new_dest_path = os.path.join(dest_dir_path, file)
                generate_page(path, template_path, new_dest_path)
        else:
            new_dir_path = os.path.join(dest_dir_path, file)
            generate_pages_recursive(path, template_path, new_dir_path)





