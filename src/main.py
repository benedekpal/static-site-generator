from textnode import TextNode
from textnode import TextType, TextNode
import os
import shutil
from block_markdown_parser import markdown_to_html_node, extract_title

def copy_folder_content(source, target):
    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)
    if os.path.exists(source):
        contents = os.listdir(source)
        for content in contents:
            source_path = os.path.join(source, content)
            target_path = os.path.join(target, content)
            if os.path.isfile(source_path):
                print(f"Copying {source_path} --> {target}")
                shutil.copy2(source_path, target)
            else:
                copy_folder_content(source_path, target_path)

def generate_page(from_path, template_path, dest_path):
    print(f"\nGenerating page from {from_path} to {dest_path} using {template_path}\n")

    fpContent = ""
    tpContent = ""

    with open(from_path, "r") as fp:
        fpContent = fp.read()

    with open(template_path, "r") as tp:
        tpContent = tp.read()

    fpMarkdown = markdown_to_html_node(fpContent).to_html()
    title = extract_title(fpContent)

    tpContent = tpContent.replace("{{ Title }}", title)
    tpContent = tpContent.replace("{{ Content }}", fpMarkdown)
    
    targetDir = os.path.dirname(dest_path)
    if not os.path.isdir(targetDir):
        os.makedirs(targetDir)
    
    with open(dest_path, "w") as dp:
        dp.write(tpContent)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for content in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, content)
        dest_path = os.path.join(dest_dir_path, content.replace(".md", ".html"))

        if os.path.isfile(content_path) and content.endswith(".md"):
            generate_page(content_path, template_path, dest_path)
        elif os.path.isdir(content_path):
            generate_pages_recursive(content_path, template_path, os.path.join(dest_dir_path, content))


def main():
    copy_folder_content("./static", "./public")

    #generate_page("./content/index.md", "./template.html", "./public/index.html")
    generate_pages_recursive("./content", "./template.html", "./public")

if __name__ == "__main__":
    main()
