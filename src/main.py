from textnode import TextNode
from textnode import TextType, TextNode

def main():
    new_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(str(new_node))

if __name__ == "__main__":
    main()
