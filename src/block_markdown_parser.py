from enum import Enum
import textwrap
import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, text_node_to_html_node, TextType
from inline_markdown_parser import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    processedBlocks = []
    for block in blocks:
        if block.strip():
            processedBlocks.append(block.strip())
    return processedBlocks

def block_to_block_type(markdownBlock):
    def is_ordered_list_block(text):
        lines = text.strip().splitlines()
        for i, line in enumerate(lines):
            expected_number = i + 1
            # STRIP LEADING WHITESPACE before matching
            l = line.lstrip()
            match = re.match(rf"^{expected_number}\.\s", l)
            if not match:
                return False
        return True

    if re.match(r"^\s*#{1,6} .*", markdownBlock):
        return BlockType.HEADING
    if re.match(r"^\s*```[\s\S]*?```$", markdownBlock, re.MULTILINE):
        return BlockType.CODE
    if re.match(r"^(\s*>\s?.*\n?)+$", markdownBlock):
        return BlockType.QUOTE
    if re.match(r"^(\s*-\s.*\n?)+$", markdownBlock):
        return BlockType.UNORDERED_LIST
    if is_ordered_list_block(markdownBlock):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def clean_block_text(block, block_type):
    match block_type:
        case BlockType.CODE:
            match = re.search(r"^```(?:[^\n]*)\n([\s\S]*?)```$", block, re.DOTALL)
            return textwrap.dedent(match.group(1))
        case BlockType.QUOTE:
            lines = block.strip().splitlines()
            # Remove ALL leading whitespace before checking for '>'
            cleaned_lines = [line.lstrip()[2:] if line.lstrip().startswith("> ") else line.lstrip().lstrip(">") for line in lines]
            return " ".join(cleaned_lines) # quotes might be single-line
        case BlockType.UNORDERED_LIST:
            lines = block.strip().splitlines()
            cleaned_lines = [line.lstrip()[2:] if line.lstrip().startswith("- ") else line.lstrip().lstrip("-") for line in lines]
            return cleaned_lines
        case BlockType.ORDERED_LIST:
            lines = block.strip().splitlines()
            cleaned_lines = [re.sub(r"^\s*\d+\.\s+", "", line) for line in lines]
            return cleaned_lines
        case BlockType.HEADING:
            #guaranteed to be heading by block_to_block_type
            def get_heading_level(markdown_line):
                match = re.match(r"^(#{1,6})\s", markdown_line)
                return len(match.group(1))
            return get_heading_level(block), re.sub(r"^#{1,6}\s+", "", block)


def markdown_to_html_node(markdown):
    markdownBlocks = markdown_to_blocks(markdown)
    #print(f"Blocks: {markdownBlocks}")
    parent_node = ParentNode("div", [])
    #print(f"parent_node.children: {parent_node.children}")
    for markdownBlock in markdownBlocks:
        markdownBlockType = block_to_block_type(markdownBlock)
        match markdownBlockType:
            case BlockType.CODE:
                code = clean_block_text(markdownBlock, BlockType.CODE)
                codeNode = text_node_to_html_node(TextNode(code, TextType.CODE))
                preNode = ParentNode("pre", [codeNode])
                parent_node.children.append(preNode)
            case BlockType.QUOTE:
                quote = clean_block_text(markdownBlock, BlockType.QUOTE)
                quoteNodes = text_to_textnodes(quote)
                blockquoteNode = ParentNode("blockquote", list(map(text_node_to_html_node, quoteNodes)))
                parent_node.children.append(blockquoteNode)
            case BlockType.UNORDERED_LIST:
                unorderedlines = clean_block_text(markdownBlock, BlockType.UNORDERED_LIST)
                liNodes = []
                for unorderedline in unorderedlines:
                    liNodes.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(unorderedline)))))
                ulNode = ParentNode("ul", liNodes)
                parent_node.children.append(ulNode)
            case BlockType.ORDERED_LIST:
                orderedlines = clean_block_text(markdownBlock, BlockType.ORDERED_LIST)
                liNodes = []
                for orderedline in orderedlines:
                    liNodes.append(ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(orderedline)))))
                olNode = ParentNode("ol", liNodes)
                parent_node.children.append(olNode)
            case BlockType.HEADING:
                levelOfHeading, headingText = clean_block_text(markdownBlock, BlockType.HEADING)
                headingNodes = text_to_textnodes(headingText)
                headNode = ParentNode("h"+str(levelOfHeading), list(map(text_node_to_html_node, headingNodes)))
                parent_node.children.append(headNode)
            case BlockType.PARAGRAPH:
                paragraph_text = re.sub(r'\s+', ' ', markdownBlock.strip())
                paragraphNodes = text_to_textnodes(paragraph_text)
                pNode = ParentNode("p", list(map(text_node_to_html_node, paragraphNodes)))
                parent_node.children.append(pNode)

    return parent_node