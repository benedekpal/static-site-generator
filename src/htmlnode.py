

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
        

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        if self.props:
            prop = self.props_to_html()
            return f"<{self.tag}{prop}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"