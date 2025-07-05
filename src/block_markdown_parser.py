

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    processedBlocks = []
    for block in blocks:
        if block:
            processedBlocks.append(block.strip())
    return processedBlocks
