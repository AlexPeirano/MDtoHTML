from textnode import *

def test_normal_bold(self):
    node = TextNode('This a **bold** one', TextType.BOLD)
    liste = split_nodes_delimiter([node], '**', TextType.BOLD)
    self.assertEqual(liste, [TextNode('This is a ', TextType.TEXT), TextNode('bold', TextType.BOLD), TexNode(' one', TextType.TEXT)])

def test_single_multiple(self):
    node = TextNode('`coding block`', TextType.CODE)
    node2 = TextNode('This a `bold one`', TextType.CODE)
    node_liste = [node, node2]
    liste = split_nodes_delimiter(node_liste, '`', TextType.CODE)
    self.assertEqual(liste, [TextNode('coding block', TextType.CODE), TextNode('This is a ', TextType.TEXT), TextNode('bold one', TextType.CODE)])


