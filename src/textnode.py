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
    
