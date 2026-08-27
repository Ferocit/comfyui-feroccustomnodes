"""ComfyUI custom node for scaling width/height to a target megapixel count."""
import math


class MegapixelScaleNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 1, "max": 1_000_000}),
                "height": ("INT", {"default": 512, "min": 1, "max": 1_000_000}),
                "megapixels": ("FLOAT", {"default": 1.0, "min": 0.01, "max": 100.0, "step": 0.01}),
            },
        }

    CATEGORY = "Feroc"
    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("width", "height")
    FUNCTION = "scale"

    def scale(self, width: int, height: int, megapixels: float) -> tuple[int, int]:
        """Scale width/height to the target megapixel count, preserving aspect ratio."""
        target_pixels = megapixels * 1_000_000
        scale_factor = math.sqrt(target_pixels / (width * height))

        new_width = max(1, round(width * scale_factor))
        new_height = max(1, round(height * scale_factor))

        return (new_width, new_height)
