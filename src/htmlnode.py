

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        buffer = ""
        for key, val in self.props.items():
            buffer += f" {key}=\"{val}\""
        return buffer
    
    def __repr__(self):
        try:
            return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
        except Exception as e:
            return "Could't get information"