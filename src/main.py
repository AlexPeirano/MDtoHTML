import os
import sys
import shutil
from textnode import *
from generate_page import *

static_path = "./static"
content_path = "./content"
docs_path = "./docs" 

def static_to_public(docs_path:str, static_path: str):
# first removes all of the files from the public dir
    for filename in os.listdir(docs_path):
        file_path = os.path.join(docs_path, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            shutil.rmtree(file_path)
# then copies every thing from static (including subdirs) and copies them into public
    
def copy_static_to_public(docs_path:str, static_path:str):
    for obj in os.listdir(static_path):
        obj_path = os.path.join(static_path, obj)
        if os.path.isfile(obj_path):
            obj_dest = os.path.join(docs_path, obj)
            shutil.copy(obj_path, obj_dest)
        else:
            obj_dest = os.path.join(docs_path, obj)
            os.mkdir(obj_dest)
            copy_static_to_public(obj_dest, obj_path)

if sys.argv:
    basepath = sys.argv[0]
else:
    basepath = '/'

def main():
    static_to_public(docs_path, static_path) 
    copy_static_to_public(docs_path, static_path)
    # gen page from content/index.md using template.html and write to public/index.html
    template_path = "./template.html"

    new_index_path = os.path.join(docs_path, 'index.html')    
    index_path = os.path.join(content_path, 'index.md')
    generate_pages_recursive(content_path, template_path, docs_path, basepath)  
main()

    
