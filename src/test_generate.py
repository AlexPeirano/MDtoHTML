import unittest
from generate_page import *

class TestGenerate(unittest.TestCase):

    def test_logic(self):
        markdown = "This is not a heading\n# This is one"
        self.assertEqual('This is one', extract_title(markdown))


if __name__ == '__main__':
    unittest.main()
