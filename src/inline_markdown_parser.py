from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    buffer = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            buffer.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown syntax, unmatched delimiter")

        for i, part in enumerate(parts):
            if part == "":
                continue  # Skip empty strings
            if i % 2 == 0:
                buffer.append(TextNode(part, TextType.TEXT, node.url))
            else:
                buffer.append(TextNode(part, text_type, node.url))

    return buffer
