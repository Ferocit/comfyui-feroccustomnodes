import random

try:
    from .config import MAX_SEED, MAX_FILE_INPUTS
    from .file_utils import read_random_line
except ImportError:
    from config import MAX_SEED, MAX_FILE_INPUTS
    from file_utils import read_random_line


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

    def get_random_lines(self, seed: int, **kwargs) -> tuple[str]:
        """Select one random line from each provided text file.

        Returns:
            Tuple containing a single string with all selected lines joined by newline.
        """
        rng = random.Random(seed)
        file_paths = [kwargs.get(f'file_path_{i}') for i in range(1, MAX_FILE_INPUTS + 1)]
        selected_lines = []

        for path in file_paths:
            if path and path.strip():
                line = read_random_line(path, rng)
                if line is not None:
                    selected_lines.append(line)

        return ("\n".join(selected_lines),)
