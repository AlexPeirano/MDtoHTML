import unittest
from textnode import *

class TestTextNode(unittest.TestCase):  
    def test_eq(self):
        node = TextNode('This is a text node', TextType.BOLD)
        node2 = TextNode('This is a text node', TextType.BOLD)
        
        self.assertEqual(node, node2)

    def test_noteq(self): 
        node = TextNode('This is a text node', TextType.CODE)
        node2 = TextNode('This is a text node', TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_urlnone(self):
        node = TextNode('This is a text node', TextType.BOLD)
        self.assertTrue(node.url == None)

if __name__ == "__main__":
    unittest.main()
   
