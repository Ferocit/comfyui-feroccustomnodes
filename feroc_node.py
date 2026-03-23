import random

try:
    from .config import MAX_SEED, MAX_FILE_INPUTS
except ImportError:
    from config import MAX_SEED, MAX_FILE_INPUTS


class RandomLineFromText:
    @classmethod
    def INPUT_TYPES(cls):
        optional = {
            f"file_path_{i}": ("STRING", {"default": ""})
            for i in range(1, MAX_FILE_INPUTS + 1)
        }
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": MAX_SEED}),
            },
            "optional": optional,
        }

    CATEGORY = "Feroc"
    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_random_lines"

    def get_random_lines(self, seed, **kwargs):
        random.seed(seed)

        file_paths = [kwargs.get(f'file_path_{i}') for i in range(1, MAX_FILE_INPUTS + 1)]
        selected_lines = []

        for path in file_paths:
            if path and path.strip():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        lines = [line for line in f if line.strip()]
                    if lines:
                        selected_lines.append(random.choice(lines))
                except FileNotFoundError:
                    print(f"[RandomLineFromText] WARNING: File not found, skipping: {path}")
                except Exception as e:
                    print(f"[RandomLineFromText] WARNING: Error reading file {path}: {e}")

        return ("\n".join(selected_lines),)
