class HTMLNode:
    def __init__(self, tag: str|None = None, value: str|None = None, children: str|None = None, props:dict[str, str]|None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if (self.props == None) | (self.props == ""):
            return ""
        else:
            string = ""
            for prop in self.props:
                string += f' {prop}="{self.props[prop]}"'
            return string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    
class LeafNode(HTMLNode):
    def __init__(self, tag: str|None, value: str|None, props: dict[str, str]|None = None):
        super().__init__(tag, value, None , props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError('All leaf must have a value')
        elif self.tag == None:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'

class ParentNode(HTMLNode):
    def __init__(self, tag: str|None, children: str|None, props: dict[str, str]|None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError('A parent node has to have a tag attribute')
        elif children is None:
            raise ValueError('A parent node has to have children')
        else:
            string = f'<{self.tag}'
            for child in self.children:
                string += child.to_html() + f'</{child.tag}>'
            return string + f'</{self.tag}>'
