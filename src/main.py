import os
import shutil
from textnode import *
import shutil

public_path = "/Users/alexpeirano/Documents/personal coding/StaticSiteGenerator/MDtoHTML/public"

static_path = "/Users/alexpeirano/Documents/personal coding/StaticSiteGenerator/MDtoHTML/static"

def static_to_public(public_path:str, static_path: str):
    for filename in os.listdir(public_path):
        file_path = os.path.join(public_path, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            shutil.rmtree(file_path)

def main():
    static_to_public(public_path, static_path) 

main()
    

    
