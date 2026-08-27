"""ComfyUI custom node for scaling width/height to a target megapixel count."""
import math

ROUND_TO_MULTIPLE = 8


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
        """Scale width/height to the target megapixel count, preserving aspect ratio.

        Results are rounded to the nearest multiple of 8 for compatibility with
        diffusion models that require dimensions divisible by 8.
        """
        target_pixels = megapixels * 1_000_000
        scale_factor = math.sqrt(target_pixels / (width * height))

        new_width = self._round_to_multiple(width * scale_factor)
        new_height = self._round_to_multiple(height * scale_factor)

        return (new_width, new_height)

    @staticmethod
    def _round_to_multiple(value: float, multiple: int = ROUND_TO_MULTIPLE) -> int:
        return max(multiple, round(value / multiple) * multiple)
