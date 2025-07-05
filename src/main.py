from textnode import TextNode
from textnode import TextType, TextNode
import os
import shutil

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


def main():
    copy_folder_content("./static", "./public")

    new_node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(str(new_node))

if __name__ == "__main__":
    main()
