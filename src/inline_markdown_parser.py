from textnode import TextType, TextNode
import re

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

def extract_markdown_images(text):
    imageTemplate = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(imageTemplate, text)
    return matches

def extract_markdown_links(text):
    linkTemplate = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(linkTemplate, text)
    return matches

def split_nodes_image(old_nodes):
    buffer = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            buffer.append(node)
            continue

        parts = extract_markdown_images(node.text)

        if parts:
            restofthetext = node.text
            for part in parts:
                split_str = f"![{part[0]}]({part[1]})"
                sections = restofthetext.split(split_str, 1)
                before = sections[0]
                after = sections[1] if len(sections) > 1 else ""

                if before:
                    buffer.append(TextNode(before, TextType.TEXT, node.url))
                buffer.append(TextNode(part[0], TextType.IMAGE, part[1]))

                restofthetext = after

            if restofthetext.strip():
                buffer.append(TextNode(restofthetext, TextType.TEXT, node.url))
        else:
            buffer.append(node)

    return buffer

def split_nodes_link(old_nodes):
    buffer = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            buffer.append(node)
            continue

        parts = extract_markdown_links(node.text)

        if parts:
            restofthetext = node.text
            for part in parts:
                sections = restofthetext.split(f"[{part[0]}]({part[1]})", 1)
                before = sections[0]
                after = sections[1] if len(sections) > 1 else ""

                if before:
                    buffer.append(TextNode(before, TextType.TEXT, node.url))
                buffer.append(TextNode(part[0], TextType.LINK, part[1]))

                restofthetext = after

            if restofthetext:
                buffer.append(TextNode(restofthetext, TextType.TEXT, node.url))

        else:
            buffer.append(node)

    return buffer

def text_to_textnodes(text):
    startingNode = TextNode(text, TextType.TEXT)
    processedNodes = [startingNode]
    processedNodes = split_nodes_image(processedNodes)
    processedNodes = split_nodes_link(processedNodes)
    processedNodes = split_nodes_delimiter(processedNodes, "**", TextType.BOLD)
    processedNodes = split_nodes_delimiter(processedNodes, "_", TextType.ITALIC)
    processedNodes = split_nodes_delimiter(processedNodes, "*", TextType.ITALIC)
    processedNodes = split_nodes_delimiter(processedNodes, "`", TextType.CODE)
    return processedNodes

