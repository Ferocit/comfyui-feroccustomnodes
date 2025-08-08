import random

class RandomLineFromText:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
            },
            "optional": {
                "file_path_1": ("STRING", {"default": ""}),
                "file_path_2": ("STRING", {"default": ""}),
                "file_path_3": ("STRING", {"default": ""}),
                "file_path_4": ("STRING", {"default": ""}),
                "file_path_5": ("STRING", {"default": ""}),
            }
        }

    CATEGORY = "Feroc"
    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_random_lines"

    def get_random_lines(self, seed, **kwargs):
        random.seed(seed)
        
        file_paths = [kwargs.get(f'file_path_{i}') for i in range(1, 6)]
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
