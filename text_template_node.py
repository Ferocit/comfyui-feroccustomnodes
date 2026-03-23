"""ComfyUI custom node for filling {placeholder} templates from wired string inputs."""
import logging
from collections import defaultdict

try:
    from .config import MAX_FILE_INPUTS
except ImportError:
    from config import MAX_FILE_INPUTS

logger = logging.getLogger(__name__)


class TextTemplateNode:
    @classmethod
    def INPUT_TYPES(cls):
        optional = {}
        for i in range(1, MAX_FILE_INPUTS + 1):
            optional[f"key_{i}"]   = ("STRING", {"default": ""})
            optional[f"value_{i}"] = ("STRING", {"default": "", "multiline": True})
        return {
            "required": {
                "template": ("STRING", {"default": "{subject} in {setting}", "multiline": True}),
            },
            "optional": optional,
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filled_template",)
    FUNCTION = "fill_template"
    CATEGORY = "Feroc"

    def fill_template(self, template: str, **kwargs) -> tuple[str]:
        """Fill {placeholder} tokens in template with the provided key/value pairs.

        Unknown placeholders are left intact. Malformed templates (e.g. unclosed braces)
        return the original template unchanged.
        """
        substitutions = {}
        for i in range(1, MAX_FILE_INPUTS + 1):
            key = kwargs.get(f"key_{i}", "")
            if key and key.strip():
                substitutions[key.strip()] = kwargs.get(f"value_{i}", "")

        class _PassthroughDict(defaultdict):
            def __missing__(self, key):
                return "{" + key + "}"

        try:
            result = template.format_map(_PassthroughDict(None, substitutions))
        except (ValueError, KeyError) as e:
            logger.warning("Template substitution error: %s", e)
            result = template

        return (result,)
