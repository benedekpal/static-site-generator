from enum import Enum
import re

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
        if block:
            processedBlocks.append(block.strip())
    return processedBlocks

def block_to_block_type(markdownBlock):
    def is_ordered_list_block(text):
        lines = text.strip().splitlines()
        for i, line in enumerate(lines):
            expected_number = i + 1
            match = re.match(rf"^{expected_number}\.\s", line)
            if not match:
                return False
        return True

    if re.match(r"#{1,6} .*", markdownBlock):
        return BlockType.HEADING
    if re.match(r"^```[\s\S]*?```$", markdownBlock, re.MULTILINE):
        return BlockType.CODE
    if re.match(r"^(>\s?.*\n?)+$", markdownBlock):
        return BlockType.QUOTE
    if re.match(r"^(-\s.*\n?)+$", markdownBlock):
        return BlockType.UNORDERED_LIST
    if is_ordered_list_block(markdownBlock):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH