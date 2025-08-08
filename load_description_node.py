import os
import time

NODE_FILE_PATH = os.path.dirname(__file__)
DESCRIPTION_FOLDER_NAME = "descriptions"
DESCRIPTION_PATH = os.path.join(NODE_FILE_PATH, DESCRIPTION_FOLDER_NAME)

# Ensure base folder exists
os.makedirs(DESCRIPTION_PATH, exist_ok=True)

def _ensure_example_exists():
    """Create examples/example.txt if there are no .txt files anywhere under descriptions."""
    for root, dirs, files in os.walk(DESCRIPTION_PATH):
        if any(f.endswith(".txt") for f in files):
            return
    example_dir = os.path.join(DESCRIPTION_PATH, "examples")
    os.makedirs(example_dir, exist_ok=True)
    placeholder_path = os.path.join(example_dir, "example.txt")
    if not os.path.exists(placeholder_path):
        with open(placeholder_path, 'w', encoding='utf-8') as f:
            f.write("Put your description files in subdirectories under 'descriptions'.")

# Create example once at import time if needed
_ensure_example_exists()

def list_all_description_files():
    """Return a sorted list of all .txt files relative to DESCRIPTION_PATH, including extension."""
    results = []
    for root, dirs, files in os.walk(DESCRIPTION_PATH):
        for file in files:
            if file.lower().endswith(".txt"):
                rel_dir = os.path.relpath(root, DESCRIPTION_PATH)
                if rel_dir == ".":
                    entry = file  # keep .txt extension so UI passes full name back
                else:
                    rel_dir_fixed = rel_dir.replace("\\", "/")
                    entry = rel_dir_fixed + "/" + file
                results.append(entry)
    if not results:
        _ensure_example_exists()
        return ["examples/example.txt"]
    return sorted(results)

class LoadDescriptionNode:
    @classmethod
    def INPUT_TYPES(cls):
        files = list_all_description_files()
        if not files:
            files = ["examples/example"]
        default_file = files[0]
        return {
            "required": {
                # Dropdown with all files
                "file_path": (files, {"default": default_file}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("description_text", "description_name")
    FUNCTION = "load_description"
    CATEGORY = "Feroc"

    @staticmethod
    def _abs_path(file_path: str) -> str:
        # Accept values with or without .txt and with either slash direction
        s = str(file_path).strip().replace("\\", "/")
        if s.endswith(".txt"):
            s = s[:-4]
        parts = [p for p in s.split("/") if p]
        return os.path.join(DESCRIPTION_PATH, *parts) + ".txt"

    @classmethod
    def IS_CHANGED(cls, file_path=None, **kwargs):
        """Re-execute when content changes based on mtime and size."""
        try:
            if not file_path or file_path == "undefined":
                files = list_all_description_files()
                file_path = files[0] if files else "examples/example.txt"
            abs_path = cls._abs_path(file_path)
            st = os.stat(abs_path)
            return f"{st.st_mtime_ns}:{st.st_size}"
        except Exception:
            return str(time.time())

    @staticmethod
    def _abs_path(file_path: str) -> str:
        parts = [p for p in str(file_path).split("/") if p]
        return os.path.join(DESCRIPTION_PATH, *parts)

    @classmethod
    def IS_CHANGED(cls, file_path=None, **kwargs):
        try:
            if not file_path or file_path == "undefined":
                files = list_all_description_files()
                file_path = files[0] if files else "examples/example.txt"
            abs_path = cls._abs_path(file_path)
            st = os.stat(abs_path)
            return f"{st.st_mtime_ns}:{st.st_size}"
        except Exception:
            return str(time.time())

    def load_description(self, file_path, **kwargs):
        if not file_path or file_path == "undefined":
            files = list_all_description_files()
            file_path = files[0] if files else "examples/example.txt"
        full_file_path = self._abs_path(file_path)
        try:
            with open(full_file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            name = os.path.splitext(os.path.basename(full_file_path))[0]
            return (text, name)
        except Exception as e:
            print(f"Error loading description from {full_file_path}: {e}")
            return ("", "")
