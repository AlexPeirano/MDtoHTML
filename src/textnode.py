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
    ORDERED_LIST = "ordered_list"

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
            return LeafNode(None,text_node.text)
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
    liste = []
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
    return liste
                
                    
def split_nodes_image(old_nodes: list[TextNode])->list[TextNode]:
    Liste = []
    for node in old_nodes:
        extracted = extract_markdown_images(node.text)
        if len(extracted) == 0:
            Liste.append(node)
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
        if len(extracted) == 0:
            Liste.append(node)
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
def markdown_to_blocks(markdown: str)->list[str]:
    import re
    splitted = re.split(r'\n[ \t]*\n', markdown)
    result = []
    for block in splitted:
        block = block.strip()
        if block != "":
            result.append(block)
    return result

## Takes a block of md text and returns a BlockType object
def block_to_block_type(block: str)->BlockType:
    headings = ['# ', '## ', '### ', '#### ', '##### ', '###### ']  
    code = '```\n' # must end with ``` 
    quote = '>' # a space is not required after but is allowed
    unordered = ['- ', '* ', '+ ']
    ordered = '. ' # must be preceded by a isdigit()

    def is_heading(block: str)->bool:
        for i in headings:
            if block.startswith(i):
                return True
            else:
                continue
        return False

    def is_code(block: str)->bool:
        stripped = block.strip()
        return stripped.startswith('```') and stripped.endswith('```') and len(stripped) > 3


    # split on newlines 
    splitted = block.splitlines()

    def is_quote(lines: list[str])->bool:
        for line in lines:
            if not line.startswith(quote):
                return False
        return True

    def is_unordered(lines: list[str])->bool:
        for line in lines:
            for tag in unordered:
                if not line.startswith(tag):
                    continue
                else:
                    return True
            return False

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
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str)->HTMLNode:
    blocks = markdown_to_blocks(markdown)
# helper func to assign blocktype to html nodes 
# create a text to children helper function 
# func that stripes the block syntax 
    def blocktype_to_tag(blocktype: BlockType)->str:
        if blocktype == BlockType.QUOTE:
            return "blockquote"
        elif blocktype == BlockType.UNOREDERD_LIST:
            return "ul"
        elif blocktype == BlockType.ORDERED_LIST:
            return "ol"
        elif blocktype == BlockType.CODE:
            return "code"
        elif blocktype == BlockType.PARAGRAPH:
            return "p"
        
    def heading_helper(block):
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                continue
        tag = f"h{count}"
        block = block[count+1:]

        return (tag, block)

    def o_list_helper(block):
        lines = block.split("\n")
        result = []
        count = 1
        for line in lines:
            line = line.removeprefix(f'{count}. ')
            count += 1
            children = text_to_children(line)
            node = ParentNode(tag='li', children=children)
            result.append(node)
        return result

    def u_list_helper(block):
        lines = block.split('\n')
        result = []
        for line in lines:
            line = line.removeprefix('* ').removeprefix('+ ').removeprefix('- ')
            children = text_to_children(line)
            node = ParentNode(tag='li', children=children)
            result.append(node)
        return result
            
    def block_to_html_node(block: str)->HTMLNode:
        blocktype = block_to_block_type(block)
        if blocktype == BlockType.PARAGRAPH:
            text = " ".join(line.strip() for line in block.splitlines())
            children = text_to_children(text)
            node = ParentNode(tag='p', children=children)
            return node
        
        elif blocktype == BlockType.QUOTE:
            mot = []
            lines = block.split('\n')
            for line in lines:  
                line = line.removeprefix('> ')
                mot.append(line)
            mot = ' '.join(mot)
            children = text_to_children(mot)
            node = ParentNode(tag='blockquote', children=children)
            return node

        elif blocktype == BlockType.UNORDERED_LIST:
            children = u_list_helper(block)
            node = ParentNode(tag='ul', children=children)
            return node

        elif blocktype == BlockType.ORDERED_LIST:
            children = o_list_helper(block)
            node = ParentNode(tag='ol', children=children)
            return node

        elif blocktype == BlockType.HEADING:
            tag, block = heading_helper(block)
            children = text_to_children(block)
            node = ParentNode(tag=tag, children=children)
            return node
        
        elif blocktype == BlockType.CODE:
            inner = block.strip()[3:-3].strip()  # remove ``` fences and surrounding whitespace
            lines = inner.splitlines()
            content = "\n".join(line.strip() for line in lines) + "\n"
            textnode = TextNode(content, TextType.TEXT)
            node = text_node_to_html_node(textnode)
            code_node = ParentNode(tag='code', children=[node])
            pre_node = ParentNode(tag='pre', children=[code_node])
            return pre_node



    def text_to_children(text:str):
        node_list = text_to_textnodes(text)
        children = []
        for node in node_list:
            child = text_node_to_html_node(node)
            children.append(child)
        return children

    liste = []
    
    for block in blocks:
        node = block_to_html_node(block)
        liste.append(node)
    big_node = ParentNode(tag='div', children=liste)
    return big_node
