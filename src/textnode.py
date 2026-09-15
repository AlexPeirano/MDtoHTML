from extract_md import *
from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "text"
    BOLD = "**bold text**"
    ITALIC = "_italic text_"
    CODE = "`code text`"
    LINKS = "[anchor text](url)"
    IMAGES = "![alt text](url)"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERERD_LIST = "ordererd_list"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
   
    def __eq__(self, other)->bool:
        if (self.text == other.text) & (self.text_type == other.text_type) & (self.url == other.url):
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node: TextNode)->LeafNode:
    if text_node is None:
        raise Exception('the text node is none')
    else:
        if text_node.text_type == TextType.TEXT:
            return LeafNode(none,text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode('b', text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode('i', text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode('code', text_node.text)
        elif text_node.text_type == TextType.link:
            return LeafNode('a', text_node.text, {'href': text_node.url})
        elif text_node.text_type == TextType.IMAGE:
            return LeafNode('img',"", {'src': text_node.url, 'alt': text_node.text})

### This parts treats inline markdown


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type:TextType)-> list[TextNode]:
    Liste = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            liste.append(node)
        else:
            split_node = node.text.split(delimiter)
            if len(split_node) % 2 == 0:
                raise Exception('Closing delimiter not found')
            else:
                for i in range(len(split_node)):
                    if split_node[i] == "":
                        continue
                    elif i % 2 == 0:
                        textnode = TextNode(split_node[i], text_type=TextType.TEXT)
                        liste.append(textnode)
                    else:
                        textnode = TextNode(split_node[i], text_type=text_type)
                        liste.append(textnode)
    return Liste
                
                    
def split_nodes_image(old_nodes: list[TextNode])->list[TextNode]:
    Liste = []
    for node in old_nodes:
        extracted = extract_markdown_images(node.text)
        if len(extracted) == 1:
            Liste.append(node.text)
        else:
            i = 0
            for i in range(len(extracted)):
                split1 = node.text.split(f"![{extracted[i][0]}]({extracted[i][1]})", maxsplit=1)
                if len(split1) == 1:
                    continue
                else:
                    Liste.append(TextNode(split1[0], TextType.TEXT))
                    split1.pop(0)
                    split1 = ''.join(split1)
                    Liste.append(TextNode(extracted[i][0], TextType.IMAGES, url=extracted[i][1]))
    return Liste



       



def split_nodes_links(old_nodes: list[TextNode])->list[TextNode]:
    Liste = []
    for node in old_nodes:
        extracted = extract_markdown_links(node.text)
        if len(extracted) == 1:
            Liste.append(node.text)
        else:
            i = 0
            for i in range(len(extracted)):
                split1 = node.text.split(f"![{extracted[i][0]}]({extracted[i][1]})", maxsplit=1)
                if len(split1) == 1:
                    continue
                else:
                    Liste.append(TextNode(split1[0], TextType.TEXT))
                    split1.pop(0)
                    split1 = ''.join(split1)
                    Liste.append(TextNode(extracted[i][0], TextType.LINKS, url=extracted[i][1]))

    return Liste
        


def text_to_textnodes(text: str)->list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)

    return nodes


# This part treats 'block' markdown (headers, paragraphs and lists'
## Takes raw md and returns a list of block strings
def mardown_to_blocks(markdown: str)->list[str]:
    splitted = markdown.split('\n\n')
    striped = [split.strip() for split in splitted]
    for block in striped:
        if block == "":
            striped.pop(block)
    return striped

## Takes a block of md text and returns a BlockType object
def block_to_block_type(block: str)->BlockType:
    headings = ['# ', '## ', '### ', '#### ', '##### ', '###### ']  
    code = '```\n' # must end with ``` 
    quote = '>' # a space is not required after but is allowed
    unordered = '- '
    ordered = '. ' # must be preceded by a isdigit()

    def is_heading(block: str)->bool:
        for i in headings:
            if block.startswith(i):
                return True
            else:
                continue
        return False

    def is_code(block: str)->bool:
        if block.startswith(code) and block.endswith('```'):
            return True
        else:
            return False


    # split on newlines 
    splitted = block.splitlines()

    def is_quote(lines: list[str])->bool:
        for line in lines:
            if not line.startswith(quote):
                return False
        return True

    def is_unordered(lines: list[str])->bool:
        for line in lines:
            if not line.startswith(unordered):
                return False
        return True

    def is_ordered(lines: list[str])->bool:
        nums = []
        for line in lines:
            split = line.split(ordered, maxsplit=1)
            if len(split) == 1:
                return False
            elif not split[0].isdigit():
                return False
            nums.append(int(split[0]))
        if not nums or nums[0] != 1:
            return False
        i = 0
        for i in range(len(nums)-1):
            if nums[i+1] != nums[i] + 1:
                return False
        return True

    if is_heading(block):
        return BlockType.HEADING
    if is_code(block):
        return BlockType.CODE
    if is_quote(splitted):
        return BlockType.QUOTE
    if is_unordered(splitted):
        return BlockType.UNORDERED_LIST
    if is_ordered(splitted):
        return BlockType.ORDERERD_LIST
    else:
        return BlockType.PARAGRAPH

