import os

NODE_FILE_PATH = os.path.dirname(__file__)
DESCRIPTION_FOLDER_NAME = "descriptions"
DESCRIPTION_PATH = os.path.join(NODE_FILE_PATH, DESCRIPTION_FOLDER_NAME)

if not os.path.exists(DESCRIPTION_PATH):
    os.makedirs(DESCRIPTION_PATH)

def get_description_files():
    if not os.path.isdir(DESCRIPTION_PATH):
        return ["No 'descriptions' folder found"]
    
    file_list = []
    for root, dirs, files in os.walk(DESCRIPTION_PATH):
        for file in files:
            if file.endswith(".txt"):
                # Get the relative path from the descriptions folder
                relative_path = os.path.relpath(os.path.join(root, file), DESCRIPTION_PATH)
                # Remove the .txt extension for display
                display_name = os.path.splitext(relative_path)[0]
                file_list.append(display_name.replace("\\", "/")) # Use forward slashes for consistency

    if not file_list:
        # Create an example file in the base descriptions directory if it's empty
        example_dir = os.path.join(DESCRIPTION_PATH, "examples")
        if not os.path.exists(example_dir):
            os.makedirs(example_dir)
        placeholder_path = os.path.join(example_dir, "example.txt")
        if not os.path.exists(placeholder_path):
            with open(placeholder_path, 'w', encoding='utf-8') as f:
                f.write("Put your description files in subdirectories under 'descriptions'.")
        file_list = ["examples/example"]

    return sorted(file_list)

class LoadDescriptionNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "description_file": (get_description_files(), ),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("description_text", "description_name",)
    FUNCTION = "load_description"
    CATEGORY = "Feroc"

    def load_description(self, description_file):
        # Add the .txt extension back for file operations
        file_path_with_ext = os.path.join(DESCRIPTION_PATH, f"{description_file}.txt")
        description_name = os.path.basename(description_file)
        
        try:
            with open(file_path_with_ext, 'r', encoding='utf-8') as f:
                text = f.read()
            return (text, description_name)
        except Exception as e:
            print(f"Error loading description: {e}")
            return ("", "")