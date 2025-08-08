import os

NODE_FILE_PATH = os.path.dirname(__file__)
DESCRIPTION_FOLDER_NAME = "descriptions"
DESCRIPTION_PATH = os.path.join(NODE_FILE_PATH, DESCRIPTION_FOLDER_NAME)

if not os.path.exists(DESCRIPTION_PATH):
    os.makedirs(DESCRIPTION_PATH)

def get_description_subdirectories():
    subdirectories = [""] # Add empty string for the root descriptions folder
    if not os.path.isdir(DESCRIPTION_PATH):
        return subdirectories

    for root, dirs, files in os.walk(DESCRIPTION_PATH):
        for d in dirs:
            relative_path = os.path.relpath(os.path.join(root, d), DESCRIPTION_PATH)
            subdirectories.append(relative_path.replace("\", "/"))
    
    # Ensure example directory exists if no other subdirectories or files are present
    if not subdirectories and not any(f.endswith(".txt") for f in os.listdir(DESCRIPTION_PATH)):
        example_dir = os.path.join(DESCRIPTION_PATH, "examples")
        if not os.path.exists(example_dir):
            os.makedirs(example_dir)
        placeholder_path = os.path.join(example_dir, "example.txt")
        if not os.path.exists(placeholder_path):
            with open(placeholder_path, 'w', encoding='utf-8') as f:
                f.write("Put your description files in subdirectories under 'descriptions'.")
        subdirectories.append("examples") # Add example directory if created

    return sorted(list(set(subdirectories))) # Use set to remove duplicates and sort

def get_description_files_in_subdir(subdirectory=""):
    full_subdir_path = os.path.join(DESCRIPTION_PATH, subdirectory)
    file_list = []
    if not os.path.isdir(full_subdir_path):
        return ["No files found"]

    for file in os.listdir(full_subdir_path):
        if file.endswith(".txt"):
            file_list.append(os.path.splitext(file)[0]) # Remove .txt extension

    if not file_list:
        # Create an example file in the base descriptions directory if it's empty
        if subdirectory == "": # Only create example in root if no files
            example_dir = os.path.join(DESCRIPTION_PATH, "examples")
            if not os.path.exists(example_dir):
                os.makedirs(example_dir)
            placeholder_path = os.path.join(example_dir, "example.txt")
            if not os.path.exists(placeholder_path):
                with open(placeholder_path, 'w', encoding='utf-8') as f:
                    f.write("Put your description files in subdirectories under 'descriptions'.")
            file_list = ["example"] # Point to the example file

    return sorted(file_list)

class LoadDescriptionNode:
    def __init__(self):
        pass

    @classmethod
    def get_files_for_dropdown(cls, subdirectory):
        return get_description_files_in_subdir(subdirectory)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "subdirectory": (get_description_subdirectories(), {"default": ""}),
                "file_name": (cls.get_files_for_dropdown, {"default": "No files found"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("description_text", "description_name",)
    FUNCTION = "load_description"
    CATEGORY = "Feroc"

    def load_description(self, subdirectory, file_name, **kwargs):
        if file_name == "No files found" or not file_name:
            print("[LoadDescriptionNode] WARNING: No file selected or found.")
            return ("", "")

        # Construct the full path
        full_file_path = os.path.join(DESCRIPTION_PATH, subdirectory, f"{file_name}.txt")
        
        try:
            with open(full_file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return (text, file_name)
        except Exception as e:
            print(f"Error loading description from {full_file_path}: {e}")
            return ("", "")