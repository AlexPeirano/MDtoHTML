import os
import shutil
from textnode import *
from generate_page import *

public_path = "./public" 
static_path = "./static"
content_path = "./content"

def static_to_public(public_path:str, static_path: str):
# first removes all of the files from the public dir
    for filename in os.listdir(public_path):
        file_path = os.path.join(public_path, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            shutil.rmtree(file_path)
# then copies every thing from static (including subdirs) and copies them into public
    
def copy_static_to_public(public_path:str, static_path:str):
    for obj in os.listdir(static_path):
        obj_path = os.path.join(static_path, obj)
        if os.path.isfile(obj_path):
            obj_dest = os.path.join(public_path, obj)
            shutil.copy(obj_path, obj_dest)
        else:
            obj_dest = os.path.join(public_path, obj)
            os.mkdir(obj_dest)
            copy_static_to_public(obj_dest, obj_path)

def main():
    static_to_public(public_path, static_path) 
    copy_static_to_public(public_path, static_path)
    # gen page from content/index.md using template.html and write to public/index.html
    template_path = "./template.html"

    new_index_path = os.path.join(public_path, 'index.html')    
    index_path = os.path.join(content_path, 'index.md')
    generate_pages_recursive(content_path, template_path, public_path)  
main()

    
