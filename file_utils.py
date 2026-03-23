"""File I/O utilities shared across ComfyUI Feroc custom nodes."""
import logging
import os
import random
from typing import Optional

try:
    from .config import DESCRIPTION_PATH, TEXT_FILE_EXTENSION, FALLBACK_FILE
except ImportError:
    from config import DESCRIPTION_PATH, TEXT_FILE_EXTENSION, FALLBACK_FILE

logger = logging.getLogger(__name__)


def read_text_file(path: str, encoding: str = 'utf-8') -> str:
    """Read a text file and return its content. Returns empty string on error."""
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        logger.warning("File not found: %s", path)
        return ""
    except OSError as e:
        logger.error("Error reading file %s: %s", path, e)
        return ""


def read_random_line(path: str, rng: random.Random) -> Optional[str]:
    """Return a random non-empty line from a file. Returns None if file is empty or missing."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f if line.strip()]
        if lines:
            return rng.choice(lines)
        logger.warning("No non-empty lines found in: %s", path)
        return None
    except FileNotFoundError:
        logger.warning("File not found, skipping: %s", path)
        return None
    except OSError as e:
        logger.error("Error reading file %s: %s", path, e)
        return None


def _ensure_example_exists() -> None:
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


def list_all_description_files() -> list[str]:
    """Return a sorted list of all .txt files relative to DESCRIPTION_PATH, including extension."""
    results = []
    for root, dirs, files in os.walk(DESCRIPTION_PATH):
        for file in files:
            if file.lower().endswith(TEXT_FILE_EXTENSION):
                rel_dir = os.path.relpath(root, DESCRIPTION_PATH)
                if rel_dir == ".":
                    entry = file
                else:
                    rel_dir_fixed = rel_dir.replace("\\", "/")
                    entry = rel_dir_fixed + "/" + file
                results.append(entry)
    if not results:
        _ensure_example_exists()
        return [FALLBACK_FILE]
    return sorted(results)


def normalize_description_path(file_path: str) -> str:
    """Normalize a file path relative to DESCRIPTION_PATH, appending .txt extension."""
    s = str(file_path).strip().replace("\\", "/")
    if s.endswith(TEXT_FILE_EXTENSION):
        s = s[:-len(TEXT_FILE_EXTENSION)]
    parts = [p for p in s.split("/") if p]
    return os.path.join(DESCRIPTION_PATH, *parts) + TEXT_FILE_EXTENSION
