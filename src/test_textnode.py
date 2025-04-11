import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, parse_text_with_delimiters
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_init_default_url(self):
        node = TextNode("Plain text", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_eq_one_with_url_one_without(self):
        node = TextNode("Text", TextType.LINK, "https://example.com")
        node2 = TextNode("Text", TextType.LINK)
        self.assertNotEqual(node, node2)
    
    def test_eq_false_with_different_types(self):
        node1 = TextNode("Text", TextType.LINK, "https://example.com")
        node2 = TextNode("Text", TextType.IMAGE, "https://example.com")
        self.assertNotEqual(node1, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold)")

    def test_repr_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        self.assertEqual(repr(node), "TextNode(This is a link, link, https://example.com)")
    
    def test_repr_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://example.com/image.png")
        self.assertEqual(repr(node), "TextNode(This is an image, image, https://example.com/image.png)")

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("Plain text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Plain text")
        self.assertEqual(html_node.props, None)
    
    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None)
    
    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)
    
    def test_text_node_to_html_node_code(self):
        text_node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")
        self.assertEqual(html_node.props, None)
    
    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Link text", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
    
    def test_text_node_to_html_node_image(self):
        text_node = TextNode("Image alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Image alt text"})
    
    def test_text_node_to_html_node_link_without_url_raises_error(self):
        text_node = TextNode("Link text", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)
    
    def test_text_node_to_html_node_image_without_url_raises_error(self):
        text_node = TextNode("Image alt text", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)

class TestParseTextWithDelimiters(unittest.TestCase):
    def test_basic_parsing(self):
        text = "Hello *world*"
        result = parse_text_with_delimiters(text, "*")
        expected = [("Hello ", False), ("world", True)]
        self.assertEqual(result, expected)
    
    def test_multiple_delimiters(self):
        text = "Hello *world* and *universe*"
        result = parse_text_with_delimiters(text, "*")
        expected = [("Hello ", False), ("world", True), (" and ", False), ("universe", True)]
        self.assertEqual(result, expected)
    
    def test_delimiter_at_start(self):
        text = "*bold* text"
        result = parse_text_with_delimiters(text, "*")
        expected = [("", False), ("bold", True), (" text", False)]
        self.assertEqual(result, expected)
    
    def test_delimiter_at_end(self):
        text = "text *bold*"
        result = parse_text_with_delimiters(text, "*")
        expected = [("text ", False), ("bold", True)]  
        self.assertEqual(result, expected)
    
    def test_empty_text(self):
        text = ""
        result = parse_text_with_delimiters(text, "*")
        self.assertEqual(result, [])
    
    def test_delimiter_only(self):
        text = "**"
        result = parse_text_with_delimiters(text, "*")
        expected = [("", False), ("", True)]  
        self.assertEqual(result, expected)
    
    def test_consecutive_delimiters(self):
        text = "a**b"
        result = parse_text_with_delimiters(text, "*")
        expected = [("a", False), ("", True), ("b", False)]
        self.assertEqual(result, expected)
    
    def test_unclosed_delimiter(self):
        text = "Hello *world"
        with self.assertRaises(ValueError):
            parse_text_with_delimiters(text, "*")
    
    def test_multi_char_delimiter(self):
        text = "Hello **world**"
        result = parse_text_with_delimiters(text, "**")
        expected = [("Hello ", False), ("world", True)] 
        self.assertEqual(result, expected)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_splitting(self):
        nodes = [TextNode("Hello *world*", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD)
        ]
        self.assertEqual(result, expected)
    
    def test_non_text_nodes_unchanged(self):
        nodes = [
            TextNode("Hello", TextType.BOLD),
            TextNode("*world*", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        
        expected = [
            TextNode("Hello", TextType.BOLD),
            TextNode("world", TextType.ITALIC)
        ]
        self.assertEqual(result, expected)
    
    def test_multiple_nodes(self):
        nodes = [
            TextNode("Hello *world*", TextType.TEXT),
            TextNode("Another *text*", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("Another ", TextType.TEXT),
            TextNode("text", TextType.BOLD)
        ]
        self.assertEqual(result, expected)
    
    def test_empty_segments_skipped(self):
        nodes = [TextNode("**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        self.assertEqual(result, [])
    
    def test_unclosed_delimiter_raises_error(self):
        nodes = [TextNode("Hello *world", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "*", TextType.BOLD)

if __name__ == "__main__":
    unittest.main()




