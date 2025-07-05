from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, othernode):
        try:
            if (self.text == othernode.text) and (self.text_type == othernode.text_type) and (self.url == othernode.url):
                return True
            return False
        except Exception as e:
            print(f"Error comparing two TextNode(s): {e}")
            return False
    
    def __repr__(self):
        try:
            return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        except Exception as e:
            return "Could't get information"
    

from htmlnode import LeafNode

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
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            print(f"{TextType.IMAGE}: {text_node}")
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid TextType for html conversion!")