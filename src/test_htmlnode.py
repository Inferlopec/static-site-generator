import unittest
from htmlnode import HTMLnode, LeafNode, ParentNode

class TestHTMLnode(unittest.TestCase):
    def test_init(self):
        node = HTMLnode("div", "content", [], {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "content")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    def test_props_to_html_empty(self):
        node = HTMLnode("p", "text")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HTMLnode("a", "link", props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')
        
    def test_props_to_html_with_single_prop(self):
        node = HTMLnode("span", "text", props={"class": "highlight"})
        self.assertEqual(node.props_to_html(), ' class="highlight"')
        
    def test_repr(self):
        node = HTMLnode("div", "content", [], {"class": "container"})
        self.assertEqual(repr(node), 'HTMLnode(div, content, [], {\'class\': \'container\'})')

class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode("p", "text", {"class": "highlight"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"class": "highlight"})

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "text")
        self.assertEqual(node.to_html(), "<p>text</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me", {"href": "https://example.com", "class": "button"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" class="button">Click me</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Plain text")
        self.assertEqual(node.to_html(), "Plain text")

    def test_leaf_to_html_empty_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_to_html_empty_string_value(self):
        node = LeafNode("p", "")
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_init(self):
        children = [LeafNode("p", "paragraph")]
        node = ParentNode("div", children, {"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, {"class": "container"})
    
    def test_parent_to_html_basic(self):
        children = [LeafNode("p", "paragraph")]
        node = ParentNode("div", children)
        self.assertEqual(node.to_html(), "<div><p>paragraph</p></div>")
    
    def test_parent_to_html_with_props(self):
        children = [LeafNode("p", "paragraph")]
        node = ParentNode("div", children, {"class": "container", "id": "main"})
        self.assertEqual(node.to_html(), '<div class="container" id="main"><p>paragraph</p></div>')
    
    def test_parent_to_html_multiple_children(self):
        children = [
            LeafNode("p", "paragraph 1"),
            LeafNode("p", "paragraph 2"),
            LeafNode("span", "some text")
        ]
        node = ParentNode("div", children)
        self.assertEqual(node.to_html(), "<div><p>paragraph 1</p><p>paragraph 2</p><span>some text</span></div>")
    
    def test_parent_to_html_nested(self):
        inner_children = [LeafNode("li", "item 1"), LeafNode("li", "item 2")]
        inner_parent = ParentNode("ul", inner_children)
        outer_children = [
            LeafNode("h1", "Title"),
            inner_parent,
            LeafNode("p", "footer")
        ]
        node = ParentNode("div", outer_children)
        self.assertEqual(node.to_html(), "<div><h1>Title</h1><ul><li>item 1</li><li>item 2</li></ul><p>footer</p></div>")
    
    def test_parent_no_tag_raises_error(self):
        children = [LeafNode("p", "paragraph")]
        node = ParentNode(None, children)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_parent_no_children_raises_error(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_parent_empty_children_list_raises_error(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
