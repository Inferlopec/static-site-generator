from enum import Enum
from htmlnode import LeafNode



class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (
            self.text == other.text and 
            self.text_type == other.text_type and 
            self.url == other.url
        )
    
    def __repr__(self):
        if self.url:  
            return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        return f"TextNode({self.text}, {self.text_type.value})"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if not text_node.url:
                raise ValueError("Link text node must have a URL")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError("Image text node must have a URL")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid text type")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split text nodes based on delimiter pairs and convert text between delimiters to the specified type.
    Example: "Hello *world*" with delimiter "*" and TextType.BOLD would result in
             TextNode("Hello ", TEXT) and TextNode("world", BOLD)
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Skip non-text nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        # Setup for parsing the current node
        text = old_node.text
        segments = parse_text_with_delimiters(text, delimiter)
        
        # Create nodes from the parsed segments
        for segment in segments:
            content, is_delimited = segment
            if content:  # Skip empty segments
                node_type = text_type if is_delimited else TextType.TEXT
                new_nodes.append(TextNode(content, node_type))
    
    return new_nodes

def parse_text_with_delimiters(text, delimiter):
    """
    Parse text with delimiters and return a list of (content, is_delimited) tuples.
    Raises ValueError if a delimiter is not properly closed.
    """
    segments = []
    current_text = ""
    inside_delimiter = False
    i = 0
    
    while i < len(text):
        # Check if we're at a delimiter
        if text[i:i+len(delimiter)] == delimiter:
            # Save the current segment before switching states
            segments.append((current_text, inside_delimiter))
            current_text = ""
            
            # Toggle the delimiter state
            inside_delimiter = not inside_delimiter
            i += len(delimiter)
        else:
            # Add the current character to our segment
            current_text += text[i]
            i += 1
    
    # Check for unclosed delimiter
    if inside_delimiter:
        raise ValueError(f"Unclosed delimiter '{delimiter}' in text: '{text}'")
    
    # Add the final segment if we have any text left
    if current_text:
        segments.append((current_text, inside_delimiter))
    
    return segments



