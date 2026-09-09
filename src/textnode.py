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
        



