import unittest
from textnode import block_to_block_type, BlockType

class TestBlockTypes(unittest.TestCase):

    def test_heading(self):
        block1 = "# this is a first heading"
        block2 = "## this is a first heading"
        block3 = "### this is a first heading"
        block4 = "#### this is a first heading"
        block5 = "##### this is a first heading"
        block6 = "###### this is a first heading"
        
        
        self.assertEqual(block_to_block_type(block1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block2), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block3), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block4), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block5), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block6), BlockType.HEADING)

    def test_code(self):
        block = "```\nthis is a code block```"

        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote block\n> Also this"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered(self):
        block = "- This is a list\n- Also this"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST
        )
    def test_ordered(self):
        block = "1. first point\n2. point"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERERD_LIST)

if __name__ == "__main__":
    unittest.main()
