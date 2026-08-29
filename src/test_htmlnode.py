import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
   def test_propsToHtml(self):
        node = HTMLNode(None, None, None, {"monstre": "double", "okalash": "brody"})

   def test_props2(self):
        node = HTMLNode(None, None, None, None)
        self.assertTrue(node.props_to_html() == "")

   def test_repr(self):
        node =HTMLNode("<p>", "jsp", "nnplus", None)
        self.assertEqual(node.__repr__(), 'HTMLNode(<p>, jsp, nnplus, None)')

if __name__ == "__main__":
    unittest.main()
