import os
import time

try:
    from .config import DESCRIPTION_PATH, TEXT_FILE_EXTENSION, FALLBACK_FILE
    from .file_utils import read_text_file, normalize_description_path
except ImportError:
    from config import DESCRIPTION_PATH, TEXT_FILE_EXTENSION, FALLBACK_FILE
    from file_utils import read_text_file, normalize_description_path

# Ensure base folder exists
os.makedirs(DESCRIPTION_PATH, exist_ok=True)


def _ensure_example_exists():
    """Create examples/example.txt if there are no .txt files anywhere under descriptions."""
    for root, dirs, files in os.walk(DESCRIPTION_PATH):
        if any(f.endswith(TEXT_FILE_EXTENSION) for f in files):
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
            if file.lower().endswith(TEXT_FILE_EXTENSION):
                rel_dir = os.path.relpath(root, DESCRIPTION_PATH)
                if rel_dir == ".":
                    entry = file  # keep .txt extension so UI passes full name back
                else:
                    rel_dir_fixed = rel_dir.replace("\\", "/")
                    entry = rel_dir_fixed + "/" + file
                results.append(entry)
    if not results:
        _ensure_example_exists()
        return [FALLBACK_FILE]
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
        return normalize_description_path(file_path)

    @staticmethod
    def _resolve_file_path(file_path: str) -> str:
        """Return file_path or fall back to the first available description file."""
        if not file_path or file_path == "undefined":
            files = list_all_description_files()
            return files[0] if files else FALLBACK_FILE
        return file_path

    @classmethod
    def IS_CHANGED(cls, file_path=None, **kwargs):
        """Re-execute when content changes based on mtime and size."""
        try:
            abs_path = cls._abs_path(cls._resolve_file_path(file_path))
            st = os.stat(abs_path)
            return f"{st.st_mtime_ns}:{st.st_size}"
        except Exception:
            return str(time.time())

    def load_description(self, file_path, **kwargs):
        full_file_path = self._abs_path(self._resolve_file_path(file_path))
        text = read_text_file(full_file_path)
        if not text and not os.path.exists(full_file_path):
            return ("", "")
        name = os.path.splitext(os.path.basename(full_file_path))[0]
        return (text, name)
