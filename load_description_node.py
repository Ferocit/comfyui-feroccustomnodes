import os
import time

try:
    from .config import DESCRIPTION_PATH, FALLBACK_FILE
    from .file_utils import read_text_file, normalize_description_path, list_all_description_files, _ensure_example_exists
except ImportError:
    from config import DESCRIPTION_PATH, FALLBACK_FILE
    from file_utils import read_text_file, normalize_description_path, list_all_description_files, _ensure_example_exists

# Ensure base folder exists
os.makedirs(DESCRIPTION_PATH, exist_ok=True)

# Create example once at import time if needed
_ensure_example_exists()


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

    def load_description(self, file_path: str, **kwargs) -> tuple[str, str]:
        """Load description text from the given file path.

        Returns:
            Tuple of (file content, filename without extension). Returns ('', '') on error.
        """
        full_file_path = self._abs_path(self._resolve_file_path(file_path))
        text = read_text_file(full_file_path)
        if not text and not os.path.exists(full_file_path):
            return ("", "")
        name = os.path.splitext(os.path.basename(full_file_path))[0]
        return (text, name)
